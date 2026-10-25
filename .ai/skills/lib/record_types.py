"""The record types, facts, closed sets, Basic Tables and construct keys the specs declare, and the parts a
citation names: what the construct checks read before they run, read here once for every skill's script that runs them
(specs/methodology/skills.md § Authoring a Skill). declared_types fills TYPES; the checks then read it.

The one reader of a block of fields is here too: every script reads where a block of fields, a field's value, a field's
list, a record and a nested record begin and end through read_block and read_item, as modeling-constructs.md § Fields
states them once."""
import re

import constructs
import layout
from spec_text import RECORD_SELECTOR, resolve, sections, strip_fences

CITATION = constructs.CITATION  # the form written once, in constructs.py


# modeling-constructs.md § Constructs § Record Form: every record type is read from its declaration, by declared_types,
# the canon's own among them; the checks hold no copy of one. A type's own placement is audit-specs' to carry out.
RECORD_FORM = "modeling-constructs.md § Constructs § Record Form"


# @canon-spec specs/methodology/modeling-constructs.md § Fields
# the rule the reader's checks name: a block's backslashes and a field's list's indentation
FIELDS = "modeling-constructs.md § Fields"


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact
# @canon-spec specs/methodology/spec-placement.md § Open Question
# the homes of the types a rule of the checks reads by their declaration: the Fact type, whose Plural Name titles a
# file's Facts sections, the types whose record section is its file's last top-level section, and the types whose
# records' Impacts each carry a section citation
FACT_HOME = "specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact"


LAST_TOP_LEVEL = ("specs/methodology/spec-placement.md § Open Question",)


FIELD_LINE = constructs.FIELD  # the form written once, in constructs.py


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Construct
# a Values cell holding a list of records of a cited type: `a list of` and the citation of the type's definition
LIST_OF = re.compile(r"^a list of (?P<cite>`[^`]+`)$")


# ---------------------------------------------------------------- the one reader of a block of fields

def _indent(line):
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip(" "))


def opens_key(line):
    """-> the FIELD match where the line opens a field's key, its first characters after its indentation the key in
    bold, so a record's first line, opening with a list marker, is none; else None."""
    m = FIELD_LINE.match(line)
    return m if m and not m["marker"] else None


def _is_item(line):
    """Whether a line is a list item whose marker is a hyphen and a space, a record's or a plain item's."""
    return re.match(r"^\s*-\s+\S", line) is not None or re.match(r"^\s*-\s*$", line) is not None


def _strip_break(line):
    """-> (the line's text without the space and the backslash ending it, whether it ended with a backslash, whether
    exactly one space stood before it)."""
    stripped = line.rstrip()
    if not stripped.endswith("\\"):
        return stripped, False, False
    body = stripped[:-1]
    return body.rstrip(), True, body.endswith(" ") and not body.endswith("  ") and len(body.rstrip()) < len(body)


def _next_nonblank(lines, j, end):
    while j < end and not lines[j].strip():
        j += 1
    return j


def _own_line(lines, i, end, problems, consumed):
    """A line of a block of fields, a key line or one continuing a value: -> its text without the backslash, after
    checking that it ends with one space and a backslash exactly where a line opening a field's key directly follows."""
    text, had, one_space = _strip_break(lines[i])
    follows = i + 1 < end and opens_key(lines[i + 1]) is not None
    if follows and not (had and one_space):
        problems.append((FIELDS, i, "a line of a block of fields that a line opening a field's key directly follows, ending with no backslash or with other than one space before it"))
    elif not follows and had:
        problems.append((FIELDS, i, "a backslash ending a line of a block of fields that no line opening a field's key follows"))
    if consumed is not None:
        consumed.add(i)
    return text


def read_item(lines, i, end=None, problems=None, consumed=None):
    """-> an item of a field's list opening at line i: {"line", "indent", "text_indent", "lines", "text", "fields"},
    its fields read as a block where it opens a field's key, a record, and None where it is a plain item, whose text
    is its first line's content. The item ends before the first line that is not blank and is indented less than its
    text (modeling-constructs.md § Fields)."""
    end = len(lines) if end is None else end
    problems = [] if problems is None else problems
    raw = lines[i]
    indent = _indent(raw)
    m = re.match(r"^(\s*)(-\s*)", raw)
    marker = len(m.group(2)) if m else 2
    text_indent = indent + marker
    item = {"line": i, "indent": indent, "text_indent": text_indent, "lines": [i], "text": None, "fields": None}
    f = FIELD_LINE.match(raw)
    if f and f["marker"]:
        fields, j = read_block(lines, i, text_indent, end, problems, consumed, first=True)
        item["fields"] = fields
        item["lines"] = list(range(i, j))
        return item, j
    item["text"] = _strip_break(raw)[0][text_indent:].strip() if len(raw) >= text_indent else raw.strip()[marker:].strip()
    if consumed is not None:
        consumed.add(i)
    j = i + 1
    while j < end:
        if not lines[j].strip():
            k = _next_nonblank(lines, j, end)
            if k < end and _indent(lines[k]) >= text_indent:
                item["lines"] += list(range(j, k))
                j = k
                continue
            break
        if _indent(lines[j]) < text_indent:
            break
        item["lines"].append(j)
        if consumed is not None:
            consumed.add(j)
        j += 1
    return item, j


