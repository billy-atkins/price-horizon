"""The audit's check of the direction a citation points: a product spec citing a product spec, and never the
methodology, by a section or by the whole file, nor the methodology a product spec."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-layered-indexes.md", "index-of-a-layered-harbor-guide", "index-of-the-harbor-method",
                                "index-of-the-harbor-application", "index-of-the-harbor-product"),
              pytest.mark.reads("audit-directions.md", "method-tides", "method-tides-citing-berths", "product-berths",
                                "moorings-citing-berths", "moorings-citing-tides", "moorings-naming-the-tides-file")]
TIDES = "specs/methodology/tides.md"
MOORINGS = "specs/application/product/moorings.md"
# the harbor's project by path: each path's fixture
HARBOUR = {"specs/index.md": "index-of-a-layered-harbor-guide", "specs/methodology/index.md": "index-of-the-harbor-method",
           "specs/application/index.md": "index-of-the-harbor-application",
           "specs/application/product/index.md": "index-of-the-harbor-product", TIDES: "method-tides",
           "specs/application/product/berths.md": "product-berths", MOORINGS: "moorings-citing-berths"}


def harbor(fixtures, path=None, key=None):
    """-> the scope of the harbor's project, the fixture `key` standing at `path` where one is given."""
    files = {**HARBOUR, **({path: key} if path else {})}
    return scope(fixtures, {k: p for p, k in files.items()})


# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_product_spec_citing_a_product_spec_passes(fixtures):
    held = harbor(fixtures)
    assert spec_checks.direction_findings(MOORINGS, held.text_of[MOORINGS], held) == []


# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("path, key, message", [
    (MOORINGS, "moorings-citing-tides", "product cites methodology: specs/methodology/tides.md"),
    (MOORINGS, "moorings-naming-the-tides-file", "product cites methodology: specs/methodology/tides.md"),
    (TIDES, "method-tides-citing-berths", "methodology cites product: specs/application/product/berths.md"),
])
def test_a_citation_crossing_between_the_methodology_and_the_application_is_reported(fixtures, path, key, message):
    held = harbor(fixtures, path, key)
    assert messages(spec_checks.direction_findings(path, held.text_of[path], held)) == [message]
