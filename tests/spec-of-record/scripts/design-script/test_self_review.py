"""The builder's self-review: the Builder Checks required of it, the script output its stamp writes into it, the
Traces its phase gives it and its reading after a round's change, each action called over a project of fixtures."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("audit-whole-project.md", "project-registry-of-one-skill")]
SELF, SECOND = REPORTS + "/self-review/1.md", REPORTS + "/self-review/2.md"
ROUND = REPORTS + "/adversarial-review/1.md"
REGISTRY = "specs/methodology/skills/registered-skills.md"
ENTRY = [DESIGN, "self-review", "Model=a model", "Effort=medium"]
FERRY, LIGHTHOUSE = "`docs/guide.md § The Ferry`", "`docs/guide.md § The Lighthouse`"
MET = [(dd.check_settled_report, "== check-settled-report " + SELF), (dd.stamp_settled_report, "== stamp-settled-report, not stamped " + SELF)]


def reviewed(work, fixtures, report, design="ferry-design-drafted", at=SELF, guide="island-guide", **more):
    """-> the root of a project holding the guide, the design given and a self-review's report at its place."""
    return project(work, fixtures, {guide: "docs/guide.md", design: DESIGN, report: at, "project-registry-of-one-skill": REGISTRY, **more})


def refused(root, monkeypatch, capsys, action, heading, at=SELF):
    """-> what an action printed of a self-review's report it reports, having held that it exits 1 and changes no
    file but the report, into which a stamp writes the script output and no stamp."""
    before = held(root)
    assert acted(monkeypatch, root, action, at) == 1
    out = capsys.readouterr().out
    after = held(root)
    assert heading.replace(SELF, at) in out and dd.report_stamp((root / at).read_text(encoding="utf-8")) is None
    assert {p: b for p, b in after.items() if p != at} == {p: b for p, b in before.items() if p != at}
    assert action is dd.stamp_settled_report or after == before
    return out


def appended(root, monkeypatch, capsys, at=SELF):
    """-> what appending a self-review's entry printed, its report stamped first."""
    assert acted(monkeypatch, root, dd.stamp_settled_report, at) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    return capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_self_review_holding_each_required_check_passes(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "ferry-self-review-report")
    before = held(root)
    assert acted(monkeypatch, root, dd.check_settled_report, SELF) == 0
    assert "== check-settled-report %s\n0 problems" % SELF in capsys.readouterr().out and held(root) == before


@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_stamp_writes_the_script_output_where_the_form_orders_it(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "ferry-self-review-report")
    assert acted(monkeypatch, root, dd.stamp_settled_report, SELF) == 0
    now = (root / SELF).read_text(encoding="utf-8")
    assert "## Script Output\n\n```text\n$ --check-cited-headings %s\n" % DESIGN in now
    assert "$ --check-target-kind %s\n== check-target-kind %s\n0 problems\n\nexit 0\n" % (DESIGN, NAME) in now
    # a self-review before the apply runs no kept tests
    assert now.index("## Builder Checks") < now.index("## Script Output") < now.index("## Settlement") and "check-kept-tests" not in now


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_self_reviews_entry_is_appended_once_stamped(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "ferry-self-review-report")
    assert "- **Entry:** self-review-1" in appended(root, monkeypatch, capsys)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-holding-no-check-of-linked-work", "self-review-holding-no-check-of-steers",
                   "self-review-holding-no-re-evaluation")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("self-review-holding-no-check-of-linked-work", "no Builder Check of linked work, which is required of it"),
    ("self-review-holding-no-check-of-steers", "no Builder Check of steers against the user's messages, which is required of it"),
    # the first self-review of a major version
    ("self-review-holding-no-re-evaluation", "no Builder Check of problem re-evaluation, which is required of it"),
])
def test_required_builder_check_missing_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(reviewed(work, fixtures, report), monkeypatch, capsys, action, heading)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-self-reviewed.md", "ferry-design-drafted-its-problem-citing-the-lighthouse")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("action, heading", MET)
def test_re_evaluation_leaving_out_a_place_the_problem_cites_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    root = reviewed(work, fixtures, "ferry-self-review-report", "ferry-design-drafted-its-problem-citing-the-lighthouse")
    assert "its Builder Checks of problem re-evaluation leave out " + LIGHTHOUSE in refused(root, monkeypatch, capsys, action, heading)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-self-reviewed.md", "ferry-design-drafted-its-problem-citing-the-lighthouse", "self-review-re-evaluating-the-ferry-and-the-lighthouse")
