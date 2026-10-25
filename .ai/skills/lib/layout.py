"""The check of where a blank line falls: each line of a Markdown file read as the element it opens or continues,
and each blank line held to the Decision Table specs/methodology/spec-style.md § Blank Lines states, read from the
canon. The element names the module holds are a copy of the table's Input Values, checked against them as the table
is read. The audit-specs script, the design-specs script and implement-specs' script, through check_form, run the
check through this one copy (specs/methodology/skills.md § Authoring a Skill). A fenced block whose info string is
`markdown` is read as spec-style.md § Markdown has it, one code block toward what stands outside it and a file of its
own within."""
import re
from pathlib import Path

import constructs
from spec_text import sections, strip_fences

# @canon-spec specs/methodology/spec-style.md § Blank Lines
RULE = "spec-style.md § Blank Lines"
HOME = "specs/methodology/spec-style.md"
SECTION = "Blank Lines"

# @canon-spec specs/methodology/spec-style.md § Blank Lines
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

# GFM's blocks as the canon meets them: a fence, a list marker, a thematic break, an ATX heading
FENCE = re.compile(r"^(`{3,}|~{3,})(.*)$")
LIST_MARKER = re.compile(r"^(?P<marker>[-*+]|\d{1,9}[.)])(?P<gap> {1,4}(?=\S)| *$)")
THEMATIC = re.compile(r"^(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$")
HEADING_LINE = re.compile(r"^#{1,6}(?:\s|$)")
MARKDOWN_INFO = "markdown"


class Line:
    """One line's reading: the element it opens or continues, whether it opens it, its indentation, the text
    indentation of the innermost list item holding it once it is read, and whether it is a code block's line."""
    __slots__ = ("kind", "opens", "indent", "holder", "fenced")

    def __init__(self, kind, opens, indent, holder, fenced=False):
        self.kind, self.opens, self.indent, self.holder, self.fenced = kind, opens, indent, holder, fenced


def _indent(line):
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip(" ")), expanded


def elements(text):
    """-> [Line or None] for each line of text, None for a blank line: the element each line opens or continues, read as
    GFM reads blocks and as spec-style.md § Markdown has a list item end before the first line that is not blank and is
    indented less than its text."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, stack, fence, front = [], [], None, None
    prev = None  # the last non-blank line's reading, where its element may continue onto the next line
    continuing_code = False
    for i, raw in enumerate(lines):
        indent, line = _indent(raw)
        content = line[indent:]
        stripped = content.strip()
        if i == 0 and stripped == "---":
            front = True
            out.append(Line(FRONT_MATTER, True, 0, None))
            prev = None
            continue
        if front:
            out.append(Line(FRONT_MATTER, False, 0, None))
            if stripped == "---":
                front = False
            continue
        if fence is not None:
            char, length, _ = fence
            closes = re.fullmatch(r"(%s{%d,})\s*" % (re.escape(char), length), content)
            out.append(Line(CODE_BLOCK, False, indent, stack[-1] if stack else None, fenced=True))
            if closes:
                fence = None
                prev = None
            continue
        if not stripped:
            out.append(None)
            prev = None
            continue
        holder_before = stack[-1] if stack else None
        # a line that is not blank and is indented less than an item's text ends the item (spec-style.md § Markdown)
        while stack and indent < stack[-1]:
            stack.pop()
        container = stack[-1] if stack else 0
        rel = indent - container
        if continuing_code and rel >= 4:
            out.append(Line(CODE_BLOCK, False, indent, stack[-1] if stack else None))
            continue
        continuing_code = False
        if rel >= 4 and (prev is None or prev.kind not in (PARAGRAPH, FIELD, LIST_ITEM, RECORD)):
            out.append(Line(CODE_BLOCK, True, indent, stack[-1] if stack else None))
            continuing_code = True
            prev = out[-1]
            continue
        m = FENCE.match(content)
        if m:
            fence = (m.group(1)[0], len(m.group(1)), m.group(2).strip())
            out.append(Line(CODE_BLOCK, True, indent, stack[-1] if stack else None, fenced=True))
            prev = None
            continue
        if HEADING_LINE.match(content):
            out.append(Line(HEADING, True, indent, stack[-1] if stack else None))
            prev = None
            continue
        if THEMATIC.match(content):
            out.append(Line(THEMATIC_BREAK, True, indent, stack[-1] if stack else None))
            prev = None
            continue
        if content.startswith("|"):
            opens = not (prev is not None and prev.kind == TABLE)
            out.append(Line(TABLE, opens, indent, stack[-1] if stack else None))
            prev = out[-1]
            continue
        lm = LIST_MARKER.match(content)
        if lm:
            width = len(lm.group("marker"))
            gap = len(lm.group("gap"))
            text_indent = indent + width + (1 if gap == 0 or gap > 4 else gap)
            stack.append(text_indent)
            f = constructs.FIELD.match(line)
            kind = RECORD if f and f["marker"] else LIST_ITEM
            out.append(Line(kind, True, indent, text_indent))
            prev = out[-1]
            continue
        f = constructs.FIELD.match(line)
        if f and not f["marker"]:
            out.append(Line(FIELD, True, indent, stack[-1] if stack else None))
            prev = out[-1]
            continue
        if prev is not None and prev.kind in (PARAGRAPH, FIELD, LIST_ITEM, RECORD) and holder_before == (stack[-1] if stack else None):
            out.append(Line(prev.kind, False, indent, stack[-1] if stack else None))
            prev = out[-1]
            continue
        out.append(Line(PARAGRAPH, True, indent, stack[-1] if stack else None))
        prev = out[-1]
    return out


def code_lines(text):
    """-> the 0-based indexes of the lines the reading gives an indented code block, which a check of the prose takes as
    literal, as it takes a fenced block's lines."""
    return {i for i, el in enumerate(elements(text)) if el is not None and el.kind == CODE_BLOCK and not el.fenced}