def read_block(lines, i, indent, end=None, problems=None, consumed=None, first=False):
    """modeling-constructs.md § Fields: the one reader of a block of fields. Reads the fields standing at `indent` from
    line i, a line opening a field's key, or a record's first line where `first` is given: each field's key, its value
    running to the next line opening a field's key or to the block's end, each line between continuing it, without the
    space and the backslash ending a line, and the list beneath a key, its items at the key's indentation or beyond,
    each item ending before the first line that is not blank and is indented less than its text. A list or a table
    ends the block's paragraph, and a field opening the next paragraph is the block's. -> ([field], the line after the
    block), each field {"key", "value", "line", "lines", "items", "inline"}; the reader's checks are appended to
    `problems` as (rule, 0-based line, message), and the lines read to `consumed`."""
    end = len(lines) if end is None else end
    problems = [] if problems is None else problems
    fields = []
    j = i
    while j < end:
        line = lines[j]
        if not line.strip():
            k = _next_nonblank(lines, j, end)
            m = opens_key(lines[k]) if k < end else None
            if m and _indent(lines[k]) == indent:
                j = k
                continue
            break
        m = FIELD_LINE.match(line)
        if not m or (m["marker"] and not (first and j == i)) or (_indent(line) != indent and not (first and j == i)):
            break
        text = _own_line(lines, j, end, problems, consumed)
        value_text = FIELD_LINE.match(text)
        field = {"key": m["key"], "value": ((value_text["value"] if value_text else m["value"]) or "").strip(),
                 "line": j, "lines": [j], "items": None, "inline": bool((m["value"] or "").strip())}
        fields.append(field)
        j += 1
        # the value's continuation lines, then the list beneath the key
        while j < end:
            line = lines[j]
            if not line.strip():
                k = _next_nonblank(lines, j, end)
                if k < end and _is_item(lines[k]) and _indent(lines[k]) >= indent and (field["items"] or not opens_key(lines[k])):
                    j = k
                    continue
                break
            if _is_item(line) and _indent(line) >= indent:
                item, j = read_item(lines, j, end, problems, consumed)
                if field["items"] is None:
                    field["items"] = []
                if item["indent"] != indent + 2:  # each item of the list, not its first alone
                    problems.append((FIELDS, item["line"], f"a field's list whose items stand other than two spaces beyond its key: {field['key']}"))
                field["items"].append(item)
                continue
            if field["items"] is not None or _indent(line) < indent or opens_key(line) or line.lstrip().startswith(("|", "#", "```")):
                break
            field["value"] = (field["value"] + " " + _own_line(lines, j, end, problems, consumed).strip()).strip()
            field["lines"].append(j)
            j += 1
        first = False
    return fields, j


def record_of(item):
    """-> a record as the checks read one, [(key, value, 0-based line)], from an item opening a field's key: a field
    holding records gives them as a list of records, and a field holding plain items the items' texts, one to a line."""
    out = []
    for f in item["fields"]:
        out.append((f["key"], value_of(f), f["line"]))
    return out


def value_of(field):
    """-> a field's value: its text, or, beneath its key, its records as a list of records, or its plain items' texts
    one to a line, after any text on its key's line."""
    if field["items"] is None:
        return field["value"]
    if any(it["fields"] is not None for it in field["items"]):
        return [record_of(it) if it["fields"] is not None else [(None, it["text"], it["line"])] for it in field["items"]]
    items = "\n".join(it["text"] for it in field["items"])
    return (field["value"] + "\n" + items) if field["value"] else items


def block_findings(text, offset=0, consumed=None):
    """modeling-constructs.md § Fields: the reader's checks over every block of fields a file holds, a record's among
    them, a fenced `markdown` block's Markdown read as a file of its own -> [(rule, 1-based line, message)]."""
    lines = strip_fences(text.replace("\r\n", "\n")).split("\n")
    problems, consumed = [], set() if consumed is None else consumed
    i = 0
    while i < len(lines):
        if i in consumed or not lines[i].strip():
            i += 1
            continue
        line = lines[i]
        if opens_key(line):
            _, i = read_block(lines, i, _indent(line), len(lines), problems, consumed)
            continue
        f = FIELD_LINE.match(line)
        if f and f["marker"]:
            _, i = read_item(lines, i, len(lines), problems, consumed)
            continue
        i += 1
    out = [(rule, line + 1 + offset, msg) for rule, line, msg in problems]
    for start, _, inner in layout.markdown_blocks(text):
        out += block_findings(inner, offset + start + 1)
    return out


