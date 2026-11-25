"""A round's report once the builder has settled it: --check-settled-report, and --log-entry, which takes the entry's
counts from the report and refuses the entry of a report the check reports."""
import pytest

from design_script_set import (AGREED, BUILDER_PARTS, CAUSE, DRAFTED, FERRY, FINDING, GOAL, JUDGMENT, NAME, Project, REVIEW, ROUND_FIELDS, RULE,
    SKILLS, a_report, a_round, passes, report_at, reports, settled_reports, shown, swap, taken_up)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-reports.md", "ferry-review-report")]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
def test_round_settled_in_its_form_passes(check):
    for skill in SKILLS:
        p, design, path = a_round("settled-passes", skill=skill)
        before = p.held(".ai")
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a taken-up review's report settled with a Cause, and writes nothing" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.held(".ai") == before, shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("--log-entry of %s appends the round's entry, its counts taken from its report and its version the one the report read" % skill,
              passes(got, "== log-entry", "- **Entry:** adversarial-review-1")
              and "**Design Version:** 1.0.1 \\\n    **Model:** a model \\\n    **Effort:** medium \\\n    **Design Flaws:** 0 \\\n    **Implementation Flaws:** 1 \\\n    **Nits:** 0 \\\n    **Dropped:** 0 \\\n    **Led To:** validating" in got[1], shown(got))
        again = p.run("--check-settled-report", path, skill=skill)
        form = p.run("--check-design-form", design, skill=skill)
        check("and the report read again once its entry stands, and the design, hold their forms", passes(again, "== check-settled-report", "0 problems") and passes(form, "== check-design-form", "0 problems"), shown(again) + shown(form))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
@pytest.mark.passes("departures-reasoned")
@pytest.mark.reports("counts-taken-from-the-report")
def test_count_given_an_entry_is_refused(check):
    p, design, path = a_round("counts")
    before = p.read(design)
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, "Nits=3")
    check("--log-entry refuses a count the builder gives, which is taken from the report alone",
          reports(got, "== log-entry, not logged", "a count given, which is taken from the check's report alone: Nits") and p.read(design) == before, shown(got))
    drop = lambda t: swap(swap(swap(t, "**Verdict:** implementation flaw", "**Verdict:** dropped"), "    **Fix Authority:** the builder's \\\n", ""), "    **Cause:** times-by-season \\\n", "    **Departure Reason:** The ferry keeps one set of hours. \\\n")
    p, design, path = a_round("counts-dropped", own=lambda t: drop("## Settlement" + t.split("## Settlement")[1]))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry counts a finding by the last word of the Settlement settling it: one its reviewer marked a flaw and the builder dropped is counted dropped",
          passes(got, "== log-entry", "**Implementation Flaws:** 0 \\\n    **Nits:** 0 \\\n    **Dropped:** 1"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.reports
def test_cold_part_is_held_to_its_fingerprint(check):
    p, design, path = a_round("cold-kept")
    p.put(path, swap(p.read(path), "A visitor in winter plans a crossing the ferry does not make.", "A visitor in winter is left on the quay."))
    got = p.run("--check-settled-report", path)
    now = p.read(path)
    check("--check-settled-report reports a part changed since the take-up, and the report goes back to its cold agent cleared of the builder's parts",
          reports(got, "== check-settled-report", ["the Findings part no longer holds what its cold agent handed back", RULE % "cold-parts-kept", "goes back to its cold agent"])
          and not any(h in now for h in BUILDER_PARTS) and "A visitor in winter is left on the quay." in now, shown(got) + now[-300:])
    p, design, path = a_round("cold-removed")
    text = p.read(path)
    p.put(path, text.split("## Searches")[0] + "## Hand-back" + text.split("## Hand-back")[1])
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry refuses the entry of a report whose cold agent's part was removed since the take-up",
          reports(got, "== log-entry, not logged", "the Searches part its cold agent handed back is removed"), shown(got))
    p = Project("cold-not-taken-up")
    design = p.design(log=DRAFTED)
    path = p.put(report_at(REVIEW), a_report("review"))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry refuses the entry of a cold agent's report the builder settled without taking it up",
          reports(got, "== log-entry, not logged", ["it holds no Hand-back part: a report a cold agent wrote is taken up by --take-up-report", RULE % "cold-parts-kept"]), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
