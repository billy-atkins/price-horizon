"""The record types, facts, closed sets, Basic Tables and construct keys the specs declare, and the parts a
citation names: what the construct checks read before they run, read here once for every skill's script that runs them
(specs/methodology/skills.md § Authoring a Skill). declared_types fills TYPES; the checks then read it."""
import re

import constructs
from spec_text import RECORD_SELECTOR, resolve, sections, strip_fences

CITATION = constructs.CITATION  # the form written once, in constructs.py


# modeling-constructs.md § Constructs § Record Form: every record type is read from its declaration, by declared_types,
# the canon's own among them; the checks hold no copy of one. A type's own placement is audit-specs' to carry out.
RECORD_FORM = "modeling-constructs.md § Constructs § Record Form"


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact
# @canon-spec specs/methodology/spec-placement.md § Open Question
# the homes of the types a rule of the checks reads by their declaration: the Fact type, whose Plural Name titles a
# file's Facts sections, the types whose record section is its file's last top-level section, and the types whose
# records' Impacts each carry a section citation
FACT_HOME = "specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact"


LAST_TOP_LEVEL = ("specs/methodology/spec-placement.md § Open Question",)


def derive(spec):
    """A type's fields, its identifying fields, its Reference Key, and its unique, required, defaulted and listed fields,
    from its tables."""
    spec["fields"] = [f for f, _, _, _, _ in spec["table"]]
    spec["identifying"] = list(spec["key"])
    spec["unique"] = [f for f, unique, _, _, _ in spec["table"] if unique == "yes"]
    spec["required"] = [f for f, _, req, _, _ in spec["table"] if req == "yes"]
    spec["defaults"] = {f: d for f, _, _, d, _ in spec["table"] if d}
    # modeling-constructs.md § Constructs § Record Form: a field's values, where its Values cell lists them
    spec["values"] = {f: constructs.quoted_values(v) for f, _, _, _, v in spec["table"]
                      if constructs.quoted_values(v) is not None}
    # a record field whose Values cite a closed set's record section, its values that set's members
    spec["cited"] = {f: v for f, _, _, _, v in spec["table"] if constructs.CITED_SET.fullmatch(v)}
    # its section fields, each row's Field, Required, Default Value and Values
    sec = spec.get("section_table", ())
    spec["section_required"] = [f for f, req, _, _ in sec if req == "yes"]
    spec["section_defaults"] = {f: d for f, _, d, _ in sec if d}
    spec["section_values"] = {f: constructs.quoted_values(v) for f, _, _, v in sec if constructs.quoted_values(v) is not None}
    return spec


# every record type the specs declare, by its Plural Name, filled by declared_types before the checks run
TYPES = {}


_TEXT_OF = {}


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
# @canon-spec specs/methodology/spec-placement.md § Environments
FIELD_KEYS = {"Kind": "environment",
              **{f: {"Diagrams": "diagram", "Record Form #2": "record section"}.get(c, "construct") for f, c, _, _ in constructs.FIELD_TABLE}}


FIELD_LINE = constructs.FIELD  # the form written once, in constructs.py


# a citation's `Key: value`, its key a field label, constructs.py's one copy of the form, or a table's name and its key's,
# joined by a dot, where its construct has more than one keyed table (modeling-constructs.md § Constructs § Keyed Construct)
KEY_VALUE = re.compile(rf'^({constructs.LABEL}(?: {constructs.LABEL})*(?:\.{constructs.LABEL}(?: {constructs.LABEL})*)*): (.+)$')


def type_of(title, r):
    """modeling-constructs.md § Constructs § Record Form: the record type a section titled `title` holds in file `r`,
    one whose Plural Name it is and whose records may sit there, a canon type's in any file under specs/ and an application spec's
    type's in the application specs; or None."""
    spec = TYPES.get(title)
    return spec if spec and r.startswith(spec["reach"]) else None


