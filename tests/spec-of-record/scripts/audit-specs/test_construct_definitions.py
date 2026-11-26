"""The construct checks' copies of the definitions, held to the file holding the definitions where the texts checked
hold it: a definition's Modifier, Extends and Implements, each table of fields or of members, and each Column | Holds
table, each read against the copy the checks keep, and each Values cell in one of its forms."""
import pytest

from audit_set import constructs

HOME = "specs/methodology/modeling-constructs.md"
DEFINING = "modeling-constructs.md § Defining Constructs"
CONSTRUCT = "modeling-constructs.md § Constructs § Construct"
DECLARED = "modeling-constructs.md § Constructs § Declared Construct"
ORDERED = "modeling-constructs.md § Constructs § Ordered Construct"
CONFIGURED = "modeling-constructs.md § Constructs § Configured Construct"
DECISION = "modeling-constructs.md § Constructs § Decision Table"
TABULAR = "modeling-constructs.md § Constructs § Tabular Construct"
MEMBERS = "modeling-constructs.md § Defining Constructs § Interfaces and Members"

pytestmark = [pytest.mark.reads("audit-constructs-definitions.md", "garden-forms-defining-and-construct",
                                "garden-forms-implements-required", "garden-forms-construct-without-a-modifier",
                                "garden-forms-construct-columns-without-holds", "garden-forms-implements-values-in-words",
                                "garden-forms-declared-construct", "garden-forms-declared-construct-extends-required",
                                "garden-forms-declared-construct-extends-by-definition",
                                "garden-forms-ordered-construct", "garden-forms-ordered-construct-order-optional",
                                "garden-forms-configured-construct", "garden-forms-configured-construct-held-in-required",
                                "garden-forms-decision-table-fields", "garden-forms-decision-table-hit-policy-first",
                                "garden-forms-tabular-columns", "garden-forms-tabular-columns-decision-table-unnamed")]


def held_to_home(fixtures, key, rule):
    """-> (line, message) of each finding of `rule` the construct checks give with the fixture `key` standing as the
    file holding the definitions."""
    found, _, _ = constructs.run_checks({HOME: fixtures[key]})
    return [(line, message) for r, _, line, message in found if r == rule]


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_definitions_fields_and_its_modifier_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-defining-and-construct", DEFINING) == []


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("garden-forms-implements-required", 11,
     "the fields table's row ('Implements', 'yes', '', 'text') differs from the script's copy ('Implements', 'no', 'none', 'text')"),
    ("garden-forms-construct-without-a-modifier", 15,
     "the definition of § Constructs § Construct reads (None, (), ()), the script's copy ('Abstract', (), ())"),
])
def test_a_definitions_fields_or_its_modifier_out_of_step_with_the_copy_is_reported(fixtures, key, line, message):
    assert held_to_home(fixtures, key, DEFINING) == [(line, message)]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_table_of_fields_columns_and_values_cells_in_their_forms_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-defining-and-construct", CONSTRUCT) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("garden-forms-construct-columns-without-holds", 11,
     "a Construct Column | Holds table giving ['Field', 'Required', 'Default Value', 'Values'], "
     "where the script's copy gives ['Field', 'Required', 'Default Value', 'Values', 'Holds']"),
    ("garden-forms-implements-values-in-words", 11, "a Values cell in none of its forms: the names of some beds"),
])
def test_a_table_of_fields_columns_or_a_values_cell_out_of_its_form_is_reported(fixtures, key, line, message):
    assert held_to_home(fixtures, key, CONSTRUCT) == [(line, message)]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declared Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_declared_constructs_members_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-declared-construct", DECLARED) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declared Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_declared_constructs_members_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-declared-construct-extends-required", DECLARED) == [
        (14, "the fields table's row ('Extends', 'yes', '', 'text') differs from the script's copy ('Extends', 'no', 'none', 'text')")]


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Interfaces and Members
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_an_interfaces_members_specified_as_the_copy_gives_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-declared-construct", MEMBERS) == []


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Interfaces and Members
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_an_interfaces_member_specified_otherwise_than_the_copy_is_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-declared-construct-extends-by-definition", MEMBERS) == [
        (11, "the members of § Constructs § Declared Construct Specified By ('Instance', 'Definition'), "
             "the script's copy ('Instance', 'Instance')")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Ordered Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_ordered_constructs_members_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-ordered-construct", ORDERED) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Ordered Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_ordered_constructs_members_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-ordered-construct-order-optional", ORDERED) == [
        (13, "the fields table's row ('Order', 'no', 'any', 'text') differs from the script's copy "
             "('Order', 'where the construct leaves open the order it takes its inputs or gives its results in', '', 'text')")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Configured Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_configured_constructs_members_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-configured-construct", CONFIGURED) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Configured Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_configured_constructs_members_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-configured-construct-held-in-required", CONFIGURED) == [
        (13, "the fields table's row ('Held In', 'yes', '', 'text') differs from the script's copy ('Held In', 'no', 'none', 'text')")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_decision_tables_fields_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-decision-table-fields", DECISION) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_decision_tables_fields_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-decision-table-hit-policy-first", DECISION) == [
        (11, "the fields table's row ('Hit Policy', 'no', 'First', '`§ Constructs § Decision Table`') differs from the script's copy "
             "('Hit Policy', 'no', 'Unique', '`§ Constructs § Decision Table`')")]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Tabular Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_each_tabular_constructs_columns_in_step_with_the_copy_pass(fixtures):
    assert held_to_home(fixtures, "garden-forms-tabular-columns", TABULAR) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Tabular Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_tabular_constructs_columns_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "garden-forms-tabular-columns-decision-table-unnamed", TABULAR) == [
        (80, "a Decision Table Column | Holds table giving [], where the script's copy gives ['Name']")]
