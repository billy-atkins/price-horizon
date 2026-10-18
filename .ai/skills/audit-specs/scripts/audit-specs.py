#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment, per
specs/methodology/scope.md § Rules and Skills. `--check-scope` runs the checks, and
`--list-candidates` lists places for a reading audit to look, printed apart from any
finding and never affecting the exit status.

Standard library and this skill's own helper, constructs.py, only. See SKILL.md.
"""

import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

# its own helper sits beside it, found from the script's own place, so the script runs the same from any working
# directory and under an interpreter that leaves the script's directory off the import path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import constructs  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import citation_links  # noqa: E402


# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link
def read(path):
    """-> a file's text with each citation's link stripped, so every check reads the citation as written."""
    return citation_links.strip(path.read_text(encoding="utf-8"))


LINK_RULE = "sourcing-and-citation.md § Writing a Citation § A Citation's Link"

# specs/methodology/scope.md § What Spec of Record Governs names where each kind is named:
# specs by their place under specs/, the agent instructions by the root AGENTS.md and
# specs/AGENTS.md, the documentation by README.md and docs/, and skills by the registry, read at
# run time. The places and names this block defines are the ones scope.md's table gives, and scope_findings checks the table still says so;
# the working files are outside the script, read by the Working-file form audit instead, and code
# is outside this skill, which audits every kind but code.
SCOPE_HOME = "scope.md § What Spec of Record Governs"
# @canon-spec specs/methodology/scope.md § What Spec of Record Governs
SCOPE_KINDS = {"Agent instructions", "Specs", "Skills", "Documentation", "Working files", "Code"}
REGISTRY = "specs/methodology/skills.md"
REGISTRY_RULE = "skills.md § Registered Skills"
AUTHORING = "specs/methodology/skills.md § Authoring a Skill"
SCOPE_TREE = "specs/methodology/scope.md"
SPECS_AGENTS = "specs/AGENTS.md"
# @canon-spec specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed
SPECS_ARCHITECTURE = "specs/architecture.md"  # in specs/AGENTS.md's layer
GLOSSARY = "specs/methodology/glossary.md"
GLOSSARY_RULE = "glossary.md § Writing an Entry"
ABBREVIATION_RULE = "glossary.md § Using an Abbreviation"
RECORDED_ABBREVIATION = re.compile(r"\(abbreviated ([^)]*)\)")
# the text a diagram shows its reader: a node's label, an edge's label, a quoted string
DIAGRAM_LABEL = re.compile(r'\[[^\]]*\]|\([^)]*\)|\{[^}]*\}|"[^"]*"|\|[^|]*\|')
AUDIT_SKILL = ".ai/skills/audit-specs/SKILL.md"
CODE_CHECKS = ".ai/skills/verify-spec-implementation/SKILL.md"  # names the check enforcing each section of code.md
COVERAGE_RULE = "scope.md § Rules and Skills"
# The tables in the audit skill naming what reads or carries out each rule section:
# (section heading, rule column header)
COVERAGE_TABLES = (("The audits", "Enforces"), ("Operating rules carried out by a step", "Operating Rule"))
DIAGRAMS_RULE = "modeling-constructs.md § Diagrams"
IMAGE = re.compile(r"!\[[^\]]*\][(\[]|<img\b", re.I)
WORKING_FILES = "specs/methodology/working-files.md"
WORKING_FILES_RULE = "working-files.md § The Working Files"
SCRIPT_SUFFIXES = {".py", ".ps1", ".sh"}
# @canon-spec specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed
LAYER = {"methodology": "specs/methodology/", "product": "specs/application/product/",
         "technical": "specs/application/technical/"}

CITATION = constructs.CITATION  # the form written once, in constructs.py, which its construct checks read too
# A whole file is a valid citation form and carries no section token, so CITATION
# never sees one. Only the direction check applies to it: naming a file in another
# layer is the same dependency whether or not a section is named. The span must
# resolve to a known file, so a passing mention of a directory is not read as one.
WHOLE_FILE = re.compile(r'`([\w./-]+\.md)`')
LOOSE_SECTION = re.compile(r'(?<!`)§')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*$', re.M)
FENCE = re.compile(r'^```', re.M)

# specs/methodology/spec-style.md § Ordinals and Counts. The findings are the forms a pattern decides alone.
ORDINALS_RULE = "spec-style.md § Ordinals and Counts"
NUMBERED_LEAD_IN = re.compile(r'^\*\*\d+[.)]\s')
NUMBERED_ITEM = re.compile(r'^\s*\d+[.)]\s')
# @canon-spec specs/methodology/working-files.md § The Working Files
WORKING_FILE = re.compile(r'\.ai/(?:plans\b|follow-ups\.md|tmp\b)')
WORKING_FILES_HOME = "specs/methodology/working-files.md"

# modeling-constructs.md § Constructs § Record Form: every record type is read from its declaration, by declared_types,
# the canon's own among them; the script holds no copy of one. A type's own placement is this script's to carry out.
RECORD_FORM = "modeling-constructs.md § Constructs § Record Form"
# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact
# @canon-spec specs/methodology/spec-placement.md § Open Question
# the homes of the types a rule of this script reads by their declaration: the Fact type, whose Plural Name titles a
# file's Facts sections, the types whose record section is its file's last top-level section, and the types whose
# records' Impacts each carry a section citation
FACT_HOME = "specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact"
LAST_TOP_LEVEL = ("specs/methodology/spec-placement.md § Open Question",)
IMPACTS_CITED = ("specs/methodology/spec-placement.md § Open Question",)


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
# modeling-constructs.md § Fields: every key a form declares, and where that form places it.
FIELDS = "modeling-constructs.md § Fields"
# modeling-constructs.md § Constructs § Basic Table: its headers, its Reference Key and its rows
TABLES = "modeling-constructs.md § Constructs § Basic Table"
MAPPING = "sourcing-and-citation.md § External Reference § A Mapping onto a Standard"
# @canon-spec specs/methodology/sourcing-and-citation.md § External Reference § A Mapping onto a Standard
# the kinds of a departure's reason, in their order: the one copy, held to the mapping's Departs For row by
# mapping_rule_findings
DEPARTS_FOR = ("the standard's gap", "the canon's form", "no need yet")
# the registered standards' Names, read from their records as a check begins; a mapping's first header names one
STANDARDS = set()
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
# @canon-spec specs/methodology/spec-placement.md § Environments
FIELD_KEYS = {"Kind": "environment",
              **{f: {"Diagrams": "diagram", "Record Form #2": "record section"}.get(c, "construct") for f, c, _, _ in constructs.FIELD_TABLE}}
# spec-placement.md § Environments: the environments file, and the closed set of kinds
ENVIRONMENTS = "specs/application/technical/environments.md"
# @canon-spec specs/methodology/spec-placement.md § Environments
KINDS = ("local", "integration", "shared", "production")
FIELD_LINE = constructs.FIELD  # the form written once, in constructs.py
RECORD_SELECTOR = re.compile(r'^(.*?)\s+\[(.*)\]$')
# spec-style.md § Bold Lead-ins and § Emphasis: bold marks only a field or a lead-in
# label, both opening a line, and italic, the one emphasis, never opens one.
BOLD_SPAN = re.compile(r'\*\*(.+?)\*\*')
# a line's opening skips indentation, a quote marker, and a list marker: -, *, + or a number
LIST_OR_QUOTE = r'\s*(?:>\s*)*(?:(?:[-*+]|\d+[.)])\s+)?'
LINE_OPENING = re.compile(r'^' + LIST_OR_QUOTE + r'$')
ITALIC_OPENING = re.compile(r'^' + LIST_OR_QUOTE + r'\*(?!\*)\S')
ODD_EMPHASIS = re.compile(r'\*\*\*|__[^_\s][^_]*__')
BOLD_LEAD_INS = "spec-style.md § Bold Lead-ins"
CLEAR_PROSE = "spec-style.md § Clear Prose"
EMPHASIS = "spec-style.md § Emphasis"
LITERAL_TEXT = "spec-style.md § Literal Text"
# a citation's `Key: value`, its key a field label, constructs.py's one copy of the form, or a table's name and its key's,
# joined by a dot, where its construct has more than one keyed table (modeling-constructs.md § Constructs § Keyed Construct)
KEY_VALUE = re.compile(rf'^({constructs.LABEL}(?: {constructs.LABEL})*(?:\.{constructs.LABEL}(?: {constructs.LABEL})*)*): (.+)$')

# The candidates are likely places, not decisions: a reading audit judges each one.
_NUM = (r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
        r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|"
        r"seventy|eighty|ninety|hundred|thousand|dozen)")
_UNIT = r"(?:%|percent|ms|seconds?|minutes?|hours?|days?|weeks?|months?|quarters?|years?)"
CANDIDATE = [
    # "the four roles", "all five drivers", "one of the three": a count of a list. A bare
    # "the two" names a pair, which the rule keeps, so it is not listed.
    ("count of a list", re.compile(
        rf"\b(?:all|each of the|any of the|none of the|one of the|of the|these|those|its|their|the)"
        rf"\s+(?!two\b){_NUM}\b(?!\s*{_UNIT})", re.I)),
    # "Two traps worth checking", "Three shapes": a count opening a sentence or lead-in.
    ("count opening a sentence", re.compile(rf"(?:^|[.!?:]\s+|\*\*|\|\s*){_NUM}\b", re.I)),
    # "eighty broken citations", "three architecture.md files": a count of things.
    ("count of things", re.compile(
        rf"\b(?!two\b){_NUM}\s+(?!{_UNIT}\b)(?:[\w.`-]+\s+){{0,2}}?[\w.`-]*[a-z]s\b", re.I)),
    ("digit count", re.compile(
        rf"(?<![\w.$§-])(?<!step )(?<!steps )\d+\s+(?!{_UNIT}\b)[a-z][a-z-]*s\b|\b\d+-way\b|#\d+\b", re.I)),
    ("ordinal", re.compile(
        r"\b(?:second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|"
        r"latter|former)\b|\b\d+(?:st|nd|rd|th)\b|\bthe (?:first|last)\s+(?:two|three|of|one)\b",
        re.I)),
    ("positional reference", re.compile(r"\b(?:item|finding|change|question|row)\s+\d+\b", re.I)),
    # "the closing sentence", "that last part": a position in a passage named by word.
    ("position word", re.compile(
        r"\b(?:opening|closing|final|last|first|penultimate)\s+(?:sentence|paragraph|clause|"
        r"part|bullet|row|column|line|entry|item|point|section|step)s?\b", re.I)),
]
NUMBERED_COMMENT = re.compile(r'^\s*(?:#\s*)?\d+[.)]\s')


def registry(root):
    """-> (skill names, problems): the skills specs/methodology/skills.md registers.

    A missing registry, a table naming no skill, or a row not naming one in backticks is a
    problem, so a broken registry is reported rather than read as an empty scope.
    """
    p = root / REGISTRY
    if not p.exists():
        return [], [(SCOPE_HOME, REGISTRY, 0, "the skills registry is missing, so the scope cannot be read")]
    names, problems, inside = [], [], False
    for n, line in enumerate(read(p).split("\n"), 1):
        if line.startswith("| Skill |"):
            inside = True
            continue
        if not inside or line.startswith("|---"):
            continue
        if not line.startswith("|"):
            if names or problems:
                break
            continue
        m = re.match(r'\|\s*`([a-z0-9-]+)`\s*\|', line)
        if m:
            names.append(m.group(1))
        else:
            problems.append((REGISTRY_RULE, REGISTRY, n, "a registry row does not name a skill in backticks"))
    if not names:
        problems.append((SCOPE_HOME, REGISTRY, 0, "the skills registry names no skill, so the scope cannot be read"))
    return names, problems


def skill_dirs(root):
    """Each registered skill's directory name, and lib, the code their scripts share, where it is there."""
    return registry(root)[0] + (["lib"] if (root / ".ai/skills/lib").is_dir() else [])


def scope_paths(root):
    """The files in scope: the root AGENTS.md, the documentation, specs/, each registered skill, and the code they share."""
    return ["AGENTS.md", "README.md", "docs", "specs"] + [".ai/skills/" + n for n in skill_dirs(root)]


def md_files(root):
    out = []
    for s in scope_paths(root):
        p = root / s
        if p.is_file() and p.suffix == ".md":
            out.append(p)
        elif p.is_dir():
            out += [f for f in p.rglob("*.md")]
    return sorted(set(out))


def strip_fences(text):
    """Blank out fenced blocks so examples inside them are not linted as live content."""
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            out.append("")
        else:
            out.append("" if inside else line)
    return "\n".join(out)


def headings(text):
    """-> [(level, title)] from live content only."""
    return [(len(m.group(1)), m.group(2)) for m in HEADING.finditer(strip_fences(text))]


