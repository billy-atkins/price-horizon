"""A place a search gives: a citation of the narrowest thing holding its lines, saying what they stand in. The file's
tests share one index of the corpus of forms, built once in the file's folder: the forms spec's section Where A Place
Stands holds the word quillwort ten times, in running text, in a row of a keyed table, in a row of a table declaring
no key, in a record, in a record sharing the first one's key, in a record keyed by a code span, in a fenced block, in
an indented code block, in a heading, and in the text under that heading."""
import pytest

from search_set import CORPUS, LIBRARY, READS_CORPUS, READS_LIBRARY, every_file, line_holding, project, search

FORMS = "specs/forms.md"
SECTION = "`specs/forms.md § Where A Place Stands"


@pytest.fixture
def corpus(shared, fixtures):
    """-> a search over every file of the corpus, written and indexed by the first test asking for it."""
    def build():
        root = project(shared.folder / "corpus", fixtures, CORPUS)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "corpus-index")
    return shared.once("corpus", build)


@pytest.fixture
def library(shared, fixtures):
    """-> a search over the library's ten files, which hold five keyed tables and two lists of records, thirty keyed
    parts in all, the records each of two lines."""
    def build():
        root = project(shared.folder / "library", fixtures, LIBRARY)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "library-index")
    return shared.once("library", build)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
@pytest.mark.parametrize("words, cited, stands", [
    ("Running text holding", "", ""),
    ("a tabled quillwort", " [Form: plain]", ", in a table"),
    ("an unkeyed quillwort", "", ", in a table"),
    ("a recorded quillwort", " [Name: a-record]", ""),
    ("a second quillwort", "", ""),
    ("no citation can write", "", ""),
    ("A fenced line holding", "", ", in a fenced block"),
    ("An indented code block", "", ""),
    ("### A Heading Holding", " § A Heading Holding Quillwort", ", in a heading"),
], ids=["running-text", "keyed-table-row", "unkeyed-table-row", "record", "record-sharing-an-earlier-key", "record-keyed-by-a-code-span",
        "fenced-block", "indented-code-block", "heading"])
def test_a_place_cites_the_narrowest_thing_holding_its_line_and_says_what_it_stands_in(corpus, fixtures, words, cited, stands):
    line = line_holding(fixtures["forms-spec"], words)
    assert {p.first: p for p in corpus.terms("quillwort").places}.get(line) == f"{SECTION}{cited}` line {line}{stands}"


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_each_place_a_search_gives_is_in_the_form_a_result_states_for_a_place(corpus):
    places = corpus.terms("quillwort").places
    assert len(places) == 10 and all(search.PLACE.match(p) for p in places)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_place_in_code_cites_its_file_with_its_line(corpus):
    code = [p for p in corpus.terms("append entry").places if p.path.startswith("code/")]
    assert code and all(p == f"`{p.path}` line {p.first}" for p in code)


@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_place_whose_lines_hold_several_keyed_parts_cites_their_section_and_says_they_stand_in_a_table(corpus, fixtures):
    first, last = line_holding(fixtures["forms-spec"], "| Form | Holds |"), line_holding(fixtures["forms-spec"], "| cited |")
    p = corpus._place(FORMS, first, last)
    assert p == f"{SECTION}` lines {first}-{last}, in a table" and p.key is None


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
@pytest.mark.parametrize("expression, cited, first, last", [
    (r"a code span\n\n```text\nA fenced line", SECTION + "`", "no citation can write", "A fenced line holding"),
    (r"line holding quillwort\.\n\n### A Heading", SECTION + "`", "An indented code block", "### A Heading Holding"),
    (r"each journal line\.\n\n## Where A Place", "`specs/forms.md`", "The LE is posted once", "## Where A Place Stands"),
], ids=["standing-in-more-than-one-kind", "running-into-a-section-beneath", "running-across-two-sections"])
def test_a_place_of_several_lines_cites_what_holds_them_all_and_says_nothing_of_where_they_stand_unless_all_stand_in_one(corpus, fixtures, expression, cited, first, last):
    at = lambda words: line_holding(fixtures["forms-spec"], words)
    assert [str(x) for x in corpus.pattern(expression).places] == [f"{cited} lines {at(first)}-{at(last)}"]


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@READS_CORPUS[0]
@READS_CORPUS[1]
def test_a_citing_place_in_a_table_s_row_cites_the_row_and_says_it_stands_in_a_table(corpus, fixtures):
    line = line_holding(fixtures["forms-spec"], "| cited |")
    assert f"{SECTION} [Form: cited]` line {line}, in a table" in corpus.citers("specs/target.md § Table").places


def keyed_parts(library):
    return library.db.execute("select f.path, p.lineage, p.key, p.line_start, p.line_end from files f join parts p on p.sha=f.sha order by f.path, p.line_start").fetchall()


@pytest.mark.action("--show-lines")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_every_keyed_part_a_place_can_cite_is_one_its_own_citation_gives_back(library):
    parts = keyed_parts(library)
    assert len(parts) == 30
    assert [[(x.first, x.last) for x in library.lines(f"{path} § {lineage} [{key}]").places] for path, lineage, key, _, _ in parts] == [[(s, e)] for _, _, _, s, e in parts]


@READS_LIBRARY[0]
@READS_LIBRARY[1]
def test_a_line_inside_a_record_cites_that_record_or_one_within_it(library):
    inside = [library._place(path, start + 1) for path, _, _, start, end in keyed_parts(library) if end > start]
    assert len(inside) == 9 and all(x.key is not None for x in inside)
