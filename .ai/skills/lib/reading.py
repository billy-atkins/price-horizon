"""The one reading of where a line of a text stands: under which headings, and in running text, a heading, a table, a
fenced block, an indented code block or the front matter; each fenced block as a unit; and the form a citation takes.
The scripts the skills share take a file's headings, its fenced blocks and a citation's form from here, the search
among them, one copy, and it imports none of them.
A check that reads the rows of a table still finds those rows for itself.

Standard library only, so any script imports it without what a search requires. It reads any text given it: a file a
target holds, a diagram quoted in a note, standard input. It reads a text as the canon has a Markdown
file read, GFM's blocks as GFM reads them, and a citation as the canon writes one. Of two headings sharing
a path, which the canon forbids and gives no reading of, a path names the first, and the second is marked.

Reading a file to judge it stays each check's own. What stands here is only where a line stands and what a citation
is."""
import functools
import re

# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
TEXT = "text"
HEADING = "a heading"
TABLE = "a table"
FENCED = "a fenced block"
INDENTED = "an indented code block"
FRONT_MATTER = "front matter"
STANDS_IN = (TEXT, HEADING, TABLE, FENCED, INDENTED, FRONT_MATTER)
# what the scan tells apart within running text, for a check that judges a file's layout
BLANK = "blank"
LIST_ITEM = "a list item"
THEMATIC_BREAK = "a thematic break"

# GFM's blocks as the canon meets them, each read on a line past its indentation: a fence, a list marker, a thematic
# break, an ATX heading
FENCE = re.compile(r"^(`{3,}|~{3,})(.*)$")
LIST_MARKER = re.compile(r"^(?P<marker>[-*+]|\d{1,9}[.)])(?P<gap> {1,4}(?=\S)| *$)")
THEMATIC = re.compile(r"^(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$")
HEADING_LINE = re.compile(r"^#{1,6}(?:\s|$)")
# an ATX heading that names a section: at the file's own level, its closing run of hashes no part of its title
SECTION_HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
QUOTE = re.compile(r"^(?: {0,3}>[ ]?)+")

# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
PATH = r"[\w.][\w./-]*"
CITED = re.compile(r"^(?:(" + PATH + r") )?§ (.+)$")
WHOLE = re.compile(r"^" + PATH + r"$")
BARE = re.compile(r"(?<![\w./-])(" + PATH + r"\.[A-Za-z]+) § ")
KEYED = re.compile(r"^(.*?) \[(.*)\]$")
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
COMMENT = r"^\s*(?://(?![/!])|#+|--|;+|%+|<!--|/\*(?![*!]))\s*"
COMMENT_END = r"\s*(?:-->|\*/)?\s*$"
ANNOTATION = re.compile(COMMENT + r"@(app|canon)-spec (\S.*?)" + COMMENT_END)


def squeeze(text):
    """-> text with each run of white space made one space and its ends trimmed, as a form normalizes a field's input."""
    return " ".join(text.split())


class Line:
    """One line of the text: its 1-based number, its text as written, where it stands, the fenced block it stands in,
    by that block's place among `blocks`, and the heading path it stands under. For a check judging a file's layout
    it also holds what the scan told apart within running text: `kind`, `opens`, whether the line opens its element,
    its indentation, `holder`, the text indentation of the innermost list item holding it, and `continues`, whether a
    line of running text continues the line above it."""
    __slots__ = ("number", "text", "stands_in", "block", "lineage", "kind", "opens", "indent", "holder", "continues")

    def __init__(self, number, text, kind, opens, indent, holder, block=None, continues=False):
        self.number, self.text, self.kind, self.opens, self.indent, self.holder = number, text, kind, opens, indent, holder
        self.block, self.continues, self.lineage = block, continues, ()
        self.stands_in = kind if kind in STANDS_IN else TEXT

    @property
    def fenced(self):
        return self.kind == FENCED


class Heading:
    """A heading naming a section: its 1-based line, its level, its title, its own path, the line its own text ends
    before, the line its sections beneath it end before, and whether it is the second or a later heading sharing its
    path. A level-1 heading is the file's title, and its path is empty."""
    __slots__ = ("line", "level", "title", "lineage", "ends", "subtree_ends", "repeated")

    def __init__(self, line, level, title, lineage, ends, subtree_ends, repeated):
        self.line, self.level, self.title, self.lineage = line, level, title, lineage
        self.ends, self.subtree_ends, self.repeated = ends, subtree_ends, repeated


