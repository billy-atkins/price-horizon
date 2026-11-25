"""The kept tests run whole in a second checkout of the project, each test giving the result it gives in the checkout.

The second checkout is a clone of the checkout at the last commit, made in the test's own folder, so it stands beneath
the checkout's working files, with the checkout's uncommitted work laid over it and the search's model copied into
it, since a clone is its own main checkout. The test runs the design script's set and the search's set there and in
the checkout, each by the runner, each run writing within a folder of its own inside this run's, and requires each
test to give the same result in both. It reads the checkout's repository and writes nothing of it: no worktree is
added to it, and nothing is written outside the run's folder.

The file and its one test take short names: the test's folder is named for them, and the model's files stand deep
within the clone, on a machine whose paths may be no longer than 260 characters.

The test is slow: a run asks for it with --slow.
"""
import concurrent.futures
import shutil

import pytest

from design_script_set import (CHECKOUT, KEPT, SET, a_run, git)

pytestmark = [pytest.mark.slow]
# the sets of kept tests run in the second checkout and in the checkout
KEPT_SETS = (SET, KEPT + "/scripts/search")


def test_alike(check, work, shared_folder):
    import search  # the checkout's own, on the path the set's conftest.py reads the shared code by
    before = git(CHECKOUT, "worktree", "list")
    second = work / "s"
    git(work, "clone", "-q", "--local", "--no-hardlinks", str(CHECKOUT), str(second))
    # the checkout's uncommitted work laid over the clone, as the kept comparison lays it over a side: each file
    # changed or new copied in, and each file removed taken out
    changed = [p for args in (("diff", "--name-only", "-z", "HEAD"), ("ls-files", "--others", "--exclude-standard", "-z")) for p in git(CHECKOUT, *args).split("\0") if p.strip()]
    for path in sorted(set(p.strip() for p in changed)):
        if (CHECKOUT / path).is_file():
            (second / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CHECKOUT / path, second / path)
        elif (second / path).is_file():
            (second / path).unlink()
    shutil.copytree(search.model_folder(), second / search.SCRATCH / "model")
    # each run in a folder of its own, of a short name, since a test's project stands deep within it
    runs = [(where, kept, shared_folder / ("%s%d" % (place, n))) for n, kept in enumerate(KEPT_SETS) for place, where in (("s", second), ("c", CHECKOUT))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        gave = dict(zip([(where, kept) for where, kept, _ in runs], pool.map(lambda run: a_run(run[0], run[2], [run[1]]), runs)))
    for kept in KEPT_SETS:
        (there_status, there, there_end), (here_status, here, here_end) = gave[(second, kept)], gave[(CHECKOUT, kept)]
        results = lambda cases: {case["test"]: case["outcome"] for case in cases or []}
        there, here = results(there), results(here)
        check("%s runs whole in the second checkout and passes: %d tests, %d failed" % (kept, len(there), sum(o == "failed" for o in there.values())), there_status == 0 and bool(there), there_end[-1500:])
        check("%s runs whole in the checkout and passes: %d tests, %d failed" % (kept, len(here), sum(o == "failed" for o in here.values())), here_status == 0 and bool(here), here_end[-1500:])
        check("%s makes the same tests in the second checkout as in the checkout" % kept, sorted(there) == sorted(here), "\n".join(sorted(set(there) ^ set(here))[:20]))
        for test in sorted(set(there) & set(here)):
            if there[test] != here[test]:
                check("%s: a test gives in the second checkout the result it gives in the checkout: %s" % (kept, test), False, "in the second checkout: %s\nin the checkout: %s" % (there[test], here[test]))
        check("%s: each test gives in the second checkout the result it gives in the checkout" % kept, there == here)
    check("the checkout's own repository holds the checkouts it held before, and no other", git(CHECKOUT, "worktree", "list") == before, git(CHECKOUT, "worktree", "list"))
