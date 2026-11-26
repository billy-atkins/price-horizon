"""The audit's check of a file's list of the technical files behind it: a list standing in a product spec alone,
naming technical files that stand in the project, in plain character order."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-layered-indexes.md", "index-of-a-layered-harbor-guide", "index-of-the-harbor-application",
                                "index-of-the-harbor-product", "index-of-the-harbor-technical"),
              pytest.mark.reads("audit-technical-specs.md", "moorings-naming-two-technical-files", "moorings-naming-itself",
                                "moorings-naming-two-technical-files-backwards", "moorings-naming-a-fuel-dock-file",
                                "berth-ledger", "chain-survey", "chain-survey-naming-the-berth-ledger")]
MOORINGS = "specs/application/product/moorings.md"
SURVEY = "specs/application/technical/chain-survey.md"
# the harbor's project by path: each path's fixture
HARBOUR = {"specs/index.md": "index-of-a-layered-harbor-guide", "specs/application/index.md": "index-of-the-harbor-application",
           "specs/application/product/index.md": "index-of-the-harbor-product",
           "specs/application/technical/index.md": "index-of-the-harbor-technical",
           "specs/application/technical/berth-ledger.md": "berth-ledger", SURVEY: "chain-survey",
           MOORINGS: "moorings-naming-two-technical-files"}


def harbor(fixtures, path=None, key=None):
    """-> the scope of the harbor's project, the fixture `key` standing at `path` where one is given."""
    files = {**HARBOUR, **({path: key} if path else {})}
    return scope(fixtures, {k: p for p, k in files.items()})


# @canon-spec specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_product_spec_naming_its_technical_files_in_order_passes(fixtures):
    held = harbor(fixtures)
    assert spec_checks.technical_specs_findings(MOORINGS, held.text_of[MOORINGS], held) == []


# @canon-spec specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("path, key, message", [
    (SURVEY, "chain-survey-naming-the-berth-ledger", "technical-specs appears outside a product spec"),
    (MOORINGS, "moorings-naming-itself", "technical-specs names a non-technical file: specs/application/product/moorings.md"),
    (MOORINGS, "moorings-naming-two-technical-files-backwards", "technical-specs is not sorted in plain character order"),
    (MOORINGS, "moorings-naming-a-fuel-dock-file", "technical-specs names a missing file: specs/application/technical/fuel-dock.md"),
])
def test_a_list_of_technical_files_out_of_its_form_is_reported(fixtures, path, key, message):
    held = harbor(fixtures, path, key)
    assert messages(spec_checks.technical_specs_findings(path, held.text_of[path], held)) == [message]