def sections(text):
    """-> {lineage: (heading_line, end_line)}, 0-based, over raw lines.

    A section's own text is the lines after its heading up to the next heading at any
    level. Fenced lines are skipped when finding headings, but kept in the numbering,
    since a diagram's fence is part of the section it sits in.
    """
    lines, heads, inside = text.split("\n"), [], False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            inside = not inside
        elif not inside:
            m = HEADING.match(line)
            if m:
                heads.append((i, len(m.group(1)), m.group(2)))
    out, stack = {}, []
    for n, (i, lvl, title) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        if lvl == 1:
            continue
        depth = lvl - 2
        stack = stack[:depth]
        while len(stack) < depth:
            stack.append(None)
        stack.append(title)
        out[" § ".join(t for t in stack if t)] = (i, end)
    return out


def resolve(cite, host):
    """A citation's (file, lineage); a same-file form resolves to its host. A record
    citation's `[...]` selector is dropped: this names the record section holding it."""
    cite = cite.strip()
    if cite.startswith("§"):
        path, target = host, cite.lstrip("§ ").strip()
    else:
        path, _, target = cite.partition(" § ")
        path, target = path.strip(), target.strip()
    m = RECORD_SELECTOR.match(target)
    return path, (m.group(1).strip() if m else target)


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


def unnamed_record_sections(r, body):
    """modeling-constructs.md § Constructs § Record Form: the lineage of each section of file `r` holding a Records
    field whose title is the Plural Name of no type whose records may sit there."""
    live = strip_fences(body).split("\n")
    return {lineage for lineage, (h, end) in sections(body).items()
            if not type_of(lineage.split(" § ")[-1], r) and "**Records:**" in live[h + 1:end]}


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


def record_findings(r, body, found):
    """Each record section in a file: its shape, its type's fields, and its placement."""
    lines = body.split("\n")
    live = strip_fences(body).split("\n")
    for lineage in unnamed_record_sections(r, body):
        found.append((RECORD_FORM, r, sections(body)[lineage][0] + 1, f"a record section titled with no declared type's Plural Name: {lineage.split(' § ')[-1]}"))
    for lineage in sections(body):
        title = lineage.split(" § ")[-1]
        spec = type_of(title, r)
        if not spec or spec["home"] == f"{r} § {lineage}":
            continue  # no type's, or its type's own definition, titled with its Plural Name and reported at the declaration
        # the section fields its type declares, before its Records, each a paragraph at the left margin
        given = [(mm["key"], (mm["value"] or "").strip(), i) for i in range(sections(body)[lineage][0] + 1, sections(body)[lineage][1])
                 for mm in [FIELD_LINE.match(live[i])] if mm and not mm["indent"] and not mm["marker"] and mm["key"] in spec["section_fields"]]
        for i in range(sections(body)[lineage][0] + 1, sections(body)[lineage][1]):
            mm = FIELD_LINE.match(live[i])
            if live[i].strip() == "**Records:**":
                break
            if mm and not mm["indent"] and not mm["marker"] and mm["key"] in FIELD_KEYS and mm["key"] not in spec["section_fields"] + ["Diagrams", "Records"]:
                found.append((spec["home"], r, i + 1, f"a section field its type does not declare: {mm['key']}"))
        keys = [k for k, _, _ in given]
        if keys != [f for f in spec["section_fields"] if f in keys]:
            found.append((spec["home"], r, sections(body)[lineage][0] + 1, f"a record section's section fields are {keys}, not in the order {spec['section_fields']}"))
        for f in spec["section_required"]:
            if f not in keys:
                found.append((spec["home"], r, sections(body)[lineage][0] + 1, f"a record section without the section field its type requires: {f}"))
        for k, v, i in given:
            if spec["section_defaults"].get(k) == v:
                found.append((spec["home"], r, i + 1, f"the {k} field written at its default value, {v}"))
            if k in spec["section_values"] and v not in spec["section_values"][k]:
                found.append((spec["home"], r, i + 1, f"the {k} field holds a value its type does not allow: {v}"))
        home = spec["home"]
        h, end = sections(body)[lineage]
        if spec["last_top_level"] and (" § " in lineage or end != len(lines)):
            found.append((home, r, h + 1, f"the {title} section is not its file's last top-level section"))
        records, problems = parse_records(body, lineage, spec["section_fields"])
        for rule, at, msg in problems:
            found.append((rule, r, at + 1, msg))
        names, given = set(), set()
        for rec in records:
            keys = [key for key, _, _ in rec]
            at = rec[0][2] + 1
            if keys != [f for f in spec["fields"] if f in keys] or any(k not in spec["fields"] for k in keys):
                found.append((home, r, at, f"a record's fields are {keys}, not {spec['fields']} in that order"))
                continue
            missing = [f for f in spec["required"] if f not in keys]
            if missing:
                found.append((home, r, at, f"a record without the field its type requires: {', '.join(missing)}"))
                continue
            values = {key: value for key, value, _ in rec}
            for key, value in values.items():
                if spec["defaults"].get(key) == value:
                    found.append((home, r, at, f"the {key} field written at its default value, {value}"))
            for key, value in values.items():
                if key in spec["values"] and value not in spec["values"][key]:
                    found.append((home, r, at, f"the {key} field holds a value its type does not allow: {value}"))
                # resolved in the file declaring the field, where its citation is written
                origin = spec.get("origin", {}).get(key)
                members = closed_set(strip_fences(_TEXT_OF[origin]), spec["cited"][key]) if key in spec["cited"] and origin else None
                if members is not None and value not in members:
                    found.append((home, r, at, f"the {key} field holds a value its closed set does not: {value}"))
            for key in spec["identifying"]:
                if not values[key]:
                    found.append((RECORD_FORM, r, at, f"an identifying value left blank: {key}"))
            ident = tuple(values[key] for key in spec["identifying"])
            if ident in names:
                found.append((RECORD_FORM, r, at, f"two records share their identifying values: {ident}"))
            names.add(ident)
            for key in [f for f in spec["unique"] if [f] != spec["identifying"]]:
                if values.get(key) and (key, values[key]) in given:
                    found.append((RECORD_FORM, r, at, f"two records share a value of {key}, a field unique on its own: {values[key]}"))
                given.add((key, values.get(key)))
            if spec["home"] in IMPACTS_CITED and "Impacts" in values and not CITATION.search(values["Impacts"]):
                found.append((home, r, at, "a record's Impacts carries no section citation"))


def environment_findings(r, body, found):
    """spec-placement.md § Environments: each environment's section opens with one Kind
    field from the closed set, on a line of its own, and holds no other; exactly one
    environment is local; and its tool and task tables carry the headers the rule sets."""
    if r != ENVIRONMENTS:
        return
    rule = "spec-placement.md § Environments"
    lines, local, opening = body.split("\n"), 0, set()
    secs = sorted(sections(body).items(), key=lambda x: x[1][0])
    # the environments are the file's top-level sections, or, where it has one, its children
    depth = 1 if sum(" § " not in lin for lin, _ in secs) == 1 else 0
    for lineage, (h, end) in secs:
        if lineage.count(" § ") != depth:
            continue
        j = next((j for j in range(h + 1, end) if lines[j].strip()), None)
        mm = re.fullmatch(r"\*\*Kind:\*\* (\S+)", lines[j].strip()) if j is not None else None
        if not mm or mm.group(1) not in KINDS or (j + 1 < end and lines[j + 1].strip()):
            found.append((rule, r, h + 1, "an environment does not open with a Kind field, on a line of its own, of local, integration, shared or production"))
            continue
        opening.add(j)
        local += mm.group(1) == "local"
    for i, line in enumerate(lines):
        if line.lstrip().startswith("**Kind:**") and i not in opening:
            found.append((rule, r, i + 1, "a Kind field other than the one opening an environment's section"))
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("| ") else []
        if cells[:1] == ["Tool"] and (cells[:3] != ["Tool", "Version", "Purpose"] or len(cells) < 4):
            found.append((rule, r, i + 1, "a tools table not headed Tool, Version and Purpose with at least one install column after them"))
        if cells[:1] == ["Task"] and cells not in (["Task", "Command", "Does"], ["Task", "Command", "Does", "Runs On"]):
            found.append((rule, r, i + 1, "a tasks table not headed Task, Command and Does, with Runs On after them where a task needs it"))
    if local != 1:
        found.append((rule, r, 0, f"{local} environments are local, not exactly one"))


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Basic Table
# a word in a proper noun's own casing, a capital after a lowercase letter within the word, which a header keeps
OWN_CASING = re.compile(r"^[A-Za-z0-9]*[a-z][A-Z][A-Za-z0-9]*$")


def header_findings(r, body, found):
    """modeling-constructs.md § Constructs § Basic Table: each Basic Table's header is a field label, but a
    header in backticks and a word in a proper noun's own casing; a construct's table, in its block, follows its
    construct's definition and is no Basic Table."""
    live = strip_fences(body)
    lines = live.split("\n")
    in_construct = {t["line"] for _, _, _, tables, _ in constructs.declarations(live, sections(body)) for t in tables}
    for i, l in enumerate(lines):
        if not l.startswith("|") or i + 1 >= len(lines) or not re.match(r"^\|[-| :]+\|\s*$", lines[i + 1]) \
                or (i > 0 and lines[i - 1].startswith("|")) or i + 1 in in_construct:
            continue
        for h in constructs._cells(l):
            # a label's first word opens with a capital, a later word made of digits alone
            if not h or h in ("...", "-") or h.startswith("`") or (all(constructs.LABEL_WORD.match(w) or OWN_CASING.match(w) for w in h.split(" "))
                                                                     and not h.split(" ")[0].isdigit()):
                continue
            found.append((TABLES, r, i + 1, f"a header that is no field label: {h}"))
        # a mapping onto a standard opened by none of its fields escapes the Basic Table's reading of its form
        cells, k = constructs._cells(l), i - 1
        while k >= 0 and not lines[k].strip():
            k -= 1
        if cells and cells[0] in STANDARDS and "Treatment" in cells \
                and not (k >= 0 and lines[k].startswith(tuple(f"**{f}:**" for f in constructs.TABLE_OPENERS))):
            found.append((MAPPING, r, i + 1, f"a mapping onto a standard opened by none of its fields: {cells[0]}"))


def field_findings(r, body, found):
    """modeling-constructs.md § Fields: each field's key is one a form declares, it sits
    where that form places it, and a key at the left margin follows a blank line."""
    raw = body.split("\n")
    live = strip_fences(body).split("\n")
    secs = sorted(sections(body).items(), key=lambda x: x[1][0])
    unnamed = unnamed_record_sections(r, body)
    for i, line in enumerate(live):
        mm = FIELD_LINE.match(line)
        if not mm:
            continue
        indent, dash, key = mm["indent"], mm["marker"], mm["key"]
        owner = [(lin, s) for lin, s in secs if s[0] < i < s[1]]
        lineage, (h, end) = owner[-1] if owner else ("", (-1, len(raw)))
        if lineage in unnamed:
            continue  # record_findings reports the section once, its type unknown
        title = lineage.split(" § ")[-1]
        spec = type_of(title, r)
        if spec and spec["home"] == f"{r} § {lineage}":
            spec = None  # its type's own definition, no record section of it
        if spec and (indent or dash) and key in spec["fields"]:
            continue  # a record's own field, whatever another form declares by the same key (§ Fields)
        # a type's own section field, whatever another form declares by the same key
        place = "record section" if spec and not indent and not dash and key in spec["section_fields"] else FIELD_KEYS.get(key)
        if place is None:
            found.append((FIELDS, r, i + 1, f"a field whose key no form declares: {key}"))
            continue
        if place == "diagram":
            ok = any(raw[j].startswith("```mermaid") for j in range(h + 1, end))
        elif place == "record section":
            ok = spec is not None and not indent and not dash
        elif place == "environment":
            ok = r == ENVIRONMENTS and not indent and not dash
        elif place == "construct":
            # modeling-constructs.md § Defining Constructs § Declaring a Construct: a paragraph of its own
            ok = not indent and not dash
        else:
            ok = spec is not None and key in spec["fields"] and bool(indent or dash)
        if not ok:
            found.append((FIELDS, r, i + 1, f"the {key} field outside the place its form gives it"))
        # Record Form: a blank line precedes each section field, at the left margin, or
        # Markdown renders it inside the line above; a record's own fields are stacked
        if spec and not indent and not dash and i > 0 and raw[i - 1].strip():
            found.append((RECORD_FORM, r, i + 1, f"the {key} field directly after a non-blank line"))


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


