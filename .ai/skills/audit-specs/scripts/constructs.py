"""audit-specs' construct checks: what modeling-constructs.md § Constructs lets a script decide.

A construct is found by its declaration, a **Construct:** field, and read from the block the
declaration opens: its fields, then its tables. Each check here decides structure from the files
alone; what a guard's fact means, what a state's work is, and whether the right construct was
chosen stay with the Construct choice and form reading audit (modeling-constructs.md § Purpose).
"""
import re
from datetime import datetime, timedelta, timezone

import expressions

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
        ("Reads", "no", "none", "text"),
        ("Conditions", "yes", "", "text"),
        ("Computed", "no", "none", "text"),
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
LIST_FIELDS = ("Reads", "Input Values", "Output Values")
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
# a date, a date and time, a time of day and a duration of either kind, the child script's copy
DATE, DATE_TIME, TIME = (expressions.LITERAL[k] for k in ("date", "date and time", "time"))
YM_DURATION, DT_DURATION = (expressions.LITERAL[k] for k in ("years and months duration", "days and time duration"))
# a fact's name, as a comparison's or a range's end names one, and a question's, the child script's copies
FACT_NAME, QUESTION = expressions.NAME, expressions.QUESTION
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# a list of values: each in double quotes, separated by commas; the one copy, which a quoted list and a list or a
# range are built from
QUOTED = r'"[^"]*"(?:\s*,\s*"[^"]*")*'
QUOTED_LIST = re.compile(r'\s*' + QUOTED + r'\s*')
# an absent value: `null` matches it, `-` where its column's values hold it, and `not(…)` around values
NULL = None


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
def quoted_values(cell):
    """The values a Values cell lists, where it is a quoted list, or None."""
    return re.findall(r'"([^"]*)"', cell) if QUOTED_LIST.fullmatch(cell) else None


def _value(s):
    """A number, or a FEEL date, date and time to the second with its offset, time of day or duration -> (its
    place on one line of its kind, its kind); None for anything else, a date or a time that does not exist
    among it."""
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
        m = TIME.fullmatch(s)
        if m:
            h, mi, sec, frac, off = m.groups()
            if int(h) > 23 or int(mi) > 59 or int(sec) > 59:
                return None
            shift = 0 if off in (None, "Z") else (1 if off[0] == "+" else -1) * (int(off[1:3]) * 3600 + int(off[4:6]) * 60)
            return int(h) * 3600 + int(mi) * 60 + int(sec) + float(frac or 0) - shift, "time"
    except ValueError:
        return None
    m = YM_DURATION.fullmatch(s)
    if m:
        sign = -1 if m.group(1) else 1
        return sign * float(int(m.group(2) or 0) * 12 + int(m.group(3) or 0)), "years and months duration"
    m = DT_DURATION.fullmatch(s)
    if m:
        sign = -1 if m.group(1) else 1
        d, h, mi, sec = (float(x or 0) for x in m.groups()[1:])
        return sign * (d * 86400 + h * 3600 + mi * 60 + sec), "days and time duration"
    return (float(s), "number") if NUMBER.fullmatch(s) else None


def _num(s):
    v = _value(s)
    return None if v is None else v[0]


def _split(body):
    """A cell's tests, split at each comma outside quotes, brackets and parentheses."""
    parts, depth, quoted, cur = [], 0, False, ""
    for ch in body:
        if ch == '"':
            quoted = not quoted
        elif not quoted and ch in "[(":
            depth += 1
        elif not quoted and ch in "])":
            depth -= 1
        if ch == "," and not quoted and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return parts + [cur.strip()]


def _end(s):
    """A comparison's or a range's end: a value -> (value, kind), a fact's name -> ("name", name), else None."""
    v = _value(s)
    if v:
        return v
    s = s.strip()
    if (FACT_NAME.fullmatch(s) or QUESTION.fullmatch(s)) and s not in ("null", "true", "false"):
        return ("name", s)
    return None


