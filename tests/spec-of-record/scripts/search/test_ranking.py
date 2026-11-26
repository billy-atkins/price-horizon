"""A ranking by meaning: a sentence restated in a longer passage, and a ranking read in parts. The file's tests of parts
share one index of the invented library, built once in the file's folder: its ten files hold well over a hundred
passages, and its section on renewals is cited from three other sections, of the files on overdue items, on holds and
on rooms."""
import pytest

from search_set import LIBRARY, READS_LIBRARY, ask, every_file, line_holding, printed_places, project, search

ASKED = "A book that is out on loan may be kept longer only when no one else has asked for it."
RENEWALS = "specs/library/loans.md § Renewals"
WADING = "A wading bird stands in the reeds at dusk and waits for the tide."
RESTATED = pytest.mark.reads("search-restated-sentence.md", "stocktake-rule-and-counts", "warehouse-notes")


@pytest.fixture
def library(shared, fixtures):
    """-> a search over the library's ten files, written and indexed by the first test asking for it."""
    def build():
        root = project(shared.folder / "project", fixtures, LIBRARY)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "index")
    return shared.once("library", build)


def restating_place(fixtures, opened, work):
    """-> the number in the ranking of the passage restating the stocktake's rule, None where it is not among the
    first hundred: one file holds a rule on counts and more than twenty short statements sharing its words, the other
    one long paragraph on other subjects, one sentence of which restates the rule in other words."""
    root = project(work / "project", fixtures, {"stocktake-rule-and-counts": "product/stocktake.md", "warehouse-notes": "product/stock-notes.md"})
    rule = fixtures["stocktake-rule-and-counts"].split("## The Rule")[1].split("##")[0].strip()
    places = opened(root, cover=every_file(root), scratch=work / "index").meaning(rule, limit=100).places
    said = line_holding(fixtures["warehouse-notes"], "Whatever figure has gone into the book")
    return next((n for n, p in enumerate(places, 1) if p.path == "product/stock-notes.md" and p.first <= said <= p.last), None)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@RESTATED
def test_a_rule_restated_in_one_sentence_of_a_longer_passage_is_ranked_by_that_sentence_among_the_first_twenty(fixtures, opened, work):
    at = restating_place(fixtures, opened, work)
    assert at is not None and at <= search.RANKED


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@RESTATED
def test_with_no_sentence_ranked_the_passage_restating_a_rule_stands_outside_the_first_twenty(fixtures, opened, work, monkeypatch):
    # the same search with no sentence ranked, the passages alone, shows the case is one the sentences decide
    monkeypatch.setattr(search, "sentences", lambda text: [])
    at = restating_place(fixtures, opened, work)
    assert at is None or at > search.RANKED


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_ranking_read_past_its_first_places_holds_no_place_twice(library):
    places = library.meaning(ASKED, limit=100).places
    assert len(places) == 100 and len(set(places)) == 100


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_search_asked_for_no_part_gives_the_first_twenty_places_and_says_which_part_it_holds(library):
    first = library.meaning(ASKED)
    assert first.places == library.meaning(ASKED, limit=100).places[:search.RANKED] and first.ranking_part() == "1 to 20"
    assert "**Ranking Part:** 1 to 20" in first.path.read_text(encoding="utf-8")


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
@pytest.mark.parametrize("size", [20, 7, 64])
def test_parts_asked_one_after_another_make_up_the_ranking_no_place_twice_and_none_missed(library, size):
    read = [place for at in range(1, 101, size) for place in library.meaning(ASKED, limit=size, start=at).places][:100]
    assert read == library.meaning(ASKED, limit=100).places


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_part_further_on_says_which_places_of_the_ranking_it_holds_and_stands_beside_the_others(library):
    first, third = library.meaning(ASKED), library.meaning(ASKED, limit=20, start=41)
    assert third.ranking_part() == "41 to 60" and first.path.exists() and third.path.exists() and first.path != third.path


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_part_asked_past_the_end_of_the_ranking_holds_no_place_and_says_so(library):
    past = library.meaning(ASKED, limit=20, start=100000)
    assert past.places == [] and past.ranking_part() == "none"


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@READS_LIBRARY[0]
@READS_LIBRARY[1]
@pytest.mark.parametrize("part", [{"limit": 0}, {"start": 0}])
def test_a_limit_or_a_start_that_is_no_whole_number_from_one_is_refused(library, part):
    with pytest.raises(ValueError):
        library.meaning(ASKED, **part)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_asked_by_a_citation_parts_asked_one_after_another_make_up_the_ranking(library):
    whole = library.meaning(RENEWALS, limit=80)
    assert len(whole.places) == 80 and [p for at in (1, 21, 41, 61) for p in library.meaning(RENEWALS, limit=20, start=at).places] == whole.places


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_asked_by_a_citation_the_ranking_gives_back_neither_that_section_nor_a_place_whose_section_cites_it(library):
    citing = {(p.path, p.lineage) for p in library.citers(RENEWALS).places}
    left_out = citing | {("specs/library/loans.md", "Renewals")}
    assert len(citing) == 3 and [p for p in library.meaning(RENEWALS, limit=80).places if (p.path, p.lineage) in left_out] == []


