"""audit-specs' construct checks: what modeling-constructs.md § Constructs lets a script decide.

A construct is found by its declaration, a **Construct:** field, and read from the block the
declaration opens: its fields, then its tables. Each check here decides structure from the files
alone; what a guard's fact means, what a state's work is, and whether the right construct was
chosen stay with the Construct choice and form reading audit (modeling-constructs.md § Purpose).
"""
import re
from datetime import datetime, timedelta, timezone

RULE = "modeling-constructs.md § Constructs"
DECLARING = "modeling-constructs.md § Constructs § Declaring a Construct"

# @canon-spec specs/methodology/modeling-constructs.md § Constructs
# modeling-constructs.md § Constructs § Declaring a Construct: the constructs a **Construct:** field may name; a Record Form is
# declared by its titles
NAMES = ("Lifecycle", "State Machine", "Decision Table", "Decision Tree", "DAG", "Algorithm", "Constraint")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct
# each table of the fields a construct declares, by the section defining it, copied here as this script reads it,
# in its order: each field's Required, Default Value and Values cells; field_table_findings holds each copy to its table
DECLARED = "Constructs § Declaring a Construct"
FIELD_TABLES = {
    DECLARED: (
        ("Construct", "yes", "", "`§ Constructs`"),
        ("Order", "where the construct leaves open the order it takes its inputs or gives its results in", "", "text"),
    ),
    "Constructs § Decision Table": (
        ("Hit Policy", "no", "Unique", "`§ Constructs § Decision Table`"),
        ("Conditions", "yes", "", "text"),
        ("Annotations", "no", "none", "text"),
        ("Input Values", "no", "none", "text"),
        ("Output Values", "where its hit policy is Priority or Output order", "", "text"),
        ("Default Output", "no", "none", "text"),
    ),
    "Constructs § Algorithm": (
        ("Inputs", "yes", "", "text"),
        ("Output", "yes", "", "text"),
    ),
}
# the fields every construct declares beyond its Construct field, and each field with the construct setting it
COMMON = tuple(f for f, _, _, _ in FIELD_TABLES[DECLARED] if f != "Construct")
FIELD_TABLE = tuple((f, "every construct but a Record Form", r, d) for f, r, d, _ in FIELD_TABLES[DECLARED]) \
    + tuple((f, title.split(" § ")[1], r, d) for title, rows in FIELD_TABLES.items() if title != DECLARED
            for f, r, d, _ in rows)
OWN_FIELDS = {c: COMMON + tuple(f for f, fc, _, _ in FIELD_TABLE if fc == c) for c in NAMES}
REQUIRED = {c: tuple(f for f, fc, req, _ in FIELD_TABLE if fc == c and req == "yes") for c in NAMES}
# each field with the section defining it, and with its Values cell
FIELD_RULE = {f: "modeling-constructs.md § " + title for title, rows in FIELD_TABLES.items() for f, _, _, _ in rows}
FIELD_VALUES = {f: v for rows in FIELD_TABLES.values() for f, _, _, v in rows}
DEFAULTS = {f: d for f, _, _, d in FIELD_TABLE if d}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# the fields whose value is a list, each item beneath the field's key; a Default Output is one where
# its table has several outcome columns
LIST_FIELDS = ("Input Values", "Output Values")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# DMN's hit policies; Unique is the default value, reported where it is written
POLICIES = ("Any", "Priority", "First", "Rule order", "Output order",
            "Collect", "Collect sum", "Collect count", "Collect min", "Collect max")

# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Lifecycle
# a States table's headers, a Lifecycle's and a State Machine's alike
STATES = ["state", "description", "initial", "terminal"]
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Tree
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Lifecycle
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# each construct's tables, by their headers; None where a Decision Table's columns are its own
FORMS = {
    "Lifecycle": [STATES, ["From", "To", "Trigger"]],
    "State Machine": [STATES, ["From", "To", "Trigger", "Guard"]],
    "Decision Tree": [["Step", "Question", "Answer", "Result"]],
    "DAG": [["task", "depends_on"]],
    "Algorithm": [["Step", "Action"]],
    "Constraint": [["Constraint", "Applies to", "Enforced by"]],
    "Decision Table": [None],
}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Lifecycle
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# the columns whose form gives `none`, or whose own check reports it; no form here gives `-`, a
# Decision Table's `-` being its cells' own and a Lifecycle's trigger reported by its own check
NONE_COLUMNS = {("State Machine", "Trigger"), ("State Machine", "Guard"), ("DAG", "depends_on"), ("Lifecycle", "Trigger")}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct
# the tables a Name column may open: a Transitions table, a Decision Table, a Constraint table
NAMEABLE = {"Lifecycle": {1}, "State Machine": {1}, "Decision Table": {0}, "Constraint": {0}}

# @canon-spec specs/methodology/modeling-constructs.md § Fields
# a field: a line opening with its key in bold, the colon inside the bold, then a space and its value or nothing;
# a list marker and indentation before the key are no part of it; the one copy, which audit-specs.py reads too
FIELD = re.compile(r'^(?P<indent>\s*)(?P<marker>-\s+)?\*\*(?P<key>[^*`]+?):\*\*(?: (?P<value>.*)|$)')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
# § Constructs § Record Form: an identifying value holds no Markdown, backtick, `§`, `;` or `]`; an
# underscore within a word, as in a state's name, is no markup
UNPLAIN = re.compile(r'[*`§;\[\]]|(?:^|\W)_|_(?:\W|$)')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Tree
# a jump as the form writes it, and the parser reading every jump: the phrase in any letters and the step number
# after it, a whole number or a branch's dotted one, ending at a space, a punctuation mark or the text's end
JUMP_WORDS = "Go to step"
JUMP = re.compile(r'(?i)\b' + re.escape(JUMP_WORDS) + r'\b(?:\s+(\d+(?:\.\d+)?)(?=$|[^\w.]|\.(?!\d)))?')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# the opening of a comparison, and the separator of its two branches, as the form writes them
COMPARISON_OPENING = "If "
SEPARATOR_OF_BRANCHES = "; otherwise, "
# the separator as it stands in any wording, and the words a comparison is written with, which a step that is no
# comparison may fold one by
SEPARATOR_MARK = SEPARATOR_OF_BRANCHES.strip(" ")
COMPARISON_WORDS = re.compile(r"(?i)\b(?:" + SEPARATOR_MARK.strip("; ,") + "|" + COMPARISON_OPENING.strip() + r")\b")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# an End that ends a step or a branch: the whole of it, or after a comma or a sentence's end, with punctuation or
# nothing after it, so a step opening with the verb, End the run, or a word, End-of-day, is no End; and an End
# ending a text, after its closing punctuation is trimmed
END_WORD = "End"
END = re.compile(r'(?:^|[,.] )' + END_WORD + r'(?=[.,;]|\s*$)')
END_AT_TAIL = re.compile(r'(?:^|[,.] )' + END_WORD + r'$')
SEPARATOR = re.compile(r',| and ')


