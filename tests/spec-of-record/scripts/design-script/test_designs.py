"""One design document checked and shown: its form, the headings it cites, its Target against its Kind, the
validation review and its stamp, and the parts of a design naming a part."""
import pytest

from design_script_set import (AGREED, APPLYING, APPLYING_RESEARCHED, APPROVED, APPROVED_RESEARCHED, DRAFTED, GOAL, NAME, NOT_DRAFTED, OBJECTIVE,
    OUTCOME, Project, SKILLS, a_design, part, passes, reports, researched, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
def test_form_passes_a_design_in_its_form(check):
    p = Project("form")
    for status, log in (("not-started", ()), ("in-progress", AGREED), ("in-progress", DRAFTED), ("approved", APPROVED), ("applying", APPLYING)):
        got = p.run("--check-design-form", p.design(status=status, log=log))
        check("--check-design-form passes a design made for the tests, %s with %d log entries" % (status, len(log)),
              passes(got, "== check-design-form " + NAME, "0 problems"), shown(got))


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
def test_form_reports_a_field_out_of_the_form(check):
    p = Project("form-field")
    got = p.run("--check-design-form", p.design(text=a_design().replace("**Spawned By:** none \\\n", "**Spawned By:** none \\\n**Reviewed By:** nobody \\\n")))
    check("--check-design-form reports a header holding a field its form does not take, naming the field",
          reports(got, "== check-design-form " + NAME, ["its header", "Reviewed By"]), shown(got))


@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
def test_cited_heading_that_stands_passes(check):
    for skill in SKILLS:
        p = Project("cited")
        got = p.run("--check-cited-headings", p.design(skill=skill, log=DRAFTED), skill=skill)
        check("--check-cited-headings of %s passes a design whose every cited heading stands" % skill,
              passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))


@pytest.mark.action("--check-cited-headings")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
def test_cited_heading_that_does_not_stand_is_reported(check, fixtures):
    for skill in SKILLS:
        p = Project("cited-broken")
        text = swap(a_design(skill=skill, log=DRAFTED), "and `docs/guide.md § The Ferry` names", "and `docs/guide.md § The Harbour` names")
        got = p.run("--check-cited-headings", p.design(skill=skill, text=text), skill=skill)
        check("--check-cited-headings of %s reports a cited heading its file does not hold, as broken" % skill,
              reports(got, "== check-cited-headings", ["BROKEN", "§ The Harbour", "no such heading", "1 broken"]), shown(got))
    p = Project("cited-none")
    got = p.run("--check-cited-headings", p.put("notes.md", fixtures["notes-citing-nothing"]))
    check("--check-cited-headings of a proposal citing nothing says so and exits 2", got[0] == 2 and "no cross-file citations found" in got[1], shown(got))


@pytest.mark.action("--check-target-kind")
@pytest.mark.passes
def test_target_of_the_designs_kind_passes(check):
    p = Project("kind")
    got = p.run("--check-target-kind", p.design(log=DRAFTED))
    check("--check-target-kind passes a documentation design whose Target names the guide", passes(got, "== check-target-kind " + NAME, "0 problems"), shown(got))
    got = p.run("--check-target-kind", p.design("code-design", skill="implement-specs", log=DRAFTED), skill="implement-specs")
    check("--check-target-kind of implement-specs passes a code design whose Target names a file of no other kind",
          passes(got, "== check-target-kind code-design", "0 problems"), shown(got))


@pytest.mark.action("--check-target-kind")
@pytest.mark.reports
def test_target_of_another_kind_is_reported(check):
    p = Project("kind-strays")
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Target="`docs/guide.md`; `specs/methodology/code.md`"))
    check("--check-target-kind reports a canon file in a documentation design's Target",
          reports(got, "== check-target-kind " + NAME, "Target names a canon-specs file in a documentation design: specs/methodology/code.md"), shown(got))
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Target="`.ai/follow-ups.md`"))
    check("--check-target-kind reports a working file in a Target",
          reports(got, "== check-target-kind " + NAME, "Target names a working file, which no design changes: .ai/follow-ups.md"), shown(got))