def _test(part):
    """One test: ("null",), ("is", value, kind), ("iv", low, low included, high, high included, kind), or
    ("sym", its text, the facts it names) for one whose end is a fact; None for none the section lists."""
    if part == "null":
        return ("null",)
    if re.fullmatch(r'"[^"]*"', part):
        return ("is", part[1:-1], "word")
    v = _value(part)
    if v:
        return ("is", v[0], v[1])  # a number, a date, a date and time, a time or a duration alone
    m = re.fullmatch(r'([\[\(])\s*(.+?)\s*\.\.\s*(.+?)\s*([\]\)])', part)
    if m:
        lo, hi = _end(m.group(2)), _end(m.group(3))
        if lo and hi and "name" in (lo[0], hi[0]):
            return ("sym", part, tuple(e[1] for e in (lo, hi) if e[0] == "name"))
        if lo and hi and lo[1] == hi[1]:
            return ("iv", lo[0], m.group(1) == "[", hi[0], m.group(4) == "]", lo[1])
        return None
    m = re.fullmatch(r'(<=|>=|<|>|=)\s*(.+)', part)
    if m:
        e = _end(m.group(2))
        if e and e[0] == "name":
            return ("sym", part, (e[1],))
        if e and m.group(1) == "=":
            return None  # `=` tests equality with a fact, a value being tested as itself
        if e:
            x, kind = e
            inf = float("inf")
            return {"<": ("iv", -inf, False, x, False, kind), "<=": ("iv", -inf, False, x, True, kind),
                    ">": ("iv", x, False, inf, False, kind), ">=": ("iv", x, True, inf, False, kind)}[m.group(1)]
    return None


def _tests(body):
    """Each test of a cell, any of which matches; a quoted value is a word however it reads, and a cell written
    plain, opening as no form does, is one word, commas and all."""
    if QUOTED_LIST.fullmatch(body):
        return [("is", q, "word") for q in re.findall(r'"([^"]*)"', body)]
    if not (FORM_OPENING.match(body) or body == "null" or re.match(r'null\s*,', body) or _value(body)):
        return [("is", body, "word")]
    tests = [_test(p) for p in _split(body)]
    return None if None in tests else tests  # it opens as a form does, and is written in none the section lists


def symbolic(cell):
    """Whether a cell tests against a fact, so what it matches waits on that fact's value."""
    return any(t[0] == "sym" for t in cell[1])


def matches(cell, x, absent=False):
    """Whether a value, or an absent one, meets a cell; a test against a fact, whose answer waits on that fact, is
    no hit here, so every check reading what a cell matches sets such a cell aside first. An absent value meets `null`; `-` where `absent`, its column's
    values holding it; and `not(…)` where each test inside is a value it is not, FEEL comparing an absent value with
    a value to false and with a comparison or a range to no answer (DMN 10.3.2.10, grammar rule 15; Table 49)."""
    neg, tests = cell
    if x is NULL:
        if not neg:
            return any(t[0] == "null" for t in tests) or absent and any(t[0] == "any" for t in tests)
        return all(t[0] == "is" or t[0] == "sym" and t[1].startswith("=") for t in tests)
    hit = False
    for test in tests:
        if test[0] == "any":
            hit = True
        elif test[0] == "is":
            hit = hit or x == test[1]  # a word never equals a number
        elif test[0] == "iv" and isinstance(x, float):
            lo, lo_in, hi, hi_in = test[1:5]
            hit = hit or ((x > lo or lo_in and x == lo) and (x < hi or hi_in and x == hi))
    return hit != neg


def _points(*cells):
    """Every boundary the cells name, a point between and beyond each, and, where they test words,
    a word none names: enough that two cells agree on these points only where they agree everywhere;
    an absent value among them where a cell tests one. A date is a whole day, so the point beside a
    date's boundary is the day before or after it."""
    words, nums, kinds, absent = set(), set(), set(), False
    for neg, tests in cells:
        for test in tests:
            if test[0] == "null":
                absent = True
            elif test[0] == "is" and isinstance(test[1], str):
                words.add(test[1])
            elif test[0] == "is":
                nums.add(test[1])
                kinds.add(test[2])
            elif test[0] == "iv":
                nums |= {x for x in (test[1], test[3]) if abs(x) != float("inf")}
                kinds.add(test[5])
    tail = [NULL] if absent else []
    if kinds == {"date"}:
        return sorted(set(nums) | {n + d for n in nums for d in (-86400.0, 86400.0)}) + tail
    if kinds:
        ns = sorted(nums) or [0.0]
        return sorted(set(ns) | {ns[0] - 1, ns[-1] + 1} | {(a + b) / 2 for a, b in zip(ns, ns[1:])}) + tail
    return sorted(words) + ["\x00a value no cell names"] + tail


