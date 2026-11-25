"""A design's research, and the log's gates on a check's entry: each place read lying in an assessed area, an area
assessed again naming its cause, the goals agreed before any check, an entry standing at the version its report read,
an audit's sub-scopes, and the research binding a design read together."""
import pytest

from design_script_set import (AGREED, APPLYING, APPLYING_RESEARCHED, APPROVED_RESEARCHED, BY_TERMS, CHECK_FIELDS, COVERS, DRAFTED, FERRY, GOAL,
    JUDGMENT, LIGHTHOUSE, NAME, Project, RESEARCH, ROUND_FIELDS, RULE, SKILLS, a_clean_report, a_design, a_report, cold_part, outside_every_area,
    passes, report_at, reports, researched, second_share, shown, swap, taken_up)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-reports.md", "ferry-research-report")]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]
@pytest.mark.passes
@pytest.mark.reports
def test_each_read_lies_in_an_assessed_area(check):
    whole = cold_part(a_report("research"))
    p = Project("reads-assessed")
    p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), swap(whole, "**Reads:**\n  - " + FERRY, "**Reads:**\n  - %s\n  - %s" % (FERRY, LIGHTHOUSE)))
    for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
        got = p.run(flag, path)
        check("%s reports a research report whose Reads hold a place lying within no Read Assessment's Area" % flag,
              reports(got, heading, "%s, a place its Reads hold, lies within no Read Assessment's Area" % LIGHTHOUSE), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "**Reads:**\n  - " + FERRY, "**Reads:**\n  - %s\n  - `.ai/plans/design-specs/%s.md`" % (FERRY, NAME)))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back passes a research report each of whose Reads lies in an Area it assesses, the design document aside", passes(got, "== check-handed-back", "0 problems"), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "    **Impact:**\n      - changes", "    **Impact:**\n      - changes\n      - none"))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a Read Assessment whose Impact holds none beside another", reports(got, "== check-handed-back", "Impact is not a list holding none alone"), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "    **Reason:** The section names the ferry and is where its times are to stand. \\\n    **Goals:**\n      - " + GOAL,
                                           "    **Reason:** The section names the ferry and is where its times are to stand. \\\n    **Goals:**\n      - guide-says-what-the-ferry-costs"))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a Read Assessment naming a goal the design does not hold", reports(got, "== check-handed-back", "Goals name guide-says-what-the-ferry-costs, which is no design goal's Name"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "steering-decisions-of-one-steer")
