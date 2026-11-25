"""--check-kept-tests: a script's kept tests run by the design script through the registered runner, each result read
from the run's report, and the folder a run writes within.

A project here holds the runner as the checkout holds it, its settings and what every test is handed, copied as the
test runs, and a set of kept tests of a script of its own, the guide's: two tests, a fixture file and the fixtures'
index. The design script runs that set in the project as it runs the checkout's own.
"""
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import pytest

from design_script_set import (DRAFTED, GUIDE_SET, GUIDE_TESTS, KEPT, KEPT_RULE, KEPT_RUN, OTHER_DESIGN, Project, RULE, SKILLS, design_documents,
    failing, git, kept_tests, outside_the_run, passes, reports, run_holds, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-kept-sets.md", "guide-script", "guide-set-conftest", "guide-set-tests", "fixture-file-of-one-line", "index-listing-one-file")]
AUDIT_SCRIPT = ".ai/skills/audit-specs/scripts/audit-specs.py"  # a script of a registered skill, which no set of the project names
RAN = "$ python -B -m pytest %s\n  2 tests, 0 failed\n"


def tides_set(p, fixtures):
    """Give a project a second set of kept tests, of a script of its own, the tides'."""
    p.put("tools/tides.py", fixtures["tides-script"])
    p.put(KEPT + "/scripts/tides/conftest.py", fixtures["tides-set-conftest"])
    p.put(KEPT + "/scripts/tides/test_tides.py", fixtures["tides-set-tests"])


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-fixture-read-by-a-kept-test]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixtures-index-lists-its-folder]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "tides-script", "tides-set-conftest", "tides-set-tests")
def test_tests_of_each_script_touched_are_run_and_no_others(check, fixtures):
    whole = "the checks of %s as a whole were made\nthe run's report: %s/report.xml\n\n0 problems" % (KEPT, KEPT_RUN)
    for skill in SKILLS:
        p = Project("kept-action")
        kept_tests(p)
        tides_set(p, fixtures)
        got = p.run("--check-kept-tests", "docs/guide.md", skill=skill)
        check("--check-kept-tests of %s, given a file a script reads a form from, runs the kept tests of that script, a change to a form alone, reads the result from the run's report, "
              "makes the checks of the tests' folder, and reports nothing: each action held both ways, each fixture read, the fixture file in its form and listed" % skill,
              passes(got, "== check-kept-tests, over 1 changed file", whole) and "the kept tests of guide, run for docs/guide.md\n" + RAN % GUIDE_TESTS in got[1]
              and "tides" not in got[1], shown(got))
    got = p.run("--check-kept-tests", "tools/tides.py", "docs/notes.md")
    check("--check-kept-tests, given the code of the second script and a file of no script, runs the second script's kept tests and no others",
          passes(got, "== check-kept-tests, over 2 changed files", whole) and "the kept tests of tides, run for tools/tides.py\n" in got[1] and "guide" not in got[1], shown(got))
    got = p.run("--check-kept-tests", KEPT + "/fixtures/guide.md")
    check("--check-kept-tests, given a fixture file, runs the kept tests of the script whose tests read a fixture from it, and no others",
          passes(got, "== check-kept-tests, over 1 changed file", whole) and "the kept tests of guide, run for %s/fixtures/guide.md\n" % KEPT in got[1] and "tides" not in got[1], shown(got))
    got = p.run("--check-kept-tests", KEPT + "/scripts/tides/test_tides.py")
    check("--check-kept-tests, given a file of a set, runs that set", passes(got, "== check-kept-tests", whole) and "the kept tests of tides, run for " in got[1] and "guide" not in got[1], shown(got))
    got = p.run("--check-kept-tests", KEPT + "/pytest.ini")
    check("--check-kept-tests, given the runner's settings, runs every set",
          passes(got, "== check-kept-tests", whole) and "the kept tests of guide, run for " in got[1] and "the kept tests of tides, run for " in got[1] and "  4 tests" not in got[1], shown(got))
    got = p.run("--check-kept-tests", KEPT + "/fixtures/index.md")
    check("--check-kept-tests, given a file under the tests that is no file of a set, runs no test and makes the checks of the tests' folder",
          passes(got, "== check-kept-tests", "the checks of %s as a whole were made\n\n0 problems" % KEPT) and "the kept tests of" not in got[1], shown(got))
    got = p.run("--check-kept-tests", "docs/notes.md", AUDIT_SCRIPT)
    check("--check-kept-tests, given a script of the skills no set names, runs none and says that script holds no kept tests",
          passes(got, "== check-kept-tests, over 2 changed files", "no set of kept tests names %s\n\n0 problems" % AUDIT_SCRIPT) and "the kept tests of" not in got[1], shown(got))
    got = p.run("--check-kept-tests", "docs/notes.md")
    check("--check-kept-tests, given a file of no script, says no changed file is one",
          passes(got, "== check-kept-tests, over 1 changed file", "no changed file is a file of a script holding kept tests\n\n0 problems"), shown(got))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