class Block:
    """A fenced block as a unit, for a script that reads one as a file of its own: the 1-based lines of its opening
    and its closing fence, the last line where none closes it, its info string, what stands before its fence on the
    line, its indentation and any quote prefix, and its lines between the fences with that taken off each."""
    __slots__ = ("opens", "closes", "info", "before", "held", "closed", "char", "length", "dedent", "quoted")

    def __init__(self, opens, info, before, char, length, dedent, quoted):
        self.opens, self.closes, self.info, self.before = opens, opens, info, before
        self.held, self.closed, self.char, self.length, self.dedent, self.quoted = [], False, char, length, dedent, quoted

    @property
    def word(self):
        """The info string's first word, as `markdown` or `mermaid`."""
        return (self.info.split() or [""])[0]

    @property
    def content(self):
        return "\n".join(self.held)


def expand(line):
    """-> (a line's indentation, the line with its tabs made spaces), a tab standing at each fourth column."""
    expanded = line.expandtabs(4)
    return len(expanded) - len(expanded.lstrip(" ")), expanded


def opens_fence(content):
    """-> the FENCE match where a line, past its indentation, opens a fenced block, else None: a run of three or more
    backticks or tildes, a backtick fence's info string holding no backtick, so a code span of three backticks opening
    a line is no fence."""
    m = FENCE.match(content)
    return m if m and not (m.group(1)[0] == "`" and "`" in m.group(2)) else None


def closes_fence(content, char, length):
    """-> whether a line, past its indentation, closes a fence: a run of the fence's own character at least as long,
    with nothing after it, so a fence nested in a longer one stays inside it."""
    return bool(re.fullmatch(r"(%s{%d,})\s*" % (re.escape(char), length), content))


def starts(line):
    """-> what a line read alone opens, TABLE, HEADING or FENCED, else None: for a reader of a block that stops at the
    first line opening one."""
    content = line.expandtabs(4).lstrip(" ")
    if content.startswith("|"):
        return TABLE
    if HEADING_LINE.match(content):
        return HEADING
    return FENCED if opens_fence(content) else None


def dedented(line, dedent):
    """-> a line of a block with the block's indentation taken off it, a line indented less brought to the margin."""
    return line[dedent:] if line[:dedent].strip() == "" else line.lstrip(" ")