def _a(name):
    return ("an " if name[0] in "AEIOU" else "a ") + name


def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


# @canon-spec specs/methodology/modeling-constructs.md § Literal Text
# literal text: a code span, one backtick to the next, literal text holding no backtick; the one reading of a
# span, which audit-specs.py reads too
CODE_SPAN = re.compile(r'`(?P<text>[^`]+)`')


def _margin_field(line):
    """A field at the left margin, as a construct's own fields stand, opening a paragraph of their own
    (modeling-constructs.md § Constructs § Declaring a Construct); a field in a list item or indented is none."""
    m = FIELD.match(line)
    return m if m and not m["indent"] and not m["marker"] else None


def _form_of(text):
    """A text with the contents of each code span, as CODE_SPAN reads one, blanked to spaces, its backticks kept,
    so a form check never reads a jump, a separator or an End quoted as literal text as the text's own, and a span
    still stands between the words around it; places in the text are kept."""
    return CODE_SPAN.sub(lambda m: "`" + " " * len(m["text"]) + "`", text)


def jumps(text):
    """Each jump in a text: (its phrase as written, its step number or None, where it starts, where it ends)."""
    return [(m.group(0), m.group(1), m.start(), m.end()) for m in JUMP.finditer(text)]


def _jump_form(rule, r, ln, text, raw, found):
    """A jump whose letters are not those of `Go to step`, or that names no step by its number, as `Go to step nine`;
    a jump naming no step has no place to end at, and is reported for its form alone. `text` is the form read, `raw`
    the cell as written, of the same length, from which a finding quotes."""
    for phrase, target, start, end in jumps(text):
        if not phrase.startswith(JUMP_WORDS):
            found.append((rule, r, ln, f"a jump not written `{JUMP_WORDS}`: {raw[start:end]}"))
        if target is None:
            shown = " ".join(raw[start:].split()[:4]).rstrip(".,;:)!?")
            found.append((rule, r, ln, f"a jump naming no step by its number: {shown}"))


def _ends_in_jump(text):
    """Whether a text's last words are its one jump naming a step, its closing punctuation aside."""
    tail = text.rstrip(" .,;:)!?")
    named = [j for j in jumps(tail) if j[1]]
    return len(named) == 1 and named[0][3] == len(tail)


def _rule_row(row):
    return set(row.replace("|", "").strip()) <= set("-: ")


def feel(text):
    """A cell in FEEL's simple unary tests -> (negated, tests), each test ("any",), ("is", value, kind) or
    ("iv", low, low included, high, high included, kind); None for a cell opening as a form does but
    written in none the section lists (modeling-constructs.md § Constructs § Decision Table). A
    cell written plain is one value, commas and all."""
    v = text.strip()
    if v == "-":
        return (False, [("any",)])
    m = re.fullmatch(r'not\((.*)\)', v)
    neg, body = (True, m.group(1).strip()) if m else (False, v)
    tests = _tests(body)
    return None if tests is None else (neg, tests)


NUMBER = re.compile(r'-?(?:\d+(?:\.\d+)?|\.\d+)')
DATE = re.compile(r'date\("(\d{4})-(\d{2})-(\d{2})"\)')
DATE_TIME = re.compile(r'date and time\("(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})"\)')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# a list of values: each in double quotes, separated by commas; the one copy, which a quoted list and a list or a
# range are built from
QUOTED = r'"[^"]*"(?:\s*,\s*"[^"]*")*'
QUOTED_LIST = re.compile(r'\s*' + QUOTED + r'\s*')


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
def quoted_values(cell):
    """The values a Values cell lists, where it is a quoted list, or None."""
    return re.findall(r'"([^"]*)"', cell) if QUOTED_LIST.fullmatch(cell) else None


def _value(s):
    """A number, a FEEL date, or a FEEL date and time to the second with its offset -> (its place on
    one timeline, its kind); None for anything else, a date or a time that does not exist among it."""
    s = s.strip()
    try:
        m = DATE.fullmatch(s)
        if m:
            return datetime(*map(int, m.groups()), tzinfo=timezone.utc).timestamp(), "date"
        m = DATE_TIME.fullmatch(s)
        if m:
            *parts, frac, off = m.groups()
            tz = timezone.utc if off == "Z" else timezone(
                (1 if off[0] == "+" else -1) * timedelta(hours=int(off[1:3]), minutes=int(off[4:6])))
            return datetime(*map(int, parts), tzinfo=tz).timestamp() + float(frac or 0), "date and time"
    except ValueError:
        return None
    return (float(s), "number") if NUMBER.fullmatch(s) else None


def _num(s):
    v = _value(s)
    return None if v is None else v[0]


def _tests(body):
    """Each test ("is", value, kind) or ("iv", low, low included, high, high included, kind); a
    quoted value is a word however it reads."""
    if QUOTED_LIST.fullmatch(body):
        return [("is", q, "word") for q in re.findall(r'"([^"]*)"', body)]
    v = _value(body)
    if v:
        return [("is", v[0], v[1])]  # a number, a date or a date and time alone
    m = re.fullmatch(r'([\[\(])\s*(.+?)\s*\.\.\s*(.+?)\s*([\]\)])', body)
    if m:
        lo, hi = _value(m.group(2)), _value(m.group(3))
        if lo and hi and lo[1] == hi[1]:
            return [("iv", lo[0], m.group(1) == "[", hi[0], m.group(4) == "]", lo[1])]
    m = re.fullmatch(r'(<=|>=|<|>)\s*(.+)', body)
    if m and _value(m.group(2)):
        x, kind = _value(m.group(2))
        inf = float("inf")
        return [{"<": ("iv", -inf, False, x, False, kind), "<=": ("iv", -inf, False, x, True, kind),
                 ">": ("iv", x, False, inf, False, kind), ">=": ("iv", x, True, inf, False, kind)}[m.group(1)]]
    if FORM_OPENING.match(body):
        return None  # it opens as a form does, and is written in none the section lists
    return [("is", body, "word")]


def matches(cell, x):
    neg, tests = cell
    hit = False
    for test in tests:
        if test[0] == "any":
            hit = True
        elif test[0] == "is":
            hit = hit or x == test[1]  # a word never equals a number
        elif isinstance(x, float):
            lo, lo_in, hi, hi_in = test[1:5]
            hit = hit or ((x > lo or lo_in and x == lo) and (x < hi or hi_in and x == hi))
    return hit != neg


