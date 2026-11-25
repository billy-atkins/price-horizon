"""The checks of the design script a real search answers: the reach of retired wording, the checks over a design's
work, a Search run as its report is handed back, checked and logged, and the research binding a design read against
the files.

The search reads one project once: `a_searched_project` has the first test of the file that asks build a project
holding the files a form is read from, the guide and a walker's notes, with the index the search builds of them, in
the file's own folder within the run's folder, and gives each test a copy of it in the test's folder. So a test's own
search reads only what the test changes.
"""

import pytest

from design_script_set import (AGREED, APPLYING, CAUSE, CHECKOUT, CHECK_FIELDS, DRAFTED, FERRY, FINDING, GOAL, JUDGMENT, KEPT, LIGHTHOUSE, NAME,
    OBJECTIVE, RESEARCH, REVIEW, ROUND_FIELDS, RULE, SEARCH_GIVES, SELF, SKILLS, STEP, a_design, a_report, builder_part, cold_part, design_documents,
    passes, report_at, reports, retiring, searching_review, shown, swap, taken_up, whole_research)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-pages.md", "walkers-notes")]


@pytest.mark.action("--show-reach")
@pytest.mark.passes
@pytest.mark.reads("design-script-record-parts.md", "retired-phrases-of-one-phrase")
def test_reach_lists_each_line_holding_a_retired_phrase(check, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("reach")
        got = p.run("--show-reach", p.design(skill=skill, text=retiring(a_design(skill=skill, log=DRAFTED))), skill=skill)
        inside = "" if skill == "design-specs" else "  (outside the Target)"
        check("--show-reach of %s lists each line of an operative file holding the phrase a design retires, marking those outside its Target" % skill,
              passes(got, "== show-reach " + NAME, "2 lines") and "docs/guide.md:7%s  [north quay]  The ferry leaves from the north quay." % inside in got[1]
              and "docs/notes.md:3  (outside the Target)  [north quay]  A walker's notes: the north quay is slippery after rain." in got[1], shown(got))


@pytest.mark.action("--show-reach")
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "retired-phrases-of-one-phrase")
def test_reach_lists_no_line_for_a_phrase_unheld(check, a_searched_project):
    p = a_searched_project("reach-none")
    got = p.run("--show-reach", p.design(text=retiring(a_design(log=DRAFTED), "south quay")))
    check("--show-reach lists no line for a phrase no operative file holds, the design document's own aside", passes(got, "== show-reach " + NAME, "\n0 lines") and "[south quay]" not in got[1], shown(got))
    got = p.run("--show-reach", ".ai/plans/design-specs/no-such-design.md")
    check("--show-reach of a file that is not there says so, exit 2", got[0] == 2 and "no design document" in got[1], shown(got))


