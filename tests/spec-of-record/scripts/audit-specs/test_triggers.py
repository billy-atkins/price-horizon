"""The construct checks of a State Machine's triggers written in FEEL: `after` takes a duration, `at` a date or a date
and time, and `when` a yes or no, and no trigger reads the wall clock by today() or now()."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § State Machine"
ORDERS = "specs/bakery/orders.md"

pytestmark = [pytest.mark.reads("audit-constructs-triggers.md", "bread-order-on-the-shelf", "bread-order-after-a-date",
                                "bread-order-when-a-count", "bread-order-at-tomorrow")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({ORDERS: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_triggers_giving_their_openings_kinds_pass(fixtures):
    assert findings(fixtures, "bread-order-on-the-shelf") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("bread-order-after-a-date", [(RULE, 19, "a trigger `after` whose expression gives date, not days and time duration "
                                             "or years and months duration: after pickup day")]),
    ("bread-order-when-a-count", [(RULE, 19, "a trigger `when` whose expression gives number, not boolean: when loaves left")]),
])
def test_a_trigger_giving_another_kind_than_its_opening_takes_is_reported(fixtures, key, found):
    assert findings(fixtures, key) == found


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# @canon-spec specs/methodology/modeling-constructs.md § Time
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_triggers_reading_time_from_facts_pass(fixtures):
    assert findings(fixtures, "bread-order-on-the-shelf") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# @canon-spec specs/methodology/modeling-constructs.md § Time
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_trigger_reading_the_wall_clock_by_today_is_reported(fixtures):
    assert findings(fixtures, "bread-order-at-tomorrow") == [
        (RULE, 19, "a trigger reading the wall clock by today() or now(), which `after` and `at` read: at today() + @\"P1D\"")]
