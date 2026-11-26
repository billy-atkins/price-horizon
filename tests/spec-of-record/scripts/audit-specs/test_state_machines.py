"""The construct checks of a State Machine read across its file: an Effect cell cites an Algorithm or a Decision Table,
a guard tests a fact for one of its Values, each state is among the Values of the fact the machine is recorded in, and
two guards from one state on one trigger never both hold."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § State Machine"
ORDERS = "specs/bakery/orders.md"

pytestmark = [pytest.mark.reads("audit-constructs-state-machines.md", "bakery-order", "bakery-order-effect-on-a-fact",
                                "bakery-order-guard-on-a-word", "bakery-order-recorded-without-a-state",
                                "bakery-order-overlapping-guards")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({ORDERS: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_machine_with_its_effect_guards_and_recorded_states_in_form_passes(fixtures):
    assert findings(fixtures, "bakery-order") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_an_effect_citing_no_algorithm_or_decision_table_is_reported(fixtures):
    assert findings(fixtures, "bakery-order-effect-on-a-fact") == [
        (RULE, 18, "an Effect cell citing no Algorithm or Decision Table: `§ Facts`")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_guard_testing_a_fact_for_a_word_outside_its_values_is_reported(fixtures):
    assert findings(fixtures, "bakery-order-guard-on-a-word") == [
        (RULE, 20, "a guard testing crust for a value outside its Values: burnt")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_state_outside_the_values_of_the_fact_its_machine_is_recorded_in_is_reported(fixtures):
    assert findings(fixtures, "bakery-order-recorded-without-a-state") == [
        (RULE, 14, "a state not among the Values of the fact its machine is recorded in: cancelled")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_two_guards_from_one_state_on_one_trigger_that_can_both_hold_are_reported(fixtures):
    assert findings(fixtures, "bakery-order-overlapping-guards") == [
        (RULE, 19, "two guards from placed on the baker packs it that can both hold")]