# ---------------------------------------------------------------- the record types the specs declare

def derive(spec, holds=None):
    """A type's fields, its identifying fields, its Reference Key, and its unique, required, defaulted, listed and
    record-holding fields, from its tables; `holds` resolves a Values cell citing a record type's definition to
    (the type's Plural Name, whether the field holds a list) or None."""
    spec["fields"] = [f for f, _, _, _, _ in spec["table"]]
    spec["identifying"] = list(spec["key"])
    spec["unique"] = [f for f, unique, _, _, _ in spec["table"] if unique == "yes"]
    spec["required"] = [f for f, _, req, _, _ in spec["table"] if req == "yes"]
    spec["defaults"] = {f: d for f, _, _, d, _ in spec["table"] if d}
    # modeling-constructs.md § Constructs § Record Form: a field's values, where its Values cell lists them
    spec["values"] = {f: constructs.quoted_values(v) for f, _, _, _, v in spec["table"]
                      if constructs.quoted_values(v) is not None}
    # a field whose Values cite a record type's definition holds its records, one or a list; a field whose Values cite
    # a closed set's record section takes its values from that set's members
    spec["holds"] = {}
    for f, _, _, _, v in spec["table"]:
        held = holds(f, v) if holds else None
        if held:
            spec["holds"][f] = held
    spec["cited"] = {f: v for f, _, _, _, v in spec["table"] if constructs.CITED_SET.fullmatch(v) and f not in spec["holds"]}
    # its section fields, each row's Field, Required, Default Value and Values
    sec = spec.get("section_table", ())
    spec["section_required"] = [f for f, req, _, _ in sec if req == "yes"]
    spec["section_defaults"] = {f: d for f, _, d, _ in sec if d}
    spec["section_values"] = {f: constructs.quoted_values(v) for f, _, _, v in sec if constructs.quoted_values(v) is not None}
    return spec


# every record type the specs declare, by its Plural Name, filled by declared_types before the checks run
TYPES = {}


# the record types a fenced `markdown` block declares, by the block's own path and the type's Plural Name, each
# reaching that block alone (modeling-constructs.md § Constructs § Record Form)
BLOCK_TYPES = {}


_TEXT_OF = {}


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
# @canon-spec specs/methodology/spec-placement.md § Environments
FIELD_KEYS = {"Kind": "environment",
              **{f: {"Diagrams": "diagram", "Record Form #2": "record section"}.get(c, "construct") for f, c, _, _ in constructs.FIELD_TABLE}}


# a citation's `Key: value`, its key a field label, constructs.py's one copy of the form, or a table's name and its key's,
# joined by a dot, where its construct has more than one keyed table (modeling-constructs.md § Constructs § Keyed Construct)
KEY_VALUE = re.compile(rf'^({constructs.LABEL}(?: {constructs.LABEL})*(?:\.{constructs.LABEL}(?: {constructs.LABEL})*)*): (.+)$')


def block_path(r, start):
    """-> the path a fenced `markdown` block is read by: its file's path, a hash and the 1-based line of its fence."""
    return f"{r}#L{start + 1}"


def type_of(title, r):
    """modeling-constructs.md § Constructs § Record Form: the record type a section titled `title` holds in file `r`,
    one whose Plural Name it is and whose records may sit there, a canon type's in any file under specs/, an application spec's
    type's in the application specs, and a fenced `markdown` block's in that block alone; or None."""
    if r in BLOCK_TYPES and title in BLOCK_TYPES[r]:
        return BLOCK_TYPES[r][title]
    spec = TYPES.get(title)
    return spec if spec and r is not None and r.split("#L")[0].startswith(spec["reach"]) else None


def _raw_type(r, line, fields, tables, lineage, reach):
    values = dict((k, v) for _, k, v in fields)
    rec = [t for t in tables if t["header"] == constructs.RECORD_FIELDS]
    sec = [t for t in tables if t["header"] == constructs.SECTION_FIELDS]
    home = f"{r} § {lineage}"
    return {"table": tuple(tuple(row[:5]) for _, row in rec[0]["rows"] if len(row) == 6),
            "key": [k.strip() for k in values.get("Reference Key", "").split(",") if k.strip()],
            "section_table": tuple(tuple(row[:4]) for _, row in sec[0]["rows"] if len(row) == 5) if sec else (),
            "home": home, "last_top_level": home in LAST_TOP_LEVEL, "declared": (r, line),
            "reach": reach, "extends": values.get("Extends", "none")}


