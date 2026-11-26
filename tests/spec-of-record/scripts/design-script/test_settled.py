"""A round's report once the builder has settled it: --check-settled-report and --stamp-settled-report, which hold
the builder's parts to their form and the cold agent's to their fingerprints, and --log-entry, which takes the entry's
counts from the stamped report, each called over a project of fixtures."""
import pytest

from design_script_set import DESIGN, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")]
REVIEW, SECOND, RESEARCH = REPORTS + "/adversarial-review/1.md", REPORTS + "/adversarial-review/2.md", REPORTS + "/handed-off-judgment/1.md"
ENTRY = [DESIGN, "adversarial-review", "Model=a model", "Effort=medium", "Led To=validating"]
FINDING, KEPT, FERRY = "reviewer-1-last-crossing-in-winter", "Settlement times-by-season-kept", "`docs/guide.md § The Ferry`"
# each way a settled report a check reports is met: checked, or refused its stamp, writing nothing
MET = [(dd.check_settled_report, "== check-settled-report " + REVIEW), (dd.stamp_settled_report, "== stamp-settled-report, not stamped " + REVIEW)]
BUILDERS_PARTS = ("## Hand-back", "## Script Output", "## Causes", "## Settlement")


def settled(work, fixtures, report, at=REVIEW, design="ferry-design-drafted", **more):
    """-> the root of a project holding the guide, the design given and a report at its place."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, report: at, **more})


def refused(work, fixtures, monkeypatch, capsys, action, heading, report):
    """-> what an action printed of a settled report it reports, having held that it exits 1 and writes nothing."""
    root = settled(work, fixtures, report)
    before = held(root)
    assert acted(monkeypatch, root, action, REVIEW) == 1
    out = capsys.readouterr().out
    assert heading in out and held(root) == before
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-settled.md", "review-taken-up-and-settled")
def test_round_settled_in_its_form_passes(fixtures, work, monkeypatch, capsys):
    root = settled(work, fixtures, "review-taken-up-and-settled")
    before = held(root)
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert "== check-settled-report %s\n0 problems" % REVIEW in capsys.readouterr().out and held(root) == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-settled.md", "review-taken-up-and-settled", "review-taken-up-its-finding-dropped")
@pytest.mark.parametrize("report, counts", [
    ("review-taken-up-and-settled", "**Design Flaws:** 0 \\\n    **Implementation Flaws:** 1 \\\n    **Nits:** 0 \\\n    **Dropped:** 0"),
    # a finding its reviewer marked a flaw and the builder dropped is counted by the last word of its Settlement
    ("review-taken-up-its-finding-dropped", "**Design Flaws:** 0 \\\n    **Implementation Flaws:** 0 \\\n    **Nits:** 0 \\\n    **Dropped:** 1"),
])
def test_entry_of_a_round_takes_its_counts_from_its_report(fixtures, work, monkeypatch, capsys, report, counts):
    root = settled(work, fixtures, report)
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    out = capsys.readouterr().out
    assert "- **Entry:** adversarial-review-1" in out and "**Design Version:** 1.0.1 \\\n    **Model:** a model \\\n    **Effort:** medium \\\n    " + counts in out


@pytest.mark.action("--check-settled-report", "--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped")
def test_report_and_design_hold_their_forms_once_the_rounds_entry_stands(fixtures, work, monkeypatch, capsys):
    root = settled(work, fixtures, "review-taken-up-and-stamped", design="ferry-design-drafted-after-its-first-round")
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0
    out = capsys.readouterr().out
    assert "== check-settled-report %s\n0 problems" % REVIEW in out and "== check-design-form ferry-times-in-the-guide\n0 problems" in out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-and-settled")
def test_count_given_an_entry_is_refused(fixtures, work, monkeypatch, capsys):
    root = settled(work, fixtures, "review-taken-up-and-settled")
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, ENTRY + ["Nits=3"]) == 1
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and "a count given, which is taken from the check's report alone: Nits" in out and held(root) == before


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-its-rationale-changed", "review-taken-up-its-reviewers-search-changed",
                   "review-taken-up-its-searches-removed")
@pytest.mark.parametrize("report, said, kept", [
    ("review-taken-up-its-rationale-changed", "the Findings part no longer holds what its cold agent handed back", "A visitor in winter is left on the quay."),
    ("review-taken-up-its-reviewers-search-changed", "the Searches part no longer holds what its cold agent handed back",
     "every place giving the hours the ferry keeps \\"),
    ("review-taken-up-its-searches-removed", "the Searches part its cold agent handed back is removed", "## Findings"),
])
def test_cold_part_changed_since_the_take_up_sends_the_report_back(fixtures, work, monkeypatch, capsys, report, said, kept):
    root = settled(work, fixtures, report)
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 1
    out, now = capsys.readouterr().out, (root / REVIEW).read_text(encoding="utf-8")
    assert said in out and "[Name: cold-parts-kept]" in out and "goes back to its cold agent" in out
    # the report goes back cleared of the parts the builder wrote, the cold agent's left as they stand
    assert not any(h in now for h in BUILDERS_PARTS) and kept in now


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-making-no-search-its-builder-adding-one-and-its-rationale-changed")
def test_report_sent_back_is_cleared_of_a_searches_part_the_builder_added(fixtures, work, monkeypatch, capsys):
    root = settled(work, fixtures, "review-taken-up-making-no-search-its-builder-adding-one-and-its-rationale-changed")
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 1
    out, now = capsys.readouterr().out, (root / REVIEW).read_text(encoding="utf-8")
    assert "the Findings part no longer holds what its cold agent handed back" in out and "goes back to its cold agent" in out
    assert "## Searches" not in now and "each-season-named" not in now and not any(h in now for h in BUILDERS_PARTS)
    assert now.startswith("# Check's Report") and "## Findings" in now and "A visitor in winter is left on the quay." in now


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
@pytest.mark.parametrize("action, heading", MET)
def test_cold_agents_report_never_taken_up_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "ferry-review-report")
    assert "it holds no Hand-back part: a report a cold agent wrote is taken up by --take-up-report" in out and "[Name: cold-parts-kept]" in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "research-taken-up-its-searches-added-after")
def test_searches_part_added_to_research_handing_none_back_is_reported(fixtures, work, monkeypatch, capsys):
    root = settled(work, fixtures, "research-taken-up-its-searches-added-after", RESEARCH)
    assert acted(monkeypatch, root, dd.check_settled_report, RESEARCH) == 1
    out = capsys.readouterr().out
    assert "a part its cold agent writes, added after the builder took the report up: Searches" in out and "[Name: cold-parts-kept]" in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-settling-its-finding-twice")
@pytest.mark.parametrize("action, heading", MET)
def test_finding_settled_twice_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "review-taken-up-settling-its-finding-twice")
    assert "Finding %s is settled by 2 Settlements, not exactly one" % FINDING in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-taken-up.md", "review-taken-up-settling-another-finding")
@pytest.mark.reads("design-script-settled.md", "review-taken-up-its-settlement-naming-a-cause-not-held", "review-taken-up-its-settlement-carried-by-a-step-not-held")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-settling-another-finding", KEPT + " settles reviewer-1-another-finding, which no Finding of the report is"),
    ("review-taken-up-its-settlement-naming-a-cause-not-held", KEPT + " names a Cause the report does not hold: times-by-tide"),
    ("review-taken-up-its-settlement-carried-by-a-step-not-held", KEPT + " is carried by a step the design does not hold: no-such-step"),
])
def test_key_naming_no_record_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-justified-by-a-goal-not-held", "review-taken-up-required-by-the-rules-justified-by-goals",
                   "review-taken-up-on-the-users-authority-with-no-decision", "review-taken-up-keeping-a-design-flaw-on-the-builders-authority")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-justified-by-a-goal-not-held", [KEPT + "'s Justifying Goals name guide-says-what-the-ferry-costs, which is no design goal's Name"]),
    ("review-taken-up-required-by-the-rules-justified-by-goals", [KEPT + " holds a Justifying Goals, which its form gives it only where its Required By names the goals",
                                                                 KEPT + " holds no Justifying Rules, which its form requires where its Required By names the rules"]),
    ("review-taken-up-on-the-users-authority-with-no-decision", [KEPT + " holds no User Decision, which its form requires where its Fix Authority is the user's"]),
    ("review-taken-up-keeping-a-design-flaw-on-the-builders-authority",
     [KEPT + " holds Fix Authority the builder's, where Whose Fix It Is gives the user the call: its Verdict is design flaw"]),
])
def test_settlement_unjustified_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, report)
    assert all(s in out for s in said)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-its-settlement-stating-order-secondary", "review-taken-up-its-changed-place-stating-order-tertiary")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-its-settlement-stating-order-secondary", KEPT + " states Order secondary, where its lineage gives primary: it lands on no earlier change"),
    ("review-taken-up-its-changed-place-stating-order-tertiary", "states Order tertiary, where its lineage gives primary: it names the findings whose fix it is"),
])
def test_order_other_than_its_lineage_gives_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, report)
    assert said in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-departing-from-its-verdict-unreasoned")
@pytest.mark.parametrize("action, heading", MET)
def test_departure_unreasoned_is_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "review-taken-up-departing-from-its-verdict-unreasoned")
    assert KEPT + " departs from Finding %s in Verdict and holds no Departure Reason" % FINDING in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-its-settling-reads-leaving-out-the-evidence")
@pytest.mark.parametrize("action, heading", MET)
def test_settling_reads_leaving_out_the_evidence_are_reported(fixtures, work, monkeypatch, capsys, action, heading):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, "review-taken-up-its-settling-reads-leaving-out-the-evidence")
    assert "its Settling Reads leave out %s, a place the Evidence of a marked Finding names" % FERRY in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-holding-no-causes", "review-taken-up-its-settlement-stating-no-ending",
                   "review-taken-up-its-cause-holding-no-misses", "review-taken-up-its-revision-rewriting-no-decision")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-holding-no-causes", "it holds no Causes part, which its form requires of it"),
    ("review-taken-up-its-settlement-stating-no-ending", "its Settlement holds no Ending, which its form requires where the report owes the statement of how its check ended"),
    ("review-taken-up-its-cause-holding-no-misses", "Cause times-by-season holds no Misses, which its form requires where it settles a design flaw or an implementation flaw"),
    ("review-taken-up-its-revision-rewriting-no-decision", "Cause times-by-season's Proposed Change holds no Decision Rewritten, which its form requires where its Kind is revision"),
])
def test_builders_part_out_of_its_form_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    assert said in refused(work, fixtures, monkeypatch, capsys, action, heading, report)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "review-taken-up-its-tactical-fix-naming-a-search-by-meaning", "review-taken-up-its-tactical-fix-citing-a-search-not-held")
@pytest.mark.parametrize("action, heading", MET)
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-its-tactical-fix-naming-a-search-by-meaning",
     ["Cause times-by-season's tactical fix names Search each-season-named, a search by meaning, which gives a part of a ranking and never every place its defect stands in",
      "Cause times-by-season's tactical fix leaves out %s, a place its Search found" % FERRY]),
    ("review-taken-up-its-tactical-fix-citing-a-search-not-held", ["Cause times-by-season's Proposed Change cites a Search the report does not hold: no-such-search"]),
])
def test_tactical_fix_naming_no_search_giving_every_place_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, said):
    out = refused(work, fixtures, monkeypatch, capsys, action, heading, report)
    assert all(s in out for s in said)


def second_round(work, fixtures, report):
    """-> the root of a project holding the design once its first round's entry stands, the first round's report as
    it was stamped, and the second round's report given."""
    return settled(work, fixtures, "review-taken-up-and-stamped", design="ferry-design-drafted-after-its-first-round", **{report: SECOND})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
