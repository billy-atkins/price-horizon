"""The one reading the search reads a file by: where a line stands, a fenced block as a unit, a heading's path and a
citation's form. The tests call the reading's units with a fixture's text."""
import pytest

from search_set import reading

TICK = "`" * 3
FORMS = pytest.mark.reads("search-reading-forms.md", "fences-headings-and-citations")
# the text holds, by its lines: a tilde fence at 5-9 with a heading and a backtick fence line inside it, a fence
# indented in a list item at 13-15, a three-backtick fence nested in a six-backtick one at 17-21, a block quoted in a
# note at 23-26, an indented code line at 28, a table at 30-31, the headings Twice at 33 and 37, and lines 39 and 40
# each holding a citation, line 40 a code span of three backticks too


@FORMS
@pytest.mark.parametrize("lines, stands", [
    (range(5, 10), reading.FENCED),
    ([10], reading.TEXT),
    ([13], reading.FENCED),
    ([28], reading.INDENTED),
    ([30, 31], reading.TABLE),
    ([40], reading.TEXT),
], ids=["tilde-fence", "after-the-fence", "fence-in-a-list-item", "indented-code", "table", "code-span-of-three-backticks"])
def test_a_line_is_told_for_what_it_stands_in(fixtures, lines, stands):
    read = reading.lines(fixtures["fences-headings-and-citations"])
    assert [read[n - 1].stands_in for n in lines] == [stands] * len(lines)


@FORMS
def test_the_fenced_blocks_of_a_text_are_each_fence_with_the_lines_of_its_fences(fixtures):
    assert [(b.opens, b.closes) for b in reading.blocks(fixtures["fences-headings-and-citations"])] == [(5, 9), (13, 15), (17, 21), (23, 26)]


@FORMS
def test_a_fence_indented_in_a_list_item_gives_a_block_dedented_by_the_fence_s_indentation(fixtures):
    block = reading.blocks(fixtures["fences-headings-and-citations"])[1]
    assert (block.word, block.content, block.before) == ("markdown", "## Drafted", "  ")


@FORMS
def test_a_fence_nested_in_a_longer_one_is_content_of_the_longer(fixtures):
    block = reading.blocks(fixtures["fences-headings-and-citations"])[2]
    assert (block.info, block.content) == ("outer", TICK + "inner\nheld\n" + TICK)


@FORMS
def test_a_block_quoted_in_a_note_has_its_quote_prefix_taken_off_its_lines(fixtures):
    block = reading.blocks(fixtures["fences-headings-and-citations"])[3]
    assert (block.word, block.before, block.content, block.closed) == ("mermaid", "> ", "flowchart LR\n  a --> b", True)


@FORMS
def test_the_live_text_blanks_each_fenced_line_to_its_own_length(fixtures):
    text = fixtures["fences-headings-and-citations"]
    live = reading.live(text)
    assert len(live) == len(text) and live.split("\n")[5] == " " * len("## Not A Heading") and live.split("\n")[2] == "## First"


@FORMS
def test_a_heading_in_a_fenced_block_is_no_heading(fixtures):
    assert [h.title for h in reading.headings(fixtures["fences-headings-and-citations"])] == ["Title", "First", "Twice", "Twice"]


@FORMS
def test_of_two_headings_sharing_a_path_the_path_names_the_first_and_the_second_is_marked(fixtures):
    text = fixtures["fences-headings-and-citations"]
    assert [h.repeated for h in reading.headings(text)] == [False, False, False, True] and reading.sections(text)[("Twice",)].line == 33


@FORMS
@pytest.mark.parametrize("line, lineage", [(1, ()), (3, ("First",)), (8, ("First",)), (39, ("Twice",))])
def test_each_line_stands_under_the_heading_path_above_it(fixtures, line, lineage):
    assert reading.lines(fixtures["fences-headings-and-citations"])[line - 1].lineage == lineage


@FORMS
def test_a_citation_gives_its_file_its_heading_path_and_its_line(fixtures):
    cites = reading.citations(fixtures["fences-headings-and-citations"])
    assert [(c.file, c.lineage, c.line) for c in cites] == [("specs/a.md", ("A", "B"), 39), ("", ("Table",), 40)]


@FORMS
def test_a_keyed_part_gives_a_pair_to_each_key_and_a_key_written_as_a_path_gives_its_names(fixtures):
    cites = reading.citations(fixtures["fences-headings-and-citations"])
    assert [c.part for c in cites] == [((("Country",), "Canada"), (("Tax Year",), "2025")), ((("States", "State"), "open"),)]


@pytest.mark.parametrize("written, lineage", [("specs/a.md", ()), ("a word", None), ("README.md", None)])
def test_a_whole_file_s_citation_gives_no_heading_path_and_text_that_is_no_citation_gives_none(written, lineage):
    cited = reading.parse_citation(written)
    assert (cited.lineage if cited else None) == lineage


@pytest.mark.reads("search-reading-forms.md", "one-diagram-block", "diagram-lines-unfenced")
@pytest.mark.parametrize("key, contents", [("one-diagram-block", ["flowchart TD"]), ("diagram-lines-unfenced", [])])
def test_the_reading_answers_for_any_text_one_that_is_no_file_among_them(fixtures, key, contents):
    assert [b.content for b in reading.blocks(fixtures[key])] == contents


def test_the_reading_needs_nothing_a_search_requires():
    assert not ({"search", "sqlite3", "spec_text"} & set(vars(reading)))