def basic_findings(r, body, found):
    """modeling-constructs.md § Constructs § Basic Table: a Basic Table's Reference Key names columns its header holds, each row's
    values under them are identifying values, unique alone or together; its Required names columns its header holds beside
    its key; and a row leaves no cell blank under either."""
    for lineage, t in ((lin, t) for lin, ts in basic_tables(body).items() for t in ts):
        missing = [k for k in t["required"] if k not in t["header"]]
        if missing:
            found.append((TABLES, r, t["field"], f"a Required naming no column its table holds: {', '.join(missing)}"))
        both = [k for k in t["required"] if k in t["key"]]
        if both:
            found.append((TABLES, r, t["field"], f"a Required naming a column its Reference Key names: {', '.join(both)}"))
        for ln, row in t["rows"]:
            for c in t["required"]:
                if c in t["header"] and not (row[t["header"].index(c)] if t["header"].index(c) < len(row) else ""):
                    found.append((TABLES, r, ln, f"a blank cell in a column its Required names: {c}"))
        # sourcing-and-citation.md § External Reference § A Mapping onto a Standard: a table headed first by a registered
        # standard's Name and holding a Treatment column is a mapping, written in its one form, a Departs For and a Why
        # on each row that departs and on no other
        if t["header"] and t["header"][0] in STANDARDS and "Treatment" in t["header"]:
            std = t["header"][0]
            if (t["header"] != [std, "Section", "Treatment", "Departs For", "Why"] or t["key"] != [std]
                    or t["required"] != ["Section", "Treatment"] or t["name"] != f"{std} Elements"):
                found.append((MAPPING, r, t["field"], "a mapping onto a standard not in its form: its Table Name the standard's "
                              "Name and `Elements`, its Reference Key that Name, its Required `Section, Treatment`, and its "
                              "columns that Name, Section, Treatment, Departs For and Why"))
                continue
            for ln, row in t["rows"]:
                treatment, kind, why = (row[k].strip() if k < len(row) else "" for k in (2, 3, 4))
                kinds = [k.strip() for k in kind.split(",")] if kind else []
                if not treatment.startswith(("the same", "differs:", "not written")):
                    found.append((MAPPING, r, ln, "a Treatment opening neither `the same`, `differs:` nor `not written`"))
                elif treatment.startswith("the same") and (kind or why):
                    found.append((MAPPING, r, ln, "a Departs For or a Why on a row whose Treatment is the same"))
                elif not treatment.startswith("the same") and (not kinds or len(kinds) > 2 or any(k not in DEPARTS_FOR for k in kinds)
                                                               or kinds != sorted(set(kinds), key=DEPARTS_FOR.index)):
                    found.append((MAPPING, r, ln, "a departure whose Departs For is not one or two of " + ", ".join(DEPARTS_FOR)
                                  + ", in that order"))
                elif not treatment.startswith("the same") and not why:
                    found.append((MAPPING, r, ln, "a departure with no Why"))
        if not t["order"]:
            found.append((TABLES, r, t["field"], "a table's opening fields out of their order, Table Name, Reference Key, Required"))
        if not t["key"]:
            continue
        missing = [k for k in t["key"] if k not in t["header"]]
        if missing:
            found.append((TABLES, r, t["field"], f"a Reference Key naming no column its table holds: {', '.join(missing)}"))
            continue
        idx = [t["header"].index(k) for k in t["key"]]
        seen = set()
        for ln, row in t["rows"]:
            values = tuple(row[i].strip() if i < len(row) else "" for i in idx)
            if any(not v for v in values):
                found.append((TABLES, r, ln, f"a key value left blank: {values}"))
            if values in seen:
                found.append((TABLES, r, ln, f"two rows sharing their key: {values}"))
            seen.add(values)
    # modeling-constructs.md § Constructs § Keyed Construct: of tables in one section keyed by the same declared columns, all but
    # one declare a distinct Table Name, a construct's keyed tables among them
    live = strip_fences(body)
    keyed = {}
    for lineage, ts in basic_tables(body).items():
        keyed.setdefault(lineage, []).extend((tuple(t["key"]), t["name"], t["field"]) for t in ts if t["key"])
    for _, construct, _, tables, lineage in constructs.declarations(live, sections(body)):
        for key, k in CONSTRUCT_KEYS.get(construct, {}).items():
            column = key.split(".")[-1]
            for t in (tables if k is None else tables[k:k + 1]):
                if column in t["header"]:
                    keyed.setdefault(lineage, []).append(((column,), t.get("name"), t["line"]))
    names = {}
    for lineage, ts in basic_tables(body).items():
        names.setdefault(lineage, []).extend((t["name"], t["field"]) for t in ts if t["name"])
    for _, _, _, tables, lineage in constructs.declarations(live, sections(body)):
        names.setdefault(lineage, []).extend((t["name"], t["line"]) for t in tables if t.get("name"))
    for lineage, ns in names.items():
        for n, (name, ln) in enumerate(ns):
            if not all(constructs.LABEL_WORD.match(w) for w in name.split(" ")) or name.split(" ")[0].isdigit():
                found.append(("modeling-constructs.md § Constructs § Tabular Construct", r, ln, f"a Table Name that is no field label: {name}"))
            if any(name == n2 for n2, _ in ns[:n]):
                found.append(("modeling-constructs.md § Constructs § Tabular Construct", r, ln, f"a Table Name another table of its section declares: {name}"))
    for lineage, ks in keyed.items():
        for n, (key, name, ln) in enumerate(ks):
            if any(key == k2 and name == n2 for k2, n2, _ in ks[:n]):
                found.append((TABLES, r, ln, f"two tables in one section keyed by {list(key)}, sharing a Table Name or both unnamed: § {lineage}"))


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


def diagram_findings(r, body, text_of, known, lineage, found):
    """modeling-constructs.md § Diagrams: each diagram's form, and its sources citing it back."""
    rule = "modeling-constructs.md § Diagrams"
    lines, secs = body.split("\n"), sections(body)
    for m in re.finditer(r'^```mermaid\s*$', body, re.M):
        start = body.count("\n", 0, m.start())
        owner = [(lin, s) for lin, s in secs.items() if s[0] < start < s[1]]
        if not owner:
            found.append((rule, r, start + 1, "a diagram with no heading of its own"))
            continue
        dlin, (h, end) = max(owner, key=lambda x: x[1][0])
        rest = [(i, lines[i]) for i in range(h + 1, end) if lines[i].strip()]
        while rest and rest[-1][1].strip() == "---":
            rest.pop()
        if not rest or rest[0][0] != start:
            found.append((rule, r, start + 1, "a diagram's section holds something before the diagram"))
            continue
        close = next((i for i in range(start + 1, end) if lines[i].startswith("```")), None)
        rest = [(i, l) for i, l in rest if close is not None and i > close]
        if not rest or not rest[0][1].startswith("**Caption:** "):
            found.append((rule, r, start + 1, "a diagram not followed by its **Caption:**"))
            continue
        caption = []
        while rest and not rest[0][1].startswith("**Sources:**"):
            caption.append(rest.pop(0))
        if rest and rest[0][0] == caption[-1][0] + 1:
            found.append((rule, r, rest[0][0] + 1, "a diagram's **Sources:** is not separated from its caption by a blank line"))
        if any(CITATION.search(l) or WHOLE_FILE.search(l) for _, l in caption):
            found.append((rule, r, caption[0][0] + 1, "a diagram's caption carries a citation"))
        if len({i for i, _ in caption}) != caption[-1][0] - caption[0][0] + 1:
            found.append((rule, r, caption[0][0] + 1, "a diagram's caption is not a single paragraph"))
        if not rest or rest[0][1].strip() != "**Sources:**":
            found.append((rule, r, start + 1, "a diagram's caption not followed by **Sources:** on its own line"))
            continue
        items = rest[1:]
        cites = []
        for i, l in items:
            mm = re.fullmatch(r'-\s+`([^`]+)`', l.strip())
            if not mm:
                found.append((rule, r, i + 1, "a diagram's section holds something other than one citation per Sources bullet"))
                continue
            if "§" not in mm.group(1):
                found.append((rule, r, i + 1, f"a Sources bullet is not a section citation: {mm.group(1)}"))
                continue
            cites.append((i, mm.group(1)))
        if not cites:
            found.append((rule, r, start + 1, "a diagram's Sources list is empty"))
        if [c for _, c in cites] != sorted(c for _, c in cites):
            found.append((rule, r, cites[0][0] + 1, "a diagram's Sources list is not sorted"))
        for i, c in cites:
            path, target = resolve(c, r)
            if path not in known or target not in lineage[path]:
                continue  # the citation check already reports it
            if (path, target) == (r, dlin):
                found.append((rule, r, i + 1, "a diagram lists its own section as a source"))
                continue
            src = text_of[path].split("\n")
            sh, se = sections(text_of[path])[target]
            back = False
            own = strip_fences("\n".join(src[sh + 1:se])).split("\n")
            if type_of(target.split(" § ")[-1], path):
                # a record section, or a record, cites its diagrams in its Diagrams field only
                start = next((k for k, l in enumerate(own) if l.strip() == "**Diagrams:**"), None)
                field = []
                if start is not None:
                    for l in own[start + 1:]:
                        if FIELD_LINE.match(l):
                            break
                        field.append(l)
                own = field
            for l in own:
                for cm in CITATION.finditer(l):
                    if resolve(cm.group(1), path) == (r, dlin):
                        back = True
            if not back:
                found.append((rule, r, i + 1, f"source does not cite the diagram back: {c}"))


def lineages(text):
    """-> set of '§'-joined ancestor paths, one per heading.

    A level-1 heading is the file's own title, not a section, so a lineage starts at
    level 2. This is why `§ Overview` resolves in a file whose first line is
    `# Payments Service`.
    """
    out, stack = set(), []
    for lvl, title in headings(text):
        if lvl == 1:
            continue
        depth = lvl - 2
        stack = stack[:depth]
        while len(stack) < depth:
            stack.append(None)
        stack.append(title)
        out.add(" § ".join(t for t in stack if t))
    return out


def layer_of(rel):
    for name, prefix in LAYER.items():
        if rel.startswith(prefix):
            return name
    if rel in (SPECS_AGENTS, SPECS_ARCHITECTURE):
        return "agents"
    return "project" if rel == "AGENTS.md" else None


def direction(src_layer, path, rel, line, found, section=True):
    """A citation never points down a layer except from specs/AGENTS.md or specs/architecture.md; application and
    methodology never cite each other in either direction, but for a Construct field citing its construct's definition,
    which the caller leaves out; an application spec never cites specs/AGENTS.md or specs/architecture.md; and no spec
    cites a section of the project's root AGENTS.md, though a plain mention of it is no citation of its content. Shared
    by both forms."""
    dst_layer = layer_of(path)
    if not (src_layer and dst_layer and src_layer != dst_layer):
        return
    specs = ("methodology", "product", "technical")
    bad = (
        (src_layer == "methodology" and dst_layer in ("product", "technical"))
        or (src_layer in ("product", "technical") and dst_layer in ("methodology", "agents"))
        or (src_layer == "product" and dst_layer == "technical")
        or (section and src_layer in specs and dst_layer == "project")
    )
    if bad:
        found.append(("sourcing-and-citation.md § Which Citations Are Allowed",
                      rel, line, f"{src_layer} cites {dst_layer}: {path}"))


def mapping_rule_findings(root):
    """sourcing-and-citation.md § External Reference § A Mapping onto a Standard: the script's copy of the kinds of a
    departure's reason against the mapping's Departs For row; and each sentence of a methodology file, its overview and
    its index aside, naming a departure from a registered standard, citing its mapping's row."""
    out = []
    sc = "specs/methodology/sourcing-and-citation.md"
    row = next((l for l in read(root / sc).split("\n") if l.startswith("| Departs For |")), "")
    if tuple(re.findall(r"`([^`]+)`", row)[:3]) != DEPARTS_FOR:
        out.append((MAPPING, sc, 0, f"the script's kinds of a departure's reason are not the Departs For row's: {list(DEPARTS_FOR)}"))
    names = sorted(STANDARDS | {"FEEL"}, key=len, reverse=True)
    if not names:
        return out
    alt = "|".join(re.escape(n) for n in names)
    named = re.compile(r"\b(?i:(?:depart(?:s|ed|ing|ures?)?|differ(?:s|ed|ing|ences?)?|deviat(?:es?|ed|ing|ions?)) from|unlike|contrary to) (?P<n>" + alt + r")\b")
    for path in sorted((root / "specs/methodology").glob("*.md")):
        if path.name in ("architecture.md", "index.md"):
            continue
        rel = path.relative_to(root).as_posix()
        lines = strip_fences(read(path)).split("\n")
        for n, line in enumerate(lines, 1):
            if line.startswith("|"):
                continue
            after = next((l for l in lines[n:] if l.strip()), "")
            opens = re.match(r"\*\*Table Name:\*\* (.+) Elements$", after)
            for sentence in re.split(r"(?<=\.)\s+(?=[A-Z`])", line):
                # a sentence opening a mapping, ending at a colon before the mapping's table, names no departure of its own
                for m in named.finditer(sentence):
                    std = "DMN" if m["n"] == "FEEL" else m["n"]
                    if sentence.rstrip().endswith(":") and opens and opens.group(1) == std:
                        continue
                    if f"{std} Elements." not in sentence:
                        out.append((MAPPING, rel, n, f"a departure from {std} named in prose, citing no row of its mapping: {sentence[:90]}"))
    return out


