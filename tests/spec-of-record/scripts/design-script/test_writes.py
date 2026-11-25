"""What an action writes: no design but the one it is run on, nothing in the designs naming a design that finishes,
and, of an action that checks or shows, no file at all."""
import pytest

from design_script_set import (AGREED, APPLYING, APPLYING_RESEARCHED, APPROVED, APPROVED_RESEARCHED, COMPLETE, DRAFTED, GOAL, NAME, REVIEW, SKILLS,
    UNFINISHED, a_design, a_report, a_workstack, cold_part, passes, report_at, reports, researched, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.reads("design-script-reports.md", "ferry-research-report", "ferry-review-report")
def test_writing_action_writes_its_own_design_alone(check):
    for skill in SKILLS:
        p = a_workstack("writes")
        own = (lambda n: n) if skill == "design-specs" else (lambda n: "design-specs/" + n)
        named = NAME if skill == "design-specs" else "implement-specs/" + NAME
        p.design("waits-on-it", log=AGREED, depends=named)
        p.design("approved-on-it", status="approved", log=APPROVED, depends=named)
        p.design("code-waits-on-it", skill="implement-specs", log=AGREED, depends=NAME if skill == "implement-specs" else "design-specs/" + NAME)
        p.design("kept-naming-it", folder=".ai/plans/%s/archive" % skill, status="applying", log=APPLYING, depends=NAME)
        p.design(NAME, folder=".ai/plans/%s/archive" % skill, log=DRAFTED, depends=own(COMPLETE))
        design = researched(p, skill=skill, text=swap(a_design(skill=skill, status="applying", log=APPLYING_RESEARCHED, depends=own(COMPLETE)), "without saying when it runs.", "without saying when it runs at all."))
        others = lambda: {k: v for k, v in p.held().items() if k != design}
        before = others()
        check("the workstack made for the test holds designs naming the one acted on, in its plans folder, in the folder beside it and in an archive, and a design of its name in the archive",
              len(before) == 9 and sum(NAME.encode() in v for v in before.values()) >= 5, sorted(before))
        for label, args in (("--stamp-validation", ("--stamp-validation", design)), ("--free-design", ("--free-design", design)), ("--log-entry", ("--log-entry", design, "goals-agreed")),
                            ("--log-entry of a second entry", ("--log-entry", design, "user-edit", "Places=docs/guide.md"))):
            was = p.read(design)
            got = p.run(*args, skill=skill)
            check("%s of %s writes the design it is run on, and leaves every other design byte for byte as it was, an archived one among them" % (label, skill),
                  got[0] == 0 and p.read(design) != was and others() == before, shown(got))
        path = p.put(report_at(REVIEW, skill=skill), cold_part(a_report("review", skill=skill, version="2.0.0")))
        was = p.read(design)
        got = p.run("--take-up-report", path, skill=skill)
        check("--take-up-report of %s writes the report alone, and no design" % skill, got[0] == 0 and "## Hand-back" in p.read(path) and p.read(design) == was and others() == before, shown(got))
        got = p.run("--refresh-links", p.root, skill=skill)
        check("--refresh-links of %s writes no design" % skill, got[0] == 0 and p.read(design) == was and others() == before, shown(got))


def test_design_finishing_leaves_those_naming_it(check):
    p = a_workstack("finishing")
    waits = p.design("waits-on-it", log=AGREED, depends=NAME)
    p.design("kept-naming-it", folder=".ai/plans/design-specs/archive", log=AGREED, depends=NAME)
    design = p.design(status="applying", log=APPLYING)
    others = lambda: {k: v for k, v in p.held().items() if k != design}
    before = others()
    blocked = p.run("--check-design-names", waits)
    # the design finishes: its builder appends its last entries and moves its Status to complete
    bypass = p.run("--log-entry", design, "audit-bypass", "Audit=specs")
    p.put(design, swap(p.read(design), "**Status:** applying", "**Status:** complete"))
    for flag, args in (("--check-design-form", (design,)), ("--check-workstack", ()), ("--show-workstack", ()), ("--check-design-names", (design,)), ("--free-design", (design,)), ("--show-design", (design,))):
        p.run(flag, *args)
    check("a design finishing writes nothing in the designs naming it: each stands byte for byte as it was, one in the archive among them", bypass[0] == 0 and others() == before, shown(bypass))
    got = p.run("--check-design-names", waits)
    check("and a design naming it, blocked by it until then, is read from the files as naming a finished design, to be freed as it is next worked",
          passes(blocked, "== check-design-names", "blocked by %s, unfinished" % NAME) and reports(got, "== check-design-names waits-on-it", "names %s, finished" % NAME), shown(got))
    (p.root / design).unlink()
    got = p.run("--check-design-names", waits)
    check("and, the finished design deleted, as naming a design that is gone", reports(got, "== check-design-names waits-on-it", "names %s, gone" % NAME) and others() == before, shown(got))


@pytest.mark.reads("design-script-reports.md", "ferry-research-report", "ferry-review-report")
def test_no_reading_action_writes_a_file(check):
    p = a_workstack("reads")
    design = researched(p, status="approved", log=APPROVED_RESEARCHED, depends=UNFINISHED)
    path = p.put(report_at(REVIEW), cold_part(a_report("review")))
    before = p.held(".")
    for args in (("--check-cited-headings", design), ("--check-design-form", design), ("--check-target-kind", design), ("--check-design", design), ("--check-workstack",), ("--show-workstack",),
                 ("--show-design", design), ("--check-design-names", design), ("--show-dependents", design, GOAL), ("--show-validation", design), ("--check-handed-back", path),
                 ("--check-audits", design), ("--check-changed-files", design), ("--check-constructs", "docs/guide.md")):
        p.run(*args)
    check("each action that checks or shows writes no file: the project stands byte for byte as it was after each", p.held(".") == before,
          sorted(k for k in set(before) | set(p.held(".")) if before.get(k) != p.held(".").get(k)))
