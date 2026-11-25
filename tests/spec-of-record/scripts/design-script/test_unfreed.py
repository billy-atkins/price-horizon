"""The log of a design naming a finished or gone design: no entry is appended until it is freed, a finished design
takes an entry as it stood, and the entries of a freeing are appended by the freeing alone."""
import pytest

from design_script_set import (ABANDONED, ABSENT, CHECK_FIELDS, COMPLETE, DRAFTED, FINISHED_STATES, FREEING, NAMING, READ_AS, a_workstack, naming,
    passes, reports, shown)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


def test_no_entry_is_appended_before_the_freeing(check):
    p = a_workstack("unfreed")
    kinds = {"entered": ("Reason=reopened",), "goals-agreed": (), "plan-change": (), "user-edit": ("Places=docs/guide.md",), "another-round": (),
             "plan-approval": ("Approval=approved",), "apply": (), "self-review": CHECK_FIELDS, "handed-off-judgment": CHECK_FIELDS}
    for state in NAMING:
        if state in FINISHED_STATES:
            continue
        for named in (COMPLETE, ABANDONED, ABSENT):
            for kind, fields in kinds.items():
                design = p.design(text=naming(state, named))
                before = p.held()
                got = p.run("--log-entry", design, kind, *fields)
                check("--log-entry appends no %s entry to a design %s naming a design %s, until it is freed" % (kind, state, READ_AS[named]) + (" (%s)" % named if named == ABANDONED else ""),
                      reports(got, "== log-entry, not logged", ["its Depends On Designs names %s, %s: " % (named, READ_AS[named]) + FREEING]) and p.held() == before, shown(got))


def test_finished_design_takes_an_entry_as_it_stood(check):
    p = a_workstack("finished-naming")
    for state in FINISHED_STATES:
        for named in (COMPLETE, ABSENT):
            design = p.design(text=naming(state, named))
            got = p.run("--log-entry", design, "entered", "Reason=reopened")
            check("--log-entry holds nothing back from a design %s for the %s design it names, the name its history" % (state, READ_AS[named]),
                  passes(got, "== log-entry", "**Entry:** entered-") and "**Depends On Designs:** " + named in p.read(design), shown(got))


def test_entries_of_a_freeing_are_the_freeings_alone(check):
    p = a_workstack("freeing-alone")
    design = p.design(log=DRAFTED)
    before = p.held()
    got = p.run("--log-entry", design, "design-reassessment", "Cause=changed foundation: %s finished" % COMPLETE)
    check("--log-entry refuses a design-reassessment entry whose Cause is a changed foundation, which the freeing alone appends",
          reports(got, "== log-entry, not logged", "an entry of a design freed for a changed foundation, which --free-design alone appends") and p.held() == before, shown(got))
    got = p.run("--log-entry", design, "entered", "Reason=freed")
    check("--log-entry refuses an entered entry whose Reason is freed, which the freeing alone appends",
          reports(got, "== log-entry, not logged", "an entry of a design freed for a changed foundation, which --free-design alone appends") and p.held() == before, shown(got))
