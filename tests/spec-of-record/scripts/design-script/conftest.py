"""The design script's set of kept tests: which files are the design script's, and what the set's tests share.

A test calls a unit of the design script with a small input written from its fixtures, or calls an action as the
entry scripts call it, in a project of fixtures written within the test's own folder, each fixture at the path the
test gives it. A few tests run an entry script as a process, each holding one part of its wiring. No project holds a
file of the canon or a copy of the skills' code: the script reads each form from the canon of the files its code
stands in, and what it checks from the project. A test file takes these names by `from design_script_set import ...`,
the name this file is registered under as the runner reads it.
"""
import subprocess
import sys
from pathlib import Path

import pytest

# The files of the script these tests are of, the design script: its code, and each file of the canon it reads a form
# from as it runs, the checks of the specs and of the code it runs over a design's work among them. A path ending in a
# slash names each file beneath it.
SCRIPT_FILES = (".ai/skills/lib/", ".ai/skills/design-specs/scripts/", ".ai/skills/implement-specs/scripts/")
FORM_FILES = (".ai/skills/audit-specs/SKILL.md", ".ai/skills/search-spec-of-record-scope/SKILL.md", "specs/AGENTS.md",
              "specs/methodology/acceptance-scenarios.md", "specs/methodology/checks.md",
              "specs/methodology/design-workflow/designs-reviews.md", "specs/methodology/design-workflow/order-of-a-designs-work.md",
              "specs/methodology/design-workflow/reviews-effort.md", "specs/methodology/expressions.md",
              "specs/methodology/modeling-constructs.md",
              "specs/methodology/scope/rules-and-skills.md", "specs/methodology/skills/authoring-a-skill.md",
              "specs/methodology/sourcing-and-citation/external-reference.md",
              "specs/methodology/sourcing-and-citation/which-citations-are-allowed.md",
              "specs/methodology/sourcing-and-citation/writing-a-citation.md", "specs/methodology/spec-placement/environments.md",
              "specs/methodology/spec-placement/index-architecture-detail.md",
              "specs/methodology/spec-placement/naming-a-capability-domain.md", "specs/methodology/spec-placement/open-question.md",
              "specs/methodology/spec-placement/product-or-technical.md", "specs/methodology/spec-placement/where-a-file-goes.md",
              "specs/methodology/spec-style/clear-prose.md", "specs/methodology/spec-style/markdown.md",
              "specs/methodology/working-files/main.md")
ACTIONS_IN = ".ai/skills/lib/design_documents.py"

PROJECT_FILES = Path(__file__).resolve().parents[4]
LIB = PROJECT_FILES / ".ai" / "skills" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
import design_documents  # noqa: E402
import spec_text  # noqa: E402

ENTRY = {skill: PROJECT_FILES / ".ai" / "skills" / skill / "scripts" / (skill + ".py") for skill in ("design-specs", "implement-specs")}
# where a design of the fixtures stands in a project, and its reports, by the name its fixtures give it
NAME = "ferry-times-in-the-guide"
DESIGN = ".ai/plans/design-specs/%s.md" % NAME
REPORTS = ".ai/tmp/design-specs/%s/reports" % NAME


def project(work, fixtures, placed):
    """-> the folder of a project of fixtures written within the test's own folder, each fixture at its path, `placed`
    mapping a fixture's key to the path it stands at."""
    root = work / "project"
    for key, path in placed.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(fixtures[key], encoding="utf-8", newline="\n")
    root.mkdir(parents=True, exist_ok=True)
    return root


def acted(monkeypatch, root, action, value, plans=None):
    """-> the exit status of one of the design script's actions, called as an entry script calls it, in the project's
    root, the plans folder of the skill running it the one given, or the design skill's."""
    monkeypatch.chdir(root)
    monkeypatch.setattr(design_documents, "PLANS", plans or ".ai/plans/design-specs")
    return action(value)


