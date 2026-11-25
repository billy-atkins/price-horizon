"""The kept tests run as the entry of a self-review over applied work is appended: --log-entry runs --check-kept-tests
over the design's changes, writes what the run gave into the report, and refuses the entry where a test fails, a check
made with the run reports, or the report judges no design a kept comparison lists.

A self-review over applied work also runs --check-work, the audit's checks, which read the canon whole. So a project
here holds the whole of what FORM_FILES names, the methodology among it, taken as the test runs. It holds the guide's
set of kept tests, as test_kept.py's projects do.
"""
import pytest

from design_script_set import (APPLYING, CHECK_FIELDS, DRAFTED, FORM_FILES, GUIDE_SET, GUIDE_TESTS, KEPT, KEPT_RULE, NAME, OTHER_DESIGN, Project,
    RE_EVALUATION, SELF, SKILLS, a_check, a_report, applied, failing, kept_tests, passes, report_at, reports, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"), pytest.mark.reads("design-script-reports.md", "ferry-self-review-report"),
              pytest.mark.reads("design-script-kept-sets.md", "guide-script", "guide-set-conftest", "guide-set-tests", "fixture-file-of-one-line", "index-listing-one-file")]
RAN = "$ --check-kept-tests\nthe kept tests of guide, run for %s\n$ python -B -m pytest " + GUIDE_TESTS + "\n  2 tests, %d failed\n"
FAILS = "%s holds a test that fails: scripts.guide.test_guide::test_no_pier_is_named" % GUIDE_TESTS
AUDIT_SCRIPT = ".ai/skills/audit-specs/scripts/audit-specs.py"  # a script of a registered skill, which no set of the project names


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
def test_entry_is_appended_where_the_kept_tests_pass(check):
    for skill in SKILLS:
        p = Project("kept-pass", canon=FORM_FILES)
        kept_tests(p)
        design, path = applied(p, skill, Target="`docs/guide.md`")
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s runs the kept tests of a script whose form the design's changes hold, a change to a form alone, writes what the run gave into the report, and appends the entry" % skill,
              passes(got, "== log-entry", "- **Entry:** self-review-1") and RAN % ("docs/guide.md", 0) in now and "the checks of %s as a whole were made\n" % KEPT in now
              and now.index("$ --check-changed-files") < now.index("$ --check-kept-tests") < now.index("## Settlement"), shown(got) + now[-900:])
    p = Project("kept-code", canon=FORM_FILES)
    kept_tests(p)
    design, path = applied(p, log=APPLYING + (("direct-edit", {"Places": "tools/guide.py"}),), Target="`docs/notes.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry runs them where the design's changes hold the script's code", passes(got, "== log-entry", "- **Entry:** self-review-1") and RAN % ("tools/guide.py", 0) in p.read(path), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
def test_entry_is_refused_where_a_kept_test_fails(check, fixtures):
    for skill in SKILLS:
        p = Project("kept-fail", canon=FORM_FILES)
        kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
        design, path = applied(p, skill, Target="`docs/guide.md`")
        before = p.read(design)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s refuses the entry of a self-review over applied work where a kept test of a script the design changed fails, the tests' result written into its report" % skill,
              reports(got, "== log-entry, not logged", ["%s: %s" % (path, FAILS), KEPT_RULE]) and p.read(design) == before
              and RAN % ("docs/guide.md", 1) + "  FAILED scripts.guide.test_guide::test_no_pier_is_named\n" in now, shown(got) + now[-700:])
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s, made apart from the entry, runs no kept test: it passes the same report and names none" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and "test_guide" not in got[1], shown(got))
    p = Project("kept-before-the-apply")
    kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
    design = p.design(log=DRAFTED)
    path = p.put(report_at(SELF), a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry runs no kept test for a self-review before the apply", passes(got, "== log-entry", "- **Entry:** self-review-1") and "check-kept-tests" not in p.read(path), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
def test_entry_is_refused_where_a_check_made_with_the_run_reports(check, fixtures):
    p = Project("kept-check-reports", canon=FORM_FILES)
    # the kept tests pass, and no test holds the script's one action where it reports
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.reports\n", ""))
    design, path = applied(p, Target="`docs/guide.md`")
    before = p.read(design)
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry of a self-review over applied work where the kept tests pass and a check made with their run reports: an action no test holds where it reports",
          reports(got, "== log-entry, not logged", ["%s: the action --show-guide of guide is held by no kept test where it reports" % path, "[Name: each-script-check-and-action-held-by-a-test]"])
          and p.read(design) == before and RAN % ("docs/guide.md", 0) in p.read(path), shown(got))
    p = Project("kept-folder-reports", canon=FORM_FILES)
    kept_tests(p)
    p.put(GUIDE_SET + "/AGENTS.md", fixtures["island-guide"])  # a file kept under the tests under the name of an agent instructions file
    # the design changed a file under the tests alone, none a set names as its script's: no test is run, and the folder is checked
    design, path = applied(p, Target="`%s/fixtures/index.md`" % KEPT, Kind="canon-specs")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry where the design's changes hold a file under the tests and a check of the tests' folder reports, though no test is run",
          reports(got, "== log-entry, not logged", ["%s/AGENTS.md carries the name of an agent instructions file" % GUIDE_SET, "[Name: no-instructions-name-kept-under-the-tests]"])
          and "$ --check-kept-tests\nthe checks of %s as a whole were made\n" % KEPT in p.read(path), shown(got) + p.read(path)[-500:])


