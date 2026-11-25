"""A spec's text as the skills' scripts share it: its sections and their lineages, where a citation resolves, and
which files are in scope, by the skills registry, and their texts. Where a line stands, in a fenced block or under a
heading, and the form a citation takes are the one reading's (reading.py), which each function here gives in the
shape its callers read.
audit-specs, design-specs, implement-specs and verify-spec-implementation read a spec through it, each reading this
one copy (specs/methodology/skills/authoring-a-skill.md § Authoring a Skill)."""
import fnmatch
import re
import subprocess
from pathlib import Path, PurePosixPath

import citation_links
import reading


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


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § A Citation's Link
def read(path):
    """-> a file's text with each citation's link stripped, so every check reads the citation as written."""
    path = path if isinstance(path, CommitTree) else Path(path)
    return citation_links.strip(path.read_text(encoding="utf-8"))


HEADING = reading.SECTION_HEADING  # a heading naming a section, the one reading's


RECORD_SELECTOR = reading.KEYED  # a citation's keyed part, the one reading's


def strip_fences(text):
    """Blank out fenced blocks so examples inside them are not linted as live content: each line of a fenced block, its
    fences among them, as the one reading finds it (reading.py), a fence indented within a list item, as a step's Draft
    stands, among them, and a fence's closing one of its character at least as long (spec-style/markdown.md
    § Markdown). An indented code block's lines stand."""
    return reading.live(text, blank="")


def headings(text):
    """-> [(level, title)] of the headings naming sections, the file's title among them, from live content only."""
    return [(h.level, h.title) for h in reading.headings(text)]


def sections(text):
    """-> {lineage: (heading_line, end_line)}, 0-based, over raw lines.

    A section's own text is the lines after its heading up to the next heading at any
    level. A fenced block's lines hold no heading, and are kept in the numbering,
    since a diagram's fence is part of the section it sits in. Of two headings sharing
    a lineage, the lineage names the first.
    """
    return {" § ".join(lineage): (h.line - 1, h.ends - 1) for lineage, h in reading.sections(text).items()}


def parse_citation(cite, host):
    """A citation's (file, lineage, selector), as the one reading reads its form; a same-file form resolves to its
    host, and the selector is the text of a record or part citation's `[...]`, or None. Text that is no citation
    names itself as a file."""
    c = reading.parse_citation(cite)
    if c is None:
        return cite.strip(), "", None
    return c.file or host, c.path, c.selector


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
    return {" § ".join(lineage) for lineage in reading.sections(text)}


# @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs
# specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs names where each kind is named:
# specs by their place under specs/, the agent instructions by the root AGENTS.md and
# specs/AGENTS.md, the documentation by README.md and docs/, and skills by the registry, read at
# run time. The places and names this block defines are the ones the scope's table gives;
# the working files are outside the script, read by the Working-file form audit instead, and code
# is outside audit-specs, which audits every kind but code.
SCOPE_HOME = "scope/what-spec-of-record-governs.md § What Spec of Record Governs"


REGISTRY = "specs/methodology/skills/registered-skills.md"


REGISTRY_RULE = "skills/registered-skills.md § Registered Skills"


def registry(root):
    """-> (skill names, problems): the skills specs/methodology/skills/registered-skills.md registers.

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


KEPT_TESTS = "tests/spec-of-record"  # the folder of the skills' kept tests
FIXTURES = KEPT_TESTS + "/fixtures"  # the one folder of the kept tests' fixture files
OPERATIVE, FIXTURE = "operative", "fixture"  # the two kinds of durable file


def durable_kind(path):
    """-> the kind of durable file a path from the root is: a fixture file where it stands under the kept tests'
    fixtures folder, whatever it holds, and an operative file anywhere else."""
    return FIXTURE if path == FIXTURES or path.startswith(FIXTURES + "/") else OPERATIVE


def scope_paths(root, kind=OPERATIVE):
    """The places in scope holding durable files of a kind. The operative files: the root AGENTS.md, the documentation,
    specs/, each registered skill, the code they share, and the kept tests' folder, whose fixtures folder a caller walking
    it leaves out by `durable_kind`. The fixture files: the fixtures folder alone."""
    if kind == FIXTURE:
        return [FIXTURES]
    return ["AGENTS.md", "README.md", "docs", "specs"] + [".ai/skills/" + n for n in skill_dirs(root)] + [KEPT_TESTS]


# @canon-spec specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure
# @canon-spec specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes
def indexed(root, folder="specs"):
    """The files the index tables name, walked from `folder`'s index.md down -> [path]: each index.md, then each file
    its rows name in their order, a row naming a subdirectory, its name ending `/`, walked in turn. A row naming what is
    not there is the index check's to report, which alone walks the filesystem."""
    idx = root / folder / "index.md"
    if not idx.is_file():
        return []
    out = [idx]
    for name in re.findall(r'^\|\s*`([^`]+)`', read(idx), re.M):
        if name.endswith("/"):
            out += indexed(root, f"{folder}/{name.rstrip('/')}")
        elif (root / folder / name).is_file():
            out.append(root / folder / name)
    return out


