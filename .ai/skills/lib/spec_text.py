"""The reading of a spec's text that the skills' scripts share: its fenced blocks, its headings, its sections and
their lineages, where a citation resolves, and which files are in scope, by the skills registry, and their texts.
audit-specs, design-specs, implement-specs and verify-spec-implementation read a spec through it, each reading this
one copy (specs/methodology/skills.md § Authoring a Skill)."""
import fnmatch
import re
import subprocess
from pathlib import Path, PurePosixPath

import citation_links


class CommitTree:
    """A commit's files read through git in memory, a path of the tree as pathlib.Path gives one: the one reader a check
    reads a tree through, the working tree being a pathlib.Path, so every check runs over either tree and writes no
    file. A file's text is read as the working tree's is, its line endings made newlines."""

    def __init__(self, repo, commit="HEAD", rel="", store=None):
        self.repo, self.commit, self.rel = Path(repo), commit, rel
        if store is None:
            out = subprocess.run(["git", "ls-tree", "-r", "-z", commit], cwd=repo, capture_output=True, check=True).stdout
            files = {}
            for entry in out.decode("utf-8").split("\0"):
                if entry:
                    meta, path = entry.split("\t", 1)
                    if meta.split()[1] == "blob":
                        files[path] = meta.split()[2]
            dirs = {""} | {p.rsplit("/", 1)[0] for f in files for p in [f] if "/" in f}
            dirs |= {d.rsplit("/", i)[0] for d in list(dirs) for i in range(1, d.count("/") + 1)}
            store = {"files": files, "dirs": dirs, "blobs": {}}
        self.store = store

    def _at(self, rel):
        return CommitTree(self.repo, self.commit, rel, self.store)

    def __truediv__(self, other):
        rel = posix_join(self.rel, str(other).replace("\\", "/"))
        return self._at(rel)

    def joinpath(self, *others):
        node = self
        for other in others:
            node = node / other
        return node

    @property
    def name(self):
        return PurePosixPath(self.rel).name

    @property
    def stem(self):
        return PurePosixPath(self.rel).stem

    @property
    def suffix(self):
        return PurePosixPath(self.rel).suffix

    @property
    def parts(self):
        return PurePosixPath(self.rel).parts

    @property
    def parent(self):
        return self._at(self.rel.rsplit("/", 1)[0] if "/" in self.rel else "")

    def as_posix(self):
        return self.rel

    def __str__(self):
        return f"{self.commit}:{self.rel}"

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, CommitTree) and (self.commit, self.rel) == (other.commit, other.rel)

    def __hash__(self):
        return hash((self.commit, self.rel))

    def __lt__(self, other):
        return self.rel < other.rel

    def resolve(self):
        return self

    def relative_to(self, other):
        base = other.rel if isinstance(other, CommitTree) else str(other)
        return PurePosixPath(self.rel).relative_to(base or ".")

    def is_relative_to(self, other):
        base = other.rel if isinstance(other, CommitTree) else str(other)
        return not base or self.rel == base or self.rel.startswith(base + "/")

    def is_file(self):
        return self.rel in self.store["files"]

    def is_dir(self):
        return self.rel in self.store["dirs"]

    def exists(self):
        return self.is_file() or self.is_dir()

    def _below(self):
        """Every file and directory under this one, as paths from the tree's root."""
        prefix = self.rel + "/" if self.rel else ""
        return sorted(p for p in self.store["files"].keys() | self.store["dirs"] if p and p.startswith(prefix))

    def iterdir(self):
        prefix = self.rel + "/" if self.rel else ""
        return [self._at(p) for p in self._below() if "/" not in p[len(prefix):]]

    def glob(self, pattern):
        prefix, steps = (self.rel + "/" if self.rel else ""), pattern.split("/")
        return [self._at(p) for p in self._below() if len(p[len(prefix):].split("/")) == len(steps)
                and all(fnmatch.fnmatchcase(s, g) for s, g in zip(p[len(prefix):].split("/"), steps))]

    def rglob(self, pattern):
        return [self._at(p) for p in self._below() if fnmatch.fnmatchcase(p.rsplit("/", 1)[-1], pattern)]

    def read_bytes(self):
        if not self.is_file():
            raise FileNotFoundError(str(self))
        blobs = self.store["blobs"]
        if not blobs:
            # every blob read in one call, as a check reads most of the tree
            shas = sorted(set(self.store["files"].values()))
            out = subprocess.run(["git", "cat-file", "--batch"], cwd=self.repo, input="\n".join(shas).encode() + b"\n",
                                 capture_output=True, check=True).stdout
            at = 0
            while at < len(out):
                end = out.index(b"\n", at)
                sha, _, size = out[at:end].decode().split(" ")
                start = end + 1
                blobs[sha] = out[start:start + int(size)]
                at = start + int(size) + 1
        return blobs[self.store["files"][self.rel]]

    def read_text(self, encoding="utf-8"):
        return self.read_bytes().decode(encoding).replace("\r\n", "\n").replace("\r", "\n")

    def tracked(self):
        """-> every file the commit holds, the tracked set a check of the working tree reads from git ls-files."""
        return set(self.store["files"])


def posix_join(base, rel):
    """-> rel joined to base, a path from the tree's root, '.' and '..' folded."""
    out = [p for p in base.split("/") if p]
    for part in rel.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            out = out[:-1]
        else:
            out.append(part)
    return "/".join(out)


def tracked(root, others=False):
    """-> the set of files version control tracks under root, as paths from it, and with others the untracked files
    git does not ignore too, or None where root is under no version control: the commit's own files, for a commit's
    tree."""
    if isinstance(root, CommitTree):
        return root.tracked()
    command = ["git", "ls-files"] + (["--cached", "--others", "--exclude-standard"] if others else [])
    try:
        out = subprocess.run(command, cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return set(out.split("\n")) - {""}


def as_root(root):
    """-> the tree a check reads: a CommitTree as it is, anything else the working tree at that path."""
    return root if isinstance(root, CommitTree) else Path(root).resolve()


# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link
def read(path):
    """-> a file's text with each citation's link stripped, so every check reads the citation as written."""
    path = path if isinstance(path, CommitTree) else Path(path)
    return citation_links.strip(path.read_text(encoding="utf-8"))


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
    root = root if isinstance(root, CommitTree) else Path(root)
    return {f.relative_to(root).as_posix(): read(f) for f in md_files(root)}
