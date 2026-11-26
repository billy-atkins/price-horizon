"""A design's research, and the log's gates on a check's entry: each place read lying in an assessed area, an area
assessed again naming its cause, the goals agreed before any check, an entry standing at the version its report read,
an audit's sub-scopes, and the research binding a design read together, each action called over a project of
fixtures."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]
RESEARCH, SECOND = REPORTS + "/handed-off-judgment/1.md", REPORTS + "/handed-off-judgment/2.md"
AUDIT, SELF = REPORTS + "/audit-specs/1.md", REPORTS + "/self-review/1.md"
JUDGMENT = [DESIGN, "handed-off-judgment", "Model=a model", "Effort=medium"]
AUDITED = [DESIGN, "audit-specs", "Model=a model", "Effort=medium", "Led To=validating"]
FERRY, LIGHTHOUSE = "`docs/guide.md § The Ferry`", "`docs/guide.md § The Lighthouse`"
HANDED = [(dd.check_handed_back, "== check-handed-back "), (dd.take_up_report, "== take-up-report, not taken up ")]
# what a design's validation reads of research whose Search holds a place no Area covers and whose goal no Search by
# terms names
UNCOVERED = ("Search ferry-times-by-meaning of %s holds %s, which no binding research report's Read Assessment's Area covers" % (RESEARCH, LIGHTHOUSE),
             "the goal guide-says-when-the-ferry-runs is named by no Search by terms of the operative files naming no commit, among the research binding the design")


def researched(work, fixtures, design, **placed):
    """-> the root of a project holding the guide, the design given and the reports given at their paths."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, **placed})


def unchanged(root, monkeypatch, action, value, code=1):
    """Hold that an action exits as given and writes nothing."""
    before = held(root)
    assert acted(monkeypatch, root, action, value) == code
    assert held(root) == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-researched.md", "research-handed-back-reading-the-lighthouse")
@pytest.mark.parametrize("action, heading", HANDED)
def test_read_lying_in_no_assessed_area_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    root = researched(work, fixtures, "ferry-design-drafted", **{"research-handed-back-reading-the-lighthouse": RESEARCH})
    unchanged(root, monkeypatch, action, RESEARCH)
    out = capsys.readouterr().out
    assert heading + RESEARCH in out and "%s, a place its Reads hold, lies within no Read Assessment's Area" % LIGHTHOUSE in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]
@pytest.mark.action("--check-handed-back")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-researched.md", "research-handed-back-reading-the-design")
def test_reads_each_in_an_assessed_area_the_design_aside_pass(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, "ferry-design-drafted", **{"research-handed-back-reading-the-design": RESEARCH})
    assert acted(monkeypatch, root, dd.check_handed_back, RESEARCH) == 0
    assert "== check-handed-back %s\n0 problems" % RESEARCH in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-handed-back")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-researched.md", "research-handed-back-its-impact-none-beside-changes", "research-handed-back-naming-a-goal-not-held")
@pytest.mark.parametrize("report, said", [
    ("research-handed-back-its-impact-none-beside-changes", "Impact is not a list holding none alone"),
    ("research-handed-back-naming-a-goal-not-held", "Goals name guide-says-what-the-ferry-costs, which is no design goal's Name"),
])
def test_read_assessment_out_of_its_form_is_reported(fixtures, work, monkeypatch, capsys, report, said):
    root = researched(work, fixtures, "ferry-design-drafted", **{report: RESEARCH})
    unchanged(root, monkeypatch, dd.check_handed_back, RESEARCH)
    assert said in capsys.readouterr().out


def assessed_again(work, fixtures, report, design="ferry-design-agreed-researched"):
    """-> the root of a project whose design's log names its first research report, with a second handed back."""
    return researched(work, fixtures, design, **{"ferry-research-report": RESEARCH, report: SECOND})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.reads("design-script-researched.md", "ferry-design-agreed-researched", "second-research-handed-back-assessing-the-ferry-again")
@pytest.mark.parametrize("action, heading", HANDED)
def test_area_assessed_again_naming_no_cause_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    root = assessed_again(work, fixtures, "second-research-handed-back-assessing-the-ferry-again")
    unchanged(root, monkeypatch, action, SECOND)
    out = capsys.readouterr().out
    assert heading + SECOND in out and "[Name: area-reassessments-name-their-cause]" in out
    assert "Read Assessment %s assesses again an Area %s already assesses, and names no cause in its Assessed Again For" % (FERRY, RESEARCH) in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
@pytest.mark.action("--check-handed-back")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.reads("design-script-researched.md", "ferry-design-agreed-researched", "second-research-handed-back-assessing-the-ferry-again-for-steer-1",
                   "second-research-handed-back-assessing-the-ferry-again-for-a-second-look")
