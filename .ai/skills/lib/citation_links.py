"""A citation's link: the anchor GitHub gives the heading a citation names, the link a citation in a file a person reads
carries, and the link stripped again for a script reading the citation. Run by no agent directly: the design-specs
skill's entry script writes the links, and the audit-specs skill's checks them.

A citation names a heading by its lineage, and GitHub addresses a heading by a flat anchor, its title lower-cased, its
punctuation dropped and its spaces made hyphens, a title met again numbered by its place among the headings of its
file. The citation is resolved to its one heading first, so the anchor reaches that heading even where titles repeat.
"""
import re
import subprocess
from pathlib import Path

# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link
# the files a person reads on GitHub, the only ones carrying links: README.md, the files under docs/, and every spec but
# specs/AGENTS.md
LINKED_ROOTS = ("specs", "docs")
LINKED_FILES = ("README.md",)
UNLINKED_NAMES = ("AGENTS.md",)
# a field whose value declares what a definition or an instance is, rather than sending a reader to text
UNLINKED_FIELDS = re.compile(r"^\s*(?:- )?\*\*(?:Construct|Extends|Implements):\*\*")
SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
LINKED = re.compile(r"\[(?P<span>(?P<d>`+)[^\n]+?(?P=d))\]\((?P<target>[/#][^)\s]*)\)")
SECTION = re.compile(r"^(?:(?P<path>[\w./-]+\.md)\s+)?§\s+(?P<lineage>.+?)(?:\s+\[[^\]]*\])?$")
WHOLE_FILE = re.compile(r"^[\w./-]+\.md$")


def linked_files(root):
    """-> the Markdown files a person reads on GitHub: under specs/ and docs/, and README.md, AGENTS.md files aside."""
    out = []
    for top in LINKED_ROOTS:
        p = root / top
        if p.is_dir():
            out += [f for f in p.rglob("*.md") if f.name not in UNLINKED_NAMES]
    out += [root / f for f in LINKED_FILES if (root / f).is_file()]
    return sorted(out)


def slug(title):
    """-> GitHub's anchor for a heading's title: inline code marks and emphasis dropped, lower case, every character
    but a letter, a digit, a space, a hyphen or an underscore dropped, and each space made a hyphen."""
    text = re.sub(r"[`*]", "", title.strip()).lower()
    text = "".join(c for c in text if c.isalnum() or c in " -_")
    return text.replace(" ", "-")


def live_lines(text):
    """-> the file's lines, a fenced block's and the front matter's blanked, so neither is read as text a reader sees."""
    lines, inside = text.split("\n"), False
    out = []
    front = bool(lines) and lines[0].strip() == "---"
    for i, line in enumerate(lines):
        if front:
            out.append("")
            if i > 0 and line.strip() == "---":
                front = False
            continue
        if line.startswith("```"):
            inside = not inside
            out.append("")
        else:
            out.append("" if inside else line)
    return out


def anchors(text):
    """-> {lineage: anchor} for each heading below the title, its anchor numbered as GitHub numbers a title met again."""
    seen, stack, out = {}, [], {}
    for line in live_lines(text):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        lvl, title = len(m.group(1)), m.group(2)
        base = slug(title)
        n = seen.get(base, 0)
        seen[base] = n + 1
        anchor = base if n == 0 else f"{base}-{n}"
        if lvl == 1:
            continue
        depth = lvl - 2
        stack = stack[:depth] + [None] * max(0, depth - len(stack)) + [title]
        out.setdefault(" § ".join(t for t in stack if t), anchor)
    return out


