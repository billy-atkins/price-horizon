"""The audit's check of a file's blocks of fields: each line a field's key directly follows ends with one space and a
backslash, and no other line of a block does, a block nested beneath a field's text and a fenced Markdown block's
fields among them, and a field's list stands two spaces beyond its key."""
import pytest

from audit_set import spec_checks

FOLLOWED = ("a line of a block of fields that a line opening a field's key directly follows, ending with no backslash "
            "or with other than one space before it")
LAST = "a backslash ending a line of a block of fields that no line opening a field's key follows"
LIST = "a field's list whose items stand other than two spaces beyond its key: Fillings"

pytestmark = [pytest.mark.reads("audit-block-fields.md", "block-fields-in-form", "block-field-line-without-backslash",
                                "block-field-line-with-two-spaces-before-backslash", "block-field-last-line-with-backslash",
                                "block-field-list-indented-four-spaces", "block-field-nested-line-without-backslash",
                                "block-field-in-markdown-block-without-backslash")]


# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_blocks_of_fields_in_form_pass(fixtures):
    assert spec_checks.block_field_findings("specs/bakery.md", fixtures["block-fields-in-form"]) == []


# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("block-field-line-without-backslash", [(3, FOLLOWED)]),
    ("block-field-line-with-two-spaces-before-backslash", [(3, FOLLOWED)]),
    ("block-field-last-line-with-backslash", [(4, LAST)]),
    ("block-field-list-indented-four-spaces", [(5, LIST), (6, LIST)]),
    ("block-field-nested-line-without-backslash", [(5, FOLLOWED)]),
    ("block-field-in-markdown-block-without-backslash", [(6, FOLLOWED)]),
])
def test_a_block_of_fields_out_of_its_form_is_reported(fixtures, key, found):
    assert [(line, message) for _, line, message in spec_checks.block_field_findings("specs/bakery.md", fixtures[key])] == found
