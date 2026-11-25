"""A report once taken up, and what the builder does after: no check then reads a cold part against the design or
the files, a fault in the builder's parts stays with the builder, and a check cut short by a freeing is logged."""
import pytest

from design_script_set import (COMPLETE, DRAFTED, FINDING, GOAL, OBJECTIVE, REVIEW, ROUND_FIELDS, SKILLS, a_report, a_round, a_workstack,
    builder_part, cold_part, passes, report_at, reports, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-reports.md", "ferry-review-report")]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
@pytest.mark.passes
def test_finding_stands_though_its_goal_is_removed(check):
    for skill in SKILLS:
        p, design, path = a_round("goal-removed", skill=skill, own=lambda t: t.replace(GOAL, "guide-gives-each-seasons-hours"))
        p.put(design, p.read(design).replace(GOAL, "guide-gives-each-seasons-hours"))
        before = p.read(path)
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a taken-up report whose Finding names a goal the builder renamed while settling: no check after the take-up reads a cold part against the design" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.read(path) == before, shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("and --log-entry of %s appends its entry" % skill, passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
    p, design, path = a_round("objective-removed", cold=lambda t: swap(t, "    **Affected Goals:**\n      - " + GOAL, "    **Affected Goals:**\n      - %s\n\n    **Affected Step Objectives:**\n      - %s" % (GOAL, OBJECTIVE)))
    p.put(design, p.read(design).replace(OBJECTIVE, "section-gives-each-seasons-crossings"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a taken-up report whose Finding names a step Objective the builder's revision replaced", passes(got, "== check-settled-report " + path, "0 problems"), shown(got))


def test_builders_fault_stays_with_the_builder(check):
    for skill in SKILLS:
        p, design, path = a_round("builders-fault", skill=skill, own=lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding"))
        before = p.read(path)
        for flag, args, heading in (("--check-settled-report", (path,), "== check-settled-report"), ("--log-entry", (design, REVIEW) + ROUND_FIELDS, "== log-entry, not logged")):
            got = p.run(flag, *args, skill=skill)
            check("%s of %s refuses a taken-up report for a Finding the builder's Settlement leaves unsettled, and leaves the report with the builder, its cold parts and its settlement as they stand" % (flag, skill),
                  reports(got, heading, "Finding %s is settled by 0 Settlements, not exactly one" % FINDING) and "goes back to its cold agent" not in got[1] and p.read(path) == before, shown(got))


def test_check_cut_short_by_a_freeing_is_logged(check):
    cut = lambda t: swap(swap(swap("## Settlement" + t.split("## Settlement")[1], "**Ending:** its own settling", "**Ending:** cut short, a design reassessment for a changed foundation"),
                              "    **Fix Authority:** the builder's \\\n    **Cause:** times-by-season \\\n", "    **Fix Authority:** the user's \\\n    **User Decision:** taken by a changed foundation \\\n"),
                         "The Objective was revised to give each season's first and last crossing.", "The design was freed, and is made afresh.")
    for skill in SKILLS:
        p = a_workstack("cut-short")
        design = p.design(skill=skill, log=DRAFTED, depends=("" if skill == "design-specs" else "design-specs/") + COMPLETE)
        text = a_report("review", skill=skill)
        path = p.put(report_at(REVIEW, skill=skill), cold_part(text))
        back = p.run("--check-handed-back", path, skill=skill)
        freed = p.run("--free-design", design, skill=skill)
        up = p.run("--take-up-report", path, skill=skill)
        p.put(path, p.read(path).rstrip("\n") + "\n\n" + cut(builder_part(text)))
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a round handed back before its design was freed, settled as cut short by the design reassessment, its findings taken by the changed foundation" % skill,
              back[0] == 0 and freed[0] == 0 and up[0] == 0 and passes(got, "== check-settled-report " + path, "0 problems"), shown(back) + shown(freed) + shown(up) + shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        now = p.read(design)
        check("--log-entry of %s appends its entry after the freeing, at the version its report read, though the goals of the new major version are not yet agreed" % skill,
              passes(got, "== log-entry", "- **Entry:** adversarial-review-1") and "**Design Version:** 1.0.1 \\\n    **Model:**" in got[1] and "**Version:** 2.0.0 \\" in now, shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and the design of %s holds its form" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))