def example_pointer_findings(root):
    """scope.md § Progressive Disclosure: each directory of the worked examples a section names exists, and each topic's
    directory, a subject's subdirectory, is named by a section of the canon outside the examples."""
    out, rule = [], "scope.md § Progressive Disclosure"
    tree = root / "specs/methodology/examples"
    named = set()
    for path in [root / "specs/AGENTS.md", *sorted((root / "specs/methodology").glob("*.md"))]:
        if not path.exists():
            continue
        rel = path.relative_to(root).as_posix()
        for n, line in enumerate(read(path).split("\n"), 1):
            for m in re.finditer(r"`(specs/methodology/examples/[^`]*?)/?`", line):
                named.add(m.group(1).rstrip("/"))
                there = root / m.group(1)
                if not (there.is_file() if m.group(1).endswith(".md") else there.is_dir()):
                    out.append((rule, rel, n, f"a worked example's directory or file that does not exist: {m.group(1)}"))
    for topic in sorted(p for p in tree.glob("*/*") if p.is_dir()) if tree.is_dir() else []:
        t = topic.relative_to(root).as_posix()
        if t not in named:
            out.append((rule, t, 0, f"a topic of the worked examples no section of the canon names: {t}"))
    return out


def check(root, warned=None):
    """-> list of (rule, path, line, message); a warning, what the specs record as a gap of the system, is appended
    to `warned` where a list is given, and is never a finding."""
    found, files = [], md_files(root)
    warned = [] if warned is None else warned
    text = {f: read(f) for f in files}
    rel = {f: f.relative_to(root).as_posix() for f in files}
    lineage = {rel[f]: lineages(text[f]) for f in files}
    known = set(rel.values())
    text_of = {rel[f]: text[f] for f in files}
    # the registered standards' Names, a mapping's first header naming one
    register = root / "specs/methodology/external-references.md"
    STANDARDS.update(re.findall(r"^- \*\*Name:\*\* (.+?)\s*$", read(register), re.M) if register.exists() else [])
    # the record types the specs declare, by their Plural Names, before any record is read
    found += declared_types(text_of)
    found += closed_set_findings(text_of)
    # each construct's Reference Key, read from its definition before any part is cited
    found += construct_keys(text_of)

    for f in files:
        r, body = rel[f], text[f]
        live = strip_fences(body)
        src_layer = layer_of(r)
        # modeling-constructs.md § Constructs: each declared construct's structure
        constructs.construct_findings(r, live, found, sections(body))

        # Fenced blocks are stripped: a citation shown inside an example is an
        # illustration, not a dependency, and linting one produces a finding
        # nobody can act on.
        for i, line in enumerate(live.split("\n"), 1):
            # spec-style.md § Literal Text: a code span opens and closes with one backtick; a line indented
            # four spaces or a tab is an indented code block, literal as a fenced one is
            if "``" in constructs.CITATION.sub(lambda m: "" if _span_fits(m) else m.group(0), line) and not line.startswith(("    ", "\t")):
                found.append((LITERAL_TEXT, r, i, "a run of backticks, where literal text opens and closes with one"))
            # a code span is literal text, so markup inside one is never bold or italic
            prose = constructs.CODE_SPAN.sub(lambda m: "x" * len(m.group(0)), line)
            for m in BOLD_SPAN.finditer(prose):
                if not LINE_OPENING.match(prose[:m.start()]):
                    found.append((EMPHASIS, r, i, f"bold outside a line's opening: {line[m.start():m.end()][:60]}"))
                elif m.group(1).endswith(":") and not FIELD_LINE.match(line):
                    found.append((FIELDS, r, i, f"a field not in its form, its key in bold, then a space, any list marker a hyphen: {line[m.start():m.end() + 10][:60]}"))
                elif not m.group(1).endswith((":", ".", "?")):
                    found.append((BOLD_LEAD_INS, r, i, f"bold opening a line closes on neither a colon nor a period: {line[m.start():m.end()][:60]}"))
            # spec-style.md § Clear Prose: no dash serves as punctuation, outside code
            if "\u2014" in prose or "\u2013" in prose:
                found.append((CLEAR_PROSE, r, i, "an em dash or an en dash, where a sentence takes a period, a comma, a colon or parentheses"))
            if ITALIC_OPENING.match(prose):
                found.append((EMPHASIS, r, i, "a line opens with italic"))
            if ODD_EMPHASIS.search(prose):
                found.append((EMPHASIS, r, i, "bold italic or underscore bold"))
            if NUMBERED_LEAD_IN.match(line):
                found.append((ORDINALS_RULE, r, i, "bold lead-in carries a number"))
            elif NUMBERED_ITEM.match(line):
                found.append((ORDINALS_RULE, r, i, "list item carries a number"))
            if r.startswith("specs/") and r not in (WORKING_FILES_HOME, SPECS_AGENTS):
                for m in WORKING_FILE.finditer(line):
                    found.append(("sourcing-and-citation.md § Which Citations Are Allowed", r, i,
                                  f"names a working file: {m.group(0)}"))
            for m in WHOLE_FILE.finditer(line):
                if m.group(1) in known:
                    direction(src_layer, m.group(1), r, i, found, section=False)

            for m in CITATION.finditer(line):
                cite = m.group(1).strip()
                if " § " not in cite and not cite.startswith("§"):
                    continue
                if cite.startswith("§"):
                    target, path = cite.lstrip("§ ").strip(), r
                else:
                    path, _, target = cite.partition(" § ")
                    path, target = path.strip(), target.strip()
                sel = RECORD_SELECTOR.match(target)
                if sel:
                    target, sel = sel.group(1).strip(), sel.group(2)

                # lineage resolves
                if path not in known:
                    relative = posixpath.normpath(posixpath.join(posixpath.dirname(r), path))
                    problem = (f"not a project-root path: {path}" if relative in known
                               else f"cites a file that does not exist: {path}")
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i, problem))
                    continue
                if target not in lineage[path]:
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  f"no such heading path in {path}: § {target}"))
                elif sel is not None:
                    record_citation(sel, path, target, text_of, r, i, found)

                # direction, but a Construct field citing its construct's definition from any layer
                if not (line.startswith("**Construct:** ") and path == constructs.HOME and target.startswith("Constructs § ")):
                    direction(src_layer, path, r, i, found)

                # index.md is never a target
                if path.endswith("index.md"):
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  "cites an index.md, which is never a citation target"))

                # a skill's files cite into .ai/skills/ only that skill's own
                if path.startswith(".ai/skills/") and path.split("/")[2] != (
                        r.split("/")[2] if r.startswith(".ai/skills/") else None):
                    found.append((AUTHORING, r, i, f"cites another skill's file: {path}"))

        # bare § outside a backtick span. Every inline span is stripped, not only the
        # ones that parse as citations, since the rule is about the span and not the form.
        for i, line in enumerate(live.split("\n"), 1):
            stripped = constructs.CODE_SPAN.sub("", constructs.CITATION.sub("", line))
            if LOOSE_SECTION.search(stripped):
                found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                              "a § outside a backtick span"))

        # heading hygiene
        seen = {}
        stack = []
        for lvl, title in headings(body):
            stack = stack[: lvl - 1] + [title]
            parent = " § ".join(stack[:-1]) or "(file)"
            if re.match(r'^\d+[.)]\s', title):
                found.append(("sourcing-and-citation.md § Titling a Heading", r, 0,
                              f"heading carries an ordinal: {title}"))
            if "§" in title:
                found.append(("sourcing-and-citation.md § Titling a Heading", r, 0,
                              f"heading contains §: {title}"))
            if "[" in title:
                found.append(("sourcing-and-citation.md § Titling a Heading", r, 0,
                              f"heading contains [: {title}"))
            key = (parent, title)
            if key in seen:
                found.append(("sourcing-and-citation.md § Titling a Heading", r, 0,
                              f"duplicate heading under {parent}: {title}"))
            seen[key] = True

        # Test Scenarios shape
        hs = headings(body)
        for idx, (lvl, title) in enumerate(hs):
            if title != "Test Scenarios":
                continue
            prev = [h for h in hs[:idx] if h[0] < lvl]
            if not prev or prev[-1][0] != lvl - 1:
                found.append(("acceptance-scenarios.md § Acceptance Scenarios", r, 0,
                              "Test Scenarios is not exactly one level below its capability"))
            after = body.split("## " if lvl == 2 else "#" * lvl + " Test Scenarios", 1)
            if "```gherkin" not in body:
                found.append(("acceptance-scenarios.md § Acceptance Scenarios", r, 0,
                              "Test Scenarios section has no ```gherkin fence"))

        # A scenario-actor check was tried here and removed. "A Given names its actor by
        # role" is real, but absence of a role name does not decide a violation: a scenario
        # about system state has no actor, and one may name its role in the Then instead.
        # Flagging every Given without a role produced mostly noise, which is worse than
        # no check because a reader stops reading the output.

        # every gherkin block parses: each Scenario: carries a Given, When and Then
        for m in re.finditer(r'^```gherkin\s*\n(.*?)^```', body, re.S | re.M):
            block = m.group(1)
            for chunk in re.split(r'^\s*Scenario:', block, flags=re.M)[1:]:
                title = chunk.split("\n", 1)[0].strip()[:48]
                for kw in ("Given", "When", "Then"):
                    if not re.search(rf'^\s*(?:{kw}|And)\b', chunk, re.M) or \
                       not re.search(rf'^\s*{kw}\b', chunk, re.M):
                        found.append(("acceptance-scenarios.md § Acceptance Scenarios", r, 0,
                                      f"scenario has no {kw}: {title}"))

        # modeling-constructs.md § Constructs § Basic Table: its headers, its Reference Key and its rows
        header_findings(r, body, found)
        basic_findings(r, body, found)

        # mermaid blocks: declared as flowcharts, in the form a diagram takes, and cited
        # back by their sources. Scoped to specs/ because a skill may legitimately carry a
        # worked example. The fence is found in the raw text: strip_fences() blanks it.
        if r.startswith("specs/"):
            diagram_findings(r, body, text_of, known, lineage, found)
            record_findings(r, body, found)
            field_findings(r, body, found)
            environment_findings(r, body, found)
            for m in re.finditer(r'^```mermaid\s*\n(.*?)^```', body, re.S | re.M):
                # a diagram opens with a config front matter block, so scan the whole
                # fence rather than its first line
                if not re.search(r'^\s*flowchart\b', m.group(1), re.M):
                    found.append(("modeling-constructs.md § Diagrams", r, 0,
                                  "a mermaid block that does not declare flowchart"))

        # technical-specs front matter: product files only, paths under technical/
        if body.startswith("---"):
            fm = body.split("---", 2)[1]
            paths = re.findall(r'^\s*-\s+(\S+\.md)\s*$', fm, re.M) if "technical-specs:" in fm else []
            if paths and not r.startswith("specs/application/product/"):
                found.append(("spec-placement.md § Naming the Technical Files Behind a Capability",
                              r, 0, "technical-specs appears outside a product spec"))
            for p in paths:
                if not p.startswith("specs/application/technical/"):
                    found.append(("spec-placement.md § Naming the Technical Files Behind a Capability",
                                  r, 0, f"technical-specs names a non-technical file: {p}"))
            if paths:
                if paths != sorted(paths):
                    found.append(("spec-placement.md § Naming the Technical Files Behind a Capability",
                                  r, 0, "technical-specs is not sorted in plain character order"))
                for p in paths:
                    if p not in known:
                        found.append(("spec-placement.md § Naming the Technical Files Behind a Capability",
                                      r, 0, f"technical-specs names a missing file: {p}"))

    # every directory has an index.md, naming each file and subdirectory beside it
    for d in sorted({root / "specs"} | {p for p in (root / "specs").rglob("*") if p.is_dir()}):
        rel_d = d.relative_to(root).as_posix()
        idx = d / "index.md"
        if not idx.exists():
            found.append(("spec-placement.md § Where a File Goes", rel_d, 0, "directory has no index.md"))
            continue
        named = set(re.findall(r'^\|\s*`([^`]+)`', read(idx), re.M))
        present = {c.name + ("/" if c.is_dir() else "") for c in d.iterdir()
                   if c.name != "index.md" and (c.is_dir() or c.suffix == ".md")}
        for missing in sorted(present - named):
            found.append(("spec-placement.md § Where a File Goes", rel_d + "/index.md", 0, f"no row names {missing}"))
        for extra in sorted(named - present):
            found.append(("spec-placement.md § Where a File Goes", rel_d + "/index.md", 0, f"a row names {extra}, which is not here"))

    # a Name column, present exactly where a part of its table is cited from outside its section
    constructs.name_column_findings(text_of, NAME_CITED, found, sections, strip_fences)
    # a submachine state, governed by one machine and left by its exits
    constructs.submachine_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # an effect, the Algorithm or the Decision Table a transition runs
    constructs.effect_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # the facts an exclusive choice's guard compares a fact with, declared in any file
    constructs.guard_fact_findings(text_of, found, sections, strip_fences)
    # the word a guard tests a fact for, one of the fact's Values
    constructs.guard_value_findings(text_of, found, sections, strip_fences)
    # the fact a machine's state is recorded in, its Values holding each state
    constructs.recorded_in_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # a configured instance's Held In, and the construct an Extends extends
    constructs.held_in_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # what runs an Algorithm, and the facts a run gives
    constructs.algorithm_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # each Constraint's rule, when it holds and what keeps it, a rule nothing keeps a warning
    constructs.constraint_findings(text_of, found, warned, sections, strip_fences, CITATION, resolve)
    # each DAG's tasks' work and what runs it, and two tasks free at once giving one fact or reading what the other gives
    constructs.dag_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    # each trigger written in FEEL in its form, and a machine's Trigger Classes
    constructs.occurrence_findings(text_of, found, sections, strip_fences, CITATION, resolve)
    found += record_type_findings(root)
    found += canon_spec_findings(root)
    found += mapping_rule_findings(root)
    found += example_pointer_findings(root)
    found += scope_findings(root)
    found += voice_table_findings(root)
    found += [(LINK_RULE, path, line, problem) for path, line, problem in citation_links.problems(root)]
    found += glossary_findings(root)
    found += abbreviation_findings(root)
    found += coverage_findings(root)
    found += ignored_findings(root)
    found += reviewer_findings(root)
    found += image_findings(root)
    return found