def _points(*cells):
    """Every boundary the cells name, a point between and beyond each, and, where they test words,
    a word none names: enough that two cells agree on these points only where they agree everywhere.
    A date is a whole day, so the point beside a date's boundary is the day before or after it."""
    words, nums, kinds = set(), set(), set()
    for neg, tests in cells:
        for test in tests:
            if test[0] == "is" and isinstance(test[1], str):
                words.add(test[1])
            elif test[0] == "is":
                nums.add(test[1])
                kinds.add(test[2])
            elif test[0] == "iv":
                nums |= {x for x in (test[1], test[3]) if abs(x) != float("inf")}
                kinds.add(test[5])
    if kinds == {"date"}:
        return sorted(set(nums) | {n + d for n in nums for d in (-86400.0, 86400.0)})
    if kinds:
        ns = sorted(nums) or [0.0]
        return sorted(set(ns) | {ns[0] - 1, ns[-1] + 1} | {(a + b) / 2 for a, b in zip(ns, ns[1:])})
    return sorted(words) + ["\x00a value no cell names"]


def overlap(a, b):
    """Whether one case can match both cells."""
    return any(matches(a, x) and matches(b, x) for x in _points(a, b))


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
FORM_OPENING = re.compile(r'not\(|[<>=!\[\]\("]|-$|(?:date and time|date|time|duration)\(')


def outside(cell, dom):
    """Whether a cell names a value its column's Input Values do not hold, or matches none they hold."""
    if any(not matches(dom, t[1]) for t in cell[1] if t[0] == "is"):
        return True
    return not any(matches(cell, x) and matches(dom, x) for x in _points(cell, dom))


def _kind(cell):
    """The kinds of value a cell tests: words, numbers, dates or dates and times; none for `-`."""
    return {t[-1] for t in cell[1] if t[0] != "any"}


def _escape(pools, rows):
    """A case, one value from each condition's pool, that no row matches, or None. Each pool's
    values are grouped by the rows still matching, so each group is searched once."""
    if not all(pools):
        return None
    seen = set()

    def walk(k, alive, case):
        if not alive:
            return tuple(case) + tuple(p[0] for p in pools[k:])
        if k == len(pools) or (k, alive) in seen:
            return None
        seen.add((k, alive))
        for x in pools[k]:
            hit = walk(k + 1, frozenset(i for i in alive if matches(rows[i][k], x)), case + [x])
            if hit is not None:
                return hit
        return None

    return walk(0, frozenset(range(len(rows))), [])


def _split_guard(text):
    """A guard's tests, split at each ` and ` outside quotes, a FEEL date and time's own aside."""
    return re.split(r' and (?!time\()(?=(?:[^"]*"[^"]*")*[^"]*$)', text)


# an outcome cell written as a condition's test would be: any value, a negation, a comparison, a range
TEST_FORM = re.compile(r'-$|not\(|(?:<=|>=|<|>)\s*\S|[\[\(][^\]\)]*\.\.')


def _ranked(value):
    """An Output Values field -> {header: [values, highest priority first]}, or None where an item
    is not a header, a colon and a quoted list."""
    out = {}
    for item in value.split("\n"):
        h, _, v = item.partition(":")
        if not QUOTED_LIST.fullmatch(v):
            return None
        out[h.strip()] = re.findall(r'"([^"]*)"', v)
    return out


def declarations(body, sections):
    """-> [(line, construct, fields, tables, lineage)] for each **Construct:** field in live text,
    and the findings of the declaration's own form."""
    lines = body.split("\n")
    secs = sorted(sections.items(), key=lambda x: x[1][0])
    out, problems = [], []
    for i, line in enumerate(lines):
        m = _margin_field(line)
        if not m or m["key"] != "Construct":
            continue
        name = (m["value"] or "").strip()
        owner = [lin for lin, (h, end) in secs if h < i < end]
        lineage = owner[-1] if owner else ""
        fields, tables, table, j = [], [], None, i + 1
        while j < len(lines):
            l = lines[j]
            f = _margin_field(l)
            if l.startswith("|"):
                if table is None:
                    table = {"header": _cells(l), "rows": [], "line": j + 1}
                    tables.append(table)
                elif not _rule_row(l):
                    table["rows"].append((j + 1, _cells(l)))
            elif not l.strip():
                table = None
                # the block ends with the last table its form gives; a table beside it is no part of it
                if name in FORMS and len(tables) == len(FORMS[name]):
                    break
            elif f and not tables:
                fields.append((j + 1, f["key"], (f["value"] or "").strip()))
            elif l.startswith("- ") and fields and not tables:
                # a field whose value is a list: its items sit beneath its key
                ln, k, v = fields[-1]
                fields[-1] = (ln, k, (v + "\n" if v else "") + l[2:].strip())
            else:
                break
            j += 1
        out.append((i + 1, name, fields, tables, lineage))
    return out