def _resolve_types(raw, out, report=True):
    """Each type's chain of bases read once, its fields and its Reference Key its own or its base's, and each field
    holding records resolved to the type it cites; -> {plural: spec}, the problems appended to out where reported."""
    by_home = {spec["home"]: p for p, spec in raw.items()}

    def base_of(p):
        e, r = raw[p]["extends"], raw[p]["declared"][0]
        cites = CITATION.findall(e) if e != "none" else []
        return by_home.get(" § ".join(resolve(cites[0], r))) if len(cites) == 1 else None

    def chain(p, seen=()):
        b = base_of(p)
        return (chain(b, seen + (p,)) if b and b not in seen + (p,) else ()) + (p,)
    own = {p: (spec["table"], spec["section_table"], spec["key"]) for p, spec in raw.items()}
    done = {}
    for p, spec in raw.items():
        types = chain(p)
        spec["table"] = tuple(row for t in types for row in own[t][0])
        # each field with the file declaring it, where a citation in its Values resolves
        spec["origin"] = {row[0]: raw[t]["declared"][0] for t in types for row in own[t][0]}
        # its Reference Key, its own or its nearest base's, of fields it gives and requires
        spec["key"] = next((own[t][2] for t in reversed(types) if own[t][2]), [])
        required = {row[0]: row[2] for row in spec["table"]}
        for k in spec["key"] if len(types) > 1 else []:
            if required.get(k) != "yes" and report:
                out.append((RECORD_FORM, *spec["declared"], f"a Reference Key naming a field the type does not give or does not require: {k}"))
        spec["section_table"] = tuple(row for t in types for row in own[t][1])
        spec["section_fields"] = [row[0] for row in spec["section_table"]]
        names = [row[0] for row in spec["table"]] + spec["section_fields"]
        for f in sorted({f for f in names if names.count(f) > 1}):
            if report:
                out.append((RECORD_FORM, *spec["declared"], f"a field a record type and its base both name: {f}"))

        def holds(field, cell, spec=spec):
            # a citation of a record type's definition, alone or after `a list of`, names the section declaring a type
            m = LIST_OF.match(cell.strip())
            cite = m["cite"] if m else cell.strip()
            if not CITATION.fullmatch(cite) or "[" in cite:
                return None
            origin = spec["origin"].get(field, spec["declared"][0])
            target = " § ".join(resolve(CITATION.findall(cite)[0], origin))
            held = by_home.get(target)
            return (held, m is not None) if held else None
        done[p] = derive(spec, holds)
    return done


def declared_types(text_of):
    """modeling-constructs.md § Constructs § Record Form: each record type a Record Form declares under specs/, by its
    Plural Name, read from its declaration, a type extending another holding its base's fields first; each added to TYPES
    and its fields' keys to FIELD_KEYS, and the closed-set resolver set. The types a fenced `markdown` block declares
    are read too, each reaching that block alone and none of their declarations' findings reported. -> the
    declarations' own findings: a defining section titled other than with the type's name, bare; a Plural Name two
    types share; a field a type and its base both name; a Reference Key naming a field the type does not give or
    does not require; and a type holding itself through fields whose Required is yes."""
    out, raw = [], {}
    # the canon's declarations first, so a type sharing a canon type's Plural Name is the one reported
    for r, body in sorted(text_of.items(), key=lambda kv: (not kv[0].startswith("specs/methodology/"), kv[0])):
        if not r.startswith("specs/"):
            continue
        for line, name, fields, tables, lineage in constructs.declarations(strip_fences(body), sections(body)):
            values = dict((k, v) for _, k, v in fields)
            plural = values.get("Plural Name", "").strip()
            rec = [t for t in tables if t["header"] == constructs.RECORD_FIELDS]
            if name != "Record Form" or not plural or not rec:
                continue  # its form is the construct check's to report
            title = lineage.split(" § ")[-1]
            if re.match(r"(?:A|An) ", title) or title == plural:
                out.append((RECORD_FORM, r, line, f"a record type's section titled other than with the type's name, bare: {title}"))
            if plural in raw:
                out.append((RECORD_FORM, r, line, f"a Plural Name another record type declares: {plural}"))
                continue
            raw[plural] = _raw_type(r, line, fields, tables, lineage,
                                    "specs/application/" if r.startswith("specs/application/") else "specs/")
    for p, spec in _resolve_types(raw, out).items():
        TYPES[p] = spec
        for key in spec["fields"]:
            FIELD_KEYS.setdefault(key, "record")
        for key in spec["section_fields"]:
            FIELD_KEYS.setdefault(key, "record section")
    out += _self_holding_findings(TYPES)
    # the types a fenced `markdown` block declares, read with the canon's, each reaching the block alone
    for r, body in sorted(text_of.items()):
        if not r.startswith("specs/"):
            continue
        for start, _, inner in layout.markdown_blocks(body):
            path = block_path(r, start)
            _TEXT_OF[path] = inner
            block_raw = {}
            for line, name, fields, tables, lineage in constructs.declarations(strip_fences(inner), sections(inner)):
                values = dict((k, v) for _, k, v in fields)
                plural = values.get("Plural Name", "").strip()
                if name != "Record Form" or not plural or not [t for t in tables if t["header"] == constructs.RECORD_FIELDS] or plural in block_raw:
                    continue
                block_raw[plural] = _raw_type(path, line, fields, tables, lineage, path)
            if block_raw:
                BLOCK_TYPES[path] = _resolve_types(block_raw, [], report=False)
                for spec in BLOCK_TYPES[path].values():
                    for key in spec["fields"]:
                        FIELD_KEYS.setdefault(key, "record")
    _TEXT_OF.update(text_of)
    constructs.CLOSED_SET = closed_set
    constructs.FACTS_SECTION = next((p for p, spec in TYPES.items() if spec["home"] == FACT_HOME), None)
    constructs.READ_FACT = read_fact
    return out


