"""The audit's check of the glossary's form: it cites nothing and holds one table of bare terms under its one header,
in sorted order, each abbreviation in its own column and each definition ending with its other full names, none of
them a term or another term's."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-glossary.md", "bakery-glossary", "bakery-glossary-unsorted", "bakery-glossary-citing",
                                "bakery-glossary-under-another-header", "bakery-glossary-of-two-tables",
                                "bakery-glossary-other-name-a-term", "bakery-glossary-other-name-shared",
                                "bakery-glossary-abbreviated-in-a-definition", "bakery-glossary-other-name-mid-definition",
                                "bakery-glossary-term-not-bare")]
GLOSSARY = "specs/methodology/glossary/glossary.md"


# @canon-spec specs/methodology/glossary/writing-an-entry.md § Writing an Entry
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_glossary_in_its_form_passes(fixtures):
    assert spec_checks.glossary_findings(scope(fixtures, {"bakery-glossary": GLOSSARY})) == []


# @canon-spec specs/methodology/glossary/writing-an-entry.md § Writing an Entry
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    (None, [(0, "the glossary is missing")]),
    ("bakery-glossary-unsorted", [(0, "the terms are not in sorted order")]),
    ("bakery-glossary-citing", [(5, "the glossary cites nothing")]),
    ("bakery-glossary-under-another-header", [(0, "the table's header is not | Term | Abbreviation | Definition |")]),
    ("bakery-glossary-of-two-tables", [(0, "the glossary does not hold exactly one table"), (0, "the terms are not in sorted order")]),
    ("bakery-glossary-other-name-a-term", [(5, "Crust: the other name proving drawer is a term")]),
    ("bakery-glossary-other-name-shared", [(6, "Sourdough Starter: the other name rind also belongs to Crust")]),
    ("bakery-glossary-abbreviated-in-a-definition", [(5, "Proving Drawer: an abbreviation goes in its Abbreviation column")]),
    ("bakery-glossary-other-name-mid-definition", [(5, "Crust: other full names are the trailing sentence, Also called")]),
    ("bakery-glossary-term-not-bare", [(5, "not a bare term: Crust (baked)")]),
])
def test_a_glossary_out_of_its_form_is_reported(fixtures, key, found):
    placed = {key: GLOSSARY} if key else {}
    assert [(f[2], f[3]) for f in spec_checks.glossary_findings(scope(fixtures, placed))] == found