def construct_findings(r, body, found, sections):
    """modeling-constructs.md § Constructs: each declared construct checked for what its form
    lets a script decide. `body` is the file's live text, its fences stripped."""
    decls = declarations(body, sections)
    lines = body.split(chr(10))
    for line, name, fields, tables, lineage in decls:
        _paragraphs(r, lines, line, fields, found)
    # a field a construct sets, outside the block a Construct field opens
    owned = {ln for _, _, fields, _, _ in decls for ln, _, _ in fields}
    own_keys = {k for keys in OWN_FIELDS.values() for k in keys}
    for i, l in enumerate(body.split(chr(10)), 1):
        f = _margin_field(l)
        if f and f["key"] in own_keys and i not in owned:
            found.append((DECLARING, r, i, f"a {f['key']} field outside a construct's block"))
    seen = {}
    for line, name, fields, tables, lineage in decls:
        if name not in NAMES:
            found.append((DECLARING, r, line, f"a Construct field naming no construct: {name}"))
            continue
        if lineage in seen:
            found.append((DECLARING, r, line, f"a second construct in one section: § {lineage}"))
        seen[lineage] = line
        _fields(r, line, name, fields, found)
        if not tables:
            found.append((DECLARING, r, line, f"{_a(name)} declared with no table"))
            continue
        forms = FORMS[name]
        if len(tables) != len(forms):
            found.append((DECLARING, r, line, f"{_a(name)} with {len(tables)} tables where its form gives {len(forms)}"))
            continue
        ok = True
        # a Decision Table's annotations may be left empty, describing no row
        notes = [c.strip() for _, k, v in fields if k == "Annotations" for c in v.split(",")]
        for k, (table, form) in enumerate(zip(tables, forms)):
            header = table["header"]
            named = header[:1] == ["Name"] and k in NAMEABLE.get(name, set())
            cols = header[1:] if named else header
            if form is not None and cols != form:
                found.append((DECLARING, r, table["line"], f"{_a(name)} table headed {header}, not {form}"))
                ok = False
            for ln, row in table["rows"]:
                ident = [row[0]] if named or (name in ("Lifecycle", "State Machine") and k == 0) or name == "DAG" else []
                for v in ident:
                    if UNPLAIN.search(v):
                        found.append((DECLARING, r, ln, f"a part's identifier that is not plain text: {v}"))
            if named:
                names = [row[1][0] for row in table["rows"]]
                if any(not n for n in names) or len(set(names)) != len(names):
                    found.append((DECLARING, r, table["line"], "a Name column with a row unnamed, or two rows sharing a Name"))
            elif "Name" in header:
                found.append((DECLARING, r, table["line"], "a column headed Name that does not open a table it may open"))
            for ln, row in table["rows"]:
                empty = [header[c] for c, v in enumerate(row) if not v and c < len(header) and header[c] not in notes]
                if empty and not (name == "Decision Tree" and empty == ["Question"]):
                    found.append((DECLARING, r, ln, f"a cell holding no value: {empty}"))
                for c, v in enumerate(row[:len(header)]):
                    if cols == form and (v == "none" and (name, header[c]) not in NONE_COLUMNS
                                         or v == "-" and (name, header[c]) != ("Lifecycle", "Trigger")):
                        found.append((DECLARING, r, ln, f"a cell holding {v} where its form does not give it: {header[c]}"))
                if len(row) != len(header):
                    found.append((DECLARING, r, ln, f"a row of {len(row)} cells under a header of {len(header)}"))
                    ok = False
        if not ok:
            continue
        check = {"Lifecycle": _machine, "State Machine": _machine, "Decision Table": _decision_table,
                 "Decision Tree": _tree, "DAG": _dag, "Algorithm": _algorithm, "Constraint": _constraint}[name]
        check(r, line, name, fields, tables, found)


def _paragraphs(r, lines, line, fields, found):
    """§ Constructs § Declaring a Construct: the Construct field and each field it sets open a paragraph of
    their own, a field whose value is a list its key on a line of its own and its items beneath."""
    for ln, key, value in [(line, "Construct", "")] + fields:
        i = ln - 1
        inline = (FIELD.match(lines[i])["value"] or "").strip()
        j = i + 1
        if not inline and key != "Construct":
            while j < len(lines) and lines[j].startswith("- "):
                j += 1
        if i > 0 and lines[i - 1].strip() or j < len(lines) and lines[j].strip():
            found.append((DECLARING, r, ln, f"the {key} field not a paragraph of its own"))
        elif key in LIST_FIELDS and inline:
            found.append((DECLARING, r, ln, f"the {key} field's list written on its key's line, not beneath it"))
        elif key == "Default Output" and not inline and j - i - 1 < 2:
            # one outcome column takes a value on the key's line; several, an item for each
            found.append((DECLARING, r, ln, "a Default Output written beneath its key with fewer than two items"))


def _fields(r, line, name, fields, found):
    allowed = OWN_FIELDS.get(name, ())
    keys = [k for _, k, _ in fields]
    for ln, key, value in fields:
        if key not in allowed:
            found.append((DECLARING, r, ln, f"a {key} field {_a(name)} does not set"))
    order = [k for k in allowed if k in keys]
    if [k for k in keys if k in allowed] != order:
        found.append((DECLARING, r, line, f"{_a(name)}'s fields out of the order {list(allowed)}"))
    for key in REQUIRED.get(name, ()):
        if key not in keys:
            found.append((FIELD_RULE[key], r, line, f"{_a(name)} with no {key} field"))
    for ln, key, value in fields:
        if key in DEFAULTS and value == DEFAULTS[key]:
            found.append((FIELD_RULE[key], r, ln, f"the {key} field written at its default value, {value}"))
        listed = quoted_values(FIELD_VALUES.get(key, "text"))
        if listed is not None and value not in listed:
            found.append((FIELD_RULE[key], r, ln, f"the {key} field holds a value its definition does not allow: {value}"))
    values = dict((k, v) for _, k, v in fields)
    if values.get("Hit Policy") in ("Priority", "Output order") and "Output Values" not in values:
        found.append((FIELD_RULE["Output Values"], r, line, f"a {values['Hit Policy']} table with no Output Values field"))
    for ln, key, value in fields:
        if key == "Hit Policy" and value not in POLICIES + (DEFAULTS["Hit Policy"],):
            found.append((RULE + " § Decision Table", r, ln, f"a Hit Policy that is none of DMN's: {value}"))


# ---------------------------------------------------------------- Lifecycle and State Machine

def _machine(r, line, name, fields, tables, found):
    rule = f"{RULE} § {name}"
    states, transitions = tables
    names = [row[0] for _, row in states["rows"]]
    for ln, row in states["rows"]:
        if SEPARATOR.search(row[0]):
            found.append((DECLARING, r, ln, f"a state's name holding a comma or the word and: {row[0]}"))
        if row[2] not in ("Yes", "No") or row[3] not in ("Yes", "No"):
            found.append((rule, r, ln, f"a state's initial or terminal neither Yes nor No: {row[0]}"))
    if len(set(names)) != len(names):
        found.append((rule, r, states["line"], "two states sharing a name"))
    initial = [row[0] for _, row in states["rows"] if row[2] == "Yes"]
    terminal = {row[0] for _, row in states["rows"] if row[3] == "Yes"}
    if len(initial) != 1:
        found.append((rule, r, states["line"], f"{'no initial state' if not initial else 'more than one initial state'}"))
    known = set(names)
    off = 1 if transitions["header"][:1] == ["Name"] else 0
    edges, triggers, outgoing = [], {}, set()
    forks, joins = [], []
    for ln, row in transitions["rows"]:
        frm, to, trig = row[off], row[off + 1], row[off + 2]
        if "," in frm:
            found.append((rule, r, ln, f"a From listing states: {frm}"))
            continue
        froms = [s.strip() for s in frm.split(" and ")]
        tos = [s.strip() for s in to.split(" and ")]
        if name == "Lifecycle" and (len(froms) > 1 or len(tos) > 1):
            found.append((rule, r, ln, "a join or a fork, which a Lifecycle has none of"))
        for s in froms + tos:
            if s not in known:
                found.append((rule, r, ln, f"a From or To naming a state the States table does not hold: {s}"))
        if name == "Lifecycle" and trig in ("", "none", "-"):
            found.append((rule, r, ln, "a transition with no trigger"))
        if len(froms) > 1:
            joins.append((ln, frozenset(froms)))
        if len(tos) > 1:
            forks.append((ln, frozenset(tos)))
        for f in froms:
            outgoing.add(f)
            for t in tos:
                edges.append((f, t))
        if name == "Lifecycle":
            key = (frm, trig)
            if key in triggers and triggers[key] != to:
                found.append((rule, r, ln, f"a trigger leading from one state to two: {trig}"))
            triggers.setdefault(key, to)
    for s in names:
        if s not in terminal and s not in outgoing:
            found.append((rule, r, states["line"], f"a state that is not terminal with no way out: {s}"))
        if s in terminal and s in outgoing:
            found.append((rule, r, states["line"], f"a terminal state with a way out: {s}"))
    if len(initial) == 1:
        reached = _reach(initial[0], edges)
        for s in names:
            if s not in reached:
                found.append((rule, r, states["line"], f"a state the initial state cannot reach: {s}"))
    if name == "State Machine":
        _forks_and_joins(r, rule, forks, joins, edges, found)
        _choices(r, rule, transitions, off, found)


