"""The builder's self-review: its entry and the script output written into its report, the Builder Checks required of
it, the Traces its phase gives it, and its reading after a round's change."""
import pytest

from design_script_set import (CAUSE, CHECK_FIELDS, DRAFTED, FERRY, FINDING, LIGHTHOUSE, LINKED, NAME, Project, REVIEW, RE_EVALUATION, ROUND_FIELDS,
    SELF, SKILLS, a_check, a_design, a_report, a_round, passes, report_at, reports, shown, swap, with_checks)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.passes
def test_entry_appended_with_its_script_output(check):
    for skill in SKILLS:
        p = Project("self-review")
        design = p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(SELF, skill=skill), a_report("self-review", skill=skill))
        before = p.held(".ai")
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a self-review's report holding each Builder Check required of it, and writes nothing" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.held(".ai") == before, shown(got))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s appends its entry, and writes the output of the checks a self-review before the apply runs into its report, where the form orders the part" % skill,
              passes(got, "== log-entry", "- **Entry:** self-review-1") and "## Script Output\n\n```text\n$ --check-cited-headings %s\n" % design in now
              and "$ --check-target-kind %s\n== check-target-kind %s\n0 problems\n\nexit 0\n" % (design, NAME) in now
              and now.index("## Builder Checks") < now.index("## Script Output") < now.index("## Settlement") and "check-kept-tests" not in now, shown(got) + now[-900:])


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.reports
def test_each_required_builder_check_is_held(check):
    whole = a_report("self-review")
    for label, text, said in (("no check of the work it hands on", swap(whole, LINKED, ""), "no Builder Check of linked work, which is required of it"),
                              ("no check of its steers", whole.split("  - **Check:** steers-read")[0] + "  - **Check:** work-handed-on" + whole.split("  - **Check:** work-handed-on")[1],
                               "no Builder Check of steers against the user's messages, which is required of it")):
        p = Project("builder-checks")
        design = p.design(log=DRAFTED)
        path = p.put(report_at(SELF), text)
        before = p.read(design)
        got = p.run("--check-settled-report", path)
        check("--check-settled-report reports a self-review holding " + label, reports(got, "== check-settled-report", said), shown(got))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        check("--log-entry refuses the entry of a self-review holding " + label, reports(got, "== log-entry, not logged", said) and p.read(design) == before, shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
@pytest.mark.reports
def test_first_self_review_re_evaluates_the_problem(check):
    for skill in SKILLS:
        whole = a_report("self-review", skill=skill)
        p = Project("re-evaluation")
        design = p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(SELF, skill=skill), swap(whole, RE_EVALUATION, ""))
        before = p.read(design)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses the first self-review of a major version recording no re-evaluation of the Problem" % skill,
              reports(got, "== log-entry, not logged", "no Builder Check of problem re-evaluation, which is required of it") and p.read(design) == before, shown(got))
        text = swap(a_design(skill=skill, log=DRAFTED), "without saying when it runs.", "without saying when it runs, though %s gives the keeper's hours." % LIGHTHOUSE)
        design = p.design(skill=skill, text=text)
        p.put(path, whole)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses one whose re-evaluation leaves out a place the Problem cites" % skill,
              reports(got, "== log-entry, not logged", "its Builder Checks of problem re-evaluation leave out " + LIGHTHOUSE) and p.read(design) == text, shown(got))
        p.put(path, swap(whole, "      - `docs/guide.md § The Ferry`\n\n    **Result:** The section still", "      - `docs/guide.md § The Ferry`\n      - %s\n\n    **Result:** The section still" % LIGHTHOUSE))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s appends one whose re-evaluation covers each place the Problem cites" % skill, passes(got, "== log-entry", "- **Entry:** self-review-1"), shown(got))
        p.put(report_at(SELF, 2, skill=skill), swap(a_report("self-review", skill=skill, entry="self-review-2"), RE_EVALUATION, ""))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s asks no re-evaluation of a later self-review of the same major version" % skill, passes(got, "== log-entry", "- **Entry:** self-review-2"), shown(got))
    p = Project("re-evaluation-again")
    log = DRAFTED + ((SELF, {}), ("design-reassessment", {"Cause": "changed foundation: quay-rebuilt finished"}), ("goals-agreed", {}), ("plan-change", {}))
    design = p.design(log=log)
    p.put(report_at(SELF, 2), swap(a_report("self-review", entry="self-review-2", version="2.0.1"), RE_EVALUATION, ""))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry asks the re-evaluation again of the first self-review of the major version a design reassessment starts",
          reports(got, "== log-entry, not logged", "no Builder Check of problem re-evaluation, which is required of it"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "hours-decision-table", "traces-of-one-mechanism")
def test_each_mechanism_is_traced(check, fixtures):
    whole = a_report("self-review")
    # the guide's section The Ferry given a Decision Table, a mechanism, and the Traces part of a report tracing it
    TABLE, TRACE = "\n" + fixtures["hours-decision-table"], fixtures["traces-of-one-mechanism"] + "\n## Builder Checks"
    p = Project("traces")
    p.put("docs/guide.md", swap(fixtures["island-guide"], "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n" + TABLE))
    design = p.design(log=DRAFTED)
    path = p.put(report_at(SELF), whole)
    before = p.read(design)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a self-review holding no Trace of a Decision Table a step's What names", reports(got, "== check-settled-report", "no Trace of the Decision Table at " + FERRY), shown(got))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses its entry", reports(got, "== log-entry, not logged", "no Trace of the Decision Table at " + FERRY) and p.read(design) == before, shown(got))
    p.put(path, swap(whole, "## Builder Checks", TRACE))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a self-review before the apply whose Trace of the mechanism holds the outcome of the mechanism's test", passes(got, "== check-settled-report", "0 problems"), shown(got))
    p.put(path, swap(whole, "## Builder Checks", swap(TRACE, " \\\n    **Outcome:** name the mechanism", "")))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Trace before the apply holding no Outcome", reports(got, "== check-settled-report", "Trace hours-by-season holds no Outcome, which its form requires where the report is a self-review's before the apply"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_after_a_round_reads_cover_each_miss(check):
    p, design, path = a_round("after-a-round")
    logged = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    worked = a_check("round-worked", "worked case", "%s § Causes [Cause: %s]" % (path, CAUSE), "%s § Findings [Finding: %s]" % (path, FINDING))
    own = p.put(report_at(SELF), with_checks(a_report("self-review"), worked))
    got = p.run("--check-settled-report", own)
    check("--check-settled-report passes a self-review after a round whose Reads cover each place a Miss names and whose worked case covers the round's Cause and its flaw",
          logged[0] == 0 and passes(got, "== check-settled-report", "0 problems"), shown(logged) + shown(got))
    p.put(own, swap(with_checks(a_report("self-review"), worked), "\n  - `docs/guide.md`\n", "\n"))
    got = p.run("--check-settled-report", own)
    check("--check-settled-report reports one whose Reads leave out a place a Miss of the phase names", reports(got, "== check-settled-report", "its Reads leave out %s, a place a Miss of the phase names" % FERRY), shown(got))
    p.put(own, a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses one working no case of the round's change", reports(got, "== log-entry, not logged", "no Builder Check of worked case, which is required of it"), shown(got))
    p.put(own, with_checks(a_report("self-review"), a_check("round-worked", "worked case", "%s § Causes [Cause: %s]" % (path, CAUSE))))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses one whose worked case leaves out the round's flaw",
          reports(got, "== log-entry, not logged", "its Builder Checks of worked case leave out `%s § Findings [Finding: %s]`" % (path, FINDING)), shown(got))
