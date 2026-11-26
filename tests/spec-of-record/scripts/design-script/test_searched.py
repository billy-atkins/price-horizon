"""The checks of the design script a real search answers: the reach of retired wording, a Search run as its report is
handed back, checked and logged, and the research binding a design read against the files, each action called over a
project of fixtures the search reads as the action runs. The design script runs no Search by meaning, so no test here
needs the search's model."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-pages.md", "walkers-notes", "notes-citing-nothing"),
              pytest.mark.reads("audit-whole-project.md", "project-registry-of-one-skill")]
REVIEW, RESEARCH, SELF = REPORTS + "/adversarial-review/1.md", REPORTS + "/handed-off-judgment/1.md", REPORTS + "/self-review/1.md"
POST_APPLY = REPORTS + "/post-apply-review/1.md"
REVIEWED = [DESIGN, "adversarial-review", "Model=a model", "Effort=medium", "Led To=validating"]
SELF_REVIEWED = [DESIGN, "self-review", "Model=a model", "Effort=medium"]
FERRY, LIGHTHOUSE, GOAL = "`docs/guide.md § The Ferry`", "`docs/guide.md § The Lighthouse`", "guide-says-when-the-ferry-runs"
FIXTURE_FILE, OTHER_FIXTURE_FILE = "tests/spec-of-record/fixtures/guide.md", "tests/spec-of-record/fixtures/harbor.md"
QUAY = "[north quay]  The ferry leaves from the north quay."
SEARCH_GIVES = "Search reviewer-1-winter-hours gives %s, which its Places do not cover"
SEARCH_INDEX = ".ai/tmp/search-spec-of-record-scope/"
HANDED = [(dd.check_handed_back, "== check-handed-back "), (dd.take_up_report, "== take-up-report ")]


def searched(work, fixtures, design, guide="island-guide", notes="walkers-notes", **placed):
    """-> the root of a project holding a guide, a walker's notes, its registry of skills, the design given and the
    further fixtures given at their paths."""
    return project(work, fixtures, {guide: "docs/guide.md", notes: "docs/notes.md", design: DESIGN,
                                    "project-registry-of-one-skill": "specs/methodology/skills/registered-skills.md", **placed})


def kept(root):
    """-> {path: bytes} of each file of a project but the index the search keeps of it, to compare before and after
    an action."""
    return {p: b for p, b in held(root).items() if not p.startswith(SEARCH_INDEX)}


@pytest.mark.action("--show-reach")
@pytest.mark.passes
@pytest.mark.reads("design-script-searched.md", "ferry-design-drafted-retiring-the-north-quay")
def test_reach_lists_each_line_holding_a_retired_phrase(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, searched(work, fixtures, "ferry-design-drafted-retiring-the-north-quay"), dd.show_reach, DESIGN) == 0
    out = capsys.readouterr().out
    assert "== show-reach " + NAME in out and "2 lines" in out and "docs/guide.md:7  " + QUAY in out
    assert "docs/notes.md:3  (outside the Target)  [north quay]  A walker's notes: the north quay is slippery after rain." in out


@pytest.mark.action("--show-reach")
@pytest.mark.reports
@pytest.mark.reads("design-script-searched.md", "ferry-design-drafted-retiring-the-south-quay")
def test_reach_lists_no_line_for_a_phrase_no_operative_file_holds(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, searched(work, fixtures, "ferry-design-drafted-retiring-the-south-quay"), dd.show_reach, DESIGN) == 0
    out = capsys.readouterr().out
    assert "== show-reach " + NAME in out and "\n0 lines" in out and "[south quay]" not in out


@pytest.mark.action("--show-reach")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_reach_of_a_file_that_is_not_there_is_refused(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, searched(work, fixtures, "ferry-design-drafted"), dd.show_reach, ".ai/plans/design-specs/no-such-design.md") == 2
    assert "no design document" in capsys.readouterr().err


@pytest.mark.action("--check-retired-wording")
@pytest.mark.passes
@pytest.mark.reads("design-script-searched.md", "ferry-design-applying-retiring-the-north-quay", "island-guide-naming-the-north-pier")
def test_target_holding_no_retired_phrase_passes(fixtures, work, monkeypatch, capsys):
    # a file outside the Target, the walker's notes, still holds the phrase
    root = searched(work, fixtures, "ferry-design-applying-retiring-the-north-quay", "island-guide-naming-the-north-pier")
    assert acted(monkeypatch, root, dd.check_retired_wording, DESIGN) == 0
    assert "== check-retired-wording %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-retired-wording")
@pytest.mark.reports
@pytest.mark.reads("design-script-searched.md", "ferry-design-applying-retiring-the-north-quay")
def test_target_holding_a_retired_phrase_is_reported(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, searched(work, fixtures, "ferry-design-applying-retiring-the-north-quay"), dd.check_retired_wording, DESIGN) == 1
    out = capsys.readouterr().out
    assert "docs/guide.md\n  line 7 holds north quay, retired for north pier: The ferry leaves from the north quay." in out and "1 problem" in out


def holding_fixture_files(work, fixtures, design):
    """-> the root of a project holding two fixture files, each one line naming the north quay, and the index listing
    them, beside the guide and the notes."""
    root = searched(work, fixtures, design, **{"fixture-file-of-one-line": FIXTURE_FILE, "index-listing-two-files": "tests/spec-of-record/fixtures/index.md"})
    return project(work, fixtures, {"fixture-file-of-one-line": OTHER_FIXTURE_FILE})


@pytest.mark.action("--show-reach", "--check-retired-wording")
@pytest.mark.passes("--show-reach")
@pytest.mark.reports("--check-retired-wording")
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line")
@pytest.mark.reads("design-script-searched.md", "ferry-design-applying-retiring-the-north-quay-in-a-fixture-file", "index-listing-two-files")
def test_retired_wording_is_found_in_a_fixture_file_the_target_holds(fixtures, work, monkeypatch, capsys):
    root = holding_fixture_files(work, fixtures, "ferry-design-applying-retiring-the-north-quay-in-a-fixture-file")
    assert acted(monkeypatch, root, dd.show_reach, DESIGN) == 0
    out = capsys.readouterr().out
    assert "3 lines" in out and "docs/guide.md:7  " + QUAY in out and "%s:7  %s" % (FIXTURE_FILE, QUAY) in out
    assert "docs/notes.md:3  (outside the Target)" in out and OTHER_FIXTURE_FILE not in out
    assert acted(monkeypatch, root, dd.check_retired_wording, DESIGN) == 1
    out = capsys.readouterr().out
    assert "%s\n  line 7 holds north quay, retired for north pier: The ferry leaves from the north quay." % FIXTURE_FILE in out
    assert "docs/guide.md\n  line 7 holds north quay" in out and "2 problems" in out and OTHER_FIXTURE_FILE not in out


@pytest.mark.action("--show-reach", "--check-retired-wording")
@pytest.mark.passes("--show-reach")
@pytest.mark.reports("--check-retired-wording")
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line")
@pytest.mark.reads("design-script-searched.md", "ferry-design-applying-retiring-the-north-quay", "index-listing-two-files")
def test_retired_wording_is_found_in_no_fixture_file_the_target_does_not_hold(fixtures, work, monkeypatch, capsys):
    root = holding_fixture_files(work, fixtures, "ferry-design-applying-retiring-the-north-quay")
    assert acted(monkeypatch, root, dd.show_reach, DESIGN) == 0
    out = capsys.readouterr().out
    assert "2 lines" in out and "tests/spec-of-record" not in out
    assert acted(monkeypatch, root, dd.check_retired_wording, DESIGN) == 1
    out = capsys.readouterr().out
    assert "docs/guide.md\n  line 7 holds north quay" in out and "1 problem" in out and "tests/spec-of-record" not in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-handed-back-searching-by-terms")
@pytest.mark.parametrize("action, heading", HANDED)
def test_reviewers_search_holding_each_place_it_gives_passes(fixtures, work, monkeypatch, capsys, action, heading):
    root = searched(work, fixtures, "ferry-design-drafted", **{"review-handed-back-searching-by-terms": REVIEW})
    assert acted(monkeypatch, root, action, REVIEW) == 0
    assert heading + REVIEW + "\n0 problems" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-handed-back-searching-by-terms-its-places-none", "review-handed-back-searching-by-terms",
                   "island-guide-its-lighthouse-beam-reaching-the-north-quay")
@pytest.mark.parametrize("action, heading", [(dd.check_handed_back, "== check-handed-back "), (dd.take_up_report, "== take-up-report, not taken up ")])
@pytest.mark.parametrize("report, guide, gives", [
    ("review-handed-back-searching-by-terms-its-places-none", "island-guide", FERRY),
    # the same Search as the files stand after a fix wrote the searched words in another section
    ("review-handed-back-searching-by-terms", "island-guide-its-lighthouse-beam-reaching-the-north-quay", LIGHTHOUSE),
])
def test_reviewers_search_giving_a_place_its_places_leave_out_is_reported(fixtures, work, monkeypatch, capsys, action, heading, report, guide, gives):
    root = searched(work, fixtures, "ferry-design-drafted", guide, **{report: REVIEW})
    before = kept(root)
    assert acted(monkeypatch, root, action, REVIEW) == 1
    out = capsys.readouterr().out
    assert heading + REVIEW in out and SEARCH_GIVES % gives in out and kept(root) == before


@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-taken-up-searching-by-terms-its-finding-unsettled", "island-guide-its-lighthouse-beam-reaching-the-north-quay")
def test_taken_up_report_is_refused_for_the_builders_fault_alone_through_a_later_fix(fixtures, work, monkeypatch, capsys):
    root = searched(work, fixtures, "ferry-design-drafted", "island-guide-its-lighthouse-beam-reaching-the-north-quay",
                    **{"review-taken-up-searching-by-terms-its-finding-unsettled": REVIEW})
    before = kept(root)
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 1
    out = capsys.readouterr().out
    # no Search of the reviewer's is run again, and the report stays with the builder
    assert "Finding reviewer-1-last-crossing-in-winter is settled by 0 Settlements, not exactly one" in out
    assert "its Places do not cover" not in out and "goes back to its cold agent" not in out and kept(root) == before


@pytest.mark.action("--check-settled-report", "--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-taken-up-searching-by-terms", "island-guide-its-lighthouse-beam-reaching-the-north-quay")
def test_taken_up_report_passes_whatever_the_files_hold_since_the_take_up(fixtures, work, monkeypatch, capsys):
    root = searched(work, fixtures, "ferry-design-drafted", "island-guide-its-lighthouse-beam-reaching-the-north-quay",
                    **{"review-taken-up-searching-by-terms": REVIEW})
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert "== check-settled-report %s\n0 problems" % REVIEW in capsys.readouterr().out
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, REVIEWED) == 0
    assert "- **Entry:** adversarial-review-1" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.action("--check-handed-back")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "research-handed-back-searching-both-ways")
def test_research_searching_each_goal_both_ways_is_handed_back(fixtures, work, monkeypatch, capsys):
    root = searched(work, fixtures, "ferry-design-drafted", notes="notes-citing-nothing", **{"research-handed-back-searching-both-ways": RESEARCH})
    assert acted(monkeypatch, root, dd.check_handed_back, RESEARCH) == 0
    assert "== check-handed-back %s\n0 problems" % RESEARCH in capsys.readouterr().out


def researched(work, fixtures, report="research-taken-up-searching-both-ways", notes="notes-citing-nothing", **more):
    """-> the root of a project whose design's log names its research, with that research's report."""
    return searched(work, fixtures, "ferry-design-drafted-researched", notes=notes, **{report: RESEARCH, **more})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.action("--check-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-searched.md", "research-taken-up-searching-both-ways")
def test_research_naming_each_goal_both_ways_over_every_operative_file_passes(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, researched(work, fixtures), dd.check_design, DESIGN) == 0
    assert "== check-design %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-searched.md", "research-taken-up-searching-both-ways")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_first_builder_check_after_research_searching_both_ways_is_appended(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, **{"ferry-self-review-report": SELF})
    assert acted(monkeypatch, root, dd.stamp_settled_report, SELF) == 0
    assert acted(monkeypatch, root, dd.log_entry, SELF_REVIEWED) == 0
    assert "- **Entry:** self-review-1" in capsys.readouterr().out


@pytest.mark.action("--stamp-validation")
@pytest.mark.passes
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-searched.md", "research-taken-up-searching-both-ways")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_design_whose_research_searches_both_ways_is_stamped_validated(fixtures, work, monkeypatch, capsys):
    root = researched(work, fixtures, **{"ferry-self-review-report": SELF})
    assert acted(monkeypatch, root, dd.stamp_settled_report, SELF) == 0
    assert acted(monkeypatch, root, dd.log_entry, SELF_REVIEWED) == 0
    assert acted(monkeypatch, root, dd.stamp_validation, DESIGN) == 0
    assert "== stamp-validation\n**Validated:** " in capsys.readouterr().out
    name, header, _, text = dd.read_design(root / DESIGN)
    assert dd.validation(text, header)[0] == "validated"


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.action("--check-design")
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-searched.md", "research-taken-up-searching-both-ways", "research-searching-both-ways-narrowed-to-the-guide")
@pytest.mark.parametrize("report, notes, said, rule", [
    # the Search by terms, run over the files as they stand, gives the notes naming the quay
    ("research-taken-up-searching-both-ways", "walkers-notes",
     "Search ferry-times-by-terms of %s gives `docs/notes.md`, which no binding research report's Read Assessment's Area covers" % RESEARCH, "research-covers-its-matches"),
    ("research-searching-both-ways-narrowed-to-the-guide", "notes-citing-nothing",
     "the Searches by terms naming the goal %s were narrowed to paths that together leave out" % GOAL, "goals-searched-over-every-operative-file"),
])
def test_research_leaving_a_place_or_a_file_out_is_reported(fixtures, work, monkeypatch, capsys, report, notes, said, rule):
    root = researched(work, fixtures, report, notes)
    before = kept(root)
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 1
    out = capsys.readouterr().out
    assert "== check-design " + NAME in out and said in out and "[Name: %s]" % rule in out and kept(root) == before


@pytest.mark.action("--check-handed-back")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "research-handed-back-searching-by-terms-for-no-word")
def test_research_searching_by_terms_for_no_word_is_reported(fixtures, work, monkeypatch, capsys):
    root = searched(work, fixtures, "ferry-design-drafted", **{"research-handed-back-searching-by-terms-for-no-word": RESEARCH})
    assert acted(monkeypatch, root, dd.check_handed_back, RESEARCH) == 1
    assert "Search ferry-times-by-terms asks nothing: its term or passage reduces to no word" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
@pytest.mark.action("--check-design")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-researched.md", "ferry-design-drafted-researched")
@pytest.mark.reads("design-script-searched.md", "research-searching-both-ways-under-an-earlier-target-name")
def test_research_logged_under_an_earlier_target_name_is_read_as_the_canon_gives_it(fixtures, work, monkeypatch, capsys):
    # each Search names the target by its earlier name, and was narrowed to two folders that between them held every
    # operative file
    root = researched(work, fixtures, "research-searching-both-ways-under-an-earlier-target-name")
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 0
    assert "== check-design %s\n0 problems" % NAME in capsys.readouterr().out
    # the scope gains an operative file outside the two folders
    project(work, fixtures, {"notes-citing-nothing": "README.md"})
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 1
    out = capsys.readouterr().out
    assert all("the Searches by %s naming the goal %s were narrowed to paths that together leave out `README.md`" % (kind, GOAL) in out for kind in ("meaning", "terms"))
    assert "2 problems" in out


def tactical(work, fixtures, report):
    """-> the root of a project holding the design drafted and a round's report settled by a tactical fix."""
    return searched(work, fixtures, "ferry-design-drafted", **{report: REVIEW})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.action("--check-settled-report", "--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-taken-up-its-tactical-fix-changing-what-its-search-of-the-design-found")
