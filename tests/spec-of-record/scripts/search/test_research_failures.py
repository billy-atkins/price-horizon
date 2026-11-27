"""The failures of a design's research the search answers for, each a test of what the search does: words that only
look alike, words standing apart, and a question asked in place of the rule's own words, which is turned back."""
import pytest

from search_set import LIBRARY, READS_LIBRARY, every_file, line_holding, lines_of, project, search

PLACED = {"read-again-and-read-against": "specs/reading.md", "run-again-together-and-apart": "specs/running.md",
          "identifier-together-and-its-words-apart": "specs/building.md", "run-and-again-in-rows-cells-and-fields": "specs/checks.md",
          "run-again-apart-in-a-cell-a-field-and-a-wrapped-paragraph": "specs/rounds.md", "run-again-apart-in-fences-and-a-heading": "specs/fences.md",
          "run-again-apart-in-python-comments-docstrings-and-code": "specs/checker.py", "run-again-apart-in-code-fences": "specs/examples.md"}
WORDS = pytest.mark.reads("search-words-apart.md", *PLACED)
LOANS = "specs/library/loans.md"
QUESTION = "When does a member lose the right to take anything out?"


@pytest.fixture
def words(shared, fixtures):
    """-> a search over a project holding each fixture of words standing together and apart: in sentences, in two
    sentences of one line, in an identifier, in rows, cells and fields, within one cell, one field and one wrapped
    paragraph, in a heading and in fenced blocks, and in Python's comments, docstrings and strings."""
    def build():
        root = project(shared.folder / "words", fixtures, PLACED)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "words-index")
    return shared.once("words", build)


def marked(places, path):
    """-> {(first line, last line, whether marked words apart)} of a result's places in one file."""
    return {(p.first, p.last, p.apart) for p in places if p.path == path}


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
    at = line_holding(fixtures["run-again-together-and-apart"], "is run again")
    assert (at, at, False) in marked(words.terms("run again").places, "specs/running.md")


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_is_found_and_marked_where_other_words_stand_between_its_words_in_one_sentence(words, fixtures):
    at = line_holding(fixtures["run-again-together-and-apart"], "runs each Search again")
    found = [p for p in words.terms("run again").places if (p.path, p.first) == ("specs/running.md", at)]
    assert len(found) == 1 and found[0].apart and str(found[0]).endswith(" words apart")


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_asked_for_exact_is_found_only_where_its_words_stand_together(words, fixtures):
    held = fixtures["run-again-together-and-apart"]
    r = words.terms("run again", exact=True)
    assert not any(p.apart for p in r.places) and r.exact and "    **Exact:** yes \\\n" in r.path.read_text(encoding="utf-8")
    # asked for exact, the search gives what it gave before the change: the words together, the two sentences of one
    # line among them, read as the index reads a line
    assert lines_of(p for p in r.places if p.path == "specs/running.md") == {("specs/running.md", line_holding(held, "is run again")),
                                                                             ("specs/running.md", line_holding(held, "have run. Again"))}
    assert search.Result.check(r.path) == []


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_asked_for_exact_and_by_default_are_two_answers_each_kept_apart(words):
    default, exact = words.terms("run again"), words.terms("run again", exact=True)
    assert default.path != exact.path and any(p.apart for p in default.places)
    again = words.terms("run again", exact=True)
    assert again.kept and not any(p.apart for p in again.places) and words.terms("run again").kept


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@WORDS
def test_a_term_is_not_found_where_its_words_stand_in_two_sentences(words, fixtures):
    at = line_holding(fixtures["run-again-together-and-apart"], "have run. Again")
    assert ("specs/running.md", at) not in lines_of(words.terms("run again").places)


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@WORDS
def test_a_term_is_not_found_where_its_words_stand_in_two_rows_two_cells_or_two_fields(words):
    assert marked(words.terms("run again").places, "specs/checks.md") == set()


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_term_is_found_apart_within_one_cell_one_field_and_one_wrapped_paragraph(words, fixtures):
    held = fixtures["run-again-apart-in-a-cell-a-field-and-a-wrapped-paragraph"]
    cell, field = line_holding(held, "runs each check again"), line_holding(held, "runs every Search once again")
    wrapped = line_holding(held, "while the script runs")
    assert marked(words.terms("run again").places, "specs/rounds.md") == {(cell, cell, True), (field, field, True), (wrapped, wrapped + 1, True)}


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reports
@WORDS
def test_a_fence_holding_markdown_is_read_as_markdown_and_a_heading_and_another_fence_hold_no_prose(words, fixtures):
    at = line_holding(fixtures["run-again-apart-in-fences-and-a-heading"], "The checker runs each Search again")
    assert marked(words.terms("run again").places, "specs/fences.md") == {(at, at, True)}


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@WORDS
def test_a_fence_of_code_is_read_as_that_code_its_comments_prose(words, fixtures):
    held = fixtures["run-again-apart-in-code-fences"]
    python, typescript, csharp = (line_holding(held, said) for said in ("# The checker runs", "// The reviewer runs", "// The auditor runs"))
    called, ts_called, cs_called = (line_holding(held, said) for said in ("ran = run_again(report)", "runAgain(report)", "RunAgain(report)"))
    assert marked(words.terms("run again").places, "specs/examples.md") == {(python, python, True), (typescript, typescript, True), (csharp, csharp, True),
                                                                             (called, called, False), (ts_called, ts_called, False), (cs_called, cs_called, False)}


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reports
@WORDS
def test_code_holds_prose_in_its_comments_and_docstrings_alone(words, fixtures):
    # the words together in code are found whatever comment stands beside them, on the next line or on their own
    held = fixtures["run-again-apart-in-python-comments-docstrings-and-code"]
    doc, comment, together = line_holding(held, "which runs each Search"), line_holding(held, "# The checker runs"), line_holding(held, "it is run again")
    named, called = line_holding(held, "def run_again"), line_holding(held, "ran = run_again_later")
    assert marked(words.terms("run again").places, "specs/checker.py") == {(doc, doc, True), (comment, comment + 1, True), (together, together, False),
                                                                            (named, named, False), (called, called, False)}


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@WORDS
def test_an_identifier_is_not_found_where_the_words_it_splits_into_stand_apart(words, fixtures):
    # the index splits TypeScript into type and script, and only words a searcher writes apart may stand apart
    held = fixtures["identifier-together-and-its-words-apart"]
    at = line_holding(held, "written in TypeScript")
    assert marked(words.terms("TypeScript").places, "specs/building.md") == {(at, at, False)}


# asked a question, the search ranks nothing: the places worded as a question is are rarely the rule answering it,
# so its searcher is told to ask again in the words of a rule
@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_question_is_turned_back_with_the_message_and_no_result(library):
    results = library.scratch / "results"
    before = sorted(results.glob("*.md")) if results.is_dir() else []
    with pytest.raises(ValueError) as refused:
        library.meaning(QUESTION)
    assert str(refused.value) == search.QUESTION_TURNED_BACK
    assert (sorted(results.glob("*.md")) if results.is_dir() else []) == before


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_passage_holding_a_question_and_closing_on_a_statement_is_ranked(library):
    r = library.meaning("When does a member lose the right to take anything out? A member owing more than five pounds borrows nothing.")
    assert r.places and r.ranking_part() == f"1 to {search.RANKED}"


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_the_rule_asked_in_other_words_is_found_among_the_first_forty_places(library, fixtures):
    r = library.meaning("Someone with unpaid charges above five pounds may not take anything out until they settle up.", limit=40)
    assert place_of_the_rule(r, fixtures) is not None