def test_finding_is_settled_once(check):
    twice = lambda t: t.rstrip("\n") + "\n\n  - **Settlement:** times-by-season-again \\" + t.split("- **Settlement:** times-by-season-kept \\")[1]
    settled_reports("a round whose Finding two Settlements settle", twice, "Finding %s is settled by 2 Settlements, not exactly one" % FINDING, RULE % "findings-settled-once")
    none = lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding")
    settled_reports("a round whose Finding no Settlement settles", none, ["Finding %s is settled by 0 Settlements, not exactly one" % FINDING,
                                                                       "Settlement times-by-season-kept settles reviewer-1-another-finding, which no Finding of the report is"], RULE % "report-keys-name-records")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
@pytest.mark.reports
def test_cited_key_names_a_record(check):
    settled_reports("a round whose Settlement names a Cause the report does not hold", lambda t: swap(t, "    **Cause:** times-by-season \\", "    **Cause:** times-by-tide \\"),
                    "Settlement times-by-season-kept names a Cause the report does not hold: times-by-tide", RULE % "report-keys-name-records")
    settled_reports("a round whose Settlement is carried by a step the design does not hold", lambda t: swap(t, "    **Cause:** times-by-season \\", "    **Cause:** times-by-season \\\n    **Carried By:** no-such-step \\"),
                    "Settlement times-by-season-kept is carried by a step the design does not hold: no-such-step", None)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
@pytest.mark.reports
def test_settlement_is_justified(check):
    settled_reports("a round whose Settlement names a goal the design does not hold as justifying it", lambda t: swap(t, "    **Justifying Goals:**\n      - " + GOAL, "    **Justifying Goals:**\n      - guide-says-what-the-ferry-costs"),
                    "Settlement times-by-season-kept's Justifying Goals name guide-says-what-the-ferry-costs, which is no design goal's Name", RULE % "settlements-justified")
    settled_reports("a round whose Settlement holds Justifying Goals where the rules require it", lambda t: swap(t, "**Required By:** the goals", "**Required By:** the rules"),
                    ["Settlement times-by-season-kept holds a Justifying Goals, which its form gives it only where its Required By names the goals",
                     "Settlement times-by-season-kept holds no Justifying Rules, which its form requires where its Required By names the rules"], RULE % "settlements-justified")
    settled_reports("a round whose Settlement gives the user's authority and holds no decision of the user's", lambda t: swap(t, "**Fix Authority:** the builder's", "**Fix Authority:** the user's"),
                    "Settlement times-by-season-kept holds no User Decision, which its form requires where its Fix Authority is the user's", RULE % "settlements-justified")
    flaw = lambda t: swap(t, "**Verdict:** implementation flaw", "**Verdict:** design flaw")
    settled_reports("a round whose Settlement keeps a design flaw on the builder's own authority", flaw,
                    "Settlement times-by-season-kept holds Fix Authority the builder's, where Whose Fix It Is gives the user the call: its Verdict is design flaw", RULE % "settlements-justified")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
@pytest.mark.reports
def test_order_follows_its_lineage(check):
    settled_reports("a round whose Settlement states an order deeper than its lineage gives", lambda t: swap(t, "    **Order:** primary \\\n    **Fix", "    **Order:** secondary \\\n    **Fix"),
                    "Settlement times-by-season-kept states Order secondary, where its lineage gives primary: it lands on no earlier change", RULE % "orders-follow-their-lineage")
    settled_reports("a round whose Changed Place states an order other than its lineage gives", lambda t: swap(t, "            **Order:** primary \\", "            **Order:** tertiary \\"),
                    "states Order tertiary, where its lineage gives primary: it names the findings whose fix it is", RULE % "orders-follow-their-lineage")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
@pytest.mark.reports
def test_departure_is_reasoned(check):
    settled_reports("a round whose Settlement departs from its Finding's Verdict and gives no reason", lambda t: swap(t, "    **Verdict:** implementation flaw \\\n    **Required", "    **Verdict:** nit \\\n    **Required"),
                    "Settlement times-by-season-kept departs from Finding %s in Verdict and holds no Departure Reason" % FINDING, RULE % "departures-reasoned")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
