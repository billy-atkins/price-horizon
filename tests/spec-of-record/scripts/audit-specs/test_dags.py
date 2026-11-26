"""The construct checks of a DAG: each dependency names a task its table holds, no task depends on itself, and no two
tasks free at once give one fact."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § DAG"
BAKE = "specs/bakery/bake.md"

pytestmark = [pytest.mark.reads("audit-constructs-dags.md", "morning-bake", "morning-bake-waiting-on-a-missing-task",
                                "morning-bake-in-a-circle", "morning-bake-two-mixers")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({BAKE: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_dag_whose_tasks_wait_for_what_they_read_passes(fixtures):
    assert findings(fixtures, "morning-bake") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("morning-bake-waiting-on-a-missing-task", [(RULE, 11, "a dependency naming a task the table does not hold: proof dough")]),
    ("morning-bake-in-a-circle", [(RULE, 8, "a task that depends on itself, directly or through others: mix dough"),
                                  (RULE, 8, "a task that depends on itself, directly or through others: bake loaves")]),
])
def test_a_dependency_out_of_a_dags_order_is_reported(fixtures, key, found):
    assert findings(fixtures, key) == found


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_two_tasks_free_at_once_giving_one_fact_are_reported(fixtures):
    assert findings(fixtures, "morning-bake-two-mixers") == [
        (RULE, 8, "two tasks free at once whose work gives one fact: mix by hand and mix by machine, dough")]