# @canon-spec specs/methodology/skills.md § Setting Up an Agent
# specs/methodology/skills.md § Setting Up an Agent names the reviewers an agent writes to set
# itself up, and specs/methodology/scope.md § Agent Agnostic keeps what it writes out of git.
REVIEWERS = ("review-light", "review-medium", "review-high")
AGNOSTIC_RULE = "scope.md § Agent Agnostic"


def reviewer_findings(root):
    """No reviewer an agent wrote to set itself up is tracked, read from git ls-files. A project
    that is not a git repository, or a machine without git, tracks nothing to check."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    return [(AGNOSTIC_RULE, p, 0, "a reviewer definition an agent wrote to set itself up is tracked")
            for p in out.splitlines() if any(c.split(".")[0] in REVIEWERS for c in PurePosixPath(p).parts)]


def image_findings(root):
    """No spec embeds an image: a diagram is checked in as source."""
    found = []
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        if not rel.startswith("specs/"):
            continue
        for n, line in enumerate(strip_fences(read(f)).split("\n"), 1):
            if IMAGE.search(constructs.CODE_SPAN.sub("", line)):
                found.append((DIAGRAMS_RULE, rel, n, "embeds an image rather than a diagram's source"))
    return found


def level2_section(text, title):
    """-> the body of the level-2 section titled `title`, or None."""
    m = re.search(r'^## ' + re.escape(title) + r'\s*$', text, re.M)
    if not m:
        return None
    body = text[m.end():]
    nxt = re.search(r'^## ', body, re.M)
    return body[:nxt.start()] if nxt else body


def first_table(text, title, column=None):
    """-> (header cells, rows of cells) of the first table in the level-2 section titled
    `title` whose header holds `column`, or of its first table where no column is given; or None."""
    body = level2_section(text, title)
    if body is None:
        return None
    cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    tables, cur = [], []
    for l in body.split("\n") + [""]:
        if l.startswith("|"):
            cur.append(l)
        elif cur:
            tables.append(cur)
            cur = []
    for t in tables:
        if len(t) >= 2 and (column is None or column in cells(t[0])):
            return cells(t[0]), [cells(l) for l in t[2:]]
    return None


def workflow_citations(root):
    """-> {(path, section)} each registered skill's steps cite, under ## Workflow in its SKILL.md
    and in each of its references, from the first step on: a Workflow's opening paragraph is
    not a step."""
    cited = set()
    for n in registry(root)[0]:
        d = root / ".ai/skills" / n
        for f in [d / "SKILL.md"] + sorted((d / "references").glob("*.md")):
            body = level2_section(strip_fences(read(f)), "Workflow") if f.exists() else None
            first = re.search(r'^(?:### |\*\*)', body or "", re.M)
            for m in CITATION.finditer(body[first.start():] if first else ""):
                path, _, target = m.group(1).partition(" § ")
                if target:
                    cited.add((path.strip(), target.strip()))
    return cited


def coverage_findings(root):
    """Every section of specs/AGENTS.md and of the methodology's files, its overview aside, is
    named, itself or through a section it sits under, in the rule column of one of the audit
    skill's coverage tables, or, for a section of code.md, in the verify skill's table of checks;
    and each operating rule is cited, itself or through a section it
    sits under, by a step of a registered skill's Workflow, which is where its step is found."""
    sk = root / AUDIT_SKILL
    if not sk.exists():
        return [(COVERAGE_RULE, AUDIT_SKILL, 0, "the audit skill is missing, so no rule's check is named")]
    text, named, operating, found = read(sk), set(), set(), []
    for title, column in COVERAGE_TABLES:
        table = first_table(text, title, column)
        if table is None:
            found.append((COVERAGE_RULE, AUDIT_SKILL, 0, f"no {column} column in a table under ## {title}"))
            continue
        k = table[0].index(column)
        for row in table[1]:
            for m in CITATION.finditer(row[k] if k < len(row) else ""):
                path, _, target = m.group(1).partition(" § ")
                if target:
                    named.add((path.strip(), target.strip()))
                    if title == COVERAGE_TABLES[1][0]:
                        operating.add((path.strip(), target.strip()))
    # specs/methodology/scope.md § Rules and Skills: a section of code.md is named by the check on code
    checks = root / CODE_CHECKS
    table = first_table(read(checks), "The checks", "Enforces") if checks.exists() else None
    for row in table[1] if table else []:
        k = table[0].index("Enforces")
        for m in CITATION.finditer(row[k] if k < len(row) else ""):
            path, _, target = m.group(1).partition(" § ")
            if target and path.strip() == "specs/methodology/code.md":
                named.add((path.strip(), target.strip()))
    cited = workflow_citations(root)
    for path, target in sorted(operating):
        if not any(p == path and (s == target or target.startswith(s + " § ")) for p, s in cited):
            found.append((COVERAGE_RULE, AUDIT_SKILL, 0,
                          f"no registered skill's Workflow step cites the operating rule {path} § {target}"))
    for f in [root / SPECS_AGENTS] + sorted((root / "specs/methodology").glob("*.md")):
        rel = f.relative_to(root).as_posix()
        if not f.exists() or f.name in ("architecture.md", "index.md"):
            continue
        for lin in sections(read(f)):
            parts = lin.split(" § ")
            if not any((rel, " § ".join(parts[:k])) in named for k in range(1, len(parts) + 1)):
                found.append((COVERAGE_RULE, rel, 0, f"no check or step names § {lin}"))
    return found


def ignored_findings(root):
    """Each working file the working-files table names is ignored by a line of .gitignore
    naming it or a directory holding it, and un-ignored by none. A line ending in a slash
    names a directory only, as git reads it."""
    wf = root / WORKING_FILES
    table = first_table(read(wf), "The Working Files") if wf.exists() else None
    if table is None:
        return [(WORKING_FILES_RULE, WORKING_FILES, 0, "no table of working files to check")]
    gi = root / ".gitignore"
    ignored, negated = set(), set()
    if gi.exists():
        for line in read(gi).split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            body = line.lstrip("!").lstrip("/")
            (negated if line.startswith("!") else ignored).add((body.rstrip("/"), body.endswith("/")))
    found = []
    for row in table[1]:
        m = re.match(r'`([^`]+)`', row[0]) if row else None
        if not m:
            continue
        is_dir = m.group(1).endswith("/")
        parts = m.group(1).rstrip("/").split("/")
        dirs = {"/".join(parts[:k]) for k in range(1, len(parts))}
        full = "/".join(parts)
        hit = lambda entries: any(n in dirs or (n == full and (is_dir or not d)) for n, d in entries)
        if not hit(ignored) or hit(negated):
            found.append((WORKING_FILES_RULE, ".gitignore", 0, f"a working file is not ignored: {m.group(1)}"))
    return found


STYLE_RULE_FILE = "specs/methodology/spec-style.md"


def style_phrases(root):
    """-> a pattern of the phrases the Example column of spec-style.md's table quotes, the one
    list of them, or None where it cannot be read."""
    f = root / STYLE_RULE_FILE
    table = first_table(read(f), "What a Finished Spec Reads Like", "Example") if f.exists() else None
    if table is None:
        return None
    k = table[0].index("Example")
    phrases = {q.strip(" ,.") for row in table[1] if k < len(row) for q in re.findall(r'"([^"]+)"', row[k])}
    phrases = sorted((p for p in phrases if p), key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(map(re.escape, phrases)) + r")\b", re.I) if phrases else None