def test_re_evaluation_covering_each_place_the_problem_cites_passes(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "self-review-re-evaluating-the-ferry-and-the-lighthouse", "ferry-design-drafted-its-problem-citing-the-lighthouse")
    assert "- **Entry:** self-review-1" in appended(root, monkeypatch, capsys)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-self-reviewed.md", "ferry-design-drafted-self-reviewed", "second-self-review-holding-no-re-evaluation")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_later_self_review_of_a_major_version_asks_no_re_evaluation(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "ferry-self-review-report", "ferry-design-drafted-self-reviewed", **{"second-self-review-holding-no-re-evaluation": SECOND})
    assert "- **Entry:** self-review-2" in appended(root, monkeypatch, capsys, SECOND)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-self-reviewed.md", "ferry-design-reassessed-after-a-self-review",
                   "second-self-review-at-the-next-major-version-holding-no-re-evaluation")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.parametrize("action, heading", MET)
def test_first_self_review_of_a_new_major_version_asks_the_re_evaluation_again(fixtures, work, monkeypatch, capsys, action, heading):
    root = reviewed(work, fixtures, "ferry-self-review-report", "ferry-design-reassessed-after-a-self-review",
                    **{"second-self-review-at-the-next-major-version-holding-no-re-evaluation": SECOND})
    out = refused(root, monkeypatch, capsys, action, heading, SECOND)
    assert "no Builder Check of problem re-evaluation, which is required of it" in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-pages-changed.md", "guide-holding-the-hours-table")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-tracing-the-hours")
def test_self_review_tracing_the_mechanism_a_step_names_passes(fixtures, work, monkeypatch, capsys):
    root = reviewed(work, fixtures, "self-review-tracing-the-hours", guide="guide-holding-the-hours-table")
    assert acted(monkeypatch, root, dd.check_settled_report, SELF) == 0
    assert "== check-settled-report %s\n0 problems" % SELF in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-pages-changed.md", "guide-holding-the-hours-table")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-tracing-the-hours-with-no-outcome")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("ferry-self-review-report", "no Trace of the Decision Table at " + FERRY),
    ("self-review-tracing-the-hours-with-no-outcome", "Trace hours-by-season holds no Outcome, which its form requires where the report is a self-review's before the apply"),
])
def test_mechanism_untraced_or_traced_out_of_form_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    root = reviewed(work, fixtures, report, guide="guide-holding-the-hours-table")
    assert said in refused(root, monkeypatch, capsys, action, heading)


def after_a_round(work, fixtures, report):
    """-> the root of a project holding the design once its first round's entry stands, that round's report, and the
    self-review given."""
    return reviewed(work, fixtures, report, "ferry-design-drafted-after-its-first-round", **{"review-taken-up-and-stamped": ROUND})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-working-the-rounds-case")
def test_self_review_after_a_round_working_its_case_and_reading_each_miss_passes(fixtures, work, monkeypatch, capsys):
    root = after_a_round(work, fixtures, "self-review-working-the-rounds-case")
    assert acted(monkeypatch, root, dd.check_settled_report, SELF) == 0
    assert "== check-settled-report %s\n0 problems" % SELF in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-working-the-rounds-case-reading-no-guide")
@pytest.mark.parametrize("action, heading", MET)
def test_reads_leaving_out_a_place_a_miss_names_are_reported(fixtures, work, monkeypatch, capsys, action, heading):
    root = after_a_round(work, fixtures, "self-review-working-the-rounds-case-reading-no-guide")
    assert "its Reads leave out %s, a place a Miss of the phase names" % FERRY in refused(root, monkeypatch, capsys, action, heading)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
@pytest.mark.reads("design-script-self-reviewed.md", "self-review-working-the-rounds-cause-alone")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("ferry-self-review-report", "no Builder Check of worked case, which is required of it"),
    ("self-review-working-the-rounds-cause-alone", "its Builder Checks of worked case leave out `%s § Findings [Finding: reviewer-1-last-crossing-in-winter]`" % ROUND),
])
def test_self_review_after_a_round_working_no_case_of_its_change_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(after_a_round(work, fixtures, report), monkeypatch, capsys, action, heading)
