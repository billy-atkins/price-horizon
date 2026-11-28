"""The search of Spec of Record's scope and the code, one copy the skills' scripts share: who cites a place, which sections are cited and
from where, which lines a citation names, where a term is used, which units of code hold a structure, which places say
the same as a passage, and which places match a pattern. .ai/skills/search-spec-of-record-scope/ runs it for an agent,
and another skill's script calls `Search` directly.

Every use first checks everything the search requires and stops where any is missing (`check_requirements`). It
answers from an index kept in its skill's scratch space, built whole on first use and brought up to date by reading
only the files that changed. Every answer is written as one file in the form its skill states (`Result`).

Where a line stands, under which headings and in which fenced block, and the form a citation takes are the one
reading's. Every place a search gives is a citation of the narrowest of a keyed part, a section or a file
holding its lines, and says what those lines stand in (`Place`). The search leaves out no place for the section or the
table it stands in: a caller leaves out by their citations the places it does not want. A search by meaning ranks a
section's prose alone, and sets places apart when asked by a citation (`meaning`).

A search answers over one target, the operative files as they stand unless it names another: the operative files as
a commit held them, the fixture files as they stand or as a commit held them, or the working files it is given the
paths of (TARGETS). A search of a commit's files is the one search that asks version control anything, and it stops
where it cannot be answered (`version_control`, `asked`).

The search keeps an index to each kind of durable file, the operative files' and the fixture files', and no index
holds a file of the other kind (`listed`, INDEX). So a search of the operative files reads, counts and ranks within
the operative files alone, whatever kind of search it is, and a search of the fixture files within the fixture files
alone. A search of the working files reads the operative files' index, which holds the working files it was given
beside the operative files their citations name.

A search by meaning ranks what it was asked against every passage and every sentence of a passage holding several,
and gives the part of that ranking its caller asks for, the first RANKED places where it asks for none. Parts asked
one after another make up the one ranking (`meaning`, TIERS).

Every result carries a snapshot code for the state of the files of its target, built from what each file holds, and
the search gives the present one on request (`snapshot`, `Search.snapshot_code`). The search keeps each answer it
computes of a kind resting on the files of its target alone, and gives it again while what was asked, the files and
its own reading stand (`Search.kept_answer`, `own_reading`). It tells its caller where a question names nothing to ask
of (`Result.names_nothing`).
"""
import ast
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
import tokenize
from pathlib import Path

import code_checks
import constructs
import reading
import spec_text

SKILL = "search-spec-of-record-scope"
SCRATCH = ".ai/tmp/" + SKILL
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSIONS = 384
SCHEMA = "12"
RANKED = 20       # the places a search by meaning gives where its caller asks for no part of its ranking
CANDIDATES = 50   # the places each ranking gives the fusion of a ranking's first places
FUSION = 60       # the constant of reciprocal rank fusion
EMBED_RUN = 256   # the texts given the model in one run, their vectors written before the next
EMBED_BATCH = 16  # the texts the model takes at once within a run, which sets the memory a run needs
SENTENCES = 0.5   # what a ranking by one sentence of what was asked weighs, beside a ranking by the whole of it
# How far each ranking is read, and the place of the whole ranking that reading fills to. A search's first places are
# fused from each ranking's first CANDIDATES, as cheaply as a search costs with no part asked for, and a part further
# on reads each ranking further. A tier never reorders the places an earlier one gave, so parts asked one after
# another make up one ranking.
TIERS = ((CANDIDATES, 40), (CANDIDATES * 4, 160), (CANDIDATES * 16, 640), (CANDIDATES * 64, None))
DEEPEST = 4096    # the most places the index's nearest-vector search gives at once
PASSAGE = 1000    # the most characters of a passage, which the model reads whole
SENTENCE = 40     # the fewest characters of a passage or a sentence worth ranking
MAX_NAME = 150    # the length the diagram skill's renders keep to, a name every system holds
MAX_PATH = 259    # the longest path every system opens, the folders above a file counted, which a result's file keeps to
FEW = 20          # the places printed with a result's name

KINDS = ("citers", "cited sections", "lines", "terms", "code structure", "meaning", "pattern")
STRUCTURES = ("defines", "calls", "constructs", "extends", "implements", "references", "annotated-with")

# the files a search answers over, one target to a search and to its result, each named for the files it reads
CURRENT_OPERATIVE = "current-operative-files"
COMMITTED_OPERATIVE = "committed-operative-files"
CURRENT_FIXTURE = "current-fixture-files"
COMMITTED_FIXTURE = "committed-fixture-files"
WORKING = "working-files"
TARGETS = (CURRENT_OPERATIVE, COMMITTED_OPERATIVE, CURRENT_FIXTURE, COMMITTED_FIXTURE, WORKING)
# the kind of durable file each target of the durable files reads, and the targets reading them as a commit held them
DURABLE_KIND = {CURRENT_OPERATIVE: spec_text.OPERATIVE, COMMITTED_OPERATIVE: spec_text.OPERATIVE,
                CURRENT_FIXTURE: spec_text.FIXTURE, COMMITTED_FIXTURE: spec_text.FIXTURE}
OF_A_COMMIT = (COMMITTED_OPERATIVE, COMMITTED_FIXTURE)
# the index of each kind of durable file, a file of its own in the scratch space, so neither holds the other's text
INDEX = {spec_text.OPERATIVE: "index.sqlite", spec_text.FIXTURE: "fixture-files-index.sqlite"}
HELD = "working-files-held"   # a working file the index holds and the search in hand was not given, its content kept
# @canon-spec specs/methodology/working-files/main.md § The Working Files
WORKING_FILES = (".ai/plans", ".ai/follow-ups.md", ".ai/tmp")
# where a place's lines stand, as a place says it
STANDS = {reading.TABLE: "table", reading.HEADING: "heading", reading.FENCED: "fenced block"}
# the form a snapshot code is written in, sixteen hexadecimal digits
SNAPSHOT = re.compile(r"[0-9a-f]{16}")
# where a question names nothing to ask of, each told apart from the others
NO_PLACE = "a citation naming no place among the files the search reads"
NO_WORD = "a term or a passage reducing to no word"
NO_FILE = "a path under which no file of the target stands"
NAMES_NOTHING = (NO_PLACE, NO_WORD, NO_FILE)
# what a search by meaning tells its searcher, in place of ranking, where it is asked a passage closing on a question:
# the places worded as a question is are rarely the rule answering it
QUESTION_TURNED_BACK = ("a search by meaning ranks places by their wording, so a question finds the places worded as the question is "
                        "and may miss the rule answering it: ask again as a statement, in the words a rule answering the question would use")
# the kinds of search whose answer rests on the files of its target alone, so the search keeps it: a search by meaning
# ranks over every content its index holds, and a search of the structure `constructs` reads the classes all of it defines
KEPT_KINDS = ("citers", "cited sections", "lines", "terms", "code structure", "pattern")
NOT_KEPT_STRUCTURES = ("constructs",)


_OWN_READING = None


def own_reading():
    """-> the code of the search's own reading: built from what this script and each module of the shared code it
    imports hold, as the files running it have them, with the form of its index and the name of its model. An answer
    the search kept is given again only under the reading that computed it."""
    global _OWN_READING
    if _OWN_READING is None:
        lib, seen, todo = Path(__file__).resolve().parent, {}, [Path(__file__).resolve()]
        while todo:
            script = todo.pop()
            if script.name in seen:
                continue
            data = script.read_bytes().replace(b"\r\n", b"\n")
            seen[script.name] = hashlib.sha256(data).hexdigest()
            try:
                tree = ast.parse(data.decode("utf-8-sig"))
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module and not node.level else []
                for name in names:
                    module = lib / (name.split(".")[0] + ".py")
                    if module.is_file():
                        todo.append(module)
        held = "\n".join(f"{name}\0{sha}" for name, sha in sorted(seen.items())) + "\n" + SCHEMA + "/" + MODEL
        _OWN_READING = hashlib.sha256(held.encode()).hexdigest()[:16]
    return _OWN_READING


# ---------------------------------------------------------------------------------------------------------------------
# The project's version control, which a search of a commit's files alone asks

class CannotSearch(Exception):
    """Raised where a search of a commit's files cannot be answered: the project is under no version control the
    search reads, git is not installed, or git answered with a failure. The search stops and says which."""


NONE_READ, NO_GIT, GIT = "none read", "git not installed", "git"


def version_control(root):
    """-> which of the cases of a search of a commit's files the project is in, told from the files and asked of git
    only where git can answer: NONE_READ, NO_GIT or GIT. A project is under git where its root or a folder above it
    holds a repository, `.git` a folder or, in a worktree or a submodule, a file. No folder is looked in that git
    itself is kept from by GIT_CEILING_DIRECTORIES, so the search and git read one project the same way. A search of
    the files as they stand never calls this."""
    folder = os.path.abspath(root)
    ceilings = {os.path.normcase(os.path.abspath(c)) for c in os.environ.get("GIT_CEILING_DIRECTORIES", "").split(os.pathsep) if c}
    while not os.path.exists(os.path.join(folder, ".git")):
        parent = os.path.dirname(folder)
        if parent == folder or os.path.normcase(parent) in ceilings:
            return NONE_READ
        folder = parent
    return GIT if shutil.which("git") else NO_GIT


def asked(command, root, **given):
    """-> git's answer to a command, its output as bytes, or a stop naming what was asked and git's own words where it
    answers with a failure or cannot be run."""
    said = "`" + " ".join(command) + "`"
    try:
        done = subprocess.run(command, cwd=root, capture_output=True, **given)
    except OSError as e:
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since git could not be run. The search asked {said}, and the answer was: {e}")
    if done.returncode:
        words = done.stderr.decode("utf-8", "replace").strip() or f"no words, and the exit code {done.returncode}"
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since git answered with a failure. The search asked {said}, and git answered: {words}")
    return done.stdout


def committed_tree(root, commit=None):
    """-> (the commit's full name, its files as spec_text.CommitTree reads them), the last commit unless another is
    named, the search stopping in each case it cannot be answered in."""
    case = version_control(root)
    if case == NONE_READ:
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since the project is under no version control the search reads: neither `{Path(root).as_posix()}` nor a folder above it holds a repository. "
                           f"A search of `{CURRENT_OPERATIVE}`, of `{CURRENT_FIXTURE}` or of `{WORKING}` needs none.")
    if case == NO_GIT:
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since the project is under git and git is not installed, or is not on the path. "
                           f"Install git, or search `{CURRENT_OPERATIVE}`, `{CURRENT_FIXTURE}` or `{WORKING}`, which need none.")
    name = asked(["git", "rev-parse", "--verify", (commit or "HEAD") + "^{commit}"], root).decode("utf-8", "replace").strip()
    def held():
        # the one reader of a commit the shared code holds lists the commit's files as it is made, and reads them all,
        # in one call to git, as the first of them is read: both are asked here, so a failure of either is told as one
        tree = spec_text.CommitTree(root, name)
        for rel in sorted(tree.tracked())[:1]:
            try:
                (tree / rel).read_bytes()
            except (ValueError, KeyError):  # git answered without failing and gave no content for a file the commit lists
                raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since git gave no content for a file the commit lists. "
                                   f"The search asked `git cat-file --batch` for the files of {name}, and git's answer holds a file it calls missing.")
        return tree

    return name, through_git(held)


def through_git(read):
    """-> what a reading of a commit gives, or a stop naming what was asked and git's own words where git fails."""
    try:
        return read()
    except subprocess.CalledProcessError as e:
        words = (e.stderr or b"").decode("utf-8", "replace").strip() or f"no words, and the exit code {e.returncode}"
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since git answered with a failure. The search asked `{' '.join(e.cmd)}`, and git answered: {words}")
    except OSError as e:
        raise CannotSearch(f"{SKILL}: the committed files cannot be searched, since git could not be run: {e}")


# ---------------------------------------------------------------------------------------------------------------------
# What the search requires

class Requirement:
    def __init__(self, name, why, install, present):
        self.name, self.why, self.install, self.present = name, why, install, present


def _module(name):
    return lambda root: importlib.util.find_spec(name) is not None


def project_root_of(folder):
    """-> the project root of the project whose files a folder holds, told from the files alone and asked of no
    version control: where the folder holds a copy version control made as a worktree, its `.git` a file naming its
    own folder in the project's repository, and that folder naming the repository the copy shares, the folder holding
    that repository; else the folder itself, the project root, one under no version control and a submodule among them."""
    folder = Path(folder).resolve()
    named = folder / ".git"
    try:
        words = named.read_text(encoding="utf-8").strip() if named.is_file() else ""
        if words.startswith("gitdir:"):
            own = (folder / words[len("gitdir:"):].strip()).resolve()
            shared = (own / (own / "commondir").read_text(encoding="utf-8").strip()).resolve()
            if shared.name == ".git" and shared.parent.is_dir():
                return shared.parent
    except (OSError, UnicodeDecodeError):
        pass
    return folder


_HOME = None


def home():
    """-> the project that keeps what the search needs beside the files it reads, the model's files: the project root
    of the project the search's own skill stands in. A copy of the project's files gives the same one, wherever the
    copy stands, so what was set up once on the machine is found from each."""
    global _HOME
    if _HOME is None:
        _HOME = project_root_of(Path(__file__).resolve().parents[3])
    return _HOME


# the most memory a process holding the search's model takes, the model and its working memory with room, which the
# kept test of scale holds a build of an index under and a run of the kept tests counts each process at
MODEL_MEMORY = 1 << 30


def model_threads():
    """-> the threads the search's model works on: the number a run of the kept tests hands the process it starts, or,
    handed none, half the machine's processors, so a search run by hand leaves the rest to whoever is using the
    machine."""
    from spec_text import MODEL_THREADS_NAMED
    handed = os.environ.get(MODEL_THREADS_NAMED, "")
    return int(handed) if handed.isdigit() and int(handed) > 0 else max(1, (os.cpu_count() or 2) // 2)


def model_folder():
    """-> where the model's files sit: the skill's scratch space in `home()`."""
    return home() / SCRATCH / "model"


def _model_present(root):
    folder = model_folder()
    return folder.is_dir() and any(f.is_file() and f.suffix == ".onnx" for f in folder.rglob("*"))


ENTRY = "python .ai/skills/" + SKILL + "/scripts/" + SKILL + ".py"
def _sqlite_present(root):
    if not hasattr(sqlite3.Connection, "enable_load_extension"):
        return False
    try:
        sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)")
    except sqlite3.Error:
        return False
    return True


REQUIREMENTS = [
    Requirement("a Python whose SQLite loads extensions and has full-text search", "the index is an SQLite database that searches text itself and loads the extension finding the nearest vectors",
                "install Python from python.org, or another build whose sqlite3 module has enable_load_extension and FTS5", _sqlite_present),
    Requirement("sqlite-vec", "finds the passages whose vectors stand nearest a passage's, inside the index",
                "python -m pip install sqlite-vec", _module("sqlite_vec")),
    Requirement("fastembed", "runs the model on this machine that turns a passage into the vector a search by meaning ranks by",
                "python -m pip install fastembed", _module("fastembed")),
    Requirement("tree-sitter", "parses code in the stack's languages into units, so code is searched as code",
                "python -m pip install tree-sitter", _module("tree_sitter")),
    Requirement("tree-sitter-typescript", "the grammar the parser reads TypeScript by",
                "python -m pip install tree-sitter-typescript", _module("tree_sitter_typescript")),
    Requirement("tree-sitter-c-sharp", "the grammar the parser reads C# by",
                "python -m pip install tree-sitter-c-sharp", _module("tree_sitter_c_sharp")),
    Requirement("markdown-it-py", "reads Markdown as CommonMark and its tables as GitHub Flavored Markdown, so a search by terms finds a phrase's words apart only where prose stands",
                "python -m pip install markdown-it-py", _module("markdown_it")),
    Requirement("uniseg", "bounds a sentence as Unicode Standard Annex #29 bounds it, so a phrase's words are found apart only within one sentence",
                "python -m pip install uniseg", _module("uniseg")),
    Requirement("the model's files", "the model " + MODEL + ", kept on this machine so a search sends no text anywhere and downloads nothing",
                ENTRY + " --install-model", _model_present),
]


