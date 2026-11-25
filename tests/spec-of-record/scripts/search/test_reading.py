"""The one reading the search reads a file by: where a line stands, a fenced block as a unit, a heading's path and a
citation's form. No action of the entry script gives these, so the tests drive the shared code."""
import pytest

TICK = "`" * 3


@pytest.mark.reads("search-reading-forms.md", "fences-headings-and-citations")
def test_a_line_is_told_for_what_it_stands_in_and_a_fenced_block_is_read_as_a_unit(fixtures, reading, check):
    # the text holds, by its lines: a tilde fence at 5-9 with a heading and a backtick fence line inside it, a fence
    # indented in a list item at 13-15, a three-backtick fence nested in a six-backtick one at 17-21, a block quoted
    # in a note at 23-26, an indented code line at 28 and a table at 30-31
    text = fixtures["fences-headings-and-citations"]
    read, found = reading.lines(text), reading.blocks(text)
    stands = lambda n: read[n - 1].stands_in
    check("a line in a tilde fence is fenced, a heading and a backtick fence written inside it among them",
          [stands(n) for n in range(5, 10)] == [reading.FENCED] * 5 and stands(10) == reading.TEXT, [stands(n) for n in range(5, 11)])
    check("a fence indented in a list item is a fence, and its block is dedented by the fence's indentation",
          stands(13) == reading.FENCED and found[1].word == "markdown" and found[1].content == "## Drafted" and found[1].before == "  ", (found[1].info, found[1].content, found[1].before))
    check("a fence nested in a longer one is content of the longer and no block of its own",
          found[2].info == "outer" and found[2].content == TICK + "inner\nheld\n" + TICK and (found[2].opens, found[2].closes) == (17, 21), (found[2].opens, found[2].closes, found[2].content))
    check("a block quoted in a note is a block, its quote prefix what stands before its fence and taken off its lines",
          found[3].word == "mermaid" and found[3].before == "> " and found[3].content == "flowchart LR\n  a --> b" and found[3].closed, (found[3].before, found[3].content))
    check("the blocks are those four, each with the lines of its fences", [(b.opens, b.closes) for b in found] == [(5, 9), (13, 15), (17, 21), (23, 26)], [(b.opens, b.closes) for b in found])
    check("a line of an indented code block stands in one, and a table's line in a table",
          stands(28) == reading.INDENTED and stands(30) == reading.TABLE and stands(31) == reading.TABLE, (stands(28), stands(30)))
    live = reading.live(text)
    check("the live text blanks each fenced line to its own length, so a place in it is the same place in the text",
          len(live) == len(text) and live.split("\n")[5] == " " * len("## Not A Heading") and live.split("\n")[2] == "## First")


@pytest.mark.reads("search-reading-forms.md", "fences-headings-and-citations")
def test_a_heading_is_read_with_its_path_and_a_path_standing_twice_is_marked(fixtures, reading, check):
    # the text's headings are Title at 1, First at 3 and Twice at 33 and at 37; a heading at 6 and one at 14 stand
    # in fenced blocks, and line 40 holds a code span of three backticks that opens no line
    text = fixtures["fences-headings-and-citations"]
    read, heads = reading.lines(text), reading.headings(text)
    check("a heading in a fenced block is no heading, and a code span of three backticks opening no line is no fence",
          [h.title for h in heads] == ["Title", "First", "Twice", "Twice"] and read[39].stands_in == reading.TEXT, [h.title for h in heads])
    check("of two headings sharing a path the path names the first, and the second is marked",
          [h.repeated for h in heads] == [False, False, False, True] and reading.sections(text)[("Twice",)].line == 33, [(h.line, h.repeated) for h in heads])
    check("each line stands under the heading path above it", read[2].lineage == ("First",) and read[7].lineage == ("First",) and read[38].lineage == ("Twice",) and read[0].lineage == (), read[38].lineage)


@pytest.mark.reads("search-reading-forms.md", "fences-headings-and-citations")
def test_a_citation_is_read_to_its_file_its_heading_path_and_its_keyed_part(fixtures, reading, check):
    # lines 39 and 40 of the text each hold one citation: one of another file's section with two keys, and one of
    # the same file keyed by a path of two names
    cites = reading.citations(fixtures["fences-headings-and-citations"])
    check("a keyed part with two keys gives a pair to each, and a key written as a path gives its names",
          [c.part for c in cites] == [((("Country",), "Canada"), (("Tax Year",), "2025")), ((("States", "State"), "open"),)], [c.part for c in cites])
    check("a citation gives its file, its heading path and its line, a citation of the same file naming none",
          [(c.file, c.lineage, c.line) for c in cites] == [("specs/a.md", ("A", "B"), 39), ("", ("Table",), 40)], [(c.file, c.lineage, c.line) for c in cites])
    check("a whole file's citation gives no heading path, and text that is no citation gives none",
          reading.parse_citation("specs/a.md").lineage == () and reading.parse_citation("a word") is None and reading.parse_citation("README.md") is None)


@pytest.mark.reads("search-reading-forms.md", "one-diagram-block", "diagram-lines-unfenced")
def test_the_reading_answers_for_any_text_and_needs_nothing_a_search_requires(fixtures, reading, check):
    # one fixture is a whole fenced block of one line, the other the lines of a diagram standing in no fence
    check("the reading answers for any text, one that is no file and holds one diagram among them",
          [b.content for b in reading.blocks(fixtures["one-diagram-block"])] == ["flowchart TD"] and reading.blocks(fixtures["diagram-lines-unfenced"]) == ())
    check("the reading needs nothing a search requires", not ({"search", "sqlite3", "spec_text"} & set(vars(reading))) and reading.__file__.endswith("reading.py"))