@pytest.mark.action("--check-retired-wording")
@pytest.mark.passes
@pytest.mark.reads("design-script-record-parts.md", "retired-phrases-of-one-phrase")
def test_target_holding_no_retired_phrase_passes(check, fixtures, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("retired-pass")
        design = p.design(skill=skill, text=retiring(a_design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`")))
        p.put("docs/guide.md", swap(fixtures["island-guide"], "north quay", "north pier"))
        got = p.run("--check-retired-wording", design, skill=skill)
        check("--check-retired-wording of %s passes where no file of the Target holds the retired phrase, a file outside it holding the phrase still" % skill,
              passes(got, "== check-retired-wording " + NAME, "0 problems"), shown(got))


@pytest.mark.action("--check-retired-wording")
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "retired-phrases-of-one-phrase")
def test_target_holding_a_retired_phrase_is_reported(check, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("retired-reports")
        design = p.design(skill=skill, text=retiring(a_design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`")))
        got = p.run("--check-retired-wording", design, skill=skill)
        check("--check-retired-wording of %s reports each line of the Target holding the retired phrase, with its replacement, and no line of a file outside it" % skill,
              reports(got, "== check-retired-wording " + NAME, ["docs/guide.md\n  line 7 holds north quay, retired for north pier: The ferry leaves from the north quay.", "1 problem"]), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_reviewers_search_is_run_at_the_hand_back(check, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("reviewers-search")
        p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(REVIEW, skill=skill), cold_part(searching_review()).replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill))
        got = p.run("--check-handed-back", path, skill=skill)
        check("--check-handed-back of %s passes a review's report whose Search by terms holds each place the search gives" % skill, passes(got, "== check-handed-back " + path, "0 problems"), shown(got))
        got = p.run("--take-up-report", path, skill=skill)
        check("--take-up-report of %s takes it up" % skill, passes(got, "== take-up-report " + path, "0 problems") and "## Hand-back" in p.read(path), shown(got))
        path = p.put(report_at(REVIEW, skill=skill), cold_part(searching_review("none")).replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill))
        for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
            got = p.run(flag, path, skill=skill)
            check("%s of %s reports a review's report whose Search by terms gives a place its Places leave out" % (flag, skill), reports(got, heading, SEARCH_GIVES % FERRY), shown(got))


@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_taken_up_report_stands_through_a_later_fix(check, fixtures, a_searched_project):
    unsettled = lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding")
    for skill in SKILLS:
        p = a_searched_project("later-fix")
        design = p.design(skill=skill, log=DRAFTED)
        text = searching_review().replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill)
        path = taken_up(p, REVIEW, cold_part(text) + "\n" + unsettled(builder_part(text)), skill=skill)
        # the builder's fix writes the searched words in a section the reviewer's Search did not give
        p.put("docs/guide.md", swap(fixtures["island-guide"], "trims the lamp at dusk.", "trims the lamp at dusk, and its beam reaches the north quay."))
        before = p.read(path)
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s refuses the report for the fault in the builder's own Settlement alone, runs no Search of the reviewer's again, and leaves the report with the builder" % skill,
              reports(got, "== check-settled-report", "Finding %s is settled by 0 Settlements, not exactly one" % FINDING) and "its Places do not cover" not in got[1]
              and "goes back to its cold agent" not in got[1] and p.read(path) == before, shown(got))
        p.put(path, before.replace("      - reviewer-1-another-finding", "      - " + FINDING))
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes it once the builder's part is put right, whatever the files have come to hold since the take-up" % skill,
              passes(got, "== check-settled-report " + path, "0 problems"), shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("and --log-entry of %s appends its entry" % skill, passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
        fresh = p.put(report_at(REVIEW, 2, skill=skill), cold_part(text).replace("adversarial-review-1", "adversarial-review-2"))
        got = p.run("--check-handed-back", fresh, skill=skill)
        check("while the same Search in a report handed back after the fix is held to the files as they then stand, by --check-handed-back of %s" % skill,
              reports(got, "== check-handed-back", SEARCH_GIVES % LIGHTHOUSE), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.passes
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-for-the-quay")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report", "ferry-self-review-report")
def test_research_searching_each_goal_both_ways_passes(check, fixtures, a_searched_project):
    p = a_searched_project("research-whole")
    p.put("docs/notes.md", fixtures["notes-citing-nothing"])  # the notes no longer name the quay the research searches for
    design = p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), cold_part(whole_research()))
    back = p.run("--check-handed-back", path)
    path = taken_up(p, JUDGMENT, whole_research())
    logged = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS)
    change = p.run("--log-entry", design, "plan-change")
    check("a research report whose Searches the search runs is handed back, taken up and logged", back[0] == 0 and logged[0] == 0 and change[0] == 0, shown(back) + shown(logged))
    got = p.run("--check-design", design)
    check("--check-design passes a design not yet approved whose research names each goal in a Search by meaning and in one by terms of every operative file, each place they give lying in an Area it assesses",
          passes(got, "== check-design " + NAME, "0 problems"), shown(got))
    own = p.put(report_at(SELF), a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry appends the first check of the builder's after that research, the research read together as its entry is appended", passes(got, "== log-entry", "- **Entry:** self-review-1"), shown(got))
    got = p.run("--stamp-validation", design)
    shown_ = p.run("--show-validation", design)
    check("--stamp-validation stamps the design, which then reads validated", passes(got, "== stamp-validation\n**Validated:** ") and ": validated;" in shown_[1], shown(got) + shown(shown_))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-for-the-quay")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_research_leaving_a_place_or_a_file_out_is_reported(check, fixtures, a_searched_project):
    p = a_searched_project("research-reports")
    design = p.design(log=AGREED + RESEARCH + (("plan-change", {}),))
    path = p.put(report_at(JUDGMENT), whole_research())
    got = p.run("--check-design", design)
    check("--check-design reports a place a research's Search by terms gives, run over the files as they stand, that no Area of the research covers",
          reports(got, "== check-design " + NAME, ["Search ferry-times-by-terms of %s gives `docs/notes.md`, which no binding research report's Read Assessment's Area covers" % path, RULE % "research-covers-its-matches"])
          and "is named by no Search" not in got[1], shown(got))
    p.put("docs/notes.md", fixtures["notes-citing-nothing"])
    p.put(path, whole_research(narrowed="    **Narrowed To:**\n      - `docs/guide.md`\n\n"))
    got = p.run("--check-design", design)
    check("--check-design reports a goal whose Searches by terms were narrowed to paths leaving an operative file out",
          reports(got, "== check-design " + NAME, ["the Searches by terms naming the goal %s were narrowed to paths that together leave out" % GOAL, RULE % "goals-searched-over-every-operative-file"]), shown(got))
    p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), cold_part(whole_research(query="...")))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a research report whose Search by terms reduces to no word", reports(got, "== check-handed-back", "Search ferry-times-by-terms asks nothing: its term or passage reduces to no word"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.passes("tactical-fixes-cover-their-searches")
