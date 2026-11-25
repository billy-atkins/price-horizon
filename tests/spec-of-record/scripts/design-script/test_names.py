"""A design naming another: each name of a Depends On Designs read from the plans folders as they stand, by
--check-design-names, --show-workstack and --check-workstack."""
import pytest

from design_script_set import (ABANDONED, ABSENT, AGREED, COMPLETE, FINISHED_STATES, NAME, NAMING, Project, READ_AS, SKILLS, UNFINISHED, a_workstack,
    each_naming, passes, reports, shown)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.action("--check-design-names")
@pytest.mark.reports
def test_names_are_read_from_the_plans_folders(check):
    p = a_workstack("names")
    for state, named, design, label in each_naming(p, "names"):
        got = p.run("--check-design-names", design)
        if state in FINISHED_STATES:
            check("--check-design-names reports nothing of %s, the name its history" % label,
                  passes(got, "== check-design-names " + NAME, "is its history, and nothing follows from it\n0 problems"), shown(got))
        elif READ_AS[named] == "unfinished":
            check("--check-design-names lists %s as blocked, and reports nothing" % label,
                  passes(got, "== check-design-names " + NAME, "blocked by %s, unfinished: it is worked no further than its agreed goals and frame\n0 problems" % named), shown(got))
        else:
            why = "a design of that name stands in a plans folder complete or abandoned" if READ_AS[named] == "finished" else "no design of that name stands in a plans folder"
            check("--check-design-names reports %s as naming a design %s" % (label, READ_AS[named]),
                  reports(got, "== check-design-names " + NAME, ["its Depends On Designs names %s, %s: %s; its foundation has changed" % (named, READ_AS[named], why), "1 problem"]), shown(got))


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
def test_naming_none_passes_and_no_plans_folder_reports(check):
    for skill in SKILLS:
        p = a_workstack("names-none")
        got = p.run("--check-design-names", p.design(skill=skill, log=AGREED), skill=skill)
        check("--check-design-names of %s passes a design naming no design" % skill, passes(got, "== check-design-names " + NAME, "0 problems") and "blocked by" not in got[1], shown(got))
        got = p.run("--check-design-names", p.design(skill=skill, folder=".ai/plans/%s/archive" % skill, log=AGREED, depends=COMPLETE), skill=skill)
        check("--check-design-names of %s reports a design standing in an archive as standing in no plans folder" % skill,
              reports(got, "== check-design-names " + NAME, "it stands in no plans folder, so it is read as no design of the workstack and written by no action"), shown(got))
    p = a_workstack("names-two")
    got = p.run("--check-design-names", p.design(log=AGREED, depends="%s; %s; %s" % (UNFINISHED, COMPLETE, ABSENT)))
    check("--check-design-names reports each finished and each gone name of a design naming several, with which it is, and lists the unfinished one",
          reports(got, "== check-design-names", ["names %s, finished" % COMPLETE, "names %s, gone" % ABSENT, "blocked by %s, unfinished" % UNFINISHED, "2 problems"]), shown(got))
    got = p.run("--check-design-names", p.design(log=AGREED, depends="implement-specs/" + ABSENT))
    check("--check-design-names reads a name of another skill's plans folder from that folder",
          reports(got, "== check-design-names", "names implement-specs/%s, gone" % ABSENT), shown(got))


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
def test_workstack_shown_reads_each_name(check):
    p = a_workstack("stack-shown")
    for state, named, design, label in each_naming(p, "stack-shown"):
        got = p.run("--show-workstack")
        status = NAMING[state][0]
        line = next((l for l in got[1].split("\n") if l.startswith("  " + NAME + " [")), "")
        if state in FINISHED_STATES:
            want = line == "  %s [%s]" % (NAME, status)
            what = "shows nothing of the name of"
        elif READ_AS[named] == "unfinished":
            want = line.startswith("  %s [%s, blocked by %s" % (NAME, status, named)) and "waiting to be freed" not in line
            what = "shows as blocked"
        else:
            want = line.startswith("  %s [%s, waiting to be freed of %s %s" % (NAME, status, named, READ_AS[named])) and "blocked by" not in line \
                and "\n  free: %s [" % NAME in got[1]
            what = "shows as waiting to be freed, and to free first,"
        check("--show-workstack %s %s" % (what, label), got[0] == 0 and "== show-workstack\nWorkstack:" in got[1] and want, line + "\n" + shown(got))
    check("--show-workstack lists each finished design as one that may be deleted or moved, and none standing in the archive",
          "Finished, each one a design that may be deleted or moved at any time:\n" in got[1] and "  %s\n  %s\n" % (COMPLETE, ABANDONED) in got[1].split("Finished, each one")[1]
          and ABSENT not in got[1], shown(got))


@pytest.mark.action("--check-workstack")
@pytest.mark.reports
def test_workstack_checked_reads_each_name(check):
    p = a_workstack("stack-checked")
    for state, named, design, label in each_naming(p, "stack-checked"):
        got = p.run("--check-workstack")
        status = NAMING[state][0]
        if status in ("approved", "applying") and READ_AS[named] == "unfinished":
            check("--check-workstack reports %s" % label,
                  reports(got, "== check-workstack", ["%s, but its Depends On Designs names %s, unfinished: no agent takes a blocked design past its framing" % (status, named), "1 problem"]), shown(got))
        else:
            check("--check-workstack reports nothing of %s" % label, passes(got, "== check-workstack", "0 problems"), shown(got))


@pytest.mark.action("--check-workstack", "--show-workstack")
@pytest.mark.passes("--check-workstack")
@pytest.mark.reports("--show-workstack")
def test_workstack_reads_a_plans_folder_given(check):
    for skill in SKILLS:
        p = a_workstack("stack-folder")
        p.design("code-design", skill="implement-specs", log=AGREED, depends="design-specs/" + UNFINISHED)
        got = p.run("--show-workstack", skill=skill)
        own, other = ("code-design", "design-specs/" + UNFINISHED) if skill == "implement-specs" else ("implement-specs/code-design", UNFINISHED)
        check("--show-workstack of %s names the designs of its own plans folder by their names and those of the folder beside it by that folder" % skill,
              got[0] == 0 and "  %s [in-progress, blocked by %s]" % (own, other) in got[1], shown(got))
        got = p.run("--check-workstack", skill=skill)
        check("--check-workstack of %s passes a workstack in sync" % skill, passes(got, "== check-workstack", "0 problems"), shown(got))
        for flag in ("--show-workstack", "--check-workstack"):
            got = p.run(flag, ".ai/plans/design-specs/archive", skill=skill)
            check("%s of %s refuses a folder that is no plans folder, the archive beneath one among them, exit 2" % (flag, skill),
                  got[0] == 2 and "no plans folder, a skill's plans directory under .ai/plans/" in got[1], shown(got))


@pytest.mark.action("--check-workstack")
@pytest.mark.reports
def test_workstack_loop_is_reported(check):
    p = Project("stack-loop")
    p.design("first", log=AGREED, depends="second")
    p.design("second", log=AGREED, depends="first")
    got = p.run("--check-workstack")
    check("--check-workstack reports designs naming each other in a cycle", reports(got, "== check-workstack", "Depends On Designs runs in a cycle: first -> second -> first"), shown(got))
    p = Project("stack-spawned")
    p.design("first", log=AGREED, Spawned_By="second")
    p.design("second", log=AGREED, Spawned_By="first")
    got = p.run("--check-workstack")
    check("--check-workstack reports designs spawned by each other in a loop", reports(got, "== check-workstack", "Spawned By runs in a loop: first -> second -> first"), shown(got))