@pytest.mark.action("--show-similar-passages", "--show-citers")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_asked_by_a_citation_the_places_whose_section_cites_it_are_listed_apart_whole(library):
    citing = {(p.path, p.lineage) for p in library.citers(RENEWALS).places}
    passages = {(path, first) for path, lineage in citing
                for (first,) in library.db.execute("select p.line_start from passages p join files f on f.sha=p.sha where f.path=? and p.lineage=?", (path, lineage))}
    apart = [note for note in library.meaning(RENEWALS, limit=80).notes if isinstance(note, search.Place)]
    assert apart and all((p.path, p.lineage) in citing for p in apart) and {(p.path, p.first) for p in apart} >= passages and len(set(apart)) == len(apart)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_the_places_listed_apart_are_the_same_with_every_part(library):
    whole = library.meaning(RENEWALS, limit=80)
    assert all(library.meaning(RENEWALS, limit=20, start=at).notes == whole.notes for at in (1, 21, 41, 61))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_asked_by_a_passage_the_search_leaves_nothing_out_and_lists_nothing_apart(library):
    r = library.meaning(ASKED, limit=120)
    assert r.notes == [] and any((p.path, p.lineage) == ("specs/library/loans.md", "Renewals") for p in r.places)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "seven-wading-birds")
def test_the_script_gives_the_part_of_a_ranking_its_limit_and_start_ask_for(fixtures, work, capsys):
    # seven sections each one sentence about a wading bird at dusk, so a ranking for such a sentence holds seven places
    root = project(work / "birds", fixtures, {"seven-wading-birds": "specs/birds.md"})
    assert ask(root, "--show-similar-passages", WADING, "--limit", "3", "--start", "2") == 0
    printed = capsys.readouterr().out
    assert len(printed_places(printed)) == 3 and "3 places, ranked" in printed


@pytest.mark.reports
@pytest.mark.reads("search-heron-project.md", "seven-wading-birds")
@pytest.mark.parametrize("argv", [
    pytest.param(["--show-similar-passages", WADING, "--limit", "0"], marks=pytest.mark.action("--show-similar-passages"), id="limit-of-none"),
    pytest.param(["--show-similar-passages", WADING, "--start", "two"], marks=pytest.mark.action("--show-similar-passages"), id="start-in-words"),
    pytest.param(["--show-citers", "specs/birds.md § The Heron", "--limit", "5"], marks=pytest.mark.action("--show-citers"), id="part-of-no-ranking"),
])
def test_the_script_refuses_a_part_that_is_no_whole_number_or_is_asked_of_no_ranking_and_writes_nothing(fixtures, work, capsys, argv):
    root = project(work / "birds", fixtures, {"seven-wading-birds": "specs/birds.md"})
    assert ask(root, *argv) == 2
    assert capsys.readouterr().out.startswith("usage:") and not (root / ".ai").exists()