@pytest.mark.reports("searches-cover-their-matches")
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-of-the-design")
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_tactical_fix_covers_each_place_its_search_found(check, fixtures, a_searched_project):
    design_path = ".ai/plans/design-specs/%s.md" % NAME
    found = "`%s § Design Plan Steps [Name: %s]`" % (design_path, OBJECTIVE)
    step = "`%s § Design Plan Steps [Name: %s]`" % (design_path, STEP)
    # a Search of the builder's own, added to the report's Searches, its Places the ones the test gives
    search = "\n\n" + swap(fixtures["search-by-terms-of-the-design"], "      - " + found, "      - %s")

    def settled(places=found, changed=found):
        p = a_searched_project("tactical-fix")
        design = p.design(log=DRAFTED)
        text = a_report("review")
        own = swap(builder_part(text), "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
                   "      - **Kind:** tactical fix \\\n        **Search:** first-crossing-named \\\n        **Reason:** The Objective's meaning stands, and only its wording names one season. \\")
        path = taken_up(p, REVIEW, cold_part(text) + "\n" + swap(own, "          - **Place:** " + step, "          - **Place:** " + changed))
        p.put(path, swap(p.read(path), "\n\n## Hand-back", search % places + "\n## Hand-back"))
        return p, design, path

    p, design, path = settled()
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a round whose tactical fix names a Search by terms of the design document, run as the report is checked, and changes each place it found",
          passes(got, "== check-settled-report " + path, "0 problems"), shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("and --log-entry appends its entry", passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
    p, design, path = settled(changed=step)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix whose Places leave out a place its Search found", reports(got, "== check-settled-report", "Cause %s's tactical fix leaves out %s, a place its Search found" % (CAUSE, found)), shown(got))
    p, design, path = settled(places="none")
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Search of the builder's own, run as the settled report is checked, giving a place its Places leave out",
          reports(got, "== check-settled-report", "Search first-crossing-named gives %s, which its Places do not cover" % found), shown(got))


FIXTURE_FILE, OTHER_FIXTURE_FILE, FIXTURES_INDEX = KEPT + "/fixtures/guide.md", KEPT + "/fixtures/harbour.md", KEPT + "/fixtures/index.md"


def fixture_files(p, fixtures):
    """Give a project two fixture files, each holding one line naming the north quay, and the index listing them."""
    p.put(FIXTURE_FILE, fixtures["fixture-file-of-one-line"])
    p.put(OTHER_FIXTURE_FILE, fixtures["fixture-file-of-one-line"])
    p.put(FIXTURES_INDEX, fixtures["index-listing-one-file"] + "| `harbour.md` | The same sentence, kept a second time |\n")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-for-the-quay")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_research_logged_under_an_earlier_target_name_is_read_as_the_canon_gives_it(check, fixtures, a_searched_project):
    earlier = "current-durable-files"
    check("the canon as it stands gives the earlier name of a target the target it is read as", design_documents.earlier_targets(CHECKOUT).get(earlier) == "current-operative-files",
          design_documents.earlier_targets(CHECKOUT))
    p = a_searched_project("earlier-names")
    p.put("docs/notes.md", fixtures["notes-citing-nothing"])  # the notes no longer name the quay the research searches for
    design = p.design(log=AGREED + RESEARCH + (("plan-change", {}),))
    # research logged before the targets were renamed: each Search names the earlier target, and was narrowed to the
    # two folders that between them held every operative file
    narrowed = "    **Narrowed To:**\n      - `docs`\n      - `specs`\n\n"
    p.put(report_at(JUDGMENT), whole_research(target=earlier, narrowed=narrowed, by_meaning_narrowed=narrowed))
    got = p.run("--check-design", design)
    check("--check-design reads research whose Searches name a target by its earlier name as searches of the operative files: over a scope those Searches cover, each goal is searched and nothing is reported",
          passes(got, "== check-design " + NAME, "0 problems"), shown(got))
    p.put("README.md", fixtures["notes-citing-nothing"])  # the scope gains an operative file outside the two folders
    got = p.run("--check-design", design)
    check("and over a scope that has gained a file those Searches' paths leave out, it reports the goal as unsearched over that file, by meaning and by terms",
          reports(got, "== check-design " + NAME, ["the Searches by meaning naming the goal %s were narrowed to paths that together leave out `README.md`" % GOAL,
                                                   "the Searches by terms naming the goal %s were narrowed to paths that together leave out `README.md`" % GOAL,
                                                   RULE % "goals-searched-over-every-operative-file", "2 problems"]), shown(got))


