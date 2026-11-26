"""The construct checks of an Algorithm: each Output fact is set, each jump reaches a step the table holds, the last
step ends or jumps, and a Rounding Mode is one of FEEL's modes."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Algorithm"
WATERING = "specs/garden/watering.md"

pytestmark = [pytest.mark.reads("audit-constructs-algorithms.md", "watering-ration", "watering-ration-never-set",
                                "watering-ration-jumping-past-its-end", "watering-ration-without-an-end",
                                "watering-ration-rounded-to-nearest")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({WATERING: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_an_algorithm_setting_its_output_on_every_path_passes(fixtures):
    assert findings(fixtures, "watering-ration") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("watering-ration-never-set", [(RULE, 5, "an Output fact nothing sets: water")]),
    ("watering-ration-jumping-past-its-end", [(RULE, 17, "a jump to a step the table does not hold: 7")]),
    ("watering-ration-without-an-end", [(RULE, 14, "a last step, or a branch of it, that neither ends nor jumps")]),
])
def test_an_algorithm_whose_steps_leave_its_run_unfinished_is_reported(fixtures, key, found):
    assert findings(fixtures, key) == found


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_rounding_mode_of_feels_passes(fixtures):
    assert findings(fixtures, "watering-ration") == []


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_rounding_mode_of_none_of_feels_modes_is_reported(fixtures):
    assert findings(fixtures, "watering-ration-rounded-to-nearest") == [
        (RULE, 5, "a Rounding Mode that is neither a mode nor a fact the Algorithm knows: nearest")]
