"""A question naming nothing to ask of: told to the caller, each case apart. The file's tests share one index of the
corpus of forms, which holds a spec at `specs/target.md` with a section Target, no section named No Such Section, no
file `specs/no-such-file.md` and no folder named nowhere."""
import pytest

from search_set import CORPUS, HERON, READS_CORPUS, READS_HERON, ask, every_file, project, search

NO_SECTION = "specs/target.md § No Such Section"


@pytest.fixture
def corpus(shared, fixtures):
    """-> a search over every file of the corpus, written and indexed by the first test of the file."""
    def build():
        root = project(shared.folder / "project", fixtures, CORPUS)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_question_naming_something_tells_its_caller_nothing_of_the_kind(corpus):
    asked = corpus.citers("specs/target.md § Target")
    assert asked.names_nothing == [] and asked.places


@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
@pytest.mark.parametrize("asked", [
    pytest.param(lambda s: s.citers(NO_SECTION), marks=pytest.mark.action("--show-citers"), id="citers"),
    pytest.param(lambda s: s.lines(NO_SECTION), marks=pytest.mark.action("--show-lines"), id="lines"),
    pytest.param(lambda s: s.citers("specs/no-such-file.md § Target"), marks=pytest.mark.action("--show-citers"), id="citers-of-a-file"),
    pytest.param(lambda s: s.meaning(NO_SECTION), marks=pytest.mark.action("--show-similar-passages"), id="meaning"),
])
def test_a_citation_naming_no_place_among_the_files_is_told_and_no_place_given(corpus, asked):
    r = asked(corpus)
    assert r.names_nothing == [search.NO_PLACE] and r.places == [] and any("does not resolve" in n for n in r.notes)


@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
@pytest.mark.parametrize("asked", [
    pytest.param(lambda s: s.terms("--- !!! ---"), marks=pytest.mark.action("--show-term-uses"), id="term"),
    pytest.param(lambda s: s.meaning("--- !!! ---"), marks=pytest.mark.action("--show-similar-passages"), id="passage"),
])
def test_a_term_or_a_passage_reducing_to_no_word_is_told(corpus, asked):
    r = asked(corpus)
    assert r.names_nothing == [search.NO_WORD] and any("reduces to no word" in n for n in r.notes)


@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
@pytest.mark.parametrize("asked", [
    pytest.param(lambda s: s.terms("posting", ["specs/nowhere"]), marks=pytest.mark.action("--show-term-uses"), id="term"),
    pytest.param(lambda s: s.pattern("posting", ["specs/nowhere"]), marks=pytest.mark.action("--show-pattern-matches"), id="pattern"),
])
def test_a_path_narrowed_to_under_which_no_file_of_the_target_stands_is_told_with_the_path(corpus, asked):
    r = asked(corpus)
    assert r.names_nothing == [search.NO_FILE] and r.places == [] and any("`specs/nowhere`" in n for n in r.notes)


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_the_one_path_holding_no_file_is_told_where_another_holds_some_and_the_answer_stands_for_the_other(corpus):
    r = corpus.terms("posting", ["specs", "specs/nowhere"])
    assert r.names_nothing == [search.NO_FILE] and r.places


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_pattern_holding_no_word_is_a_question_as_any_other(corpus):
    assert corpus.pattern("§  +").names_nothing == []


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_question_holding_two_cases_is_told_both_each_apart(corpus):
    assert sorted(corpus.terms("--- !!! ---", ["specs/nowhere"]).names_nothing) == sorted([search.NO_WORD, search.NO_FILE]) and len(set(search.NAMES_NOTHING)) == 3


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_an_answer_the_search_kept_tells_it_as_the_answer_computed_did(corpus):
    computed = corpus.terms("posting", ["code/nowhere"])
    kept = corpus.terms("posting", ["code/nowhere"])
    assert kept.kept and kept.names_nothing == computed.names_nothing == [search.NO_FILE] and kept.body() == computed.body()


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_HERON[0]
def test_a_search_of_the_working_files_given_a_path_holding_no_file_is_told_so(fixtures, opened, work):
    root = project(work / "heron", fixtures, HERON)
    r = opened(root, scratch=work / "index", target=search.WORKING, paths=[".ai/plans/no-such-plans"]).terms("heron")
    assert r.names_nothing == [search.NO_FILE] and r.places == []


@pytest.mark.reports
@READS_HERON[0]
@pytest.mark.parametrize("argv, case", [
    pytest.param(["--show-citers", NO_SECTION], search.NO_PLACE, marks=pytest.mark.action("--show-citers"), id="citation"),
    pytest.param(["--show-term-uses", "heron", "--paths", "specs/nowhere"], search.NO_FILE, marks=pytest.mark.action("--show-term-uses"), id="path"),
])
def test_the_script_says_what_a_question_named_nothing_by(fixtures, work, capsys, argv, case):
    assert ask(project(work / "heron", fixtures, HERON), *argv) == 0
    assert "the question names nothing to ask of: " + case in capsys.readouterr().out
