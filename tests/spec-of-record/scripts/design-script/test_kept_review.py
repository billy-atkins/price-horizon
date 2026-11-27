"""The kept tests run as a self-review over applied work is validated: --stamp-settled-report runs the design script's
checks over the work and --check-kept-tests over the design's changes, read from version control, writes what both
gave into the report's Script Output, and stamps the report only where no test fails, no check made with the run
reports and the report judges each design a kept comparison lists. Each project is a ferry design applied to the
guide, with the guide's set of kept tests and its own runner, all written as fixtures and committed, then the guide
changed."""
import pytest

from design_script_set import (DESIGN, GUIDE_SET, KEPT_FIXTURES, KEPT_RUN, KEPT_SET_READS, NAME, REPORTS, acted, committed, design_documents as dd, held,
                               kept_set, project)

pytestmark = list(KEPT_SET_READS) + [pytest.mark.reads("design-script-ferry.md", "island-guide"),
                                     pytest.mark.reads("design-script-pages-changed.md", "guide-giving-the-first-ferry")]
SELF = REPORTS + "/self-review/1.md"
COMPARISON = GUIDE_SET + "/comparison.py"
OTHER_DESIGN = ".ai/plans/design-specs/other-design.md"
SEARCH_INDEX = ".ai/tmp/search-spec-of-record-scope/"
RAN = "$ --check-kept-tests\nthe kept tests of guide, run for docs/guide.md\n$ python -B -m pytest " + GUIDE_SET + "/test_guide.py\n  2 tests, %d failed\n"
FAILS = "%s/test_guide.py holds a test that fails: scripts.guide.test_guide::test_no_pier_is_named" % GUIDE_SET


def paths(skill):
    """-> (where the design stands in a skill's plans folder, where its first self-review's report stands)."""
    return ".ai/plans/%s/%s.md" % (skill, NAME), ".ai/tmp/%s/%s/reports/self-review/1.md" % (skill, NAME)


def applied(work, fixtures, tests="guide-set-tests", design="ferry-design-applying", before=None, after=None, report="ferry-self-review-report",
            skill="design-specs"):
    """-> the root of a project holding the guide's set of kept tests, its file of tests the fixture `tests` names, the
    guide and the design given in the skill's plans folder, with what before maps, committed; then the guide giving
    the first ferry, the self-review's report given, and what after maps."""
    at, report_at = paths(skill)
    root = committed(kept_set(work, fixtures, dict({"island-guide": "docs/guide.md", design: at}, **(before or {})), tests=tests))
    project(work, fixtures, dict({"guide-giving-the-first-ferry": "docs/guide.md", report: report_at}, **(after or {})))
    return root


def stamped(monkeypatch, root, skill="design-specs"):
    """-> (the exit status of --stamp-settled-report of the self-review, the report's text after it)."""
    report_at = paths(skill)[1]
    code = acted(monkeypatch, root, dd.stamp_settled_report, report_at, plans=".ai/plans/" + skill)
    return code, (root / report_at).read_text(encoding="utf-8")


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("skill", ["design-specs", "implement-specs"])
def test_report_is_stamped_where_the_kept_tests_pass_their_output_and_the_works_in_it(fixtures, work, monkeypatch, skill):
    code, text = stamped(monkeypatch, applied(work, fixtures, skill=skill), skill)
    assert code == 0 and dd.report_stamp(text) is not None
    assert "$ --check-work %s\n== check-work %s\n\n0 findings new against the last commit, over 1 changed file\n" % (paths(skill)[0], NAME) in text
    assert RAN % 0 in text and "the checks of tests/spec-of-record as a whole were made\n" in text
    assert text.index("$ --check-changed-files") < text.index("$ --check-kept-tests") < text.index("## Settlement")


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_report_is_not_stamped_where_a_kept_test_fails_the_tests_result_in_it(fixtures, work, monkeypatch, capsys):
    root = applied(work, fixtures, tests="guide-set-tests-one-failing")
    before = (root / DESIGN).read_bytes()
    code, text = stamped(monkeypatch, root)
    out = capsys.readouterr().out
    assert code == 1 and "== stamp-settled-report, not stamped " + SELF in out and "%s: %s" % (SELF, FAILS) in out and dd.KEPT_TESTS_RULE in out
    assert dd.report_stamp(text) is None and RAN % 1 + "  FAILED scripts.guide.test_guide::test_no_pier_is_named\n" in text
    assert (root / DESIGN).read_bytes() == before


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-holding-no-test-where-it-reports")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.parametrize("tests, after, said", [
    ("guide-set-tests-holding-no-test-where-it-reports", {}, "the action --show-guide of guide is held by no kept test where it reports"),
    ("guide-set-tests", {"notes-citing-nothing": KEPT_FIXTURES + "/notes/agents.md"}, KEPT_FIXTURES + "/notes/agents.md carries the name of an agent instructions file"),
])
def test_report_is_not_stamped_where_a_check_made_with_the_run_reports(fixtures, work, monkeypatch, capsys, tests, after, said):
    code, text = stamped(monkeypatch, applied(work, fixtures, tests=tests, after=after))
    assert code == 1 and "%s: %s" % (SELF, said) in capsys.readouterr().out and dd.report_stamp(text) is None


