"""The vectors the search computes: none as it brings its index up to date or answers a search by terms, and, for a
search by meaning, the vector of each passage and sentence the index holds none for, each computed once and kept."""
import pytest

from search_set import CORPUS, READS_CORPUS, every_file, project, vectors_held

pytestmark = READS_CORPUS
BY_TERMS = [
    pytest.param(lambda s: s.citers("specs/target.md § Target"), marks=pytest.mark.action("--show-citers"), id="citers"),
    pytest.param(lambda s: s.cited_sections(), marks=pytest.mark.action("--show-cited-sections"), id="cited-sections"),
    pytest.param(lambda s: s.lines("specs/target.md § Target"), marks=pytest.mark.action("--show-lines"), id="lines"),
    pytest.param(lambda s: s.terms("append entry"), marks=pytest.mark.action("--show-term-uses"), id="terms"),
    pytest.param(lambda s: s.pattern("§  +"), marks=pytest.mark.action("--show-pattern-matches"), id="pattern"),
    pytest.param(lambda s: s.code_structure("defines", "Ledger"), marks=pytest.mark.action("--show-code-structure"), id="code-structure"),
]


def embedded(s):
    """-> the vectors the index keeps, one to each text it computed one for."""
    return s.db.execute("select count(*) from embeddings").fetchone()[0]


def test_bringing_the_index_up_to_date_computes_no_vector(fixtures, opened, work):
    root = project(work / "project", fixtures, CORPUS)
    s = opened(root, cover=every_file(root), scratch=work / "index")
    assert s.built and embedded(s) == 0 and vectors_held(s)[0] == 0 and vectors_held(s)[1] > 0 and s.embedder is None


@pytest.mark.passes
@pytest.mark.parametrize("asked", BY_TERMS)
def test_a_search_by_terms_computes_no_vector(fixtures, opened, work, asked):
    root = project(work / "project", fixtures, CORPUS)
    s = opened(root, cover=every_file(root), scratch=work / "index")
    asked(s)
    assert embedded(s) == 0 and s.embedder is None


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_a_search_by_meaning_computes_the_vector_of_each_passage_and_sentence_missing_one(fixtures, opened, work):
    root = project(work / "project", fixtures, CORPUS)
    s = opened(root, cover=every_file(root), scratch=work / "index")
    s.meaning("Every posting is recorded a single time and never twice.")
    texts = s.db.execute("select count(*) from (select text_sha from passages union select text_sha from sentences)").fetchone()[0]
    held, of = vectors_held(s)
    assert texts > 0 and embedded(s) == texts and held == of


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "reeds-spec")
def test_a_later_search_by_meaning_computes_the_vectors_of_a_file_new_to_the_index_alone(fixtures, opened, work):
    # the corpus searched by meaning once, then given a spec on reeds, whose three sentences no other file holds
    root = project(work / "project", fixtures, CORPUS)
    first = opened(root, cover=every_file(root), scratch=work / "index")
    first.meaning("Every posting is recorded a single time and never twice.")
    before = embedded(first)
    first.db.close()
    project(root, fixtures, {"reeds-spec": "specs/reeds.md"})
    s = opened(root, cover=every_file(root), scratch=work / "index")
    assert embedded(s) == before
    s.meaning("Every posting is recorded a single time and never twice.")
    new = s.db.execute("select count(*) from (select p.text_sha from passages p join files f on f.sha=p.sha where f.path='specs/reeds.md'"
                       " union select x.text_sha from sentences x join files f on f.sha=x.sha where f.path='specs/reeds.md')").fetchone()[0]
    assert new == 3 and embedded(s) == before + new
