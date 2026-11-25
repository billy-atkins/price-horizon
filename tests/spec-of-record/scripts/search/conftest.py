"""The search's set of kept tests: which files are the search's, and what the set's files share.

A test drives the search's entry script as a process of its own (`script`), or, where no action reaches what it
tests, the shared code itself (`search`, `reading`, `opened`). Each project a test searches is one it writes from its
fixtures into its own folder, and what the tests of one file share is built once in that file's own folder within the
run's folder (`shared`). The search writes in two places: the scratch space a search is given, or, given none, the
one under the project it searches, and so always within the run's folder; and the model's files, which stand where
the search installs them once on a machine and are no run's output.
"""
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

# The files of the script these tests are of, the search: its code, and each file of the canon it reads a form from
# as it runs. A path ending in a slash names each file beneath it.
SCRIPT_FILES = (".ai/skills/lib/search.py", ".ai/skills/lib/reading.py", ".ai/skills/lib/spec_text.py", ".ai/skills/lib/citation_links.py",
                ".ai/skills/lib/code_checks.py", ".ai/skills/lib/constructs.py", ".ai/skills/lib/expressions.py",
                ".ai/skills/search-spec-of-record-scope/scripts/")
FORM_FILES = ("specs/methodology/glossary/glossary.md", "specs/methodology/skills/registered-skills.md")
ACTIONS_IN = ".ai/skills/lib/search.py"

CHECKOUT = Path(__file__).resolve().parents[4]
LIB = CHECKOUT / ".ai" / "skills" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
import reading as the_reading  # noqa: E402
import search as the_search  # noqa: E402
import spec_text  # noqa: E402

ENTRY = CHECKOUT / ".ai" / "skills" / the_search.SKILL / "scripts" / (the_search.SKILL + ".py")
SKILL_FOLDER = Path(".ai") / "skills" / the_search.SKILL

# where each fixture of a project stands in it: the corpus of forms, the small project about a heron, and the
# invented library, whose files cite each other by these paths
CORPUS = {"forms-spec": "specs/forms.md", "target-spec": "specs/target.md", "promise-product-file": "product/promise.md",
          "ledger-glossary": "specs/methodology/glossary/glossary.md", "ledger-python": "code/sample.py", "ledger-typescript": "code/sample.ts",
          "ledger-csharp": "code/sample.cs", "ledger-table-sql": "code/schema.sql", "ledger-settings-yaml": "code/settings.yaml"}
HERON = {"heron-spec": "specs/target.md", "stack-naming-one-code-root": the_search.code_checks.STACK, "heron-function": "code/sample.py",
         "egret-function": "src/other.py", "design-citing-the-heron": ".ai/plans/design-specs/a-design.md",
         "plan-citing-the-heron": ".ai/plans/other-plan.md", "follow-ups-naming-a-heron": ".ai/follow-ups.md"}
LIBRARY = {"library-" + name: "specs/library/%s.md" % name
           for name in ("membership", "loans", "overdue", "holds", "catalogue", "donations", "opening", "volunteers", "rooms", "events")}


def files_under(root):
    return sorted(p.relative_to(root).as_posix() for p in Path(root).rglob("*") if p.is_file())


def lines_of(places):
    """-> {(path, first line)} of a result's places."""
    return {(place.path, place.first) for place in places}


def paths_of(result):
    return sorted({p.path for p in result.places})


def line_holding(root, path, words):
    for n, line in enumerate((Path(root) / path).read_text(encoding="utf-8").split("\n"), 1):
        if words in line:
            return n
    raise AssertionError("%s holds no line with: %s" % (path, words))


def put(root, rel, text):
    f = Path(root) / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8", newline="\n")


def written(root, fixtures, places, under=""):
    """Write each fixture of a project where it stands in it -> the project's root."""
    for key, rel in places.items():
        put(root, under + rel, fixtures[key])
    return Path(root)


def a_corpus(root, fixtures):
    """The corpus of forms: two specs, a product file, a glossary and code in five languages."""
    return written(root, fixtures, CORPUS)


def a_project(root, fixtures):
    """A small project: a spec, a stack naming `code` as its code root, code in two folders, working files, and the
    folder of the search's skill, by which a run of the entry script within the project takes it for its checkout."""
    (Path(root) / SKILL_FOLDER).mkdir(parents=True, exist_ok=True)
    return written(root, fixtures, HERON)


