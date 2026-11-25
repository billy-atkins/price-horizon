"""What every kept test of Spec of Record's scripts is given.

A run writes only within its one folder among the working files, .ai/tmp/kept-tests/ of the checkout, or, for a run
another run started, the folder that run names for it. The same clean-up runs before and after each test, over the
test's own folder, and before and after the run, after which the folder holds the run's report alone.

A test is handed:
  work       its own folder within the run's folder, empty as the test starts and removed as it ends
  fixtures   the snippets of the fixtures its `reads` marker names, by key
  check      a function recording one check the test makes: check(what, holds, detail). The test fails as it ends
             where any check it made did not hold, each named, so one run shows every check that failed
  checkout   the root of the checkout the tests are run in
  run_folder the run's folder

A run takes --action FLAG and --script-check NAME, each choosing the tests naming it, --slow, running the tests marked
slow too, and --kept-links FILE, writing what each test names, for the design script's checks of coverage.
"""
import json
import os
import re
import sys
from pathlib import Path

import pytest

CHECKOUT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CHECKOUT / ".ai" / "skills" / "lib"))
import spec_text  # noqa: E402  the reading the skills' scripts share: the form of a fixture file, and the one clean-up

RUN = Path(os.environ.get(spec_text.KEPT_RUN_NAMED) or CHECKOUT / spec_text.KEPT_RUN).resolve()
FIXTURES = CHECKOUT / spec_text.FIXTURES
WAYS = ("passes", "reports")
HELD = {}  # a fixture file's name -> {key: snippet}, read once in a run

# each process a test starts writes no compiled module, finds no repository above the run's folder, and is told no
# folder of a run: a run a test starts names its own
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["GIT_CEILING_DIRECTORIES"] = str(RUN.parent)
os.environ.pop(spec_text.KEPT_RUN_NAMED, None)


def pytest_addoption(parser):
    group = parser.getgroup("the kept tests of Spec of Record")
    group.addoption("--action", action="append", default=[], help="run the tests naming this action of their script alone")
    group.addoption("--script-check", action="append", default=[], help="run the tests naming this Script Check alone")
    group.addoption("--slow", action="store_true", default=False, help="run the tests marked slow too")
    group.addoption("--kept-links", default=None, help="write what each test names to this file: its actions, the way it holds them, its Script Checks and its fixtures")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # a compiled module left beside a kept file, by a run started without -B, is cleared as any run starts
    for compiled in sorted(Path(__file__).parent.rglob("__pycache__")):
        spec_text.clear_run(compiled)
        compiled.rmdir()
    if not sys.dont_write_bytecode:
        raise pytest.UsageError("the kept tests are run with python -B, so a run compiles no module beside a file it reads: "
                                "python -B -m pytest tests/spec-of-record")
    spec_text.clear_run(RUN)
    if not config.option.xmlpath:
        config.option.xmlpath = str(RUN / spec_text.KEPT_REPORT)
    if not config.option.basetemp:
        config.option.basetemp = str(RUN / "runner")


def pytest_unconfigure(config):
    spec_text.clear_run(RUN, keep=(spec_text.KEPT_REPORT,))


CHECKS = pytest.StashKey()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    """A test whose own code ran whole fails where a check it recorded did not hold, each such check named."""
    result = yield
    made = item.stash.get(CHECKS, [])
    failed = ["%s%s" % (what, "\n    " + str(detail).replace("\n", "\n    ") if detail not in ("", None) else "") for what, holds, detail in made if not holds]
    if failed:
        pytest.fail("%d of %d checks did not hold:\n  %s" % (len(failed), len(made), "\n  ".join(failed)), pytrace=False)
    return result


def names(item, marker):
    return [str(a) for m in item.iter_markers(marker) for a in m.args]


def read_fixtures(item):
    """-> [(fixture file, key)] for each fixture a test's `reads` markers name."""
    return [(str(m.args[0]), str(key)) for m in item.iter_markers("reads") for key in m.args[1:]]


def script_checks(item):
    """-> the Name of each Script Check a test's canon-spec annotations cite."""
    path = Path(str(item.path))
    held = item.session.stash.setdefault(ANNOTATIONS, {})
    if path not in held:
        held[path] = spec_text.test_annotations(path.read_text(encoding="utf-8"))
    cited = held[path].get(getattr(item, "originalname", None) or item.name, [])
    return [n for n in (spec_text.check_named(c) for c in cited) if n]


ANNOTATIONS = pytest.StashKey()


def pytest_collection_modifyitems(config, items):
    actions, checks = set(config.getoption("--action")), set(config.getoption("--script-check"))
    kept, left = [], []
    for item in items:
        chosen = (not actions or actions & set(names(item, "action"))) and (not checks or checks & set(script_checks(item)))
        slow = item.get_closest_marker("slow") is not None and not config.getoption("--slow")
        (kept if chosen and not slow else left).append(item)
    links = config.getoption("--kept-links")
    if links:
        # every test found, the ones a run leaves out among them: what the tests hold is read of them all
        rows = [{"test": item.nodeid, "file": Path(str(item.path)).resolve().relative_to(CHECKOUT).as_posix(),
                 "actions": names(item, "action"), "script_checks": script_checks(item),
                 "ways": {way: names(item, way) for way in WAYS if item.get_closest_marker(way) is not None},
                 "slow": item.get_closest_marker("slow") is not None,
                 "reads": read_fixtures(item)} for item in items]
        Path(links).parent.mkdir(parents=True, exist_ok=True)
        Path(links).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if left:
        config.hook.pytest_deselected(items=left)
        items[:] = kept


@pytest.fixture(scope="session")
def checkout():
    return CHECKOUT


@pytest.fixture(scope="session")
def run_folder():
    """The run's one folder among the working files."""
    return RUN


@pytest.fixture(autouse=True)
def work(request):
    """The test's own folder within the run's folder: cleared before the test starts and after it ends."""
    folder = RUN / "work" / re.sub(r"[^A-Za-z0-9]+", "-", request.node.nodeid)[-80:].strip("-")
    spec_text.clear_run(folder)
    yield folder
    spec_text.clear_run(folder)
    try:
        folder.rmdir()
    except OSError:
        pass


@pytest.fixture
def fixtures(request):
    """-> {key: snippet} for the fixtures the test's `reads` markers name, and no other."""
    out = {}
    for name, key in read_fixtures(request.node):
        if name not in HELD:
            path = FIXTURES / name
            if not path.is_file():
                raise pytest.UsageError("%s names the fixture file %s, which does not stand under %s" % (request.node.nodeid, name, spec_text.FIXTURES))
            found, problems = spec_text.fixtures_of(path.read_text(encoding="utf-8"))
            if problems:
                raise pytest.UsageError("%s is out of the form of a fixture file: line %d, %s" % (name, problems[0][0], problems[0][1]))
            HELD[name] = {f["key"]: f["snippet"] for f in found}
        if key not in HELD[name]:
            raise pytest.UsageError("%s names the fixture %s, which %s does not hold" % (request.node.nodeid, key, name))
        if key in out and out[key] != HELD[name][key]:
            raise pytest.UsageError("%s takes two fixtures under the key %s" % (request.node.nodeid, key))
        out[key] = HELD[name][key]
    return out


@pytest.fixture
def check(request):
    """-> check(what, holds, detail=""): records one check the test makes. The test fails as its own code ends where a
    check it made did not hold, naming each, so one run shows every check that failed."""
    made = request.node.stash.setdefault(CHECKS, [])

    def record(what, holds, detail=""):
        made.append((str(what), bool(holds), detail))
    return record