def test_tactical_fix_changing_each_place_its_search_of_the_design_found_passes(fixtures, work, monkeypatch, capsys):
    root = tactical(work, fixtures, "review-taken-up-its-tactical-fix-changing-what-its-search-of-the-design-found")
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert "== check-settled-report %s\n0 problems" % REVIEW in capsys.readouterr().out
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, REVIEWED) == 0
    assert "- **Entry:** adversarial-review-1" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-taken-up-its-tactical-fix-changing-the-step-alone",
                   "review-taken-up-its-tactical-fix-naming-a-search-of-the-design-placing-none")
@pytest.mark.parametrize("report, said", [
    ("review-taken-up-its-tactical-fix-changing-the-step-alone",
     "Cause times-by-season's tactical fix leaves out `%s § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`, a place its Search found" % DESIGN),
    # the builder's own Search is run as the settled report is checked
    ("review-taken-up-its-tactical-fix-naming-a-search-of-the-design-placing-none",
     "Search first-crossing-named gives `%s § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`, which its Places do not cover" % DESIGN),
])
def test_tactical_fix_or_its_search_leaving_out_a_place_found_is_reported(fixtures, work, monkeypatch, capsys, report, said):
    root = tactical(work, fixtures, report)
    before = kept(root)
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 1
    assert said in capsys.readouterr().out and kept(root) == before