def _self_holding_findings(types):
    """modeling-constructs.md § Constructs § Record Form: a type holding itself through fields whose Required is yes,
    its own or through other types' in turn, each citing a record type's definition, since no record could end its
    nesting -> findings at each such type's declaration."""
    out = []
    edges = {p: {held for f, (held, _) in spec["holds"].items() if f in spec["required"]} for p, spec in types.items()}

    def reaches(start, p, seen):
        for q in edges.get(p, ()):
            if q == start or (q not in seen and reaches(start, q, seen | {q})):
                return True
        return False
    for p, spec in types.items():
        if reaches(p, p, {p}):
            out.append((RECORD_FORM, *spec["declared"], f"a record type holding itself through fields whose Required is yes: {p}"))
    return out


def closed_set(body, cell, host=None):
    """modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact: the identifying values of the members of the
    closed set a Facts record's Values cites, the records of its record section, of a type identifying them by one field,
    or the rows of its Basic Table keyed by one column, or None where it cites no such section; `host` the path the
    citing text is read by, a fenced block's own among them."""
    cites = CITATION.findall(cell)
    if len(cites) != 1 or "[" in cites[0]:
        return None
    path, target = resolve(cites[0], None)
    text = body if path is None else _TEXT_OF.get(path)
    title = target.split(" § ")[-1]
    # a section of another file read as the type reaching that file; one of the citing file read by its title's type,
    # record_findings reporting it where that type's records may not sit
    spec = type_of(title, path) if path else (type_of(title, host) if host else TYPES.get(title))
    if text is not None and target in sections(text) and not spec:
        # a closed set kept as a Basic Table keyed by one column, its members that column's values
        keyed = [t for t in basic_tables(text).get(target, []) if len(t["key"]) == 1 and t["key"][0] in t["header"]]
        if len(keyed) == 1:
            i = keyed[0]["header"].index(keyed[0]["key"][0])
            return [row[i] for _, row in keyed[0]["rows"] if i < len(row)]
    if text is None or target not in sections(text) or not spec or len(spec["identifying"]) != 1:
        return None
    records, _ = parse_records(text, target, spec["section_fields"])
    return [v for rec in records for k, v, _ in rec if k == spec["identifying"][0]]


def read_fact(host, cite, name):
    """modeling-constructs.md § Constructs § Decision Table: the Facts record a Reads item cites, in its file or another,
    -> (Type, Values, May Be Absent), or None where it cites none."""
    path, target = resolve(cite, host)
    text = _TEXT_OF.get(path)
    if text is None or target not in sections(text):
        return None
    for _, n, d in constructs.fact_records(strip_fences(text), {target: sections(text)[target]}):
        if n == name:
            return constructs.facts_of([(0, n, d)])[n]
    return None


