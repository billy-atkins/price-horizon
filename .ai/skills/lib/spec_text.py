"""The reading of a spec's text that the skills' scripts share: its fenced blocks, its headings, its sections and
their lineages, where a citation resolves, and which files are in scope, by the skills registry, and their texts.
audit-specs, design-specs, implement-specs and verify-spec-implementation read a spec through it, each reading this
one copy (specs/methodology/skills.md § Authoring a Skill)."""
import re
from pathlib import Path

import citation_links


# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link
def read(path):
    """-> a file's text with each citation's link stripped, so every check reads the citation as written."""
    return citation_links.strip(Path(path).read_text(encoding="utf-8"))


HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*$', re.M)


RECORD_SELECTOR = re.compile(r'^(.*?)\s+\[(.*)\]$')


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


def parse_citation(cite, host):
    """A citation's (file, lineage, selector); a same-file form resolves to its host, and the selector is the text of
    a record or part citation's `[...]`, or None."""
    cite = cite.strip()
    if cite.startswith("§"):
        path, target = host, cite.lstrip("§ ").strip()
    else:
        path, _, target = cite.partition(" § ")
        path, target = path.strip(), target.strip()
    m = RECORD_SELECTOR.match(target)
    return (path, m.group(1).strip(), m.group(2)) if m else (path, target, None)


def resolve(cite, host):
    """A citation's (file, lineage); a same-file form resolves to its host. A record
    citation's `[...]` selector is dropped: this names the record section holding it."""
    path, target, _ = parse_citation(cite, host)
    return path, target


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


# @canon-spec specs/methodology/scope.md § What Spec of Record Governs
# specs/methodology/scope.md § What Spec of Record Governs names where each kind is named:
# specs by their place under specs/, the agent instructions by the root AGENTS.md and
# specs/AGENTS.md, the documentation by README.md and docs/, and skills by the registry, read at
# run time. The places and names this block defines are the ones scope.md's table gives;
# the working files are outside the script, read by the Working-file form audit instead, and code
# is outside audit-specs, which audits every kind but code.
SCOPE_HOME = "scope.md § What Spec of Record Governs"


REGISTRY = "specs/methodology/skills.md"


REGISTRY_RULE = "skills.md § Registered Skills"


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


def spec_texts(root):
    """-> {path from the root: text, citations' links stripped} for every Markdown file in scope."""
    root = Path(root)
    return {f.relative_to(root).as_posix(): read(f) for f in md_files(root)}
