"""The audit's set of kept tests: which files are the audit's, and what the set's tests share.

A test calls one of the audit's check units with the input the unit's kind takes, written from the test's fixtures:
a file's path and its text, those with a scope, or a scope alone. A scope is read from a project of fixtures held in
memory, each fixture placed at the path the test gives it, so no test writes a project to audit and none audits the
project's own files. The audit reads its forms from the canon of the files its code stands in, as it does when it
is run by hand. A test file takes these names by `from audit_set import ...`, the name this file is registered under
as the runner reads it.
"""
import sys
from pathlib import Path

# The files of the script these tests are of, the audit: its code, and each file of the canon it reads a form from
# as it runs. A path ending in a slash names each file beneath it.
SCRIPT_FILES = (".ai/skills/audit-specs/scripts/", ".ai/skills/lib/")
FORM_FILES = (".ai/skills/audit-specs/SKILL.md", ".ai/skills/search-spec-of-record-scope/SKILL.md", "specs/AGENTS.md",
              "specs/methodology/acceptance-scenarios.md", "specs/methodology/checks.md",
              "specs/methodology/design-workflow/designs-reviews.md", "specs/methodology/design-workflow/order-of-a-designs-work.md",
              "specs/methodology/design-workflow/reviews-effort.md", "specs/methodology/expressions.md",
              "specs/methodology/modeling-constructs.md", "specs/methodology/scope/rules-and-skills.md",
              "specs/methodology/skills/authoring-a-skill.md", "specs/methodology/sourcing-and-citation/external-reference.md",
              "specs/methodology/sourcing-and-citation/which-citations-are-allowed.md",
              "specs/methodology/sourcing-and-citation/writing-a-citation.md", "specs/methodology/spec-placement/environments.md",
              "specs/methodology/spec-placement/index-architecture-detail.md",
              "specs/methodology/spec-placement/naming-a-capability-domain.md", "specs/methodology/spec-placement/open-question.md",
              "specs/methodology/spec-placement/product-or-technical.md", "specs/methodology/spec-placement/where-a-file-goes.md",
              "specs/methodology/spec-style/clear-prose.md", "specs/methodology/spec-style/markdown.md",
              "specs/methodology/working-files/main.md")
ACTIONS_IN = ".ai/skills/audit-specs/scripts/audit-specs.py"

PROJECT_FILES = Path(__file__).resolve().parents[4]
LIB = PROJECT_FILES / ".ai" / "skills" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
import citation_links  # noqa: E402
import code_checks  # noqa: E402
import constructs  # noqa: E402
import layout  # noqa: E402
import record_types  # noqa: E402
import spec_checks  # noqa: E402
import spec_text  # noqa: E402

ENTRY = PROJECT_FILES / ".ai" / "skills" / "audit-specs" / "scripts" / "audit-specs.py"


def entry_script():
    """-> the audit's entry script as a module, loaded from its file once, so a test calls the unit carrying out an
    action."""
    if "audit_entry_script" not in sys.modules:
        import importlib.util
        spec = importlib.util.spec_from_file_location("audit_entry_script", ENTRY)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return sys.modules["audit_entry_script"]


def project(work, fixtures, placed):
    """-> the folder of a project of fixtures written within the test's own folder, each fixture at its path, for a
    test running an action over a project on disk."""
    root = work / "project"
    for key, path in placed.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(fixtures[key], encoding="utf-8", newline="\n")
    return root


def scope(fixtures, placed, tracked=None):
    """-> the audit's scope of a project of fixtures held in memory: each fixture placed at its path, `placed` mapping
    a fixture's key to the path it stands at; `tracked`, the paths version control tracks, all of them where none is
    given."""
    return spec_checks.Scope({path: fixtures[key] for key, path in placed.items()}, tracked)


def messages(found, rule=None):
    """-> the messages of a unit's findings, of one rule where one is given, in the order the unit gives them."""
    return [f[-1] for f in found if rule is None or f[0] == rule]


sys.modules["audit_set"] = sys.modules[__name__]