def test_failing_test_is_named_from_the_report(check, fixtures):
    for skill in SKILLS:
        p = Project("kept-action-fails")
        kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
        got = p.run("--check-kept-tests", "docs/guide.md", skill=skill)
        check("--check-kept-tests of %s fails where a kept test fails, naming the test and what it reported from the run's report" % skill,
              reports(got, "== check-kept-tests, over 1 changed file",
                      ["  2 tests, 1 failed\n  FAILED scripts.guide.test_guide::test_no_pier_is_named\n", "1 of 1 checks did not hold:", "two and two make four", KEPT_RULE,
                       "%s holds a test that fails: scripts.guide.test_guide::test_no_pier_is_named" % GUIDE_TESTS, "1 problem"])
              and "test_the_quay_is_named" not in got[1], shown(got))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-ferry.md", "ferry-design")
def test_given_no_file_the_changed_files_are_read(check, fixtures):
    p = Project("kept-action-changed")
    kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
    git(p.root, "init", "-q")
    p.commit()
    p.design(log=DRAFTED)
    got = p.run("--check-kept-tests")
    check("--check-kept-tests given no file runs nothing where the checkout holds only working files changed", passes(got, "== check-kept-tests, over 0 changed files", "0 problems"), shown(got))
    p.put("docs/guide.md", fixtures["island-guide"] + "\nThe ferry does not run on the feast day.\n")
    got = p.run("--check-kept-tests")
    check("--check-kept-tests given no file runs the kept tests of the script whose form the checkout holds changed against the last commit, and fails where one fails",
          reports(got, "== check-kept-tests, over 1 changed file", ["run for docs/guide.md", "%s holds a test that fails: " % GUIDE_TESTS]), shown(got))
    p.put(GUIDE_TESTS, fixtures["guide-set-tests"])
    got = p.run("--check-kept-tests")
    check("and reads a file of tests changed with it as a changed file, and passes where the tests pass",
          passes(got, "== check-kept-tests, over 2 changed files", "0 problems") and "run for docs/guide.md, %s\n" % GUIDE_TESTS in got[1], shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "test-ending-its-process", "test-recording-a-property")
def test_run_leaving_no_report_or_one_out_of_the_schema_could_not_be_run(check, fixtures):
    rule = RULE % "kept-test-results-read-from-the-report"
    p = Project("kept-no-report")
    # a test of the file ends the process running it, so the run writes no report
    kept_tests(p, tests=fixtures["guide-set-tests"] + "\n\n" + fixtures["test-ending-its-process"])
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests reports a file of tests whose run left no report as one that could not be run, and gives no result of it",
          reports(got, "== check-kept-tests", ["%s could not be run: the run left no report at report.xml, exit 3" % GUIDE_TESTS, rule, "1 problem"]) and " tests, " not in got[1], shown(got))
    p = Project("kept-out-of-the-schema")
    # a test of the file writes, within its own entry of the report, an element the schema declares within no test's
    kept_tests(p, tests=fixtures["guide-set-tests"] + "\n\n" + fixtures["test-recording-a-property"])
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests reports a file of tests whose run's report is out of the registered schema as one that could not be run, and gives no result of it",
          reports(got, "== check-kept-tests", ["%s could not be run: the run's report is out of the registered schema: testcase holds properties, which the schema does not declare within it" % GUIDE_TESTS,
                                               rule, "1 problem"]) and " tests, " not in got[1], shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reports