def missing_requirements(root):
    return [r for r in REQUIREMENTS if not r.present(root)]


def requirements_report(root):
    """-> (the report's text, the count missing): each thing the search requires, present or missing, with why the
    search needs it and the command installing it."""
    missing = missing_requirements(root)
    out = []
    if missing:
        out.append(f"{SKILL}: the search cannot run. Of the {len(REQUIREMENTS)} things it requires, {len(missing)} {'is' if len(missing) == 1 else 'are'} missing.")
    else:
        out.append(f"{SKILL}: everything the search requires is present.")
    for r in REQUIREMENTS:
        out.append(f"  {'MISSING' if r in missing else 'present'}  {r.name}: {r.why}")
        if r in missing:
            out.append(f"           to install it: {r.install}")
    if missing:
        out.append("Every kind of search checks all of these before it reads or writes, so install each one missing, then run the search again.")
        if any(r.name == "the model's files" for r in missing) and any(r.name == "fastembed" for r in missing):
            out.append("Install fastembed before the model's files, since it downloads them.")
    return "\n".join(out), len(missing)


class MissingRequirements(Exception):
    """Raised by any use of the search where something it requires is missing, before anything is read or written."""


def check_requirements(root):
    text, count = requirements_report(root)
    if count:
        raise MissingRequirements(text)


def install_model(root):
    """Download the model's files into the skill's scratch space in `home()`, where every search of the project finds
    them: the one action that reaches the network, run by the user's own command and never by a search."""
    if not _module("fastembed")(root):
        raise MissingRequirements(f"{SKILL}: fastembed is missing, and it downloads the model's files.\n  install it with: python -m pip install fastembed")
    from fastembed import TextEmbedding
    folder = model_folder()
    folder.mkdir(parents=True, exist_ok=True)
    model = TextEmbedding(model_name=MODEL, cache_dir=str(folder))
    list(model.embed(["a passage"]))
    return folder


# ---------------------------------------------------------------------------------------------------------------------
# A Markdown file as the index holds it, each part taken from the one reading

LINK = re.compile(r"\[(`[^`\n]+`)\]\((?:/|#)[^)\s]*\)")
BARE = reading.BARE
ANNOTATION = reading.ANNOTATION
squeeze = reading.squeeze


def strip_links(text):
    """-> text with the link each citation carries set aside, the citation left as written."""
    return LINK.sub(r"\1", text)


def written(rows):
    """-> the text the rows were read from, which the one reading keeps once read."""
    return "\n".join(r[0] for r in rows)


def markdown_lines(text):
    """-> [(line, fenced, info)] for each line of a Markdown file, as the one reading reads it: whether it stands in
    a fenced block, its fences among it, and the block's info string. Front matter is read as a block of its own, its
    info `front matter`."""
    found = reading.blocks(text)
    return [(ln.text, ln.kind in (reading.FENCED, reading.FRONT_MATTER),
             "front matter" if ln.kind == reading.FRONT_MATTER else found[ln.block].word if ln.kind == reading.FENCED else "")
            for ln in reading.lines(text)]


def markdown_headings(rows):
    """-> [(lineage, occurrence, level, line, own_end, subtree_end)], lines 1-based, ends exclusive, from the headings
    the one reading gives. A level-1 heading is the file's title and opens no lineage. The whole file is the lineage
    ''. `occurrence` counts the headings sharing a lineage, the first being 1."""
    heads = [h for h in reading.headings(written(rows)) if h.level > 1]
    total = len(rows) + 1
    out, seen = [("", 1, 0, 1, heads[0].line if heads else total, total)], {}
    for h in heads:
        lineage = " § ".join(squeeze(title) for title in h.lineage)
        seen[lineage] = seen.get(lineage, 0) + 1
        out.append((lineage, seen[lineage], h.level, h.line, h.ends, h.subtree_ends))
    return out


def parse_citation(written):
    """-> (path or None for the same file, lineage, key or None) of a citation as written, as the one reading reads
    its form, or None where the text is no citation. A whole-file citation gives the lineage ''."""
    c = reading.parse_citation(written)
    return None if c is None else (c.file or None, c.path, c.key)


def markdown_citations(rows, headings):
    """-> [(line, host lineage, form, fenced, written, path, lineage, key)] for each citation a Markdown file holds: a
    code span in a citation's form, one broken across lines among them, an annotation's line in a fenced block, and each
    `technical-specs` entry of the front matter, a label. A same-file citation in a fenced `markdown` block names a
    section of the file that block holds, so it is no citer of the file around it and is left out."""
    out, text = [], written(rows)

    def host(line):
        best = ""
        for lineage, _, _, start, _, _ in headings[1:]:
            if start <= line:
                best = lineage
        return best

    # a code span is read outside every fenced block and then within each block's own lines, as the one reading gives
    # them, so a fence's backticks never pair with a code span's, and a span never runs across a fence
    spanned = set()
    for offset, held in reading.spans(text):
        parsed = parse_citation(held)
        if not parsed:
            continue
        line = reading.line_at(text, offset).number
        _, fenced, info = rows[line - 1]
        spanned.add(line)
        if fenced and info == "markdown" and parsed[0] is None:
            continue
        out.append((line, host(line), "citation", int(fenced), squeeze(held), parsed[0], parsed[1], parsed[2]))
    front = False
    for i, (line, fenced, info) in enumerate(rows):
        if info == "front matter":
            if line.strip().startswith("technical-specs:"):
                front = True
            elif front and line.strip().startswith("- "):
                path = line.strip()[2:].strip().strip("'\"")
                out.append((i + 1, "", "label", 0, path, path, "", None))
            elif not line.startswith((" ", "\t")):
                front = False
        elif fenced:
            a = ANNOTATION.match(line)
            parsed = parse_citation(a.group(2)) if a else None
            if parsed and parsed[0]:
                out.append((i + 1, host(i + 1), "annotation", 1, squeeze(a.group(2)), parsed[0], parsed[1], parsed[2]))
            elif not reading.FENCE.match(line.lstrip()):
                # a citation written bare in a fenced block, as a brief writes one: where it ends is told only by the
                # headings of the file it names, so the rest of its line is kept and read against them as it is asked for
                found = list(BARE.finditer(line))
                for n, b in enumerate(found):
                    rest = squeeze(line[b.end():found[n + 1].start()] if n + 1 < len(found) else line[b.end():])
                    if rest and line[max(0, b.start() - 1):b.start()] != "`":
                        out.append((i + 1, host(i + 1), "bare", 1, squeeze(b.group(1) + " § " + rest), b.group(1), rest, None))
    return sorted(set(out), key=lambda c: tuple("" if v is None else v for v in c))


def markdown_passages(rows, headings):
    """-> [(lineage, line_start, line_end, text)]: each section's own text in passages the model reads whole, split at
    its blank lines and then at its sentences. A fenced block's lines are left out, a diagram's and an example's among
    them, since they state nothing in prose."""
    out = []
    heading = {ln.number for ln in reading.lines(written(rows)) if ln.kind == reading.HEADING}
    for lineage, _, _, start, own_end, _ in headings:
        block, first = [], None
        for n in range(start, own_end + 1):
            row = rows[n - 1] if n < own_end and n - 1 < len(rows) else ("", False, "")
            live = row[0].strip() and not row[1] and n not in heading
            if live:
                block.append(row[0].strip())
                first = first or n
            elif block:
                text = squeeze(strip_markup(" ".join(block)))
                for piece in split_passage(text):
                    out.append((lineage, first, n - 1, piece))
                block, first = [], None
    return out


def strip_markup(text):
    return re.sub(r"[`*|\\]+", " ", text)


def sentences(text):
    """-> the sentences of a passage worth ranking alone, or none where it holds one: a rule restated in one sentence
    of a longer passage is ranked by that sentence, which the passage's other sentences would otherwise drown."""
    out = [s.strip() for s in re.split(r"(?<=[.?!:;]) ", text)]
    out = [s for s in out if len(s) >= SENTENCE]
    return out if len(out) > 1 else []


def split_passage(text):
    if len(text) < SENTENCE:
        return []
    if len(text) <= PASSAGE:
        return [text]
    out, cur = [], ""
    for sentence in re.split(r"(?<=[.?!]) ", text):
        if cur and len(cur) + len(sentence) + 1 > PASSAGE:
            out.append(cur)
            cur = ""
        cur = (cur + " " + sentence).strip()
        while len(cur) > PASSAGE:
            out.append(cur[:PASSAGE])
            cur = cur[PASSAGE:]
    return out + ([cur] if len(cur) >= SENTENCE else [])


def item_field(text):
    """-> (indentation, key, value) of a line that is a list item opening with a field, or None. The field's form is
    the one copy the construct module holds."""
    m = constructs.FIELD.match(text)
    return (m.group("indent"), m.group("key"), m.group("value")) if m and m.group("marker") and m.group("value") is not None else None


def bare_field(text):
    """-> (key, value) of a line that is a field standing in no list item, or None."""
    m = constructs.FIELD.match(text)
    return (m.group("key"), m.group("value") or "") if m and not m.group("marker") else None


def section_parts(rows):
    """-> (items, table rows) of a section's lines, [(line, text)], read once for every keyed part asked of it: each
    list item opening with a field, as (its place among the rows, its indentation, the field's key, its value), and
    each row of each table, as (its line, the Table Name standing above it, the table's header, the row's cells)."""
    items, tabled, named, header = [], [], None, None
    for i, (n, text) in enumerate(rows):
        m, f = item_field(text), bare_field(text)
        if m:
            items.append((i, len(m[0]), squeeze(m[1]), squeeze(m[2])))
        if f and f[0] == "Table Name" and f[1]:
            named = squeeze(f[1])
        if not text.strip().startswith("|"):
            header = None
            continue
        cells = [squeeze(c) for c in text.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if set(text.strip()) <= set("|-: "):
            continue
        tabled.append((n, named, header, cells))
    return items, tabled


def find_part(rows, key, parts=None):
    """-> (first line, last line) of the keyed part a key names within a section's lines, [(line, text)]: a record, by
    its identifying fields, or a table's row, by the columns its key names, or None where it names none."""
    pairs = [tuple(squeeze(x) for x in p.split(":", 1)) for p in key.split("; ") if ":" in p]
    if not pairs:
        return None
    items, tabled = parts or section_parts(rows)
    table = None
    if "." in pairs[0][0]:
        table = pairs[0][0].split(".", 1)[0]
        pairs = [(k.split(".", 1)[-1], v) for k, v in pairs]
    for i, indent, name, value in [] if table else items:
        if (name, value) != pairs[0]:
            continue
        n = end = rows[i][0]
        for n2, t2 in rows[i + 1:]:
            if t2.strip() and len(t2) - len(t2.lstrip()) <= indent:
                break
            if t2.strip():
                end = n2
        item = "\n".join(t for nn, t in rows[i:] if nn <= end)
        if all(re.search(r"\*\*" + re.escape(k) + r":\*\* " + re.escape(v) + r"(?: \\)?\s*$", item, re.M) for k, v in pairs[1:]):
            return n, end
    for n, named, header, cells in tabled:
        if table and named != table:
            continue
        if all(k in header and header.index(k) < len(cells) and cells[header.index(k)].strip("`") == v.strip("`") for k, v in pairs):
            return n, n
    return None


def markdown_parts(texts, fenced, headings):
    """-> [(lineage, key, first line, last line)] for each keyed part a file's sections hold, as a citation of the part
    writes its key: a record, by the field its item opens with, and a row of a table declaring a Reference Key or a
    Table Name, by its key's columns. Only a part its own citation gives back is listed, so a place citing a part never
    names another: a key two parts of a section share names the first alone. Where two headings share a path, a
    citation of the path names what both hold together, so the parts under each are listed, and a key both hold names
    the first."""
    out, listed = [], set()
    for lineage, occurrence, _, start, own_end, subtree_end in headings:
        if not lineage:
            continue
        rows = [(n, texts[n - 1]) for n in range(start, min(subtree_end, len(texts) + 1))]
        parts = section_parts(rows)
        keys, fields, table = [], {}, None
        for n in range(start, min(own_end, len(texts) + 1)):
            text = texts[n - 1]
            if fenced[n - 1]:
                continue
            if not text.strip().startswith("|"):
                table = None
                m, f = item_field(text), bare_field(text)
                if m:
                    keys.append((n, squeeze(m[1]) + ": " + squeeze(m[2])))
                if f:
                    fields[squeeze(f[0])] = squeeze(f[1])
                elif text.strip() and not m:
                    fields = {}
                continue
            cells = [squeeze(c) for c in text.strip().strip("|").split("|")]
            if table is None:
                named = fields.get("Table Name")
                columns = [squeeze(c) for c in re.split(r"[;,]", fields.get("Reference Key", "")) if squeeze(c)] or ([cells[0]] if named else [])
                table = (cells, columns if columns and all(c in cells for c in columns) else [], named)
                fields = {}
                continue
            header, columns, named = table
            if columns and not set(text.strip()) <= set("|-: ") and len(cells) == len(header):
                keys.append((n, "; ".join((named + "." if named else "") + c + ": " + cells[header.index(c)].strip("`") for c in columns)))
        for n, key in keys:
            # a citation is written in a code span, so a key holding a backtick is one no citation can write
            span = None if "`" in key else find_part(rows, key, parts)
            if span and span[0] == n and (lineage, key) not in listed:
                listed.add((lineage, key))
                out.append((lineage, key, span[0], span[1]))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Code read by a parser for its language

LANGUAGES = {".py": "python", ".ts": "typescript", ".tsx": "tsx", ".cs": "c_sharp"}
# a language with no units: a file of it is one unit, and no structure is searched in it
NO_UNITS = {".yaml": "YAML", ".yml": "YAML", ".json": "JSON", ".toml": "TOML", ".ini": "INI"}
TREE_SITTER = {
    "typescript": {
        "unit": {"class_declaration": "class", "abstract_class_declaration": "class", "interface_declaration": "interface",
                 "function_declaration": "function", "method_definition": "method", "enum_declaration": "enum",
                 "type_alias_declaration": "type"},
        "call": ("call_expression", "function"), "new": ("new_expression", "constructor"),
        "extends": ("extends_clause", "extends_type_clause"), "implements": ("implements_clause",),
        "names": ("identifier", "type_identifier", "property_identifier"), "skip": ("comment", "string", "template_string"),
    },
    "c_sharp": {
        "unit": {"class_declaration": "class", "interface_declaration": "interface", "struct_declaration": "struct",
                 "record_declaration": "record", "enum_declaration": "enum", "method_declaration": "method",
                 "constructor_declaration": "constructor", "local_function_statement": "function"},
        "call": ("invocation_expression", "function"), "new": ("object_creation_expression", "type"),
        "extends": ("base_list",), "implements": ("base_list",),
        "names": ("identifier",), "skip": ("comment", "string_literal", "verbatim_string_literal", "interpolated_string_expression"),
    },
}
TREE_SITTER["tsx"] = TREE_SITTER["typescript"]


def comment_annotations(lines):
    """-> [(line, written, path, lineage, key)] for each plain comment line holding a spec annotation."""
    out = []
    for i, line in enumerate(lines, 1):
        m = ANNOTATION.match(line)
        parsed = parse_citation(m.group(2)) if m else None
        if parsed and parsed[0]:
            out.append((i, squeeze(m.group(2)), parsed[0], parsed[1], parsed[2]))
    return out


def unit_under(units, line):
    """-> the name of the unit an annotation on `line` stands over: the first unit opening after it, the run of
    annotations and comments between them passed over, or the file's own unit where none opens after it."""
    after = sorted((u for u in units if u[2] > line and u[1] != "module" and u[1] != "file"), key=lambda u: u[2])
    return after[0][0] if after else units[0][0]


def read_python(text, stem):
    """-> (units, structures, note): [(name, kind, line_start, line_end)] and [(structure, name, unit, line)]."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError) as e:
        return [(stem, "file", 1, text.count("\n") + 1)], [], f"its parser could not read it: {e}"
    units, structures = [(stem, "module", 1, text.count("\n") + 1)], []

    def walk(node, unit, in_class):
        for child in ast.iter_child_nodes(node):
            here, inner = unit, in_class
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "class" if isinstance(child, ast.ClassDef) else ("method" if in_class else "function")
                name = (unit + "." if unit != stem else "") + child.name
                first = min([child.lineno] + [d.lineno for d in child.decorator_list])
                units.append((name, kind, first, child.end_lineno))
                structures.append(("defines", child.name, name, child.lineno))
                if isinstance(child, ast.ClassDef):
                    for base in child.bases:
                        target = base.id if isinstance(base, ast.Name) else getattr(base, "attr", None)
                        if target:
                            structures.append(("extends", target, name, child.lineno))
                here, inner = name, isinstance(child, ast.ClassDef)
            elif isinstance(child, ast.Call):
                f = child.func
                target = f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)
                if target:
                    structures.append(("calls", target, unit, child.lineno))
            elif isinstance(child, ast.Name):
                structures.append(("references", child.id, unit, child.lineno))
            elif isinstance(child, ast.Attribute):
                structures.append(("references", child.attr, unit, child.lineno))
            elif isinstance(child, ast.Assign) and unit == stem:
                for t in child.targets:
                    if isinstance(t, ast.Name):
                        units.append((t.id, "constant", child.lineno, child.end_lineno))
                        structures.append(("defines", t.id, t.id, child.lineno))
            walk(child, here, inner)

    walk(tree, stem, False)
    return units, sorted(set(structures)), ""


def python_comment_lines(text):
    """-> the set of lines holding only a comment, read by Python's own tokenizer, so a string is never one."""
    out = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT and not tok.line[:tok.start[1]].strip():
                out.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None
    return out


_PARSERS = {}


def tree_sitter_parser(language):
    if language not in _PARSERS:
        from tree_sitter import Language, Parser
        if language in ("typescript", "tsx"):
            import tree_sitter_typescript as grammar
            pointer = grammar.language_tsx() if language == "tsx" else grammar.language_typescript()
        else:
            import tree_sitter_c_sharp as grammar
            pointer = grammar.language()
        _PARSERS[language] = Parser(Language(pointer))
    return _PARSERS[language]


def read_tree_sitter(text, stem, language):
    """-> (units, structures, note, comment lines) for a file in a language tree-sitter parses."""
    spec = TREE_SITTER[language]
    source = text.encode("utf-8")
    tree = tree_sitter_parser(language).parse(source)
    units, structures, comments = [(stem, "module", 1, text.count("\n") + 1)], [], set()

    def word(node):
        return source[node.start_byte:node.end_byte].decode("utf-8", "replace")

    def last_name(node):
        """-> the name a callee or a type is written with: its last identifier."""
        if node is None:
            return None
        if node.type in spec["names"]:
            return word(node)
        found = None
        for child in node.children:
            if child.type in spec["skip"] or child.type in ("arguments", "argument_list", "type_arguments", "type_argument_list"):
                continue
            found = last_name(child) or found
        return found

    def walk(node, unit):
        here = unit
        if node.type == "comment":
            for n in range(node.start_point[0] + 1, node.end_point[0] + 2):
                comments.add(n)
            return
        if node.type in spec["skip"]:
            return
        if node.type in spec["unit"]:
            name_node = node.child_by_field_name("name")
            if name_node is not None:
                name = (unit + "." if unit != stem else "") + word(name_node)
                units.append((name, spec["unit"][node.type], node.start_point[0] + 1, node.end_point[0] + 1))
                structures.append(("defines", word(name_node), name, node.start_point[0] + 1))
                here = name
        if node.type == spec["call"][0]:
            target = last_name(node.child_by_field_name(spec["call"][1]))
            if target:
                structures.append(("calls", target, unit, node.start_point[0] + 1))
        if node.type == spec["new"][0]:
            target = last_name(node.child_by_field_name(spec["new"][1]))
            if target:
                structures.append(("constructs", target, unit, node.start_point[0] + 1))
        for structure in ("extends", "implements"):
            if node.type in spec[structure]:
                for child in node.named_children:
                    target = last_name(child)
                    if target:
                        structures.append((structure, target, unit, node.start_point[0] + 1))
        if node.type in spec["names"]:
            structures.append(("references", word(node), unit, node.start_point[0] + 1))
        for child in node.children:
            walk(child, here)

    walk(tree.root_node, stem)
    note = "its parser met text it could not read, and what it read is listed" if tree.root_node.has_error else ""
    return units, sorted(set(structures)), note, comments


# ---------------------------------------------------------------------------------------------------------------------
# Terms

def normalize(text):
    """-> text with an identifier split into its words, at a change of case and between a letter and a digit, so
    `append_entry`, `--append-entry` and `AppendEntry` are each found by `append entry`. The index's tokenizer splits at
    every other character that is no letter or digit, and reduces each word to its stem."""
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)


