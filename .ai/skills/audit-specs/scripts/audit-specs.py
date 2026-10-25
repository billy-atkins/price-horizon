#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment, per
specs/methodology/scope.md § Rules and Skills. `--check-scope` runs the checks, and
`--list-candidates` lists places for a reading audit to look, printed apart from any
finding and never affecting the exit status.

Standard library and the code the skills share in .ai/skills/lib/ only: constructs.py, the construct checks, with
expressions.py; spec_text.py, the reading of a spec's text; record_types.py, the record types and facts the specs
declare; and citation_links.py. See SKILL.md.
"""

import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

# the shared code, found from the script's own place, so the script runs the same from any working directory and
# under an interpreter that leaves the script's directory off the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import citation_links  # noqa: E402
import constructs  # noqa: E402
import layout  # noqa: E402
from record_types import (  # noqa: E402
    CONSTRUCT_KEYS, FACT_HOME, FIELD_KEYS, FIELD_LINE, KEY_VALUE, LAST_TOP_LEVEL, NAME_CITED, RECORD_FORM,
    TYPES, _TEXT_OF, basic_tables, block_findings, block_path, cited_value_findings, closed_set, closed_set_findings,
    _indent, construct_keys, declared_types, derive, opens_key, parse_records, part_citation, read_block, read_fact,
    record_citation, row_citation, type_of, value_of)
from spec_text import (  # noqa: E402
    HEADING, REGISTRY, REGISTRY_RULE, SCOPE_HOME, headings, lineages, md_files, parse_citation, read, registry, resolve, scope_paths,
    sections, skill_dirs, strip_fences)


LINK_RULE = "sourcing-and-citation.md § Writing a Citation § A Citation's Link"

# @canon-spec specs/methodology/scope.md § What Spec of Record Governs
SCOPE_KINDS = {"Agent instructions", "Specs", "Skills", "Documentation", "Working files", "Code"}
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
# The tables in the audit skill naming what reads or carries out each section stating rules:
# (section heading, the column naming the sections)
COVERAGE_TABLES = (("The audits", "Enforces"), ("Operating rules carried out by a step", "Section"))
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
FENCE = re.compile(r'^```', re.M)

# specs/methodology/spec-style.md § Ordinals and Counts. The findings are the forms a pattern decides alone.
ORDINALS_RULE = "spec-style.md § Ordinals and Counts"
NUMBERED_LEAD_IN = re.compile(r'^\*\*\d+[.)]\s')
NUMBERED_ITEM = re.compile(r'^\s*\d+[.)]\s')
# @canon-spec specs/methodology/working-files.md § The Working Files
WORKING_FILE = re.compile(r'\.ai/(?:plans\b|follow-ups\.md|tmp\b)')
WORKING_FILES_HOME = "specs/methodology/working-files.md"

IMPACTS_CITED = ("specs/methodology/spec-placement.md § Open Question",)


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
# spec-placement.md § Environments: the environments file, and the closed set of kinds
ENVIRONMENTS = "specs/application/technical/environments.md"
# @canon-spec specs/methodology/spec-placement.md § Environments
KINDS = ("local", "integration", "shared", "production")
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


def unnamed_record_sections(r, body):
    """modeling-constructs.md § Constructs § Record Form: the lineage of each section of file `r` holding a Records
    field whose title is the Plural Name of no type whose records may sit there."""
    live = strip_fences(body).split("\n")
    return {lineage for lineage, (h, end) in sections(body).items()
            if not type_of(lineage.split(" § ")[-1], r) and any(_records_key(l) for l in live[h + 1:end])}


def _records_key(line):
    f = opens_key(line)
    return f is not None and f["key"] == "Records" and not f["indent"]


def record_findings(r, body, found):
    """Each record section in a file: its shape, its type's fields, and its placement, each nested record checked
    against the type its field cites; a fenced block whose info string is `markdown` is read as the Markdown it holds,
    its record sections checked against the types the block declares and the canon's."""
    _record_findings(r, body, found, r, 0)
    for start, _, inner in layout.markdown_blocks(body):
        _record_findings(block_path(r, start), inner, found, r, start + 1)