# the worked examples, which keep a tree of their own (scope/progressive-disclosure.md § Progressive Disclosure)
EXAMPLES = "specs/methodology/examples/"


def methodology_files(root):
    """The methodology's own files, as the index walk finds them: each file under specs/methodology/ its index tables
    name, a document laid out as a folder's files among them, its worked examples and each index.md aside -> [path]."""
    return [p for p in indexed(root, "specs/methodology")
            if p.name != "index.md" and not p.relative_to(root).as_posix().startswith(EXAMPLES)]


def md_files(root, kind=OPERATIVE):
    """The Markdown files in scope of a kind of durable file: of the operative files, the specifications' as the index
    walk finds them and every other scope path's, no fixture file among them; of the fixture files, each Markdown file of
    the fixtures folder."""
    out = []
    for s in scope_paths(root, kind):
        p = root / s
        if s == "specs":
            out += indexed(root, "specs")
        elif p.is_file() and p.suffix == ".md":
            out.append(p)
        elif p.is_dir():
            out += [f for f in p.rglob("*.md") if durable_kind(f.relative_to(root).as_posix()) == kind]
    return sorted(set(out))


def spec_texts(root):
    """-> {path from the root: text, citations' links stripped} for every Markdown file in scope."""
    root = root if isinstance(root, CommitTree) else Path(root)
    return {f.relative_to(root).as_posix(): read(f) for f in md_files(root)}


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests § Fixture
# the form of a fixture file: its one field opening the fixtures, each fixture's three fields in their order, and the
# name of the index of the fixtures' folder
FIXTURE_RECORDS, FIXTURE_FIELDS, FIXTURES_INDEX = "**Records:**", ("Fixture", "Holds", "Snippet"), "index.md"
FIXTURE_INDENT = 6  # the spaces a fixture's fenced block stands in from, as a record's block field stands
FIXTURE_KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def fixtures_of(text):
    """-> ([{key, holds, language, snippet, line}], [(1-based line, problem)]) for a fixture file's text: each fixture
    it holds, its snippet as the tests read it, the fenced block's own indent taken off and each line ending in a line
    feed, and each line that is no part of a fixture in its form. Nothing is said of what a snippet holds."""
    lines = text.replace("\r\n", "\n").split("\n")
    found, problems, n = [], [], 0
    while n < len(lines) and not lines[n].strip():
        n += 1
    if n == len(lines) or lines[n].rstrip() != FIXTURE_RECORDS:
        return found, [(n + 1 if n < len(lines) else 1, "the file does not open with %s, so it holds no fixture in its form" % FIXTURE_RECORDS)]
    n += 1
    opening = re.compile(r"  - \*\*%s:\*\* (.+?) \\$" % FIXTURE_FIELDS[0])
    while n < len(lines):
        if not lines[n].strip():
            n += 1
            continue
        at, start = n + 1, opening.match(lines[n])
        if not start:
            problems.append((at, "text that is no part of a fixture: %s" % lines[n].strip()[:80]))
            n += 1
            continue
        key = start.group(1).strip()
        if not FIXTURE_KEY.fullmatch(key):
            problems.append((at, "the fixture's key, %s, is not lower-case words joined by hyphens" % key))
        if key in [f["key"] for f in found]:
            problems.append((at, "the key %s is held by an earlier fixture of the file" % key))
        holds = re.match(r"    \*\*%s:\*\* (.+?) \\$" % FIXTURE_FIELDS[1], lines[n + 1]) if n + 1 < len(lines) else None
        named = n + 2 < len(lines) and lines[n + 2].rstrip() == "    **%s:**" % FIXTURE_FIELDS[2]
        m = n + 3
        while m < len(lines) and not lines[m].strip():
            m += 1
        fence = re.match(r" {%d}(`{3,}|~{3,})(\S*)\s*$" % FIXTURE_INDENT, lines[m]) if m < len(lines) else None
        if not holds or not named or not fence:
            problems.append((at, "the fixture %s lacks %s" % (key, "its Holds, what the snippet holds" if not holds else
                                                             "its Snippet" if not named else "a fenced block holding its snippet")))
            n += 1
            continue
        if not fence.group(2):
            problems.append((m + 1, "the fenced block of the fixture %s names no language" % key))
        closing = re.compile(r" {%d}%s{%d,}\s*$" % (FIXTURE_INDENT, re.escape(fence.group(1)[0]), len(fence.group(1))))
        end = next((e for e in range(m + 1, len(lines)) if closing.match(lines[e])), None)
        if end is None:
            problems.append((m + 1, "the fenced block of the fixture %s is never closed" % key))
            break
        body = lines[m + 1:end]
        shallow = [m + 2 + i for i, l in enumerate(body) if l.strip() and not l.startswith(" " * FIXTURE_INDENT)]
        if shallow:
            problems.append((shallow[0], "a line of the fixture %s's snippet stands outside its fenced block's indent" % key))
        found.append({"key": key, "holds": holds.group(1).strip(), "language": fence.group(2), "line": at,
                      "snippet": "".join(l[FIXTURE_INDENT:] + "\n" for l in body)})
        n = end + 1
    return found, problems


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests § A Run
# where a run of the kept tests writes, among the working files, the report it leaves there, and the name a run
# started by another is told its own folder under
KEPT_RUN, KEPT_REPORT, KEPT_RUN_NAMED = ".ai/tmp/kept-tests", "report.xml", "SPEC_OF_RECORD_KEPT_RUN"