@pytest.mark.reports
def test_settling_reads_cover_the_evidence(check):
    settled_reports("a round whose Settling Reads leave out a place its marked Finding's Evidence names", lambda t: swap(t, "**Settling Reads:**\n  - " + FERRY, "**Settling Reads:**\n  - `docs/guide.md § The Lighthouse`"),
                    "its Settling Reads leave out %s, a place the Evidence of a marked Finding names" % FERRY, RULE % "settling-reads-cover-the-evidence")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
@pytest.mark.reports
def test_round_settled_out_of_its_form_is_reported(check):
    settled_reports("a round holding a marked Finding and no Causes", lambda t: "## Settlement" + swap(t.split("## Settlement")[1], "    **Cause:** times-by-season \\\n", ""),
                    "it holds no Causes part, which its form requires of it", None)
    settled_reports("a round whose Settlement states no Ending", lambda t: swap(t, "**Ending:** its own settling \\\n", ""),
                    "its Settlement holds no Ending, which its form requires where the report owes the statement of how its check ended", None)
    settled_reports("a round whose Cause settling a flaw holds no Misses", lambda t: t.split("    **Misses:**")[0] + "    **Proposed Change:**" + t.split("    **Proposed Change:**")[1],
                    "Cause times-by-season holds no Misses, which its form requires where it settles a design flaw or an implementation flaw", None)
    settled_reports("a round whose revision names no decision it rewrites", lambda t: swap(t, "        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\\n", ""),
                    "Cause times-by-season's Proposed Change holds no Decision Rewritten, which its form requires where its Kind is revision", None)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "search-by-meaning-for-one-season")
