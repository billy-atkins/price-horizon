#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment, per
specs/methodology/scope.md § Rules and Skills. `--check-scope` runs the checks, and
`--list-candidates` lists places for a reading audit to look, printed apart from any
finding and never affecting the exit status.

Standard library only. See SKILL.md.
"""

import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

# specs/methodology/scope.md § What Spec of Record Governs names where each kind is named:
# specs by their place under specs/, the agent instructions by the root AGENTS.md and
# specs/AGENTS.md, and skills by the registry, read at run time. The places and names this
# block defines are the ones scope.md's table gives, and scope_findings checks the table still says so;
# the working files are outside the script, read by the Working-file form audit instead, and code
# is outside this skill, which audits every kind but code.
SCOPE_HOME = "scope.md § What Spec of Record Governs"
SCOPE_KINDS = {"Agent instructions", "Specs", "Skills", "Working files", "Code"}
REGISTRY = "specs/methodology/skills.md"
REGISTRY_RULE = "skills.md § Registered Skills"
AUTHORING = "specs/methodology/skills.md § Authoring a Skill"
SCOPE_TREE = "specs/methodology/scope.md"
SPECS_AGENTS = "specs/AGENTS.md"
GLOSSARY = "specs/methodology/glossary.md"
GLOSSARY_RULE = "glossary.md § Writing an Entry"
AUDIT_SKILL = ".ai/skills/audit-specs/SKILL.md"
CODE_CHECKS = ".ai/skills/verify-spec-implementation/SKILL.md"  # names the check enforcing each section of code.md
COVERAGE_RULE = "scope.md § Rules and Skills"
# The tables in the audit skill naming what reads or carries out each rule section:
# (section heading, rule column header)
COVERAGE_TABLES = (("The audits", "Enforces"), ("Operating rules carried out by a step", "Operating rule"))
DIAGRAMS_RULE = "modeling-constructs.md § Diagrams"
IMAGE = re.compile(r"!\[[^\]]*\][(\[]|<img\b", re.I)
WORKING_FILES = "specs/methodology/working-files.md"
WORKING_FILES_RULE = "working-files.md § The Working Files"
SCRIPT_SUFFIXES = {".py", ".ps1", ".sh"}
LAYER = {"methodology": "specs/methodology/", "product": "specs/application/product/",
         "technical": "specs/application/technical/"}
ROLE_TABLE = "specs/application/product/roles.md"

# A citation is `§ Title` or `path/to.md § Title`. A backtick span merely containing the
# section token is not one: `§` alone, or `## § Vision` shown as a forbidden heading form,
# are the token being discussed rather than used.
CITATION = re.compile(r'`((?:[\w./-]+\.md\s*)?§\s+[^`]+)`')
# A whole file is a valid citation form and carries no section token, so CITATION
# never sees one. Only the direction check applies to it: naming a file in another
# layer is the same dependency whether or not a section is named. The span must
# resolve to a known file, so a passing mention of a directory is not read as one.
WHOLE_FILE = re.compile(r'`([\w./-]+\.md)`')
LOOSE_SECTION = re.compile(r'(?<!`)§')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*$', re.M)
FENCE = re.compile(r'^```', re.M)

# specs/AGENTS.md § Ordinals and Counts. The findings are the forms a pattern decides alone.
NUMBERED_LEAD_IN = re.compile(r'^\*\*\d+[.)]\s')
NUMBERED_ITEM = re.compile(r'^\s*\d+[.)]\s')
WORKING_FILE = re.compile(r'\.ai/(?:plans\b|follow-ups\.md|tmp\b)')
WORKING_FILES_HOME = "specs/methodology/working-files.md"

# modeling-constructs.md § Constructs § Record Form. The record-type registry: each type's
# name, which titles its record sections, its record fields in order, and which of them
# identify a record, and any section fields of its own beyond Diagrams. Adding a type
# means adding it here; FIELD_KEYS takes its keys from this registry.
RECORD_FORM = "modeling-constructs.md § Constructs § Record Form"
RECORD_TYPES = {
    "Open Questions": {
        "fields": ["Name", "Open Question", "Provisional Answer", "Impacts"],
        "identifying": ["Name"],
        "section_fields": [],
        "home": "spec-placement.md § An Open Question",
        "last_top_level": True,
    },
}
# modeling-constructs.md § Fields: every key a form declares, and where that form places it.
FIELDS = "modeling-constructs.md § Fields"
FIELD_KEYS = {"Caption": "diagram", "Sources": "diagram",
              "Diagrams": "record section", "Records": "record section", "Kind": "environment"}
# spec-placement.md § Environments: the environments file, and the closed set of kinds
ENVIRONMENTS = "specs/application/technical/environments.md"
KINDS = ("local", "integration", "shared", "production")
for _type, _spec in RECORD_TYPES.items():
    for _key in _spec["fields"]:
        FIELD_KEYS[_key] = "record"
    for _key in _spec["section_fields"]:
        FIELD_KEYS[_key] = "record section"
# A field opens a line with its key in bold, the colon inside the bold; a list marker and
# indentation before the key are no part of it.
FIELD_LINE = re.compile(r'^(\s*)(-\s+)?\*\*([^*`]+?):\*\*(?:\s|$)')
RECORD_SELECTOR = re.compile(r'^(.*?)\s+\[(.*)\]$')
# modeling-constructs.md § Bold Lead-ins and § Emphasis: bold marks only a field or a dash
# label, both opening a line, and italic, the one emphasis, never opens one.
BOLD_SPAN = re.compile(r'\*\*(.+?)\*\*')
# a line's opening skips indentation, a quote marker, and a list marker: -, *, + or a number
LIST_OR_QUOTE = r'\s*(?:>\s*)*(?:(?:[-*+]|\d+[.)])\s+)?'
LINE_OPENING = re.compile(r'^' + LIST_OR_QUOTE + r'$')
ITALIC_OPENING = re.compile(r'^' + LIST_OR_QUOTE + r'\*(?!\*)\S')
ODD_EMPHASIS = re.compile(r'\*\*\*|__[^_\s][^_]*__')
BOLD_LEAD_INS = "modeling-constructs.md § Bold Lead-ins"
EMPHASIS = "modeling-constructs.md § Emphasis"
KEY_VALUE = re.compile(r'^([A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*(?: [A-Z0-9][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)*): (.+)$')
UNPLAIN = re.compile(r'[*_`§;\]\[]')

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
    for n, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
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
    """The files in scope: the root AGENTS.md, specs/, each registered skill, and the code they share."""
    return ["AGENTS.md", "specs"] + [".ai/skills/" + n for n in skill_dirs(root)]


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


def parse_records(body, lineage):
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
            current = [(mm.group(3), text[mm.end():].strip(), i)] if mm else [(None, "", i)]
            records.append(current)
            if not mm:
                problems.append((RECORD_FORM, i, "a record does not open with a field"))
        elif text.startswith("  ") and current is not None:
            mm = FIELD_LINE.match(text)
            if mm and len(mm.group(1)) == 2 and not mm.group(2):
                current.append((mm.group(3), text[mm.end():].strip(), i))
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
    for lineage in sections(body):
        title = lineage.split(" § ")[-1]
        spec = RECORD_TYPES.get(title)
        if not spec:
            continue
        home = spec["home"]
        h, end = sections(body)[lineage]
        if spec["last_top_level"] and (" § " in lineage or end != len(lines)):
            found.append((home, r, h + 1, f"the {title} section is not its file's last top-level section"))
        records, problems = parse_records(body, lineage)
        for rule, at, msg in problems:
            found.append((rule, r, at + 1, msg))
        names = set()
        for rec in records:
            keys = [key for key, _, _ in rec]
            at = rec[0][2] + 1
            if keys != spec["fields"]:
                found.append((home, r, at, f"a record's fields are {keys}, not {spec['fields']}"))
                continue
            values = {key: value for key, value, _ in rec}
            for key in spec["identifying"]:
                if not values[key] or UNPLAIN.search(values[key]):
                    found.append((RECORD_FORM, r, at, f"an identifying value is not plain text: {key}: {values[key]}"))
            ident = tuple(values[key] for key in spec["identifying"])
            if ident in names:
                found.append((RECORD_FORM, r, at, f"two records share their identifying values: {ident}"))
            names.add(ident)
            if "Impacts" in values and not CITATION.search(values["Impacts"]):
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


def field_findings(r, body, found):
    """modeling-constructs.md § Fields: each field's key is one a form declares, it sits
    where that form places it, and a key at the left margin follows a blank line."""
    raw = body.split("\n")
    live = strip_fences(body).split("\n")
    secs = sorted(sections(body).items(), key=lambda x: x[1][0])
    for i, line in enumerate(live):
        mm = FIELD_LINE.match(line)
        if not mm:
            continue
        indent, dash, key = mm.group(1), mm.group(2), mm.group(3)
        owner = [(lin, s) for lin, s in secs if s[0] < i < s[1]]
        lineage, (h, end) = owner[-1] if owner else ("", (-1, len(raw)))
        title = lineage.split(" § ")[-1]
        place = FIELD_KEYS.get(key)
        if place is None:
            found.append((FIELDS, r, i + 1, f"a field whose key no form declares: {key}"))
            continue
        if place == "diagram":
            ok = any(raw[j].startswith("```mermaid") for j in range(h + 1, end))
        elif place == "record section":
            ok = title in RECORD_TYPES and not indent and not dash
        elif place == "environment":
            ok = r == ENVIRONMENTS and not indent and not dash
        else:
            ok = title in RECORD_TYPES and key in RECORD_TYPES[title]["fields"] and bool(indent or dash)
        if not ok:
            found.append((FIELDS, r, i + 1, f"the {key} field outside the place its form gives it"))
        # Record Form: a blank line precedes each section field, at the left margin, or
        # Markdown renders it inside the line above; a record's own fields are stacked
        if title in RECORD_TYPES and not indent and not dash and i > 0 and raw[i - 1].strip():
            found.append((RECORD_FORM, r, i + 1, f"the {key} field directly after a non-blank line"))


def record_citation(sel, path, target, text_of, r, line, found):
    """sourcing-and-citation.md § Writing a Citation: a record citation names every
    identifying field of its type, in order, and matches exactly one record."""
    rule = "sourcing-and-citation.md § Writing a Citation"
    title = target.split(" § ")[-1]
    spec = RECORD_TYPES.get(title)
    if not spec:
        found.append((rule, r, line, f"a record citation on a section that is no record section: § {target}"))
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
    records, _ = parse_records(text_of[path], target)
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
            if target.split(" § ")[-1] in RECORD_TYPES:
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
    level 2. This is why `§ Citation Format` resolves in a file whose first line is
    `# PriceHorizon — Agent Instructions`.
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
    if rel == SPECS_AGENTS:
        return "agents"
    return "project" if rel == "AGENTS.md" else None


def direction(src_layer, path, rel, line, found, section=True):
    """A citation never points down a layer except from specs/AGENTS.md; application and
    methodology never cite each other in either direction; an application spec never
    cites specs/AGENTS.md; and no spec cites a section of the project's root AGENTS.md,
    though a plain mention of it is no citation of its content. Shared by both forms."""
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


def check(root):
    """-> list of (rule, path, line, message)."""
    found, files = [], md_files(root)
    text = {f: f.read_text(encoding="utf-8") for f in files}
    rel = {f: f.relative_to(root).as_posix() for f in files}
    lineage = {rel[f]: lineages(text[f]) for f in files}
    known = set(rel.values())
    text_of = {rel[f]: text[f] for f in files}

    # roles, for the scenario-actor check
    roles = set()
    rt = root / ROLE_TABLE
    if rt.exists():
        for line in rt.read_text(encoding="utf-8").split("\n"):
            m = re.match(r'\|\s*([A-Z][A-Za-z ]+?)\s*\|', line)
            if m and m.group(1) not in ("Role", "Field", "Step"):
                roles.add(m.group(1).strip())

    for f in files:
        r, body = rel[f], text[f]
        live = strip_fences(body)
        src_layer = layer_of(r)

        # Fenced blocks are stripped: a citation shown inside an example is an
        # illustration, not a dependency, and linting one produces a finding
        # nobody can act on.
        for i, line in enumerate(live.split("\n"), 1):
            # a code span is literal text, so markup inside one is never bold or italic
            prose = re.sub(r'`[^`]*`', lambda m: "x" * len(m.group(0)), line)
            for m in BOLD_SPAN.finditer(prose):
                if not LINE_OPENING.match(prose[:m.start()]):
                    found.append((EMPHASIS, r, i, f"bold outside a line's opening: {line[m.start():m.end()][:60]}"))
                elif not (m.group(1).endswith(":") or m.group(1).endswith(" —")):
                    found.append((BOLD_LEAD_INS, r, i, f"bold opening a line closes on neither a colon nor a dash: {line[m.start():m.end()][:60]}"))
            if ITALIC_OPENING.match(prose):
                found.append((EMPHASIS, r, i, "a line opens with italic"))
            if ODD_EMPHASIS.search(prose):
                found.append((EMPHASIS, r, i, "bold italic or underscore bold"))
            if NUMBERED_LEAD_IN.match(line):
                found.append(("specs/AGENTS.md § Ordinals and Counts", r, i, "bold lead-in carries a number"))
            elif NUMBERED_ITEM.match(line):
                found.append(("specs/AGENTS.md § Ordinals and Counts", r, i, "list item carries a number"))
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

                # direction
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
            stripped = re.sub(r'`[^`]*`', "", line)
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

        # mermaid blocks: declared as flowcharts, in the form a diagram takes, and cited
        # back by their sources. Scoped to specs/ because a skill may legitimately carry a
        # worked example. The fence is found in the raw text: strip_fences() blanks it.
        if r.startswith("specs/"):
            diagram_findings(r, body, text_of, known, lineage, found)
            record_findings(r, body, found)
            field_findings(r, body, found)
            environment_findings(r, body, found)
            for m in re.finditer(r'^```mermaid\s*\n(.*?)^```', body, re.S | re.M):
                # a diagram opens with a config frontmatter block, so scan the whole
                # fence rather than its first line
                if not re.search(r'^\s*flowchart\b', m.group(1), re.M):
                    found.append(("modeling-constructs.md § Diagrams", r, 0,
                                  "a mermaid block that does not declare flowchart"))

        # technical-specs frontmatter: product files only, paths under technical/
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
                                  r, 0, "technical-specs is not alphabetically sorted"))
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
        named = set(re.findall(r'^\|\s*`([^`]+)`', idx.read_text(encoding="utf-8"), re.M))
        present = {c.name + ("/" if c.is_dir() else "") for c in d.iterdir()
                   if c.name != "index.md" and (c.is_dir() or c.suffix == ".md")}
        for missing in sorted(present - named):
            found.append(("spec-placement.md § Where a File Goes", rel_d + "/index.md", 0, f"no row names {missing}"))
        for extra in sorted(named - present):
            found.append(("spec-placement.md § Where a File Goes", rel_d + "/index.md", 0, f"a row names {extra}, which is not here"))

    found += scope_findings(root)
    found += glossary_findings(root)
    found += coverage_findings(root)
    found += ignored_findings(root)
    found += reviewer_findings(root)
    found += image_findings(root)
    return found


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
        for n, line in enumerate(strip_fences(f.read_text(encoding="utf-8")).split("\n"), 1):
            if IMAGE.search(re.sub(r'`[^`]*`', "", line)):
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
            body = level2_section(strip_fences(f.read_text(encoding="utf-8")), "Workflow") if f.exists() else None
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
    text, named, operating, found = sk.read_text(encoding="utf-8"), set(), set(), []
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
    table = first_table(checks.read_text(encoding="utf-8"), "The checks", "Enforces") if checks.exists() else None
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
        for lin in sections(f.read_text(encoding="utf-8")):
            parts = lin.split(" § ")
            if not any((rel, " § ".join(parts[:k])) in named for k in range(1, len(parts) + 1)):
                found.append((COVERAGE_RULE, rel, 0, f"no check or step names § {lin}"))
    return found


def ignored_findings(root):
    """Each working file the working-files table names is ignored by a line of .gitignore
    naming it or a directory holding it, and un-ignored by none. A line ending in a slash
    names a directory only, as git reads it."""
    wf = root / WORKING_FILES
    table = first_table(wf.read_text(encoding="utf-8"), "The Working Files") if wf.exists() else None
    if table is None:
        return [(WORKING_FILES_RULE, WORKING_FILES, 0, "no table of working files to check")]
    gi = root / ".gitignore"
    ignored, negated = set(), set()
    if gi.exists():
        for line in gi.read_text(encoding="utf-8").split("\n"):
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
    table = first_table(f.read_text(encoding="utf-8"), "What a Finished Spec Reads Like", "Example") if f.exists() else None
    if table is None:
        return None
    k = table[0].index("Example")
    phrases = {q.strip(" ,.") for row in table[1] if k < len(row) for q in re.findall(r'"([^"]+)"', row[k])}
    phrases = sorted((p for p in phrases if p), key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(map(re.escape, phrases)) + r")\b", re.I) if phrases else None
VENDOR_NAMES = re.compile(r"\b(Claude|Anthropic|OpenAI|Codex|GPT|Copilot|Cursor|Gemini)\b|CLAUDE\.md|\.claude/|\.cursor/")


def style_and_agent_candidates(root):
    """-> list of (path, line, kind, context), for the Finished style and Agent agnostic audits.
    Places to read, never findings."""
    out, style = [], style_phrases(root)
    for f in md_files(root) if style else []:
        rel = f.relative_to(root).as_posix()
        if not rel.startswith("specs/") or rel in (SPECS_AGENTS, STYLE_RULE_FILE):
            continue
        for n, line in enumerate(strip_fences(f.read_text(encoding="utf-8")).split("\n"), 1):
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
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            m = VENDOR_NAMES.search(line)
            if m and not line.startswith("VENDOR_NAMES"):
                a, b = max(0, m.start() - 60), min(len(line), m.end() + 60)
                out.append((rel, n, "a line naming a vendor, model or tool", line[a:b].strip()))
    return out


# A definition's other names are its trailing sentences: "Abbreviated X." with one name,
# then "Also called X." or "Also called X, Y.", each optional.
OTHER_NAMES = re.compile(r'(?:\s*Abbreviated ([^.,]+)\.)?(?:\s*Also called ([^.]+)\.)?\s*$')
BARE_TERM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ,'-]*$")
TABLE_RULE = re.compile(r'^\|[\s|:-]+\|$', re.M)


def glossary_terms(root):
    """-> (header, [(line, term, other names, definition, where the other names start)]),
    or None when there is no glossary."""
    g = root / GLOSSARY
    if not g.exists():
        return None
    rows, header = [], None
    for n, line in enumerate(g.read_text(encoding="utf-8").split("\n"), 1):
        if not line.startswith("|") or TABLE_RULE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        term, definition = cells[0], "|".join(cells[1:])
        m = OTHER_NAMES.search(definition)
        others = ([m.group(1).strip()] if m.group(1) else []) + \
                 ([x.strip() for x in m.group(2).split(",")] if m.group(2) else [])
        rows.append((n, term, others, definition, m.start(), len(cells)))
    return header, rows


def glossary_findings(root):
    """The glossary cites nothing and holds one table of bare terms, unique and sorted, each
    definition ending with its other names in the fixed form, none shared or equal to a term."""
    got = glossary_terms(root)
    if got is None:
        return [(GLOSSARY_RULE, GLOSSARY, 0, "the glossary is missing")]
    header, rows = got
    found, text = [], (root / GLOSSARY).read_text(encoding="utf-8")
    for n, line in enumerate(strip_fences(text).split("\n"), 1):
        if CITATION.search(line) or WHOLE_FILE.search(line):
            found.append((GLOSSARY_RULE, GLOSSARY, n, "the glossary cites nothing"))
    if header != ["Term", "Definition"]:
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the table's header is not | Term | Definition |"))
    if len(TABLE_RULE.findall(text)) != 1:
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the glossary does not hold exactly one table"))
    folded = [t.casefold() for _, t, _, _, _, _ in rows]
    if folded != sorted(folded):
        found.append((GLOSSARY_RULE, GLOSSARY, 0, "the terms are not in sorted order"))
    owner = {}
    for n, term, others, definition, trail, width in rows:
        if width != 2:
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: a row holds a term and a definition, nothing else"))
        if not definition:
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: no definition"))
        if not BARE_TERM.match(term):
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"not a bare term: {term}"))
        if folded.count(term.casefold()) > 1:
            found.append((GLOSSARY_RULE, GLOSSARY, n, f"the term is listed twice: {term}"))
        if re.search(r'\b(?:Abbreviated|Also called)\b', definition[:trail]):
            found.append((GLOSSARY_RULE, GLOSSARY, n,
                          f"{term}: other names are the trailing sentences, Abbreviated with one name, then Also called"))
        for o in others:
            k = o.casefold()
            if k in folded:
                found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: the other name {o} is a term"))
            elif owner.setdefault(k, term) != term:
                found.append((GLOSSARY_RULE, GLOSSARY, n, f"{term}: the other name {o} also belongs to {owner[k]}"))
    return found


def glossary_candidates(root):
    """-> list of (path, line, kind, context), for the Glossary terms audit: a line outside the
    glossary where a term or one of its other names seems to be defined. Places to read."""
    got, out = glossary_terms(root), []
    if got is None:
        return out
    names = set()
    for _, term, others, _, _, _ in got[1]:
        names.update([term] + others)
    alt = "|".join(sorted((r'\s+'.join(map(re.escape, x.split())) for x in names), key=len, reverse=True))
    name = rf"(?:{alt})s?"
    # A definition equates the term with a kind, "A field is a key-value pair", or glosses it
    # in apposition, "Spec of Record, the method"; "is written" or "is missing" states a rule
    # about the term instead, and a term after an article or a comma is an item in a list.
    defining = re.compile(
        rf"(?:(?:^|[.!?:]\s+|\|\s*|—\s*)|\b(?:a|an|the)\s+){name}\b(?:\s*\([^)]*\)|\s*`[^`]*`)?"
        rf"\s+(?:(?:is|are)\s+(?:a|an|the|one|what|where|how)\b|means\b|names\s+\w)"
        rf"|(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)(?<!,\s)\b{name},\s+(?:a|an|the)\b", re.I)
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        if rel == GLOSSARY:
            continue
        for n, line in enumerate(strip_fences(f.read_text(encoding="utf-8")).split("\n"), 1):
            m = defining.search(line)
            if m:
                a, b = max(0, m.start() - 40), min(len(line), m.end() + 60)
                out.append((rel, n, "a glossary term that may be defined here", line[a:b].strip()))
    return out


def scope_findings(root):
    """scope.md, the skills registry, and each registered skill's form."""
    found = []
    names, problems = registry(root)
    found += problems
    scope = root / SCOPE_TREE
    if not scope.exists():
        return found + [(SCOPE_HOME, SCOPE_TREE, 0, "the scope file is missing")]
    text = scope.read_text(encoding="utf-8")
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
        fm = re.match(r'^---\n(.*?)\n---', (d / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n"), re.S)
        meta = dict(re.findall(r'^(\w+):\s*(.*)$', fm.group(1), re.M)) if fm else {}
        if not fm:
            found.append((AUTHORING, rel, 1, "SKILL.md does not open with YAML front matter"))
        if meta.get("name", "").strip() != n or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)+', n):
            found.append((AUTHORING, rel, 1, f"front matter name is not the kebab-case directory name {n}"))
        if not meta.get("description", "").strip():
            found.append((AUTHORING, rel, 1, "front matter has no description"))
        if level2_section(strip_fences((d / "SKILL.md").read_text(encoding="utf-8")), "Workflow") is None:
            found.append((AUTHORING, rel, 0, "SKILL.md has no ## Workflow section"))
        if (d / "scripts").is_dir() and not (d / "scripts" / (n + ".py")).exists():
            found.append((AUTHORING, f".ai/skills/{n}/scripts", 0, f"no entry-point script named {n}.py"))
    return found


def script_lines(path):
    """-> [(line_no, text)] of a script's comments and docstrings, where its prose is."""
    out, in_doc = [], False
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
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
        md = strip_fences(f.read_text(encoding="utf-8")).split("\n")
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
        for n, line in enumerate(strip_fences(f.read_text(encoding="utf-8")).split("\n"), 1):
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


def skill_candidates(root):
    """An unregistered skill whose SKILL.md cites the method's rules, which may belong to the
    method or may simply follow Authoring a Skill; and a registered skill's script importing
    from outside the standard library, which the rule allows where the standard library
    cannot serve. Places to read, never findings."""
    out, names = [], set(registry(root)[0])
    base = root / ".ai/skills"
    if base.is_dir():
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            sk = d / "SKILL.md"
            if d.name not in names and sk.exists() and re.search(r'specs/(?:methodology/|AGENTS\.md)', sk.read_text(encoding="utf-8")):
                out.append((f".ai/skills/{d.name}/SKILL.md", 0, "unregistered skill citing the method's rules", d.name))
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    if not stdlib:
        out.append(("(this Python)", 0, "imports not checked", "sys.stdlib_module_names needs Python 3.10 or later"))
    # specs/methodology/skills.md § Authoring a Skill: a skill's entry script may import the code the skills share
    lib = {p.stem for p in (base / "lib").glob("*.py")} if (base / "lib").is_dir() else set()
    for n in sorted(names) + (["lib"] if lib else []):
        for py in sorted((base / n).rglob("*.py")):
            for k, line in enumerate(py.read_text(encoding="utf-8").split("\n"), 1):
                m = re.match(r'^\s*(?:import\s+([A-Za-z_]\w*)|from\s+([A-Za-z_]\w*)[\w.]*\s+import\b)', line)
                mod = m and (m.group(1) or m.group(2))
                if mod and stdlib and mod not in stdlib and mod not in lib:
                    out.append((py.relative_to(root).as_posix(), k, "import from outside the standard library", line.strip()))
    return out


def literal_candidates(root):
    """-> list of (path, line, kind, context), for the Markup audit.

    A backtick span naming no heading, field key, path, citation, identifier or markup
    the tree holds may be a name; an italic span of more than a few words may be stress
    that needs structure instead. Places to read, never findings.
    """
    known, out, fenced = set(FIELD_KEYS), [], []
    for f in md_files(root):
        text = f.read_text(encoding="utf-8")
        known.update(title for _, title in headings(text))
        # a span written verbatim in a fenced example, a Gherkin keyword or a Mermaid
        # directive, is literal text the tree itself shows
        fenced += re.findall(r'^```[^\n]*\n(.*?)^```', text, re.S | re.M)
    fenced_words = set(" ".join(fenced).split())
    fenced_text = "\n".join(fenced)
    literal = re.compile(r'[§/._*\[\]:=()<>#;~]|^-|^[a-z0-9-]+$')
    for f in md_files(root):
        rel = f.relative_to(root).as_posix()
        for n, line in enumerate(strip_fences(f.read_text(encoding="utf-8")).split("\n"), 1):
            for m in re.finditer(r'`([^`]+)`', line):
                span = m.group(1)
                if span in known or literal.search(span) or span in fenced_words or span in fenced_text:
                    continue
                out.append((rel, n, "backtick span that may be a name", span))
            prose = re.sub(r'`[^`]*`', "", line)
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
        found = check(root)
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
        print("\nCandidates for the Skill form audit: places to read, not findings")
        for path, line, name, context in skill_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
        print("\nCandidates for the Ordinals and counts audit: text pointed at by direction, places to read, not findings")
        for path, line, name, context in direction_candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