def applied(work, fixtures, design, report):
    """-> the root of a project holding two fixture files and an applying design, its post-apply review settled by a
    tactical fix."""
    holding_fixture_files(work, fixtures, design)
    return project(work, fixtures, {report: POST_APPLY})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line")
@pytest.mark.reads("design-script-searched.md", "index-listing-two-files", "ferry-design-applying-to-the-guide-the-notes-and-the-fixtures",
                   "ferry-design-applying-to-the-guide-and-the-notes", "post-apply-review-taken-up-searching-the-fixture-files-beside-changing-every-place",
                   "post-apply-review-taken-up-searching-the-operative-files-alone")
@pytest.mark.parametrize("design, report", [
    ("ferry-design-applying-to-the-guide-the-notes-and-the-fixtures", "post-apply-review-taken-up-searching-the-fixture-files-beside-changing-every-place"),
    # a design whose Target holds no fixture file asks no Search of the fixture files
    ("ferry-design-applying-to-the-guide-and-the-notes", "post-apply-review-taken-up-searching-the-operative-files-alone"),
])
def test_tactical_fix_over_applied_work_covering_each_search_it_owes_passes(fixtures, work, monkeypatch, capsys, design, report):
    root = applied(work, fixtures, design, report)
    assert acted(monkeypatch, root, dd.check_settled_report, POST_APPLY) == 0
    assert "== check-settled-report %s\n0 problems" % POST_APPLY in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line")
