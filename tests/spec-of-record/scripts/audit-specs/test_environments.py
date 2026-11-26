"""The audit's check of the environments document: each environment opening with its Kind, exactly one of them
local, and its tables of tools and of tasks headed as their form gives them."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-layered-indexes.md", "index-of-a-layered-harbor-guide", "index-of-the-harbor-application",
                                "index-of-the-harbor-technical"),
              pytest.mark.reads("audit-environments.md", "harbor-office-environments", "harbor-office-environments-none-local",
                                "harbor-office-environment-without-a-kind", "harbor-office-tools-out-of-order",
                                "harbor-office-tasks-out-of-order")]
ENVIRONMENTS = "specs/application/technical/environments.md"


def harbor(fixtures, key):
    """-> the scope of the harbor's project, the fixture `key` standing as its environments document."""
    return scope(fixtures, {"index-of-a-layered-harbor-guide": "specs/index.md",
                            "index-of-the-harbor-application": "specs/application/index.md",
                            "index-of-the-harbor-technical": "specs/application/technical/index.md", key: ENVIRONMENTS})


# @canon-spec specs/methodology/spec-placement/environments.md § Environments
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_environments_each_of_a_kind_one_local_pass(fixtures):
    held = harbor(fixtures, "harbor-office-environments")
    assert spec_checks.environments_findings(ENVIRONMENTS, held.text_of[ENVIRONMENTS], held) == []


# @canon-spec specs/methodology/spec-placement/environments.md § Environments
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("harbor-office-environments-none-local", 0, "0 environments are local, not exactly one"),
    ("harbor-office-environment-without-a-kind", 9,
     "an environment does not open with a Kind field, on a line of its own, of local, integration, shared or production"),
    ("harbor-office-tools-out-of-order", 9,
     "a tools table not headed Tool, Version and Purpose with at least one install column after them"),
    ("harbor-office-tasks-out-of-order", 9,
     "a tasks table not headed Task, Command and Does, with Runs On after them where a task needs it"),
])
def test_an_environment_out_of_its_form_is_reported(fixtures, key, line, message):
    held = harbor(fixtures, key)
    assert [(n, m) for _, n, m in spec_checks.environments_findings(ENVIRONMENTS, held.text_of[ENVIRONMENTS], held)] == [
        (line, message)]