def test_area_assessed_again_names_a_cause(check):
    first = ".ai/tmp/design-specs/%s/reports/handed-off-judgment/1.md" % NAME
    p, path = second_share()
    for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
        got = p.run(flag, path)
        check("%s reports a research report assessing again an Area a binding report assesses, naming no cause" % flag,
              reports(got, heading, ["Read Assessment %s assesses again an Area %s already assesses, and names no cause in its Assessed Again For" % (FERRY, first), RULE % "area-reassessments-name-their-cause"]), shown(got))
    p, path = second_share(cause="steer-1")
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a cause naming a set of steers the design's log does not hold",
          reports(got, "== check-handed-back", "names steer-1, a set's entry the design's log does not hold"), shown(got))
    p, path = second_share(cause="a second look")
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a cause that is neither a set of steers nor a finding", reports(got, "== check-handed-back", "names a second look, neither a set's steer entry nor a finding cited as a place"), shown(got))
    p, path = second_share(cause="steer-1", steer=True)
    got = p.run("--check-handed-back", path)
    check("--check-handed-back passes a research report assessing an Area again for a set of steers logged after the report that assessed it", passes(got, "== check-handed-back", "0 problems"), shown(got))
    got = p.run("--take-up-report", path)
    check("and --take-up-report takes it up", passes(got, "== take-up-report " + path, "0 problems"), shown(got))
    p, path = second_share(area=LIGHTHOUSE)
    got = p.run("--check-handed-back", path)
    check("--check-handed-back asks no cause of a research report assessing an Area no binding report assesses", passes(got, "== check-handed-back", "0 problems"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
@pytest.mark.passes
@pytest.mark.reports
def test_no_checks_entry_before_the_goals_agreement(check):
    for skill in SKILLS:
        p = Project("goals-gate")
        design = p.design(skill=skill, log=(("entered", {"Reason": "taken up"}),))
        taken_up(p, JUDGMENT, a_report("research", skill=skill, version="0.1.0").replace("**Design Version:** 0.1.0 \\\n", "**Design Version:** 1.0.0 \\\n"), skill=skill)
        before = p.read(design)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses a check's entry before the user's agreement to the goals" % skill,
              reports(got, "== log-entry, not logged", ["a check's entry with no goals-agreed entry before it in its major version", RULE % "goals-agreed-before-checks"]) and p.read(design) == before, shown(got))
        agreed = p.run("--log-entry", design, "goals-agreed", skill=skill)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s appends it once the goals are agreed" % skill, agreed[0] == 0 and passes(got, "== log-entry", "- **Entry:** handed-off-judgment-1"), shown(got))
        for flag in ("--check-design-form", "--check-design"):
            got = p.run(flag, p.design("gate-in-a-log", skill=skill, log=(("entered", {"Reason": "taken up"}),) + RESEARCH), skill=skill)
            check("%s of %s reports a log holding a check's entry with no goals-agreed entry before it" % (flag, skill),
                  reports(got, "== %s gate-in-a-log" % flag[2:], ["log entry handed-off-judgment-1 is a check's entry with no goals-agreed entry before it in its major version", RULE % "goals-agreed-before-checks"]), shown(got))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
@pytest.mark.passes
@pytest.mark.reports
def test_entry_stands_at_the_version_read(check):
    for skill in SKILLS:
        p = Project("version-read")
        design = p.design(skill=skill, log=DRAFTED)
        path = taken_up(p, JUDGMENT, a_report("research", skill=skill, version="1.0.0"), skill=skill)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s stamps a check's entry at the version its report read, an earlier one the log held, and leaves the header at the log's" % skill,
              passes(got, "== log-entry", "**Design Version:** 1.0.0 \\\n    **Model:**") and "**Version:** 1.0.1 \\" in p.read(design), shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and --check-design-form of %s passes the log it wrote" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))
        p = Project("version-never-held")
        design = p.design(skill=skill, log=DRAFTED)
        taken_up(p, JUDGMENT, a_report("research", skill=skill, version="1.4.0"), skill=skill)
        before = p.read(design)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses a check's entry whose report read a version the log never held" % skill,
              reports(got, "== log-entry, not logged", ["Reading holds Design Version 1.4.0, a version the design's log never held", RULE % "entry-at-the-version-read"]) and p.read(design) == before, shown(got))
        for flag in ("--check-design-form", "--check-design"):
            got = p.run(flag, p.design("version-in-a-log", skill=skill, log=AGREED + (("handed-off-judgment", {"Design Version": "1.4.0"}),)), skill=skill)
            check("%s of %s reports a log holding a check's entry at a version the log never held before it" % (flag, skill),
                  reports(got, "== %s version-in-a-log" % flag[2:], ["log entry handed-off-judgment-1's Design Version is 1.4.0, a version its log never held before it", RULE % "entry-at-the-version-read"]), shown(got))
    p = Project("version-form")
    got = p.run("--check-design-form", p.design(text=swap(a_design(log=DRAFTED), "**Version:** 1.0.1", "**Version:** 1.2.0")))
    check("--check-design-form reports a header whose Version is not the one its log gives", reports(got, "== check-design-form", "Version is 1.2.0, where its log gives 1.0.1"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_audit_entry_holds_sub_scopes(check):
    for skill in SKILLS:
        p = Project("sub-scopes")
        for flag in ("--check-design-form", "--check-design"):
            good = p.run(flag, researched(p, skill=skill, status="applying", log=APPLYING_RESEARCHED + (("audit-specs", {"Design Version": "1.0.1", "Settled Sub-scopes": "documentation; other"}),)), skill=skill)
            check("%s of %s passes a log whose audit entry holds sub-scopes alone" % (flag, skill), passes(good, "== %s %s" % (flag[2:], NAME), "0 problems"), shown(good))
            got = p.run(flag, researched(p, skill=skill, status="applying", log=APPLYING_RESEARCHED + (("audit-specs", {"Design Version": "1.0.1", "Settled Sub-scopes": "documentation; the-attic"}),)), skill=skill)
            check("%s of %s reports a log whose audit entry names what is no sub-scope" % (flag, skill),
                  reports(got, "== %s %s" % (flag[2:], NAME), "an audit-specs entry's Settled Sub-scopes names the-attic, not one of core-canon, skills, application-specs, documentation, other"), shown(got))
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put(report_at("audit-specs", skill=skill), a_clean_report("audit-specs"))
        before = p.read(design)
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=the-attic", skill=skill)
        check("--log-entry of %s refuses an audit's entry naming what is no sub-scope" % skill, reports(got, "== log-entry, not logged", "Settled Sub-scopes names the-attic, not one of") and p.read(design) == before, shown(got))
        kept, dropped = ("documentation", "core-canon") if skill == "design-specs" else ("other", "documentation")
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=" + dropped, skill=skill)
        check("--log-entry of %s refuses an audit's entry whose Settled Sub-scopes drop a sub-scope holding a file the design changed" % skill,
              reports(got, "== log-entry, not logged", "the audit-specs entry's Settled Sub-scopes drop %s, each holding a file the design changed" % kept) and p.read(design) == before, shown(got))
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=%s; %s" % (dropped, kept), skill=skill)
        check("--log-entry of %s appends an audit's entry whose Settled Sub-scopes keep each sub-scope the design changed" % skill, passes(got, "== log-entry", "**Settled Sub-scopes:** %s; %s" % (dropped, kept)), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
@pytest.mark.reports
def test_binding_research_is_read_together(check):
    for skill in SKILLS:
        p = Project("research-union")
        area = LIGHTHOUSE
        path = p.put(report_at(JUDGMENT, skill=skill), outside_every_area(a_report("research", skill=skill)) if skill == "design-specs"
                     else swap(a_report("research", skill=skill), "    **Places:**\n      - `src/ferry.py`", "    **Places:**\n      - `src/ferry.py`\n      - " + LIGHTHOUSE))
        design = p.design(skill=skill, log=AGREED + RESEARCH + (("plan-change", {}),))
        for flag in ("--check-design", "--stamp-validation"):
            got = p.run(flag, design, skill=skill)
            check("%s of %s reports, of a design not yet approved, a place its research's Search holds that no Area it assesses covers, and a goal no Search by terms names" % (flag, skill),
                  reports(got, "== " + ("check-design " + NAME if flag == "--check-design" else "stamp-validation, not stamped"),
                          [COVERS % (path, area), RULE % "research-covers-its-matches", BY_TERMS, RULE % "goals-searched-over-every-operative-file"]), shown(got))


@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_first_builder_check_reads_the_research(check):
    p = Project("research-at-the-entry")
    design = p.design(log=AGREED + RESEARCH + (("plan-change", {}),))
    path = p.put(report_at(JUDGMENT), outside_every_area(a_report("research")))
    own = p.put(report_at("self-review"), a_report("self-review"))
    before = p.read(design)
    for flag, args, heading in (("--check-settled-report", (own,), "== check-settled-report"), ("--log-entry", (design, "self-review") + CHECK_FIELDS, "== log-entry, not logged")):
        got = p.run(flag, *args)
        check("%s refuses a self-review standing first after research whose Search holds a place no Area covers, and whose goal no Search by terms names" % flag,
              reports(got, heading, [COVERS % (path, LIGHTHOUSE), BY_TERMS]) and p.read(design) == before, shown(got))


def test_approved_designs_research_is_not_read_again(check):
    for skill in SKILLS:
        for status, log in (("approved", APPROVED_RESEARCHED), ("applying", APPLYING_RESEARCHED), ("complete", APPLYING_RESEARCHED)):
            p = Project("research-frozen")
            design = p.design(skill=skill, status=status, log=log)
            p.put(report_at(JUDGMENT, skill=skill), outside_every_area(a_report("research")) if skill == "design-specs"
                  else swap(a_report("research", skill=skill), "    **Places:**\n      - `src/ferry.py`", "    **Places:**\n      - `src/ferry.py`\n      - " + LIGHTHOUSE))
            got = p.run("--check-design", design, skill=skill)
            check("--check-design of %s reports nothing of the research of a design that is %s: no place as unassessed, and no goal as unsearched" % (skill, status),
                  passes(got, "== check-design " + NAME, "0 problems"), shown(got))