def markdown_blocks(text):
    """-> [(opening fence's 0-based line, closing fence's line, the Markdown the block holds)] for each fenced block
    whose info string is `markdown`, the block's lines dedented by the fence's indentation."""
    lines, out, fence = text.replace("\r\n", "\n").split("\n"), [], None
    for i, raw in enumerate(lines):
        indent, line = _indent(raw)
        content = line[indent:]
        if fence is not None:
            start, char, length, dedent, held = fence
            if re.fullmatch(r"(%s{%d,})\s*" % (re.escape(char), length), content):
                if held is not None:
                    out.append((start, i, "\n".join(l[dedent:] if l[:dedent].strip() == "" else l.lstrip(" ") for l in held)))
                fence = None
            elif held is not None:
                held.append(line)
            continue
        m = FENCE.match(content)
        if m:
            info = m.group(2).strip().split(" ")[0] if m.group(2).strip() else ""
            fence = (i, m.group(1)[0], len(m.group(1)), indent, [] if info == MARKDOWN_INFO else None)
    return out


_RULES = {}


def rules(root):
    """-> (the rows of the Decision Table § Blank Lines states, each {column: cell}, its conditions and its outcome
    column, or None, and the problems with reading it), read from the canon under root once."""
    root = Path(root).resolve()
    if root in _RULES:
        return _RULES[root]
    home = root / HOME
    problems = []
    table = None
    if home.is_file():
        import citation_links
        body = citation_links.strip(home.read_text(encoding="utf-8")).replace("\r\n", "\n")
        secs = sections(body)
        for line, name, fields, tables, lineage in constructs.declarations(strip_fences(body), secs):
            if lineage != SECTION or name != "Decision Table" or not tables:
                continue
            values = dict((k, v) for _, k, v in fields)
            conditions = [c.strip() for c in values.get("Conditions", "").split(",") if c.strip()]
            header = tables[0]["header"]
            outcome = next((c for c in header if c not in conditions), None)
            if conditions and outcome and all(c in header for c in conditions):
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
    if table is None:
        problems.append((RULE, HOME, 0, "the layout check reads no Decision Table of where a blank line falls in spec-style.md § Blank Lines"))
    _RULES[root] = (table, problems)
    return _RULES[root]


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


def decide(table, above, below, ends):
    """-> whether a blank line stands between the element above and the element below, by the table's first matching
    row, or None where no row matches."""
    rows, conditions, outcome = table
    given = dict(zip(conditions, (above, below, ends)))
    for row in rows:
        if all(_matches(row[c], given[c]) for c in conditions):
            return row[outcome].strip() == "true"
    return None


def findings(text, table, offset=0):
    """-> [(rule, 1-based line, message)]: each blank line missing where the table gives true, and each standing where
    it gives false, between one element and the next; a fenced `markdown` block's Markdown read as a file of its own."""
    out = []
    if table is None:
        return out
    els = elements(text)
    prev, blank = None, None
    for i, el in enumerate(els):
        if el is None:
            if prev is not None and blank is None:
                blank = i
            continue
        if el.opens and prev is not None:
            above = els[prev]
            ends = above.holder is not None and el.indent < above.holder
            want = decide(table, above.kind, el.kind, ends)
            if want is True and blank is None:
                out.append((RULE, i + 1 + offset, f"a blank line missing between {above.kind} and {el.kind}"))
            elif want is False and blank is not None:
                out.append((RULE, blank + 1 + offset, f"a blank line between {above.kind} and {el.kind}, where none falls"))
        prev, blank = i, None
    for start, _, inner in markdown_blocks(text):
        out += findings(inner, table, offset + start + 1)
    return out
