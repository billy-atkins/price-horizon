"""The listing of cited sections: each place cited, with every place citing it."""
import pytest

pytestmark = [pytest.mark.reads("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary"),
              pytest.mark.reads("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")]


@pytest.fixture
def corpus(shared, fixtures, tools):
    """-> (the corpus's root, a search over every file of it), written and indexed by the first test of the file."""
    def build():
        root = tools.a_corpus(shared.folder / "project", fixtures)
        return root, shared.opened(root, cover=tools.files_under(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


@pytest.mark.action("--show-cited-sections", "--show-citers")
@pytest.mark.passes
def test_cited_sections_lists_each_place_cited_with_every_place_citing_it(corpus, tools, search, check):
    # the forms spec and the code cite the target spec's file, its sections Target and Table, the child of Target
    # and one record of it; one citation of the child stands bare in a fenced block of the forms spec
    root, s = corpus
    r = s.cited_sections()
    groups, order = {}, []
    for place in r.places:
        citing, _, cited = place.partition(" cites ")
        cited = cited.strip("`")
        order += [cited] if cited not in order else []
        groups.setdefault(cited, set()).add(citing)
    check("the listing is every place, each a citing place saying what it cites, and passes the check of a result's form",
          r.kind == "cited sections" and r.completeness == "complete" and search.Result.check(r.path) == [] and all(" cites `" in p for p in r.places), search.Result.check(r.path))
    check("a section, a section within it, a keyed part and a file are each listed as cited",
          {"specs/target.md § Target", "specs/target.md § Target § Child", "specs/target.md § Target [Name: first-record]", "specs/target.md", "specs/target.md § Table"} <= set(groups), sorted(groups))
    check("the places are ordered by what is cited, so the places citing one stand together", order == sorted(order), order)
    differ = {}
    for cited, citing in groups.items():
        alone = {str(p) for p in s.citers(cited).places}
        if alone != citing:
            differ[cited] = sorted(alone ^ citing)
    check(f"what it gives for each of the {len(groups)} places cited agrees with the places citing that one, asked alone", not differ, differ)
    check("a citation written bare in a fenced block is listed under the heading it names",
          any(p.startswith(f"`specs/forms.md § Fences` line {tools.line_holding(root, 'specs/forms.md', 'Do the work as specs/target.md')}, in a fenced block cites") for p in r.places if p.endswith("`specs/target.md § Target § Child`")), r.places)
    narrowed = s.cited_sections(["code"])
    check("narrowed to a folder, it lists the citing places in that folder alone", bool(narrowed.places) and all(p.startswith("`code/") for p in narrowed.places), narrowed.places)


@pytest.mark.action("--check-result")
@pytest.mark.reports
def test_a_result_saying_what_a_place_cites_is_in_its_form_only_as_a_listing_of_cited_sections(corpus, tools, check):
    # the test's variant of a result: the listing of cited sections, its Kind rewritten to that of a search for citers
    root, s = corpus
    r = s.cited_sections()
    problems = tools.changed(r.path, "**Kind:** cited sections", "**Kind:** citers")
    check("a result saying what a place cites is in its form only as a listing of cited sections", any("no listing of cited sections" in p for p in problems), problems)
