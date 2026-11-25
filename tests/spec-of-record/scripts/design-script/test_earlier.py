"""Designs written under earlier rules: the old Depends On field, a Reliance, a design approved while it named an
unfinished design, and a log's old values, each read as it was written and written by no action now."""
import pytest

from design_script_set import (ABSENT, APPROVED, BLOCKED, COMPLETE, DRAFTED, NAME, OLD_FIELD, READ_AS, SKILLS, UNFINISHED, a_design, a_workstack,
    naming, passes, reports, shown, swap, with_old_field, with_reliance)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


def test_old_depends_on_field_is_reported_and_unread(check):
    for skill in SKILLS:
        p = a_workstack("old-field")
        named = UNFINISHED if skill == "design-specs" else "design-specs/" + UNFINISHED
        design = p.design(skill=skill, text=with_old_field(a_design(skill=skill, log=DRAFTED), named))
        got = p.run("--check-design-form", design, skill=skill)
        check("--check-design-form of %s reports a design holding the old Depends On field, naming the field" % skill,
              reports(got, "== check-design-form " + NAME, "its header gives Depends On, a field its form does not take; leaves out Depends On Designs, a field its form requires"), shown(got))
        own = NAME if skill == "design-specs" else NAME
        got = p.run("--check-workstack", skill=skill)
        check("--check-workstack of %s reports it, naming the field" % skill,
              reports(got, "== check-workstack", "its header gives Depends On, a field its form does not take\n"), shown(got))
        got = p.run("--show-workstack", skill=skill)
        line = next((l for l in got[1].split("\n") if l.strip().startswith(own + " [")), "")
        check("--show-workstack of %s reads the old field as no name: the design is blocked by nothing" % skill, got[0] == 0 and line.strip() == own + " [in-progress]", line + shown(got))
        got = p.run("--check-design-names", design, skill=skill)
        check("--check-design-names of %s reads the old field as no name" % skill, passes(got, "== check-design-names", "0 problems") and "blocked by" not in got[1], shown(got))
        got = p.run("--free-design", p.design("old-finished", skill=skill, text=with_old_field(a_design("old-finished", skill=skill, log=DRAFTED), ("" if skill == "design-specs" else "design-specs/") + COMPLETE)), skill=skill)
        check("--free-design of %s reads the old field as no name, and writes nothing" % skill, passes(got, "== free-design old-finished", "names no finished or gone design, so nothing is written")
              and OLD_FIELD in p.read(".ai/plans/%s/old-finished.md" % skill), shown(got))
        got = p.run("--log-entry", design, "plan-change", skill=skill)
        check("--log-entry of %s reads the old field as no name: an entry of work past the frame is appended" % skill, passes(got, "== log-entry", "- **Entry:** plan-change-2"), shown(got))


@pytest.mark.reads("design-script-record-parts.md", "reliances-on-one-design")
def test_reliance_is_reported_by_the_form(check):
    p = a_workstack("reliance")
    got = p.run("--check-design-form", p.design(text=with_reliance(a_design(log=DRAFTED, depends=UNFINISHED), UNFINISHED)))
    check("--check-design-form reports a design holding a Reliance on a design its Depends On Designs names",
          reports(got, "== check-design-form", "its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in its Depends On Designs alone")
          and "which its Depends On Designs does not" not in got[1], shown(got))
    got = p.run("--check-design-form", p.design(text=with_reliance(a_design(log=DRAFTED, depends=UNFINISHED), COMPLETE)))
    check("--check-design-form reports a design holding a Reliance on a design its Depends On Designs does not name, naming that design",
          reports(got, "== check-design-form", "its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in its Depends On Designs alone; "
                  "its Reliances name %s, which its Depends On Designs does not" % COMPLETE), shown(got))
    got = p.run("--check-design-names", p.design(text=with_reliance(a_design(log=DRAFTED), COMPLETE)))
    check("and no action reads which designs a design depends on from a Reliance: --check-design-names reports nothing of it", passes(got, "== check-design-names", "0 problems"), shown(got))
    got = p.run("--show-workstack")
    check("nor does --show-workstack", "waiting to be freed" not in got[1] and "  %s [in-progress]" % NAME in got[1], shown(got))