def test_tactical_fix_names_a_search_giving_every_place(check, fixtures):
    search = "\n\n" + fixtures["search-by-meaning-for-one-season"]  # a Search of the builder's own, added to the report's Searches
    p, design, path = a_round("tactical")
    text = p.read(path)
    text = swap(text, "\n\n## Hand-back", search + "\n## Hand-back")
    text = swap(text, "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
                "      - **Kind:** tactical fix \\\n        **Search:** each-season-named \\\n        **Reason:** The Objective's meaning stands, and only its wording names one season. \\")
    p.put(path, text)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix naming a Search by meaning, which gives a part of a ranking",
          reports(got, "== check-settled-report", ["Cause times-by-season's tactical fix names Search each-season-named, a search by meaning, which gives a part of a ranking and never every place its defect stands in",
                                                  "Cause times-by-season's tactical fix leaves out %s, a place its Search found" % FERRY]), shown(got))
    p.put(path, swap(text, "        **Search:** each-season-named \\", "        **Search:** no-such-search \\"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix citing a Search the report does not hold",
          reports(got, "== check-settled-report", "Cause times-by-season's Proposed Change cites a Search the report does not hold: no-such-search"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
@pytest.mark.passes
@pytest.mark.reports("earlier-reports-listed", "orders-follow-their-lineage")
def test_second_round_names_the_first_and_lands_deeper(check):
    first = ".ai/tmp/design-specs/%s/reports/adversarial-review/1.md" % NAME
    lands = "`%s § Causes [Cause: %s]`" % (first, CAUSE)

    def second(earlier=True, order="secondary"):
        p, design, path = a_round("second-round")
        logged = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
        text = a_report("review", entry="adversarial-review-2").replace("reviewer-1", "reviewer-2").replace(CAUSE, "times-by-season-again")
        text = swap(text, "        **Delivers:** An Objective giving the first and the last crossing of each season.\n",
                    "        **Delivers:** An Objective giving the first and the last crossing of each season.\n\n    **Lands On:** %s\n" % lands)
        text = swap(text, "    **Cause:** times-by-season-again \\\n", "    **Cause:** times-by-season-again \\\n    **Lands On:** %s \\\n" % lands)
        text = swap(text, "    **Order:** primary \\\n    **Fix", "    **Order:** %s \\\n    **Fix" % order)
        if earlier:
            text = swap(text, "**Earlier Reports:**\n  - none\n\n**Settling", "**Earlier Reports:**\n  - `%s`\n\n**Settling" % first)
            text = swap(text, "    **Earlier Reports:**\n      - none", "    **Earlier Reports:**\n      - `%s`" % first)
        return p, design, taken_up(p, REVIEW, text, n=2), logged

    p, design, path, logged = second()
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a second round naming the first round's report among its Earlier Reports, its finding landing on the first round's change settled as secondary",
          logged[0] == 0 and passes(got, "== check-settled-report " + path, "0 problems"), shown(logged) + shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("and --log-entry appends its entry", passes(got, "== log-entry", "- **Entry:** adversarial-review-2"), shown(got))
    p, design, path, _ = second(earlier=False)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a second round whose Earlier Reports leave out the first round's report",
          reports(got, "== check-settled-report", "its Earlier Reports leave out `%s`, a report of the phase's record" % first), shown(got))
    p, design, path, _ = second(order="primary")
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Settlement stating primary for a finding landing on an earlier round's change",
          reports(got, "== check-settled-report", "states Order primary, where its lineage gives secondary: it lands on %s, whose order is primary" % lands), shown(got))


def no_searches(cold):
    """-> a review's cold part as a reviewer who made no Search hands it back: its Searches part, its last, left out."""
    return cold.split("\n## Searches")[0] + "\n"


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_searches_part_is_the_builders_whole_only_in_a_review_handing_none_back(check, fixtures):
    added = RULE % "cold-parts-kept"
    # a handed-off judgment's report, research, handed back holding no Searches part and taken up, to which a
    # Searches part, the base report's own, is added after the take-up
    whole = a_report("research")
    searches = "\n## Searches" + whole.split("\n## Searches")[1].split("\n## Read Assessments")[0]
    p = Project("judgment-searches-added")
    p.design(log=AGREED)
    path = taken_up(p, JUDGMENT, swap(whole, searches, ""))
    p.put(path, swap(p.read(path), "\n## Read Assessments", searches + "\n## Read Assessments"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Searches part added, after the take-up, to a handed-off judgment's report whose cold agent handed none back: the part is its cold agent's to write",
          reports(got, "== check-settled-report", ["a part its cold agent writes, added after the builder took the report up: Searches", added]), shown(got))
    # a review's report whose reviewer handed Searches back, one line of the reviewer's own Search changed since
    p, design, path = a_round("reviewers-search-changed")
    p.put(path, swap(p.read(path), "every place giving the hours the ferry keeps in winter", "every place giving the hours the ferry keeps"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a review's Searches part its reviewer handed back, a line of the reviewer's own Search changed since the take-up",
          reports(got, "== check-settled-report", ["the Searches part no longer holds what its cold agent handed back", added, "goes back to its cold agent"]), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--check-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "search-by-meaning-for-one-season")
def test_report_sent_back_is_cleared_of_a_searches_part_the_builder_added(check, fixtures):
    # a review whose reviewer handed no Searches back, taken up and settled; the builder adds a Searches part holding
    # a Search of its own, and a line of the reviewer's Findings is changed since the take-up
    p, design, path = a_round("sent-back-cleared", cold=no_searches)
    text = swap(p.read(path), "\n\n## Hand-back", "\n\n## Searches\n\n**Records:**\n" + fixtures["search-by-meaning-for-one-season"] + "\n## Hand-back")
    p.put(path, swap(text, "A visitor in winter plans a crossing the ferry does not make.", "A visitor in winter is left on the quay."))
    got = p.run("--check-settled-report", path)
    now = p.read(path)
    check("--check-settled-report sends a report whose cold part changed back to its cold agent cleared of a Searches part the builder added whole, with every other part the builder wrote, "
          "the cold agent's parts left as they stand",
          reports(got, "== check-settled-report", ["the Findings part no longer holds what its cold agent handed back", RULE % "cold-parts-kept", "goes back to its cold agent"])
          and "## Searches" not in now and "each-season-named" not in now and not any(h in now for h in BUILDER_PARTS)
          and "A visitor in winter is left on the quay." in now and now.startswith("# Check's Report") and "## Findings" in now, shown(got) + now[-400:])