# A sentence long enough, and chained enough, that it may need a second read: a candidate for
# the reading of specs/methodology/spec-style.md § Clear Prose, never a finding.
LONG_SENTENCE_WORDS, LONG_SENTENCE_MARKS = 40, 6
SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z*`(\"])")


# A path into the application specs, which in the canon may be an example drawn from inside the
# house: a candidate for the reading of specs/methodology/spec-style.md § Clear Prose, never a
# finding. The files every project's application specs hold, by the methodology's own rules,
# and paths written as examples, are no candidates.
APPLICATION_PATH = re.compile(r"specs/application/[\w./-]+\.md")
# @canon-spec specs/methodology/spec-placement.md § Environments
# @canon-spec specs/methodology/spec-placement.md § Index, Architecture, Detail
# @canon-spec specs/methodology/spec-placement.md § The Technical Stack
GENERIC_APPLICATION_FILES = {"specs/application/index.md", "specs/application/product/index.md",
                             "specs/application/product/architecture.md", "specs/application/technical/index.md",
                             "specs/application/technical/architecture.md", "specs/application/technical/stack.md",
                             "specs/application/technical/environments.md"}
EXAMPLE_PATH = re.compile(r"/example[\w-]*(?:/|\.md$)")


def application_paths(text):
    """-> (line, path) for each path into the application specs naming a file of a project's
    own, fenced blocks included, since an example is often fenced."""
    for n, line in enumerate(text.split("\n"), 1):
        for m in APPLICATION_PATH.finditer(line):
            path = m.group(0)
            if path not in GENERIC_APPLICATION_FILES and not EXAMPLE_PATH.search(path):
                yield n, path


def prose_sentences(text):
    """-> (line, sentence as written, sentence masked) for each sentence of prose; headings, tables and
    fenced blocks aside. Inline code is masked at its own length, so a sentence is cut from the line
    as written; the masked sentence also hides quoted text, which a rule quoting a pattern holds."""
    for n, line in enumerate(strip_fences(text).split("\n"), 1):
        if not line.strip() or line.lstrip().startswith(("#", "|", "---")):
            continue
        masked = constructs.CODE_SPAN.sub(lambda m: "X" * len(m.group(0)), line)
        hidden = QUOTED.sub(lambda q: "Q" * len(q.group(0)), masked)
        start = 0
        for m in list(SENTENCE_BREAK.finditer(masked)) + [None]:
            end = m.start() if m else len(masked)
            yield n, line[start:end], hidden[start:end]
            start = m.end() if m else end


def words_of(sentence):
    """-> the words of a sentence: a word holds a letter or a digit, so a dash or a list marker is none."""
    return [w for w in sentence.split() if re.search(r"[A-Za-z0-9]", w)]


def long_sentences(text):
    """-> (line, sentence) for each sentence of prose over LONG_SENTENCE_WORDS words holding
    LONG_SENTENCE_MARKS or more commas, semicolons and colons; inline code counts as one word whose
    marks are not counted."""
    for n, s, _ in prose_sentences(text):
        code = code_masked(s)
        if len(words_of(code)) > LONG_SENTENCE_WORDS and len(re.findall(r"[,;:]", code)) >= LONG_SENTENCE_MARKS:
            yield n, s


# The words and the constructions specs/methodology/spec-style.md § Clear Prose has a reader test:
# candidates for its reading, never findings, since a word or a construction stays wherever it is
# natural and adds real value to its sentence. The words are an editorial list, read from the
# section's tables at run time, as specs/methodology/skills.md § Authoring a Skill has such a list read.
QUOTED = re.compile(r'"[^"\n]*"')
# The tables' names are a copy, since a table renamed would leave its words unread; --check-scope
# reports a name the section no longer holds.
# @canon-spec specs/methodology/spec-style.md § Clear Prose
VOICE_TABLES = ("Emphasis Words", "Generic Terms")
# The script's own search terms for the constructions § Clear Prose names, no copy of a list the canon
# holds: a construction they miss is the reading audit's to find.
SENTENCE_PATTERNS = (
    ("a comma that may splice two statements", re.compile(r",\s+(?:it is|there is|this is)\b", re.I)),
    ("a contrast that may say what a thing is not", re.compile(r",\s+not\b|\brather than\b|\bnot just\b", re.I)),
    ("a clause that may trail a finished sentence", re.compile(r",\s+(?:meaning|ensuring|making|allowing|leaving|giving|save|unlike)\b[^,;:]*[.!?]?\s*$", re.I)),
    ("a reason that may want a sentence of its own", re.compile(r",\s+(?:so|since|because)\b[^,;:]*[.!?]?\s*$", re.I)),
    ("a chain of its", re.compile(r"(?:\bits\b.*){3}|(?:\b(?:its own|itself)\b.*){2}", re.I)),
    ("never and always in one sentence", re.compile(r"^(?=.*\bnever\b)(?=.*\balways\b)", re.I)),
    ("a contraction", re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'m|'d)\b|\b(?:it|that|there|what|here|who|let)'s\b", re.I)),
    ("a curly quotation mark", re.compile("[“”‘’]")),
)
# A sentence's long constructions are read only where the sentence is long.
LONG_ONLY = {"a reason that may want a sentence of its own"}
# A span holding a section token or a path to a file: the script's own reading of a citation, for the
# candidate of where a citation sits.
CITATION_SPAN = re.compile(r"`[^`]*(?:§|/[^`\s]*\.md)[^`]*`")
# A paragraph of long sentences with no short one between: the script's own measure, which the pilot tunes.
RHYTHM_SENTENCES, RHYTHM_MEAN, RHYTHM_SHORT = 3, 30, 15


def clear_prose(root):
    """-> the text of spec-style.md § Clear Prose, or "" where it is missing."""
    f = root / STYLE_RULE_FILE
    return (level2_section(read(f), "Clear Prose") or "") if f.exists() else ""


def voice_table_findings(root):
    """-> a finding for each table VOICE_TABLES names that spec-style.md § Clear Prose does not hold."""
    held = set(re.findall(r"^\*\*Table Name:\*\* (.+?)\s*$", clear_prose(root), re.M))
    return [("spec-style.md § Clear Prose", STYLE_RULE_FILE, 0,
             f"no table named {t}, which the script reads its words from") for t in VOICE_TABLES if t not in held]


def voice_terms(root):
    """-> a pattern of the terms the tables VOICE_TABLES name in spec-style.md § Clear Prose, a term
    matched with a plain ending, or None."""
    body = clear_prose(root)
    terms, table = [], None
    for line in body.split("\n"):
        m = re.match(r"^\*\*Table Name:\*\* (.+)$", line)
        if m:
            table = m.group(1).strip()
        elif table in VOICE_TABLES and line.startswith("|") and not TABLE_RULE.match(line):
            cell = line.strip().strip("|").split("|")[0].strip()
            if cell != "Term":
                terms.append(cell)
        elif line.strip() and not line.startswith(("|", "**Reference Key:**", "**Required:**")):
            table = None
    terms = sorted(set(terms), key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(term_forms(t) for t in terms) + r")\b", re.I) if terms else None


def term_forms(term):
    """-> a pattern of a term's plain forms: its first word with an ending, a final "e" dropped
    before "-ing" and "-ed", and a final "s" of a verb phrase's first word dropped first, as
    "serves as" reads "serving as"; the rest of a phrase as written."""
    first, _, rest = term.partition(" ")
    stem = first[:-1] if rest and first.endswith("s") else first
    forms = [re.escape(stem) + r"(?:s|es|ly|d|ed|ing)?"]
    if stem.endswith("e"):
        forms.append(re.escape(stem[:-1]) + r"(?:ing|ed)")
    head = "(?:" + "|".join(forms) + ")"
    return head + ((r"\s+" + re.escape(rest)) if rest else "")


def voice_files(root):
    """-> the files the Finished style audit reads for Clear Prose: the specs, the documentation and
    both AGENTS.md files; the skills are Skill form's to read for it."""
    return [f for f in md_files(root) if not f.relative_to(root).as_posix().startswith(".ai/")]


def citation_candidates(root):
    """-> (path, line, kind, context) for each sentence carrying more than one citation, and each
    citation inside its clause, in every Markdown file in scope, the skills among them, where
    `§ Writing a Citation` reaches."""
    out = []
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        for n, s, _ in prose_sentences(read(f)):
            if len(CITATION_SPAN.findall(s)) > 1:
                out.append((rel, n, "more than one citation in a sentence", s.strip()))
            if any(inside_clause(s[:m.start()], s[m.end():]) for m in CITATION_SPAN.finditer(s)):
                out.append((rel, n, "a citation inside its clause", s.strip()))
    return out


def inside_clause(before, after):
    """-> whether a citation sits inside its clause: it neither closes the clause, nor stands in
    parentheses or a quotation, nor opens its sentence, a lead-in or a list marker before it, nor
    follows "as" or "per", as in "as `X` has it", nor takes a possessive; each of those is a name or a gloss.
    The reader decides whether any other is a name."""
    closes = re.match(r"\s*\)?\s*(?:[.;:,!?]|$)", after)
    enclosed = before.count("(") > before.count(")") or before.count('"') % 2
    opens = re.fullmatch(r"\s*(?:[-*]\s+|\d+\.\s+)?(?:\*\*[^*]*\*\*\s*)?", before)
    named = re.search(r"\b(?:as|per)\s+(?:[\w-]+\s+){0,3}$", before, re.I) or after.startswith("'")
    return not (closes or enclosed or opens or named)


def code_masked(s):
    """-> a sentence with its inline code masked, so code counts as one word."""
    return constructs.CODE_SPAN.sub(lambda m: "X" * len(m.group(0)), s)


def voice_candidates(root):
    """-> list of (path, line, kind, context) for each word and construction Clear Prose has a
    reader test in a sentence of prose, tables and headings aside, each paragraph whose rhythm or
    semicolons a reader tests, each sentence carrying more than one citation, and each citation inside
    its clause. Places to read, never findings."""
    out, terms = [], voice_terms(root)
    for f in voice_files(root):
        rel, text = f.relative_to(root).as_posix(), read(f)
        for n, s, masked in prose_sentences(text):
            long = len(words_of(code_masked(s))) > LONG_SENTENCE_WORDS
            for m in terms.finditer(masked) if terms else ():
                out.append((rel, n, f"a word kept only for its value: {m.group(1).lower()}", s.strip()))
            for kind, pattern in SENTENCE_PATTERNS:
                if (long or kind not in LONG_ONLY) and pattern.search(masked):
                    out.append((rel, n, kind, s.strip()))
        for n, lengths, semicolons in paragraphs(text):
            if len(lengths) >= RHYTHM_SENTENCES:
                shape = f"{len(lengths)} sentences, {round(sum(lengths) / len(lengths))} words on average, the shortest {min(lengths)}"
                if sum(lengths) / len(lengths) > RHYTHM_MEAN:
                    out.append((rel, n, "a paragraph whose sentences average long", shape))
                elif min(lengths) >= RHYTHM_SHORT:
                    out.append((rel, n, "a paragraph with no short sentence", shape))
            if semicolons > 1:
                out.append((rel, n, "more than one semicolon in a paragraph", f"{semicolons} semicolons"))
    return out + citation_candidates(root)


def paragraphs(text):
    """-> (first line, [words in each sentence], semicolons) for each paragraph of prose: lines
    between blank lines, a list item, a heading, a table, a field and a fenced block each ending one;
    inline code and quoted text hold no semicolon counted."""
    lines = strip_fences(text).split("\n")
    cur, first = [], 0
    for n, line in enumerate(lines + [""], 1):
        stripped = line.lstrip()
        prose = stripped and not stripped.startswith(("#", "|", "---", "- ", "* ", "> ")) and not re.match(r"^\d+\. ", stripped) \
            and not re.match(r"^\*\*[^*]+:\*\*", stripped)
        if prose:
            first = first or n
            cur.append(line)
            continue
        if cur:
            sentences = list(prose_sentences("\n".join(cur)))
            lengths = [len(words_of(code_masked(s))) for _, s, _ in sentences if words_of(code_masked(s))]
            yield first, lengths, sum(masked.count(";") for _, _, masked in sentences)
        cur, first = [], 0


VENDOR_NAMES = re.compile(r"\b(Claude|Anthropic|OpenAI|Codex|GPT|Copilot|Cursor|Gemini)\b|CLAUDE\.md|\.claude/|\.cursor/")


def style_and_agent_candidates(root):
    """-> list of (path, line, kind, context), for the Finished style and Agent agnostic audits.
    Places to read, never findings."""
    out, style = [], style_phrases(root)
    for f in md_files(root) if style else []:
        rel = f.relative_to(root).as_posix()
        if not rel.startswith("specs/") or rel in (SPECS_AGENTS, STYLE_RULE_FILE):
            continue
        for n, line in enumerate(strip_fences(read(f)).split("\n"), 1):
            m = style.search(line)
            if m:
                a, b = max(0, m.start() - 60), min(len(line), m.end() + 60)
                out.append((rel, n, "a phrase that may be drafting residue", line[a:b].strip()))
    instructions = [root / "AGENTS.md", root / SPECS_AGENTS]
    for name in skill_dirs(root):
        base = root / ".ai/skills" / name
        if base.is_dir():
            instructions += sorted(p for p in base.rglob("*") if p.suffix in {".md"} | SCRIPT_SUFFIXES)
    for f in instructions:
        if not f.exists():
            continue
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(read(f).split("\n"), 1):
            m = VENDOR_NAMES.search(line)
            if m and not line.startswith("VENDOR_NAMES"):
                a, b = max(0, m.start() - 60), min(len(line), m.end() + 60)
                out.append((rel, n, "a line naming a vendor, model or tool", line[a:b].strip()))
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        if rel.startswith(".ai/skills/"):
            continue
        for n, s in long_sentences(read(f)):
            out.append((rel, n, "a long sentence of chained clauses, which may need a second read", s.strip()))
        if rel in (SPECS_AGENTS, SPECS_ARCHITECTURE) or rel.startswith("specs/methodology/"):
            for n, path in application_paths(read(f)):
                out.append((rel, n, "a path into the application specs, which may be an example from inside the house", path))
    return out


# A definition's other full names are its trailing sentence, "Also called X." or "Also called
# X, Y.", optional; a term's abbreviation is in its own column.
OTHER_NAMES = re.compile(r'(?:\s*Also called ([^.]+)\.)?\s*$')
BARE_TERM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ,'-]*$")
TABLE_RULE = re.compile(r'^\|[\s|:-]+\|$', re.M)


def glossary_terms(root):
    """-> (header, [(line, term, abbreviation, other names, definition, where the other names
    start, cells)]), or None when there is no glossary."""
    g = root / GLOSSARY
    if not g.exists():
        return None
    rows, header = [], None
    for n, line in enumerate(read(g).split("\n"), 1):
        if not line.startswith("|") or TABLE_RULE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        term, abbreviation, definition = cells[0], (cells[1] if len(cells) > 2 else ""), "|".join(cells[2:])
        m = OTHER_NAMES.search(definition)
        others = ([abbreviation] if abbreviation else []) + \
                 ([x.strip() for x in m.group(1).split(",")] if m.group(1) else [])
        rows.append((n, term, abbreviation, others, definition, m.start(), len(cells)))
    return header, rows


def glossary_findings(root):
    """The glossary cites nothing and holds one table of bare terms, unique and sorted, each with
    its abbreviation in its own column and its definition ending with its other full names in the
    fixed form, none shared or equal to a term."""
    got = glossary_terms(root)
    if got is None:
        return [(GLOSSARY_RULE, GLOSSARY, 0, "the glossary is missing")]
    header, rows = got
    found, text = [], read((root / GLOSSARY))
    for n, line in enumerate(strip_fences(text).split("\n"), 1):
        if CITATION.search(line) or WHOLE_FILE.search(line):
            found.append((GLOSSARY_RULE, GLOSSARY, n, "the glossary cites nothing"))
    if header != ["Term", "Abbreviation", "Definition"]:
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the table's header is not | Term | Abbreviation | Definition |"))
    if len(TABLE_RULE.findall(text)) != 1:
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the glossary does not hold exactly one table"))
    folded = [t.casefold() for _, t, _, _, _, _, _ in rows]
    if folded != sorted(folded):
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the terms are not in sorted order"))
    owner = {}
    for n, term, abbreviation, others, definition, trail, width in rows:
        if width != 3:
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: a row holds a term, its abbreviation or none, and a definition, nothing else"))
        if abbreviation and not BARE_TERM.match(abbreviation):
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: not a bare abbreviation: {abbreviation}"))
        if not BARE_TERM.match(term):
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"not a bare term: {term}"))
        if folded.count(term.casefold()) > 1 and [t for _, t, *_ in rows].count(term) == 1:
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"the term is listed twice: {term}"))
        if re.search(r'\bAbbreviated\b', definition):
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: an abbreviation goes in its Abbreviation column"))
        if re.search(r'\bAlso called\b', definition[:trail]):
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: other full names are the trailing sentence, Also called"))
        for o in others:
            k = o.casefold()
            if k in folded:
                found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: the other name {o} is a term"))
            elif owner.setdefault(k, term) != term:
                found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: the other name {o} also belongs to {owner[k]}"))
    return found