@pytest.mark.action("--check-settled-report", "--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped", "second-review-taken-up-landing-on-the-first")
def test_second_round_naming_the_first_and_landing_deeper_passes(fixtures, work, monkeypatch, capsys):
    root = second_round(work, fixtures, "second-review-taken-up-landing-on-the-first")
    assert acted(monkeypatch, root, dd.check_settled_report, SECOND) == 0
    assert "== check-settled-report %s\n0 problems" % SECOND in capsys.readouterr().out
    assert acted(monkeypatch, root, dd.stamp_settled_report, SECOND) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    assert "- **Entry:** adversarial-review-2" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-settled.md", "ferry-design-drafted-after-its-first-round", "review-taken-up-and-stamped",
                   "second-review-taken-up-listing-no-earlier-report", "second-review-taken-up-stating-primary")
@pytest.mark.parametrize("report, said", [
    ("second-review-taken-up-listing-no-earlier-report", "its Earlier Reports leave out `%s`, a report of the phase's record" % REVIEW),
    ("second-review-taken-up-stating-primary",
     "states Order primary, where its lineage gives secondary: it lands on `%s § Causes [Cause: times-by-season]`, whose order is primary" % REVIEW),
])
def test_second_round_leaving_the_first_out_or_stating_its_order_is_reported(fixtures, work, monkeypatch, capsys, report, said):
    root = second_round(work, fixtures, report)
    before = held(root)
    assert acted(monkeypatch, root, dd.check_settled_report, SECOND) == 1
    out = capsys.readouterr().out
    assert "== check-settled-report " + SECOND in out and said in out and held(root) == before
