"""--check-kept-tests: the kept tests of each script a set of changed files holds a file of, and its kept comparison,
run in a project of fixtures by that project's own runner, each result read from the run's report; and the units of a
run, each held by calling it: the sets read from their files, what the runner gives of each test it finds, the run's
report read and held to the registered schema, and the run leaving the machine to the person using it."""
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

from design_script_set import (GUIDE_SET, GUIDE_TESTS, KEPT, KEPT_FIXTURES, KEPT_RUN, KEPT_SET_READS, acted, committed, design_documents as dd,
                               held, kept_set, project, spec_text)

pytestmark = list(KEPT_SET_READS)
TIDES = {"tides-script": "tools/tides.py", "tides-set-conftest": KEPT + "/scripts/tides/conftest.py",
         "tides-set-tests": KEPT + "/scripts/tides/test_tides.py"}
COMPARISON = GUIDE_SET + "/comparison.py"
OTHER_DESIGN = ".ai/plans/design-specs/other-design.md"
FAILED = "scripts.guide.test_guide::test_no_pier_is_named"


def ran_for(output):
    """-> {a script: the changed files its kept tests were run for} of what a run gave."""
    return dict(line[len("the kept tests of "):].split(", run for ", 1) for line in output.split("\n") if line.startswith("the kept tests of "))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "tides-script", "tides-set-conftest", "tides-set-tests")
@pytest.mark.parametrize("changed, run", [
    (["docs/guide.md"], {"guide": "docs/guide.md"}),
    (["tools/tides.py", "docs/notes.md"], {"tides": "tools/tides.py"}),
    ([KEPT_FIXTURES + "/guide.md"], {"guide": KEPT_FIXTURES + "/guide.md"}),
    ([KEPT + "/scripts/tides/test_tides.py"], {"tides": KEPT + "/scripts/tides/test_tides.py"}),
    ([KEPT + "/pytest.ini"], {"guide": KEPT + "/pytest.ini", "tides": KEPT + "/pytest.ini"}),
    ([KEPT_FIXTURES + "/index.md"], {}),
])
def test_tests_of_each_script_a_change_holds_a_file_of_are_run_and_no_others(fixtures, work, changed, run):
    output, problems, listed = dd.kept_tests_run(kept_set(work, fixtures, TIDES), changed)
    assert problems == [] and listed is None
    assert ran_for(output) == run
    assert "the checks of %s as a whole were made\n" % KEPT in output
    assert output.count("  2 tests, 0 failed\n") == len(run)


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill")
@pytest.mark.parametrize("changed, said", [
    (["docs/notes.md", ".ai/skills/bake-bread/scripts/bake-bread.py"], "no set of kept tests names .ai/skills/bake-bread/scripts/bake-bread.py\n"),
    (["docs/notes.md"], "no changed file is a file of a script holding kept tests\n"),
])
def test_change_holding_no_file_of_a_set_runs_no_test_and_says_so(fixtures, work, changed, said):
    root = kept_set(work, fixtures, {"registry-of-one-skill": "specs/methodology/skills/registered-skills.md"})
    output, problems, _ = dd.kept_tests_run(root, changed)
    assert output == said and problems == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
