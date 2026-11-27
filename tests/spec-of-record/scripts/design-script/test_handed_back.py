"""A cold agent's report as it is handed back and taken up: --check-handed-back, which holds its part to its form,
and --take-up-report, which writes a fingerprint of each part it wrote, each called over a project of fixtures."""
import re

import pytest

from design_script_set import DESIGN, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")]
REVIEW, RESEARCH = REPORTS + "/adversarial-review/1.md", REPORTS + "/handed-off-judgment/1.md"
FINDING = "reviewer-1-last-crossing-in-winter"
# each way a report out of its form is met: checked as it is handed back, or refused its take-up, writing nothing
MET = [(dd.check_handed_back, "== check-handed-back " + REVIEW), (dd.take_up_report, "== take-up-report, not taken up " + REVIEW)]


def handed_back(work, fixtures, report, at=REVIEW, design="ferry-design-drafted"):
    """-> the root of a project holding the guide, the design drafted and the report given where its cold agent hands
    it back."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, report: at})


def refused(work, fixtures, monkeypatch, capsys, action, heading, report, design="ferry-design-drafted"):
    """-> what an action printed of a report it reports, having held that it exits 1 and writes nothing."""
    root = handed_back(work, fixtures, report, design=design)
    before = held(root)
    assert acted(monkeypatch, root, action, REVIEW) == 1
    out = capsys.readouterr().out
    assert heading in out and held(root) == before
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back")
@pytest.mark.passes
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back", "research-handed-back")
@pytest.mark.parametrize("report, at", [("review-handed-back", REVIEW), ("research-handed-back", RESEARCH)])
def test_cold_part_in_its_form_passes(fixtures, work, monkeypatch, capsys, report, at):
    root = handed_back(work, fixtures, report, at)
    before = held(root)
    assert acted(monkeypatch, root, dd.check_handed_back, at) == 0
    assert "== check-handed-back %s\n0 problems" % at in capsys.readouterr().out and held(root) == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-titled-for-another-entry", "review-handed-back-titled-for-another-design",
                   "review-handed-back-holding-no-reading", "review-handed-back-its-parts-out-of-order", "review-handed-back-holding-a-part-of-no-form",
                   "review-handed-back-its-marked-finding-holding-no-decision", "review-handed-back-its-verdict-out-of-its-values")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-handed-back-titled-for-another-entry", "its title's Entry is adversarial-review-7, not adversarial-review-1"),
    ("review-handed-back-titled-for-another-design", "its title's Design is another-design, not ferry-times-in-the-guide"),
    ("review-handed-back-holding-no-reading", "it holds no Reading part, which its form requires of it"),
    ("review-handed-back-its-parts-out-of-order", "the report gives its parts out of order: its form gives them as Reading, Goal Judgments, Findings, Searches"),
    ("review-handed-back-holding-a-part-of-no-form", "a part the form does not give: Afterthoughts"),
    ("review-handed-back-its-marked-finding-holding-no-decision", "Finding %s holds no Decision, which its form requires where its Verdict is a mark" % FINDING),
    ("review-handed-back-its-verdict-out-of-its-values", "the Verdict field holds a value its closed set does not: a worry"),
])
def test_cold_part_out_of_its_form_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-holding-the-builders-part")
@pytest.mark.parametrize("action, heading", MET)
def test_cold_part_holding_a_part_the_builder_writes_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "review-handed-back-holding-the-builders-part")
    assert "[Name: cold-parts-kept]" in out and "a part its cold agent does not write, the builder's or the design script's: Settlement" in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-its-finding-naming-a-goal-not-held", "review-handed-back-its-marked-finding-naming-nothing")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-handed-back-its-finding-naming-a-goal-not-held",
     "Finding %s's Affected Goals names guide-says-what-the-ferry-costs, which the design ferry-times-in-the-guide does not hold" % FINDING),
    ("review-handed-back-its-marked-finding-naming-nothing",
     "Finding %s, marked a implementation flaw, names no goal, Frame Outcome or step Objective it bears on and cites no rule it breaks" % FINDING),
])
def test_finding_anchored_in_nothing_the_design_holds_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, report)
    assert "§ A Check's Report § Finding" in out and said in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-its-reads-holding-no-citation")
@pytest.mark.parametrize("action, heading", MET)
def test_read_that_is_no_citation_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "review-handed-back-its-reads-holding-no-citation")
    assert "Collecting Reads holds an item that is no citation of a place with its path: the guide" in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-landing-on-a-change-not-cited", "review-handed-back-citing-a-report-no-entry-names")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-handed-back-landing-on-a-change-not-cited", "Finding %s lands on an earlier change not cited with its report: times-by-season" % FINDING),
    ("review-handed-back-citing-a-report-no-entry-names", "in a report no entry of the design's current major version names"),
])
def test_key_naming_no_record_of_a_cited_report_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-its-ranking-part-none", "review-handed-back-its-snapshot-no-code")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-handed-back-its-ranking-part-none", "Search reviewer-1-winter-hours's Ranking Part is none, and its Places hold 1"),
    ("review-handed-back-its-snapshot-no-code", "Search reviewer-1-winter-hours's Snapshot is yesterday, not a snapshot code"),
])
def test_search_out_of_its_form_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back-a-field-line-unbroken", "review-handed-back-no-blank-line-after-a-list")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-handed-back-a-field-line-unbroken", "specs/methodology/modeling-constructs.md § Fields\n"),
    ("review-handed-back-no-blank-line-after-a-list", "specs/methodology/spec-style/markdown.md § Blank Lines\n"),
])
def test_report_laid_out_otherwise_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("action", [dd.check_handed_back, dd.take_up_report])
def test_report_of_no_cold_agent_is_refused(fixtures, work, monkeypatch, capsys, action):
    at = REPORTS + "/self-review/1.md"
    root = handed_back(work, fixtures, "ferry-self-review-report", at)
    before = held(root)
    assert acted(monkeypatch, root, action, at) == 2
    assert "takes a review's or a handed-off judgment's report at its path" in capsys.readouterr().err and held(root) == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--take-up-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-handed-back.md", "review-handed-back", "research-handed-back", "review-handed-back-making-no-search")
@pytest.mark.parametrize("report, at, parts", [
    ("review-handed-back", REVIEW, ("Title", "Reading", "Goal Judgments", "Findings", "Searches")),
    ("research-handed-back", RESEARCH, ("Title", "Reading", "Searches", "Read Assessments")),
    ("review-handed-back-making-no-search", REVIEW, ("Title", "Reading", "Goal Judgments", "Findings")),
])
def test_take_up_writes_each_cold_parts_fingerprint(fixtures, work, monkeypatch, capsys, report, at, parts):
    root = handed_back(work, fixtures, report, at)
    assert acted(monkeypatch, root, dd.take_up_report, at) == 0
    assert "== take-up-report %s\n0 problems" % at in capsys.readouterr().out
    now = (root / at).read_text(encoding="utf-8")
    assert now.startswith(fixtures[report].rstrip("\n") + "\n\n## Hand-back\n\n")
    marks = re.findall(r"^- ([A-Za-z -]+): [0-9a-f]{64}(, \d+ lines)?$", now.split("## Hand-back")[-1], re.M)
    # a part's fingerprint gives its count of lines where the builder may add to the part, a review's Searches
    assert tuple(m[0] for m in marks) == parts and [bool(m[1]) for m in marks] == [at == REVIEW and m[0] == "Searches" for m in marks]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-handed-back")
@pytest.mark.passes
@pytest.mark.reads("design-script-handed-back.md", "goals-all-met",
                   "goals-upheld-failure",
                   "goals-historical-account",
                   "goals-structure")
@pytest.mark.reads("design-script-reports.md", "ferry-design-with-means-for-objective", "ferry-design-with-replaced-goal")
@pytest.mark.parametrize("report, design", [
    ("goals-all-met", "ferry-design-drafted"),
    ("goals-upheld-failure", "ferry-design-drafted"),
    ("goals-historical-account", "ferry-design-with-replaced-goal"),
    ("goals-structure", "ferry-design-with-means-for-objective"),
])
def test_accounts_for_the_goals_read(fixtures, work, monkeypatch, capsys, report, design):
    root = handed_back(work, fixtures, report, design=design)
    assert acted(monkeypatch, root, dd.check_handed_back, REVIEW) == 0
    assert "0 problems" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "goals-missing",
                   "goals-repeated",
                   "goals-stale",
                   "goals-misattributed",
                   "goals-unsubstantiated",
                   "goals-dropped",
                   "goals-different-goal",
                   "goals-structure-with-answers",
                   "goals-future", "goals-unexplained-stop", "goals-before-agreement")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("goals-missing", "holds no goal judgments"),
    ("goals-repeated", "repeated goal judgment"),
    ("goals-stale", "unrecognized goal or wording"),
    ("goals-misattributed", "missing goal judgment"),
    ("goals-unsubstantiated", "needs an upheld design flaw"),
    ("goals-dropped", "needs an upheld design flaw"),
    ("goals-different-goal", "needs an upheld design flaw"),
    ("goals-structure-with-answers", "belong only to a full pre-approval review"),
    ("goals-future", "future design version"),
    ("goals-unexplained-stop", "a structural stop needs a marked finding"),
    ("goals-before-agreement", "a version the log held with agreed goals"),
])
def test_incomplete_goal_evidence_is_refused(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-handed-back.md", "goals-all-met")
@pytest.mark.reads("design-script-reports.md", "ferry-design-with-replaced-goal")
@pytest.mark.parametrize("action, heading", MET)
def test_historical_review_cannot_claim_independent_comparison(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "goals-all-met", "ferry-design-with-replaced-goal")
    assert "Goal Comparison must read reviewer's account only" in out
