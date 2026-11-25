"""The design script's kept comparison, comparison.py of this set: which designs a change to the script, or to a form
it reads, reads differently, and the comparison run by the design script itself.

A project here holds the design script's own code, the skills copied as the test runs, under version control, since
the comparison reads the last commit's script. Each side of a comparison is a worktree under the project, standing
deep, so the tests of this file take short names: a test's folder is named for it.
"""
import pytest

from design_script_set import (CHECKOUT, COMPARISON, MAIN, RULE, RUNNER, SCRIPT, SET, a_script_project, compared, copy_files, git, listed, passes,
    shown, swap, three_designs)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


def test_one_design_listed(check):
    p = a_script_project("compared")
    plans = three_designs(p)
    got = compared(p, plans)
    check("the comparison lists no design where the script stands as the last commit held it", got[0] == 0 and listed(got) == [] and "0 designs read differently, of 3" in got[1], shown(got))
    p.put(SCRIPT, swap(p.read(SCRIPT), "\"Name is not a slug: \"", "\"Name is no slug: \""))
    got = compared(p, plans)
    check("after a change to the message of one check, it lists the one design that check reports, with each action reading it differently, and no other",
          got[0] == 0 and listed(got) == [plans + "/odd-name.md"] and "1 design read differently, of 3" in got[1]
          and "--check-design-form: exit 1 at both, its output differing" in got[1] and "- Name is not a slug: Odd Name" in got[1] and "+ Name is no slug: Odd Name" in got[1], shown(got))
    check("and it leaves no worktree behind, and the checkout's own files as they were",
          not (p.root / ".ai/tmp/worktrees/design-script-comparison-then").exists() and not (p.root / ".ai/tmp/worktrees/design-script-comparison-now").exists()
          and git(p.root, "worktree", "list").count("\n") == 0 and git(p.root, "status", "--porcelain", "--", ".ai/skills", "specs") == "M " + SCRIPT, git(p.root, "status", "--porcelain"))


def test_form_and_code(check):
    p = a_script_project("compared-form")
    plans = three_designs(p)
    form = swap(p.read(MAIN), "**Plural Name:** Design Goals", "**Plural Name:** Goals of a Design")
    p.put(MAIN, form)
    got = compared(p, plans)
    check("after a change to a form alone, the script as it stands reading it, the comparison lists each design the form's change reads differently: every one",
          got[0] == 0 and sorted(listed(got)) == sorted(plans + "/%s.md" % n for n in ("first-design", "second-design", "odd-name")) and "declares no Plural Name Design Goals" in got[1], shown(got))
    p.put(SCRIPT, swap(p.read(SCRIPT), "declared_type(GOAL_HOME, \"Design Goals\", root)", "declared_type(GOAL_HOME, \"Goals of a Design\", root)"))
    got = compared(p, plans)
    check("after the same change made together with the code reading it, each side reading the canon of its own tree, it lists no design",
          got[0] == 0 and listed(got) == [] and "0 designs read differently, of 3" in got[1], shown(got))


def test_cannot_be_made(check):
    p = a_script_project("compared-refused")
    got = compared(p, "docs")
    check("the comparison refuses a folder that is no plans folder, exit 2", got[0] == 2 and "design-script-comparison takes plans folders" in got[1], shown(got))
    p = a_script_project("compared-no-git", versioned=False)
    got = compared(p, three_designs(p))
    check("the comparison says it cannot be made where the project is under no version control, exit 2", got[0] == 2 and "cannot be made" in got[1], shown(got))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-kept-sets.md", "test-standing-in")
def test_run_by_the_script(check, fixtures):
    # the design script's own set stands in the project as the checkout holds it, its conftest.py saying which files
    # are the script's, with the runner's settings and one test standing in for the set's own, which holds nothing: so
    # the run reports each action and each Script Check as unheld, and nothing of the comparison
    p = a_script_project("compared-by-the-script", versioned=False)
    three_designs(p)
    copy_files(CHECKOUT, p.root, RUNNER + (SET + "/conftest.py",))
    p.put(SET + "/test_stand_in.py", fixtures["test-standing-in"])
    git(p.root, "init", "-q")
    p.commit()
    p.put(SCRIPT, swap(p.read(SCRIPT), "\"Name is not a slug: \"", "\"Name is no slug: \""))
    got = p.run("--check-kept-tests", SCRIPT)
    problems = [line for line in got[1].split("== check-kept-tests")[-1].split("\n") if line.startswith("specs/")]
    check("--check-kept-tests, given the design script's code, runs its kept tests and its kept comparison, which lists the one design read differently",
          "== check-kept-tests, over 1 changed file" in got[1] and "the kept tests of design-script, run for %s\n" % SCRIPT in got[1] and "$ python -B %s\n" % COMPARISON in got[1]
          and "\ndesign .ai/plans/design-specs/odd-name.md\n" in got[1] and "1 design read differently, of 3" in got[1] and "  1 test, 0 failed" in got[1], shown(got))
    check("and reports nothing for what the comparison lists: each problem it gives is of what the stand-in test leaves unheld",
          bool(problems) and all(RULE % "each-script-check-and-action-held-by-a-test" in line for line in problems) and "could not be made" not in got[1], "\n".join(sorted(set(problems))))
    got = p.run("--check-kept-tests", MAIN)
    check("--check-kept-tests, given a file of the canon the design script reads a form from, runs them too: a change to a form alone",
          "the kept tests of design-script, run for %s\n" % MAIN in got[1] and "$ python -B %s\n" % COMPARISON in got[1], shown(got))
    times = p.run("--show-kept-test-times")
    check("and the runner takes the comparison for no test", "comparison" not in times[1] and passes(times, "== show-kept-test-times, 1 test"), shown(times))