def test_failing_test_is_named_with_what_it_reported_from_the_report(fixtures, work):
    output, problems, _ = dd.kept_tests_run(kept_set(work, fixtures, tests="guide-set-tests-one-failing"), ["docs/guide.md"])
    assert "  2 tests, 1 failed\n  FAILED %s\n" % FAILED in output and "two and two make four" in output
    assert "test_the_quay_is_named" not in output
    assert problems == [(dd.KEPT_TESTS_RULE, "%s holds a test that fails: %s" % (GUIDE_TESTS, FAILED))]


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-ferry.md", "island-guide")
@pytest.mark.reads("design-script-pages.md", "walkers-notes")
@pytest.mark.parametrize("changes, code, said", [
    ({}, 0, "== check-kept-tests, over 0 changed files\n"),
    ({"walkers-notes": ".ai/tmp/notes.md"}, 0, "== check-kept-tests, over 0 changed files\n"),
    ({"island-guide": "docs/guide.md"}, 1, "the kept tests of guide, run for docs/guide.md\n"),
    ({"island-guide": "docs/guide.md", "guide-set-tests": GUIDE_TESTS}, 0, "the kept tests of guide, run for docs/guide.md, %s\n" % GUIDE_TESTS),
])
def test_given_no_file_the_files_changed_against_the_last_commit_are_read_the_working_files_aside(fixtures, work, monkeypatch, capsys, changes, code, said):
    root = committed(kept_set(work, fixtures, tests="guide-set-tests-one-failing"))
    project(work, fixtures, changes)
    assert acted(monkeypatch, root, dd.check_kept_tests, []) == code
    assert said in capsys.readouterr().out


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "test-ending-its-process", "test-recording-a-property")
@pytest.mark.parametrize("more, said", [
    ("test-ending-its-process", "the run left no report at report.xml, exit 3"),
    ("test-recording-a-property", "the run's report is out of the registered schema: testcase holds properties, which the schema does not declare within it, exit 0"),
])
def test_file_whose_run_leaves_no_report_in_the_schema_could_not_be_run(fixtures, work, more, said):
    root = kept_set(work, fixtures, {more: GUIDE_SET + "/test_more.py"})
    output, problems, _ = dd.kept_tests_run(root, ["docs/guide.md"])
    assert problems == [(dd.KEPT_REPORT_RULE, "%s/test_more.py could not be run: %s" % (GUIDE_SET, said))]
    assert "  2 tests, 0 failed\n" in output


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
def test_run_leaves_one_report_in_the_registered_schema_holding_each_test_with_its_time(fixtures, work):
    root = kept_set(work, fixtures, tests="guide-set-tests-one-failing")
    dd.kept_tests_run(root, ["docs/guide.md"])
    report = ET.parse(root / KEPT_RUN / "report.xml").getroot()
    assert dd.junit_problems(report) == []
    assert [case.attrib["name"] for case in report.iter("testcase")] == ["test_the_quay_is_named", "test_no_pier_is_named"]
    assert all(float(case.attrib["time"]) >= 0 for case in report.iter("testcase")) and len(list(report.iter("failure"))) == 1


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-pages.md", "walkers-notes")
@pytest.mark.parametrize("tests", ["guide-set-tests", "guide-set-tests-one-failing"])
def test_run_writes_within_its_folder_and_leaves_its_report_there_alone(fixtures, work, tests):
    # what a run cut off left in the run's folder, which the next run clears as it starts
    root = kept_set(work, fixtures, {"walkers-notes": KEPT_RUN + "/work/cut-off/notes.md"}, tests=tests)
    before = {path: text for path, text in held(root).items() if not path.startswith(KEPT_RUN + "/")}
    dd.kept_tests_run(root, ["docs/guide.md"])
    assert {path: text for path, text in held(root).items() if not path.startswith(KEPT_RUN + "/")} == before
    assert sorted(p.name for p in (root / KEPT_RUN).iterdir()) == ["report.xml"]


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "comparison-listing-one-design")
def test_comparison_is_run_beside_the_tests_and_fails_nothing_for_what_it_lists(fixtures, work, monkeypatch, capsys):
    root = kept_set(work, fixtures, {"comparison-listing-one-design": COMPARISON})
    assert acted(monkeypatch, root, dd.check_kept_tests, ["tools/guide.py"]) == 0
    out = capsys.readouterr().out
    assert "$ python -B %s\ndesign %s\n\n1 design read differently, of 1\nexit 0\n" % (COMPARISON, OTHER_DESIGN) in out
    assert out.index("$ python -B -m pytest " + GUIDE_TESTS) < out.index("$ python -B " + COMPARISON) and "\n0 problems\n" in out


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "comparison-listing-one-design", "tides-script", "tides-set-conftest", "tides-set-tests")
@pytest.mark.parametrize("changed, listed", [(["tools/guide.py"], [OTHER_DESIGN]), (["tools/tides.py"], None)])
def test_comparison_is_run_where_a_file_of_its_script_changed_and_lists_its_designs(fixtures, work, changed, listed):
    root = kept_set(work, fixtures, dict(TIDES, **{"comparison-listing-one-design": COMPARISON}))
    output, problems, got = dd.kept_tests_run(root, changed)
    assert got == listed and problems == [] and ("comparison" in output) == bool(listed)


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "comparison-that-cannot-be-made")
def test_comparison_that_cannot_be_made_is_reported(fixtures, work):
    root = kept_set(work, fixtures, {"comparison-that-cannot-be-made": COMPARISON})
    _, problems, listed = dd.kept_tests_run(root, ["tools/guide.py"])
    assert problems == [(dd.KEPT_TESTS_RULE, "%s could not be made, exit 2" % COMPARISON)] and listed is None


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "test-standing-in")
@pytest.mark.reads("design-script-kept-runs.md", "ledger-set-conftest-naming-its-code-as-one-path", "tests-file-holding-no-test", "tests-file-of-no-python")
@pytest.mark.parametrize("placed, left_out, said", [
    ({"ledger-set-conftest-naming-its-code-as-one-path": KEPT + "/scripts/ledger/conftest.py", "test-standing-in": KEPT + "/scripts/ledger/test_ledger.py"}, (),
     KEPT + "/scripts/ledger cannot be run: its conftest.py names no SCRIPT_FILES as a tuple of paths at its top level"),
    ({}, ("guide-set-tests",), GUIDE_SET + " holds no file of tests"),
    ({"tests-file-holding-no-test": GUIDE_SET + "/test_none.py"}, (), GUIDE_SET + "/test_none.py holds no test the runner finds"),
    ({"tests-file-of-no-python": GUIDE_SET + "/test_broken.py"}, (), "the runner could not find the kept tests, exit 2"),
])
def test_set_that_cannot_be_run_is_reported(fixtures, work, placed, left_out, said):
    _, problems, _ = dd.kept_tests_run(kept_set(work, fixtures, placed, left_out=left_out), ["docs/guide.md"])
    assert [msg for rule, msg in problems if rule == dd.KEPT_TESTS_RULE and msg.startswith(said)]


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "comparison-listing-one-design")
def test_set_is_read_from_its_files_never_run(fixtures, work):
    root = kept_set(work, fixtures, {"comparison-listing-one-design": COMPARISON})
    assert dd.kept_scripts(root) == [{"script": "guide", "folder": GUIDE_SET, "files": ("tools/guide.py", "docs/guide.md"), "actions_in": "tools/guide.py",
                                      "why": None, "tests": [GUIDE_TESTS], "comparison": COMPARISON}]
    assert not (root / KEPT_RUN).exists()


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "test-standing-in")
@pytest.mark.reads("design-script-kept-runs.md", "ledger-set-conftest-naming-its-code-as-one-path")
def test_set_naming_its_code_as_one_path_cannot_be_read(fixtures, work):
    root = kept_set(work, fixtures, {"ledger-set-conftest-naming-its-code-as-one-path": KEPT + "/scripts/ledger/conftest.py",
                                     "test-standing-in": KEPT + "/scripts/ledger/test_ledger.py"})
    ledger = next(one for one in dd.kept_scripts(root) if one["script"] == "ledger")
    assert ledger["files"] is None and ledger["why"] == "its conftest.py names no SCRIPT_FILES as a tuple of paths at its top level"