def declared_types(text_of):
    """modeling-constructs.md § Constructs § Record Form: each record type a Record Form declares under specs/, by its
    Plural Name, read from its declaration, a type extending another holding its base's fields first; each added to TYPES
    and its fields' keys to FIELD_KEYS, and the closed-set resolver set. -> the
    declarations' own findings: a defining section titled other than with the type's name, bare; a Plural Name two
    types share; a field a type and its base both name; and a Reference Key naming a field the type does not give or
    does not require."""
    out, raw, ext = [], {}, {}
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
            title, home = lineage.split(" § ")[-1], f"{r} § {lineage}"
            if re.match(r"(?:A|An) ", title) or title == plural:
                out.append((RECORD_FORM, r, line, f"a record type's section titled other than with the type's name, bare: {title}"))
            if plural in raw:
                out.append((RECORD_FORM, r, line, f"a Plural Name another record type declares: {plural}"))
                continue
            sec = [t for t in tables if t["header"] == constructs.SECTION_FIELDS]
            raw[plural] = {"table": tuple(tuple(row[:5]) for _, row in rec[0]["rows"] if len(row) == 6),
                           "key": [k.strip() for k in values.get("Reference Key", "").split(",") if k.strip()],
                           "section_table": tuple(tuple(row[:4]) for _, row in sec[0]["rows"] if len(row) == 5) if sec else (),
                           "home": home, "last_top_level": home in LAST_TOP_LEVEL, "declared": (r, line),
                           "reach": "specs/application/" if r.startswith("specs/application/") else "specs/"}
            ext[plural] = (values.get("Extends", "none"), r)
    by_home = {spec["home"]: p for p, spec in raw.items()}

    def base_of(p):
        e, r = ext[p]
        cites = CITATION.findall(e) if e != "none" else []
        return by_home.get(" § ".join(resolve(cites[0], r))) if len(cites) == 1 else None

    def chain(p, seen=()):
        b = base_of(p)
        return (chain(b, seen + (p,)) if b and b not in seen + (p,) else ()) + (p,)
    # each type's own tables, read before any is extended, so a chain of bases is read once
    own = {p: (spec["table"], spec["section_table"], spec["key"]) for p, spec in raw.items()}
    for p, spec in raw.items():
        types = chain(p)
        spec["table"] = tuple(row for t in types for row in own[t][0])
        # each field with the file declaring it, where a citation in its Values resolves
        spec["origin"] = {row[0]: raw[t]["declared"][0] for t in types for row in own[t][0]}
        # its Reference Key, its own or its nearest base's, of fields it gives and requires
        spec["key"] = next((own[t][2] for t in reversed(types) if own[t][2]), [])
        required = {row[0]: row[2] for row in spec["table"]}
        for k in spec["key"] if len(types) > 1 else []:
            if required.get(k) != "yes":
                out.append((RECORD_FORM, *spec["declared"], f"a Reference Key naming a field the type does not give or does not require: {k}"))
        spec["section_table"] = tuple(row for t in types for row in own[t][1])
        spec["section_fields"] = [row[0] for row in spec["section_table"]]
        names = [row[0] for row in spec["table"]] + spec["section_fields"]
        for f in sorted({f for f in names if names.count(f) > 1}):
            out.append((RECORD_FORM, *spec["declared"], f"a field a record type and its base both name: {f}"))
        TYPES[p] = derive(spec)
        for key in spec["fields"]:
            FIELD_KEYS.setdefault(key, "record")
        for key in spec["section_fields"]:
            FIELD_KEYS.setdefault(key, "record section")
    _TEXT_OF.update(text_of)
    constructs.CLOSED_SET = closed_set
    constructs.FACTS_SECTION = next((p for p, spec in TYPES.items() if spec["home"] == FACT_HOME), None)
    constructs.READ_FACT = read_fact
    return out