@pytest.mark.reads("design-script-searched.md", "index-listing-two-files", "ferry-design-applying-to-the-guide-the-notes-and-the-fixtures",
                   "post-apply-review-taken-up-searching-the-operative-files-alone",
                   "post-apply-review-taken-up-searching-the-fixture-files-beside-changing-the-operative-places")
@pytest.mark.parametrize("report, said, unsaid", [
    ("post-apply-review-taken-up-searching-the-operative-files-alone",
     ["Cause times-by-season's tactical fix names Search ferry-times-by-terms of the operative files with no Search of current-fixture-files asking the same beside it, "
      "though the design's Target holds a fixture file"], "\0"),
    ("post-apply-review-taken-up-searching-the-fixture-files-beside-changing-the-operative-places",
     ["Cause times-by-season's tactical fix leaves out `%s`, a place its Search found" % f for f in (FIXTURE_FILE, OTHER_FIXTURE_FILE)],
     "with no Search of current-fixture-files"),
])
def test_tactical_fix_over_applied_work_leaving_the_fixture_files_out_is_reported(fixtures, work, monkeypatch, capsys, report, said, unsaid):
    root = applied(work, fixtures, "ferry-design-applying-to-the-guide-the-notes-and-the-fixtures", report)
    assert acted(monkeypatch, root, dd.check_settled_report, POST_APPLY) == 1
    out = capsys.readouterr().out
    assert all(s in out for s in said) and unsaid not in out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report", "--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-searched.md", "review-taken-up-making-no-search-its-builder-adding-a-search-of-the-design")
def test_builder_adds_the_searches_part_to_a_review_whose_reviewer_made_none(fixtures, work, monkeypatch, capsys):
    root = tactical(work, fixtures, "review-taken-up-making-no-search-its-builder-adding-a-search-of-the-design")
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    out = capsys.readouterr().out
    assert "== check-settled-report %s\n0 problems" % REVIEW in out and "cold agent" not in out
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, REVIEWED) == 0
    assert "- **Entry:** adversarial-review-1" in capsys.readouterr().out