def abbreviation_findings(root):
    """glossary.md § Using an Abbreviation: an abbreviation inside the house, in the glossary's
    Abbreviation column or recorded in the application specs as "(abbreviated X)", is used in no
    specification, AGENTS.md file or skill, its scripts among it, but where it is recorded, and is
    recorded once; the term is spelled out everywhere else, and the short form is for people."""
    got = glossary_terms(root)
    names = [abbreviation for _, _, abbreviation, _, _, _, _ in got[1] if abbreviation] if got else []
    found = []
    app = sorted((root / "specs" / "application").rglob("*.md"))
    for f in app:
        for n, line in enumerate(read(f).split("\n"), 1):
            for m in RECORDED_ABBREVIATION.finditer(line):
                if not re.fullmatch(r"[A-Za-z0-9]+", m.group(1)):
                    found.append((ABBREVIATION_RULE, f.relative_to(root).as_posix(), n,
                                  "not a bare abbreviation: " + m.group(1)))
                    continue
                if m.group(1) in names:
                    found.append((ABBREVIATION_RULE, f.relative_to(root).as_posix(), n,
                                  "an abbreviation inside the house recorded a second time: " + m.group(1)))
                names.append(m.group(1))
    if not names:
        return []
    used = re.compile(r"(?<![A-Za-z0-9])(?:%s)s?(?![A-Za-z0-9])" % "|".join(re.escape(n) for n in sorted(set(names), key=len, reverse=True)), re.I)
    files = [p for p in md_files(root) if not p.relative_to(root).as_posix().startswith(".ai/")]
    for name in skill_dirs(root):
        base = root / ".ai/skills" / name
        if base.is_dir():
            files += sorted(p for p in base.rglob("*") if p.suffix in {".md"} | SCRIPT_SUFFIXES)
    for f in files:
        rel = f.relative_to(root).as_posix()
        if not f.is_file():
            continue
        diagram = False
        for n, line in enumerate(read(f).split("\n"), 1):
            if line.strip().startswith("```"):
                diagram = line.strip() == "```mermaid"
                continue
            if diagram:
                # a diagram's node ids are identifiers, not prose; only the text it shows is read
                line = " ".join(m.group(0) for m in DIAGRAM_LABEL.finditer(line))
            if rel == GLOSSARY and line.startswith("|"):
                # the Abbreviation column is where the methodology's are recorded
                cells = line.split("|")
                if len(cells) > 3:
                    line = "|".join(cells[:2] + [""] + cells[3:])
            if f in app:
                line = RECORDED_ABBREVIATION.sub("", line)
            for m in used.finditer(line):
                found.append((ABBREVIATION_RULE, rel, n,
                              "an abbreviation inside the house, for people only; spell out its term: " + m.group(0)))
    return found



def glossary_candidates(root):
    """-> list of (path, line, kind, context), for the Glossary terms audit: a line outside the
    glossary where a term or one of its other names seems to be defined. Places to read."""
    got, out = glossary_terms(root), []
    if got is None:
        return out
    names = set()
    for _, term, _, others, _, _, _ in got[1]:
        names.update([term] + others)
    alt = "|".join(sorted((r'\s+'.join(map(re.escape, x.split())) for x in names), key=len, reverse=True))
    name = rf"(?:{alt})s?"
    # A definition equates the term with a kind, "A field is a key-value pair", or glosses it
    # in apposition, "Spec of Record, the methodology"; "is written" or "is missing" states a rule
    # about the term instead, and a term after an article or a comma is an item in a list.
    defining = re.compile(
        rf"(?:(?:^|[.!?:]\s+|\|\s*)|\b(?:a|an|the)\s+){name}\b(?:\s*\([^)]*\)|\s*{constructs.CODE_SPAN.pattern})?"
        rf"\s+(?:(?:is|are)\s+(?:a|an|the|one|what|where|how)\b|means\b|names\s+\w)"
        rf"|(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)(?<!,\s)\b{name},\s+(?:a|an|the)\b", re.I)
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        if rel == GLOSSARY:
            continue
        for n, line in enumerate(strip_fences(read(f)).split("\n"), 1):
            m = defining.search(line)
            if m:
                a, b = max(0, m.start() - 40), min(len(line), m.end() + 60)
                out.append((rel, n, "a glossary term that may be defined here", line[a:b].strip()))
    return out


def record_type_findings(root):
    """modeling-constructs.md § Constructs § Construct: constructs.py's copy of each table of the fields a definition or a
    construct declares, by the section defining it, and of each definition's Modifier, Extends and Implements, against its table where it is defined, row by row, so a change to
    either is a finding until the copy is brought into sync; a record type has no copy, read from its declaration."""
    out = []
    path = "specs/methodology/modeling-constructs.md"
    text = read((root / path))
    for rule, line, msg in constructs.field_table_findings(text, sections(text)):
        out.append((rule, path, line or 1, msg))
    for rule, line, msg in constructs.column_table_findings(text, sections(text)):
        out.append((rule, path, line or 1, msg))
    for rule, line, msg in constructs.definition_findings(text, sections(text)):
        out.append((rule, path, line or 1, msg))
    # FEEL's built-in functions, the child script's copy held to the table in their home
    path = "specs/methodology/expressions.md"
    text = read((root / path))
    for line, msg in constructs.expressions.function_table_findings(text):
        out.append(("expressions.md § Expressions § FEEL § Its Functions", path, line or 1, msg))
    for line, msg in constructs.expressions.keyword_findings(text):
        out.append(("expressions.md § Expressions § FEEL § Names", path, line or 1, msg))
    for line, msg in constructs.expressions.library_table_findings(text):
        out.append(("expressions.md § Expressions § FEEL § The Canon's Functions", path, line or 1, msg))
    return out


# sourcing-and-citation.md § Writing a Citation § Citing From Code: a comment line naming the tag, and the
# form it takes in a script, a comment of its own holding the tag, a space and a citation
CITING_FROM_CODE = "sourcing-and-citation.md § Writing a Citation § Citing From Code"
# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code
CANON_SPEC_TAG = "@canon-spec"
# a comment naming the tag anywhere on a line, a line of code's trailing one among them; then its form
CANON_SPEC = re.compile(r"#.*" + CANON_SPEC_TAG + r"\b")
CANON_SPEC_FORM = re.compile(r"^\s*# " + CANON_SPEC_TAG + r" (\S.*?)\s*$")


def canon_spec_findings(root):
    """Each canon-spec annotation in a registered skill's scripts or the code the skills share: in its
    form, citing `specs/AGENTS.md` or a methodology file, or a section of one, that exists, and each
    run of them on consecutive lines sorted in plain character order."""
    out = []
    for name in skill_dirs(root):
        for f in sorted((root / ".ai/skills" / name).rglob("*")):
            if f.suffix not in SCRIPT_SUFFIXES or "__pycache__" in f.parts:
                continue
            rel = f.relative_to(root).as_posix()
            run = []
            for i, line in enumerate(read(f).split("\n") + [""], 1):
                if not CANON_SPEC.search(line):
                    if run and [c for _, c in run] != sorted(c for _, c in run):
                        out.append((CITING_FROM_CODE, rel, run[0][0], "canon-spec annotations not sorted in plain character order"))
                    run = []
                    continue
                m = CANON_SPEC_FORM.match(line)
                if not m:
                    out.append((CITING_FROM_CODE, rel, i, "a canon-spec annotation not in its form: " + line.strip()))
                    continue
                cite = m.group(1)
                run.append((i, cite))
                path, _, lineage = cite.partition(" § ")
                target = root / path
                if not (path == SPECS_AGENTS or path.startswith("specs/methodology/")) or not path.endswith(".md"):
                    out.append((CITING_FROM_CODE, rel, i, "a canon-spec annotation citing neither specs/AGENTS.md nor a methodology spec: " + cite))
                elif path.endswith("/index.md"):
                    out.append((CITING_FROM_CODE, rel, i, "a canon-spec annotation citing an index.md, never a citation target: " + cite))
                elif not target.is_file():
                    out.append((CITING_FROM_CODE, rel, i, "a canon-spec annotation naming no file: " + path))
                elif lineage and lineage not in sections(read(target)):
                    out.append((CITING_FROM_CODE, rel, i, "a canon-spec annotation naming no heading: " + cite))
    return out


def scope_findings(root):
    """scope.md, the skills registry, and each registered skill's form."""
    found = []
    names, problems = registry(root)
    found += problems
    scope = root / SCOPE_TREE
    if not scope.exists():
        return found + [(SCOPE_HOME, SCOPE_TREE, 0, "the scope file is missing")]
    text = read(scope)
    section = re.search(r'^## What Spec of Record Governs\n(.*?)(?=^## )', text, re.S | re.M)
    rows = re.findall(r'^\|\s*([A-Z][^|]*?)\s*\|[^|]*\|([^|]*)\|', section.group(1) if section else "", re.M)
    rows = [(k, named) for k, named in rows if k != "Kind"]
    kinds = {k for k, _ in rows}
    if kinds != SCOPE_KINDS:
        found.append((SCOPE_HOME, SCOPE_TREE, 0, f"the kinds are {sorted(kinds)}, not the ones the script reads, {sorted(SCOPE_KINDS)}"))
    for kind, named in rows:
        for home in re.findall(r'`([^`]+)`', named):
            path = home.split(" § ")[0].strip()
            if path.endswith((".md", "/")) and not (root / path.rstrip("/")).exists():
                found.append((SCOPE_HOME, SCOPE_TREE, 0, f"the {kind} row names {path}, which does not exist"))
    # the tree names exactly the methodology's files, and every path it names exists
    tree = re.search(r'^## The Shape of the Scope\n.*?^```\n(.*?)^```', text, re.S | re.M)
    rule = "scope.md § The Shape of the Scope"
    if not tree:
        found.append((rule, SCOPE_TREE, 0, "the scope's tree is missing"))
        return found + skill_findings(root, names)
    stack, listed = [], set()
    for line in tree.group(1).split("\n"):
        m = re.match(r'^([│ ├└─]*)(\S+)', line)
        if not m or not m.group(2).strip("…"):
            continue
        depth, name = len(m.group(1)) // 4, m.group(2)
        stack = stack[:depth] + [name]
        path = "".join(s if s.endswith("/") else s + "/" for s in stack[:-1]) + name
        if "<" in path:
            continue
        full = path
        if not (root / full.rstrip("/")).exists():
            found.append((rule, SCOPE_TREE, 0, f"the tree names {full}, which does not exist"))
        if full.startswith("specs/methodology/") and full.count("/") == 2 and not name.endswith("/"):
            listed.add(name)
    actual = {p.name for p in (root / "specs/methodology").glob("*.md")}
    for n in sorted(actual - listed):
        found.append((rule, SCOPE_TREE, 0, f"the tree does not name specs/methodology/{n}"))
    for n in sorted(listed - actual):
        found.append((rule, SCOPE_TREE, 0, f"the tree names specs/methodology/{n}, which is not there"))
    return found + skill_findings(root, names)


def skill_findings(root, names):
    """specs/methodology/skills.md § Authoring a Skill, for each registered skill."""
    found = []
    for n in names:
        d = root / ".ai/skills" / n
        rel = f".ai/skills/{n}/SKILL.md"
        if not (d / "SKILL.md").exists():
            found.append((REGISTRY_RULE, REGISTRY, 0, f"the registered skill {n} has no SKILL.md"))
            continue
        fm = re.match(r'^---\n(.*?)\n---', read((d / "SKILL.md")).replace("\r\n", "\n"), re.S)
        meta = dict(re.findall(r'^(\w+):\s*(.*)$', fm.group(1), re.M)) if fm else {}
        if not fm:
            found.append((AUTHORING, rel, 1, "SKILL.md does not open with YAML front matter"))
        if meta.get("name", "").strip() != n or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+', n):
            found.append((AUTHORING, rel, 1, f"front matter name is not the kebab-case directory name {n}"))
        if not meta.get("description", "").strip():
            found.append((AUTHORING, rel, 1, "front matter has no description"))
        if len(meta.get("description", "").strip()) > 1024:
            found.append((AUTHORING, rel, 1, "front matter description is longer than 1024 characters"))
        if len(n) > 64:
            found.append((AUTHORING, rel, 1, f"skill name is longer than 64 characters: {n}"))
        if level2_section(strip_fences(read((d / "SKILL.md"))), "Workflow") is None:
            found.append((AUTHORING, rel, 0, "SKILL.md has no ## Workflow section"))
        if (d / "scripts").is_dir() and not (d / "scripts" / (n + ".py")).exists():
            found.append((AUTHORING, f".ai/skills/{n}/scripts", 0, f"no entry-point script named {n}.py"))
    return found


