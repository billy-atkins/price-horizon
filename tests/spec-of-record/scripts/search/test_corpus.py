"""Each kind of search over the corpus of forms: two specs, a product file, a glossary and code in five languages,
which hold faults on purpose, a doubled space in a citation, a heading path standing twice and headings inside fenced
blocks among them. The file's tests share one index of the corpus, built once in the file's folder."""
import pytest

from search_set import CORPUS, READS_CORPUS, every_file, line_holding, lines_of, project, search

pytestmark = READS_CORPUS
FORMS = "specs/forms.md"
TARGET = "specs/target.md § Target"
# an annotation line of a fixture, its tag written in two parts so this file's own line reads as no annotation
ANNOTATED = "# @canon" "-spec specs/target.md § Target"
SHARED_PATH = "the path `Twice` stands more than once in the file, 2 times"


@pytest.fixture
def corpus(shared, fixtures):
    """-> a search over every file of the corpus, written and indexed by the first test of the file."""
    def build():
        root = project(shared.folder / "project", fixtures, CORPUS)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


@pytest.fixture
def at(fixtures):
    """-> at(words): the line of the forms spec holding the words."""
    return lambda words: line_holding(fixtures["forms-spec"], words)


def test_a_heading_inside_a_fenced_block_is_no_heading_of_its_file(corpus):
    # the forms spec writes headings inside a tilde fence, a fence indented in a list item and a fence nested in a
    # longer one; its own headings are the eight named here, the path Twice standing twice
    heads = [r[0] for r in corpus.db.execute("select h.lineage from files f join headings h on h.sha=f.sha where f.path=? and h.lineage != '' order by h.line", (FORMS,))]
    assert heads == ["Citations", "Fences", "After The Fences", "Twice", "Twice", "Terms", "Where A Place Stands", "Where A Place Stands § A Heading Holding Quillwort"]


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_citers_lists_every_place_citing_a_section_in_whatever_form(corpus, at):
    # the forms spec cites the section plainly, with a doubled space, across two lines, with a link, inside a tilde
    # fence, inside a backtick fence and as a fenced annotation; the code annotates it in Python, TypeScript and YAML
    want = {(FORMS, at(w)) for w in ("A plain citation", "a doubled space", "broken across lines", "carrying its link", "The span: `specs/target.md § Target`", ANNOTATED)}
    want |= {(FORMS, at("## Not A Heading In Tildes") + 1), ("code/sample.py", 11), ("code/sample.ts", 7), ("code/settings.yaml", 1)}
    assert lines_of(corpus.citers(TARGET).places) == want


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@pytest.mark.parametrize("words", ["A mention that is no citation", "A same-file citation of the block"])
def test_a_mention_outside_a_code_span_and_a_same_file_citation_in_a_fenced_markdown_block_cite_no_other_file(corpus, at, words):
    assert (FORMS, at(words)) not in lines_of(corpus.citers(TARGET).places)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_citing_place_in_a_fenced_block_says_so_and_no_other_does(corpus, at):
    places = corpus.citers(TARGET).places
    assert sorted(p.first for p in places if p.stands == "fenced block") == sorted([at("The span: `specs/target.md § Target`"), at(ANNOTATED), at("## Not A Heading In Tildes") + 1])
    assert all(p.endswith(", in a fenced block") == (p.stands == "fenced block") for p in places)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_citation_written_bare_in_a_fenced_block_is_read_to_the_heading_it_names(corpus, at):
    said = f"`specs/forms.md § Fences` line {at('Do the work as specs/target.md')}, in a fenced block: cites a section within it, as `specs/target.md § Target § Child`"
    assert any(n.startswith(said) for n in corpus.citers(TARGET).notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_keyed_part_s_citers_are_listed_with_the_places_citing_the_section_holding_it_told_apart(corpus, at):
    part = corpus.citers(TARGET + " [Name: first-record]")
    assert lines_of(part.places) == {(FORMS, at("A citation of a part of it"))} and sum(": cites the section holding it" in n for n in part.notes) >= 5


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@pytest.mark.parametrize("said", ["an annotation over the unit `Ledger`", "cites a section within it", "cites a part of it, `[Name: first-record]`", "cites its file"])
def test_a_place_citing_a_section_within_it_a_part_of_it_or_its_file_is_told_apart_and_an_annotation_with_its_unit(corpus, said):
    assert said in "\n".join(corpus.citers(TARGET).notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_the_same_search_gives_the_same_file_s_name(corpus):
    assert corpus.citers(TARGET).name == corpus.citers(TARGET).name


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_citation_asked_for_with_loose_white_space_is_the_same_citation(corpus):
    assert lines_of(corpus.citers("specs/target.md  §   Target").places) == lines_of(corpus.citers(TARGET).places)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_technical_specs_entry_is_listed_with_its_file_s_citers_marked_as_a_label(corpus):
    r = corpus.citers("specs/target.md")
    assert ("product/promise.md", 3) in lines_of(r.places) and "a `technical-specs` label, not a citation" in "\n".join(r.notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_citation_after_a_fenced_block_is_placed_at_its_own_line_and_section_and_not_marked_as_fenced(corpus, at):
    after = at("A citation after every fenced block")
    r = corpus.citers("specs/target.md § Table")
    assert f"`specs/forms.md § After The Fences` line {after}" in r.places and not any(n.startswith(f"`specs/forms.md § After The Fences` line {after}:") for n in r.notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_an_annotation_in_a_language_with_no_parser_is_still_a_citer(corpus):
    assert {("code/schema.sql", 1), ("code/sample.py", 3)} <= lines_of(corpus.citers("specs/target.md § Table").places)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_search_narrowed_to_a_folder_lists_no_place_outside_it(corpus):
    assert {p for p, _ in lines_of(corpus.citers(TARGET, ["code"]).places)} == {"code/sample.py", "code/sample.ts", "code/settings.yaml"}


@pytest.mark.action("--show-lines")
@pytest.mark.passes
@pytest.mark.parametrize("cited, places", [
    (TARGET, ["`specs/target.md § Target` lines 5-15"]),
    (TARGET + " § Child", ["`specs/target.md § Target § Child` lines 16-19"]),
    (TARGET + " [Name: second-record]", ["`specs/target.md § Target [Name: second-record]` lines 13-14"]),
    ("specs/target.md § Table [States.State: closed]", ["`specs/target.md § Table [States.State: closed]` line 27, in a table"]),
], ids=["section", "child", "record", "table-row"])
def test_lines_gives_the_lines_of_what_a_citation_names(corpus, cited, places):
    # the target spec holds text before its first section at lines 1-4, the section Target at 5-15 with a record at
    # 13-14, its child at 16-19, and a table whose row for the state closed stands at line 27
    assert corpus.lines(cited).places == places


@pytest.mark.action("--show-lines")
@pytest.mark.passes
@pytest.mark.parametrize("cited, notes", [
    (TARGET, ["lines 5-19: its whole subtree", "lines 1-4: its file's text"]),
    (TARGET + " § Child", ["lines 5-19: its parent whole", "lines 5-15: an ancestor's text"]),
], ids=["section", "child"])
def test_lines_notes_what_holds_the_lines_named(corpus, cited, notes):
    assert all(any(said in n for n in corpus.lines(cited).notes) for said in notes)


@pytest.mark.action("--show-lines")
@pytest.mark.reports
def test_lines_reports_a_citation_that_does_not_resolve_with_why(corpus):
    r = corpus.lines("specs/target.md § Missing")
    assert not r.places and "holds no section `Missing`" in r.notes[0]


def twice(fixtures):
    """-> the lines of the forms spec's two headings sharing the path Twice."""
    return [n for n, line in enumerate(fixtures["forms-spec"].split("\n"), 1) if line == "## Twice"]


@pytest.mark.action("--show-lines")
@pytest.mark.passes
def test_a_citation_of_a_path_two_headings_share_gives_the_lines_of_both_and_says_where_the_path_stands(corpus, fixtures, at):
    first, second = twice(fixtures)
    r = corpus.lines("specs/forms.md § Twice")
    assert r.places == [f"`specs/forms.md § Twice` lines {first}-{second - 1}", f"`specs/forms.md § Twice` lines {second}-{at('## Terms') - 1}"]
    assert any(f"{SHARED_PATH}, at lines {first}, {second}" in n for n in r.notes)


@pytest.mark.passes
@pytest.mark.parametrize("kind", [pytest.param("terms", marks=pytest.mark.action("--show-term-uses")),
                                  pytest.param("pattern", marks=pytest.mark.action("--show-pattern-matches"))])
@pytest.mark.parametrize("words, sentence", [("first section of this path", "The first section"), ("second section of this path", "The second section")],
                         ids=["first", "second"])
def test_a_place_under_either_of_two_headings_sharing_a_path_is_cited_by_the_path_with_its_own_line(corpus, at, kind, words, sentence):
    r = getattr(corpus, kind)(words)
    assert [str(p) for p in r.places] == [f"`specs/forms.md § Twice` line {at(sentence)}"] and any(SHARED_PATH in n for n in r.notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_citation_under_each_of_two_headings_sharing_a_path_is_found_cited_by_the_path(corpus, at):
    r = corpus.citers("specs/forms.md § Terms")
    assert {f"`specs/forms.md § Twice` line {at('trims the lamp wick')}", f"`specs/forms.md § Twice` line {at('ferry across the estuary')}"} <= set(r.places)
    assert any(SHARED_PATH in n for n in r.notes)


@pytest.mark.passes
@pytest.mark.parametrize("name", ["lamp-first", "lamp-second"])
@pytest.mark.parametrize("kind", [pytest.param("lines", marks=pytest.mark.action("--show-lines")),
                                  pytest.param("terms", marks=pytest.mark.action("--show-term-uses"))])
def test_a_keyed_part_under_either_of_two_headings_sharing_a_path_is_cited_by_its_own_citation(corpus, at, name, kind):
    line = at(f"**Name:** {name}")
    if kind == "lines":
        assert corpus.lines(f"specs/forms.md § Twice [Name: {name}]").places == [f"`specs/forms.md § Twice [Name: {name}]` lines {line}-{line + 1}"]
    else:
        assert [str(p) for p in corpus.terms(name).places] == [f"`specs/forms.md § Twice [Name: {name}]` line {line}"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_terms_finds_a_term_in_every_form_it_takes_and_marks_where_its_words_stand_apart(corpus, at):
    # the forms spec writes the term append entry as a function's name, a flag, a class's name, a plural and a phrase
    # broken across two lines, and once with its words standing apart in one sentence, which is found marked words
    # apart; the code calls and defines it in three languages
    together = {(FORMS, at(w)) for w in ("function append_entry", "flag --append-entry", "class AppendEntry", "appending entries", "the clerk will append")}
    together |= {("code/sample.py", 19), ("code/sample.py", 27), ("code/sample.ts", 12), ("code/sample.ts", 18), ("code/sample.cs", 12), ("code/sample.cs", 15)}
    places = corpus.terms("append entry").places
    assert lines_of(p for p in places if not p.apart) == together
    assert lines_of(p for p in places if p.apart) == {(FORMS, at("Nothing here appends an unrelated thing"))}
    assert lines_of(corpus.terms("append entry", exact=True).places) == together


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_terms_finds_a_term_under_each_other_name_the_project_s_glossary_gives_it_and_names_the_forms_searched(corpus, at):
    # the glossary gives ledger entry the abbreviation LE and the other name journal line
    r = corpus.terms("ledger entry")
    assert {(FORMS, at("The LE is posted once")), ("specs/target.md", 7)} <= lines_of(r.places) and "`LE`" in r.run_as and "`journal line`" in r.run_as


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
@pytest.mark.parametrize("expression, words", [
    ("§  +", "a doubled space"),
    (r"\]\(/specs/target\.md#target\)", "carrying its link"),
    (r"§\nTarget", "broken across lines"),
], ids=["only-where-it-matches", "a-link-as-written", "across-lines"])
def test_pattern_lists_every_place_an_expression_matches_over_a_file_s_whole_text_as_written(corpus, at, expression, words):
    assert lines_of(corpus.pattern(expression).places) == {(FORMS, at(words))}


def units(corpus, structure, name):
    """-> {file:line unit} of each unit a search for a structure lists."""
    r = corpus.code_structure(structure, name)
    return {n.split(": the unit ")[0].replace("` line ", ":").strip("`") + " " + n.split(": the unit ")[1].strip("`") for n in r.notes if ": the unit `" in n}


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
@pytest.mark.parametrize("structure, name, found", [
    ("calls", "append_entry", {"code/sample.py:19 Ledger.post"}),
    ("calls", "appendEntry", {"code/sample.ts:12 Ledger.post"}),
    ("calls", "AppendEntry", {"code/sample.cs:12 Ledger.Post"}),
    ("constructs", "Receipt", {"code/sample.py:18 Ledger.post", "code/sample.ts:11 Ledger.post", "code/sample.cs:11 Ledger.Post"}),
    ("extends", "Base", {"code/sample.py:13 Ledger", "code/sample.ts:8 Ledger", "code/sample.cs:6 Ledger"}),
    ("implements", "Auditable", {"code/sample.ts:8 Ledger"}),
    ("implements", "IAuditable", {"code/sample.cs:6 Ledger"}),
    ("defines", "Ledger", {"code/sample.py:13 Ledger", "code/sample.ts:8 Ledger", "code/sample.cs:6 Ledger"}),
])
def test_code_structure_lists_the_units_holding_a_structure_in_each_language(corpus, structure, name, found):
    # each of the three samples of code holds a class Ledger that extends Base, and a method that constructs a
    # Receipt and calls the function appending an entry
    assert units(corpus, structure, name) == found


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
@pytest.mark.parametrize("structure", ["calls", "constructs", "references"])
@pytest.mark.parametrize("name", ["Fake", "calls_in_a_string", "calls_in_a_comment", "callsInAString", "callsInAComment", "CallsInAString", "CallsInAComment"])
def test_code_structure_never_matches_a_name_in_a_comment_or_a_string(corpus, structure, name):
    assert units(corpus, structure, name) == set()


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
@pytest.mark.parametrize("said", ["`code/sample.py` line 12: the unit `Ledger`", "`code/sample.cs` line 5: the unit `Ledger`",
                                  "`code/settings.yaml`: YAML has no units", "`code/schema.sql`: the search has no parser for a .sql file"])
def test_code_structure_lists_a_unit_carrying_an_annotation_and_names_a_language_with_no_units_or_no_parser(corpus, said):
    assert said in "\n".join(corpus.code_structure("annotated-with", TARGET + " § Child").notes)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_a_result_s_file_holds_its_own_name_says_its_places_are_to_read_and_whether_they_are_every_place(corpus):
    r = corpus.citers("specs/target.md § Table")
    held = r.path.read_text(encoding="utf-8")
    assert held.count(r.name) == 1 and "places to read, never findings" in held and "**Completeness:** complete" in held


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_a_result_s_name_is_one_every_system_holds(corpus):
    long = corpus.terms("append entry " + "and a very long question holding a section sign § brackets [ ] and slashes / \\ " * 6)
    assert len(long.name) <= search.MAX_NAME and set(long.name) <= set("abcdefghijklmnopqrstuvwxyz0123456789-.")


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_meaning_asked_by_a_citation_lists_a_place_whose_section_cites_it_apart_from_the_ranking(corpus):
    # the forms spec's section Citations cites the target spec's section Target
    r = corpus.meaning(TARGET)
    assert not any(p.startswith("`specs/forms.md § Citations`") for p in r.places) and any(n.startswith("`specs/forms.md § Citations`") for n in r.notes)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_meaning_ranks_a_place_saying_the_same_in_other_words_among_its_first(corpus):
    # the product file says each posting is written exactly one time
    r = corpus.meaning("Every posting is recorded a single time and never twice.")
    assert r.completeness == "ranked" and any(p.startswith("`product/promise.md § What Is Promised`") for p in r.places[:3])


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.parametrize("asked, words", [
    ("A boat crossing the river mouth takes at most forty people while the high spring tide runs.", "ferry across the estuary"),
    ("Each evening before dark the lighthouse keeper cuts back the wick of the lamp.", "trims the lamp wick"),
], ids=["second", "first"])
def test_meaning_gives_a_passage_under_either_of_two_headings_sharing_a_path_cited_by_the_path_with_its_own_lines(corpus, at, asked, words):
    # each of the two sections sharing the path Twice holds one sentence, on a lighthouse keeper's lamp and on a
    # ferry's passengers
    r = corpus.meaning(asked)
    assert f"`specs/forms.md § Twice` line {at(words)}" in r.places[:5] and any(SHARED_PATH in n for n in r.notes)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_meaning_asked_by_a_path_two_headings_share_takes_what_both_hold_and_gives_a_passage_of_neither(corpus):
    r = corpus.meaning("specs/forms.md § Twice", limit=200)
    assert r.places and not any(p.startswith("`specs/forms.md § Twice`") for p in r.places)
