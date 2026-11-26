"""The construct checks leave a form template out, a skill's or the core canon's, told by its name wherever it
sits: the placeholders of a construct it lays out are checked in no file so named, and in a file named otherwise
they are."""
import pytest

from audit_set import constructs

pytestmark = [pytest.mark.reads("audit-constructs-form-templates.md", "bed-plan-with-placeholders")]


def findings(fixtures, path):
    found, _, _ = constructs.run_checks({path: fixtures["bed-plan-with-placeholders"]})
    return found


# @canon-spec specs/methodology/scope/form-templates.md § Form Templates
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("path", ["specs/garden/bed-plan-form-template.md",
                                  ".ai/skills/garden/references/bed-plan-form-template.md"])
def test_a_construct_in_a_form_template_is_left_unchecked(fixtures, path):
    assert findings(fixtures, path) == []


# @canon-spec specs/methodology/scope/form-templates.md § Form Templates
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_the_same_construct_in_a_file_named_otherwise_is_checked(fixtures):
    path = "specs/garden/bed-plan.md"
    assert findings(fixtures, path) == [
        ("modeling-constructs.md § Constructs § Decision Table", path, 10,
         "a condition's header neither a fact's name nor a computation: {condition}")]