def closed_set_findings(text_of):
    """modeling-constructs.md § Constructs § Record Form: a closed set's records sit in the one record section a Values
    cites, a fact's or a field's; another section of its type holding records where they may sit is reported, and so is
    a field whose Values cite the definition of the set's type, since a field naming a member cites the set's section."""
    out, homes = [], {}
    for r, body in text_of.items():
        if not r.startswith("specs/"):
            continue
        for _, _, d in constructs.fact_records(strip_fences(body), sections(body)):
            if d.get("cited"):
                path, target = resolve(CITATION.findall(d["cited"])[0], r)
                homes[(path, target)] = target.split(" § ")[-1]
    for spec in TYPES.values():
        for f, cell in spec["cited"].items():
            path, target = resolve(CITATION.findall(cell)[0], spec["origin"].get(f, spec["declared"][0]))
            homes[(path, target)] = target.split(" § ")[-1]
    closed = set()
    for (path, target), title in homes.items():
        spec = type_of(title, path)
        if not spec:
            continue
        closed.add(title)
        for r, body in text_of.items():
            if not r.startswith(spec["reach"]):
                continue
            live = strip_fences(body).split("\n")
            for lineage, (h, end) in sections(body).items():
                if lineage.split(" § ")[-1] == title and (r, lineage) != (path, target) and any(opens_key(l) and opens_key(l)["key"] == "Records" for l in live[h + 1:end]):
                    out.append((RECORD_FORM, r, h + 1, f"a second record section of the closed set {path} § {target}"))
    for p, spec in TYPES.items():
        for f, (held, _) in spec["holds"].items():
            if held in closed:
                out.append((RECORD_FORM, *spec["declared"], f"a field whose Values cite the definition of a type whose record section a Values cites, the set's home, where a field naming a member cites that section: {f}"))
    return out


def parse_records(body, lineage, section_keys=()):
    """modeling-constructs.md § Constructs § Record Form: a record section's records, read through the one reader.

    -> (records, problems): each record a list of (key, value, line) in the order written, a field holding records
    giving them as a list of records and a field holding plain items their texts one to a line; each problem (rule,
    0-based line, message). A record section holds only fields: an optional Diagrams list, then the section fields
    its type declares, then Records, whose value is one list item per record.
    """
    lines = body.split("\n")
    h, end = sections(body)[lineage]
    while end > h + 1 and lines[end - 1].strip() in ("", "---"):
        end -= 1
    problems, records = [], []
    k = _next_nonblank(lines, h + 1, end)
    fields, j = read_block(lines, k, 0, end, problems) if k < end and opens_key(lines[k]) and _indent(lines[k]) == 0 else ([], k)
    keys = [f["key"] for f in fields]
    if fields and fields[0]["key"] == "Diagrams":
        cites = []
        for it in fields[0]["items"] or []:
            mm = re.fullmatch(r'`([^`]+)`', it["text"] or "") if it["fields"] is None else None
            if mm:
                cites.append(mm.group(1))
            else:
                problems.append((RECORD_FORM, it["line"], "a Diagrams bullet is not one citation"))
        if not cites:
            problems.append((RECORD_FORM, h, "a record section's Diagrams field lists no diagram"))
        elif cites != sorted(cites):
            problems.append((RECORD_FORM, h, "a record section's Diagrams list is not sorted"))
    elif "Diagrams" in keys:
        problems.append((RECORD_FORM, fields[keys.index("Diagrams")]["line"], "a record section's Diagrams field standing after another field"))
    if "Records" not in keys or keys[-1] != "Records":
        problems.append((RECORD_FORM, h, "a record section does not hold its records under **Records:**"))
        return records, problems
    recs = fields[-1]
    if recs["inline"]:
        problems.append((RECORD_FORM, recs["line"], "a record section's Records written on its key's line, not beneath it"))
    for it in recs["items"] or []:
        if it["fields"] is None:
            problems.append((RECORD_FORM, it["line"], "a record does not open with a field"))
            continue
        records.append(record_of(it))
    k = _next_nonblank(lines, j, end)
    if k < end:
        problems.append((RECORD_FORM, k, "a record section holds something other than its fields"))
    if not records:
        problems.append((RECORD_FORM, h, "a record section holds no record"))
    return records, problems


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Keyed Construct
# a part of a construct is named by its construct's section and its key, the column its construct's definition
# declares in a Reference Key field, read from the canon before any citation: {construct: {key, ...}}
CONSTRUCT_KEYS = {}


# the (path, lineage) of each construct a part's citation by Name names, from outside its section
NAME_CITED = set()