def held(root, under="."):
    """-> {path: bytes} of each file under a folder of a project, to compare before and after an action."""
    base = Path(root) / under
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(base.rglob("*")) if p.is_file()}


def entry_run(root, *args, skill="design-specs"):
    """-> (the exit status, what it printed) of an entry script run as a process of its own at a project's root."""
    done = subprocess.run([sys.executable, "-B", str(ENTRY[skill])] + [str(a) for a in args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8")
    return done.returncode, done.stdout + done.stderr


def git(root, *args):
    """-> what git prints, run in a project with a user of its own and no signing, the test failing where it fails."""
    done = subprocess.run(["git", "-c", "user.name=design-script-tests", "-c", "user.email=design-script-tests@example.invalid",
                           "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main"] + list(args),
                          cwd=root, capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, "git %s: %s" % (" ".join(args), done.stderr)
    return done.stdout.strip()


def committed(root):
    """Put a project under version control, every file it holds committed -> its root."""
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "a commit made for a test")
    return root


sys.modules["design_script_set"] = sys.modules[__name__]

# the kept tests' group: a project's own runner and its set of kept tests, written as fixtures, which the design script
# runs in that project in place of the project's own
KEPT = "tests/spec-of-record"
KEPT_RUN = ".ai/tmp/kept-tests"
GUIDE_SET = KEPT + "/scripts/guide"
GUIDE_TESTS = GUIDE_SET + "/test_guide.py"
KEPT_FIXTURES = KEPT + "/fixtures"
# the fixtures kept_set takes beside the guide's file of tests, which a test names among its own
KEPT_SET_READS = (pytest.mark.reads("design-script-kept-runs.md", "kept-runner-settings", "kept-runner-conftest"),
                  pytest.mark.reads("design-script-kept-sets.md", "guide-script", "guide-set-conftest", "fixture-file-of-one-line",
                                    "index-listing-one-file"))


def kept_set(work, fixtures, placed=None, tests="guide-set-tests", left_out=()):
    """-> the root of a project of fixtures holding a runner of its own and the guide's set of kept tests: the
    runner's settings and what it hands each test, the guide's script at tools/guide.py, the file its set says which
    files are its script's in, its file of
    tests, the fixture `tests` names, the fixture file one test reads and the fixtures' index, each but the keys
    left_out; and each fixture placed maps to its path, written after them."""
    held = {"kept-runner-settings": KEPT + "/pytest.ini", "kept-runner-conftest": KEPT + "/conftest.py", "guide-script": "tools/guide.py",
            "guide-set-conftest": GUIDE_SET + "/conftest.py", tests: GUIDE_TESTS, "fixture-file-of-one-line": KEPT_FIXTURES + "/guide.md",
            "index-listing-one-file": KEPT_FIXTURES + "/index.md"}
    for key in left_out:
        held.pop(key)
    held.update(placed or {})
    return project(work, fixtures, held)


# the workstack's and the log's group: the designs a name in a Depends On Designs can be of, one unfinished, one
# complete and one abandoned in the design skill's plans folder, and one complete in its archive, where no design of
# the workstack stands; a test file takes WORKSTACK_READS among its markers

WORKSTACK = {"quay-rebuilt-in-progress": ".ai/plans/design-specs/quay-rebuilt.md",
             "harbor-dredged-complete": ".ai/plans/design-specs/harbor-dredged.md",
             "pier-closed-abandoned": ".ai/plans/design-specs/pier-closed.md",
             "tide-tables-printed-complete": ".ai/plans/design-specs/archive/tide-tables-printed.md"}
WORKSTACK_READS = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
                   pytest.mark.reads("design-script-workstack.md", "quay-rebuilt-in-progress", "pier-closed-abandoned", "tide-tables-printed-complete"),
                   pytest.mark.reads("design-script-once-mishandled.md", "harbor-dredged-complete")]


def workstack(work, fixtures, placed=None):
    """-> the root of a project holding the guide and the designs of WORKSTACK, with each fixture placed at its path."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", **WORKSTACK, **(placed or {})})
