"""The log of a design naming an unfinished design: an entry that begins or continues work past the frame is refused,
and each other entry is appended."""
import pytest

from design_script_set import (BLOCKED, FINISHED_STATES, NAMING, PAST_THE_FRAME, SKILLS, UNFINISHED, a_workstack, log_kinds, naming, other_entry,
    own_lib, passes, reports, shown)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


def test_work_past_the_frame_is_refused_when_blocked(check):
    p = a_workstack("blocked")
    check("the tests hold each kind of entry the script refuses a blocked design", set(PAST_THE_FRAME) == set(own_lib().PAST_THE_FRAME), sorted(own_lib().PAST_THE_FRAME))
    for skill in SKILLS:
        named = UNFINISHED if skill == "design-specs" else "design-specs/" + UNFINISHED
        for state in NAMING:
            if state in FINISHED_STATES or (skill == "implement-specs" and state != "in progress after its goals"):
                continue
            for kind, fields in PAST_THE_FRAME.items():
                design = p.design(skill=skill, text=naming(state, named, skill=skill))
                before = p.held()
                got = p.run("--log-entry", design, kind, *fields, skill=skill)
                check("--log-entry of %s refuses a %s entry to a design %s naming an unfinished design" % (skill, kind, state),
                      reports(got, "== log-entry, not logged", kind + " " + BLOCKED % named) and p.held() == before, shown(got))


@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report", "review-report-finding-nothing", "audit-report-finding-nothing")
def test_each_other_entry_is_appended_when_blocked(check):
    kinds = [k for k in log_kinds() if k not in PAST_THE_FRAME and k != "reassessment"]
    for kind in kinds:
        p = a_workstack("blocked-appended")
        applied = kind in ("post-apply-review", "audit-specs", "verify-spec-implementation", "direct-edit", "audit-bypass", "passes-choice")
        state = "applying" if applied else "in progress after its goals"
        design = p.design(text=naming(state, UNFINISHED))
        fields = other_entry(p, design, kind)
        if fields is None:
            check("the tests give an entry of the kind %s its fields, a kind the canon gives a design's log" % kind, False)
            continue
        got = p.run("--log-entry", design, kind, *fields)
        check("--log-entry appends a %s entry to a design %s naming an unfinished design, an entry of no work past its frame" % (kind, state),
              passes(got, "== log-entry", "- **Entry:** %s-" % kind) and "**Depends On Designs:** " + UNFINISHED in p.read(design), shown(got))
    p = a_workstack("blocked-complete")
    design = p.design(text=naming("complete", UNFINISHED))
    got = p.run("--log-entry", design, "plan-change")
    check("--log-entry holds nothing back from a complete design for the unfinished design it names", passes(got, "== log-entry", "- **Entry:** plan-change-"), shown(got))
