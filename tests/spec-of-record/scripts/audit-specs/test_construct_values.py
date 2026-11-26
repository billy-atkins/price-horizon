"""The construct checks of a record type's Values cell: a cell holding a list of records of a cited type, `a list of`
and the citation of the type's definition, takes one of a Values cell's forms, and the words alone take none."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Construct"
BEDS = "specs/garden/beds.md"

pytestmark = [pytest.mark.reads("audit-constructs-record-values.md", "beds-holding-plantings", "beds-holding-plantings-in-words")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({BEDS: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_list_of_a_cited_record_type_passes(fixtures):
    assert findings(fixtures, "beds-holding-plantings") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_list_of_records_named_in_words_is_reported(fixtures):
    assert findings(fixtures, "beds-holding-plantings-in-words") == [
        (RULE, 26, "a Values cell in none of its forms: a list of plantings")]