def phrase(text):
    """-> the index's query for a phrase: its words in order, or None where it holds no word."""
    words = re.findall(r"[^\W_]+", normalize(text))
    return '"' + " ".join(words) + '"' if words else None


def is_question(asked):
    """Whether what a search by meaning was asked is a passage closing on a question: its last character, past any
    closing quotation mark or bracket, a question mark. A citation is never one, nor a passage holding a question
    within it and closing on a statement."""
    parsed = parse_citation(asked)
    return not (parsed and parsed[0]) and asked.rstrip().rstrip("\"'”’)]»").endswith(("?", "？"))


# ---------------------------------------------------------------------------------------------------------------------
# Where prose stands, the one place a phrase's words may stand apart
#
# The search defines neither prose nor a sentence. It reads where prose stands in a file by the standard of the file's
# kind: Markdown as CommonMark reads it, a table as GitHub Flavored Markdown reads it, and code by its language's
# grammar, Python's own tokenizer and parser or tree-sitter's. Within each run of prose, a sentence is bounded as
# Unicode Standard Annex #29, Unicode Text Segmentation, bounds it.

# the languages a fenced block may name to hold Markdown, read as Markdown
MARKDOWN_FENCES = ("markdown", "md")
# the names a fenced block may give a language the search parses, each with the language its code is read as
CODE_FENCES = {"python": "python", "py": "python", "typescript": "typescript", "ts": "typescript", "tsx": "tsx",
               "csharp": "c_sharp", "cs": "c_sharp", "c#": "c_sharp"}


def stems(text):
    """-> the stems of a text's words in their order, each reduced by the tokenizer the index reduces its words by, so
    a phrase's words are matched against a sentence as the index matches them."""
    if stems.db is None:
        stems.db = sqlite3.connect(":memory:")
        stems.db.execute("create virtual table said using fts5(x, tokenize='porter unicode61')")
        stems.db.execute("create virtual table said_terms using fts5vocab(said, instance)")
    stems.db.execute("delete from said")
    stems.db.execute("insert into said(rowid, x) values (1, ?)", (normalize(text),))
    return [term for (term,) in stems.db.execute("select term from said_terms order by offset")]


stems.db = None


def together_in(got, wanted):
    """Whether the stems wanted stand together, in their order, among the stems got."""
    return any(got[i:i + len(wanted)] == wanted for i in range(len(got) - len(wanted) + 1))


def words_apart(sentence, groups):
    """Whether a sentence holds the groups of stems wanted in their order, each group's stems together, with other
    words between the groups, and holds them nowhere together."""
    got, at = stems(sentence), 0
    for group in groups:
        at = next((i + len(group) for i in range(at, len(got) - len(group) + 1) if got[i:i + len(group)] == group), None)
        if at is None:
            return False
    return not together_in(got, [s for g in groups for s in g])


def prose_sentences(text, kind, language):
    """-> [(first line, last line, sentence)] of each sentence of prose a file holds, its lines counted from 1: in
    Markdown, the prose `markdown_prose` reads; in code, the prose of its comments and docstrings; in any other file,
    none."""
    if kind == "markdown":
        runs = markdown_prose(text)
    elif kind == "code":
        runs = code_prose(text, language)
    else:
        runs = []
    return [s for run in runs for s in run_sentences(run)]


def code_prose(text, language):
    """-> [run] of the prose of code in a language the search parses, as its grammar reads its comments and
    docstrings, or none for any other language."""
    if language == "python":
        return python_prose(text)
    if language in TREE_SITTER:
        return tree_sitter_prose(text, language)
    return []


def markdown_prose(text, offset=0):
    """-> [run], each run a list of (line, its text), of the prose a Markdown text holds, as CommonMark reads its blocks
    and GitHub Flavored Markdown its tables: a paragraph, its lines one run, a list's item among them; a field's value in
    a record form, which the hard line break ending it bounds; and a table's cell. A heading holds no prose. A fenced
    block is read as what it holds: one naming Markdown as Markdown, and one naming a language the search parses as
    that language's code, its comments and docstrings its prose. Any other fenced block, an indented block of code and
    HTML hold none. `offset` is the number of lines standing above the text in its file."""
    from markdown_it import MarkdownIt
    tokens = MarkdownIt("commonmark").enable("table").parse(text)
    runs, heading = [], False
    for tok in tokens:
        if tok.type == "heading_open":
            heading = True
        elif tok.type == "heading_close":
            heading = False
        elif tok.type == "inline" and not heading and tok.map:
            runs += inline_runs(tok.content, offset + tok.map[0] + 1)
        elif tok.type == "fence" and tok.map:
            named = (tok.info.strip().split() or [""])[0].lower()
            # the fence's own line stands above its content, which starts on the line after it
            above = offset + tok.map[0] + 1
            if named in MARKDOWN_FENCES:
                runs += markdown_prose(tok.content, above)
            elif named in CODE_FENCES:
                runs += [[(line + above, said) for line, said in run] for run in code_prose(tok.content, CODE_FENCES[named])]
    return runs


def inline_runs(content, first):
    """-> [run] of an inline block's text whose first line is the file's line `first`: its lines joined into one run,
    as CommonMark joins a paragraph's, each hard line break, a backslash or two spaces ending a line, ending a run."""
    runs, run = [], []
    for k, line in enumerate(content.split("\n")):
        hard = line.endswith("\\") or line.endswith("  ")
        run.append((first + k, line[:-1] if line.endswith("\\") else line))
        if hard:
            runs.append(run)
            run = []
    return runs + ([run] if run else [])


def python_prose(text):
    """-> [run] of the prose of Python code, as its own tokenizer and parser read it: each comment standing alone on
    its line joined with the comments on the lines below it into one run, an empty comment ending a run; a comment
    after code a run of its own; and each docstring, its paragraphs each a run."""
    runs, run, last = [], [], None
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []
    for tok in tokens:
        if tok.type != tokenize.COMMENT:
            if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT) and run:
                runs.append(run)
                run = []
            continue
        line, said = tok.start[0], tok.string.lstrip("#").strip()
        alone = not tok.line[:tok.start[1]].strip()
        if run and (not alone or last != line - 1 or not said):
            runs.append(run)
            run = []
        if said:
            run.append((line, said))
        if not alone and run:
            runs.append(run)
            run = []
        last = line
    if run:
        runs.append(run)
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return runs
    lines = text.split("\n")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            head = node.body[0]
            if isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant) and isinstance(head.value.value, str):
                written = lines[head.lineno - 1:head.end_lineno]
                written[-1] = written[-1][:head.end_col_offset]
                written[0] = written[0][head.col_offset:]
                written = [re.sub(r'^[rRbBuU]*("""|\'\'\'|"|\')', "", w) if i == 0 else w for i, w in enumerate(written)]
                written[-1] = re.sub(r'("""|\'\'\'|"|\')$', "", written[-1])
                runs += paragraphs([(head.lineno + i, w.strip()) for i, w in enumerate(written)])
    return runs


def paragraphs(lines):
    """-> [run] of a comment's or a docstring's lines, (line, text), a blank line ending each run."""
    runs, run = [], []
    for line, said in lines:
        if said:
            run.append((line, said))
        elif run:
            runs.append(run)
            run = []
    return runs + ([run] if run else [])