def closed_set(body, cell):
    """modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact: the identifying values of the members of the
    closed set a Facts record's Values cites, the records of its record section, of a type identifying them by one field,
    or the rows of its Basic Table keyed by one column, or None where it cites no such section."""
    cites = CITATION.findall(cell)
    if len(cites) != 1 or "[" in cites[0]:
        return None
    path, target = resolve(cites[0], None)
    text = body if path is None else _TEXT_OF.get(path)
    # a section of another file read as the type reaching that file; one of the citing file read by its title's type,
    # record_findings reporting it where that type's records may not sit
    spec = type_of(target.split(" § ")[-1], path) if path else TYPES.get(target.split(" § ")[-1])
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
    """modeling-constructs.md § Constructs § Record Form: a closed set's records sit in the one record section a fact's
    Values cite; another section of its type holding records where they may sit is reported."""
    out, homes = [], {}
    for r, body in text_of.items():
        if not r.startswith("specs/"):
            continue
        for _, _, d in constructs.fact_records(strip_fences(body), sections(body)):
            if d.get("cited"):
                path, target = resolve(CITATION.findall(d["cited"])[0], r)
                homes[(path, target)] = target.split(" § ")[-1]
    for (path, target), title in homes.items():
        spec = type_of(title, path)
        if not spec:
            continue
        for r, body in text_of.items():
            if not r.startswith(spec["reach"]):
                continue
            live = strip_fences(body).split("\n")
            for lineage, (h, end) in sections(body).items():
                if lineage.split(" § ")[-1] == title and (r, lineage) != (path, target) and "**Records:**" in live[h + 1:end]:
                    out.append((RECORD_FORM, r, h + 1, f"a second record section of the closed set {path} § {target}"))
    return out