def overlap(a, b):
    """Whether one case can match both cells; a cell testing against a fact is set aside, never overlapping."""
    if symbolic(a) or symbolic(b):
        return False
    return any(matches(a, x) and matches(b, x) for x in _points(a, b))


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
FORM_OPENING = re.compile(r'not\(|[<>=!\[\]\("]|-$|(?:date and time|date|time|duration)\(')


def outside(cell, dom):
    """Whether a cell names a value its column's Input Values do not hold, or matches none they hold."""
    if symbolic(cell):
        return False
    if any(not matches(dom, t[1]) for t in cell[1] if t[0] == "is"):
        return True
    if any(t[0] == "null" for t in cell[1]) and not matches(dom, NULL):
        return True
    return not any(matches(cell, x) and matches(dom, x) for x in _points(cell, dom))


def _kind(cell):
    """The kinds of value a cell tests: words, numbers, dates, dates and times, times or durations; none for
    `-`, `null` or a test against a fact."""
    return {t[-1] for t in cell[1] if t[0] in ("is", "iv")}


def _escape(pools, rows, absent=None):
    """A case, one value from each condition's pool, that no row matches, or None. Each pool's
    values are grouped by the rows still matching, so each group is searched once; `absent` says, for each
    condition, whether its values hold an absent one, which `-` then matches."""
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
            hit = walk(k + 1, frozenset(i for i in alive if matches(rows[i][k], x, bool(absent and absent[k]))),
                       case + [x])
            if hit is not None:
                return hit
        return None

    return walk(0, frozenset(range(len(rows))), [])


def _split_guard(text):
    """A guard's tests, split at each ` and ` outside quotes, a FEEL date and time's own aside."""
    return re.split(r' and (?!time\()(?=(?:[^"]*"[^"]*")*[^"]*$)', text)


# an outcome cell written as a condition's test would be: any value, a negation, a comparison, a range
TEST_FORM = re.compile(r'-$|not\(|(?:<=|>=|<|>|=)\s*\S|[\[\(][^\]\)]*\.\.|null\s*,')


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
    records = fact_records(body, sections)
    facts = facts_of(records)
    for ln, msg in fact_record_findings(records):
        found.append((f"{DECLARING} § A Fact", r, ln, msg))
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
        if name == "Decision Table":
            _decision_table(r, line, name, fields, tables, found, facts)
        else:
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
        if cell is not None and len(cell[1]) == 1 and not FORM_OPENING.match(inner) and re.search(r"[:,]", inner):
            return None  # a value written plain, without quotes, holds no colon or comma
        if cell is None or symbolic(cell) or m.group(1).strip() in out:
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

LIST_OR_RANGE = re.compile(r'(?:null\s*,\s*)?(?:' + QUOTED + r'|[\[\(].+\.\..+[\]\)])(?:\s*,\s*null)?')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# a Reads item: a fact's or an outcome's name, a colon, and the citation of where it is declared or decided
READS_ITEM = re.compile(r'([^:`]+?):\s*`[^`]*§[^`]+`')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct § A Fact
# a Facts record's Type, and the kind of value a cell tests for it
TYPE_KINDS = {"string": "word", "number": "number", "boolean": "boolean", "date": "date", "time": "time",
              "date and time": "date and time", "days and time duration": "days and time duration",
              "years and months duration": "years and months duration"}


def multi_hit(policy):
    """Whether a hit policy takes the outcome of every row a case matches: Rule order, Output order, a Collect."""
    return policy in ("Rule order", "Output order") or policy.startswith("Collect")