def _reach(start, edges):
    seen, todo = {start}, [start]
    while todo:
        s = todo.pop()
        for a, b in edges:
            if a == s and b not in seen:
                seen.add(b)
                todo.append(b)
    return seen


def _forks_and_joins(r, rule, forks, joins, edges, found):
    """Every fork is closed by one join from states its branches reach, and a join closes one fork:
    a pairing of forks and joins sought whole, so an outer fork never takes an inner fork's join."""
    can = []
    for _, branches in forks:
        reach = set()
        for b in branches:
            reach |= _reach(b, edges)
        can.append([j for j, (_, froms) in enumerate(joins) if froms <= reach])
    closer = {}  # join -> fork

    def take(f, tried):
        for j in can[f]:
            if j not in tried:
                tried.add(j)
                if j not in closer or take(closer[j], tried):
                    closer[j] = f
                    return True
        return False

    for f, (ln, _) in enumerate(forks):
        if not take(f, set()):
            found.append((rule, r, ln, "a fork no join closes"))
    for j, (ln, _) in enumerate(joins):
        if j not in closer:
            found.append((rule, r, ln, "a join no fork opens"))


def guard(text):
    """A guard -> {fact: cell}, or None where it is prose or a cell is in no listed form; `none`
    tests no fact."""
    if text.strip() == "none":
        return {}
    out = {}
    for part in _split_guard(text):
        m = re.fullmatch(r'\s*([^:,"]+?):\s*(.+?)\s*', part)
        if not m:
            return None
        cell = feel(m.group(2))
        inner = re.sub(r"^not\((.*)\)$", r"\1", m.group(2).strip())
        if cell is not None and not FORM_OPENING.match(inner) and re.search(r"[:,]", inner):
            return None  # a value written plain, without quotes, holds no colon or comma
        if cell is None or m.group(1).strip() in out:
            return None  # a row tests each of its facts once, in a form the section lists
        out[m.group(1).strip()] = cell
    return out


def _choices(r, rule, transitions, off, found):
    """An exclusive choice: two or more transitions from one state on one trigger, or on none,
    whose guards, read as a Unique Decision Table over their facts, never both hold."""
    groups = {}
    for ln, row in transitions["rows"]:
        trig = row[off + 2] if row[off + 2] else "none"
        groups.setdefault((row[off], trig), []).append((ln, row[off + 3]))
    for (frm, trig), rows in groups.items():
        if len(rows) < 2:
            continue
        parsed = []
        for ln, g in rows:
            p = guard(g)
            if p is None:
                found.append((rule, r, ln, f"an exclusive choice's guard not written as a Decision Table's row: {g}"))
            elif any(not any(matches(c, x) for x in _points(c)) for c in p.values()):
                found.append((rule, r, ln, f"a guard no case meets: {g}"))
            parsed.append((ln, p))
        kinds = {}
        for _, p in parsed:
            for fact, c in (p or {}).items():
                kinds.setdefault(fact, set()).update(_kind(c))
        for fact, ks in kinds.items():
            if len(ks) > 1:
                found.append((rule, r, rows[0][0], f"an exclusive choice's fact tested as values of more than one kind: {fact}"))
        for a in range(len(parsed)):
            for b in range(a + 1, len(parsed)):
                (la, ga), (lb, gb) = parsed[a], parsed[b]
                if ga is None or gb is None:
                    continue
                facts = set(ga) | set(gb)
                if all(overlap(ga.get(f, feel("-")), gb.get(f, feel("-"))) for f in facts):
                    found.append((rule, r, lb, f"two guards from {frm} on {trig} that can both hold"))


# ---------------------------------------------------------------- Decision Table

LIST_OR_RANGE = re.compile(QUOTED + r'|[\[\(].+\.\..+[\]\)]')


def _named(value):
    """A list field's items, `Header: cell` each -> {header: cell}."""
    out = {}
    for item in value.split("\n"):
        h, _, c = item.partition(":")
        cell = feel(c.strip()) if h.strip() and c.strip() else None
        if cell:
            out[h.strip()] = cell
    return out


