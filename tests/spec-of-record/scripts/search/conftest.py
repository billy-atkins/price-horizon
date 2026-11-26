"""The search's set of kept tests: which files are the search's, and what the set's tests share.

A test calls a unit of the search, or of the one reading it reads a file by, over a project of fixtures it writes
within its own folder (`project`), each fixture at the path the test gives it: the project's glossary and its registry
of skills among them where a test needs them, since the search reads those of the project it searches and no form of
the canon. A search a test opens is closed as the test ends (`opened`). What the tests of one file share is built once
by that file's own fixture, in the file's folder within the run's folder (`shared`). A test of an action calls `main`,
the unit the entry script runs, with the project's root; a few tests run the entry script as a process to hold its
wiring (`run_entry`). The search writes in the scratch space it is given, or the one under the project it searches,
and so always within the run's folder, and reads the model's files from where it installs them once on a machine,
which are no run's output. A test file takes these names by `from search_set import ...`, the name this file is
registered under as the runner reads it.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

# The files of the script these tests are of, the search: its code, and each file of the canon it reads a form from
# as it runs, which are none. A path ending in a slash names each file beneath it.
SCRIPT_FILES = (".ai/skills/lib/search.py", ".ai/skills/lib/reading.py", ".ai/skills/lib/spec_text.py", ".ai/skills/lib/citation_links.py",
                ".ai/skills/lib/code_checks.py", ".ai/skills/lib/constructs.py", ".ai/skills/lib/expressions.py",
                ".ai/skills/search-spec-of-record-scope/scripts/")
FORM_FILES = ()
ACTIONS_IN = ".ai/skills/lib/search.py"

CHECKOUT = Path(__file__).resolve().parents[4]
LIB = CHECKOUT / ".ai" / "skills" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
import reading  # noqa: E402
import search  # noqa: E402
import spec_text  # noqa: E402

ENTRY = CHECKOUT / ".ai" / "skills" / search.SKILL / "scripts" / (search.SKILL + ".py")
SKILL_FOLDER = ".ai/skills/" + search.SKILL

# where each fixture of a project stands in it: the corpus of forms, the small project about a heron, and the
# invented library, whose files cite each other by these paths
CORPUS = {"forms-spec": "specs/forms.md", "target-spec": "specs/target.md", "promise-product-file": "product/promise.md",
          "ledger-glossary": "specs/methodology/glossary/glossary.md", "ledger-python": "code/sample.py", "ledger-typescript": "code/sample.ts",
          "ledger-csharp": "code/sample.cs", "ledger-table-sql": "code/schema.sql", "ledger-settings-yaml": "code/settings.yaml"}
HERON = {"heron-spec": "specs/target.md", "stack-naming-one-code-root": search.code_checks.STACK, "heron-function": "code/sample.py",
         "egret-function": "src/other.py", "design-citing-the-heron": ".ai/plans/design-specs/a-design.md",
         "plan-citing-the-heron": ".ai/plans/other-plan.md", "follow-ups-naming-a-heron": ".ai/follow-ups.md"}
LIBRARY = {"library-" + name: "specs/library/%s.md" % name
           for name in ("membership", "loans", "overdue", "holds", "catalogue", "donations", "opening", "volunteers", "rooms", "events")}
# the `reads` marker of each of those projects
READS_CORPUS = [pytest.mark.reads("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary"),
                pytest.mark.reads("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")]
READS_HERON = [pytest.mark.reads("search-heron-project.md", *HERON)]
READS_LIBRARY = [pytest.mark.reads("search-library-lending.md", *list(LIBRARY)[:5]), pytest.mark.reads("search-library-premises.md", *list(LIBRARY)[5:])]


def project(root, fixtures, placed):
    """-> the root of a project of fixtures written at `root`, each fixture at its path, `placed` mapping a fixture's
    key to the path it stands at."""
    root = Path(root)
    for key, path in placed.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(fixtures[key], encoding="utf-8", newline="\n")
    return root


def result_file(folder, text):
    """-> the path of a result's text, a fixture, written in a folder under the name its Result field holds."""
    path = Path(folder) / re.search(r"^  - \*\*Result:\*\* (\S+) \\$", text, re.M).group(1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def every_file(root):
    """-> each file under a project's root, by its path from the root, for a search told to cover them all."""
    return sorted(p.relative_to(root).as_posix() for p in Path(root).rglob("*") if p.is_file())


def lines_of(places):
    """-> {(path, first line)} of a result's places."""
    return {(place.path, place.first) for place in places}


def paths_of(result):
    return sorted({p.path for p in result.places})


def line_holding(text, words):
    """-> the number of the first line of a text holding the words."""
    return next(n for n, line in enumerate(text.split("\n"), 1) if words in line)


def printed_places(printed):
    """-> the places a run printed, each on a line of its own beneath the result's name and its count."""
    return [line.strip() for line in printed.split("\n") if line.startswith("  `")]


def ask(root, *argv):
    """-> the exit code of the entry script's `main` asked over a project, what it prints being the test's to read."""
    return search.main(["search"] + [str(a) for a in argv], root=root)


def run_entry(root, *argv, env=None):
    """-> (the exit code, what was printed) of the entry script run as a process in a project. The project is given
    the skill's folder, empty, by which a run there takes the project for the checkout it answers over and writes in."""
    (Path(root) / SKILL_FOLDER).mkdir(parents=True, exist_ok=True)
    done = subprocess.run([sys.executable, "-B", str(ENTRY)] + [str(a) for a in argv], cwd=root, capture_output=True, env=dict(os.environ, **(env or {})))
    return done.returncode, (done.stdout + done.stderr).decode("utf-8", "replace").replace("\r\n", "\n")


def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=search-tests", "-c", "user.email=search-tests@example.invalid", "-c", "core.autocrlf=false",
                           "-c", "commit.gpgsign=false"] + list(args), cwd=root, capture_output=True, text=True)
    if done.returncode:
        raise AssertionError("git %s: %s" % (" ".join(args), done.stderr))
    return done.stdout.strip()


def vectors_held(s):
    """-> (the vectors an index holds, the passages and sentences it holds): each a count."""
    held = sum(s.db.execute("select count(*) from %s" % t).fetchone()[0] for t in ("passage_vectors", "sentence_vectors"))
    texts = sum(s.db.execute("select count(*) from %s" % t).fetchone()[0] for t in ("passages", "sentences"))
    return held, texts


class Opened:
    """The searches a test or a file's own fixture opened, each index closed as the test or the file ends, so the
    clean-up that follows finds no file held open."""

    def __init__(self):
        self.held = []

    def __call__(self, root, **given):
        given.setdefault("quiet", True)
        found = search.Search(root, **given)
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


sys.modules["search_set"] = sys.modules[__name__]