def test_report_of_a_real_run_holds_to_the_registered_schema(check, fixtures):
    p = Project("kept-schema")
    kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
    got = p.run("--check-kept-tests", "docs/guide.md")
    report = ET.parse(p.root / KEPT_RUN / "report.xml").getroot()
    check("the report of a real run, one test passing and one failing, holds to the registered schema, and holds each test with its time",
          got[0] == 1 and design_documents.junit_problems(report) == [] and [case.attrib["name"] for case in report.iter("testcase")] == ["test_the_quay_is_named", "test_no_pier_is_named"]
          and all(float(case.attrib["time"]) >= 0 for case in report.iter("testcase")) and len(list(report.iter("failure"))) == 1, design_documents.junit_problems(report))
    cases, _ = design_documents.read_kept_report(p.root / KEPT_RUN / "report.xml")
    check("and the design script reads each test's result from it", [(case["test"].split("::")[1], case["outcome"]) for case in cases or []]
          == [("test_the_quay_is_named", "passed"), ("test_no_pier_is_named", "failed")], cases)
    # the same report given an attribute, and then an element, the schema does not declare
    next(report.iter("testcase")).set("ferry", "north quay")
    check("a report holding an attribute the schema does not declare is out of the schema",
          design_documents.junit_problems(report) == ["testcase holds the attribute ferry, which the schema does not declare of it"], design_documents.junit_problems(report))
    report = ET.parse(p.root / KEPT_RUN / "report.xml").getroot()
    ET.SubElement(next(report.iter("testcase")), "crossing")
    check("and so is one holding an element the schema does not declare",
          design_documents.junit_problems(report) == ["testcase holds crossing, which the schema does not declare within it"], design_documents.junit_problems(report))
    report = ET.parse(p.root / KEPT_RUN / "report.xml").getroot()
    del next(report.iter("testcase")).attrib["name"]
    check("and one lacking an attribute the schema requires", design_documents.junit_problems(report) == ["testcase lacks the attribute name"], design_documents.junit_problems(report))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-kept-sets.md", "comparison-listing-one-design", "tides-script", "tides-set-conftest", "tides-set-tests")
def test_comparison_is_run_and_fails_nothing_for_what_it_lists(check, fixtures):
    comparison = GUIDE_SET + "/comparison.py"
    p = Project("kept-comparison")
    kept_tests(p, comparison=fixtures["comparison-listing-one-design"])
    tides_set(p, fixtures)
    got = p.run("--check-kept-tests", "tools/guide.py")
    check("--check-kept-tests runs the kept comparison of a script the changed files hold a file of, beside its tests, and reports nothing for the design it lists",
          passes(got, "== check-kept-tests, over 1 changed file", "0 problems") and RAN % GUIDE_TESTS + "$ python -B %s\ndesign %s\n" % (comparison, OTHER_DESIGN) in got[1]
          and "1 design read differently, of 1\nexit 0\n" in got[1], shown(got))
    times = p.run("--show-kept-test-times")
    check("and the runner takes the comparison for no test", passes(times, "== show-kept-test-times, 2 tests") and "comparison" not in times[1], shown(times))
    got = p.run("--check-kept-tests", "tools/tides.py")
    check("--check-kept-tests runs no comparison of a script none of whose files the changed files hold", passes(got, "== check-kept-tests", "0 problems") and "comparison" not in got[1], shown(got))
    # the comparison ending as one that could not be made
    p.put(comparison, fixtures["comparison-listing-one-design"] + "raise SystemExit(2)\n")
    got = p.run("--check-kept-tests", "tools/guide.py")
    check("--check-kept-tests fails where a kept comparison could not be made", reports(got, "== check-kept-tests", ["%s could not be made, exit 2" % comparison, KEPT_RULE, "1 problem"]), shown(got))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "test-standing-in")
def test_set_that_cannot_be_run_is_reported(check, fixtures):
    p = Project("kept-unread")
    kept_tests(p)
    # a second set whose conftest.py names its script's code as one path, and not as a tuple of paths
    p.put(KEPT + "/scripts/ledger/conftest.py", swap(fixtures["guide-set-conftest"], "(\"tools/guide.py\",)", "\"tools/ledger.py\""))
    got = p.run("--check-kept-tests", "docs/notes.md")
    check("--check-kept-tests fails where a set of kept tests does not say which files are its script's, whatever files it is given",
          reports(got, "== check-kept-tests", ["%s/scripts/ledger cannot be run: its conftest.py names no SCRIPT_FILES as a tuple of paths at its top level" % KEPT, KEPT_RULE, "1 problem"]), shown(got))
    p = Project("kept-no-tests")
    kept_tests(p)
    (p.root / GUIDE_TESTS).unlink()
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests fails where a set a changed file calls for holds no file of tests", reports(got, "== check-kept-tests", ["%s holds no file of tests" % GUIDE_SET, KEPT_RULE]), shown(got))
    p = Project("kept-no-test-found")
    kept_tests(p)
    p.put(GUIDE_SET + "/test_none.py", "import pytest\n")
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests fails where a file of tests holds no test the runner finds, and runs the set's other file",
          reports(got, "== check-kept-tests", ["%s/test_none.py holds no test the runner finds" % GUIDE_SET, KEPT_RULE, RAN % GUIDE_TESTS, "1 problem"]), shown(got))
    p = Project("kept-not-found")
    kept_tests(p)
    p.put(GUIDE_SET + "/test_broken.py", "def test_broken(:\n")
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests fails where the runner cannot find the tests, a file of them being no Python",
          reports(got, "== check-kept-tests", ["the runner could not find the kept tests, exit 2", KEPT_RULE]), shown(got))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-kept-sets.md", "test-waiting-in-its-folder")