def _decision_table(r, line, name, fields, tables, found):
    rule = f"{RULE} § Decision Table"
    table = tables[0]
    header = table["header"]
    off = 1 if header[:1] == ["Name"] else 0
    cols = header[off:]
    values = dict((k, v) for _, k, v in fields)
    policy = values.get("Hit Policy", "Unique")
    notes = [] if values.get("Annotations", "none") == "none" else [c.strip() for c in values["Annotations"].split(",")]
    if "Conditions" not in values:
        return  # its missing Conditions field is reported with its fields
    conds = [c.strip() for c in values["Conditions"].split(",")]
    if any(c not in cols for c in notes + conds):
        found.append((rule, r, line, "a Conditions or Annotations field naming no column of its table"))
        return
    n, m = len(conds), len(notes)
    # § Its columns: its conditions first, then one or more outcomes, then its annotations
    if cols[:n] != conds or (m and cols[len(cols) - m:] != notes) or len(cols) - n - m < 1:
        found.append((rule, r, line, "columns not conditions first, then one or more outcomes, then annotations"))
        return
    idx = list(range(off, off + n))
    outs = list(range(off + n, len(header) - m))
    if "Default Output" in values and values["Default Output"] != DEFAULTS["Default Output"]:
        items = values["Default Output"].split("\n")
        named = [i.partition(":")[0].strip() for i in items]
        if len(outs) == 1 and (len(items) != 1 or values["Default Output"].startswith(header[outs[0]] + ":")):
            found.append((rule, r, line, "a Default Output that is not one value, for its one outcome column"))
        elif len(outs) > 1 and (sorted(named) != sorted(header[k] for k in outs)
                                or any(not i.partition(":")[2].strip() for i in items)):
            found.append((rule, r, line, "a Default Output that is not an item for each outcome column, its header, a colon and its value"))
    # an aggregating Collect: one outcome column, of numbers but for a count
    if policy.startswith("Collect ") and (len(outs) != 1 or policy != "Collect count"
                                          and any(_num(row[outs[0]]) is None for _, row in table["rows"])):
        found.append((rule, r, line, f"a {policy} table whose outcome is not one column{'' if policy == 'Collect count' else ' of numbers'}"))
    # an outcome cell is never written as a test, which would show a condition declared an outcome
    for ln, row in table["rows"]:
        for k in outs:
            if TEST_FORM.match(row[k]):
                found.append((rule, r, ln, f"an outcome cell written as a test: {row[k][:20]}"))
    cells = {}
    for ln, row in table["rows"]:
        for k in idx:
            cells[(ln, k)] = feel(row[k])
            if cells[(ln, k)] is None:
                found.append((rule, r, ln, f"a cell in no form the section lists: {row[k]}"))
    if None in cells.values():
        return
    if values.get("Input Values", "none") != "none":
        for item in values["Input Values"].split("\n"):
            h, _, c = item.partition(":")
            if not (h.strip() and LIST_OR_RANGE.fullmatch(c.strip()) and feel(c.strip())):
                found.append((rule, r, line, f"an Input Values item that is not a header, a colon, and a quoted list or a range: {item}"))
    domains = _named(values.get("Input Values", ""))
    for k in idx:
        if header[k].endswith("?"):
            if header[k] in domains:
                found.append((rule, r, line, f"Input Values given for a question, whose values are Yes and No: {header[k]}"))
            domains[header[k]] = feel('"Yes", "No"')
    for k in idx:
        kinds = set().union(*[_kind(cells[(ln, k)]) for ln, _ in table["rows"]],
                            _kind(domains[header[k]]) if header[k] in domains else set())
        if len(kinds) > 1:
            found.append((rule, r, table["line"], f"a condition column testing values of more than one kind: {header[k]}"))
            return
    for h in domains:
        if h not in conds:
            found.append((rule, r, line, f"Input Values for a column that is no condition: {h}"))
    doms = [domains.get(header[k]) for k in idx]
    rows = [(ln, [cells[(ln, k)] for k in idx], [row[k] for k in outs]) for ln, row in table["rows"]]
    for ln, conds_, _ in rows:
        for k, c, d in zip(idx, conds_, doms):
            if d and outside(c, d):
                found.append((rule, r, ln, f"a cell outside its column's Input Values: {header[k]}"))
    ranked = None
    if "Output Values" in values:
        ranked = _ranked(values["Output Values"])
        if policy not in ("Priority", "Output order"):
            found.append((rule, r, line, "an Output Values field where the hit policy reads none"))
        elif ranked is None or any(h not in [header[k] for k in outs] for h in ranked):
            found.append((rule, r, line, "an Output Values item that is not an outcome column's header and a quoted list"))
            ranked = None
    if ranked:
        for ln, _, ob in rows:
            for h, allowed in ranked.items():
                if ob[outs.index(header.index(h))] not in allowed:
                    found.append((rule, r, ln, f"an outcome missing from its Output Values: {h}"))
                    return

    def rank(ob):
        return tuple(allowed.index(ob[outs.index(header.index(h))]) for h, allowed in ranked.items())

    for a in range(len(rows)):
        for b in range(a + 1, len(rows)):
            (la, ca, oa), (lb, cb, ob) = rows[a], rows[b]
            # a case lies within its columns' Input Values, where they are given
            meet = all(any(matches(x, v) and matches(y, v) and (not d or matches(d, v))
                           for v in _points(x, y, *([d] if d else [])))
                       for x, y, d in zip(ca, cb, doms))
            if policy == "Unique" and meet:
                found.append((rule, r, lb, "a case two rows match, where the hit policy is Unique"))
            if policy == "Any" and meet and oa != ob:
                found.append((rule, r, lb, "two rows a case matches giving different outcomes, where the hit policy is Any"))

    def pool(k, *cs):
        return [x for x in _points(*cs, *([doms[k]] if doms[k] else [])) if all(matches(c, x) for c in cs[:1])
                and (not doms[k] or matches(doms[k], x))]

    # a row that gives no case its outcome: one matching no case, or, where a row ahead takes a
    # case first, one whose every case a row ahead takes
    for b, (lb, cb, ob) in enumerate(rows):
        ahead = [c for a, (_, c, o) in enumerate(rows)
                 if policy == "First" and a < b or policy == "Priority" and ranked and rank(o) < rank(ob)]
        pools = [pool(k, cb[k], *[c[k] for c in ahead]) for k in range(len(idx))]
        if _escape(pools, ahead) is None:
            found.append((rule, r, lb, "a row that gives no case its outcome"))
    # coverage, decided where every condition gives its Input Values and no Default Output stands in
    if "Default Output" not in values and all(doms):
        case = _escape([pool(k, doms[k], *[c[k] for _, c, _ in rows]) for k in range(len(idx))],
                       [c for _, c, _ in rows])
        if case is not None:
            # a date or a date and time shown as FEEL writes it, not as its place on the timeline
            epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
            shown = tuple(x if not isinstance(x, float) or not _kind(doms[k]) & {"date", "date and time"}
                          else (epoch + timedelta(seconds=x)).isoformat()[:10 if _kind(doms[k]) == {"date"} else None]
                          for k, x in enumerate(case))
            found.append((rule, r, table["line"], f"a case no row matches: {shown}"))