def computing(header):
    """Whether a condition's header computes the value its column tests, a question never doing so."""
    return not header.endswith("?") and bool(expressions.COMPUTING.search(header))


def _outcome(v):
    """An outcome cell's value, a word quoted or plain alike; a quoted value that would read as another kind
    plain, `"5"`, stays quoted, a word and not that value."""
    if re.fullmatch(r'"[^"]*"', v) and _value(v[1:-1]) is None and v[1:-1] not in ("null", "-"):
        return v[1:-1]
    return v


def _shown(x, kinds):
    """A case's value as FEEL writes it, not as its place on its line: a date, a date and time, a time or a
    duration; an absent value as `null`."""
    if x is NULL:
        return "null"
    if not isinstance(x, float) or kinds <= {"number"}:
        return x
    if kinds == {"date"} or kinds == {"date and time"}:
        s = (datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=x)).isoformat()
        return f'date("{s[:10]}")' if kinds == {"date"} else f'date and time("{s}")'
    if kinds == {"time"}:
        s = int(x) % 86400
        return f'time("{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}")'
    sign, n = ("-" if x < 0 else ""), abs(x)
    if kinds == {"years and months duration"}:
        return f'duration("{sign}P{int(n) // 12}Y{int(n) % 12}M")'
    if kinds == {"days and time duration"}:
        d, rest = divmod(n, 86400)
        h, rest = divmod(rest, 3600)
        mi, s = divmod(rest, 60)
        return f'duration("{sign}P{int(d)}DT{int(h)}H{int(mi)}M{s:g}S")'
    return x


def fact_records(body, sections):
    """Each record of a file's Facts sections -> [(line, name, {field: value})]."""
    lines, out = body.split(chr(10)), []
    for lineage, (h, end) in sections.items():
        if lineage.rsplit(" § ", 1)[-1] != "Facts":
            continue
        for i in range(h, end):
            f = FIELD.match(lines[i])  # a record's fields, its first after a list marker, the rest indented
            if f and f["key"] == "Name" and f["marker"]:
                out.append((i + 1, (f["value"] or "").strip(), {}))
            elif f and out and out[-1][0] > h:
                out[-1][2][f["key"]] = (f["value"] or "").strip()
    return out


def facts_of(records):
    """The facts a file's Facts records declare -> {name: (Type, Values, May Be Absent)}."""
    return {n: (d.get("Type", ""), d.get("Values", "none"), d.get("May Be Absent", "No")) for _, n, d in records}


def fact_record_findings(records):
    """§ Constructs § Declaring a Construct § A Fact: a record whose name is no fact's name, or a boolean fact's
    asking no question, and Values naming a fact -> [(line, message)]."""
    out = []
    for line, name, d in records:
        if d.get("Type") == "boolean" and not QUESTION.fullmatch(name):
            out.append((line, f"a boolean fact whose name asks no question: {name}"))
        elif d.get("Type") != "boolean" and not FACT_NAME.fullmatch(name):
            out.append((line, f"a Facts record's name that is no fact's name: {name}"))
        cell = feel(d["Values"]) if d.get("Values", "none") != "none" else None
        if cell and symbolic(cell):
            out.append((line, f"a Facts record's Values naming a fact: {name}"))
    return out


def _named(value):
    """A list field's items, `Header: cell` each -> {header: cell}."""
    out = {}
    for item in value.split("\n"):
        h, _, c = item.partition(":")
        cell = feel(c.strip()) if h.strip() and c.strip() else None
        if cell:
            out[h.strip()] = cell
    return out


def domains_of(header, idx, values, facts):
    """Each condition's values: its Input Values item, a question's `Yes` and `No`, or its Facts record's Values,
    `null` among them where its fact may be absent -> {header: cell}."""
    given = values.get("Input Values", "")
    domains = _named(given)
    for k in idx:
        h = header[k]
        if h.endswith("?"):
            domains[h] = feel('"Yes", "No"')
        if h in facts:
            _, fvalues, absent = facts[h]
            dom = domains.get(h) or (feel(fvalues) if fvalues != "none" else None)
            if dom and symbolic(dom):
                dom = None  # Values naming a fact, reported at its record, give the column none
            if dom and absent == "Yes":
                dom = (dom[0], dom[1] + [("null",)])
            if dom:
                domains[h] = dom
    return domains