def tree_sitter_prose(text, language):
    """-> [run] of the prose of code tree-sitter parses, as its grammar reads the code's comments: each comment
    standing alone on its line joined with the line comments on the lines below it into one run, a block comment's
    paragraphs each a run with the stars opening its lines left out, and a comment after code a run of its own."""
    source = text.encode("utf-8")
    try:
        tree = tree_sitter_parser(language).parse(source)
    except Exception:  # the grammar could not be loaded or read the text: no prose is read from it
        return []
    lines, found, stack = text.split("\n"), [], [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type == "comment":
            found.append(node)
        stack.extend(reversed(node.children))
    runs, run, last = [], [], None
    for node in sorted(found, key=lambda n: n.start_byte):
        written = source[node.start_byte:node.end_byte].decode("utf-8", "replace")
        line = node.start_point[0] + 1
        alone = not lines[line - 1][:node.start_point[1]].strip()
        if written.startswith("//"):
            said = written.lstrip("/").strip()
            if run and (not alone or last != line - 1 or not said):
                runs.append(run)
                run = []
            if said:
                run.append((line, said))
            if not alone and run:
                runs.append(run)
                run = []
            last = line
            continue
        if run:
            runs.append(run)
            run = []
        body = re.sub(r"^/\*+|\*+/$", "", written).split("\n")
        runs += paragraphs([(line + i, re.sub(r"^\s*\*?\s?", "", b).strip()) for i, b in enumerate(body)])
    return runs + ([run] if run else [])


def run_sentences(run):
    """-> [(first line, last line, sentence)] of a run of prose, its lines joined by a space as CommonMark joins a
    paragraph's, each sentence bounded as Unicode Standard Annex #29 bounds it."""
    from uniseg.sentencebreak import sentences
    joined, at = "", []
    for line, piece in run:
        if joined:
            joined += " "
            at.append(line)
        joined += piece
        at += [line] * len(piece)
    out, pos = [], 0
    for sentence in sentences(joined):
        said = sentence.strip()
        if said:
            start = pos + len(sentence) - len(sentence.lstrip())
            out.append((at[start], at[start + len(said) - 1], said))
        pos += len(sentence)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# A search's result

class Place(str):
    """A place to read, as a result writes it: a citation of the narrowest of a keyed part, a section or a file that
    holds every line the place gives, with its lines and, where they all stand in one, `in a table`, `in a heading` or
    `in a fenced block`, and, where it holds a phrase's words with other words between them within one sentence,
    `words apart`. It keeps what it was written from: its file, its section's heading path, its keyed part's key, its
    first and last line, and whether its words stand apart."""

    def __new__(cls, path, lineage, key, first, last, stands="", apart=False):
        cite = path + (" § " + lineage if lineage else "") + (f" [{key}]" if key else "")
        text = (f"`{cite}` " + (f"line {first}" if last in (None, first) else f"lines {first}-{last}") + (f", in a {stands}" if stands else "")
                + (" words apart" if apart else ""))
        place = super().__new__(cls, text)
        place.path, place.lineage, place.key, place.first, place.last, place.stands = path, lineage, key, first, first if last is None else last, stands
        place.apart = apart
        return place

    def marked_apart(self):
        """-> the same place, marked as holding a phrase's words with other words between them."""
        return Place(self.path, self.lineage, self.key, self.first, self.last, self.stands, apart=True)


PLACE = re.compile(r"^`[^`\n]+`(?: lines? \d+(?:-\d+)?)?(?:, in a (?:table|heading|fenced block))?(?: words apart)?(?: cites `[^`\n]+`)?$")


class Result:
    """What a search gave, written as one file in the form the search skill gives a search's result, the same whoever
    asked."""

    def __init__(self, kind, query, narrowed, run_as, completeness, places, notes=(), target=CURRENT_OPERATIVE, commit=None, part=None, names_nothing=(), exact=False):
        self.kind, self.query, self.narrowed, self.run_as = kind, squeeze(query), list(narrowed), run_as
        # whether a search by terms was asked for exact, giving only where a phrase's words stand together
        self.exact = bool(exact) and kind == "terms"
        self.completeness, self.places, self.notes = completeness, list(places), list(notes)
        # the commit its asker named to the search, and the last commit where a search of the committed files named
        # none: a result holds the first only where one was asked for, so a record copied from it pins no search
        self.target, self.commit, self.last_commit = target, commit, None
        # the snapshot code of the files of the target as the search answered
        self.snapshot = None
        # where the question names nothing to ask of, each one of NAMES_NOTHING, and whether the answer is one the
        # search kept and gave again
        self.names_nothing, self.kept = list(names_nothing), False
        # the part of a ranking the places are: the place of the ranking the first of them is, and how many they are
        self.part = part if part or completeness == "complete" else (1, len(self.places))
        self.name = self.path = None

    def ranking_part(self):
        """-> the part of its ranking a ranked result holds, by its first place's number in the ranking and its
        last's, as `1 to 20`, or `none` where the ranking holds no place there."""
        first, count = self.part
        return f"{first} to {first + count - 1}" if count else "none"

    def body(self):
        def items(values, pad="      "):
            return "".join(f"{pad}- {v}\n" for v in values)

        out = f"    **Kind:** {self.kind} \\\n    **Query:** {self.query} \\\n" + ("    **Exact:** yes \\\n" if self.exact else "") + f"    **Target:** {self.target} \\\n"
        if self.commit:
            out += f"    **Commit:** {self.commit} \\\n"
        if self.last_commit:
            out += f"    **Last Commit:** {self.last_commit} \\\n"
        if self.narrowed:
            out += "    **Narrowed To:**\n" + items(f"`{p}`" for p in self.narrowed) + "\n"
        out += f"    **Snapshot:** {self.snapshot} \\\n"
        out += f"    **Run As:** {self.run_as} \\\n    **Completeness:** {self.completeness} \\\n"
        if self.completeness == "ranked":
            out += f"    **Ranking Part:** {self.ranking_part()} \\\n"
        out += "    **Places:**" + ("\n" + items(self.places) if self.places else " none\n")
        if self.notes:
            out += "\n    **Notes:**\n" + items(self.notes)
        return out

    def text(self):
        return ("# Search Result\n\nThe places are places to read, never findings. They are "
                + ("every place the search found." if self.completeness == "complete" else "a part of a ranking, and never every place.")
                + "\n\n**Records:**\n  - **Result:** " + self.name + " \\\n" + self.body())

    def write(self, folder):
        """Name the result from the kind of search, what was asked and its content, and write it. The name tells the
        result apart by its two hashes, and holds as many of the words asked as fit: no more than MAX_NAME, and no
        more than leaves the file's whole path within MAX_PATH, so a folder standing deep, as one of a copy of the project's files kept
        beneath its working files does, shortens the words and never makes a path too long to open. An earlier
        result of the same question under another name is cleared, another part of the same ranking being another
        question. A run that finds a file changed clears every result before it answers, so no result outlives the
        files it answered for."""
        part = "\0" + self.run_as if self.completeness == "ranked" else ""
        part += "\0exact" if self.exact else ""   # a search asked for exact is another question than one asked by default
        asked = hashlib.sha256((self.kind + "\0" + self.query + "\0" + "\0".join(self.narrowed) + "\0" + self.target + "\0" + (self.commit or "") + part).encode()).hexdigest()[:6]
        content = hashlib.sha256(self.body().encode()).hexdigest()[:8]
        kind = self.kind.replace(" ", "-")
        slug = re.sub(r"[^a-z0-9]+", "-", self.query.lower()).strip("-")
        longest = min(MAX_NAME, MAX_PATH - len(str(Path(folder).resolve())) - 1)
        room = longest - len(kind) - len(asked) - len(content) - len(".md") - 3
        slug = slug[:max(room, 0)].strip("-") or "query"
        self.name = f"{kind}-{slug}-{asked}-{content}.md"
        folder.mkdir(parents=True, exist_ok=True)
        for stale in folder.glob(f"{kind}-*-{asked}-*.md"):
            if stale.name != self.name:
                stale.unlink()
        self.path = folder / self.name
        self.path.write_bytes(self.text().encode("utf-8"))
        return self.path

    @staticmethod
    def check(path):
        """-> [problems] of a result's file against the form its skill states: the name it holds is its file's, and
        the hash its name ends with is its content's, so a file whose content was changed no longer gives it."""
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^  - \*\*Result:\*\* (\S+) \\\n", text, re.M)
        if not m or not text.startswith("# Search Result\n"):
            return [f"{path.name}: it is not a search's result in the form the skill states"]
        problems = []
        if m.group(1) != path.name:
            problems.append(f"{path.name}: its Result names `{m.group(1)}`, another file")
        held = {}
        for field in ("Kind", "Query", "Exact", "Target", "Commit", "Last Commit", "Snapshot", "Run As", "Completeness", "Ranking Part", "Places"):
            f = re.search(r"^    \*\*" + field + r":\*\*(?: (.*?))?(?: \\)?$", text, re.M)
            if f:
                held[field] = (f.group(1) or "").strip()
            elif field not in ("Exact", "Commit", "Last Commit", "Ranking Part"):
                problems.append(f"{path.name}: it holds no {field}")
        if held.get("Kind") not in KINDS + (None,):
            problems.append(f"{path.name}: its Kind is `{held['Kind']}`, no kind of search")
        # a result holding no Exact was asked by default, its value "no" read where none is written
        if "Exact" in held and held["Exact"] not in ("yes", "no"):
            problems.append(f"{path.name}: its Exact is `{held['Exact']}`, neither yes nor no")
        elif held.get("Exact") == "yes" and held.get("Kind") != "terms":
            problems.append(f"{path.name}: it was asked for exact, and only a search by terms is")
        if held.get("Target") not in TARGETS + (None,):
            problems.append(f"{path.name}: its Target is `{held['Target']}`, not one of {', '.join(TARGETS)}")
        if "Target" in held:
            # a Commit is the one its asker named, and a Last Commit the one a search naming none read: a result of
            # the committed files holds exactly one of the two, and a result of another target neither
            commits = [name for name in ("Commit", "Last Commit") if name in held]
            if held["Target"] in OF_A_COMMIT and len(commits) != 1:
                problems.append(f"{path.name}: it answered over the committed files and " + ("holds neither the Commit its asker named nor the Last Commit it read" if not commits else "holds both a Commit and a Last Commit"))
            elif held["Target"] not in OF_A_COMMIT and commits:
                problems.append(f"{path.name}: it names a {commits[0]}, and its Target is not the committed files")
        if "Snapshot" in held and not SNAPSHOT.fullmatch(held["Snapshot"]):
            problems.append(f"{path.name}: its Snapshot is `{held['Snapshot']}`, not a snapshot code, sixteen hexadecimal digits")
        if held.get("Target") == WORKING and "\n    **Narrowed To:**" not in text:
            problems.append(f"{path.name}: it answered over the working files and holds no Narrowed To, the paths it was given")
        listed = re.search(r"^    \*\*Places:\*\*\n((?:      - .*\n)*)", text, re.M)
        count = len(listed.group(1).splitlines()) if listed else 0
        if (held.get("Completeness") == "ranked") != ("Ranking Part" in held) and "Completeness" in held:
            problems.append(f"{path.name}: " + ("its places are a part of a ranking and it names no Ranking Part" if held["Completeness"] == "ranked" else "it names a Ranking Part, and its places are no part of a ranking"))
        elif "Ranking Part" in held:
            part = re.fullmatch(r"(\d+) to (\d+)", held["Ranking Part"])
            if not part and held["Ranking Part"] != "none":
                problems.append(f"{path.name}: its Ranking Part is `{held['Ranking Part']}`, neither `none` nor its first place's number in the ranking and its last's, as `1 to 20`")
            elif (int(part.group(2)) - int(part.group(1)) + 1 if part else 0) != count or (part and int(part.group(1)) < 1):
                problems.append(f"{path.name}: its Ranking Part is `{held['Ranking Part']}`, and it holds {count} place{'' if count == 1 else 's'}")
        for item in listed.group(1).splitlines() if listed else []:
            if not PLACE.match(item[8:]):
                problems.append(f"{path.name}: a place not in its form, a citation with its lines: {item[8:]}")
            elif (" cites `" in item) != (held.get("Kind") == "cited sections"):
                problems.append(f"{path.name}: " + ("a place of a listing of cited sections that says nothing of what it cites: " if held.get("Kind") == "cited sections" else "a place saying what it cites, in a result that is no listing of cited sections: ") + item[8:])
        content = hashlib.sha256(text[m.end():].encode()).hexdigest()[:8]
        if not path.stem.endswith("-" + content):
            problems.append(f"{path.name}: its content was changed since the search wrote it, since its name no longer ends with the hash of its content, {content}")
        return problems

    def summary(self, root):
        where = self.path.relative_to(root).as_posix() if self.path else "(not written)"
        count = len(self.places)
        out = [f"{where}", f"{count} place{'' if count == 1 else 's'}, {self.completeness}: places to read, never findings"]
        if count <= FEW:
            out += ["  " + p for p in self.places]
        return "\n".join(out)


# ---------------------------------------------------------------------------------------------------------------------
# The index and the searches

def under(base, root):
    """-> each file under a folder, as a path from the root, a cache a tool leaves aside: the folder one of the files
    as they stand, or one of a commit's."""
    if isinstance(base, spec_text.CommitTree):
        for f in base.rglob("*"):
            if f.is_file() and "__pycache__" not in f.rel.split("/") and not f.rel.endswith((".pyc", ".pyo")):
                yield f.rel
        return
    for folder, folders, files in os.walk(base):
        folders[:] = sorted(d for d in folders if d != "__pycache__")
        for name in sorted(files):
            if not name.endswith((".pyc", ".pyo")):
                yield (Path(folder) / name).relative_to(root).as_posix()


def listed(tree, root, kind=spec_text.OPERATIVE):
    """-> [path from the root] of every durable file of a kind a tree holds, the files as they stand or a commit's.
    The operative files are the files of each kind the canon names for the scope, read from the scope's own listing,
    and the stack's code roots less the paths it excludes, no fixture file among them. The fixture files are the
    files of the kept tests' fixtures folder alone. Each file is told for its kind by where it stands
    (`spec_text.durable_kind`), so neither listing holds a file of the other."""
    out = set()
    # @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs
    for place in spec_text.scope_paths(tree, kind):
        base = tree / place
        if base.is_file():
            out.add(place)
        elif base.is_dir():
            out.update(under(base, root))
    # @canon-spec specs/methodology/spec-placement/technical-stack.md § The Technical Stack
    stack = code_checks.code_roots(tree) if kind == spec_text.OPERATIVE else None
    if stack:
        out.update(rel for _, rel in code_checks.code_files(tree, *stack) if "__pycache__" not in rel.split("/"))
    return sorted(rel for rel in out if spec_text.durable_kind(rel) == kind)


def operative_files(root, committed=False):
    """-> [path from the root] of every operative file, as the files stand or, committed, as the last commit holds
    them, listed with no search run and no index opened: nothing the search requires is asked for, but git for the
    committed files, the search stopping as `committed_tree` has it where they cannot be read."""
    root = Path(root).resolve()
    return listed(committed_tree(root)[1] if committed else root, root, spec_text.OPERATIVE)


def fixture_files(root, committed=False):
    """-> [path from the root] of every fixture file, as the files stand or, committed, as the last commit holds them,
    listed as `operative_files` lists the operative files."""
    root = Path(root).resolve()
    return listed(committed_tree(root)[1] if committed else root, root, spec_text.FIXTURE)


class Search:
    """The search over one project and one target. `Search(root)` checks everything the search requires, then brings
    the index up to date for the operative files as they stand. `target` names another: COMMITTED_OPERATIVE, the
    operative files as `commit` held them, the last commit unless one is named; CURRENT_FIXTURE and COMMITTED_FIXTURE,
    the fixture files the same two ways; or WORKING, the working files under `paths`, which that target requires. It
    opens the index of the kind of durable file its target reads, which holds no file of the other kind, so nothing it
    answers rests on one. `cover`, given by a test, names the files to cover in place of the canon's listing, each
    still told for its kind by where it stands."""

    def __init__(self, root, cover=None, scratch=None, quiet=False, target=CURRENT_OPERATIVE, commit=None, paths=None):
        self.root = Path(root).resolve()
        check_requirements(self.root)
        if target not in TARGETS:
            raise ValueError(f"no target `{target}`: a target is one of {', '.join(TARGETS)}")
        if commit and target not in OF_A_COMMIT:
            raise ValueError(f"a commit is named for a search of `{COMMITTED_OPERATIVE}` or of `{COMMITTED_FIXTURE}` alone, and this one is of `{target}`")
        self.target, self.commit, self.tree, self.paths = target, None, None, self._narrow(paths)
        # the kind of durable file whose index the search reads: its target's, and the operative files' for a search
        # of the working files, which reads what its places cite against them
        self.kind = DURABLE_KIND.get(target, spec_text.OPERATIVE)
        # whether its asker named the commit: a search naming none reads the last commit, and its result says so
        self.named = bool(commit)
        self.computed, self._codes = 0, {}
        if target == WORKING:
            if not self.paths:
                raise ValueError(f"a search of `{WORKING}` answers over the paths it is given and is given none: name them with --paths")
            for p in self.paths:
                if not any(p == w or p.startswith(w + "/") for w in WORKING_FILES):
                    raise ValueError(f"`{p}` is no working file: a search of `{WORKING}` covers paths under " + ", ".join(f"`{w}`" for w in WORKING_FILES) + " alone")
        if target in OF_A_COMMIT:
            # asked before anything is read or written, so a search that cannot be answered leaves nothing behind
            self.commit, self.tree = committed_tree(self.root, commit)
        self.scratch = Path(scratch) if scratch else self.root / SCRATCH
        self.cover, self.quiet, self.embedder = cover, quiet, None
        self.read_count, self.built, self.seconds, self._lineages, self.repeated = 0, False, 0.0, {}, set()
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.db = self._open()
        self.update()

    # -- the files a search covers

    def covered(self, target=None):
        """-> [path from the root] of every file a target holds, the search's own unless another is named. A target of
        the durable files holds the files of its kind alone, the operative files or the fixture files, as `listed`
        gives them: as they stand, read from the folders with no version control asked, or as the commit held them,
        the scope's listing and the stack read from the commit too. The working files are those under the paths the
        search was given. A cache a tool leaves among them is not listed."""
        target = target or self.target
        if target == WORKING:
            found = set()
            for p in self.paths:
                base = self.root / p
                found.update([p] if base.is_file() else self._under(base) if base.is_dir() else [])
            own = SCRATCH + "/"   # the search's own index and results are no place a search reads
            return sorted(f for f in found if not f.startswith(own) and (self.cover is None or f in self.cover))
        tree, kind = self.tree if target in OF_A_COMMIT else self.root, DURABLE_KIND[target]
        if self.cover is not None:
            return sorted(f for f in self.cover if spec_text.durable_kind(f) == kind and (target not in OF_A_COMMIT or (tree / f).is_file()))
        return listed(tree, self.root, kind)

    def _under(self, base):
        return under(base, self.root)

    # -- the index

    def _open(self):
        """-> the index of the kind of durable file the search reads, opened, and made where it is new or its form or
        its model is another's. Every table a search reads, a ranking's words and vectors among them, holds the
        content of that index's files alone."""
        import sqlite_vec
        db = sqlite3.connect(self.scratch / INDEX[self.kind])
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        db.execute("create table if not exists meta(key text primary key, value text)")
        row = db.execute("select value from meta where key='schema'").fetchone()
        if not row or row[0] != SCHEMA + "/" + MODEL:
            for (name,) in db.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' and name != 'meta'").fetchall():
                try:
                    db.execute(f"drop table if exists {name}")
                except sqlite3.OperationalError:
                    pass
            db.executescript(f"""
                create table placed(target text, path text, sha text, size integer, mtime_ns integer, stamp text, primary key(target, path));
                create table contents(sha text primary key, kind text, language text, note text);
                create table lines(sha text, n integer, text text, stands text, primary key(sha, n));
                create table parts(sha text, lineage text, key text, line_start integer, line_end integer);
                create index parts_sha on parts(sha, lineage);
                create virtual table terms using fts5(norm, sha unindexed, n unindexed, tokenize='porter unicode61');
                create virtual table term_pairs using fts5(norm, sha unindexed, n unindexed, tokenize='porter unicode61');
                create table headings(sha text, lineage text, occurrence integer, level integer, line integer, own_end integer, subtree_end integer);
                create table citations(sha text, line integer, host text, form text, fenced integer, written text, path text, lineage text, key text, unit text);
                create table units(sha text, name text, kind text, line_start integer, line_end integer);
                create table structures(sha text, structure text, name text, unit text, line integer);
                create table passages(id integer primary key, sha text, lineage text, line_start integer, line_end integer, text text, text_sha text);
                create virtual table passage_terms using fts5(norm, pid unindexed, tokenize='porter unicode61');
                create table embeddings(text_sha text primary key, vector blob);
                create virtual table passage_vectors using vec0(embedding float[{DIMENSIONS}] distance_metric=cosine);
                create table sentences(id integer primary key, sha text, pid integer, text text, text_sha text);
                create virtual table sentence_terms using fts5(norm, pid unindexed, tokenize='porter unicode61');
                create virtual table sentence_vectors using vec0(embedding float[{DIMENSIONS}] distance_metric=cosine);
                create index sentences_sha on sentences(sha);
                create index sentences_text on sentences(text_sha);
                create index placed_sha on placed(sha);
                create index headings_sha on headings(sha);
                create index citations_target on citations(path, lineage);
                create index citations_sha on citations(sha);
                create index structures_name on structures(name, structure);
                create index passages_sha on passages(sha);
                create index passages_text on passages(text_sha);
                create table term_rows(sha text, name text, first integer, last integer);
                create index term_rows_sha on term_rows(sha);
                create index units_sha on units(sha);
                create index structures_sha on structures(sha);
            """)
            db.execute("insert or replace into meta values('schema', ?)", (SCHEMA + "/" + MODEL,))
            db.commit()
            self.built = True
        # the answers the search kept, one to a question: what was asked, the snapshot code of the files it answered
        # over, the code of the search's own reading, and for a search of the working files the code of the operative
        # files as they stand (`kept_answer`)
        db.execute("create table if not exists answers(asked text primary key, snapshot text, reading text, operative text, held text)")
        # the index holds each target's files apart, which content stands at which path in each, and a search reads
        # its own target's alone: `files` is those, and `known` adds the operative files as they stand for a search of
        # the working files, which reads a place a working file cites against them and gives no place among them
        known = (self.target, CURRENT_OPERATIVE) if self.target == WORKING else (self.target,)
        db.execute(f"create temp view files as select path, sha, size, mtime_ns from placed where target = '{self.target}'")
        db.execute("create temp view known as select path, sha from placed where target in (" + ", ".join(f"'{t}'" for t in known) + ")")
        return db

    def update(self):
        """Bring the index up to date for the search's target, and for the operative files as they stand where a search
        of the working files reads what its places cite against them. Any file changed clears every result."""
        started = time.perf_counter()
        changed = self._bring(CURRENT_OPERATIVE) if self.target == WORKING else False
        listed, mine = self._bring(self.target, own=True)
        if changed or mine:
            for stale in (self.scratch / "results").glob("*.md"):
                stale.unlink()
        self.db.commit()
        self.seconds = time.perf_counter() - started
        if not self.quiet:
            if self.built:
                print(f"index: built whole from {self.read_count} files in {self.seconds:.1f} seconds", file=sys.stderr)
            else:
                print(f"index: {listed} files covered, {self.read_count} read again, {self.seconds:.2f} seconds", file=sys.stderr)

    def _bring(self, target, own=False):
        """Bring one target's files up to date -> whether any changed, with the count listed where `own`. A file as it
        stands is read only where its size or the time it was changed differs from what the index holds, and a
        commit's only where git's own name for its content does. A content is parsed only where it is new to the
        index. A working file the search in hand was not given keeps its content in the index, held apart, so a search
        given it again reads it only where it changed."""
        db, tree = self.db, self.tree if target in OF_A_COMMIT else None
        sources = (WORKING, HELD) if target == WORKING else (target,)
        held = {}
        for source in sources:
            for p, sha, size, mtime, stamp in db.execute("select path, sha, size, mtime_ns, stamp from placed where target=?", (source,)):
                held[p] = (sha, size, mtime, stamp, source)
        listed, left, read, moved = self.covered(target), set(), 0, False
        stack = code_checks.code_roots(tree or self.root) if self.cover is None else None
        self._roots = stack[0] if stack else []
        for rel in listed:
            was = held.get(rel)
            if tree is not None:
                stamp, size, mtime = tree.store["files"][rel], 0, 0
                same = was and was[3] == stamp
            else:
                try:
                    stat = (self.root / rel).stat()
                except OSError:
                    continue
                stamp, size, mtime = "", stat.st_size, stat.st_mtime_ns
                same = was and was[1] == size and was[2] == mtime
            if same:
                if was[4] != target:
                    db.execute("update placed set target=? where target=? and path=?", (target, was[4], rel))
                    moved = True
                continue
            data = ((tree if tree is not None else self.root) / rel).read_bytes()  # a commit's files are held already
            read += 1
            sha = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
            if not db.execute("select 1 from contents where sha=?", (sha,)).fetchone():
                self._index(sha, rel, data)
            if was:
                left.add(was[0])
                db.execute("delete from placed where target=? and path=?", (was[4], rel))
            db.execute("insert or replace into placed values(?,?,?,?,?,?)", (target, rel, sha, size, mtime, stamp))
        gone = set(held) - set(listed)
        for p in gone:
            if target == WORKING and (self.root / p).is_file():
                if held[p][4] != HELD:
                    db.execute("update placed set target=? where target=? and path=?", (HELD, WORKING, p))
                    moved = True
                continue
            left.add(held[p][0])
            db.execute("delete from placed where target=? and path=?", (held[p][4], p))
        gone = {p for p in gone if not (target == WORKING and (self.root / p).is_file())}
        self.read_count += read
        if read or gone:
            # only the content a changed or removed file held is looked at again, so this costs what changed; no
            # vector is computed here, since only a search by meaning reads one (`_embed_missing`)
            for sha in left:
                if not db.execute("select 1 from placed where sha=? limit 1", (sha,)).fetchone():
                    self._drop(sha)
        changed = bool(read or gone or moved)
        return (len(listed), changed) if own else changed

    def _drop(self, sha):
        """Take out of the index what one content gave, no file holding that content any more."""
        db = self.db
        passages = db.execute("select id, text_sha from passages where sha=?", (sha,)).fetchall()
        parts = db.execute("select id, text_sha from sentences where sha=?", (sha,)).fetchall()
        db.executemany("delete from passage_vectors where rowid=?", [(pid,) for pid, _ in passages])
        db.executemany("delete from passage_terms where rowid=?", [(pid,) for pid, _ in passages])
        db.executemany("delete from sentence_vectors where rowid=?", [(sid,) for sid, _ in parts])
        db.executemany("delete from sentence_terms where rowid=?", [(sid,) for sid, _ in parts])
        for name, first, last in db.execute("select name, first, last from term_rows where sha=?", (sha,)).fetchall():
            db.execute(f"delete from {name} where rowid between ? and ?", (first, last))
        for table in ("contents", "lines", "parts", "term_rows", "headings", "citations", "units", "structures", "passages", "sentences"):
            db.execute(f"delete from {table} where sha=?", (sha,))
        db.executemany("delete from embeddings where text_sha=? and not exists (select 1 from passages where text_sha=?) and not exists (select 1 from sentences where text_sha=?)",
                       [(ts, ts, ts) for ts in {ts for _, ts in passages + parts}])

    def _terms(self, name, sha, rows):
        """Index the words of a content's lines under row numbers of its own run, kept so the rows are found again by
        their numbers when the content leaves the index."""
        db = self.db
        first = (db.execute("select value from meta where key=?", (name,)).fetchone() or ("0",))[0]
        first = int(first) + 1
        db.executemany(f"insert into {name}(rowid, norm, sha, n) values(?,?,?,?)", [(first + i, norm, sha, n) for i, (norm, n) in enumerate(rows)])
        if rows:
            db.execute("insert into term_rows values(?,?,?,?)", (sha, name, first, first + len(rows) - 1))
            db.execute("insert or replace into meta values(?,?)", (name, str(first + len(rows) - 1)))

    def _index(self, sha, rel, data):
        db, suffix, stem = self.db, Path(rel).suffix.lower(), Path(rel).stem
        try:
            text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        except UnicodeDecodeError:
            db.execute("insert into contents values(?,?,?,?)", (sha, "binary", "", "it is no text, and nothing in it is searched"))
            return
        lines = text.split("\n")
        kind, language, note, stands = "text", "", "", [""] * len(lines)
        if suffix == ".md":
            kind = "markdown"
            plain = strip_links(text)
            rows = markdown_lines(plain)
            stands = [STANDS.get(ln.stands_in, "") for ln in reading.lines(plain)]
            heads = markdown_headings(rows)
            db.executemany("insert into headings values(?,?,?,?,?,?,?)", [(sha,) + h for h in heads])
            db.executemany("insert into parts values(?,?,?,?,?)", [(sha,) + p for p in markdown_parts([r[0] for r in rows], [r[1] for r in rows], heads)])
            db.executemany("insert into citations values(?,?,?,?,?,?,?,?,?,'')", [(sha,) + c for c in markdown_citations(rows, heads)])
            db.executemany("insert into passages(sha, lineage, line_start, line_end, text, text_sha) values(?,?,?,?,?,?)",
                           [(sha, p[0], p[1], p[2], p[3], hashlib.sha256(p[3].encode()).hexdigest()) for p in markdown_passages(rows, heads)])
        elif suffix in LANGUAGES or suffix in NO_UNITS or self._is_code(rel):
            kind, language = "code", LANGUAGES.get(suffix, "")
            comments = None
            if language == "python":
                units, structures, note = read_python(text, stem)
                comments = python_comment_lines(text)
            elif language:
                units, structures, note, comments = read_tree_sitter(text, stem, language)
            else:
                units, structures = [(stem, "file", 1, len(lines))], []
                note = (f"{NO_UNITS[suffix]} has no units, so the file is one unit and no structure is searched in it" if suffix in NO_UNITS
                        else f"the search has no parser for a {suffix or 'file of this kind'} file, so the file is one unit and no structure is searched in it")
            db.executemany("insert into units values(?,?,?,?,?)", [(sha,) + u for u in units])
            db.executemany("insert into structures values(?,?,?,?,?)", [(sha,) + s for s in structures])
            for line, written, path, lineage, key in comment_annotations(lines):
                if comments is not None and line not in comments:
                    continue
                db.execute("insert into citations values(?,?,?,?,?,?,?,?,?,?)", (sha, line, "", "annotation", 0, written, path, lineage, key, unit_under(units, line)))
            if language == "python":
                try:
                    for node in ast.walk(ast.parse(text)):
                        doc = ast.get_docstring(node) if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) else None
                        for piece in split_passage(squeeze(doc)) if doc else []:
                            first = getattr(node, "lineno", 1)
                            db.execute("insert into passages(sha, lineage, line_start, line_end, text, text_sha) values(?,?,?,?,?,?)",
                                       (sha, "", first, first + doc.count("\n") + 1, piece, hashlib.sha256(piece.encode()).hexdigest()))
                except (SyntaxError, ValueError):
                    pass
        db.execute("insert into contents values(?,?,?,?)", (sha, kind, language, note))
        db.executemany("insert into lines values(?,?,?,?)", [(sha, i + 1, line, stands[i] if i < len(stands) else "") for i, line in enumerate(lines)])
        self._terms("terms", sha, [(normalize(line), i + 1) for i, line in enumerate(lines) if line.strip()])
        self._terms("term_pairs", sha, [(normalize(line + " " + lines[i + 1]), i + 1) for i, line in enumerate(lines[:-1]) if line.strip() and lines[i + 1].strip()])
        held = db.execute("select id, text from passages where sha=?", (sha,)).fetchall()
        db.executemany("insert into passage_terms(rowid, norm, pid) values(?,?,?)", [(pid, normalize(t), pid) for pid, t in held])
        db.executemany("insert into sentences(sha, pid, text, text_sha) values(?,?,?,?)",
                       [(sha, pid, s, hashlib.sha256(s.encode()).hexdigest()) for pid, t in held for s in sentences(t)])
        db.executemany("insert into sentence_terms(rowid, norm, pid) values(?,?,?)",
                       [(sid, normalize(t), pid) for sid, pid, t in db.execute("select id, pid, text from sentences where sha=?", (sha,)).fetchall()])

    def _is_code(self, rel):
        if self.cover is not None:
            return Path(rel).suffix.lower() not in ("", ".txt")
        if self._roots is None:
            stack = code_checks.code_roots(self.root)
            self._roots = stack[0] if stack else []
        return rel.startswith(".ai/skills/") and "/scripts/" in rel or any(rel.startswith(r + "/") for r in self._roots)

    _roots = None

    def _embed(self, new):
        """Give each passage of the contents new to the index its vector, and each sentence of a passage holding
        several: a text the index already holds a vector for is not run through the model again."""
        db, todo = self.db, {}
        for sha in new:
            for table in ("passages", "sentences"):
                for text, text_sha in db.execute(f"select text, text_sha from {table} where sha=? and text_sha not in (select text_sha from embeddings)", (sha,)):
                    todo[text_sha] = text
        # the model pads a batch to its longest text, and holds what a batch needs: texts of a like length are run
        # together, a few at a time, and each run's vectors are written before the next, so memory stays level
        ordered = sorted(todo.items(), key=lambda item: len(item[1]))
        for at in range(0, len(ordered), EMBED_RUN):
            run = ordered[at:at + EMBED_RUN]
            db.executemany("insert or replace into embeddings values(?,?)", list(zip([k for k, _ in run], self._vectors([v for _, v in run]))))
        for sha in new:
            db.execute("insert into passage_vectors(rowid, embedding) select p.id, e.vector from passages p join embeddings e on e.text_sha = p.text_sha"
                       " where p.sha=? and p.id not in (select rowid from passage_vectors)", (sha,))
            db.execute("insert into sentence_vectors(rowid, embedding) select s.id, e.vector from sentences s join embeddings e on e.text_sha = s.text_sha"
                       " where s.sha=? and s.id not in (select rowid from sentence_vectors)", (sha,))

    def _embed_missing(self):
        """Give each passage and each sentence the index holds with no vector yet its vector, through `_embed`, so only
        a search by meaning computes one, and the vectors it writes are kept for every later search."""
        missing = [sha for (sha,) in self.db.execute(
            "select sha from passages where id not in (select rowid from passage_vectors)"
            " union select sha from sentences where id not in (select rowid from sentence_vectors)")]
        if missing:
            self._embed(missing)
            self.db.commit()

    def _vectors(self, texts):
        import sqlite_vec
        if self.embedder is None:
            from fastembed import TextEmbedding
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            self.embedder = TextEmbedding(model_name=MODEL, cache_dir=str(model_folder()), local_files_only=True,
                                          threads=model_threads())
        return [sqlite_vec.serialize_float32([float(x) for x in v]) for v in self.embedder.embed(texts, batch_size=EMBED_BATCH)]

    # -- helpers the searches share

    def _narrow(self, narrowed):
        """-> the paths a search is narrowed to, a search of the working files being narrowed to the paths it was given
        where it names none narrower."""
        return [p.replace("\\", "/").strip("/") for p in narrowed or []] or list(getattr(self, "paths", []))

    def _within(self, path, narrowed):
        return not narrowed or any(path == n or path.startswith(n + "/") for n in narrowed)

    def _place(self, path, line, end=None):
        """-> a place to read: a citation of the narrowest of a keyed part, a section or a file that holds every line
        from `line` to `end`, with those lines and what they all stand in. Where two headings of a file share a path,
        the path names what both hold, read together: a place under either is cited by the path with its own lines, and
        the result notes that the path stands more than once and where, so its reader reads each."""
        end = line if end is None else end
        row = self.db.execute(
            "select h.lineage, f.sha from files f join headings h on h.sha = f.sha where f.path=? and h.line<=? and h.subtree_end>? and h.lineage != '' "
            "order by h.line desc limit 1", (path, line, end)).fetchone()
        lineage, key = (row[0] if row else ""), None
        if row:
            if self.db.execute("select count(*) from headings where sha=? and lineage=?", (row[1], lineage)).fetchone()[0] > 1:
                self.repeated.add((path, lineage))
            part = self.db.execute("select key from parts where sha=? and lineage=? and line_start<=? and line_end>=? order by line_end - line_start, line_start limit 1",
                                   (row[1], lineage, line, end)).fetchone()
            key = part[0] if part else None
        return Place(path, lineage, key, line, end, self._stands(path, line, end))

    def _stands(self, path, line, end):
        """-> what every line of a place that is not blank stands in, `table`, `heading` or `fenced block`, or '' where
        they stand in running text or in more than one."""
        found = {r[0] for r in self.db.execute("select distinct l.stands from files f join lines l on l.sha=f.sha where f.path=? and l.n between ? and ? and trim(l.text) != ''", (path, line, end))}
        return found.pop() if len(found) == 1 else ""

    def _finish(self, result):
        result.target = self.target
        result.commit, result.last_commit = (self.commit, None) if self.named else (None, self.commit)
        result.snapshot = self.snapshot_code()
        for path, lineage in sorted(self.repeated):
            result.notes.append(self._shared(path, lineage))
        self.repeated.clear()
        if self.target == WORKING and not result.narrowed:
            result.narrowed = list(self.paths)
        result.write(self.scratch / "results")
        return result

    # -- the state of the files a search answers for, and the answers the search keeps

    def snapshot_code(self, target=None):
        """-> the snapshot code of the files of a target as the index now holds them, the search's own unless another
        is named: built from the path and the content of each file, in the order of their paths, and written as
        sixteen hexadecimal digits. One code for the whole target, whatever paths a search is narrowed to; for the
        working files, the code of the paths the search was given. It is built one way whatever the target, so the
        files a commit held and the files as they stand take one code where each file holds the same."""
        target = target or self.target
        if target not in self._codes:
            held = hashlib.sha256()
            for path, sha in self.db.execute("select path, sha from placed where target=? order by path", (target,)):
                held.update(f"{path}\0{sha}\n".encode())
            self._codes[target] = held.hexdigest()[:16]
        return self._codes[target]

    def _asked(self, kind, query, narrowed, exact=False):
        """-> the name the search keeps an answer under: the kind of search, what was asked, whether a search by terms
        was asked for exact, the target, with the commit its asker named, and the paths it was narrowed to."""
        asked = [kind, squeeze(query), "exact" if exact else "", self.target, self.commit if self.named else "", "\0".join(narrowed), "\0".join(self.paths)]
        return hashlib.sha256("\1".join(asked).encode()).hexdigest()

    def kept_answer(self, kind, query, narrowed, exact=False):
        """-> the answer the search kept for this question, or None where it kept none that still stands: the same kind of
        search, Query, asking for exact or by default, Target, with the Commit, and paths, kept under the snapshot code the Target's files now take and under
        the code of the search's own reading, built from what this script and each module of the shared code it imports hold
        as the files running it have them, with the index's form and the model's name. An answer is kept only of a kind
        resting on its Target's files alone: none of a search by meaning, and none of a search of the structure `constructs`.
        Each other answer the search computes is kept so, with the index."""
        if not self._keeps(kind, query):
            return None
        row = self.db.execute("select snapshot, reading, operative, held from answers where asked=?", (self._asked(kind, query, narrowed, exact),)).fetchone()
        if not row or (row[0], row[1], row[2]) != (self.snapshot_code(), own_reading(), self._operative()):
            return None
        held = json.loads(row[3])
        places = [Place(*p) if isinstance(p, list) else p for p in held["places"]]
        result = Result(kind, held["query"], held["narrowed"], held["run_as"], held["completeness"], places, held["notes"], names_nothing=held["names_nothing"], exact=exact)
        result.kept = True
        return result

    def _keeps(self, kind, query):
        return kind in KEPT_KINDS and not (kind == "code structure" and squeeze(query).split(" ")[0] in NOT_KEPT_STRUCTURES)

    def _operative(self):
        """-> the snapshot code of the operative files as they stand, which a search of the working files reads what its
        places cite against and so keeps its answer under too, or '' for a search of another target."""
        return self.snapshot_code(CURRENT_OPERATIVE) if self.target == WORKING else ""

    def _keep(self, result, query, narrowed):
        """Keep an answer the search computed, in place of any it kept for the same question."""
        if not self._keeps(result.kind, query):
            return
        places = [[p.path, p.lineage, p.key, p.first, p.last, p.stands, p.apart] if isinstance(p, Place) else str(p) for p in result.places]
        held = json.dumps({"query": result.query, "narrowed": result.narrowed, "run_as": result.run_as, "completeness": result.completeness,
                           "places": places, "notes": [str(n) for n in result.notes], "names_nothing": result.names_nothing})
        self.db.execute("insert or replace into answers values(?,?,?,?,?)", (self._asked(result.kind, query, narrowed, result.exact), self.snapshot_code(), own_reading(), self._operative(), held))
        self.db.commit()

    def _answer(self, kind, query, narrowed, compute, exact=False):
        """-> the result of a search of a kind the search may keep an answer of: the answer it kept where one still
        stands, and otherwise the answer computed anew, which it then keeps."""
        kept = self.kept_answer(kind, query, narrowed, exact)
        if kept is not None:
            return self._finish(kept)
        self.computed += 1
        result = compute()
        self._nothing_under(result, narrowed)
        result = self._finish(result)
        self._keep(result, query, narrowed)
        return result

    def _nothing_under(self, result, narrowed):
        """Tell the caller of each path the search was narrowed to under which no file of its target stands."""
        for path in narrowed:
            if not self.db.execute("select 1 from files where path=? or (path > ? and path < ?) limit 1", (path, path + "/", path + "0")).fetchone():
                result.notes.append(f"the search was narrowed to `{path}`, and no file of `{self.target}` stands under it, so it asked of nothing there")
                if NO_FILE not in result.names_nothing:
                    result.names_nothing.append(NO_FILE)

    def _shared(self, path, lineage, among="files"):
        """-> the note of a path more than one heading of a file holds: how many times it stands and at which lines,
        so a reader of a place under one of them reads each."""
        at = [r[0] for r in self.db.execute(f"select h.line from {among} f join headings h on h.sha=f.sha where f.path=? and h.lineage=? order by h.line", (path, lineage))]
        return (f"`{path}`: the path `{lineage}` stands more than once in the file, {len(at)} times, at lines {', '.join(str(n) for n in at)}. "
                f"A citation of it names what they hold together, so read each")

    def _rows(self, path, first, last, among="files"):
        """-> [(line, text, a citation's link set aside)] of a file's lines from `first` up to `last`."""
        return [(n, strip_links(text)) for n, text in self.db.execute(
            f"select l.n, l.text from {among} f join lines l on l.sha=f.sha where f.path=? and l.n>=? and l.n<? order by l.n", (path, first, last))]

    def _resolve(self, citation, among="files"):
        """-> (path, lineage, key, why): the place a citation names among the target's files, or why it names none.
        With `among` "known", a search of the working files reads it against the operative files as they stand too,
        for the place a working file cites."""
        parsed = parse_citation(citation.strip().strip("`"))
        if not parsed:
            return None, None, None, "it is not in a citation's form"
        path, lineage, key = parsed
        if path is None:
            return None, None, None, "it names no file, and a search has no file of its own to read a same-file citation against"
        if not self.db.execute(f"select 1 from {among} where path=? or path like ?", (path, path + "/%")).fetchone():
            return path, lineage, key, f"`{path}` is not among the files the search covers"
        if lineage and not self.db.execute(f"select 1 from {among} f join headings h on h.sha=f.sha where f.path=? and h.lineage=?", (path, lineage)).fetchone():
            return path, lineage, key, f"`{path}` holds no section `{lineage}`"
        return path, lineage, key, None

    # -- who cites a place

    def citers(self, citation, narrowed=None):
        narrowed = self._narrow(narrowed)
        return self._answer("citers", citation, narrowed, lambda: self._citing(citation, narrowed))

    def _citing(self, citation, narrowed=None):
        """-> the result of a search for the places citing a place, not yet written as a file."""
        narrowed = self._narrow(narrowed)
        path, lineage, key, why = self._resolve(citation, "known")
        if why and path is None:
            return Result("citers", citation, narrowed, "as asked", "complete", [], [f"the citation does not resolve: {why}"], names_nothing=[NO_PLACE])
        columns = "select f.path, c.line, c.form, c.fenced, c.written, coalesce(c.path, f.path), c.lineage, c.key, c.unit from citations c join files f on f.sha = c.sha "
        rows = sorted(set(
            self.db.execute(columns + "where c.path = ?", (path,)).fetchall()
            + self.db.execute(columns + "where c.path > ? and c.path < ?", (path + "/", path + "0")).fetchall()
            + self.db.execute(columns + "where c.path is null and c.sha in (select sha from files where path = ?)", (path,)).fetchall()),
            key=lambda r: (r[0], r[1], r[4], r[2]))
        places, notes, related = [], [], []
        for host, line, form, fenced, written, target, tl, tk, unit in rows:
            if not self._within(host, narrowed):
                continue
            how = None
            if form == "bare":
                tl, tk = self._bare(target, tl)
                if tl is None:
                    continue
                written = target + " § " + tl + (f" [{tk}]" if tk else "")
            if target == path and tl == lineage and (tk or None) == key:
                how = "cites it"
            elif target == path and tl == lineage and key and not tk:
                how = "cites the section holding it"
            elif form == "label" and target == path and not lineage:
                how = "cites it"
            elif target == path and tl == lineage and key is None and tk:
                how = f"cites a part of it, `[{tk}]`"
            elif target == path and lineage and tl.startswith(lineage + " § "):
                how = "cites a section within it"
            elif target == path and lineage and tl and lineage.startswith(tl + " § "):
                how = "cites a section above it"
            elif target == path and lineage and not tl:
                how = "cites its file"
            elif target == path and not lineage and tl:
                how = "cites a section within it"
            elif target != path and target.startswith(path + "/"):
                how = "cites a file within it"
            if how is None:
                continue
            place = self._place(host, line)
            marks = [m for m in ("a `technical-specs` label, not a citation" if form == "label" else "",
                                 f"an annotation over the unit `{unit}`" if form == "annotation" and unit else ("an annotation" if form == "annotation" else "")) if m]
            if how == "cites it":
                places.append(place)
                if marks:
                    notes.append(f"{place}: {', '.join(marks)}")
            else:
                related.append(f"{place}: {how}{', ' + ', '.join(marks) if marks else ''}, as `{written}`")
        if why:
            notes.insert(0, f"the citation does not resolve: {why}")
        if related:
            notes.append("Related places, each told apart from the places citing it:")
            notes += related
        return Result("citers", citation, narrowed, "as asked", "complete", places, notes, names_nothing=[NO_PLACE] if why else [])

    # -- which sections are cited, and from where

    def cited_sections(self, narrowed=None):
        """-> every section, keyed part and file a place of the target cites, each with every place citing it: a place
        is a citing place of the target and says what it cites, the list ordered by what is cited, so what is cited is
        no place of the result. What it gives for one agrees with the places `citers` gives asked of that one alone."""
        narrowed = self._narrow(narrowed)
        return self._answer("cited sections", "every place cited", narrowed, lambda: self._cited_sections(narrowed))

    def _cited_sections(self, narrowed):
        rows = self.db.execute("select f.path, c.line, c.form, c.written, coalesce(c.path, f.path), c.lineage, c.key from citations c join files f on f.sha = c.sha").fetchall()
        found = set()
        for host, line, form, written, target, lineage, key in rows:
            if not self._within(host, narrowed):
                continue
            if form == "bare":
                lineage, key = self._bare(target, lineage)
                if lineage is None:
                    continue
            cited = target + (" § " + lineage if lineage else "") + (f" [{key}]" if key else "")
            found.add((cited, host, line))
        places = [f"{self._place(host, line)} cites `{cited}`" for cited, host, line in sorted(found)]
        run = ("every citation the target's files hold, each read to the section, the keyed part or the file it names, as written: a citation of a place that does not stand is listed as written, "
               "and a citation of a section within a section is listed under its own and not under the one above it")
        return Result("cited sections", "every place cited", narrowed, run, "complete", places)

    def _bare(self, path, rest):
        """-> (lineage, key) a citation written bare names: the longest heading path of the file it names that the rest
        of its line opens with, and the key standing in brackets right after it, or (None, None) where it opens with
        none."""
        if path not in self._lineages:
            self._lineages[path] = sorted((r[0] for r in self.db.execute(
                "select distinct h.lineage from known f join headings h on h.sha=f.sha where f.path=? and h.lineage != ''", (path,))), key=len, reverse=True)
        for lineage in self._lineages[path]:
            if rest == lineage or (rest.startswith(lineage) and not (rest[len(lineage)].isalnum() or rest[len(lineage):].startswith(" § "))):
                key = re.match(r" \[([^\]]*)\]", rest[len(lineage):])
                return lineage, ("; ".join(squeeze(p) for p in key.group(1).split(";")) if key else None)
        return None, None

    # -- which lines a citation names

    def lines(self, citation, narrowed=None):
        return self._answer("lines", citation, [], lambda: self._lines(citation))

    def _lines(self, citation):
        path, lineage, key, why = self._resolve(citation)
        if why:
            return Result("lines", citation, [], "as asked", "complete", [], [f"the citation does not resolve: {why}"], names_nothing=[NO_PLACE])
        if (self.root / path).is_dir():
            return Result("lines", citation, [], "as asked", "complete", [f"`{path}/`"], ["it names a folder, which holds no lines of its own"])
        heads = self.db.execute("select h.lineage, h.occurrence, h.level, h.line, h.own_end, h.subtree_end from files f join headings h on h.sha=f.sha "
                                "where f.path=? order by h.line", (path,)).fetchall()
        total = self.db.execute("select count(*) from files f join lines l on l.sha=f.sha where f.path=?", (path,)).fetchone()[0]
        if not heads:
            return Result("lines", citation, [], "as asked", "complete", [Place(path, "", None, 1, total, self._stands(path, 1, total))])
        # where two headings share the path, a citation of it names what both hold together: each one's lines are
        # given, a keyed part being the first of them to hold its key
        mine = [h for h in heads if h[0] == lineage]
        head, notes = mine[0], []
        if len(mine) > 1:
            notes.append(self._shared(path, lineage))
        cite = f"`{path}{' § ' + lineage if lineage else ''}`"
        places = []
        if key:
            head, span = next(((h, found) for h in mine for found in [self._part(path, h, key)] if found), (head, None))
            if not span:
                return Result("lines", citation, [], "as asked", "complete", [], [f"the citation does not resolve: {cite} holds no part `[{key}]`"], names_nothing=[NO_PLACE])
            places.append(Place(path, lineage, key, span[0], span[1], self._stands(path, span[0], span[1])))
            notes.append(f"{cite} lines {head[3]}-{head[5] - 1}: the section holding the part")
        else:
            for h in mine:
                places.append(Place(path, lineage, None, h[3], h[4] - 1, self._stands(path, h[3], h[4] - 1)))
                if lineage and h[5] != h[4]:
                    notes.append(f"{cite} lines {h[3]}-{h[5] - 1}: its whole subtree")
        segments = lineage.split(" § ") if lineage else []
        for depth in range(len(segments) - 1, -1, -1):
            above = " § ".join(segments[:depth])
            h = next((x for x in heads if x[0] == above), None)
            if h is None:
                continue
            label = f"`{path}{' § ' + above if above else ''}`"
            if depth == len(segments) - 1 and above:
                notes.append(f"{label} lines {h[3]}-{h[5] - 1}: its parent whole")
            if h[4] > h[3]:
                notes.append(f"{label} lines {h[3]}-{h[4] - 1}: " + ("its file's text before its first section" if not above else "an ancestor's text before its first child heading"))
        return Result("lines", citation, [], "as asked", "complete", places, notes)

    def _part(self, path, head, key):
        """-> (first line, last line) of the keyed part a citation names within a section: a record, by its
        identifying fields, or a table's row, by the columns its key names."""
        return find_part(self._rows(path, head[3], head[5]), key)

    # -- where a term is used

    def other_names(self, term):
        """-> the other names the glossary gives a term: its abbreviation and each name its entry is also called."""
        rows = self.db.execute("select l.text from known f join lines l on l.sha=f.sha where f.path='specs/methodology/glossary/glossary.md' and l.text like '|%'").fetchall()
        wanted = squeeze(term).lower()
        for (text,) in rows:
            cells = [squeeze(c) for c in strip_links(text).strip().strip("|").split("|")]
            if len(cells) < 3 or cells[0] in ("Term", "") or set(cells[0]) <= set("-: "):
                continue
            names = [cells[0]] + ([cells[1]] if cells[1] else [])
            also = re.search(r"Also called ([^.]*)\.", cells[2])
            names += [squeeze(n) for n in also.group(1).split(",")] if also else []
            if wanted in [n.lower() for n in names]:
                return [n for n in names if n.lower() != wanted]
        return []

    def terms(self, term, narrowed=None, exact=False):
        """-> every place using a word, a phrase or an identifier, in every form it takes and under every other name the
        glossary gives it: where a form's words stand together, and, unless asked for exact, each sentence of prose
        holding a form's words in their order with other words between, marked `words apart`."""
        narrowed = self._narrow(narrowed)
        return self._answer("terms", term, narrowed, lambda: self._terms_used(term, narrowed, exact), exact)

    def _terms_used(self, term, narrowed, exact=False):
        forms = [squeeze(term)] + self.other_names(term)
        found = {}
        for form in forms:
            query = phrase(form)
            if not query:
                continue
            alone = set(self.db.execute("select f.path, t.n from terms t join files f on f.sha = t.sha where terms match ?", (query,)))
            # a phrase standing only where a line is read with the line after it is broken across the two
            broken = {(path, n) for path, n in self.db.execute("select f.path, t.n from term_pairs t join files f on f.sha = t.sha where term_pairs match ?", (query,))
                      if (path, n) not in alone and (path, n + 1) not in alone}
            for path, n in alone | broken:
                if self._within(path, narrowed) and (exact or self._together_in_prose(path, n, form, (path, n) in broken)):
                    found.setdefault((path, n), form)
        places = [self._place(path, n) for path, n in sorted(found)]
        if not exact:
            apart = self._words_apart(forms, narrowed)
            places = sorted(places + [self._place(path, first, last).marked_apart() for path, first, last in apart], key=lambda p: (p.path, p.first, p.apart))
        run = ("each form searched as a phrase, every word reduced to its stem and every identifier split into its words: "
               + ", ".join(f"`{f}`" for f in forms) + (". The glossary gives the term no other name" if len(forms) == 1 else ". The names after the first are the glossary's other names for it")
               + (". Asked for exact, only where a form's words stand together" if exact else
                  ". A form written as more than one word is found too where those words stand in their order within one sentence of prose with other words between them, "
                  "each such place marked `words apart`; an identifier written as one word keeps its words together"))
        result = Result("terms", term, narrowed, run, "complete", places, exact=exact)
        if not phrase(squeeze(term)):
            result.notes.append("the term reduces to no word, so the search asked of nothing by it")
            result.names_nothing.append(NO_WORD)
        return result

    # -- which places match a pattern

    def _prose(self, path):
        """-> [(first line, last line, sentence)] of each sentence of prose a file of the target holds, read once for each
        content in a search, as `prose_sentences` reads them."""
        row = self.db.execute("select f.sha, c.kind, c.language from files f join contents c on c.sha = f.sha where f.path=?", (path,)).fetchone()
        if not row:
            return []
        held = self.__dict__.setdefault("_prose_of", {})
        if row[0] not in held:
            text = "\n".join(r[0] for r in self.db.execute("select text from lines where sha=? order by n", (row[0],)))
            held[row[0]] = prose_sentences(text, row[1], row[2])
        return held[row[0]]

    def _together_in_prose(self, path, n, form, broken=False):
        """Whether a place where the index finds a form's words together holds them together within one sentence: on
        line n alone, or, broken, across line n and the line after it. A form of one word always does, and so do lines
        no sentence of prose covers, since words outside prose, in code or in a heading, are found together alone. Lines
        of prose do only where a sentence covering them holds the form's words together, or, on one line, where the
        line's text outside the sentences standing on it alone, code before a comment, holds them: so words standing
        in two sentences, two cells, two rows or two fields are never found together."""
        wanted = stems(form)
        if len(wanted) < 2:
            return True
        last_line = n + 1 if broken else n
        covering = [(first, last, s) for first, last, s in self._prose(path) if first <= last_line and last >= n]
        if not covering or any(together_in(stems(s), wanted) for _, _, s in covering):
            return True
        if broken:
            return False
        rest = self._line(path, n)
        for first, last, s in covering:
            if first == last == n:
                rest = rest.replace(s, " ")
        return together_in(stems(rest), wanted)

    def _line(self, path, n):
        """-> the text of a file's line n, counted from 1, as the index holds it."""
        row = self.db.execute("select l.text from lines l join files f on f.sha = l.sha where f.path=? and l.n=?", (path, n)).fetchone()
        return row[0] if row else ""

    def _words_apart(self, forms, narrowed):
        """-> {(path, first line, last line)} of each sentence of prose holding a form's words in their order with other
        words between them and holding them nowhere together. Each word of a form as its searcher wrote it, apart from
        the next by white space, is one group of stems: an identifier the index splits into several words, `TypeScript`
        or `append_entry`, stays one group, so only the words a searcher wrote apart may stand apart. A file is read
        only where it holds every word of the form somewhere."""
        apart = set()
        for form in forms:
            groups = [g for g in (stems(word) for word in form.split()) if g]
            if len(groups) < 2:
                continue
            holding = None
            for word in set(re.findall(r"[^\W_]+", normalize(form))):
                shas = {r[0] for r in self.db.execute("select sha from terms where terms match ?", (f'"{word}"',))}
                holding = shas if holding is None else holding & shas
                if not holding:
                    break
            for path, in self.db.execute("select path from files where sha in (%s) order by path" % ",".join("?" * len(holding or ())), tuple(holding or ())) if holding else []:
                if not self._within(path, narrowed):
                    continue
                for first, last, sentence in self._prose(path):
                    if words_apart(sentence, groups):
                        apart.add((path, first, last))
        return apart

    def pattern(self, expression, narrowed=None):
        narrowed = self._narrow(narrowed)
        regex = re.compile(expression, re.M)   # a pattern that is no regular expression is refused before anything is read
        return self._answer("pattern", expression, narrowed, lambda: self._pattern(expression, regex, narrowed))

    def _pattern(self, expression, regex, narrowed):
        places = []
        for path, sha in self.db.execute("select path, sha from files order by path").fetchall():
            if not self._within(path, narrowed):
                continue
            lines = [r[0] for r in self.db.execute("select text from lines where sha=? order by n", (sha,))]
            if not lines:
                continue
            text, starts, at = "\n".join(lines), [], 0
            for line in lines:
                starts.append(at)
                at += len(line) + 1
            seen = set()
            for m in regex.finditer(text):
                first = max(i for i, s in enumerate(starts) if s <= m.start()) + 1
                last = max(i for i, s in enumerate(starts) if s <= max(m.start(), m.end() - 1)) + 1
                if (first, last) not in seen:
                    seen.add((first, last))
                    places.append(self._place(path, first, last))
        return Result("pattern", expression, narrowed, "as asked, in Python's `re` syntax with `^` and `$` matching at each line, over each file's whole text. A pattern is for a flaw in formatting or structure: a term, a citer or a structure has a search of its own",
                      "complete", places)

    # -- which units of code hold a structure

    def code_structure(self, structure, name, narrowed=None):
        narrowed = self._narrow(narrowed)
        if structure not in STRUCTURES:
            raise ValueError(f"no structure `{structure}`: a structure is one of {', '.join(STRUCTURES)}")
        return self._answer("code structure", f"{structure} {name}", narrowed, lambda: self._code_structure(structure, name, narrowed))

    def _code_structure(self, structure, name, narrowed):
        places, notes = [], []
        if structure == "annotated-with":
            rows = self.db.execute("select f.path, c.line, c.unit, c.written from citations c join files f on f.sha=c.sha where c.form='annotation' and c.fenced=0 "
                                   "and c.written like ? order by f.path, c.line", ("%" + name + "%",)).fetchall()
            for path, line, unit, written in rows:
                if self._within(path, narrowed):
                    places.append(self._place(path, line))
                    notes.append(f"`{path}` line {line}: the unit `{unit}`, annotated with `{written}`")
        else:
            wanted = [structure] + (["calls"] if structure == "constructs" else [])
            classes = {r[0] for r in self.db.execute("select distinct s.name from structures s join units u on u.sha=s.sha and u.name=s.unit "
                                                     "where s.structure='defines' and u.kind in ('class','struct','record')")}
            rows = self.db.execute(f"select f.path, s.line, s.unit, s.structure, c.language from structures s join files f on f.sha=s.sha join contents c on c.sha=s.sha "
                                   f"where s.name=? and s.structure in ({','.join('?' * len(wanted))}) order by f.path, s.line, s.unit", [name] + wanted).fetchall()
            seen = set()
            for path, line, unit, found, language in rows:
                if not self._within(path, narrowed) or (path, line, unit) in seen:
                    continue
                if structure == "constructs" and found == "calls" and not (name in classes or (language == "python" and name[:1].isupper())):
                    continue
                seen.add((path, line, unit))
                places.append(self._place(path, line))
                notes.append(f"`{path}` line {line}: the unit `{unit}`")
            if structure in ("extends", "implements") and any(r[4] == "c_sharp" for r in rows):
                notes.append("C#'s syntax does not tell a class extended from an interface implemented, so each name in a type's base list is listed for both.")
        blind = self.db.execute("select f.path, c.note from files f join contents c on c.sha=f.sha where c.kind='code' and c.note != '' order by f.path").fetchall()
        blind = [(p, n) for p, n in blind if self._within(p, narrowed)]
        if blind:
            notes.append("Files no structure was searched in, or not wholly:")
            notes += [f"`{p}`: {n}" for p, n in blind]
        run = "as asked, matched on the name as the code writes it, in no comment and no string. The answer holds what the syntax shows, and is blind to a call made by reflection or by a name built as the code runs"
        return Result("code structure", f"{structure} {name}", narrowed, run, "complete", places, notes)

    # -- which places say the same as a passage

    def meaning(self, passage, narrowed=None, limit=None, start=None):
        """-> a part of the ranking of the places saying the same as a passage, or as the section a citation names:
        `limit` places from the place `start`, the first RANKED where neither is given. What was asked is ranked
        against every passage and against every sentence of a passage holding several, by its words and by the
        model's vectors, and so is each sentence of what was asked, weighed less, so a rule restated in one sentence
        of a longer passage is ranked by that sentence. The place given is the passage a sentence stands in.

        Asked by a citation, the search gives others and not the one it was given: the ranking holds neither that
        section nor a place whose section cites it, and those places are listed apart, whole, with every part. Asked
        by a passage, it sets no place apart, and its caller leaves out by their citations the places it does not want.
        What it ranks is a section's prose: no line of a fenced block, no heading, no front matter, and no passage or
        sentence shorter than SENTENCE.

        Parts asked one after another make up one ranking while the files stand: the first places are fused from each
        ranking's first CANDIDATES, and a part further on reads each ranking further without reordering what an
        earlier reading gave (TIERS)."""
        limit, start = RANKED if limit is None else limit, 1 if start is None else start
        if limit < 1 or start < 1:
            raise ValueError("a ranking's limit and its start are each a whole number from 1")
        asked, own, citing = squeeze(passage.strip("`")) if passage.strip().startswith("`") else squeeze(passage), None, set()
        if is_question(asked):
            raise ValueError(QUESTION_TURNED_BACK)
        narrowed = self._narrow(narrowed)
        self._embed_missing()
        texts = [asked]

        def nothing(note, names=()):
            return self._finish(Result("meaning", passage, narrowed, "as asked", "ranked", [], [note], part=(start, 0), names_nothing=names))

        if parse_citation(asked) and parse_citation(asked)[0]:
            path, lineage, key, why = self._resolve(asked, "known")
            if why:
                return nothing(f"the citation does not resolve: {why}", [NO_PLACE])
            own = (path, lineage)
            texts = [r[0] for r in self.db.execute("select p.text from passages p join known f on f.sha=p.sha where f.path=? and p.lineage=? order by p.line_start", (path, lineage))]
            if not texts:
                return nothing("the place it names holds no passage of prose to compare")
            citing = {(p.path, p.lineage) for p in self._citing(f"{own[0]}{' § ' + own[1] if own[1] else ''}").places}
        units = [[text] + sentences(text) for text in texts]
        vectors = iter(self._vectors([u for group in units for u in group]))
        units = [[(u, next(vectors)) for u in group] for group in units]
        stands, passage_of = {}, {}

        def where(pid):
            """-> the file and the section a passage stands in, or None where it stands in no file of the target or
            outside what the search is narrowed to."""
            if pid not in stands:
                at = self.db.execute("select f.path, p.lineage from passages p join files f on f.sha=p.sha where p.id=? order by f.path limit 1", (pid,)).fetchone()
                stands[pid] = tuple(at) if at and self._within(at[0], narrowed) else None
            return stands[pid]

        def holding(sids):
            """-> the passages a ranking of sentences stands in, each once, at its best sentence's place."""
            for sid in sids:
                if sid not in passage_of:
                    passage_of[sid] = self.db.execute("select pid from sentences where id=?", (sid,)).fetchone()[0]
            return list(dict.fromkeys(passage_of[sid] for sid in sids))

        def rankings(text, vector):
            """-> the rankings of the passages against one text: by its words and by its vector, each against every
            passage and against every sentence. Each takes how many rows to read and gives the rows it read and the
            passages they rank."""
            words = re.findall(r"[^\W_]+", normalize(text))
            query = " OR ".join('"' + w + '"' for w in dict.fromkeys(words))

            def passage_terms(pool):
                rows = [r[0] for r in self.db.execute("select pid from passage_terms where passage_terms match ? order by bm25(passage_terms) limit ?", (query, pool))] if words else []
                return len(rows), rows

            def passage_vectors(pool):
                rows = [r[0] for r in self.db.execute("select rowid from passage_vectors where embedding match ? and k = ? order by distance", (vector, pool))]
                return len(rows), rows

            def sentence_terms(pool):
                rows = [r[0] for r in self.db.execute("select pid from sentence_terms where sentence_terms match ? order by bm25(sentence_terms) limit ?", (query, pool))] if words else []
                return len(rows), list(dict.fromkeys(rows))

            def sentence_vectors(pool):
                rows = [r[0] for r in self.db.execute("select rowid from sentence_vectors where embedding match ? and k = ? order by distance", (vector, pool))]
                return len(rows), holding(rows)

            return passage_terms, passage_vectors, sentence_terms, sentence_vectors

        def candidates(fetch, depth):
            """-> the first `depth` passages of a ranking that stand in the target's files, within what the search is
            narrowed to, and whether the ranking held more. The index holds the passages of each target reading its
            kind of durable file, and of no file of the other kind, so more of the ranking is read until that many of
            the target's own are found or the ranking ends."""
            pool = min(depth * 4, DEEPEST)
            while True:
                read, ranking = fetch(pool)
                kept = []
                for pid in ranking:
                    if where(pid) is None or where(pid) == own:
                        continue
                    kept.append(pid)
                    if len(kept) == depth:
                        return kept, True
                if read < pool or pool >= DEEPEST:
                    return kept, False
                pool = min(pool * 4, DEEPEST)

        def fused(depth):
            """-> the places in the order the rankings read to `depth` fuse to, and whether any ranking held more."""
            scores, more = {}, False

            def add(ranking, weight):
                for rank, pid in enumerate(ranking, 1):
                    scores[pid] = scores.get(pid, 0.0) + weight / (FUSION + rank)

            for group in units:
                for fetch in rankings(*group[0]):
                    ranking, held = candidates(fetch, depth)
                    more = more or held
                    add(ranking, 1.0)
                # each kind of ranking by the sentences of what was asked is one ranking, a passage standing at the
                # best place any sentence gives it
                for kind in range(4) if len(group) > 1 else ():
                    best = {}
                    for unit in group[1:]:
                        ranking, held = candidates(rankings(*unit)[kind], depth)
                        more = more or held
                        for rank, pid in enumerate(ranking):
                            best[pid] = min(best.get(pid, rank), rank)
                    add(sorted(best, key=lambda p: (best[p], p)), SENTENCES)
            order, seen = [], set()
            for pid in sorted(scores, key=lambda p: (-scores[p], p)):
                for path, first, last in self.db.execute("select f.path, p.line_start, p.line_end from passages p join files f on f.sha=p.sha where p.id=? order by f.path", (pid,)):
                    place = self._place(path, first, last)
                    if place not in seen and self._within(path, narrowed):
                        seen.add(place)
                        order.append(place)
            return order, more

        ranking, given, alike = [], set(), None
        for depth, upto in TIERS:
            order, more = fused(depth)
            alike = order if alike is None else alike
            for place in order:
                if upto is not None and len(ranking) >= upto:
                    break
                if place not in given and (place.path, place.lineage) not in citing:
                    given.add(place)
                    ranking.append(place)
            if len(ranking) >= start - 1 + limit or not more:
                break
        places, notes = ranking[start - 1:start - 1 + limit], []
        if citing:
            # the places listed apart are every passage of a section citing the one asked with, the same whatever part
            # is asked for: those most alike first, in the order the first reading ranks them, then the rest
            apart = [p for p in alike if (p.path, p.lineage) in citing]
            held = set(apart)
            for path, lineage in sorted(citing):
                for first, last in self.db.execute("select p.line_start, p.line_end from passages p join files f on f.sha=p.sha where f.path=? and p.lineage=? order by p.line_start", (path, lineage)).fetchall():
                    place = self._place(path, first, last)
                    if place not in held and self._within(path, narrowed):
                        held.add(place)
                        apart.append(place)
            if apart:
                notes.append("Places whose section cites the passage's own, listed apart, since each may rely on it and not restate it:")
                notes += apart
        run = (f"what was asked, and each sentence of it, ranked against every passage and every sentence of a passage by its words and by the vectors of the model `{MODEL}`, "
               f"run on this machine, the rankings fused, and {limit} place{'' if limit == 1 else 's'} given from place {start} of the ranking")
        self.computed += 1
        result = Result("meaning", passage, narrowed, run, "ranked", places, notes, part=(start, len(places)))
        if own is None and not re.findall(r"[^\W_]+", normalize(asked)):
            result.notes.append("the passage reduces to no word, so nothing of it was ranked by its words")
            result.names_nothing.append(NO_WORD)
        self._nothing_under(result, narrowed)
        return self._finish(result)