def _tree(r, line, name, fields, tables, found):
    rule = f"{RULE} § Decision Tree"
    rows = tables[0]["rows"]
    steps, first = {}, {}
    ids = [row[0] for _, row in rows]
    if len(set(ids)) != len(ids):
        found.append((rule, r, tables[0]["line"], "two branches sharing a number"))
    for ln, row in rows:
        result = _form_of(row[3])
        m = re.fullmatch(r'(\d+)\.(\d+)', row[0])
        if not m:
            found.append((rule, r, ln, f"a branch numbered other than step and branch: {row[0]}"))
            continue
        step = m.group(1)
        if step not in first:
            first[step] = ln
            if not row[1]:
                found.append((rule, r, ln, f"step {step}'s first branch with no question"))
        elif row[1]:
            found.append((rule, r, ln, f"a question written on a branch of step {step} but its first"))
        steps.setdefault(step, set())
        if not row[3]:
            found.append((rule, r, ln, "a branch with no result"))
        elif any(j[1] for j in jumps(result)) and not (_ends_in_jump(result)
                                                       and result.lower().startswith(JUMP_WORDS.lower())):
            found.append((rule, r, ln, f"a result holding a jump and more: {row[3]}"))
        _jump_form(rule, r, ln, result, row[3], found)
        steps[step] |= {j[1] for j in jumps(result) if j[1]}
    numbers = {i.split(".")[0] for i in ids}
    for ln, row in rows:
        for target in [j[1] for j in jumps(_form_of(row[3])) if j[1]]:
            if "." in target:
                found.append((rule, r, ln, f"a jump naming a branch, not a step: {target}"))
            elif target not in numbers:
                found.append((rule, r, ln, f"a jump to a step the table does not hold: {target}"))
    if "1" not in steps:
        found.append((rule, r, tables[0]["line"], "no step 1 to start at"))
        return
    reached, todo = {"1"}, ["1"]
    while todo:
        s = todo.pop()
        for t in steps.get(s, ()):
            if t not in reached:
                reached.add(t)
                todo.append(t)
    for s in steps:
        if s not in reached:
            found.append((rule, r, first[s], f"a step no path from step 1 reaches: {s}"))
        if s in _reach_from(steps, s):
            found.append((rule, r, first[s], f"a step that leads back to itself: {s}"))


def _reach_from(graph, start):
    seen, todo = set(), list(graph.get(start, ()))
    while todo:
        s = todo.pop()
        if s not in seen:
            seen.add(s)
            todo.extend(graph.get(s, ()))
    return seen


# ---------------------------------------------------------------- DAG

def _dag(r, line, name, fields, tables, found):
    rule = f"{RULE} § DAG"
    rows = tables[0]["rows"]
    names = [row[0] for _, row in rows]
    if len(set(names)) != len(names):
        found.append((rule, r, tables[0]["line"], "two tasks sharing a name"))
    graph = {}
    for ln, row in rows:
        if SEPARATOR.search(row[0]):
            found.append((DECLARING, r, ln, f"a task's name holding a comma or the word and: {row[0]}"))
        deps = [] if row[1] == "none" else [d.strip() for d in row[1].split(",")]
        for d in deps:
            if d not in names:
                found.append((rule, r, ln, f"a dependency naming a task the table does not hold: {d}"))
        graph[row[0]] = set(deps)
    for t in names:
        if t in _reach_from(graph, t):
            found.append((rule, r, tables[0]["line"], f"a task that depends on itself, directly or through others: {t}"))


# ---------------------------------------------------------------- Algorithm

def _algorithm(r, line, name, fields, tables, found):
    rule = f"{RULE} § Algorithm"
    rows = tables[0]["rows"]
    numbers = [row[0] for _, row in rows]
    if numbers != [str(n) for n in range(1, len(rows) + 1)]:
        found.append((rule, r, tables[0]["line"], "steps not numbered from 1 in order"))
        return
    for ln, row in rows:
        step, action = int(row[0]), _form_of(row[1])
        comparison = action.startswith(COMPARISON_OPENING)
        if comparison and action.count(SEPARATOR_OF_BRANCHES) != 1:
            found.append((rule, r, ln, f"a comparison not written in its form: step {step}"))
        branches = action.split(SEPARATOR_OF_BRANCHES) if comparison else [action]
        _jump_form(rule, r, ln, action, row[1], found)
        # the separator of a comparison's branches in a step that is no comparison: a comparison folded into it
        if not comparison and SEPARATOR_MARK in action:
            found.append((rule, r, ln, f"a comparison's `{SEPARATOR_MARK}` in a step that is no comparison: step {step}"))
        for b in branches:
            tail = b.rstrip(". ")
            # a branch's jump naming a step ends it, alone; a jump naming none is reported for its form alone
            if any(j[1] for j in jumps(b)) and not _ends_in_jump(b) or END.search(b) and not END_AT_TAIL.search(tail):
                found.append((rule, r, ln, f"a jump or an End that does not end its branch: step {step}"))
        for target in [j[1] for j in jumps(action) if j[1]]:
            if not target.isdigit() or not 1 <= int(target) <= len(rows):
                found.append((rule, r, ln, f"a jump to a step the table does not hold: {target}"))
            elif int(target) <= step and not comparison:
                found.append((rule, r, ln, f"a step that is no comparison going back: step {step}"))
        if comparison:
            back = [b for b in branches if any(j[1] and j[1].isdigit() and int(j[1]) <= step for j in jumps(b))]
            if back and len(back) == len(branches):
                found.append((rule, r, ln, f"a comparison going back on every branch, with none going forward: step {step}"))
        if step == len(rows):
            for b in branches:
                if not (b.rstrip(". ").endswith(END_WORD) or jumps(b)):
                    found.append((rule, r, ln, "a last step, or a branch of it, that neither ends nor jumps"))


# ---------------------------------------------------------------- Constraint

# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation
# a citation: a section token and a title in one backtick span, after a file's path where it cites another file,
# never the token alone; the one copy of the form, which audit-specs.py reads as its own and an Enforced by names
# what enforces its rule by
CITATION = re.compile(r'`((?:[\w./-]+\.md\s*)?§\s+[^`]+)`')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
# the words an Enforced by opens with where its value is that nothing enforces the rule, the canon's "nothing in its
# Enforced by column", and the pattern matching them and the colon ending that value
NOTHING_WORDS = "nothing|none"
NOTHING_ENFORCES = re.compile(r'(?i)\s*(?:' + NOTHING_WORDS + r')\s*:')


def _constraint(r, line, name, fields, tables, found):
    rule = f"{RULE} § Constraint"
    table = tables[0]
    off = 1 if table["header"][:1] == ["Name"] else 0
    for ln, row in table["rows"]:
        enforced = row[off + 2]
        nothing = NOTHING_ENFORCES.match(_form_of(enforced))
        if not CITATION.search(enforced):
            found.append((rule, r, ln, "a rule stated but enforced nowhere: its Enforced by cites nothing"))
        # a cell whose value is that nothing enforces the rule, `nothing:` or `none:`, whatever it cites after
        elif nothing:
            word = enforced[nothing.start():nothing.end()].replace(" ", "").lower()
            found.append((rule, r, ln, f"a rule stated but enforced nowhere: its Enforced by opens `{word}`"))


# ---------------------------------------------------------------- a Name column, present where it is cited

