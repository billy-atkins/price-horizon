"""The listing of cited sections: each place cited, with every place citing it. The file's tests share one index of
the corpus of forms, built once in the file's folder: the forms spec and the code cite the target spec's file, its
sections Target and Table, the child of Target and one record of it, one citation of the child standing bare in a
fenced block of the forms spec."""
import pytest

from search_set import CORPUS, READS_CORPUS, every_file, line_holding, project

pytestmark = READS_CORPUS + [pytest.mark.action("--show-cited-sections"), pytest.mark.passes]


@pytest.fixture
def corpus(shared, fixtures):
    """-> a search over every file of the corpus, written and indexed by the first test of the file."""
    def build():
        root = project(shared.folder / "project", fixtures, CORPUS)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


def cited_by(result):
    """-> {what is cited: {each place citing it}} of a listing of cited sections."""
    groups = {}
    for place in result.places:
        citing, _, cited = place.partition(" cites ")
        groups.setdefault(cited.strip("`"), set()).add(citing)
    return groups


def test_the_listing_is_complete_and_each_place_says_what_it_cites(corpus):
    r = corpus.cited_sections()
    assert r.kind == "cited sections" and r.completeness == "complete" and r.places and all(" cites `" in p for p in r.places)


@pytest.mark.parametrize("cited", ["specs/target.md § Target", "specs/target.md § Target § Child", "specs/target.md § Target [Name: first-record]",
                                   "specs/target.md", "specs/target.md § Table"])
def test_a_section_a_section_within_it_a_keyed_part_and_a_file_are_each_listed_as_cited(corpus, cited):
    assert cited in cited_by(corpus.cited_sections())


def test_the_places_are_ordered_by_what_is_cited(corpus):
    order = list(dict.fromkeys(p.partition(" cites ")[2].strip("`") for p in corpus.cited_sections().places))
    assert order == sorted(order)


@pytest.mark.action("--show-citers")
def test_what_it_gives_for_each_place_cited_agrees_with_the_places_citing_that_one_asked_alone(corpus):
    groups = cited_by(corpus.cited_sections())
    assert {cited: {str(p) for p in corpus.citers(cited).places} for cited in groups} == groups


def test_a_citation_written_bare_in_a_fenced_block_is_listed_under_the_heading_it_names(corpus, fixtures):
    bare = line_holding(fixtures["forms-spec"], "Do the work as specs/target.md")
    assert f"`specs/forms.md § Fences` line {bare}, in a fenced block" in cited_by(corpus.cited_sections())["specs/target.md § Target § Child"]


def test_narrowed_to_a_folder_it_lists_the_citing_places_in_that_folder_alone(corpus):
    narrowed = corpus.cited_sections(["code"])
    assert narrowed.places and all(p.startswith("`code/") for p in narrowed.places)