@pytest.mark.parametrize("report, said", [
    ("second-research-handed-back-assessing-the-ferry-again-for-steer-1", "names steer-1, a set's entry the design's log does not hold"),
    ("second-research-handed-back-assessing-the-ferry-again-for-a-second-look", "names a second look, neither a set's steer entry nor a finding cited as a place"),
])
def test_area_assessed_again_for_what_is_no_cause_is_reported(fixtures, work, monkeypatch, capsys, report, said):
    unchanged(assessed_again(work, fixtures, report), monkeypatch, dd.check_handed_back, SECOND)
    assert said in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.reads("design-script-researched.md", "ferry-design-agreed-researched", "ferry-design-agreed-researched-and-steered",
                   "second-research-handed-back-assessing-the-ferry-again-for-steer-1", "second-research-handed-back-assessing-the-lighthouse")
@pytest.mark.parametrize("action, heading", [(dd.check_handed_back, "== check-handed-back "), (dd.take_up_report, "== take-up-report ")])
@pytest.mark.parametrize("design, report", [
    # assessed again for a set of steers logged after the report that assessed it
    ("ferry-design-agreed-researched-and-steered", "second-research-handed-back-assessing-the-ferry-again-for-steer-1"),
    # an Area no binding report assesses asks no cause
    ("ferry-design-agreed-researched", "second-research-handed-back-assessing-the-lighthouse"),
])
def test_area_assessed_again_for_its_cause_or_first_assessed_passes(fixtures, work, monkeypatch, capsys, action, heading, design, report):
    assert acted(monkeypatch, assessed_again(work, fixtures, report, design), action, SECOND) == 0
    assert heading + SECOND + "\n0 problems" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-entered", "research-taken-up")
def test_checks_entry_before_the_goals_agreement_is_refused(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, "ferry-design-entered", **{"research-taken-up": RESEARCH})
    assert acted(monkeypatch, root, dd.stamp_settled_report, RESEARCH) == 0
    unchanged(root, monkeypatch, dd.log_entry, JUDGMENT)
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and "[Name: goals-agreed-before-checks]" in out
    assert "a check's entry with no goals-agreed entry before it in its major version" in out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-researched.md", "ferry-design-entered", "research-taken-up")
def test_checks_entry_once_the_goals_are_agreed_is_appended(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, "ferry-design-entered", **{"research-taken-up": RESEARCH})
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "goals-agreed"]) == 0
    assert acted(monkeypatch, root, dd.stamp_settled_report, RESEARCH) == 0
    assert acted(monkeypatch, root, dd.log_entry, JUDGMENT) == 0
    assert "- **Entry:** handed-off-judgment-1" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
@pytest.mark.action("--check-design-form", "--check-design")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-researched-before-its-goals-agreed", "ferry-design-logging-research-at-a-version-never-held")
@pytest.mark.parametrize("action, heading", [(dd.check_design_form, "== check-design-form " + NAME), (dd.check_design, "== check-design " + NAME)])
@pytest.mark.parametrize("design, said, rule", [
    ("ferry-design-researched-before-its-goals-agreed",
     "log entry handed-off-judgment-1 is a check's entry with no goals-agreed entry before it in its major version", "goals-agreed-before-checks"),
    ("ferry-design-logging-research-at-a-version-never-held",
     "log entry handed-off-judgment-1's Design Version is 1.4.0, a version its log never held before it", "entry-at-the-version-read"),
])
def test_log_holding_a_checks_entry_out_of_its_gates_is_reported(fixtures, work, monkeypatch, capsys, action, heading, design, said, rule):
    unchanged(researched(work, fixtures, design), monkeypatch, action, DESIGN)
    out = capsys.readouterr().out
    assert heading in out and said in out and "[Name: %s]" % rule in out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-researched.md", "research-taken-up")
def test_checks_entry_stands_at_the_version_its_report_read(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, "ferry-design-drafted", **{"research-taken-up": RESEARCH})
    assert acted(monkeypatch, root, dd.stamp_settled_report, RESEARCH) == 0
    assert acted(monkeypatch, root, dd.log_entry, JUDGMENT) == 0
    # an earlier version the log held, the header left at the log's
    assert "**Design Version:** 1.0.0 \\\n    **Model:**" in capsys.readouterr().out
    assert "**Version:** 1.0.1 \\" in (root / DESIGN).read_text(encoding="utf-8")
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-researched.md", "research-taken-up-reading-version-1-4-0")
def test_checks_entry_whose_report_read_a_version_never_held_is_refused(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, "ferry-design-drafted", **{"research-taken-up-reading-version-1-4-0": RESEARCH})
    assert acted(monkeypatch, root, dd.stamp_settled_report, RESEARCH) == 0
    before = (root / DESIGN).read_bytes()
    assert acted(monkeypatch, root, dd.log_entry, JUDGMENT) == 1
    out = capsys.readouterr().out
    assert "Reading holds Design Version 1.4.0, a version the design's log never held" in out and "[Name: entry-at-the-version-read]" in out
    assert (root / DESIGN).read_bytes() == before


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-its-header-at-1-2-0")
def test_header_version_other_than_its_log_gives_is_reported(fixtures, work, monkeypatch, capsys):
    unchanged(researched(work, fixtures, "ferry-design-drafted-its-header-at-1-2-0"), monkeypatch, dd.check_design_form, DESIGN)
    assert "Version is 1.2.0, where its log gives 1.0.1" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