def test_run_writes_within_its_folder_and_leaves_its_report_alone(check, fixtures):
    p = Project("kept-run-folder")
    kept_tests(p)
    before = outside_the_run(p)
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("a run that passed changed nothing of the project outside the run's folder, and left that folder holding the run's report alone",
          passes(got, "== check-kept-tests", "0 problems") and outside_the_run(p) == before and run_holds(p) == ["report.xml"],
          (run_holds(p), sorted(k for k in set(before) ^ set(outside_the_run(p)))))
    p.put(GUIDE_TESTS, failing(fixtures["guide-set-tests"]))
    before = outside_the_run(p)
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("a run that failed changed nothing outside the run's folder either, and left it holding the run's report alone",
          got[0] == 1 and outside_the_run(p) == before and run_holds(p) == ["report.xml"], (run_holds(p), sorted(k for k in set(before) ^ set(outside_the_run(p)))))
    # a run cut off: made by hand, of a file whose one more test writes into its own folder and waits, and killed as
    # that test waits
    p.put(GUIDE_TESTS, fixtures["guide-set-tests"] + "\n\n" + fixtures["test-waiting-in-its-folder"])
    before = outside_the_run(p)
    by_hand = [sys.executable, "-B", "-m", "pytest", KEPT, "-q"]
    run = subprocess.Popen(by_hand, cwd=p.root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        waited = time.monotonic()
        while not list((p.root / KEPT_RUN).glob("work/*/started.txt")) and run.poll() is None and time.monotonic() - waited < 90:
            time.sleep(0.2)
        started = [f.relative_to(p.root / KEPT_RUN).as_posix() for f in (p.root / KEPT_RUN).glob("work/*/started.txt")]
    finally:
        run.kill()
        run.wait()
    check("a run cut off as a test ran left, within the run's folder, what that test had written, and changed nothing outside it",
          len(started) == 1 and "work" in run_holds(p) and "report.xml" not in run_holds(p) and outside_the_run(p) == before, (started, run_holds(p)))
    p.put(GUIDE_TESTS, fixtures["guide-set-tests"])
    before = outside_the_run(p)
    again = subprocess.run(by_hand, cwd=p.root, capture_output=True, text=True)
    check("the next run, made by hand, cleared what the cut-off run left: the folder holds that run's report alone, and nothing outside it is changed",
          again.returncode == 0 and run_holds(p) == ["report.xml"] and outside_the_run(p) == before, (again.stdout[-600:], run_holds(p)))

# what a process prints of its own priority: on Windows its priority class, elsewhere how far it is niced
OWN_PRIORITY = ("import os\n"
                "if os.name == 'nt':\n"
                "    import ctypes\n"
                "    k = ctypes.windll.kernel32\n"
                "    k.GetCurrentProcess.restype = ctypes.c_void_p\n"
                "    k.GetPriorityClass.argtypes = (ctypes.c_void_p,)\n"
                "    k.GetPriorityClass.restype = ctypes.c_uint32\n"
                "    print('below' if k.GetPriorityClass(k.GetCurrentProcess()) in (0x4000, 0x40) else 'ordinary')\n"
                "else:\n"
                "    print('below' if os.getpriority(os.PRIO_PROCESS, 0) >= 10 else 'ordinary')\n")


def test_run_stands_below_the_priority_of_a_persons_own_work(check):
    own = subprocess.run([sys.executable, "-c", OWN_PRIORITY], capture_output=True, text=True)
    check("a process a kept test starts runs below the priority of a person's own work, as the run it belongs to does, so "
          "the machine stays the person's while the tests run", own.stdout.strip() == "below", own.stdout + own.stderr)
    nested = subprocess.run([sys.executable, "-c", "import subprocess, sys; print(subprocess.run([sys.executable, '-c', %r], "
                             "capture_output=True, text=True).stdout.strip())" % OWN_PRIORITY], capture_output=True, text=True)
    check("and so does a process that process starts in turn", nested.stdout.strip() == "below", nested.stdout + nested.stderr)
