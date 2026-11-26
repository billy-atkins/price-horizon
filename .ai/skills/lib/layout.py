"""The check of where a blank line falls: each line of a Markdown file read as the element it opens or continues,
and each blank line held to the canon's table of blank lines, read from the canon. The element names the module holds
are a copy of the table's Input Values, and the conditions it works out a copy of the table's Conditions, each checked
against the table as it is read. The audit-specs script, the design-specs script and implement-specs' script, through
check_form, run the check through this one copy. A fenced block whose info string is `markdown` is read as the canon's
Markdown style has it, one code block toward what stands outside it and a file of its own within."""
import constructs
import reading
from spec_text import checkout, sections, strip_fences

# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
RULE = "spec-style/markdown.md § Blank Lines"
HOME = "specs/methodology/spec-style/markdown.md"
SECTION = "Blank Lines"

# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
# the elements a line opens or continues, a copy of the Input Values the table gives, compared with them in rules()
FRONT_MATTER = "front matter"
HEADING = "a heading"
PARAGRAPH = "a paragraph"
FIELD = "a field"
RECORD = "a record"
LIST_ITEM = "a list item"
TABLE = "a table"
CODE_BLOCK = "a code block"
THEMATIC_BREAK = "a thematic break"
ELEMENTS = (FRONT_MATTER, HEADING, PARAGRAPH, FIELD, RECORD, LIST_ITEM, TABLE, CODE_BLOCK, THEMATIC_BREAK)

# where a line stands, a fence, a list marker and a heading among it, is the one reading's; the names
# kept here are its own, for the scripts that read them from this module
FENCE = reading.FENCE
MARKDOWN_INFO = "markdown"


class Line:
    """One line's reading: the element it opens or continues, whether it opens it, its indentation, the text
    indentation of the innermost list item holding it once it is read, and whether it is a code block's line."""
    __slots__ = ("kind", "opens", "indent", "holder", "fenced")

    def __init__(self, kind, opens, indent, holder, fenced=False):
        self.kind, self.opens, self.indent, self.holder, self.fenced = kind, opens, indent, holder, fenced


def _indent(line):
    return reading.expand(line)


def elements(text):
    """-> [Line or None] for each line of text, None for a blank line: the element each line opens or continues. Where
    a line stands, in a fenced or an indented code block, a heading, a table, a list item or the front matter, is the
    one reading's, read as GFM reads blocks and as the canon's Markdown style has a list item end before the first line that is not blank and is indented less than its text. What this check tells apart for
    itself is a field, a record and a paragraph within running text."""
    kinds = {reading.FRONT_MATTER: FRONT_MATTER, reading.HEADING: HEADING, reading.TABLE: TABLE, reading.FENCED: CODE_BLOCK,
             reading.INDENTED: CODE_BLOCK, reading.THEMATIC_BREAK: THEMATIC_BREAK}
    out, prev = [], None  # prev: the line above's reading, where running text may continue it
    for ln in reading.lines(text.replace("\r\n", "\n")):
        if ln.kind == reading.BLANK:
            out.append(None)
            prev = None
            continue
        if ln.kind in kinds:
            out.append(Line(kinds[ln.kind], ln.opens, ln.indent, ln.holder, fenced=ln.fenced))
            prev = None
            continue
        f = constructs.FIELD.match(ln.text.expandtabs(4))
        if ln.kind == reading.LIST_ITEM:
            out.append(Line(RECORD if f and f["marker"] else LIST_ITEM, True, ln.indent, ln.holder))
        elif f and not f["marker"]:
            out.append(Line(FIELD, True, ln.indent, ln.holder))
        elif ln.continues and prev is not None:
            out.append(Line(prev.kind, False, ln.indent, ln.holder))
        else:
            out.append(Line(PARAGRAPH, True, ln.indent, ln.holder))
        prev = out[-1]
    return out


def code_lines(text):
    """-> the 0-based indexes of the lines the reading gives an indented code block, which a check of the prose takes as
    literal, as it takes a fenced block's lines."""
    return {i for i, el in enumerate(elements(text)) if el is not None and el.kind == CODE_BLOCK and not el.fenced}


def markdown_blocks(text):
    """-> [(opening fence's 0-based line, closing fence's line, the Markdown the block holds)] for each fenced block
    whose info string is `markdown`, the block's lines dedented by the fence's indentation, as the one reading gives a
    block."""
    return [(b.opens - 1, b.closes - 1, b.content) for b in reading.blocks(text.replace("\r\n", "\n"))
            if b.closed and b.word == MARKDOWN_INFO]


_RULES = {}