class Resolver:
    """Resolves a citation's span, in the file holding it, to the link it carries, reading each file once."""

    def __init__(self, root):
        self.root, self.cache = root, {}
        # a link reaches only a file GitHub serves, one version control tracks; where the files are under none, as in a
        # scratch copy, every file is taken as served
        try:
            out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=root,
                                 capture_output=True, text=True, check=True).stdout
            self.tracked = set(out.split("\n")) - {""} or None
        except (OSError, subprocess.CalledProcessError):
            self.tracked = None

    def served(self, rel):
        """-> whether GitHub serves the file: one version control tracks, never an index.md, which nothing cites."""
        if Path(rel).name == "index.md" or not (self.root / rel).is_file():
            return False
        return self.tracked is None or rel in self.tracked

    def file_anchors(self, rel):
        if rel not in self.cache:
            f = self.root / rel
            self.cache[rel] = anchors(f.read_text(encoding="utf-8").replace("\r\n", "\n")) if f.is_file() else None
        return self.cache[rel]

    def target(self, span, host):
        """-> the link's target for a citation's span, or None where it is no citation or resolves to nothing."""
        text = " ".join(span.split())
        m = SECTION.match(text)
        if m:
            rel = m.group("path") or host
            if not self.served(rel):
                return None
            found = self.file_anchors(rel)
            anchor = found.get(m.group("lineage")) if found else None
            if anchor is None:
                return None
            return f"#{anchor}" if not m.group("path") else f"/{rel}#{anchor}"
        # a whole file is cited by its path from the repository's root; a bare file name, as a row of an index.md
        # naming a file beside it or words naming a kind of file, is no citation
        if WHOLE_FILE.match(text) and "/" in text and self.served(text):
            return f"/{text}"
        return None


def strip(text):
    """-> the text with each link a citation carries removed, the citation's span left as written, a fenced block's
    example of a link left as it stands."""
    lines = text.split("\n")
    live = live_lines(text)
    return "\n".join(LINKED.sub(lambda m: m.group("span"), line) if live[i] else line for i, line in enumerate(lines))


def refresh_tree(root):
    """-> the files under root whose links refresh changed, each written back with its line endings kept."""
    resolver, changed = Resolver(root), []
    for f in linked_files(root):
        raw = f.read_bytes()
        crlf = b"\r\n" in raw
        text = raw.decode("utf-8").replace("\r\n", "\n")
        new = refresh(text, f.relative_to(root).as_posix(), resolver)
        if new != text:
            f.write_bytes((new.replace("\n", "\r\n") if crlf else new).encode("utf-8"))
            changed.append(f)
    return changed


def problems(root):
    """-> (path, line, problem) for each line of a file a person reads whose links refresh would change, and each link in
    a file no person reads on GitHub, a skill or an AGENTS.md file, or in a Construct, an Extends or an Implements field."""
    resolver, out = Resolver(root), []
    linked = set(linked_files(root))
    for f in linked:
        text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        rel = f.relative_to(root).as_posix()
        for n, (old, new) in enumerate(zip(text.split("\n"), refresh(text, rel, resolver).split("\n")), 1):
            if old != new:
                out.append((rel, n, "a citation's link missing, not reaching what the citation resolves to, or standing where none belongs"))
    others = [f for f in (root / ".ai/skills").rglob("*.md")] if (root / ".ai/skills").is_dir() else []
    others += [f for f in root.rglob("AGENTS.md") if ".ai" not in f.relative_to(root).parts]
    for f in sorted(set(others) - linked):
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            if LINKED.search(line):
                out.append((f.relative_to(root).as_posix(), n, "a citation's link in a file agents read, which carries none"))
    return out


def refresh(text, host, resolver):
    """-> the text with each citation a reader sees carrying the link its citation resolves to, a link that no longer
    resolves removed, a fenced block, the front matter, a heading and a Construct, an Extends or an Implements
    field's value left alone."""
    lines = strip(text).split("\n")
    live = live_lines("\n".join(lines))
    held = False  # within a Construct, an Extends or an Implements field whose value is a list beneath its key
    for i, line in enumerate(lines):
        if UNLINKED_FIELDS.match(line):
            held = line.rstrip().endswith(":**")
            continue
        if held and re.match(r"^\s*- ", line):
            continue
        held = False
        if not live[i] or line.lstrip().startswith("#"):
            continue

        def link(m):
            target = resolver.target(m.group(2), host)
            return f"[{m.group(0)}]({target})" if target else m.group(0)
        lines[i] = SPAN.sub(link, line)
    return "\n".join(lines)