@functools.lru_cache(maxsize=256)
def _read(text):
    """-> (lines, blocks, headings) of a text, read once and kept."""
    raws = text.split("\n")
    out, blocks, stack, fence, front = [], [], [], None, False
    prev = None  # the last line's reading, where its element may continue onto the next line; None after a blank line
    continuing_code = False
    for i, original in enumerate(raws):
        raw = original[:-1] if original.endswith("\r") else original
        indent, line = expand(raw)
        content = line[indent:]
        stripped = content.strip()
        holder = stack[-1] if stack else None
        if i == 0 and stripped == "---":
            front = True
            out.append(Line(1, original, FRONT_MATTER, True, 0, None))
            prev = None
            continue
        if front:
            out.append(Line(i + 1, original, FRONT_MATTER, False, 0, None))
            if stripped in ("---", "..."):
                front = False
            continue
        if fence is not None:
            block = blocks[fence]
            quote = QUOTE.match(raw) if block.quoted else None
            if block.quoted and not quote:
                fence = None  # a line outside the quote ends the quote, and the block quoted in it
            else:
                inner = expand(raw[quote.end():])[1] if quote else line
                inner_indent = len(inner) - len(inner.lstrip(" "))
                out.append(Line(i + 1, original, FENCED, False, indent, holder, block=fence))
                block.closes = i + 1
                if closes_fence(inner[inner_indent:], block.char, block.length):
                    block.closed = True
                    fence = None
                    prev = None
                else:
                    block.held.append(dedented(inner, block.dedent))
                continue
        if not stripped:
            out.append(Line(i + 1, original, BLANK, False, indent, holder))
            prev = None
            continue
        holder_before = holder
        # a line that is not blank and is indented less than an item's text ends the item, as the canon's Markdown has it
        while stack and indent < stack[-1]:
            stack.pop()
        holder = stack[-1] if stack else None
        rel = indent - (holder or 0)
        textual = prev is not None and prev.kind in (TEXT, LIST_ITEM)
        if continuing_code and rel >= 4:
            out.append(Line(i + 1, original, INDENTED, False, indent, holder))
            continue
        continuing_code = False
        if rel >= 4 and not textual:
            out.append(Line(i + 1, original, INDENTED, True, indent, holder))
            continuing_code = True
            prev = out[-1]
            continue
        quote = QUOTE.match(raw)
        quoted = expand(raw[quote.end():])[1] if quote else None
        m = opens_fence(quoted.lstrip(" ")) if quote else opens_fence(content)
        if m:
            dedent = len(quoted) - len(quoted.lstrip(" ")) if quote else indent
            before = (quote.group(0) if quote else "") + " " * dedent
            blocks.append(Block(i + 1, m.group(2).strip(), before, m.group(1)[0], len(m.group(1)), dedent, bool(quote)))
            fence = len(blocks) - 1
            out.append(Line(i + 1, original, FENCED, True, indent, holder, block=fence))
            prev = None
            continue
        if HEADING_LINE.match(content):
            out.append(Line(i + 1, original, HEADING, True, indent, holder))
            prev = None
            continue
        if THEMATIC.match(content):
            out.append(Line(i + 1, original, THEMATIC_BREAK, True, indent, holder))
            prev = None
            continue
        if content.startswith("|"):
            out.append(Line(i + 1, original, TABLE, not (prev is not None and prev.kind == TABLE), indent, holder))
            prev = out[-1]
            continue
        lm = LIST_MARKER.match(content)
        if lm:
            gap = len(lm.group("gap"))
            text_indent = indent + len(lm.group("marker")) + (1 if gap == 0 or gap > 4 else gap)
            stack.append(text_indent)
            out.append(Line(i + 1, original, LIST_ITEM, True, indent, text_indent))
            prev = out[-1]
            continue
        out.append(Line(i + 1, original, TEXT, True, indent, holder, continues=textual and holder_before == holder))
        prev = out[-1]
    # the headings naming sections: each at the file's own level, in no list item, and the path each line stands under
    heads = []
    for ln in out:
        m = SECTION_HEADING.match(ln.text.rstrip("\r")) if ln.kind == HEADING and ln.holder is None else None
        if m:
            heads.append((ln.number, len(m.group(1)), m.group(2)))
    total = len(out) + 1
    headings, stack, seen = [], [], {}
    for n, (number, level, title) in enumerate(heads):
        ends = heads[n + 1][0] if n + 1 < len(heads) else total
        subtree_ends = next((h[0] for h in heads[n + 1:] if h[1] <= level), total)
        if level == 1:
            headings.append(Heading(number, 1, title, (), ends, subtree_ends, False))
            continue
        stack = stack[:level - 2]
        while len(stack) < level - 2:
            stack.append(None)
        stack.append(title)
        lineage = tuple(t for t in stack if t)
        seen[lineage] = seen.get(lineage, 0) + 1
        headings.append(Heading(number, level, title, lineage, ends, subtree_ends, seen[lineage] > 1))
    at, current = 0, ()
    for ln in out:
        while at < len(headings) and headings[at].line <= ln.number:
            current = headings[at].lineage if headings[at].level > 1 else current
            at += 1
        ln.lineage = current
    return tuple(out), tuple(blocks), tuple(headings)


def lines(text):
    """-> [Line], one to each line of the text, in order."""
    return _read(text)[0]


def blocks(text):
    """-> [Block], each fenced block of the text, a block inside a longer fence being content of the longer and no
    Block."""
    return _read(text)[1]


def headings(text):
    """-> [Heading], each heading naming a section, in order, the file's title among them."""
    return _read(text)[2]


def sections(text):
    """-> {path: Heading} for each section below the title, a path two headings share naming the first."""
    out = {}
    for h in headings(text):
        if h.level > 1:
            out.setdefault(h.lineage, h)
    return out


