"""The entry scripts' wiring, each run as a process of its own at a project's root: each takes an action's flag,
reaches the unit carrying it out, prints what it gives and exits as it says, over its own skill's plans folder, and
refuses a run it cannot make."""
import pytest

from design_script_set import DESIGN, NAME, entry_run, project

pytestmark = [pytest.mark.reads("design-script-designs.md", "ferry-design-holding-a-field-out-of-its-form", "code-design-drafted")]


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
def test_entry_script_takes_a_flag_reaches_its_action_and_exits_as_it_says(fixtures, work):
    root = project(work, fixtures, {"ferry-design-holding-a-field-out-of-its-form": DESIGN})
    code, out = entry_run(root, "--check-design-form", DESIGN)
    assert code == 1 and "== check-design-form " + NAME in out and "Reviewed By" in out


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
def test_implementation_skills_entry_script_reads_its_own_plans_folder(fixtures, work):
    root = project(work, fixtures, {"code-design-drafted": ".ai/plans/implement-specs/code-design.md"})
    code, out = entry_run(root, "--show-workstack", skill="implement-specs")
    assert code == 0 and "  code-design [in-progress]" in out and "implement-specs/code-design" not in out


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.parametrize("given, said", [([], "usage: design-specs.py"), (["--check-no-such-thing"], "unrecognized arguments")])
def test_entry_script_refuses_a_run_it_cannot_make(work, given, said):
    work.mkdir(parents=True, exist_ok=True)
    code, out = entry_run(work, *given)
    assert code == 2 and said in out
