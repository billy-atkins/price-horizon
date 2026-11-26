"""The construct checks of a submachine state: a state governed by another State Machine names it after the words
governed by, and is left as that machine's terminal states have it."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § State Machine § A Submachine State"
ORDERS = "specs/bakery/orders.md"

pytestmark = [pytest.mark.reads("audit-constructs-submachines.md", "bread-order-baked-in-one-batch",
                                "bread-order-baked-in-a-batch-of-two-ends", "bread-order-governed-by-its-facts")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({ORDERS: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_governed_state_left_by_its_machines_one_end_passes(fixtures):
    assert findings(fixtures, "bread-order-baked-in-one-batch") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("bread-order-baked-in-a-batch-of-two-ends", [
        (RULE, 20, "a transition from a governed state guarded by no terminal state of its machine: none"),
        (RULE, 11, "a governed state left by no transition for its machine's terminal state: baked"),
        (RULE, 11, "a governed state left by no transition for its machine's terminal state: burnt")]),
    ("bread-order-governed-by-its-facts", [(RULE, 11, "the words governed by naming no State Machine: baking")]),
])
def test_a_governed_state_out_of_step_with_its_machine_is_reported(fixtures, key, found):
    assert findings(fixtures, key) == found
