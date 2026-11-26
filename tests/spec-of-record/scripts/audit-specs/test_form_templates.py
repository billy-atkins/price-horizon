"""The audit's check of a form template among the specifications: its first placeholder cites the section stating its
form, each heading it lays out is one of that form's parts, in their order, and each field it lays out for a record
type is a field the type declares, in the type's order."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-form-templates.md", "index-of-the-loaf-card", "loaf-card-form",
                                "loaf-card-template-in-its-form", "loaf-card-template-citing-no-form",
                                "loaf-card-template-of-a-rolls-heading", "loaf-card-template-of-notes-first",
                                "loaf-card-template-of-a-shape-field", "loaf-card-template-of-crust-before-weight")]
TEMPLATE = "specs/loaf-card-form-template.md"
BAKERY = {"index-of-the-loaf-card": "specs/index.md", "loaf-card-form": "specs/loaf-card.md"}


# @canon-spec specs/methodology/scope/form-templates.md § Form Templates § Script Checks [Name: form-template-in-its-form]
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_template_in_its_form_passes(fixtures):
    placed = BAKERY | {"loaf-card-template-in-its-form": TEMPLATE}
    assert spec_checks.form_template_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/scope/form-templates.md § Form Templates § Script Checks [Name: form-template-in-its-form]
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("loaf-card-template-citing-no-form", 1, "a form template whose first placeholder cites no section stating its form"),
    ("loaf-card-template-of-a-rolls-heading", 9, "a heading no part of its form gives: ## Rolls"),
    ("loaf-card-template-of-notes-first", 9, "a heading out of its form's order: ## Loaves"),
    ("loaf-card-template-of-a-shape-field", 10, "a field its record type does not declare: Shape"),
    ("loaf-card-template-of-crust-before-weight", 10, "a field out of its record type's order: Weight"),
])
def test_a_template_out_of_its_form_is_reported(fixtures, key, line, message):
    found = spec_checks.form_template_findings(scope(fixtures, BAKERY | {key: TEMPLATE}))
    assert [(path, n, m) for _, path, n, m in found] == [(TEMPLATE, line, message)]
