"""The design script's kept comparison: which designs the script of the last commit and the script as it stands read
differently, each side reading its own tree's form, held over a project of fixtures whose script at the design
script's place is a stand-in, under version control."""
import subprocess
import sys
from pathlib import Path

import pytest

from design_script_set import committed, git, project

pytestmark = [pytest.mark.reads("design-script-compared.md", "stand-in-design-script", "stand-in-design-script-marking-approval", "status-form",
                                "status-form-renamed"),
              pytest.mark.reads("design-script-designs.md", "ferry-design-drafted", "ferry-design-approved")]
COMPARISON = Path(__file__).parent / "comparison.py"
SCRIPT, FORM, PLANS = ".ai/skills/lib/design_documents.py", "specs/status-form.md", ".ai/plans/design-specs"
DRAFTED, APPROVED = PLANS + "/first-design.md", PLANS + "/second-design.md"


def compared(root, *args):
    done = subprocess.run([sys.executable, "-B", str(COMPARISON)] + list(args), cwd=root, capture_output=True, text=True, encoding="utf-8")
    return done.returncode, done.stdout + done.stderr


def stand_in(work, fixtures, versioned=True):
    root = project(work, fixtures, {"stand-in-design-script": SCRIPT, "status-form": FORM, "ferry-design-drafted": DRAFTED,
                                    "ferry-design-approved": APPROVED})
    return committed(root) if versioned else root


@pytest.mark.parametrize("changed, listed", [
    ({}, []),
    ({"stand-in-design-script-marking-approval": SCRIPT}, [APPROVED]),
    ({"status-form-renamed": FORM}, [DRAFTED, APPROVED]),
])
def test_comparison_lists_each_design_the_two_sides_read_differently(fixtures, work, changed, listed):
    root = stand_in(work, fixtures)
    project(work, fixtures, changed)
    code, out = compared(root, PLANS)
    assert code == 0, out
    assert sorted(line[len("design "):] for line in out.split("\n") if line.startswith("design ")) == sorted(listed)
    assert "%d design%s read differently, of 2" % (len(listed), "" if len(listed) == 1 else "s") in out


def test_comparison_leaves_no_worktree_behind(fixtures, work):
    root = stand_in(work, fixtures)
    project(work, fixtures, {"stand-in-design-script-marking-approval": SCRIPT})
    assert compared(root, PLANS)[0] == 0
    assert not (root / ".ai/tmp/worktrees/design-script-comparison-then").exists()
    assert not (root / ".ai/tmp/worktrees/design-script-comparison-now").exists()
    assert git(root, "worktree", "list").count("\n") == 0 and git(root, "status", "--porcelain") == "M " + SCRIPT


@pytest.mark.parametrize("versioned, given, said", [
    (True, "docs", "design-script-comparison takes plans folders"),
    (False, PLANS, "cannot be made"),
])
def test_comparison_that_cannot_be_made_says_so(fixtures, work, versioned, given, said):
    code, out = compared(stand_in(work, fixtures, versioned), given)
    assert code == 2 and said in out