@pytest.mark.action("--check-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_approved_design_with_its_research_passes(check):
    for skill in SKILLS:
        p = Project("validation")
        got = p.run("--check-design", researched(p, skill=skill, status="approved", log=APPROVED_RESEARCHED), skill=skill)
        check("--check-design of %s passes an approved design in its form, each Assessed Area resting on the research its log names" % skill,
              passes(got, "== check-design " + NAME, "0 problems"), shown(got))


@pytest.mark.action("--check-design")
@pytest.mark.reports
def test_design_not_yet_stated_is_reported(check):
    p = Project("validation-reports")
    got = p.run("--check-design", p.design(status="not-started"))
    check("--check-design reports the goals, the frame and the steps a design has yet to state",
          reports(got, "== check-design " + NAME, ["its design goals are not yet stated", "its design frame's Scope is not yet stated", "its steps are not yet drafted"]), shown(got))
    got = p.run("--check-design", p.design(status="approved", log=APPROVED_RESEARCHED))
    check("--check-design reports an Assessed Area resting on a report that does not stand in the design's folder",
          reports(got, "== check-design " + NAME, "has no Read Assessment of its Area in the reports the validation review reads"), shown(got))


@pytest.mark.action("--show-dependents")
@pytest.mark.passes
def test_dependents_of_a_part_are_listed(check):
    p = Project("dependents")
    design = p.design(log=DRAFTED)
    got = p.run("--show-dependents", design, GOAL)
    check("--show-dependents lists each part of the design naming a goal: its case, its principle, its Frame Outcome and its step Objective",
          passes(got, "== show-dependents %s %s (goal %s)" % (NAME, GOAL, GOAL), "4 parts name or cite " + GOAL)
          and all(w in got[1] for w in ("case visitor-planning-a-crossing", "principle times-stated-where-the-ferry-is-named", "frame outcome " + OUTCOME, OBJECTIVE)), shown(got))
    got = p.run("--show-dependents", design, OUTCOME)
    check("--show-dependents lists the one step Objective upholding a Frame Outcome", passes(got, "== show-dependents", "1 part names or cites " + OUTCOME), shown(got))


@pytest.mark.action("--show-dependents")
@pytest.mark.reports
def test_dependents_of_no_part_are_refused(check):
    p = Project("dependents-none")
    got = p.run("--show-dependents", p.design(log=DRAFTED), "no-such-part")
    check("--show-dependents refuses a Name no part of the design takes, exit 2",
          got[0] == 2 and "holds no goal, case, principle, Frame Outcome, step or step Objective named no-such-part" in got[1], shown(got))


@pytest.mark.action("--show-validation")
@pytest.mark.passes
def test_validated_design_is_shown_validated(check):
    p = Project("shown-validated")
    got = p.run("--show-validation", p.design(status="approved", log=APPROVED))
    check("--show-validation shows a design whose stamp matches its content as validated", passes(got, "== show-validation", NAME + ": validated; stamped sha256:"), shown(got))


@pytest.mark.action("--show-validation")
@pytest.mark.reports
def test_stale_or_unstamped_design_is_shown_so(check):
    p = Project("shown-stale")
    got = p.run("--show-validation", p.design(log=DRAFTED))
    check("--show-validation shows a design holding no stamp as never stamped", passes(got, "== show-validation", NAME + ": never stamped; stamped none"), shown(got))
    text = swap(a_design(status="approved", log=APPROVED), "without saying when it runs.", "without saying when it runs, or from where.")
    got = p.run("--show-validation", p.design(text=text))
    check("--show-validation shows a design edited since its stamp as stale", passes(got, "== show-validation", NAME + ": stale; stamped sha256:"), shown(got))


@pytest.mark.action("--stamp-validation")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_design_passing_validation_is_stamped(check):
    for skill in SKILLS:
        p = Project("stamp")
        text = swap(a_design(skill=skill, status="applying", log=APPLYING_RESEARCHED), "without saying when it runs.", "without saying when it runs, or from where.")
        design = researched(p, skill=skill, text=text)
        was = p.run("--show-validation", design, skill=skill)
        got = p.run("--stamp-validation", design, skill=skill)
        now = p.run("--show-validation", design, skill=skill)
        check("--stamp-validation of %s writes the stamp of a design the validation review passes, which then reads validated" % skill,
              ": stale;" in was[1] and passes(got, "== stamp-validation\n**Validated:** ") and ": validated;" in now[1], shown(got) + shown(now))
        again = p.run("--stamp-validation", design, skill=skill)
        check("--stamp-validation of %s leaves a current stamp as it stands" % skill, passes(again, "== stamp-validation", "already validated, the stamp current"), shown(again))


@pytest.mark.action("--stamp-validation")
@pytest.mark.reports
def test_design_failing_validation_is_not_stamped(check):
    p = Project("stamp-refused")
    design = p.design(log=AGREED, text=part(a_design(log=AGREED), "## Design Plan Steps", NOT_DRAFTED))
    before = p.held()
    got = p.run("--stamp-validation", design)
    check("--stamp-validation refuses a design whose steps are not yet drafted, and writes nothing",
          reports(got, "== stamp-validation, not stamped", "its steps are not yet drafted") and p.held() == before, shown(got))
    kept = p.design(folder=".ai/plans/design-specs/archive", status="applying", log=APPLYING)
    before = p.held()
    got = p.run("--stamp-validation", kept)
    check("--stamp-validation refuses a design standing in no plans folder, and writes nothing",
          reports(got, "== stamp-validation, not stamped", "it stands in no plans folder") and p.held() == before, shown(got))