def construct_keys(text_of):
    """modeling-constructs.md § Constructs § Keyed Construct: each construct's Reference Key, read from its definition's section, one
    column or a list's items, one to a keyed table in the order its tables come, each the table and its column joined by a
    dot, the place's name the path's own and the column one of that place's table ->
    CONSTRUCT_KEYS {construct: {key: its table's index, or None for every table}}."""
    out, home = [], "specs/methodology/modeling-constructs.md"
    body = strip_fences(text_of.get(home, ""))
    lines = body.split("\n")
    for lineage, (h, end) in sections(body).items():
        parts = lineage.split(" § ")
        if len(parts) != 2 or parts[0] != "Constructs" or parts[1] not in constructs.FORMS:
            continue
        i = next((k for k in range(h + 1, end) if opens_key(lines[k]) and opens_key(lines[k])["key"] == "Reference Key" and _indent(lines[k]) == 0), None)
        if i is None:
            continue
        fields, _ = read_block(lines, i, 0, end)
        field = fields[0]
        if field["value"]:
            CONSTRUCT_KEYS[parts[1]] = {field["value"]: None}
            continue
        items = [it["text"] for it in field["items"] or [] if it["fields"] is None]
        forms = constructs.FORMS[parts[1]]

        def keyed(k, item):
            levels = item.strip().split(".")
            return len(levels) == 2 and levels[-1] in (forms[k] or []) + ["Name"]
        if not items or len(items) != len(forms) or any(not KEY_VALUE.match(it.strip() + ": x") or not keyed(k, it) for k, it in enumerate(items)):
            out.append((constructs.KEYED, home, i + 1, f"a construct's definition whose Reference Key is empty, or a list not giving, for each of its tables, a path to one of its columns: {parts[1]}"))
            continue
        CONSTRUCT_KEYS[parts[1]] = {it.strip(): k for k, it in enumerate(items)}
    return out


def part_citation(sel, path, target, text_of, r, line, found):
    """sourcing-and-citation.md § Writing a Citation: a part's citation names one identifier
    of the construct its section declares, and a part of that construct holds it."""
    rule = "sourcing-and-citation.md § Writing a Citation"
    body = text_of[path]
    declared = [d for d in constructs.declarations(strip_fences(body), sections(body)) if d[4] == target]
    keyed = [t for t in basic_tables(body).get(target, []) if t["key"]]
    cols = [(KEY_VALUE.match(p.strip()) or re.match(r'()', '')).group(1) for p in sel.split("; ")]
    named = cols[0].split(".")[0] if "." in cols[0] else None
    # the Basic Table the citation's path or its key's columns name, where it names no construct's key
    own = {k.split(".")[-1] for k in CONSTRUCT_KEYS.get(declared[0][1], {})} if declared else set()
    picked = [t for t in keyed if (t["name"] == named if named else t["key"] == cols and not t["name"])]
    if keyed and (not declared or picked or cols[0].split(".")[-1] not in own):
        if len(picked) != 1:
            found.append((rule, r, line, f"a row citation naming no one table its section holds by its path or its key's columns: § {target} [{sel}]"))
        else:
            row_citation(sel, target, picked[0], r, line, found)
        return
    if not declared:
        found.append((rule, r, line, f"a bracket on a section that is no record section, declares no construct and holds no Basic Table declaring a Reference Key: § {target}"))
        return
    _, construct, _, tables, _ = declared[0]
    cited_value_findings(sel, r, line, found)
    m = KEY_VALUE.match(sel.strip())
    keys = CONSTRUCT_KEYS.get(construct, {})
    key = m.group(1) if m else None
    # a key its construct names by its table, written alone, is read so in the application specs alone until they are
    # migrated (modeling-constructs.md § Constructs § Keyed Construct)
    if m and key not in keys and r.startswith("specs/application/"):
        key = next((k for k in keys if k.endswith("." + key)), key)
    if not m or key not in keys or ";" in sel:
        found.append((rule, r, line, f"a part citation not written as one key a {construct} has: [{sel}]"))
        return
    column, value = key.split(".")[-1], m.group(2).strip()
    k = keys[key]
    values = [row[t["header"].index(column)] for t in (tables if k is None else tables[k:k + 1])
              if column in t["header"]
              for _, row in t["rows"] if len(row) == len(t["header"])]
    if not [v for v in values if v == value]:
        found.append((rule, r, line, f"a part citation matches no part: § {target} [{sel}]"))
    elif column == "Name" and (path != r or not sections(body)[target][0] < line - 1 < sections(body)[target][1]):
        NAME_CITED.add((path, target))