def _record_findings(host, body, found, r, offset):
    """The record sections of `body`, read by the path `host`, a fenced block's own among them, each finding reported
    in file `r` at the body's line plus `offset`."""
    lines = body.split("\n")
    live = strip_fences(body).split("\n")

    def at(i):
        return i + 1 + offset
    for lineage in unnamed_record_sections(host, body):
        found.append((RECORD_FORM, r, at(sections(body)[lineage][0]), f"a record section titled with no declared type's Plural Name: {lineage.split(' § ')[-1]}"))
    for lineage in sections(body):
        title = lineage.split(" § ")[-1]
        spec = type_of(title, host)
        if not spec or spec["home"] == f"{host} § {lineage}":
            continue  # no type's, or its type's own definition, titled with its Plural Name and reported at the declaration
        h, end = sections(body)[lineage]
        # the section fields its type declares, before its Records, read from the section's block through the one
        # reader (modeling-constructs.md § Fields)
        first = next((i for i in range(h + 1, end) if opens_key(live[i]) and not opens_key(live[i])["indent"]), None)
        block = read_block(live, first, 0, end)[0] if first is not None else []
        given = [(f["key"], (value_of(f) if isinstance(value_of(f), str) else "").strip(), f["line"])
                 for f in block if f["key"] in spec["section_fields"]]
        for i in range(h + 1, end):
            mm = opens_key(live[i])
            if _records_key(live[i]):
                break
            if mm and not mm["indent"] and mm["key"] in FIELD_KEYS and mm["key"] not in spec["section_fields"] + ["Diagrams", "Records"]:
                found.append((spec["home"], r, at(i), f"a section field its type does not declare: {mm['key']}"))
        keys = [k for k, _, _ in given]
        if keys != [f for f in spec["section_fields"] if f in keys]:
            found.append((spec["home"], r, at(h), f"a record section's section fields are {keys}, not in the order {spec['section_fields']}"))
        for f in spec["section_required"]:
            if f not in keys:
                found.append((spec["home"], r, at(h), f"a record section without the section field its type requires: {f}"))
        for k, v, i in given:
            if spec["section_defaults"].get(k) == v:
                found.append((spec["home"], r, at(i), f"the {k} field written at its default value, {v}"))
            if k in spec["section_values"] and v not in spec["section_values"][k]:
                found.append((spec["home"], r, at(i), f"the {k} field holds a value its type does not allow: {v}"))
        if spec["last_top_level"] and (" § " in lineage or end != len(lines)):
            found.append((spec["home"], r, at(h), f"the {title} section is not its file's last top-level section"))
        records, problems = parse_records(body, lineage, spec["section_fields"])
        for rule, i, msg in problems:
            found.append((rule, r, at(i), msg))
        _check_records(records, spec, host, r, at, found, f"the {title} section")


def _check_records(records, spec, host, r, at, found, scope):
    """modeling-constructs.md § Constructs § Record Form: each record of one collection, a record section's own items
    or the records one field holds, against its type: its fields, their order, its required fields, its values, its
    identifying values and its unique fields, and each field holding records checked against the type it cites in
    turn."""
    home, names, given = spec["home"], set(), set()
    for rec in records:
        line = at(rec[0][2])
        if rec[0][0] is None:
            found.append((home, r, line, f"an item of {scope} that is no record of its type, opening with no field"))
            continue
        keys = [key for key, _, _ in rec]
        if keys[0] not in spec["fields"]:
            found.append((home, r, line, f"an item of {scope} that is no record of its type, opening with no field its type gives: {keys[0]}"))
            continue
        if keys != [f for f in spec["fields"] if f in keys] or any(k not in spec["fields"] for k in keys):
            found.append((home, r, line, f"a record's fields are {keys}, not {spec['fields']} in that order"))
            continue
        missing = [f for f in spec["required"] if f not in keys]
        if missing:
            found.append((home, r, line, f"a record without the field its type requires: {', '.join(missing)}"))
            continue
        values = {key: value for key, value, _ in rec}
        for key, value in values.items():
            if key in spec["holds"]:
                held, many = spec["holds"][key]
                if not isinstance(value, list):
                    found.append((home, r, line, f"a field holding records whose value is no list of records: {key}"))
                    continue
                if not many and len(value) > 1:
                    found.append((home, r, line, f"a field holding one record holding more than one item: {key}"))
                held_spec = type_of(held, host)
                if held_spec:
                    _check_records(value, held_spec, host, r, at, found, f"the {key} field")
                continue
            if isinstance(value, list):
                found.append((home, r, line, f"the {key} field holds records where its Values hold none"))
                continue
            if spec["defaults"].get(key) == value:
                found.append((home, r, line, f"the {key} field written at its default value, {value}"))
            if key in spec["values"] and value not in spec["values"][key]:
                found.append((home, r, line, f"the {key} field holds a value its type does not allow: {value}"))
            # resolved in the file declaring the field, where its citation is written
            origin = spec.get("origin", {}).get(key)
            members = closed_set(strip_fences(_TEXT_OF[origin]), spec["cited"][key], origin) if key in spec["cited"] and origin in _TEXT_OF else None
            if members is not None and value not in members:
                found.append((home, r, line, f"the {key} field holds a value its closed set does not: {value}"))
        for key in spec["identifying"]:
            if not values.get(key):
                found.append((RECORD_FORM, r, line, f"an identifying value left blank: {key}"))
        ident = tuple(str(values.get(key, "")) for key in spec["identifying"])
        if ident in names:
            found.append((RECORD_FORM, r, line, f"two records of {scope} share their identifying values: {ident}"))
        names.add(ident)
        for key in [f for f in spec["unique"] if [f] != spec["identifying"]]:
            if values.get(key) and (key, str(values[key])) in given:
                found.append((RECORD_FORM, r, line, f"two records of {scope} share a value of {key}, a field unique on its own: {values[key]}"))
            given.add((key, str(values.get(key))))
        if spec["home"] in IMPACTS_CITED and "Impacts" in values and not CITATION.search(str(values["Impacts"])):
            found.append((home, r, line, "a record's Impacts carries no section citation"))



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
        f = opens_key(lines[j]) if j is not None else None
        mm = re.fullmatch(r"(\S+)", (f["value"] or "").strip()) if f and f["key"] == "Kind" and not f["indent"] else None
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
    """modeling-constructs.md § Fields: each field's key is one a form declares, and it sits where that form places it,
    a record's fields, a nested record's among them, placed by the one reader through the type its field cites."""
    raw = body.split("\n")
    live = strip_fences(body).split("\n")
    secs = sorted(sections(body).items(), key=lambda x: x[1][0])
    unnamed = unnamed_record_sections(r, body)
    # the lines the reader places as a record's fields, in a record section of a known type, at any depth
    placed = set()
    for lineage in sections(body):
        spec = type_of(lineage.split(" § ")[-1], r)
        if spec and spec["home"] != f"{r} § {lineage}":
            records, _ = parse_records(body, lineage, spec["section_fields"])
            todo = list(records)
            while todo:
                rec = todo.pop()
                for key, value, i in rec:
                    placed.add(i)
                    if isinstance(value, list):
                        todo += value
    for i, line in enumerate(live):
        mm = FIELD_LINE.match(line)
        if not mm or i in placed:
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
            # modeling-constructs.md § Defining Constructs § Declaring a Construct: a field of the construct's block
            ok = not indent and not dash
        else:
            ok = spec is not None and key in spec["fields"] and bool(indent or dash)
        if not ok:
            found.append((FIELDS, r, i + 1, f"the {key} field outside the place its form gives it"))



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