@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-to-the-guide-and-the-tides")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.reads("design-script-pages.md", "spring-tides-page")
def test_no_kept_test_is_run_where_the_designs_changes_hold_no_file_of_a_script(fixtures, work, monkeypatch):
    root = applied(work, fixtures, tests="guide-set-tests-one-failing", design="ferry-design-applying-to-the-guide-and-the-tides",
                   after={"island-guide": "docs/guide.md", "spring-tides-page": "docs/tides/spring.md"})
    code, text = stamped(monkeypatch, root)
    assert code == 0 and "$ --check-kept-tests\nno changed file is a file of a script holding kept tests\n" in text and "test_guide" not in text


@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-before-approval")
def test_self_review_before_the_apply_runs_no_kept_test(fixtures, work, monkeypatch):
    root = applied(work, fixtures, tests="guide-set-tests-one-failing", design="ferry-design-drafted", report="ferry-self-review-before-approval")
    code, text = stamped(monkeypatch, root)
    assert code == 0 and "check-kept-tests" not in text


@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-one-failing")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_report_checked_apart_runs_no_kept_test_and_writes_nothing(fixtures, work, monkeypatch, capsys):
    root = applied(work, fixtures, tests="guide-set-tests-one-failing")
    before = held(root)
    assert acted(monkeypatch, root, dd.check_settled_report, SELF) == 0
    assert "test_guide" not in capsys.readouterr().out and not (root / KEPT_RUN).exists()
    # the search the checks read through keeps its index among the working files, and nothing else is written
    assert {p: b for p, b in held(root).items() if not p.startswith(SEARCH_INDEX)} == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "comparison-listing-one-design")
@pytest.mark.reads("design-script-kept-runs.md", "ferry-self-review-report-judging-the-other-design", "ferry-self-review-report-judging-its-own-design")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("report, said", [
    ("ferry-self-review-report", "no Builder Check of differential test, which is required of it"),
    ("ferry-self-review-report-judging-its-own-design", "its Builder Checks of differential test leave out `%s`" % OTHER_DESIGN),
    ("ferry-self-review-report-judging-the-other-design", None),
])
def test_self_review_judges_each_design_the_kept_comparison_lists(fixtures, work, monkeypatch, capsys, report, said):
    root = applied(work, fixtures, before={"comparison-listing-one-design": COMPARISON}, report=report)
    code, text = stamped(monkeypatch, root)
    assert "$ python -B %s\ndesign %s\n" % (COMPARISON, OTHER_DESIGN) in text
    assert (code, dd.report_stamp(text) is None) == ((1, True) if said else (0, False))
    assert said is None or said in capsys.readouterr().out


@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "comparison-that-cannot-be-made", "comparison-listing-no-design")
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("comparison, code, said", [
    ("comparison-that-cannot-be-made", 1, "%s could not be made, exit 2" % COMPARISON),
    ("comparison-listing-no-design", 0, "0 designs read differently, of 1"),
])
def test_comparison_made_or_not_is_written_and_asks_no_judgment_where_it_lists_none(fixtures, work, monkeypatch, capsys, comparison, code, said):
    got, text = stamped(monkeypatch, applied(work, fixtures, before={comparison: COMPARISON}))
    assert got == code and said in (capsys.readouterr().out if code else text)