def live(text, front_matter=False, blank=None):
    """-> the text with each line of a fenced block, its fences among them, blanked to its own length, so a place in it
    is the same place in the text as written; with front_matter, the front matter's lines too. `blank` gives what a
    blanked line becomes, a line of spaces as long unless given."""
    out = []
    for ln in lines(text):
        if ln.kind == FENCED or (front_matter and ln.kind == FRONT_MATTER):
            out.append(" " * len(ln.text) if blank is None else blank)
        else:
            out.append(ln.text)
    return "\n".join(out)


class Citation:
    """The one form of a citation, a spec annotation's among them: the file it names, '' for a place in the same file;
    the heading path, () for a whole file; the keyed part, () or a pair to each key it gives, (the key's path, as
    ('States', 'State'), its value); the text of its keyed part as written, or None; its line, 0 for one written alone;
    and where that line stands."""
    __slots__ = ("file", "lineage", "part", "selector", "line", "stands_in", "written")

    def __init__(self, file, lineage, selector, written, line=0, stands_in=TEXT):
        self.file, self.lineage, self.selector, self.written, self.line, self.stands_in = file, lineage, selector, written, line, stands_in
        self.part = keyed_part(selector)

    @property
    def path(self):
        """The heading path as a citation writes it, its headings joined by the section mark."""
        return " § ".join(self.lineage)

    @property
    def key(self):
        """The keyed part as a citation writes it, each key's item squeezed, or None."""
        return None if self.selector is None else "; ".join(squeeze(p) for p in self.selector.split(";"))


def keyed_part(selector):
    """-> a keyed part's pairs, (the key's path, its value) to each key the part gives: `Country: Canada; Tax Year:
    2025` gives two, and `States.State: open` one whose path holds two names."""
    if selector is None:
        return ()
    out = []
    for item in selector.split(";"):
        key, _, value = item.partition(":")
        if key.strip():
            out.append((tuple(squeeze(k) for k in key.split(".")), squeeze(value)))
    return tuple(out)


def parse_citation(written):
    """-> the Citation of one citation written alone, its white space squeezed, or None where the text is no citation.
    A whole-file citation names a path holding a folder and gives no heading path."""
    text = squeeze(written)
    m = CITED.match(text)
    if m:
        target, selector = m.group(2), None
        k = KEYED.match(target)
        if k:
            target, selector = k.group(1), k.group(2)
        return Citation(m.group(1) or "", tuple(squeeze(s) for s in target.split("§")), selector, text)
    if WHOLE.match(text) and "/" in text:
        return Citation(text.rstrip("/"), (), None, text)
    return None


def spans(text):
    """-> [(offset, the text a code span holds)] for each code span, read outside every fenced block and then within
    each block's own lines, so a fence's backticks never pair with a span's and a span never runs across a fence or a
    blank line. An offset is a place in the text as written."""
    read = lines(text)
    starts_at, at = [], 0
    for ln in read:
        starts_at.append(at)
        at += len(ln.text) + 1
    regions = [(live(text, front_matter=True), 0)]
    for b in blocks(text):
        run = []
        # a line written as a fence inside a longer one is no span's text, so a block's lines are read in the runs
        # such lines part
        for ln in list(read[b.opens:b.closes - (1 if b.closed else 0)]) + [None]:
            if ln is not None and not FENCE.match(ln.text.expandtabs(4).strip()):
                run.append(ln)
            elif run:
                regions.append(("\n".join(x.text for x in run), starts_at[run[0].number - 1]))
                run = []
    out = []
    for region, base in regions:
        for m in SPAN.finditer(region):
            if "\n\n" not in m.group(2):
                out.append((base + m.start(), m.group(2)))
    return sorted(out)


def line_at(text, offset):
    """-> the Line a place in the text stands in."""
    return lines(text)[text.count("\n", 0, offset)]


def citations(text):
    """-> [Citation], every citation the text holds in a code span, one broken across lines among them, each with its
    line and where that line stands, a citation in a fenced block marked by it."""
    out = []
    for offset, held in spans(text):
        c = parse_citation(held)
        if c:
            ln = line_at(text, offset)
            c.line, c.stands_in = ln.number, ln.stands_in
            out.append(c)
    return out