def diagram_findings(r, body, text_of, known, lineage, found):
    """modeling-constructs.md § Diagrams: each diagram's form, its Caption and Sources a block of fields read through the
    one reader, and its sources citing it back."""
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
        first = opens_key(rest[0][1]) if rest else None
        if not first or first["key"] != "Caption" or first["indent"]:
            found.append((rule, r, start + 1, "a diagram not followed by its **Caption:**"))
            continue
        stop = rest[-1][0] + 1
        fields, after = read_block(lines, rest[0][0], 0, stop)
        keys = [f["key"] for f in fields]
        caption = fields[0]
        if any(CITATION.search(l) or WHOLE_FILE.search(l) for l in [lines[i] for i in caption["lines"]]):
            found.append((rule, r, caption["line"] + 1, "a diagram's caption carries a citation"))
        if "Sources" not in keys:
            found.append((rule, r, start + 1, "a diagram's caption not followed by its **Sources:**"))
            continue
        sources = fields[keys.index("Sources")]
        if keys != ["Caption", "Sources"] or any(i for i in range(after, stop) if lines[i].strip()):
            found.append((rule, r, start + 1, "a diagram's section holds something other than its diagram, its Caption and its Sources"))
        if sources["inline"]:
            found.append((rule, r, sources["line"] + 1, "a diagram's Sources written on its key's line, not beneath it"))
        cites = []
        for it in sources["items"] or []:
            mm = re.fullmatch(r'`([^`]+)`', it["text"] or "") if it["fields"] is None else None
            if not mm:
                found.append((rule, r, it["line"] + 1, "a diagram's section holds something other than one citation per Sources bullet"))
                continue
            if "§" not in mm.group(1):
                found.append((rule, r, it["line"] + 1, f"a Sources bullet is not a section citation: {mm.group(1)}"))
                continue
            cites.append((it["line"], mm.group(1)))
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
                k = next((k for k, l in enumerate(own) if opens_key(l) and opens_key(l)["key"] == "Diagrams"), None)
                field = []
                if k is not None:
                    # the Diagrams field's list, read through the one reader (modeling-constructs.md § Fields)
                    fields, _ = read_block(own, k, _indent(own[k]), len(own))
                    field = (value_of(fields[0]) or "").split("\n") if fields else []
                own = field
            for l in own:
                for cm in CITATION.finditer(l):
                    if resolve(cm.group(1), path) == (r, dlin):
                        back = True
            if not back:
                found.append((rule, r, i + 1, f"source does not cite the diagram back: {c}"))



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
            f = opens_key(after)
            opens = re.match(r"(.+) Elements$", (f["value"] or "").strip()) if f and f["key"] == "Table Name" else None
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
    STANDARDS.update(m["value"].strip() for l in (read(register).split("\n") if register.exists() else [])
                     for m in [FIELD_LINE.match(l)] if m and m["marker"] and m["key"] == "Name" and m["value"])
    # spec-style.md § Blank Lines and modeling-constructs.md § Fields: the layout check and the reader's checks of a
    # block, over every file in scope, the rule's table read from the canon once
    blank_lines, table_problems = layout.rules(root)
    found += table_problems
    # modeling-constructs.md § Constructs: the construct checks whole, the record types, facts and Reference Keys they
    # read set up first and left in place, the citation checks reading them
    construct_found, construct_warned, _ = constructs.run_checks(text_of)
    found += construct_found
    warned += construct_warned

    for f in files:
        r, body = rel[f], text[f]
        live = strip_fences(body)
        src_layer = layer_of(r)
        found += [(rule, r, line, msg) for rule, line, msg in layout.findings(body, blank_lines)]
        found += [(rule, r, line, msg) for rule, line, msg in block_findings(body)]
        code = layout.code_lines(live)

        # Fenced blocks are stripped: a citation shown inside an example is an
        # illustration, not a dependency, and linting one produces a finding
        # nobody can act on.
        for i, line in enumerate(live.split("\n"), 1):
            # spec-style.md § Literal Text: a code span opens and closes with one backtick; a line the layout
            # reading gives an indented code block is literal as a fenced one is
            if "``" in constructs.CITATION.sub(lambda m: "" if _span_fits(m) else m.group(0), line) and (i - 1) not in code:
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
                path, target, sel = parse_citation(cite, r)

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
    named, itself or through a section it sits under, in the column naming the sections in one of
    the audit skill's coverage tables, or, for a section of code.md, in the verify skill's table of checks;
    and each section stating operating rules is cited, itself or through a section it
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
                          f"no registered skill's Workflow step cites the section stating operating rules {path} § {target}"))
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
    held = {m["value"].strip() for l in clear_prose(root).split("\n") for m in [opens_key(l)] if m and m["key"] == "Table Name" and m["value"]}
    return [("spec-style.md § Clear Prose", STYLE_RULE_FILE, 0,
             f"no table named {t}, which the script reads its words from") for t in VOICE_TABLES if t not in held]


