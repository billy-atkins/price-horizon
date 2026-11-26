"""The audit's check of departures from a registered standard: the script's kinds of a departure's reason are the
ones the mapping's Departs For row names, where the project holds that row's file, and each sentence of a methodology
file naming a departure from a registered standard cites its mapping's row; a project holding no register of its own
has it reported missing."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-departures.md", "specs-index-of-the-methodology",
                                "methodology-index-of-crusts-and-sourcing", "sourcing-index-of-external-reference",
                                "departure-reasons-row-in-order", "departure-reasons-row-of-two-kinds",
                                "register-of-one-standard", "crusts-departing-citing-the-row",
                                "crusts-departing-citing-no-row")]
ROW = "specs/methodology/sourcing-and-citation/external-reference.md"
CRUSTS = "specs/methodology/crusts.md"
BAKERY = {"specs-index-of-the-methodology": "specs/index.md",
          "methodology-index-of-crusts-and-sourcing": "specs/methodology/index.md",
          "sourcing-index-of-external-reference": "specs/methodology/sourcing-and-citation/index.md",
          "register-of-one-standard": "specs/methodology/external-references.md"}


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("row", ["departure-reasons-row-in-order", None], ids=["row-held", "no-row-held"])
def test_a_departure_citing_its_row_and_the_reasons_in_step_pass(fixtures, row):
    placed = BAKERY | {"crusts-departing-citing-the-row": CRUSTS} | ({row: ROW} if row else {})
    assert spec_checks.mapping_rule_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_the_reasons_out_of_step_with_the_departs_for_row_are_reported(fixtures):
    placed = BAKERY | {"crusts-departing-citing-the-row": CRUSTS, "departure-reasons-row-of-two-kinds": ROW}
    found = spec_checks.mapping_rule_findings(scope(fixtures, placed))
    assert [(path, line, message) for _, path, line, message in found] == [
        (ROW, 0, "the script's kinds of a departure's reason are not the Departs For row's: "
                 "[\"the standard's gap\", \"the canon's form\", 'no need yet']")]


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_departure_in_prose_citing_no_row_is_reported(fixtures):
    placed = BAKERY | {"crusts-departing-citing-no-row": CRUSTS, "departure-reasons-row-in-order": ROW}
    found = spec_checks.mapping_rule_findings(scope(fixtures, placed))
    assert [(path, line, message) for _, path, line, message in found] == [
        (CRUSTS, 5, "a departure from BreadML named in prose, citing no row of its mapping: "
                    "A crust's colour departs from BreadML, as the ovens need.")]


# @canon-spec specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_project_holding_no_register_is_reported(fixtures):
    placed = {k: p for k, p in BAKERY.items() if k != "register-of-one-standard"} | {"crusts-departing-citing-no-row": CRUSTS}
    found = spec_checks.mapping_rule_findings(scope(fixtures, placed))
    assert [(path, line, message) for _, path, line, message in found] == [
        ("specs/methodology/external-references.md", 0, "no register of external standards, so no departure from one is checked")]
