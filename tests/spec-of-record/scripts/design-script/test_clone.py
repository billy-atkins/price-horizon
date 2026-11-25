"""The kept tests run whole in a second checkout of the project, and pass there.

The second checkout is a clone of the checkout at the last commit, made in the test's own folder, so it stands beneath
the checkout's working files, with the checkout's uncommitted work laid over it, the runner's settings and what every
test is handed among it, and the search's model copied into it, since a clone is its own main checkout. The test runs
the design script's set and the search's set there once, by the runner, in a run writing within a folder of its own
inside this run's, and requires every test to pass. That run leaves this file out, or it would clone again without
end. The test reads the checkout's repository and writes nothing of it: no worktree is added to it, and nothing is
written outside the run's folder.

The file and its one test take short names, and the clone is the test's folder itself: the folder is named for them,
and the model's files stand deep within the clone, on a machine whose paths may be no longer than 260 characters.
"""
import shutil

from design_script_set import (CHECKOUT, KEPT, SET, a_run, git)

# the sets of kept tests run in the second checkout, and this file, which the run there leaves out
KEPT_SETS = (SET, KEPT + "/scripts/search")
THIS_FILE = SET + "/test_clone.py"


def test_runs(check, work, shared_folder):
    import search  # the checkout's own, on the path the set's conftest.py reads the shared code by
    before = git(CHECKOUT, "worktree", "list")
    second = work
    git(work, "clone", "-q", "--local", "--no-hardlinks", str(CHECKOUT), ".")
    # the checkout's uncommitted work laid over the clone, as the kept comparison lays it over a side: each file
    # changed or new copied in, and each file removed taken out
    changed = [p for args in (("diff", "--name-only", "-z", "HEAD"), ("ls-files", "--others", "--exclude-standard", "-z")) for p in git(CHECKOUT, *args).split("\0") if p.strip()]
    for path in sorted(set(p.strip() for p in changed)):
        if (CHECKOUT / path).is_file():
            (second / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CHECKOUT / path, second / path)
        elif (second / path).is_file():
            (second / path).unlink()
    alike = [path for path in (KEPT + "/conftest.py", KEPT + "/pytest.ini", THIS_FILE) if (second / path).read_bytes().replace(b"\r\n", b"\n") != (CHECKOUT / path).read_bytes().replace(b"\r\n", b"\n")]
    check("the second checkout holds the runner's settings, what every test is handed and this file as the checkout holds them", not alike, alike)
    shutil.copytree(search.model_folder(), second / search.SCRATCH / "model")
    status, cases, printed = a_run(second, shared_folder / "s", list(KEPT_SETS) + ["--ignore=" + THIS_FILE])
    results = {case["test"]: case["outcome"] for case in cases or []}
    failed = sorted(test for test, outcome in results.items() if outcome == "failed")
    check("the run in the second checkout found the tests of both sets, and none of this file",
          any("design-script" in test for test in results) and any(".search." in test for test in results) and not any("test_clone" in test for test in results), sorted(results)[:5])
    check("both sets run whole in the second checkout and every test passes: %d tests, %d failed" % (len(results), len(failed)), status == 0 and bool(results) and not failed,
          "\n".join(failed) + "\n" + printed[-3000:])
    check("the checkout's own repository holds the checkouts it held before, and no other", git(CHECKOUT, "worktree", "list") == before, git(CHECKOUT, "worktree", "list"))
