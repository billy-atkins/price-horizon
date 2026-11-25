"""A place a search gives: a citation of the narrowest thing holding its lines, saying what they stand in."""
import pytest

CORPUS_SPECS = ("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary")
CORPUS_CODE = ("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")
LENDING = ("search-library-lending.md", "library-membership", "library-loans", "library-overdue", "library-holds", "library-catalogue")
PREMISES = ("search-library-premises.md", "library-donations", "library-opening", "library-volunteers", "library-rooms", "library-events")
FORMS = "specs/forms.md"
SECTION = "`specs/forms.md § Where A Place Stands"


@pytest.fixture
def corpus(shared, fixtures, tools):
    """-> (the corpus's root, a search over every file of it), written and indexed by the first test asking for it."""
    def build():
        root = tools.a_corpus(shared.folder / "project", fixtures)
        return root, shared.opened(root, cover=tools.files_under(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads(*CORPUS_SPECS)
@pytest.mark.reads(*CORPUS_CODE)
def test_a_place_cites_the_narrowest_thing_holding_its_line_and_says_what_it_stands_in(corpus, tools, search, check):
    # the forms spec's section Where A Place Stands holds the word quillwort ten times: in running text, in a row of
    # a keyed table, in a row of a table declaring no key, in a record, in a record sharing the first one's key, in
    # a record keyed by a code span, in a fenced block, in an indented code block, in a heading, and in the text
    # under that heading
    root, s = corpus
    r = s.terms("quillwort")
    by = {p.first: p for p in r.places}
    n = lambda words: tools.line_holding(root, FORMS, words)
    at = lambda words: by.get(n(words))

    check("a place in running text is a citation of its section with its line, and says nothing of where it stands",
          at("Running text holding") == f"{SECTION}` line {n('Running text holding')}", at("Running text holding"))
    check("a place in a row of a table declaring its key cites the row's keyed part, and says it stands in a table",
          at("a tabled quillwort") == f"{SECTION} [Form: plain]` line {n('a tabled quillwort')}, in a table", at("a tabled quillwort"))
    check("a place in a row of a table declaring no key cites the section, and says it stands in a table",
          at("an unkeyed quillwort") == f"{SECTION}` line {n('an unkeyed quillwort')}, in a table", at("an unkeyed quillwort"))
    check("a place in a record cites the record's keyed part", at("a recorded quillwort") == f"{SECTION} [Name: a-record]` line {n('a recorded quillwort')}", at("a recorded quillwort"))
    check("a place in a record whose key an earlier record shares cites the section, since the key's citation names the earlier one",
          at("a second quillwort") == f"{SECTION}` line {n('a second quillwort')}", at("a second quillwort"))
    check("a place in a record whose key holds a code span cites the section, since a citation is written in a code span and cannot hold one",
          at("no citation can write") == f"{SECTION}` line {n('no citation can write')}", at("no citation can write"))
    check("a place in a fenced block says so", at("A fenced line holding") == f"{SECTION}` line {n('A fenced line holding')}, in a fenced block", at("A fenced line holding"))
    check("a place in an indented code block stands in none of a table, a heading and a fenced block",
          at("An indented code block's line") == f"{SECTION}` line {n('An indented code block')}", at("An indented code block's line"))
    check("a place in a heading cites the section the heading opens, and says it stands in a heading",
          at("### A Heading Holding Quillwort") == f"{SECTION} § A Heading Holding Quillwort` line {n('### A Heading Holding')}, in a heading", at("### A Heading Holding Quillwort"))
    check("the search for the word gave those nine places and the last line's, each in the form a result states for a place",
          len(r.places) == 10 and all(search.PLACE.match(p) for p in r.places) and search.Result.check(r.path) == [], (len(r.places), search.Result.check(r.path)))
    code = [x for x in s.terms("append entry").places if x.path.startswith("code/")]
    check("a place in code cites its file with its line", bool(code) and all(x == f"`{x.path}` line {x.first}" for x in code), code)


@pytest.mark.action("--show-pattern-matches", "--show-citers")
@pytest.mark.passes
@pytest.mark.reads(*CORPUS_SPECS)
@pytest.mark.reads(*CORPUS_CODE)
def test_a_place_of_several_lines_cites_what_holds_them_all(corpus, tools, check):
    # in the forms spec's section Where A Place Stands a keyed table of two rows runs from its header to the row
    # keyed cited, which holds a citation; a record's last line is followed by a fenced block; an indented code line
    # is followed by a heading; and the section before it ends on a sentence naming each journal line
    root, s = corpus
    n = lambda words: tools.line_holding(root, FORMS, words)
    first, last = n("| Form | Holds |"), n("| cited |")
    p = s._place(FORMS, first, last)
    check("a place whose lines hold several keyed parts cites their section with all its lines, and says they stand in a table",
          p == f"{SECTION}` lines {first}-{last}, in a table" and p.key is None, p)
    r = s.pattern(r"a code span\n\n```text\nA fenced line")
    check("a place whose lines stand in more than one of them says nothing of where it stands", [str(x) for x in r.places] == [f"{SECTION}` lines {n('no citation can write')}-{n('A fenced line holding')}"], r.places)
    r = s.pattern(r"line holding quillwort\.\n\n### A Heading")
    check("a place whose lines run from a section into a section beneath it cites the section holding both",
          [(x.lineage, x.first, x.last) for x in r.places] == [("Where A Place Stands", n("An indented code block"), n("### A Heading Holding"))], r.places)
    r = s.pattern(r"each journal line\.\n\n## Where A Place")
    check("a place whose lines run across two sections of a file cites the file",
          [str(x) for x in r.places] == [f"`specs/forms.md` lines {n('The LE is posted once')}-{n('## Where A Place Stands')}"], r.places)
    r = s.citers("specs/target.md § Table")
    cited = next((x for x in r.places if x.first == n("| cited |")), None)
    check("a citing place in a table's row cites the row and says it stands in a table", cited == f"{SECTION} [Form: cited]` line {n('| cited |')}, in a table", r.places)


@pytest.mark.action("--show-lines")
@pytest.mark.passes
@pytest.mark.reads(*LENDING)
@pytest.mark.reads(*PREMISES)
def test_every_keyed_part_a_place_can_cite_is_one_its_own_citation_gives_back(fixtures, tools, opened, work, check):
    # the library's files hold five keyed tables and two lists of records, thirty keyed parts in all, the records
    # each of two lines
    root = tools.a_library(work / "project", fixtures)
    s = opened(root, cover=tools.files_under(root), scratch=work / "index")
    parts = s.db.execute("select f.path, p.lineage, p.key, p.line_start, p.line_end from files f join parts p on p.sha=f.sha order by f.path, p.line_start").fetchall()
    wrong = []
    for path, lineage, key, start, end in parts:
        got = s.lines(f"{path} § {lineage} [{key}]").places
        if [(x.first, x.last) for x in got] != [(start, end)]:
            wrong.append((path, lineage, key, start, end, got))
    check(f"a citation of a keyed part gives back the part's own lines, for each of the {len(parts)} parts the library's files hold", len(parts) == 30 and not wrong, (len(parts), wrong[:3]))
    rows = [(path, key, start) for path, lineage, key, start, end in parts if end > start]
    inside = [(path, key, s._place(path, start + 1)) for path, key, start in rows]
    check("a line inside a record cites that record or one within it", len(inside) == 9 and all(x.key is not None for _, _, x in inside), [i for i in inside if i[2].key is None][:3])