def parse_records(body, lineage, section_keys=()):
    """modeling-constructs.md § Constructs § Record Form: a record section's records.

    -> (records, problems): each record a list of (key, value, line) in the order
    written; each problem (rule, line, message). A record section holds only fields: an
    optional Diagrams list, then Records, whose value is one list item per record, the
    first field on the item's line and each later one on a line indented two spaces directly
    beneath the one before, with no blank line inside a record.
    """
    lines = body.split("\n")
    h, end = sections(body)[lineage]
    rows = [(i, lines[i]) for i in range(h + 1, end)]
    while rows and rows[-1][1].strip() in ("", "---"):
        rows.pop()
    problems, records = [], []
    k = 0

    def skip():
        nonlocal k
        while k < len(rows) and not rows[k][1].strip():
            k += 1

    skip()
    if k < len(rows) and rows[k][1].strip() == "**Diagrams:**":
        k += 1
        cites = []
        while k < len(rows) and (rows[k][1].startswith("- ") or (not rows[k][1].strip() and k + 1 < len(rows) and rows[k + 1][1].startswith("- "))):
            if not rows[k][1].strip():
                k += 1
                continue
            mm = re.fullmatch(r'-\s+`([^`]+)`', rows[k][1].strip())
            if mm:
                cites.append(mm.group(1))
            else:
                problems.append((RECORD_FORM, rows[k][0], "a Diagrams bullet is not one citation"))
            k += 1
        if not cites:
            problems.append((RECORD_FORM, h, "a record section's Diagrams field lists no diagram"))
        elif cites != sorted(cites):
            problems.append((RECORD_FORM, h, "a record section's Diagrams list is not sorted"))
        skip()
    # the section fields its type declares, each a paragraph of its own
    while k < len(rows) and FIELD_LINE.match(rows[k][1]) and not FIELD_LINE.match(rows[k][1])["indent"] \
            and not FIELD_LINE.match(rows[k][1])["marker"] and rows[k][1].strip() != "**Records:**":
        k += 1
        while k < len(rows) and rows[k][1].strip():
            k += 1
        skip()
    if k >= len(rows) or rows[k][1].strip() != "**Records:**":
        problems.append((RECORD_FORM, h, "a record section does not hold its records under **Records:**"))
        return records, problems
    k += 1
    current = None
    gap = False
    for i, text in rows[k:]:
        if not text.strip():
            gap = True
            continue
        if gap and text.startswith("  ") and current is not None:
            problems.append((RECORD_FORM, i, "a blank line inside a record: its fields are stacked"))
        gap = False
        if text.startswith("- "):
            mm = FIELD_LINE.match(text)
            current = [(mm["key"], (mm["value"] or "").strip(), i)] if mm else [(None, "", i)]
            records.append(current)
            if not mm:
                problems.append((RECORD_FORM, i, "a record does not open with a field"))
        elif text.startswith("  ") and current is not None:
            mm = FIELD_LINE.match(text)
            if mm and len(mm["indent"]) == 2 and not mm["marker"]:
                current.append((mm["key"], (mm["value"] or "").strip(), i))
            elif current:
                key, value, at = current[-1]
                current[-1] = (key, (value + " " + text.strip()).strip(), at)
        else:
            problems.append((RECORD_FORM, i, "a record section holds something other than its fields"))
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
    for lineage, (h, end) in sections(body).items():
        parts = lineage.split(" § ")
        if len(parts) != 2 or parts[0] != "Constructs" or parts[1] not in constructs.FORMS:
            continue
        lines = body.split("\n")[h + 1:end]
        i = next((k for k, l in enumerate(lines) if l.startswith("**Reference Key:**")), None)
        if i is None:
            continue
        value = lines[i][len("**Reference Key:**"):].strip()
        if value:
            CONSTRUCT_KEYS[parts[1]] = {value: None}
            continue
        # a list, read to its last item past any blank line before it: one item to each of the construct's tables, a table
        # and its column joined by a dot
        items = []
        for l in lines[i + 1:]:
            if not items and not l.strip():
                continue
            if not l.startswith("- "):
                break
            items.append(l[2:])
        forms = constructs.FORMS[parts[1]]

        def keyed(k, item):
            levels = item.strip().split(".")
            return len(levels) == 2 and levels[-1] in (forms[k] or []) + ["Name"]
        if not items or len(items) != len(forms) or any(not KEY_VALUE.match(it.strip() + ": x") or not keyed(k, it) for k, it in enumerate(items)):
            out.append((constructs.KEYED, home, h + 1 + i, f"a construct's definition whose Reference Key is empty, or a list not giving, for each of its tables, a path to one of its columns: {parts[1]}"))
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
    "rows": [(line, [cell])], "line": n, "field": n}]}, a table declaring no Reference Key keyed by no column."""
    live = strip_fences(body)
    lines, secs = live.split("\n"), sorted(sections(body).items(), key=lambda x: x[1][0])
    decls = constructs.declarations(live, sections(body))
    in_construct = {t["line"] for _, _, _, tables, _ in decls for t in tables}
    in_construct |= {t["classes"]["line"] for _, _, _, tables, _ in decls for t in tables if "classes" in t}
    declared = {lin for _, _, _, _, lin in decls}
    out = {}
    for i, l in enumerate(lines):
        if not l.startswith("|") or (i and lines[i - 1].startswith("|")) or i + 1 in in_construct:
            continue
        given, k = {}, i - 1
        while k >= 0:
            while k >= 0 and not lines[k].strip():
                k -= 1
            name = next((f for f in constructs.TABLE_OPENERS if k >= 0 and lines[k].startswith(f"**{f}:**")), None)
            if name is None or name in given:
                break
            given[name] = (k + 1, [c.strip() for c in lines[k][len(name) + 5:].split(",") if c.strip()])
            k -= 1
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
    identifying field of its type, in order, and matches exactly one record."""
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
            if [dict((k, v) for k, v, _ in rec).get(key, "").strip() for key in keys] == wanted]
    if len(hits) != 1:
        found.append((rule, r, line, f"a record citation matches {len(hits)} records: § {target} [{sel}]"))