def basic_tables(body):
    """modeling-constructs.md § Constructs § Basic Table: each section's Basic Tables that a Reference Key field, a Required
    field or both before it open, in live text -> {lineage: [{"key": [column], "required": [column], "header": [cell],
    "rows": [(line, [cell])], "line": n, "field": n}]}, a table declaring no Reference Key keyed by no column; a table's
    opening fields read through the one reader, so a backslash ending a field's line is no part of its value."""
    live = strip_fences(body)
    lines, secs = live.split("\n"), sorted(sections(body).items(), key=lambda x: x[1][0])
    decls = constructs.declarations(live, sections(body))
    in_construct = {t["line"] for _, _, _, tables, _ in decls for t in tables}
    in_construct |= {t["classes"]["line"] for _, _, _, tables, _ in decls for t in tables if "classes" in t}
    out = {}
    for i, l in enumerate(lines):
        if not l.startswith("|") or (i and lines[i - 1].startswith("|")) or i + 1 in in_construct:
            continue
        # the table's opening fields, the trailing run of them in the block of fields directly before it, read through
        # the one reader (modeling-constructs.md § Fields)
        k = i - 1
        while k >= 0 and not lines[k].strip():
            k -= 1
        start = k
        while start >= 0 and lines[start].strip() and not lines[start].lstrip().startswith(("|", "#", "```")):
            start -= 1
        first = next((n for n in range(start + 1, k + 1) if opens_key(lines[n]) and _indent(lines[n]) == 0), None)
        given = {}
        for f in (read_block(lines, first, 0, k + 1)[0] if first is not None else []):
            if f["key"] not in constructs.TABLE_OPENERS or f["key"] in given:
                given = {}
                continue
            value = value_of(f)
            value = value if isinstance(value, str) else ""
            given[f["key"]] = (f["line"] + 1, [c.strip() for c in value.split(",") if c.strip()])
        if not given:
            continue
        owner = [lin for lin, (h, end) in secs if h < i < end]
        rows, j = [], i + 2
        while j < len(lines) and lines[j].startswith("|"):
            rows.append((j + 1, constructs._cells(lines[j])))
            j += 1
        lineage = owner[-1] if owner else ""
        out.setdefault(lineage, []).append({
            "key": given.get("Reference Key", (0, []))[1], "required": given.get("Required", (0, []))[1],
            "name": ", ".join(given.get("Table Name", (0, []))[1]) or None,
            "order": [f for f in constructs.TABLE_OPENERS if f in given] == sorted(given, key=lambda g: given[g][0]),
            "header": constructs._cells(l), "rows": rows, "line": i + 1,
            "field": min(n for n, _ in given.values())})
    return out


def cited_value_findings(sel, r, line, found):
    """modeling-constructs.md § Constructs § Keyed Construct: a key value a citation names holds no section sign, semicolon or
    bracket, whatever it names, a row, a record or a construct's part."""
    for p in sel.split("; "):
        m = KEY_VALUE.match(p.strip())
        if m and re.search(r'[§;\]]', m.group(2)):
            found.append(("modeling-constructs.md § Constructs § Keyed Construct", r, line,
                          f"a cited key value holding a section sign, a semicolon or a bracket: [{sel}]"))


def row_citation(sel, target, table, r, line, found):
    """sourcing-and-citation.md § Writing a Citation: a Basic Table's row is named by the columns its Reference Key
    names, in their order, and matches exactly one row."""
    rule = "sourcing-and-citation.md § Writing a Citation"
    pairs = [KEY_VALUE.match(p.strip()) for p in sel.split("; ")]
    # a named table's key written as the path its name and its column make
    prefix = f"{table['name']}." if table.get("name") else ""
    if not all(pairs) or [p.group(1) for p in pairs] != [prefix + k for k in table["key"]]:
        found.append((rule, r, line, f"a row citation naming {[p.group(1) for p in pairs if p] or sel}, not its table's Reference Key {[prefix + k for k in table['key']]}: § {target}"))
        return
    idx = [table["header"].index(k) for k in table["key"] if k in table["header"]]
    wanted = [p.group(2).strip() for p in pairs]
    cited_value_findings(sel, r, line, found)
    hits = [row for _, row in table["rows"] if len(idx) == len(wanted) and [row[i].strip() if i < len(row) else "" for i in idx] == wanted]
    if len(hits) != 1:
        found.append((rule, r, line, f"a row citation matches {len(hits)} rows: § {target} [{sel}]"))


def record_citation(sel, path, target, text_of, r, line, found):
    """sourcing-and-citation.md § Writing a Citation: a record citation names every
    identifying field of its type, in order, and matches exactly one record, a record section's own item."""
    rule = "sourcing-and-citation.md § Writing a Citation"
    cited_value_findings(sel, r, line, found)
    title = target.split(" § ")[-1]
    spec = type_of(title, path)
    if not spec:
        part_citation(sel, path, target, text_of, r, line, found)
        return
    pairs = [KEY_VALUE.match(p.strip()) for p in sel.split("; ")]
    if not all(pairs):
        found.append((rule, r, line, f"a record citation not written as Key: value pairs: [{sel}]"))
        return
    keys = [p.group(1) for p in pairs]
    if keys != spec["identifying"]:
        found.append((rule, r, line, f"a record citation names {keys}, not {spec['identifying']}"))
        return
    wanted = [p.group(2).strip() for p in pairs]
    records, _ = parse_records(text_of[path], target, spec["section_fields"])
    hits = [rec for rec in records
            if [str(dict((k, v) for k, v, _ in rec).get(key, "")).strip() for key in keys] == wanted]
    if len(hits) != 1:
        found.append((rule, r, line, f"a record citation matches {len(hits)} records: § {target} [{sel}]"))
