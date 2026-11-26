"""The audit's check that the section on clear prose still holds each table of words the script reads its words
from, by the table's name."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-voice-tables.md", "plain-writing-with-both-word-tables", "plain-writing-with-one-word-table",
                                "plain-writing-without-word-tables"),
              pytest.mark.reads("audit-index-chains.md", "index-of-specs-holding-a-methodology",
                                "index-of-a-methodology-holding-a-style-folder", "index-of-a-style-folder-holding-clear-prose")]
CLEAR_PROSE = "specs/methodology/spec-style/clear-prose.md"
INDEXED = {"index-of-specs-holding-a-methodology": "specs/index.md",
           "index-of-a-methodology-holding-a-style-folder": "specs/methodology/index.md",
           "index-of-a-style-folder-holding-clear-prose": "specs/methodology/spec-style/index.md"}


# @canon-spec specs/methodology/spec-style/clear-prose.md § Clear Prose
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_section_holding_each_table_of_words_passes(fixtures):
    placed = dict(INDEXED, **{"plain-writing-with-both-word-tables": CLEAR_PROSE})
    assert spec_checks.voice_table_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/spec-style/clear-prose.md § Clear Prose
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, found", [
    ("plain-writing-with-one-word-table", ["no table named Generic Terms, which the script reads its words from"]),
    ("plain-writing-without-word-tables", ["no table named Emphasis Words, which the script reads its words from",
                                           "no table named Generic Terms, which the script reads its words from"]),
])
def test_a_table_of_words_gone_from_the_section_is_reported(fixtures, key, found):
    placed = dict(INDEXED, **{key: CLEAR_PROSE})
    assert messages(spec_checks.voice_table_findings(scope(fixtures, placed))) == found
