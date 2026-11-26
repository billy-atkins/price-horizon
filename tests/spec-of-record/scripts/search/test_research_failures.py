"""The failures of a design's research the search answers for, each a test of what the search does: words that only
look alike, words standing apart, and a question asked in place of the rule's own words."""
import pytest

from search_set import LIBRARY, READS_LIBRARY, every_file, line_holding, lines_of, project, search

WORDS = pytest.mark.reads("search-words-apart.md", "read-again-and-read-against", "run-again-together-and-apart")
LOANS = "specs/library/loans.md"
QUESTION = "When does a member lose the right to take anything out?"


@pytest.fixture
def words(shared, fixtures):
    """-> a search over two files: one saying `read against` in one sentence and `read again` in another, the other
    saying `runs each Search again`, its words apart, in one sentence and `is run again` in another."""
    def build():
        root = project(shared.folder / "words", fixtures, {"read-again-and-read-against": "specs/reading.md", "run-again-together-and-apart": "specs/running.md"})
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "words-index")
    return shared.once("words", build)


@pytest.fixture
def library(shared, fixtures):
    """-> a search over the library's ten files, whose file on loans holds, as a paragraph of one sentence, the rule
    that a member owing more than five pounds borrows nothing until the debt is cleared."""
    def build():
        root = project(shared.folder / "library", fixtures, LIBRARY)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "library-index")
    return shared.once("library", build)


def place_of_the_rule(result, fixtures):
    rule = line_holding(fixtures["library-loans"], "A member owing more than five pounds borrows nothing")
    return next((n for n, p in enumerate(result.places, 1) if p.path == LOANS and p.first <= rule <= p.last), None)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_is_found_as_a_phrase_and_not_where_its_words_only_look_alike(words, fixtures):
    at = line_holding(fixtures["read-again-and-read-against"], "checked is read again")
    assert lines_of(words.terms("read again").places) == {("specs/reading.md", at)}


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_is_found_where_its_words_stand_together_in_whatever_form_each_takes(words, fixtures):
    assert ("specs/running.md", line_holding(fixtures["run-again-together-and-apart"], "is run again")) in lines_of(words.terms("run again").places)


# a limit of the search, stated in its skill: a term is searched as a phrase, its words in their order with none between
@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@WORDS
def test_a_term_is_not_found_where_other_words_stand_between_its_words(words, fixtures):
    assert ("specs/running.md", line_holding(fixtures["run-again-together-and-apart"], "runs each Search again")) not in lines_of(words.terms("run again").places)


# a limit of the search, stated in its skill: asked a question, it ranks the places worded as the question is, and the
# rule answering it, which shares almost none of its words, stands outside the first twenty
@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@READS_LIBRARY[0]
@READS_LIBRARY[1]
@pytest.mark.parametrize("limit", [None, 40])
def test_a_question_does_not_find_the_rule_answering_it(library, fixtures, limit):
    r = library.meaning(QUESTION, limit=limit)
    assert place_of_the_rule(r, fixtures) is None and r.ranking_part() == f"1 to {limit or search.RANKED}"


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_the_rule_asked_in_other_words_is_found_among_the_first_forty_places(library, fixtures):
    r = library.meaning("Someone with unpaid charges above five pounds may not take anything out until they settle up.", limit=40)
    assert place_of_the_rule(r, fixtures) is not None