def clear_run(folder, keep=()):
    """The one clean-up of a run of the kept tests: removes everything a folder holds but the names kept, files git
    left read-only among it, and leaves the folder standing. It runs before and after a test, over the test's own
    folder, and before and after a run, over the run's, where the run's report is kept."""
    import os
    import shutil
    import stat

    def writable(function, path, _):
        try:
            os.chmod(path, stat.S_IWRITE)
            function(path)
        except OSError:
            pass
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for held in folder.iterdir():
        if held.name in keep:
            continue
        if held.is_dir() and not held.is_symlink():
            shutil.rmtree(held, onerror=writable)
        else:
            try:
                held.unlink()
            except OSError:
                writable(os.unlink, str(held), None)


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
# the comment sign is written by its code, so the line reads as no annotation itself
ANNOTATION = re.compile(r"\s*\x23\s*@canon-spec\s+(.+?)\s*$")
CHECK_NAMED = re.compile(r"\[Name: ([^\]]+)\]\s*$")


def test_annotations(text):
    """-> {a test function's name: [the citation of each canon-spec annotation standing over it]} for a kept test
    file's text, an annotation standing over a function where it is among the comment lines directly above the
    function's first line, its decorators' among it."""
    import ast
    lines, out = text.replace("\r\n", "\n").split("\n"), {}
    for node in ast.walk(ast.parse(text)):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        at = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 2
        cited = []
        while at >= 0 and lines[at].lstrip().startswith("#"):
            named = ANNOTATION.match(lines[at])
            if named:
                cited.insert(0, named.group(1))
            at -= 1
        if cited:
            out[node.name] = cited
    return out


def check_named(citation):
    """-> the Name of the check's record a citation names, or None where it names no record by a Name."""
    named = CHECK_NAMED.search(citation)
    return named.group(1).strip() if named else None