def name_column_findings(text_of, cited, found, sections, strip_fences):
    """§ Constructs § Declaring a Construct: a table opens with a Name column exactly where a part
    of it is cited from outside its construct's section. `cited` holds the (path, lineage) pairs a
    part's citation by Name resolved to."""
    for r, body in text_of.items():
        live = strip_fences(body)
        for line, name, fields, tables, lineage in declarations(live, sections(body)):
            named = any(t["header"][:1] == ["Name"] for t in tables)
            if named and (r, lineage) not in cited:
                found.append((DECLARING, r, line, f"a Name column no citation from outside its section names a part by: § {lineage}"))


# ---------------------------------------------------------------- candidates for the reading audit

# @canon-spec specs/methodology/modeling-constructs.md § Constructs
# a construct's tables known by their leading columns, so one written in an earlier form is found too
LEADS = (("state", "description"), ("From", "To"), ("Step", "Question"), ("task",), ("Step", "Action"),
         ("Constraint", "Applies to"))


def construct_candidates(files, sections, strip_fences):
    """-> [(path, line, pattern, context)] for the Construct choice and form audit: a Decision
    Table whose cells do not settle that every case is matched, a table shaped as a construct's
    with no declaration, an Algorithm's step that may fold a comparison, and an Enforced by that may
    say nothing enforces its rule. `files` holds (path, body) pairs."""
    out = []
    for r, body in files:
        live = strip_fences(body)
        declared = set()
        for line, name, fields, tables, lineage in declarations(live, sections(body)):
            declared |= {t["line"] for t in tables}
            if name == "Decision Table" and tables and not _settled(fields, tables[0]):
                out.append((r, line, "coverage the cells do not settle",
                            f"§ {lineage}: whether every case matches a row is read"))
            # wording a script cannot judge, listed for the reading audit to read: a step that is no comparison
            # holding a comparison's words, its separator aside, which the Algorithm's check reports; and an
            # Enforced by opening nothing or none and holding a citation, its opening `nothing:` or `none:` aside,
            # which the Constraint's check reports
            if name == "Algorithm" and tables:
                for ln, row in tables[0]["rows"]:
                    text = _form_of(row[1])
                    if not text.startswith(COMPARISON_OPENING) and SEPARATOR_MARK not in text \
                            and COMPARISON_WORDS.search(text):
                        out.append((r, ln, "a comparison a step may fold", f"§ {lineage}: {row[1][:100]}"))
            if name == "Constraint" and tables:
                off = 1 if tables[0]["header"][:1] == ["Name"] else 0
                for ln, row in tables[0]["rows"]:
                    cell = row[off + 2] if len(row) > off + 2 else ""
                    if re.match(r'(?i)\s*(?:' + NOTHING_WORDS + r')\b', _form_of(cell)) and CITATION.search(cell) \
                            and not NOTHING_ENFORCES.match(_form_of(cell)):
                        out.append((r, ln, "an Enforced by that may say nothing enforces it", f"§ {lineage}: {cell[:100]}"))
        lines = live.split("\n")
        for i, l in enumerate(lines):
            if l.startswith("|") and (i == 0 or not lines[i - 1].startswith("|")) and i + 1 not in declared:
                header = tuple(_cells(l))
                rows = []
                for nxt in lines[i + 2:]:
                    if not nxt.startswith("|"):
                        break
                    rows.append(_cells(nxt))
                # a construct's form shows its tables with placeholder rows, and declares none
                template = any("..." in row for row in rows)
                lead = header[1:] if header[:1] == ("Name",) else header
                if not template and any(lead[:len(k)] == k for k in LEADS):
                    out.append((r, i + 1, "a construct's table with no declaration", l.strip()[:120]))
    return out


def _settled(fields, table):
    """Whether a Decision Table's coverage is decided or settled: Input Values for every condition,
    a question's Yes and No among them, a Default Output, a row testing no condition, or, with one
    condition, a not(…) row whose excluded values the other rows match."""
    header = table["header"]
    off = 1 if header[:1] == ["Name"] else 0
    values = dict((k, v) for _, k, v in fields)
    if "Conditions" not in values:
        return True  # its missing Conditions field is reported, and there is nothing to read
    conds = [c.strip() for c in values["Conditions"].split(",")]
    if any(c not in header for c in conds):
        return False
    # Input Values decide coverage, a question's Yes and No among them, and a Default Output settles it
    if "Default Output" in values or all(c in _named(values.get("Input Values", "")) or c.endswith("?") for c in conds):
        return True
    idx = [header.index(c) for c in conds]
    rows = [[feel(row[k]) for k in idx] for _, row in table["rows"]]
    if any(c is None for row in rows for c in row):
        return True  # a cell in no listed form is reported, and there is nothing to read
    if any(all(c == (False, [("any",)]) for c in row) for row in rows):
        return True
    # with one condition and a not(…) row, every value the cells name, and one none names, is matched
    if len(idx) == 1 and any(row[0][0] for row in rows):
        return all(any(matches(row[0], x) for row in rows) for x in _points(*[row[0] for row in rows]))
    return False


# ---------------------------------------------------------------- the fields table, held to its home

# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
def values_form(cell):
    """Whether a Values cell takes one of its forms: a quoted list, a citation of the section listing the values, or
    text."""
    return cell == "text" or bool(QUOTED_LIST.fullmatch(cell)) or bool(CITATION.fullmatch(cell))


def field_table_findings(text, sections):
    """§ Constructs § Declaring a Construct: FIELD_TABLES, this script's copy of each table of the fields a
    construct declares, against that table in `text`, modeling-constructs.md as it stands, whose sections
    are `sections`: each row's Field, Required, Default Value and Values, in its order, and each Values cell in one
    of the forms `§ Constructs § Record Form` gives it. -> [(rule, line, message)]."""
    lines, found = text.split("\n"), []
    for title, copy in FIELD_TABLES.items():
        start, end = sections.get(title, (0, 0))
        own = lines[start:end]
        h = next((i for i, l in enumerate(own) if l.startswith("| Field | Required | Default Value | Values |")), None)
        if h is None:
            found.append(("modeling-constructs.md § " + title, start + 1, f"no table of the fields § {title} defines"))
            continue
        rows = []
        for i in range(h + 2, len(own)):
            if not own[i].startswith("|"):
                break
            rows.append((start + i + 1, tuple(_cells(own[i])[:4])))
        found += [("modeling-constructs.md § " + title, ln, f"the fields table's row {row} differs from the script's copy {c}")
                  for (ln, row), c in zip(rows, copy) if row != c]
        found += [(RULE + " § Record Form", ln, f"a Values cell in none of its forms: {row[3]}")
                  for ln, row in rows if len(row) > 3 and not values_form(row[3])]
        if len(rows) != len(copy):
            found.append(("modeling-constructs.md § " + title, start + h + 1,
                          f"the fields table of § {title} holds {len(rows)} fields, the script's copy {len(copy)}"))
    return found