@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "comparison-listing-one-design")
def test_runner_gives_what_each_test_names_and_runs_none(fixtures, work):
    root = kept_set(work, fixtures, {"comparison-listing-one-design": COMPARISON})
    rows, why = dd.kept_links(root, root / KEPT_RUN)
    assert why is None and rows == [
        {"test": "scripts/guide/test_guide.py::test_the_quay_is_named", "file": GUIDE_TESTS, "actions": ["--show-guide"], "script_checks": [],
         "ways": {"passes": []}, "reads": [["guide.md", "quay-line"]]},
        {"test": "scripts/guide/test_guide.py::test_no_pier_is_named", "file": GUIDE_TESTS, "actions": ["--show-guide"], "script_checks": [],
         "ways": {"reports": []}, "reads": []}]
    assert not list((root / KEPT_RUN).rglob("report.xml"))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "tests-file-of-no-python")
def test_runner_that_cannot_find_the_tests_says_why(fixtures, work):
    root = kept_set(work, fixtures, {"tests-file-of-no-python": GUIDE_SET + "/test_broken.py"})
    rows, why = dd.kept_links(root, root / KEPT_RUN)
    assert rows is None and why.startswith("the runner could not find the kept tests, exit 2: ")


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "kept-report-of-two-tests")
def test_report_is_read_test_by_test(fixtures, work):
    cases, root = dd.read_kept_report(project(work, fixtures, {"kept-report-of-two-tests": "report.xml"}) / "report.xml")
    assert root.tag == "testsuites" and cases == [
        {"test": "scripts.guide.test_guide::test_the_quay_is_named", "said": "", "time": "0.010", "outcome": "passed"},
        {"test": FAILED, "said": "AssertionError: two and two make four", "time": "0.030", "outcome": "failed"}]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "kept-report-that-is-no-xml", "kept-report-holding-an-undeclared-attribute")
