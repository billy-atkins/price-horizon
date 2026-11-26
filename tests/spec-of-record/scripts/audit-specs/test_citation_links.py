"""The audit's check of a citation's link: a citation in a file a person reads carries the link reaching the heading
it names, and a citation in a file agents read carries none."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-citation-links.md", "harbor-tides", "harbor-readme-citing-by-link", "harbor-readme-citing-bare",
                                "harbor-readme-citing-by-a-stale-link")]
TIDES = {"harbor-tides": "docs/tides.md"}


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § A Citation's Link
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_citation_carrying_the_link_it_resolves_to_passes(fixtures):
    placed = dict(TIDES, **{"harbor-readme-citing-by-link": "README.md"})
    assert spec_checks.citation_link_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § A Citation's Link
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, at, message", [
    ("harbor-readme-citing-bare", "README.md",
     "a citation's link missing, not reaching what the citation resolves to, or standing where none belongs"),
    ("harbor-readme-citing-by-a-stale-link", "README.md",
     "a citation's link missing, not reaching what the citation resolves to, or standing where none belongs"),
    ("harbor-readme-citing-by-link", ".ai/skills/moor-a-boat/SKILL.md", "a citation's link in a file agents read, which carries none"),
])
def test_a_citation_out_of_step_with_its_link_is_reported(fixtures, key, at, message):
    placed = dict(TIDES, **{key: at})
    assert [f[1:] for f in spec_checks.citation_link_findings(scope(fixtures, placed))] == [(at, 3, message)]
