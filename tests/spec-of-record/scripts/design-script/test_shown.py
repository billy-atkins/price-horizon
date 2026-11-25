"""--show-design: the header and the goals of a design standing in a plans folder, and nothing else of it."""
import pytest

from design_script_set import (ABSENT, DRAFTED, GOAL, NAME, OUTCOME, PROBLEM_WORDS, SKILLS, STEP, STEP_WORDS, UNFINISHED, a_design, a_workstack,
    part, passes, reports, shown, swap, with_old_field)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.action("--show-design")
@pytest.mark.passes
def test_header_and_goals_are_shown(check):
    for skill in SKILLS:
        p = a_workstack("shown")
        p.design("code-design", skill="implement-specs", log=DRAFTED)
        design = p.design(skill=skill, log=DRAFTED, depends=("" if skill == "design-specs" else "design-specs/") + UNFINISHED)
        before = p.held()
        for given in (design, NAME):
            got = p.run("--show-design", given, skill=skill)
            check("--show-design of %s shows the header and the goals of a design given by its %s, and nothing else of it" % (skill, "file" if given == design else "name"),
                  passes(got, "== show-design %s [in-progress]" % NAME, "0 problems")
                  and all(w in got[1] for w in ("Name: " + NAME, "Version: 1.0.1", "Status: in-progress", "Depends On Designs: ", "Validated: none",
                                                "Design Goals:\n  - Name: %s\n    Description: The guide says when the ferry runs." % GOAL))
                  and not any(w in got[1] for w in (PROBLEM_WORDS, STEP_WORDS, STEP, OUTCOME, "Entry:")) and p.held() == before, shown(got))
        other = "implement-specs/code-design" if skill == "design-specs" else "design-specs/" + UNFINISHED
        got = p.run("--show-design", other, skill=skill)
        check("--show-design of %s shows a design of the plans folder beside its own, by the name a Depends On Designs gives it" % skill,
              passes(got, "== show-design %s [in-progress]" % other, "0 problems") and "Name: " + other.split("/")[1] in got[1], shown(got))
    p = a_workstack("shown-unstated")
    got = p.run("--show-design", p.design(status="not-started"))
    check("--show-design shows the goals of a design that has stated none as the section holds them", passes(got, "== show-design %s [not-started]" % NAME, "Design Goals:\n  Not yet stated.\n0 problems"), shown(got))


@pytest.mark.action("--show-design")
@pytest.mark.reports
def test_older_form_is_shown_as_far_as_it_reads(check):
    p = a_workstack("shown-older")
    text = with_old_field(a_design(log=DRAFTED), UNFINISHED)
    text = swap(text, "**Kind:** documentation \\\n", "")
    text = part(text, "## Design Goals", "The guide is to say when the ferry runs.")
    design = p.design(text=text)
    before = p.held()
    got = p.run("--show-design", design)
    check("--show-design shows each field an older design holds, names each missing or not valid, and writes nothing",
          reports(got, "== show-design %s [in-progress]" % NAME, ["Name: " + NAME, "Depends On: " + UNFINISHED, "Design Goals:\n  The guide is to say when the ferry runs.",
                                                                 "Missing or not valid, so the design is old and suspect, and stays as it is until its own builder takes it up:",
                                                                 "its header", "Kind is not ", "Design Goals has no Records field"])
          and PROBLEM_WORDS not in got[1] and p.held() == before, shown(got))
    got = p.run("--show-design", p.design("no-goals", text=part(a_design("no-goals", status="in-progress", log=DRAFTED), "## Design Goals", None)))
    check("--show-design names the goals' section where a design holds none", reports(got, "== show-design no-goals", "it holds no Design Goals section"), shown(got))


@pytest.mark.action("--show-design")
@pytest.mark.reports
def test_nothing_shown_outside_the_plans_folders(check):
    p = a_workstack("shown-outside")
    before = p.held()
    for given, label in ((".ai/plans/design-specs/archive/%s.md" % ABSENT, "by its file in an archive"), (ABSENT, "by its name, standing in an archive alone"),
                         (p.design(folder="elsewhere", log=DRAFTED), "by its file outside every plans folder"), ("no-such-design", "by a name no design takes")):
        got = p.run("--show-design", given)
        check("--show-design shows nothing of a design given %s, and says it stands in no plans folder" % label,
              reports(got, "== show-design", "no design of that name stands in a plans folder, so nothing of it is shown")
              and "Name:" not in got[1] and "Design Goals" not in got[1], shown(got))
    check("and writes nothing", {k: v for k, v in p.held().items()} == before)