def voice_terms(root):
    """-> a pattern of the terms the tables VOICE_TABLES name in spec-style.md § Clear Prose, a term
    matched with a plain ending, or None."""
    body = clear_prose(root)
    terms, table = [], None
    for line in body.split("\n"):
        m = opens_key(line)
        if m and m["key"] == "Table Name":
            table = (m["value"] or "").strip()
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
    parser.add_argument("--check-layout", nargs="+", metavar="FILE",
                        help="run the layout check and the reader's checks of a block over the given Markdown files alone, "
                             "as the Working-file form audit runs them over .ai/follow-ups.md; exits 1 on any finding")
    parser.add_argument("--root", metavar="DIR", default=".",
                        help="the project root the scope is read from; the current directory unless given")
    args = parser.parse_args(argv[1:])
    if not (args.check_scope or args.list_candidates or args.check_layout):
        parser.print_usage(sys.stderr)
        return 2
    root = Path(args.root).resolve()
    if not (root / "specs").is_dir():
        parser.error(f"--root {args.root} holds no specs/ directory")
    status = 0

    if args.check_layout:
        table, found = layout.rules(root)
        for value in args.check_layout:
            path = Path(value)
            if not path.is_file():
                parser.error(f"--check-layout names no file: {value}")
            body = read(path)
            rel = path.resolve().relative_to(root).as_posix() if path.resolve().is_relative_to(root) else value
            found += [(rule, rel, line, msg) for rule, line, msg in layout.findings(body, table) + block_findings(body)]
        for rule, path, line, msg in sorted(found):
            print(f"{path}:{line}  {rule}\n  {msg}")
        n = len(found)
        print(f"\n{n} finding{'' if n == 1 else 's'} over {len(args.check_layout)} file{'' if len(args.check_layout) == 1 else 's'}")
        status = 1 if n else 0

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
        text_of = {f.relative_to(root).as_posix(): read(f) for f in md_files(root)}
        for path, line, name, context in constructs.run_checks(text_of)[2]:
            print(f"  {path}:{line}  [{name}]\n    {context}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