def snapshot(root, target=CURRENT_OPERATIVE, paths=None, commit=None, cover=None, scratch=None):
    """-> the snapshot code of the files of a target as they stand, fresh: the files are walked, a file whose size or
    time of change moved is read again, as the index is brought up to date today, and the code is built from the path
    and the content of each file, in the order of their paths. One code for the whole target, whatever paths a search
    is narrowed to; for the working files, the code of the paths named. The code is built one way whatever the target,
    so the files a commit held and the files as they stand take one code where each file holds the same. Nothing is
    kept running between calls."""
    search = Search(root, cover=cover, scratch=scratch, quiet=True, target=target, commit=commit, paths=paths if target == WORKING else None)
    try:
        return search.snapshot_code()
    finally:
        search.db.close()


# ---------------------------------------------------------------------------------------------------------------------
# The entry script's actions

def files_worked_over():
    """-> the folder holding the files a search naming no project works over: the nearest folder at or above the
    working directory that holds the search's own skill, as the project root and each copy of the project's files do,
    whichever holds the script being run. It is told from the files. Where the working directory lies in no such
    folder, the search answers over the one its own script stands in."""
    here = Path.cwd().resolve()
    return next((p for p in (here, *here.parents) if (p / ".ai" / "skills" / SKILL).is_dir()), Path(__file__).resolve().parents[3])