def script_lines(path):
    """-> [(line_no, text)] of a script's comments and docstrings, where its prose is."""
    out, in_doc = [], False
    for n, line in enumerate(read(path).split("\n"), 1):
        s = line.strip()
        if path.suffix == ".py" and s.count('"""') % 2 == 1:
            out.append((n, line))
            in_doc = not in_doc
        elif in_doc or s.startswith("#"):
            out.append((n, line))
    return out


def candidates(root):
    """-> list of (path, line, pattern, context), for the Ordinals and counts audit."""
    out = []

    def scan(rel, n, line, patterns):
        for name, rx in patterns:
            m = rx.search(line)
            if m:
                s, e = max(0, m.start() - 60), min(len(line), m.end() + 60)
                out.append((rel, n, name, line[s:e].strip()))

    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        md = strip_fences(read(f)).split("\n")
        for n, line in enumerate(md, 1):
            if n < len(md) and md[n].strip() and not HEADING.match(line):
                # a count wrapped onto the next line: add that line's opening words
                line = line + " " + " ".join(md[n].split()[:3])
            patterns = CANDIDATE + ([("count in a heading", re.compile(rf"\b{_NUM}\b|\d", re.I))]
                                    if HEADING.match(line) else [])
            scan(rel, n, line, patterns)
    for s in [".ai/skills/" + n for n in skill_dirs(root)]:
        base = root / s
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.suffix not in SCRIPT_SUFFIXES:
                continue
            rel = f.relative_to(root).as_posix()
            lines = script_lines(f)
            for k, (n, line) in enumerate(lines):
                # a count wrapped onto the next line, "three" then "architecture.md files"
                nxt = " " + lines[k + 1][1].strip() if k + 1 < len(lines) else ""
                scan(rel, n, line + nxt, CANDIDATE + [("numbered comment", NUMBERED_COMMENT)])
    return out


# specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text: other text pointed at by
# direction rather than cited. A word placing something in a hierarchy or a layout, one
# level below a heading, is none of this, so these are places to read, never findings.
DIRECTION = re.compile(
    r"\b(?:the|each|every|this|these|those|its|in|as|per|by|defined|described|stated|shown|given|listed)\s+"
    r"(?:[\w-]+\s+){0,4}?(?:above|below)\b(?!\s+(?:the|an|its|their|every|one|that|which|them)\b)"
    r"|\b(?:already\s+)?(?:named|described|stated|given|listed|defined|shown|mentioned|drawn)\s+(?:above|below|next|earlier)\b"
    r"|\bfollows?\s+the\s+(?:table|list|tree|steps?)\b"
    r"|\bsteps?\s+[\d.]+(?:\s*(?:,|and|to)\s*[\d.]+)*\s+(?:above|below)\b"
    r"|\b(?:what|that|which|as)\s+(?:follows?|precedes?)\b(?!\s+(?:from|for)\b)|\bsee\s+(?:above|below)\b"
    r"|\b(?:the\s+following|these\s+[\w-]+(?:\s+[\w-]+)?)\s*:"
    r"|\b(?:earlier|later)\s+in\s+this\s+(?:file|section|skill|document)\b"
    r"|\bas\s+(?:described|stated|noted|shown|given|defined)\s+(?:earlier|previously)\b|\b(?:foregoing|aforementioned)\b"
    r"|`\s+(?:above|below)\b|\((?:above|below)\)"
    r"|\b(?:next|previous|preceding|following|later|earlier)\s+(?:[\w-]+\s+)?(?:step|section|table|paragraph|list|heading|row|audit|algorithm|tree|lifecycle|constraint|dag|machine|form)s?\b",
    re.I)


def direction_candidates(root):
    """-> list of (path, line, pattern, context): candidate lines pointing at other text by direction,
    for the Ordinals and counts audit."""
    out = []
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(strip_fences(read(f)).split("\n"), 1):
            m = DIRECTION.search(line)
            if m:
                s, e = max(0, m.start() - 60), min(len(line), m.end() + 40)
                out.append((rel, n, "pointed at by direction", line[s:e].strip()))
    for base in [root / ".ai/skills" / n for n in skill_dirs(root)]:
        for f in sorted(base.rglob("*")) if base.is_dir() else []:
            if f.suffix in SCRIPT_SUFFIXES:
                for n, line in script_lines(f):
                    m = DIRECTION.search(line)
                    if m:
                        s, e = max(0, m.start() - 60), min(len(line), m.end() + 40)
                        out.append((f.relative_to(root).as_posix(), n, "pointed at by direction", line[s:e].strip()))
    return out


def _span_fits(m):
    """spec-style.md § Literal Text: a citation's span of one backtick, or of one more than the longest run its text holds."""
    delim, text = len(m.group(0)) - len(m.group(0).lstrip("`")), m.group(1)
    runs = [len(r) for r in re.findall(r"`+", text)]
    return delim == 1 if not runs else delim == max(runs) + 1


def skill_candidates(root):
    """An unregistered skill whose SKILL.md cites the methodology's rules, which may belong to the
    methodology or may simply follow Authoring a Skill; and a registered skill's script importing
    from outside the standard library, which the rule allows where the standard library
    cannot serve; and a skill's long sentence of chained clauses, and a path into the application
    specs in a skill, for the Skill form audit's reading of
    specs/methodology/spec-style.md § Clear Prose. Places to read, never findings."""
    out, names = [], set(registry(root)[0])
    base = root / ".ai/skills"
    if base.is_dir():
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            sk = d / "SKILL.md"
            if d.name not in names and sk.exists() and re.search(r'specs/(?:methodology/|AGENTS\.md)', read(sk)):
                out.append((f".ai/skills/{d.name}/SKILL.md", 0, "unregistered skill citing the methodology's rules", d.name))
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    if not stdlib:
        out.append(("(this Python)", 0, "imports not checked", "sys.stdlib_module_names needs Python 3.10 or later"))
    # specs/methodology/skills.md § Authoring a Skill: a skill's script may import its own helpers beside it and the code the skills share
    lib = {p.stem for p in (base / "lib").glob("*.py")} if (base / "lib").is_dir() else set()
    for n in sorted(names) + (["lib"] if lib else []):
        for py in sorted((base / n).rglob("*.py")):
            for k, line in enumerate(read(py).split("\n"), 1):
                m = re.match(r'^\s*(?:import\s+([A-Za-z_]\w*)|from\s+([A-Za-z_]\w*)[\w.]*\s+import\b)', line)
                mod = m and (m.group(1) or m.group(2))
                if mod and stdlib and mod not in stdlib and mod not in lib and not (py.parent / f"{mod}.py").exists():
                    out.append((py.relative_to(root).as_posix(), k, "import from outside the standard library", line.strip()))
    for n in sorted(names) + (["lib"] if lib else []):
        for f in sorted((base / n).rglob("*.md")):
            for k, s in long_sentences(read(f)):
                out.append((f.relative_to(root).as_posix(), k, "a long sentence of chained clauses, which may need a second read", s.strip()))
            for k, path in application_paths(read(f)):
                out.append((f.relative_to(root).as_posix(), k, "a path into the application specs, which may be an example from inside the house", path))
        for f in sorted(p for p in (base / n).rglob("*") if p.suffix in SCRIPT_SUFFIXES):
            for k, path in application_paths(read(f)):
                out.append((f.relative_to(root).as_posix(), k, "a path into the application specs, which may be an example from inside the house", path))
    return out


def literal_candidates(root):
    """-> list of (path, line, kind, context), for the Markup audit.

    A backtick span naming no heading, field key, path, citation, identifier or markup
    the tree holds may be a name; an italic span of more than a few words may be stress
    that needs structure instead. Places to read, never findings.
    """
    known, out, fenced = set(FIELD_KEYS), [], []
    for f in md_files(root):
        text = read(f)
        known.update(title for _, title in headings(text))
        # a span written verbatim in a fenced example, a Gherkin keyword or a Mermaid
        # directive, is literal text the tree itself shows
        fenced += re.findall(r'^```[^\n]*\n(.*?)^```', text, re.S | re.M)
    fenced_words = set(" ".join(fenced).split())
    fenced_text = "\n".join(fenced)
    literal = re.compile(r'[§/._*\[\]:=()<>#;~]|^-|^[a-z0-9-]+$')
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(strip_fences(read(f)).split("\n"), 1):
            for m in constructs.CODE_SPAN.finditer(line):
                span = m["text"]
                if span in known or literal.search(span) or span in fenced_words or span in fenced_text:
                    continue
                out.append((rel, n, "backtick span that may be a name", span))
            prose = constructs.CODE_SPAN.sub("", line)
            for m in re.finditer(r'(?<![*\w])\*(?!\*)([^*]+?)\*(?!\*)', prose):
                if len(m.group(1).split()) > 6:
                    out.append((rel, n, "italic span longer than a short phrase", m.group(1)[:80]))
    return out


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    # Actions are flags per specs/methodology/skills.md § Authoring a Skill.
    parser = argparse.ArgumentParser(prog="audit-specs.py", description=__doc__.split("\n\n")[0], allow_abbrev=False)
    parser.add_argument("--check-scope", action="store_true",
                        help="check the files Spec of Record governs against every rule the files alone decide, "
                             "each finding named for the rule it breaks; exits 1 on any finding")
    parser.add_argument("--list-candidates", action="store_true",
                        help="list places for the reading audits to look, printed apart from any finding, "
                             "and never itself a finding")
    parser.add_argument("--detail", action="store_true",
                        help="with --list-candidates, list every word and construction Clear Prose has a reader test, "
                             "rather than their count for each file")
    parser.add_argument("--root", metavar="DIR", default=".",
                        help="the project root the scope is read from; the current directory unless given")
    args = parser.parse_args(argv[1:])
    if not (args.check_scope or args.list_candidates):
        parser.print_usage(sys.stderr)
        return 2
    root = Path(args.root).resolve()
    if not (root / "specs").is_dir():
        parser.error(f"--root {args.root} holds no specs/ directory")
    status = 0

    if args.check_scope:
        warned = []
        found = check(root, warned)
        by_rule = {}
        for rule, path, line, msg in found:
            by_rule.setdefault(rule, []).append((path, line, msg))
        for rule in sorted(by_rule):
            print(f"\n{rule}")
            for path, line, msg in sorted(by_rule[rule]):
                where = f"{path}:{line}" if line else path
                print(f"  {where}\n    {msg}")
        n = len(found)
        print(f"\n{n} finding{'' if n == 1 else 's'} across {len(md_files(root))} files")
        status = 1 if n else 0
        if warned:
            # a warning is what the specs record as the system's gap: listed on every run, and never a finding
            print(f"\nWarnings, {len(warned)} rule{'' if len(warned) == 1 else 's'} the specs record as kept by nothing; listed, not findings")
            for rule, path, line, msg in sorted(warned):
                print(f"  {path}:{line}\n    {msg}")

    if args.list_candidates:
        print("\nCandidates for the Ordinals and counts audit: numbers, places to read, not findings")
        for path, line, name, context in candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Markup audit: places to read, not findings")
        for path, line, name, context in literal_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Glossary terms audit: places to read, not findings")
        for path, line, name, context in glossary_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Finished style and Agent agnostic audits: places to read, not findings")
        for path, line, name, context in style_and_agent_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Finished style audit's reading of Clear Prose and of where a citation sits: places to read, "
              "not findings" + ("" if args.detail else "; counts for each file, --detail listing each"))
        voice = voice_candidates(root)
        if args.detail:
            for path, line, name, context in voice:
                print(f"  {path}:{line}  [{name}]\n    {context}")
        else:
            counts = {}
            for path, _, name, _ in voice:
                kind = name.split(":")[0]
                counts.setdefault(path, {}).setdefault(kind, 0)
                counts[path][kind] += 1
            for path in sorted(counts):
                print(f"  {path}: {sum(counts[path].values())}  " + "; ".join(f"{k} {v}" for k, v in sorted(counts[path].items())))
        print("\nCandidates for the Skill form audit: places to read, not findings")
        for path, line, name, context in skill_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Ordinals and counts audit: text pointed at by direction, places to read, not findings")
        for path, line, name, context in direction_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Construct choice and form audit: places to read, not findings")
        files = [(f.relative_to(root).as_posix(), read(f)) for f in md_files(root)]
        for path, line, name, context in constructs.construct_candidates(files, sections, strip_fences):
            print(f"  {path}:{line}  [{name}]\n    {context}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