def a_library(root, fixtures, under=""):
    """The invented library's ten files, each at the path its citations name it by."""
    return written(root, fixtures, LIBRARY, under)


def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=search-tests", "-c", "user.email=search-tests@example.invalid", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"] + list(args),
                          cwd=root, capture_output=True, text=True)
    if done.returncode:
        raise AssertionError("git %s: %s" % (" ".join(args), done.stderr))
    return done.stdout.strip()


def changed(path, was, now):
    """-> the problems the check of a result's form reports of a copy of a result with one thing changed."""
    copy = path.with_name("changed-" + path.name)
    copy.write_text(path.read_text(encoding="utf-8").replace(was, now), encoding="utf-8", newline="\n")
    try:
        return the_search.Result.check(copy)
    finally:
        copy.unlink()


def same_answer(one, other):
    """-> whether two results hold the same answer: the same record but its name, each place the same place."""
    def places(r):
        return [(str(p),) + tuple(getattr(p, name, None) for name in ("path", "first", "last", "lineage", "key", "stands")) for p in r.places]
    return one.body() == other.body() and places(one) == places(other) and one.notes == other.notes and one.names_nothing == other.names_nothing


def moved_in_time(path):
    """Move a file's time of change and leave what it holds."""
    held = path.stat()
    os.utime(path, ns=(held.st_atime_ns + 5_000_000_000, held.st_mtime_ns + 5_000_000_000))


def run_script(root, *args, env=None, cwd=None):
    """-> (the exit code, what was printed) of the search's entry script, run as a process of its own in a project
    that holds the skill's folder, so the project is the checkout the run answers over and writes in."""
    root = Path(root)
    if not (root / SKILL_FOLDER).is_dir():
        raise AssertionError("%s holds no %s, so a run of the entry script there would answer over another checkout" % (root, SKILL_FOLDER.as_posix()))
    done = subprocess.run([sys.executable, "-B", str(ENTRY)] + [str(a) for a in args], cwd=cwd or root, capture_output=True, env=dict(os.environ, **(env or {})))
    return done.returncode, (done.stdout + done.stderr).decode("utf-8", "replace").replace("\r\n", "\n")


@pytest.fixture(scope="session")
def search():
    """The search's shared code, for what no action of the entry script reaches."""
    return the_search


@pytest.fixture(scope="session")
def reading():
    """The one reading the search reads a file by."""
    return the_reading


@pytest.fixture(scope="session")
def tools():
    """What the set's files share in writing a project and reading a result."""
    return types.SimpleNamespace(files_under=files_under, lines_of=lines_of, paths_of=paths_of, line_holding=line_holding, put=put, a_corpus=a_corpus,
                                 a_project=a_project, a_library=a_library, git=git, changed=changed, same_answer=same_answer, moved_in_time=moved_in_time,
                                 CORPUS=CORPUS, HERON=HERON, LIBRARY=LIBRARY, SKILL_FOLDER=SKILL_FOLDER, ENTRY=ENTRY)


@pytest.fixture(scope="session")
def script():
    """-> script(root, *args, env=None, cwd=None): the entry script run as a process over a project."""
    return run_script


class Opened:
    """The searches a test or a file's shared fixture opened, each index closed as the test or the file ends, so the
    clean-up that follows finds no file held open."""

    def __init__(self):
        self.held = []

    def __call__(self, root, **given):
        given.setdefault("quiet", True)
        found = the_search.Search(root, **given)
        self.held.append(found)
        return found

    def close(self):
        for found in self.held:
            found.db.close()
        self.held = []


@pytest.fixture
def opened(work):
    """-> opened(root, **given): a search over a project, its index closed as the test ends, before its folder is cleared."""
    held = Opened()
    yield held
    held.close()


class Shared:
    """What the tests of one file share: a folder of the file's own within the run's folder, and each thing built in
    it once, by the first test asking for it."""

    def __init__(self, folder):
        self.folder, self.opened, self.built = folder, Opened(), {}

    def once(self, name, build):
        if name not in self.built:
            self.built[name] = build()
        return self.built[name]


@pytest.fixture(scope="module")
def shared(request, run_folder):
    """The file's own folder within the run's folder, named for the file, cleared before its first test and after its last."""
    folder = run_folder / Path(str(request.path)).stem
    spec_text.clear_run(folder)
    held = Shared(folder)
    yield held
    held.opened.close()
    spec_text.clear_run(folder)
    try:
        folder.rmdir()
    except OSError:
        pass