def _decision_table(r, line, name, fields, tables, found, facts=None):
    rule = f"{RULE} § Decision Table"
    facts = facts or {}
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
    computed = [] if values.get("Computed", "none") == "none" else [c.strip() for c in values["Computed"].split(",")]
    if any(c not in [header[k] for k in outs] for c in computed):
        found.append((rule, r, line, "a Computed field naming a column that is no outcome"))
        return
    # § Its facts: what a cell, a computed header or a computed outcome may name, each with its kind where known
    reads = []
    for item in [] if values.get("Reads", "none") == "none" else values["Reads"].split("\n"):
        mm = READS_ITEM.fullmatch(item.strip())
        named = mm and re.search(r'\[Name: ([^\]]+)\]', item)
        if not mm or not (FACT_NAME.fullmatch(mm.group(1).strip()) or QUESTION.fullmatch(mm.group(1).strip())):
            found.append((rule, r, line, f"a Reads item that is not a name, a colon and a citation: {item}"))
        elif named and named.group(1).strip() != mm.group(1).strip():
            found.append((rule, r, line, f"a Reads item named otherwise than the Facts record it cites: {item}"))
        else:
            reads.append(mm.group(1).strip())
    typed = {f: TYPE_KINDS.get(t) for f, (t, _, _) in facts.items()}
    known = dict({h: None for h in reads}, **typed)
    for k in idx:
        if not computing(header[k]):
            known.setdefault(header[k], "boolean" if header[k].endswith("?") else None)
    feel_kinds = {k: ("string" if v == "word" else v) for k, v in known.items()}
    for k in idx:
        if not computing(header[k]) and not FACT_NAME.fullmatch(header[k]) and not QUESTION.fullmatch(header[k]):
            found.append((rule, r, table["line"], f"a condition's header neither a fact's name nor a computation: {header[k]}"))
        if computing(header[k]):
            for p in expressions.check(header[k], feel_kinds)[1]:
                found.append((rule, r, table["line"], f"{p}, in the computed header {header[k]}"))
    if "Default Output" in values and values["Default Output"] != DEFAULTS["Default Output"]:
        items = values["Default Output"].split("\n")
        named = [i.partition(":")[0].strip() for i in items]
        if len(outs) == 1 and (len(items) != 1 or values["Default Output"].startswith(header[outs[0]] + ":")):
            found.append((rule, r, line, "a Default Output that is not one value, for its one outcome column"))
        elif len(outs) > 1 and (sorted(named) != sorted(header[k] for k in outs)
                                or any(not i.partition(":")[2].strip() for i in items)):
            found.append((rule, r, line, "a Default Output that is not an item for each outcome column, its header, a colon and its value"))
        # § Its values: under First, the outcome where no other row matches is a last row testing nothing
        if policy == "First":
            found.append((rule, r, line, "a First table's fall-through written as a Default Output, not a last row testing nothing"))
    # § Its outcomes: a computed column's cells are FEEL over the facts a cell may name, their kinds agreeing
    kinds_out = {}
    for ln, row in table["rows"]:
        for k in outs:
            if header[k] in computed:
                kind, problems = expressions.check(row[k], feel_kinds)
                kinds_out[(ln, k)] = kind
                for p in problems:
                    found.append((rule, r, ln, f"{p}, in the computed outcome {row[k]}"))
    # an aggregating Collect: one outcome column, of numbers but for a count
    agg_ok = lambda ln, k, v: kinds_out.get((ln, k)) in ("number", None) if header[k] in computed \
        else (_value(v) or (None, None))[1] == "number"
    if policy.startswith("Collect ") and (len(outs) != 1 or policy != "Collect count"
                                          and any(not agg_ok(ln, outs[0], row[outs[0]]) for ln, row in table["rows"])):
        found.append((rule, r, line, f"a {policy} table whose outcome is not one column{'' if policy == 'Collect count' else ' of numbers'}"))
    # an outcome cell is never written as a test, which would show a condition declared an outcome
    for ln, row in table["rows"]:
        for k in outs:
            if header[k] not in computed and (TEST_FORM.match(row[k]) or row[k].startswith("[")
                                              or FORM_OPENING.match(row[k]) and len(_split(row[k])) > 1):
                found.append((rule, r, ln, f"an outcome cell written as a test: {row[k][:20]}"))
    cells = {}
    for ln, row in table["rows"]:
        for k in idx:
            cells[(ln, k)] = feel(row[k])
            if cells[(ln, k)] is None:
                found.append((rule, r, ln, f"a cell in no form the section lists: {row[k]}"))
            else:
                for t in cells[(ln, k)][1]:
                    for fact in (t[2] if t[0] == "sym" else ()):
                        if fact not in known:
                            found.append((rule, r, ln, f"a cell naming a fact no condition, Reads item or Facts record declares: {fact}"))
    if None in cells.values():
        return
    if values.get("Input Values", "none") != "none":
        for item in values["Input Values"].split("\n"):
            h, _, c = item.partition(":")
            if not (h.strip() and LIST_OR_RANGE.fullmatch(c.strip()) and feel(c.strip())) or symbolic(feel(c.strip())):
                found.append((rule, r, line, f"an Input Values item that is not a header, a colon, and a quoted list or a range of values: {item}"))
            elif h.strip() in facts:
                found.append((rule, r, line, f"Input Values given for a fact its Facts record declares: {h.strip()}"))
            elif h.strip().endswith("?"):
                found.append((rule, r, line, f"Input Values given for a question, whose values are Yes and No: {h.strip()}"))
    domains = {h: d for h, d in domains_of(header, idx, values, facts).items() if not symbolic(d)}
    for k in idx:
        if header[k] not in facts:
            continue
        ftype, _, absent = facts[header[k]]
        want = TYPE_KINDS.get(ftype)
        for ln, _ in table["rows"]:
            c = cells[(ln, k)]
            if any(t[0] == "null" for t in c[1]) and absent != "Yes":
                found.append((rule, r, ln, f"a null cell for a fact that may not be absent: {header[k]}"))
            got = _kind(c) - ({"word"} if want == "boolean" else set())
            if want and got and got != {want}:
                found.append((rule, r, ln, f"a cell testing a {', '.join(sorted(got))} where its fact is a {ftype}: {header[k]}"))
    for k in idx:
        kinds = set().union(*[_kind(cells[(ln, k)]) for ln, _ in table["rows"]],
                            _kind(domains[header[k]]) if header[k] in domains else set())
        if len(kinds) > 1:
            found.append((rule, r, table["line"], f"a condition column testing values of more than one kind: {header[k]}"))
            return
        # a cell ending at a fact tests it against a fact of the column's kind
        col = "boolean" if header[k].endswith("?") else TYPE_KINDS.get(facts[header[k]][0]) if header[k] in facts \
            else (kinds.pop() if kinds else None)
        for ln, _ in table["rows"]:
            for t in cells[(ln, k)][1]:
                for fact in (t[2] if t[0] == "sym" else ()):
                    if col and known.get(fact) and known[fact] != col:
                        found.append((rule, r, ln, f"a cell testing a {col} column against a {known[fact]} fact: {fact}"))
    for h in domains:
        if h not in conds:
            found.append((rule, r, line, f"Input Values for a column that is no condition: {h}"))
    doms = [domains.get(header[k]) for k in idx]
    absent = [bool(d and matches(d, NULL)) or header[k] in facts and facts[header[k]][2] == "Yes"
              for k, d in zip(idx, doms)]
    rows = [(ln, [cells[(ln, k)] for k in idx], [_outcome(row[k]) for k in outs]) for ln, row in table["rows"]]
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
            if any(symbolic(x) or symbolic(y) for x, y in zip(ca, cb)):
                continue  # what a cell testing against a fact matches waits on that fact, read by the audit
            # a case lies within its columns' Input Values, where they are given
            meet = all(any(matches(x, v, ab) and matches(y, v, ab) and (not d or matches(d, v))
                           for v in _points(x, y, *([d] if d else [])))
                       for x, y, d, ab in zip(ca, cb, doms, absent))
            if policy == "Unique" and meet:
                found.append((rule, r, lb, "a case two rows match, where the hit policy is Unique"))
            if policy == "Any" and meet and oa != ob:
                found.append((rule, r, lb, "two rows a case matches giving different outcomes, where the hit policy is Any"))
    if any(symbolic(c) for c in cells.values()):
        return  # which rows a case reaches, and whether every case is matched, wait on the facts it names

    def pool(k, *cs):
        return [x for x in _points(*cs, *([doms[k]] if doms[k] else [])) if all(matches(c, x, absent[k]) for c in cs[:1])
                and (not doms[k] or matches(doms[k], x))]

    # a row that gives no case its outcome: one matching no case, or, where a row ahead takes a
    # case first, one whose every case a row ahead takes
    for b, (lb, cb, ob) in enumerate(rows):
        ahead = [c for a, (_, c, o) in enumerate(rows)
                 if policy == "First" and a < b or policy == "Priority" and ranked and rank(o) < rank(ob)]
        pools = [pool(k, cb[k], *[c[k] for c in ahead]) for k in range(len(idx))]
        if _escape(pools, ahead, absent) is None:
            found.append((rule, r, lb, "a row that gives no case its outcome"))
    # coverage, decided where every condition gives its values, no Default Output stands in, and the table takes one
    # row's outcome: under a hit policy taking every row it matches, a case matching none means no row applies
    if "Default Output" not in values and all(doms) and not multi_hit(policy):
        case = _escape([pool(k, doms[k], *[c[k] for _, c, _ in rows]) for k in range(len(idx))],
                       [c for _, c, _ in rows], absent)
        if case is not None:
            shown = tuple(_shown(x, _kind(doms[k])) for k, x in enumerate(case))
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
    Table a cell of which tests against a fact, a Decision Table whose cells do not settle that every case is
    matched, a table shaped as a construct's
    with no declaration, an Algorithm's step that may fold a comparison, and an Enforced by that may
    say nothing enforces its rule. `files` holds (path, body) pairs."""
    out = []
    for r, body in files:
        live = strip_fences(body)
        declared = set()
        secs = sections(body)
        facts = facts_of(fact_records(live, secs))
        for line, name, fields, tables, lineage in declarations(live, secs):
            declared |= {t["line"] for t in tables}
            if name == "Decision Table" and tables and _against_a_fact(fields, tables[0]):
                out.append((r, line, "cells testing against a fact",
                            f"§ {lineage}: which rows a case reaches, and whether every case matches one, is read"))
            elif name == "Decision Table" and tables and not _settled(fields, tables[0], facts):
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


def _against_a_fact(fields, table):
    """Whether a Decision Table holds a cell testing against a fact, which the script sets aside."""
    header = table["header"]
    values = dict((k, v) for _, k, v in fields)
    conds = [c.strip() for c in values.get("Conditions", "").split(",") if c.strip()]
    idx = [header.index(c) for c in conds if c in header]
    return any((c := feel(row[k])) is not None and symbolic(c) for _, row in table["rows"] for k in idx)


def _settled(fields, table, facts=None):
    """Whether a Decision Table's coverage is decided or settled: its values for every condition, an Input
    Values item, a question's Yes and No or a Facts record's Values, a Default Output, a hit policy taking every row
    a case matches, a row testing no condition, or, with one condition, a not(…) row whose excluded values the other
    rows match."""
    header = table["header"]
    off = 1 if header[:1] == ["Name"] else 0
    values = dict((k, v) for _, k, v in fields)
    if "Conditions" not in values:
        return True  # its missing Conditions field is reported, and there is nothing to read
    conds = [c.strip() for c in values["Conditions"].split(",")]
    if any(c not in header for c in conds):
        return False
    # a condition's values decide coverage, and a Default Output or a hit policy taking every row settles it
    domains = domains_of(header, [header.index(c) for c in conds], values, facts or {})
    if "Default Output" in values or multi_hit(values.get("Hit Policy", "Unique")) or all(c in domains for c in conds):
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
