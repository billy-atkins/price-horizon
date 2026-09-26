#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment: a check that cannot decide
is worse than no check, because a confident false clear is harder to notice than a
missing one. `--candidates` decides nothing either: it lists places for a reading
audit to look, printed apart from the findings and never affecting the exit status.

Standard library only. See SKILL.md.
"""

import re
import sys
from pathlib import Path

SCOPE = ["specs", "AGENTS.md", ".ai/skills", "README.md"]
# Scripts are read only for candidates: the findings are Markdown forms.
SCRIPT_SCOPE = [".ai/skills", "scripts"]
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

# AGENTS.md § Ordinals and Counts. The findings are the forms a pattern decides alone.
NUMBERED_LEAD_IN = re.compile(r'^\*\*\d+[.)]\s')
NUMBERED_ITEM = re.compile(r'^\s*\d+[.)]\s')
WORKING_FILE = re.compile(r'\.ai/(?:designs\.md|follow-ups\.md|tmp\b)')
WORKING_FILES_HOME = "specs/methodology/working-files.md"

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


def md_files(root):
    out = []
    for s in SCOPE:
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
    """A citation's (file, lineage); a same-file form resolves to its host."""
    cite = cite.strip()
    if cite.startswith("§"):
        return host, cite.lstrip("§ ").strip()
    path, _, target = cite.partition(" § ")
    return path.strip(), target.strip()


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
    return "agents" if rel == "AGENTS.md" else None


def direction(src_layer, path, rel, line, found):
    """A citation never points down a layer except from AGENTS.md, and application
    and methodology never cite each other in either direction. Shared by both
    citation forms."""
    dst_layer = layer_of(path)
    if not (src_layer and dst_layer and src_layer != dst_layer):
        return
    bad = (
        (src_layer == "methodology" and dst_layer in ("product", "technical"))
        or (src_layer in ("product", "technical") and dst_layer == "methodology")
        or (src_layer == "product" and dst_layer == "technical")
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
            if NUMBERED_LEAD_IN.match(line):
                found.append(("AGENTS.md § Ordinals and Counts", r, i, "bold lead-in carries a number"))
            elif NUMBERED_ITEM.match(line):
                found.append(("AGENTS.md § Ordinals and Counts", r, i, "list item carries a number"))
            if r.startswith("specs/") and r != WORKING_FILES_HOME:
                for m in WORKING_FILE.finditer(line):
                    found.append(("sourcing-and-citation.md § Which Citations Are Allowed", r, i,
                                  f"names a working file: {m.group(0)}"))
            for m in WHOLE_FILE.finditer(line):
                if m.group(1) in known:
                    direction(src_layer, m.group(1), r, i, found)

            for m in CITATION.finditer(line):
                cite = m.group(1).strip()
                if " § " not in cite and not cite.startswith("§"):
                    continue
                if cite.startswith("§"):
                    target, path = cite.lstrip("§ ").strip(), r
                else:
                    path, _, target = cite.partition(" § ")
                    path, target = path.strip(), target.strip()

                # lineage resolves
                if path not in known:
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  f"cites a file that does not exist: {path}"))
                    continue
                if target not in lineage[path]:
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  f"no such heading path in {path}: § {target}"))

                # direction
                direction(src_layer, path, r, i, found)

                # index.md is never a target
                if path.endswith("index.md"):
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  "cites an index.md, which is never a citation target"))

                # cross-file citations use a project-root path
                if path != r and not path.startswith("specs/") and path != "AGENTS.md":
                    found.append(("sourcing-and-citation.md § Writing a Citation", r, i,
                                  f"not a project-root path: {path}"))

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

    # every directory has an index.md
    for d in sorted({f.parent for f in files if "specs" in f.parts}):
        if not (d / "index.md").exists():
            found.append(("spec-placement.md § Where a File Goes",
                          d.relative_to(root).as_posix(), 0, "directory has no index.md"))

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
    for s in SCRIPT_SCOPE:
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


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = [a for a in argv[1:] if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path.cwd()
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

    if "--candidates" in argv:
        print("\nCandidates for AGENTS.md § Ordinals and Counts: places to read, not findings")
        for path, line, name, context in candidates(root):
            print(f"  {path}:{line}  [{name}]\n    {context}")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