class Asked:
    """What one run of the entry script asked: the project, the values its action takes, the paths it is narrowed to,
    the target and the commit it names, and the part of a ranking it asks for."""

    def __init__(self, root, values, narrowed, target, commit, part, exact=False):
        self.root, self.values, self.narrowed, self.target, self.commit, self.part = root, values, narrowed, target, commit, part
        self.exact = exact

    def search(self):
        """-> the search over the project and the target asked for, the operative files as they stand where none is
        named, its index brought up to date."""
        return Search(self.root, target=self.target or CURRENT_OPERATIVE, commit=self.commit, paths=self.narrowed if self.target == WORKING else None)


def stopping(action):
    """-> an action that stops with its reason in place of an answer: with the exit code 1 where something the search
    requires is missing or a commit's files cannot be searched, and 2 where it was asked what the search refuses."""
    def run(asked):
        try:
            return action(asked)
        except (MissingRequirements, CannotSearch) as e:
            print(e)
            return 1
        except (ValueError, re.error) as e:
            print(f"{SKILL}: {e}")
            return 2
    return run


def _places(asked, ask):
    """-> 0, one search run: its result's file, its count and its places where they are few printed, with each thing
    the question named nothing by and each note of a short result."""
    search = asked.search()
    result = ask(search)
    search.db.close()
    print(result.summary(asked.root))
    for nothing in result.names_nothing:
        print("  the question names nothing to ask of: " + nothing)
    for note in result.notes[:FEW] if len(result.places) <= FEW else []:
        print("  note: " + note)
    return 0


