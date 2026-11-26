"""The audit's checks of records and fields: a record section titled with a declared type's name, standing where its
type places it and holding records of its type's fields; and each field keyed as a form declares, where that form
places it."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-records.md", "index-of-a-harbor-dues-guide", "dues-with-open-questions-last",
                                "dues-with-open-questions-first", "dues-with-an-open-question-of-no-impacts",
                                "dues-with-moorings-let", "dues-with-a-tide-height", "dues-with-a-caption")]
DUES = "specs/dues.md"


def harbor(fixtures, key):
    """-> the scope of a harbor's project: its guide, and the fixture `key` as its dues."""
    return scope(fixtures, {"index-of-a-harbor-dues-guide": "specs/index.md", key: DUES})


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference
# @canon-spec specs/methodology/spec-placement/open-question.md § Open Question
# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_record_section_of_its_type_in_its_place_passes(fixtures):
    held = harbor(fixtures, "dues-with-open-questions-last")
    assert spec_checks.record_form_findings(DUES, held.text_of[DUES], held) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference
# @canon-spec specs/methodology/spec-placement/open-question.md § Open Question
# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("dues-with-open-questions-first", 3, "the Open Questions section is not its file's last top-level section"),
    ("dues-with-an-open-question-of-no-impacts", 10, "a record without the field its type requires: Impacts"),
    ("dues-with-moorings-let", 3, "a record section titled with no declared type's Plural Name: Moorings Let"),
])
def test_a_record_section_out_of_its_type_is_reported(fixtures, key, line, message):
    held = harbor(fixtures, key)
    assert [(n, m) for _, n, m in spec_checks.record_form_findings(DUES, held.text_of[DUES], held)] == [(line, message)]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_fields_each_in_their_place_pass(fixtures):
    held = harbor(fixtures, "dues-with-open-questions-last")
    assert spec_checks.field_place_findings(DUES, held.text_of[DUES], held) == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/modeling-constructs.md § Fields § A Nested Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("dues-with-a-tide-height", "a field whose key no form declares: Tide Height"),
    ("dues-with-a-caption", "the Caption field outside the place its form gives it"),
])
def test_a_field_out_of_its_place_is_reported(fixtures, key, message):
    held = harbor(fixtures, key)
    assert [(n, m) for _, n, m in spec_checks.field_place_findings(DUES, held.text_of[DUES], held)] == [(7, message)]
