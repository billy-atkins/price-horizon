"""The construct checks of a Constraint: each rule is a FEEL yes or no, holds always or after or before a cited
operation, and is enforced by citations."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Constraint"
PLOTS = "specs/garden/plots.md"

pytestmark = [pytest.mark.reads("audit-constructs-constraints.md", "allotment-rules", "allotment-rules-held-sometimes",
                                "allotment-rules-kept-by-the-committee", "allotment-rules-counting-plots")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({PLOTS: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_rules_holding_always_and_after_an_algorithm_each_enforced_pass(fixtures):
    assert findings(fixtures, "allotment-rules") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("allotment-rules-held-sometimes",
     [(RULE, 9, "an Applies To that is neither `always` nor `after` or `before` a citation: sometimes")]),
    ("allotment-rules-kept-by-the-committee", [(RULE, 9, "a rule stated but enforced nowhere: its Enforced By cites nothing")]),
    ("allotment-rules-counting-plots", [(RULE, 9, "a rule giving no yes or no, a number: count(plots)")]),
])
def test_a_rule_out_of_its_form_is_reported(fixtures, key, found):
    assert findings(fixtures, key) == found
