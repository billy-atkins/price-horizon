"""The audit's checks of tables: a Basic Table's headers each a field label, its Reference Key naming columns it holds
with no key value left blank or given twice, and no cell left blank under its Required; and a table mapping a
registered standard held to the one form a mapping takes, each row's Treatment and its departure in their form."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-tables.md", "visiting-boats-table", "visiting-boats-table-with-a-lowercase-header",
                                "visiting-boats-table-keyed-by-name", "visiting-boats-table-naming-curlew-twice",
                                "visiting-boats-table-missing-a-length", "register-of-harborml", "harborml-mapping",
                                "harborml-mapping-opened-by-no-field", "harborml-mapping-without-a-why-column",
                                "harborml-mapping-of-a-loose-treatment", "harborml-mapping-of-a-departure-without-a-why")]
BOATS = "docs/boats.md"
TIDE_RECORDS = "docs/tide-records.md"
REGISTER = "specs/methodology/external-references.md"


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Basic Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Keyed Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_basic_table_in_its_form_passes(fixtures):
    held = scope(fixtures, {"visiting-boats-table": BOATS})
    assert spec_checks.table_findings(BOATS, held.text_of[BOATS], held) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Basic Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Keyed Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("visiting-boats-table-with-a-lowercase-header", 8, "a header that is no field label: home port"),
    ("visiting-boats-table-keyed-by-name", 5, "a Reference Key naming no column its table holds: Name"),
    ("visiting-boats-table-naming-curlew-twice", 11, "two rows sharing their key: ('Curlew',)"),
    ("visiting-boats-table-missing-a-length", 11, "a blank cell in a column its Required names: Length"),
])
def test_a_basic_table_out_of_its_form_is_reported(fixtures, key, line, message):
    held = scope(fixtures, {key: BOATS})
    assert [(n, m) for _, n, m in spec_checks.table_findings(BOATS, held.text_of[BOATS], held)] == [(line, message)]


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_mapping_onto_a_standard_in_its_form_passes(fixtures):
    held = scope(fixtures, {"register-of-harborml": REGISTER, "harborml-mapping": TIDE_RECORDS})
    assert spec_checks.mapping_table_findings(TIDE_RECORDS, held.text_of[TIDE_RECORDS], held) == []


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("harborml-mapping-opened-by-no-field", "a mapping onto a standard opened by none of its fields: HarborML"),
    ("harborml-mapping-without-a-why-column",
     "a mapping onto a standard not in its form: its Table Name the standard's Name and `Elements`, its Reference Key "
     "that Name, its Required `Section, Treatment`, and its columns that Name, Section, Treatment, Departs For and Why"),
    ("harborml-mapping-of-a-loose-treatment", "a Treatment opening neither `the same`, `differs:` nor `not written`"),
    ("harborml-mapping-of-a-departure-without-a-why", "a departure with no Why"),
])
def test_a_mapping_onto_a_standard_out_of_its_form_is_reported(fixtures, key, message):
    held = scope(fixtures, {"register-of-harborml": REGISTER, key: TIDE_RECORDS})
    assert messages(spec_checks.mapping_table_findings(TIDE_RECORDS, held.text_of[TIDE_RECORDS], held)) == [message]