@pytest.mark.reads("design-script-record-parts.md", "reliances-on-one-design")
def test_reliance_brought_to_the_form_is_freed(check):
    for named in (COMPLETE, ABSENT, UNFINISHED):
        p = a_workstack("reliance-brought")
        design = p.design(text=with_reliance(a_design(log=DRAFTED), named))
        check("until its builder brings it to the form, the check of its form reports it", reports(p.run("--check-design-form", design), "== check-design-form", "its Reliances name " + named))
        # the builder next working it brings it to the form: the Reliance's design a name in its Depends On Designs
        p.design(text=a_design(log=DRAFTED, depends=named))
        form = p.run("--check-design-form", design)
        names = p.run("--check-design-names", design)
        if named == UNFINISHED:
            got = p.run("--log-entry", design, "plan-change")
            check("brought to the form, a design that relied on an unfinished design holds its form and waits: an entry of work past its frame is refused",
                  passes(form, "== check-design-form", "0 problems") and passes(names, "== check-design-names", "blocked by " + named)
                  and reports(got, "== log-entry, not logged", "plan-change " + BLOCKED % named), shown(got))
        else:
            got = p.run("--free-design", design)
            check("brought to the form, a design that relied on a design %s is reported by the check of its names, and freed, stands reassessed" % READ_AS[named],
                  passes(form, "== check-design-form", "0 problems") and reports(names, "== check-design-names", "names %s, %s" % (named, READ_AS[named]))
                  and passes(got, "== free-design", "reassessed, its goals to agree again") and "**Version:** 2.0.0" in p.read(design), shown(got))


def test_approved_while_blocked_is_reported_until_moved_back(check):
    for state in ("approved", "applying"):
        p = a_workstack("earlier-approved")
        design = p.design(text=naming(state, UNFINISHED))
        got = p.run("--check-workstack")
        check("--check-workstack reports a design %s under the earlier rules while it names an unfinished design" % state,
              reports(got, "== check-workstack", "%s, but its Depends On Designs names %s, unfinished" % (state, UNFINISHED)), shown(got))
        shown_ = p.run("--show-workstack")
        check("and --show-workstack lists it to move back", "\n  move back: %s [%s, blocked by %s" % (NAME, state, UNFINISHED) in shown_[1], shown(shown_))
        # its builder next working it moves it back: its Status in-progress, and the entry of that move
        p.put(design, swap(p.read(design), "**Status:** " + state, "**Status:** in-progress"))
        moved = p.run("--log-entry", design, "entered", "Reason=" + ("a dependency named" if state == "approved" else "sent back for a dependency"))
        got = p.run("--check-workstack")
        refused = p.run("--log-entry", design, "plan-approval", "Approval=approved")
        check("moved back from %s, it is reported no longer, and waits: an entry of work past its frame is refused" % state,
              passes(moved, "== log-entry", "- **Entry:** entered-2") and passes(got, "== check-workstack", "0 problems")
              and reports(refused, "== log-entry, not logged", "plan-approval " + BLOCKED % UNFINISHED), shown(moved) + shown(got) + shown(refused))


def test_drafted_while_blocked_is_reported_by_no_check(check):
    p = a_workstack("earlier-drafted")
    log = DRAFTED + (("adversarial-review", {"Design Version": "1.0.1"}), ("plan-change", {}))
    design = p.design(log=log, depends=UNFINISHED)
    for flag, args, heading in (("--check-design-form", (design,), "== check-design-form"), ("--check-workstack", (), "== check-workstack"), ("--check-design-names", (design,), "== check-design-names")):
        got = p.run(flag, *args)
        check("%s reports nothing of a design whose steps were drafted and reviewed while it named an unfinished design" % flag, passes(got, heading, "0 problems"), shown(got))
    got = p.run("--log-entry", design, "another-round")
    check("and its work goes no further: an entry of that work is refused", reports(got, "== log-entry, not logged", "another-round " + BLOCKED % UNFINISHED), shown(got))


def test_old_dependency_entry_is_read_and_never_appended(check):
    p = a_workstack("earlier-log")
    design = p.design(log=APPROVED + (("entered", {"Reason": "sent back to reassess"}), ("entered", {"Reason": "a dependency finished"})), status="in-progress")
    got = p.run("--check-design-form", design)
    check("--check-design-form reports nothing of a log holding an entered entry whose Reason the earlier rules gave", passes(got, "== check-design-form", "0 problems"), shown(got))
    before = p.read(design)
    for reason in ("sent back to reassess", "a dependency finished", "a dependency moved back"):
        got = p.run("--log-entry", design, "entered", "Reason=" + reason)
        check("--log-entry appends no entered entry whose Reason is `%s`, a value the entry reason no longer takes" % reason,
              reports(got, "== log-entry, not logged", "an entered entry's Reason is not one of") and p.read(design) == before, shown(got))