@pytest.mark.action("--check-design-form", "--check-design")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.reads("design-script-researched.md", "ferry-design-applying-audited-in-its-sub-scopes", "ferry-design-applying-audited-in-the-attic")
@pytest.mark.parametrize("action, heading", [(dd.check_design_form, "== check-design-form " + NAME), (dd.check_design, "== check-design " + NAME)])
@pytest.mark.parametrize("design, code, said", [
    ("ferry-design-applying-audited-in-its-sub-scopes", 0, "0 problems"),
    ("ferry-design-applying-audited-in-the-attic", 1,
     "an audit-specs entry's Settled Sub-scopes names the-attic, not one of core-canon, skills, application-specs, documentation, other"),
])
def test_audit_entry_in_a_log_naming_sub_scopes_alone(fixtures, work, monkeypatch, capsys, action, heading, design, code, said):
    assert acted(monkeypatch, researched(work, fixtures, design, **{"ferry-research-report": RESEARCH}), action, DESIGN) == code
    out = capsys.readouterr().out
    assert heading in out and said in out


def audited(work, fixtures, monkeypatch):
    """-> the root of a project holding the design applying to the guide and its audit's report, stamped."""
    root = researched(work, fixtures, "ferry-design-applying", **{"audit-report-finding-nothing": AUDIT})
    assert acted(monkeypatch, root, dd.stamp_settled_report, AUDIT) == 0
    return root


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
@pytest.mark.parametrize("settled, said", [
    ("the-attic", "Settled Sub-scopes names the-attic, not one of"),
    ("core-canon", "the audit-specs entry's Settled Sub-scopes drop documentation, each holding a file the design changed"),
])
def test_audit_entry_naming_no_sub_scope_or_dropping_a_changed_one_is_refused(fixtures, work, monkeypatch, capsys, settled, said):
    root = audited(work, fixtures, monkeypatch)
    unchanged(root, monkeypatch, dd.log_entry, AUDITED + ["Settled Sub-scopes=" + settled])
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and said in out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_audit_entry_keeping_each_changed_sub_scope_is_appended(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, monkeypatch)
    assert acted(monkeypatch, root, dd.log_entry, AUDITED + ["Settled Sub-scopes=core-canon; documentation"]) == 0
    assert "**Settled Sub-scopes:** core-canon; documentation" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.action("--check-design", "--stamp-validation")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-research-report-reading-the-lighthouse")
@pytest.mark.parametrize("action, heading", [(dd.check_design, "== check-design " + NAME), (dd.stamp_validation, "== stamp-validation, not stamped")])
def test_binding_research_leaving_a_place_or_a_goal_out_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    root = researched(work, fixtures, "ferry-design-drafted-researched", **{"ferry-research-report-reading-the-lighthouse": RESEARCH})
    unchanged(root, monkeypatch, action, DESIGN)
    out = capsys.readouterr().out
    assert heading in out and all(s in out for s in UNCOVERED)
    assert "[Name: research-covers-its-matches]" in out and "[Name: goals-searched-over-every-operative-file]" in out


@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-research-report-reading-the-lighthouse")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("action, heading", [(dd.check_settled_report, "== check-settled-report"), (dd.stamp_settled_report, "== stamp-settled-report, not stamped")])
def test_first_builder_check_after_research_reads_the_research(fixtures, work, monkeypatch, capsys, action, heading):
    root = researched(work, fixtures, "ferry-design-drafted-researched", **{"ferry-research-report-reading-the-lighthouse": RESEARCH,
                                                                            "ferry-self-review-report": SELF})
    before = (root / DESIGN).read_bytes()
    assert acted(monkeypatch, root, action, SELF) == 1
    out = capsys.readouterr().out
    assert heading in out and all(s in out for s in UNCOVERED) and (root / DESIGN).read_bytes() == before


@pytest.mark.action("--check-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-approved-researched")
@pytest.mark.reads("design-script-researched.md", "ferry-design-applying-researched", "ferry-design-complete-researched")
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-research-report-reading-the-lighthouse")
@pytest.mark.parametrize("design", ["ferry-design-approved-researched", "ferry-design-applying-researched", "ferry-design-complete-researched"])
def test_research_of_a_design_past_its_approval_is_not_read_again(fixtures, work, monkeypatch, capsys, design):
    root = researched(work, fixtures, design, **{"ferry-research-report-reading-the-lighthouse": RESEARCH})
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 0
    assert "== check-design %s\n0 problems" % NAME in capsys.readouterr().out