def rules(text=None):
    """-> (the rows of the canon's Decision Table of blank lines, each {column: cell}, its conditions and its outcome
    column, or None, and the problems with reading it), read from the canon of the checkout once, whatever root a
    check is given; or, given the text of the table's file as a scope holds it, read from that text, citations' links
    stripped, so the module's copy of the table's names is held against the file a check is handed."""
    root = checkout()
    if text is None and root in _RULES:
        return _RULES[root]
    home = root / HOME
    problems = []
    table, unknown = None, []
    if text is not None or home.is_file():
        import citation_links
        body = (text if text is not None else citation_links.strip(home.read_text(encoding="utf-8"))).replace("\r\n", "\n")
        secs = sections(body)
        for line, name, fields, tables, lineage in constructs.declarations(strip_fences(body), secs):
            if lineage != SECTION or name != "Decision Table" or not tables:
                continue
            values = dict((k, v) for _, k, v in fields)
            conditions = [c.strip() for c in values.get("Conditions", "").split(",") if c.strip()]
            header = tables[0]["header"]
            outcome = next((c for c in header if c not in conditions), None)
            # a condition the table names that findings() does not work out leaves the table unread, reported here
            unknown = [c for c in conditions if c not in CONDITIONS]
            for name in unknown:
                problems.append((RULE, HOME, 0, f"a condition the table names that the module does not work out: {name}"))
            if conditions and outcome and all(c in header for c in conditions) and not unknown:
                rows = [dict(zip(header, cells)) for _, cells in tables[0]["rows"] if len(cells) == len(header)]
                table = (rows, conditions, outcome)
            # the element names this module holds, compared with the Input Values the table gives, so a renamed
            # element fails where the names stand
            given = set()
            for item in values.get("Input Values", "").split("\n"):
                quoted = constructs.quoted_values(item.split(":", 1)[1].strip()) if ":" in item else None
                given.update(quoted or ())
            for name in sorted(set(ELEMENTS) - given):
                problems.append((RULE, HOME, 0, f"an element name the module holds that the table's Input Values do not give: {name}"))
            for name in sorted(given - set(ELEMENTS)):
                problems.append((RULE, HOME, 0, f"an element the table's Input Values give that the module lacks: {name}"))
            break
    if table is None and not unknown:
        problems.append((RULE, HOME, 0, "the layout check reads no Decision Table of where a blank line falls in spec-style/markdown.md § Blank Lines"))
    if text is not None:
        return table, problems
    _RULES[root] = (table, problems)
    return _RULES[root]


# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
# the table's conditions, a copy of the names it gives, each one findings() works out, compared with them in rules()
ABOVE = "The element above"
BELOW = "The element below"
ENDS = "Ends a list item?"
NESTED = "Nested beneath the field above?"
CONDITIONS = (ABOVE, BELOW, ENDS, NESTED)


def _matches(cell, value):
    cell = cell.strip()
    if cell == "-":
        return True
    quoted = constructs.quoted_values(cell)
    if quoted is not None:
        return value in quoted
    if cell in ("true", "false"):
        return value is (cell == "true")
    return value == cell


def decide(table, given):
    """-> whether a blank line stands between the element above and the element below, by the table's first row
    matching `given`, {condition's name: its value}, or None where no row matches."""
    rows, conditions, outcome = table
    for row in rows:
        if all(_matches(row[c], given[c]) for c in conditions):
            return row[outcome].strip() == "true"
    return None


def _key_indent(el):
    """The indentation of the key a field's or a record's line opens: a record's key stands at its item's text."""
    return el.holder if el.kind == RECORD else el.indent


def findings(text, table, offset=0):
    """-> [(rule, 1-based line, message)]: each blank line missing where the table gives true, and each standing where
    it gives false, between one element and the next; a fenced `markdown` block's Markdown read as a file of its own."""
    out = []
    if table is None:
        return out
    els = elements(text)
    prev, blank, opened = None, None, None  # opened: the line opening the element above, a field's key line among them
    for i, el in enumerate(els):
        if el is None:
            if prev is not None and blank is None:
                blank = i
            continue
        if el.opens and prev is not None:
            above = els[prev]
            nested = (el.kind == FIELD and above.kind in (FIELD, RECORD) and opened is not None
                      and el.indent == _key_indent(els[opened]) + 2)
            want = decide(table, {ABOVE: above.kind, BELOW: el.kind,
                                  ENDS: above.holder is not None and el.indent < above.holder, NESTED: nested})
            if want is True and blank is None:
                out.append((RULE, i + 1 + offset, f"a blank line missing between {above.kind} and {el.kind}"))
            elif want is False and blank is not None:
                out.append((RULE, blank + 1 + offset, f"a blank line between {above.kind} and {el.kind}, where none falls"))
        if el.opens:
            opened = i
        prev, blank = i, None
    for start, _, inner in markdown_blocks(text):
        out += findings(inner, table, offset + start + 1)
    return out