@pytest.mark.action("--show-reach", "--check-retired-wording")
@pytest.mark.passes("--show-reach")
@pytest.mark.reports("--check-retired-wording")
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line", "index-listing-one-file")
@pytest.mark.reads("design-script-record-parts.md", "retired-phrases-of-one-phrase")
def test_retired_wording_is_found_in_a_fixture_file_the_target_holds(check, fixtures, a_searched_project):
    quay = "[north quay]  The ferry leaves from the north quay."
    p = a_searched_project("retired-in-fixtures")
    fixture_files(p, fixtures)
    design = p.design(text=retiring(a_design(status="applying", log=APPLYING, Target="`docs/guide.md`; `%s`" % FIXTURE_FILE)))
    got = p.run("--show-reach", design)
    check("--show-reach lists, beside each line of an operative file holding the retired phrase, the line of a fixture file the Target holds, and no line of a fixture file no Target holds",
          passes(got, "== show-reach " + NAME, "3 lines") and "docs/guide.md:7  " + quay in got[1] and "%s:7  %s" % (FIXTURE_FILE, quay) in got[1]
          and "docs/notes.md:3  (outside the Target)" in got[1] and OTHER_FIXTURE_FILE not in got[1], shown(got))
    got = p.run("--check-retired-wording", design)
    check("--check-retired-wording reports the line of a fixture file the Target holds, and no line of a fixture file no Target holds",
          reports(got, "== check-retired-wording " + NAME, ["%s\n  line 7 holds north quay, retired for north pier: The ferry leaves from the north quay." % FIXTURE_FILE,
                                                             "docs/guide.md\n  line 7 holds north quay", "2 problems"]) and OTHER_FIXTURE_FILE not in got[1], shown(got))
    design = p.design(text=retiring(a_design(status="applying", log=APPLYING, Target="`docs/guide.md`")))
    got = p.run("--show-reach", design)
    check("--show-reach lists no line of a fixture file for a design whose Target holds none", passes(got, "== show-reach " + NAME, "2 lines") and KEPT not in got[1], shown(got))
    got = p.run("--check-retired-wording", design)
    check("nor does --check-retired-wording report one", reports(got, "== check-retired-wording " + NAME, ["docs/guide.md\n  line 7 holds north quay", "1 problem"]) and KEPT not in got[1], shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line", "index-listing-one-file")
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-for-the-quay")
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_tactical_fix_over_applied_work_searches_the_fixture_files_a_target_holds(check, fixtures, a_searched_project):
    kind = "post-apply-review"
    # a place a tactical fix changes, settling the review's one finding, and the Search of the operative files it names
    a_place = "          - **Place:** %s \\\n            **Order:** primary \\\n            **Settles:**\n              - " + FINDING + "\n"
    step = "`.ai/plans/design-specs/%s.md § Design Plan Steps [Name: %s]`" % (NAME, STEP)
    operative = swap(fixtures["search-by-terms-for-the-quay"], "      - " + FERRY + "\n", "      - " + FERRY + "\n      - `docs/notes.md`\n")
    # the Search standing beside it: the same asked of the fixture files, giving the one line of each
    beside = swap(swap(operative, "ferry-times-by-terms", "ferry-times-by-terms-in-the-fixtures"), "    **Snapshot:**", "    **Target:** current-fixture-files \\\n    **Snapshot:**")
    beside = swap(beside, "      - " + FERRY + "\n      - `docs/notes.md`\n", "      - `%s`\n      - `%s`\n" % (FIXTURE_FILE, OTHER_FIXTURE_FILE))

    def settled(target, searches, places):
        p = a_searched_project("tactical-applied")
        fixture_files(p, fixtures)
        design = p.design(status="applying", log=APPLYING, Target=target)
        # a review over applied work: its finding and the finding's Settlement each say where the finding lies
        text = swap(a_report("review", entry=kind + "-1"), "        **Delivers:** An Objective giving the first and the last crossing of each season.\n",
                    "        **Delivers:** An Objective giving the first and the last crossing of each season.\n\n    **Lies In:** the writing\n")
        text = swap(text, "    **Fix Authority:** the builder's \\\n", "    **Fix Authority:** the builder's \\\n    **Lies In:** the writing \\\n")
        own = swap(builder_part(text), "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
                   "      - **Kind:** tactical fix \\\n        **Search:** ferry-times-by-terms \\\n        **Reason:** The section's meaning stands, and only its wording names the quay. \\")
        own = swap(own, a_place % step, "\n".join(a_place % place for place in places))
        path = taken_up(p, kind, cold_part(text) + "\n" + own)
        p.put(path, swap(p.read(path), "\n\n## Hand-back", "\n\n" + "\n".join(searches) + "\n## Hand-back"))
        return p, path

    with_fixtures = "`docs/guide.md`; `docs/notes.md`; `%s/fixtures/`" % KEPT
    changed = [FERRY, "`docs/notes.md`"]
    p, path = settled(with_fixtures, [operative], changed)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix over applied work whose Search of the operative files has no Search of the fixture files beside it, where the design's Target holds a fixture file",
          reports(got, "== check-settled-report", "Cause %s's tactical fix names Search ferry-times-by-terms of the operative files with no Search of current-fixture-files asking the same beside it, "
                  "though the design's Target holds a fixture file" % CAUSE), shown(got))
    p, path = settled(with_fixtures, [operative, beside], changed)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix whose Places leave out a place the Search of the fixture files found",
          reports(got, "== check-settled-report", ["Cause %s's tactical fix leaves out `%s`, a place its Search found" % (CAUSE, FIXTURE_FILE),
                                                  "Cause %s's tactical fix leaves out `%s`, a place its Search found" % (CAUSE, OTHER_FIXTURE_FILE)])
          and "with no Search of current-fixture-files" not in got[1], shown(got))
    p, path = settled(with_fixtures, [operative, beside], changed + ["`%s`" % FIXTURE_FILE, "`%s`" % OTHER_FIXTURE_FILE])
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a tactical fix whose Places cover each place its Search of the operative files and the Search of the fixture files beside it found",
          passes(got, "== check-settled-report " + path, "0 problems"), shown(got))
    p, path = settled("`docs/guide.md`; `docs/notes.md`", [operative], changed)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report asks no Search of the fixture files of a tactical fix of a design whose Target holds no fixture file",
          passes(got, "== check-settled-report " + path, "0 problems"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-record-parts.md", "search-by-terms-of-the-design")
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_builder_adds_the_searches_part_to_a_review_whose_reviewer_made_none(check, fixtures, a_searched_project):
    found = "`.ai/plans/design-specs/%s.md § Design Plan Steps [Name: %s]`" % (NAME, OBJECTIVE)
    step = "`.ai/plans/design-specs/%s.md § Design Plan Steps [Name: %s]`" % (NAME, STEP)
    p = a_searched_project("builders-searches")
    design = p.design(log=DRAFTED)
    text = a_report("review")
    # the reviewer made no Search, so its cold part holds no Searches part; the builder settles the finding by a
    # tactical fix naming a Search of its own, changing the place that Search found
    cold = cold_part(text).split("\n## Searches")[0] + "\n"
    own = swap(builder_part(text), "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
               "      - **Kind:** tactical fix \\\n        **Search:** first-crossing-named \\\n        **Reason:** The Objective's meaning stands, and only its wording names one season. \\")
    path = taken_up(p, REVIEW, cold + "\n" + swap(own, "          - **Place:** " + step, "          - **Place:** " + found))
    taken = p.read(path)
    check("the take-up of a review whose reviewer handed no Searches back writes no fingerprint of a Searches part", "## Hand-back" in taken and "- Searches: " not in taken, taken[-500:])
    # the Searches part the builder adds, whole, where the form orders it
    p.put(path, swap(taken, "\n\n## Hand-back", "\n\n## Searches\n\n**Records:**\n" + fixtures["search-by-terms-of-the-design"] + "\n## Hand-back"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a review's report whose reviewer handed no Searches back and whose builder added the Searches part, a tactical fix naming the builder's Search: it reports nothing of the cold agent's parts",
          passes(got, "== check-settled-report " + path, "0 problems") and "cold agent" not in got[1], shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("and --log-entry appends its entry", passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