@pytest.mark.parametrize("report, why", [
    (None, "the run left no report at report.xml"),
    ("kept-report-that-is-no-xml", "the run's report is no XML: "),
    ("kept-report-holding-an-undeclared-attribute", "the run's report is out of the registered schema: testcase holds the attribute ferry, which the schema does not declare of it"),
])
def test_report_not_standing_no_xml_or_out_of_the_schema_is_not_read(fixtures, work, report, why):
    root = project(work, fixtures, {report: "report.xml"} if report else {})
    cases, said = dd.read_kept_report(root / "report.xml")
    assert cases is None and said.startswith(why)


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "kept-report-of-two-tests", "kept-report-holding-an-undeclared-attribute",
                   "kept-report-holding-an-undeclared-element", "kept-report-of-a-test-lacking-its-name")
@pytest.mark.parametrize("report, problems", [
    ("kept-report-of-two-tests", []),
    ("kept-report-holding-an-undeclared-attribute", ["testcase holds the attribute ferry, which the schema does not declare of it"]),
    ("kept-report-holding-an-undeclared-element", ["testcase holds crossing, which the schema does not declare within it"]),
    ("kept-report-of-a-test-lacking-its-name", ["testcase lacks the attribute name"]),
])
def test_report_is_held_to_the_registered_schema(fixtures, report, problems):
    assert dd.junit_problems(ET.fromstring(fixtures[report].split("?>", 1)[1])) == problems


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--show-kept-test-times")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "kept-report-of-two-tests")
def test_times_of_the_last_run_are_shown_the_slowest_first(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"kept-report-of-two-tests": KEPT_RUN + "/report.xml"})
    assert acted(monkeypatch, root, dd.show_kept_test_times, None) == 0
    assert capsys.readouterr().out == ("== show-kept-test-times, 2 tests\n    0.03 s  failed  %s\n"
                                       "    0.01 s  passed  scripts.guide.test_guide::test_the_quay_is_named\n\n" % FAILED)


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--show-kept-test-times")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "kept-report-that-is-no-xml", "kept-report-holding-an-undeclared-attribute")
@pytest.mark.parametrize("report, said", [
    (None, "the run left no report at report.xml"),
    ("kept-report-holding-an-undeclared-attribute", "the run's report is out of the registered schema: testcase holds the attribute ferry"),
    ("kept-report-that-is-no-xml", "the run's report is no XML"),
])
def test_times_are_refused_where_no_report_in_the_schema_stands(fixtures, work, monkeypatch, capsys, report, said):
    root = project(work, fixtures, {report: KEPT_RUN + "/report.xml"} if report else {})
    assert acted(monkeypatch, root, dd.show_kept_test_times, None) == 2
    assert "--show-kept-test-times reads %s/report.xml: %s" % (KEPT_RUN, said) in capsys.readouterr().err


# what a process prints of its own priority, setting none: on Windows its priority class, elsewhere how far it is niced
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


@pytest.mark.action("--check-kept-tests")
def test_run_stands_below_the_priority_of_a_persons_own_work_and_so_does_each_process_it_starts():
    assert spec_text.yield_the_machine() is True
    started = subprocess.run([sys.executable, "-c", OWN_PRIORITY], capture_output=True, text=True)
    assert started.stdout.strip() == "below", started.stdout + started.stderr