@pytest.mark.action("--log-entry")
def test_no_kept_test_is_run_where_no_file_of_a_script_changed(check, fixtures):
    p = Project("kept-none", canon=FORM_FILES)
    kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
    design, path = applied(p, log=APPLYING + (("direct-edit", {"Places": AUDIT_SCRIPT}),), Target="`docs/notes.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    now = p.read(path)
    check("--log-entry runs no kept test of a script none of whose files the design changed, says which changed script no set of kept tests names, and appends the entry",
          passes(got, "== log-entry", "- **Entry:** self-review-1") and "$ --check-kept-tests\nno set of kept tests names %s\n" % AUDIT_SCRIPT in now and "test_guide" not in now, shown(got) + now[-400:])


@pytest.mark.action("--log-entry")
def test_pass_proving_the_fixes_runs_the_kept_tests_too(check, fixtures):
    p = Project("kept-pass-of-the-fixes", canon=FORM_FILES)
    kept_tests(p, tests=failing(fixtures["guide-set-tests"]))
    design = p.design(status="applying", log=APPLYING + ((SELF, {}), ("post-apply-review", {})), Target="`docs/guide.md`")
    path = p.put(report_at(SELF, 2), swap(a_report("self-review", entry="self-review-2"), RE_EVALUATION, ""))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry of a pass proving the fixes, a self-review after the apply's review, where a kept test fails",
          reports(got, "== log-entry, not logged", [FAILS, KEPT_RULE]), shown(got))
    p.put(GUIDE_TESTS, fixtures["guide-set-tests"])
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("and appends it where they pass", passes(got, "== log-entry", "- **Entry:** self-review-2") and RAN % ("docs/guide.md", 0) in p.read(path), shown(got))


@pytest.mark.action("--log-entry")
@pytest.mark.reads("design-script-kept-sets.md", "comparison-listing-one-design")
def test_self_review_judges_each_design_a_comparison_lists(check, fixtures):
    comparison, lists = GUIDE_SET + "/comparison.py", fixtures["comparison-listing-one-design"]
    judged = a_check("comparison-judged", "differential test", OTHER_DESIGN)
    for label, checks, said in (("recording no differential test", (), "no Builder Check of differential test, which is required of it"),
                                ("whose differential test leaves out a design the comparison lists", (a_check("comparison-judged", "differential test", ".ai/plans/design-specs/%s.md" % NAME),),
                                 "its Builder Checks of differential test leave out `%s`" % OTHER_DESIGN),
                                ("whose differential test judges each design the comparison lists", (judged,), None)):
        p = Project("kept-comparison", canon=FORM_FILES)
        kept_tests(p, comparison=lists)
        design, path = applied(p, checks=checks, Target="`docs/guide.md`")
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        if said:
            check("--log-entry runs the kept comparison of a script the design changed, and refuses the entry of a self-review " + label,
                  reports(got, "== log-entry, not logged", said) and "$ python -B %s\ndesign %s\n" % (comparison, OTHER_DESIGN) in p.read(path), shown(got) + p.read(path)[-500:])
        else:
            check("--log-entry appends the entry of a self-review " + label, passes(got, "== log-entry", "- **Entry:** self-review-1") and "design " + OTHER_DESIGN in p.read(path), shown(got))
    p = Project("kept-comparison-failed", canon=FORM_FILES)
    kept_tests(p, comparison=lists + "raise SystemExit(2)\n")  # the comparison ending as one that could not be made
    design, path = applied(p, Target="`docs/guide.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry where the comparison could not be made", reports(got, "== log-entry, not logged", ["%s could not be made, exit 2" % comparison, KEPT_RULE]), shown(got))
    p = Project("kept-comparison-lists-none", canon=FORM_FILES)
    kept_tests(p, comparison=swap(swap(lists, "print(\"design %s\")\n" % OTHER_DESIGN, ""), "1 design read differently, of 1", "0 designs read differently, of 1"))
    design, path = applied(p, Target="`docs/guide.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry asks no differential test where the comparison lists no design", passes(got, "== log-entry", "- **Entry:** self-review-1") and "0 designs read differently" in p.read(path), shown(got))