@stopping
def run_show_citers(asked):
    return _places(asked, lambda search: search.citers(asked.values[0], asked.narrowed))


@stopping
def run_show_cited_sections(asked):
    return _places(asked, lambda search: search.cited_sections(asked.narrowed))


@stopping
def run_show_lines(asked):
    return _places(asked, lambda search: search.lines(asked.values[0], asked.narrowed))


@stopping
def run_show_term_uses(asked):
    return _places(asked, lambda search: search.terms(asked.values[0], asked.narrowed, exact=asked.exact))


@stopping
def run_show_code_structure(asked):
    return _places(asked, lambda search: search.code_structure(asked.values[0], asked.values[1], asked.narrowed))


@stopping
def run_show_similar_passages(asked):
    return _places(asked, lambda search: search.meaning(asked.values[0], asked.narrowed, **asked.part))


@stopping
def run_show_pattern_matches(asked):
    return _places(asked, lambda search: search.pattern(asked.values[0], asked.narrowed))


@stopping
def run_show_snapshot_code(asked):
    search = asked.search()
    code = search.snapshot_code()
    search.db.close()
    print(code)
    print(f"the snapshot code of `{search.target}`" + (f" under {', '.join('`' + p + '`' for p in search.paths)}" if search.target == WORKING else "")
          + (f" at the commit {search.commit}" if search.target in OF_A_COMMIT else "") + ", as its files now stand")
    return 0


