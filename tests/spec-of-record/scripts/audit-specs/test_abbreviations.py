"""The audit's check of the abbreviations inside the house: each recorded once, in the glossary's own column or in the
application specs, as a bare abbreviation, and used nowhere else, its term spelled out instead."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-abbreviations.md", "proving-leaflet-spelled-out", "proving-leaflet-abbreviated",
                                "index-of-specs-holding-an-application", "index-of-a-bakery-application", "ovens-recording-dko",
                                "ovens-recording-pd", "ovens-recording-a-spaced-abbreviation"),
              pytest.mark.reads("audit-glossary.md", "bakery-glossary"),
              pytest.mark.reads("audit-skill-form.md", "registry-of-a-bread-skill")]
OVENS = "specs/application/ovens.md"
BAKERY = {"bakery-glossary": "specs/methodology/glossary/glossary.md", "proving-leaflet-spelled-out": "docs/proving.md",
          "index-of-specs-holding-an-application": "specs/index.md", "index-of-a-bakery-application": "specs/application/index.md",
          "ovens-recording-dko": OVENS}


# @canon-spec specs/methodology/glossary/using-an-abbreviation.md § Using an Abbreviation
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_abbreviations_recorded_once_and_spelled_out_elsewhere_pass(fixtures):
    assert spec_checks.abbreviation_findings(scope(fixtures, BAKERY)) == []


# @canon-spec specs/methodology/glossary/using-an-abbreviation.md § Using an Abbreviation
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("added, found", [
    ({"proving-leaflet-abbreviated": "docs/proving.md"},
     [("docs/proving.md", 3, "an abbreviation inside the house, for people only; spell out its term: PD")]),
    ({"proving-leaflet-abbreviated": ".ai/skills/bake-bread/SKILL.md",
      "registry-of-a-bread-skill": "specs/methodology/skills/registered-skills.md"},
     [(".ai/skills/bake-bread/SKILL.md", 3, "an abbreviation inside the house, for people only; spell out its term: PD")]),
    ({"ovens-recording-pd": OVENS}, [(OVENS, 3, "an abbreviation inside the house recorded a second time: PD")]),
    ({"ovens-recording-a-spaced-abbreviation": OVENS}, [(OVENS, 3, "not a bare abbreviation: D O")]),
])
def test_an_abbreviation_used_or_recorded_out_of_its_place_is_reported(fixtures, added, found):
    placed = {k: p for k, p in BAKERY.items() if p not in added.values()}
    assert [f[1:] for f in spec_checks.abbreviation_findings(scope(fixtures, dict(placed, **added)))] == found
