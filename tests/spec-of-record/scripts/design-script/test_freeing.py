"""--free-design: a design freed of each finished or gone design it names, reassessed where its goals are agreed, and
no design written but that one."""
import re

import pytest

from design_script_set import (ABSENT, AGREED_STATES, APPROVED_RESEARCHED, COMPLETE, DRAFTED, FINISHED_STATES, JUDGMENT, NAME, NAMING, READ_AS,
    SKILLS, UNFINISHED, a_workstack, each_naming, passes, report_at, reports, researched, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.action("--free-design")
@pytest.mark.passes
def test_design_is_freed_of_finished_and_gone_names(check):
    p = a_workstack("freed")
    for state, named, design, label in each_naming(p, "freed"):
        others = {k: v for k, v in p.held().items() if k != design}
        before = p.read(design)
        got = p.run("--free-design", design)
        now = p.read(design)
        status = NAMING[state][0]
        same = {k: v for k, v in p.held().items() if k != design} == others
        if state in FINISHED_STATES:
            check("--free-design writes nothing to %s" % label, passes(got, "== free-design %s [%s]" % (NAME, status), "so it is never written") and now == before and same, shown(got))
        elif READ_AS[named] == "unfinished":
            check("--free-design writes nothing to %s" % label,
                  passes(got, "== free-design " + NAME, "its Depends On Designs names no finished or gone design, so nothing is written") and now == before and same, shown(got))
        elif state not in AGREED_STATES:
            check("--free-design frees %s of the name, and appends no entry: its goals are not agreed" % label,
                  passes(got, "== free-design " + NAME, ["freed of %s, %s; its Depends On Designs now none" % (named, READ_AS[named])][0])
                  and "its goals are not agreed in its current major version, so no entry is appended" in got[1]
                  and now == before.replace("**Depends On Designs:** " + named, "**Depends On Designs:** none") and same, shown(got))
        else:
            moved = status in ("approved", "applying")
            entries = re.findall(r"- \*\*Entry:\*\* (\S+)", now)[len(NAMING[state][1]):]
            check("--free-design frees %s, which then stands reassessed: at a new major version, in progress, the cause in its log%s"
                  % (label, ", with the entry of its return to in-progress" if moved else ""),
                  passes(got, "== free-design " + NAME, "reassessed, its goals to agree again")
                  and "**Depends On Designs:** none" in now and "**Version:** 2.0.0 \\\n**Status:** in-progress" in now
                  and entries == ["design-reassessment-1"] + (["entered-2"] if moved else [])
                  and "**Design Version:** 2.0.0 \\\n    **Cause:** changed foundation: %s %s\n" % (named, READ_AS[named]) in now
                  and ("**Reason:** freed" in now) == moved and "Decision" not in now.split("design-reassessment-1")[1] and "Diagnosis" not in now and same,
                  shown(got) + now[-900:])
            form = p.run("--check-design-form", design)
            check("and %s, freed, holds the form of a design" % label, passes(form, "== check-design-form " + NAME, "0 problems"), shown(form))
            again = p.run("--check-design-names", design)
            check("and %s, freed, names no finished or gone design, so an entry of its framing is appended to it" % label,
                  passes(again, "== check-design-names", "0 problems") and p.run("--log-entry", design, "goals-agreed")[0] == 0
                  and "**Version:** 2.0.0" in p.read(design), shown(again))


@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_no_earlier_report_binds_a_freed_design(check):
    for skill in SKILLS:
        p = a_workstack("freed-unbound")
        named = ("" if skill == "design-specs" else "design-specs/") + ABSENT
        design = researched(p, skill=skill, status="approved", log=APPROVED_RESEARCHED)
        bound = p.run("--check-design", design, skill=skill)
        p.put(design, swap(p.read(design), "**Depends On Designs:** none", "**Depends On Designs:** " + named))
        freed = p.run("--free-design", design, skill=skill)
        got = p.run("--check-design", design, skill=skill)
        check("--check-design of %s reads the research of an approved design until it is freed, and, freed of a gone design and reassessed, reads none of it: its Assessed Area rests on a report of no entry of its current major version" % skill,
              passes(bound, "== check-design " + NAME, "0 problems") and passes(freed, "== free-design " + NAME, "moved back from approved to in-progress")
              and reports(got, "== check-design " + NAME, "1 assessed area rests on %s, a report the validation review does not read: no handed-off-judgment entry of the design's current major version names it" % report_at(JUDGMENT, skill=skill))
              and "Read Assessment's Area covers" not in got[1] and "is named by no Search" not in got[1], shown(freed) + shown(got))


def test_freeing_keeps_each_unfinished_name(check):
    for skill in SKILLS:
        p = a_workstack("freed-kept")
        own = lambda n: n if skill == "design-specs" else "design-specs/" + n
        design = p.design(skill=skill, log=DRAFTED, depends="; ".join(own(n) for n in (COMPLETE, UNFINISHED, ABSENT)))
        got = p.run("--free-design", design, skill=skill)
        now = p.read(design)
        check("--free-design of %s removes each finished and each gone name of a design naming several, keeps the unfinished one, and names each in the one Cause" % skill,
              passes(got, "== free-design " + NAME, "freed of %s, finished; %s, gone; its Depends On Designs now %s" % (own(COMPLETE), own(ABSENT), own(UNFINISHED)))
              and "**Depends On Designs:** %s \\" % own(UNFINISHED) in now
              and "**Cause:** changed foundation: %s finished; %s gone\n" % (own(COMPLETE), own(ABSENT)) in now, shown(got))


@pytest.mark.action("--free-design")
@pytest.mark.reports
def test_freeing_refuses_a_design_in_no_plans_folder(check):
    p = a_workstack("freed-outside")
    design = p.design(folder=".ai/plans/design-specs/archive", log=DRAFTED, depends=COMPLETE)
    before = p.held()
    got = p.run("--free-design", design)
    check("--free-design reports a design standing in an archive as standing in no plans folder, and writes nothing",
          reports(got, "== free-design, not freed", "it stands in no plans folder") and p.held() == before, shown(got))
    design = p.design(folder="elsewhere", log=DRAFTED, depends=COMPLETE)
    got = p.run("--free-design", design)
    check("--free-design reports a design standing outside every plans folder the same way", reports(got, "== free-design, not freed", "it stands in no plans folder"), shown(got))
    got = p.run("--free-design", ".ai/plans/design-specs/no-such-file.md")
    check("--free-design of a file that is not there says so, exit 2", got[0] == 2 and "no design document" in got[1], shown(got))