def run_check_requirements(asked):
    text, count = requirements_report(asked.root)
    print(text)
    return 1 if count else 0


def run_check_result(asked):
    if not Path(asked.values[0]).is_file():
        print(f"{SKILL}: no file {asked.values[0]}")
        return 2
    problems = Result.check(asked.values[0])
    print("\n".join(problems) if problems else f"{Path(asked.values[0]).name}: a search's result in its form, its content as the search wrote it")
    return 1 if problems else 0


@stopping
def run_install_model(asked):
    print(f"{SKILL}: the model's files are in {install_model(asked.root).as_posix()}, where every search of the project finds them")
    return 0


# The script's actions, stated once: each action's flag, the values it takes, the unit that runs it and what it gives.
# `main` runs an action from this tuple and the usage is written from it, so the actions are read from here alone.
FLAGS = (
    ("--show-citers", "CITATION", run_show_citers, "every place citing a section, a keyed part or a file"),
    ("--show-cited-sections", "", run_show_cited_sections, "each section, keyed part and file cited, with every place citing it"),
    ("--show-lines", "CITATION", run_show_lines, "the lines a citation names"),
    ("--show-term-uses", "TERM", run_show_term_uses, "every place using a word, a phrase or an identifier, in every form it takes"),
    ("--show-code-structure", "STRUCTURE NAME", run_show_code_structure, "every unit of code holding a structure: " + ", ".join(STRUCTURES)),
    ("--show-similar-passages", "PASSAGE", run_show_similar_passages, "the places stating the same as a passage, or as a cited section, in other words"),
    ("--show-pattern-matches", "EXPRESSION", run_show_pattern_matches, "every place a regular expression matches, for a flaw in formatting or structure"),
    ("--show-snapshot-code", "", run_show_snapshot_code, "the present snapshot code of a target's files, read fresh"),
    ("--check-requirements", "", run_check_requirements, "what the search requires, and whether each is present"),
    ("--check-result", "FILE", run_check_result, "whether a result's file is in its form and its content is as the search wrote it"),
    ("--install-model", "", run_install_model, "download the model's files, the one action that reaches the network"),
)
# what an action may be given beside its values: each option's flag, the value it takes and what it sets
OPTIONS = (
    ("--target", "TARGET", "the files to answer over, one of:"),
    ("--commit", "COMMIT", f"the commit a search of {COMMITTED_OPERATIVE} or of {COMMITTED_FIXTURE} answers for, the last where none is named"),
    ("--limit", "N", f"how many places of its ranking --show-similar-passages gives, {RANKED} where none is named"),
    ("--start", "N", "the place of its ranking it gives them from, the first where none is named"),
    ("--paths", "PATH ...", f"answer over these files and folders alone, which a search of {WORKING} requires"),
    ("--exact", "", "--show-term-uses gives only where a phrase's words stand together, and no sentence holding them apart"),
)
COVERS = (
    (CURRENT_OPERATIVE, "the operative files as they stand, where none is named"),
    (COMMITTED_OPERATIVE, "the operative files as a commit held them"),
    (CURRENT_FIXTURE, "the fixture files as they stand"),
    (COMMITTED_FIXTURE, "the fixture files as a commit held them"),
    (WORKING, "the working files under the paths given"),
)


def usage():
    """-> the script's usage, written from its actions, its options and its targets as they are stated."""
    def row(flag, metavar, text):
        return f"  {(flag + ' ' + metavar).strip():<39}{text}"

    widest = max(len(target) for target, _ in COVERS)
    out = [f"usage: {SKILL}.py ACTION " + " ".join(f"[{(flag + ' ' + metavar).strip()}]" for flag, metavar, _ in OPTIONS), "",
           "Each action answers one question over the files of Spec of Record's scope and the code, and writes its result as a",
           f"file under {SCRATCH}/results/. Every search first checks everything the search requires.", ""]
    out += [row(flag, metavar, text) for flag, metavar, _, text in FLAGS] + [""]
    for flag, metavar, text in OPTIONS:
        out.append(row(flag, metavar, text))
        if flag == "--target":
            out += [" " * 43 + f"{target:<{widest + 2}}{covers}" for target, covers in COVERS]
    return "\n".join(out) + "\n"


USAGE = usage()


def main(argv, root=None):
    root = Path(root).resolve() if root else files_worked_over()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = list(argv[1:])
    narrowed = []
    if "--paths" in args:
        at = args.index("--paths")
        narrowed = [a for a in args[at + 1:] if not a.startswith("--")]
        del args[at:at + 1 + len(narrowed)]
        if not narrowed:
            print(USAGE)
            return 2
    # asking for exact is a search by terms' alone, and takes no value
    exact = "--exact" in args
    if exact:
        args.remove("--exact")
        if "--show-term-uses" not in args:
            print(USAGE)
            return 2
    given = {}
    for flag in [flag for flag, metavar, _ in OPTIONS if flag != "--paths" and metavar]:
        if flag in args:
            at = args.index(flag)
            if at + 1 >= len(args) or args[at + 1].startswith("--"):
                print(USAGE)
                return 2
            given[flag] = args[at + 1]
            del args[at:at + 2]
    part = {}
    for flag in ("--limit", "--start"):
        # a part is asked of a ranking alone, and by a whole number from 1
        if flag in given and (not given[flag].isdigit() or int(given[flag]) < 1 or "--show-similar-passages" not in args):
            print(USAGE)
            return 2
        if flag in given:
            part[flag[2:]] = int(given[flag])
    # an action takes as many values as its statement names, and nothing else
    actions = {flag: (len(metavar.split()), run) for flag, metavar, run, _ in FLAGS}
    if not args or args[0] not in actions or len(args) != 1 + actions[args[0]][0]:
        print(USAGE)
        return 2
    return actions[args[0]][1](Asked(root, args[1:], narrowed, given.get("--target"), given.get("--commit"), part, exact))
