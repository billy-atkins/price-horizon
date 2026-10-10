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
NAMES = ("State Machine", "Decision Table", "Decision Tree", "DAG", "Algorithm", "Constraint")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
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
        ("Runs When", "yes", "", "text"),
        ("Precision", "no", "34", "text"),
        ("Rounding Mode", "no", "half even", "text"),
    ),
    "Constructs § State Machine": (
        ("Protocol", "no", "No", '"Yes", "No"'),
        ("Recorded In", "no", "none", "text"),
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
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# the fields whose value is a list, each item beneath the field's key, an Algorithm's Inputs and Output taking none
# on the key's line; a Default Output is one where its table has several outcome columns
LIST_FIELDS = ("Inputs", "Output", "Reads", "Input Values", "Output Values")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# DMN's hit policies; Unique is the default value, reported where it is written
POLICIES = ("Any", "Priority", "First", "Rule order", "Output order",
            "Collect", "Collect sum", "Collect count", "Collect min", "Collect max")

# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# a States table's headers
STATES = ["state", "description", "initial", "terminal"]
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Tree
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# each construct's tables, by their headers; None where a Decision Table's columns are its own
FORMS = {
    "State Machine": [STATES, ["From", "To", "Trigger"]],
    "Decision Tree": [["Step", "Question", "Answer", "Result"]],
    "DAG": [["task", "depends_on"]],
    "Algorithm": [["Step", "Action"]],
    "Constraint": [["Constraint", "Applies to", "Enforced by"]],
    "Decision Table": [None],
}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § DAG
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# the columns whose form gives `none`; no form here gives `-`, a Decision Table's `-` being its cells' own
NONE_COLUMNS = {("State Machine", "Trigger"), ("State Machine", "Guard"), ("State Machine", "Effect"),
                ("DAG", "depends_on"), ("Algorithm", "Terminates")}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# a transition's trigger or guard of none, as a row writes it: the one copy
NONE_CELL = "none"
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# the columns a construct's table may add after its form's own, any of them, in this order: a State Machine's
# Transitions table's Guard, its Effect, or both; an Algorithm's Terminates
OPTIONAL_COLUMNS = {("State Machine", 1): ["Guard", "Effect"], ("Algorithm", 0): ["Terminates"]}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct
# the tables a Name column may open: a Transitions table, a Decision Table, a Constraint table
NAMEABLE = {"State Machine": {1}, "Decision Table": {0}, "Constraint": {0}}

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
    """A cell -> (negated, tests), each test as `_test` sorts it into the forms the checks read, or set aside for
    the parser to judge with the names in scope (modeling-constructs.md § Constructs § Decision Table). A cell
    written plain is one value, commas and all."""
    v = text.strip()
    if v == "-":
        return (False, [("any",)])
    m = re.fullmatch(r'not\((.*)\)', v)
    neg, body = (True, m.group(1).strip()) if m else (False, v)
    return neg, _tests(body)


NUMBER = re.compile(r'-?(?:\d+(?:\.\d+)?|\.\d+)')
# a date, a date and time, a time of day and a duration of either kind, the child script's copy
DATE, DATE_TIME, TIME = (expressions.LITERAL[k] for k in ("date", "date and time", "time"))
YM_DURATION, DT_DURATION = (expressions.LITERAL[k] for k in ("years and months duration", "days and time duration"))
# a fact's name, as a comparison's or a range's end names one, and a question's, the child script's copies
FACT_NAME, QUESTION = expressions.NAME, expressions.QUESTION


def _is_name(text):
    """Whether a text is a fact's name or a question's."""
    return bool(FACT_NAME.fullmatch(text) or QUESTION.fullmatch(text))


def _feel(text):
    """Whether a text is in a form FEEL has, its names left to the judgment of their scope."""
    return not any("no form FEEL has" in p for p in expressions.check(text, {}, lambda n: True)[1])
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
    at = re.fullmatch(r'@"([^"]*)"', s)
    if at:
        # an `@` value, read as the date, the date and time, the time or the duration it writes
        return next((v for v in (_value(f'{k}("{at.group(1)}")') for k in ("date", "date and time", "time", "duration"))
                     if v), None)
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
        elif not quoted and ch in "[({":
            depth += 1
        elif not quoted and ch in "])}":
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
    if _is_name(s) and s not in ("null", "true", "false"):
        return ("name", s)
    return None


def _test(part):
    """One test: ("null",), ("is", value, kind), ("iv", low, low included, high, high included, kind), or
    ("sym", its text, the facts it names) for one whose end is a fact, or ("sym", its text, ()) for any other, which the
    checks set aside and the parser judges with the names in scope; ("eqv", its text) for a value after `=`."""
    if part == "null":
        return ("null",)
    if part in ("true", "false"):
        return ("is", part, "boolean")
    # a value tested after `=`, which a cell writes alone: FEEL, and the canon's one writing of it kept
    m = re.fullmatch(r'=\s*(.+)', part)
    if m and (_value(m.group(1)) or re.fullmatch(r'"[^"]*"', m.group(1).strip()) or m.group(1).strip() in ("true", "false", "null")):
        return ("eqv", part)
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
    m = re.fullmatch(r'(<=|>=|<|>|=)\s*(.+)', part)
    if m:
        e = _end(m.group(2))
        if e and e[0] == "name":
            return ("sym", part, (e[1],))
        if e:
            x, kind = e
            inf = float("inf")
            return {"<": ("iv", -inf, False, x, False, kind), "<=": ("iv", -inf, False, x, True, kind),
                    ">": ("iv", x, False, inf, False, kind), ">=": ("iv", x, True, inf, False, kind)}[m.group(1)]
    # any other text: set aside, the parser, given the names in scope, judging whether it is FEEL
    return ("sym", part, ())


def _tests(body):
    """Each test of a cell, any of which matches; a quoted value is a word however it reads, and a cell written
    plain, opening as no form does and holding no `?`, is one word, commas and all, an expression a cell tests
    equality with written after `=`."""
    if QUOTED_LIST.fullmatch(body):
        return [("is", q, "word") for q in re.findall(r'"([^"]*)"', body)]
    if not (FORM_OPENING.match(body) or body in ("null", "true", "false") or re.match(r'(?:null|true|false)\s*,', body)
            or _value(body) or "?" in body):
        return [("is", body, "word")]
    return [_test(p) for p in _split(body)]


def names_a_fact(cell):
    """Whether a cell's test ends at a fact's name, as `< due date` does."""
    return any(t[0] == "sym" and t[2] for t in cell[1])


def symbolic(cell):
    """Whether a cell tests against a fact, or in a form the checks do not read, so what it matches is read."""
    return any(t[0] in ("sym", "eqv") for t in cell[1])


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
FORM_OPENING = re.compile(r'not\(|[<>=!\[\]\("@{]|-$|(?:date and time|date|time|duration)\(')


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
            extra = OPTIONAL_COLUMNS.get((name, k), [])
            if form is not None and cols not in [form + [x for i, x in enumerate(extra) if n >> i & 1] for n in range(2 ** len(extra))]:
                found.append((DECLARING, r, table["line"], f"{_a(name)} table headed {header}, not {form}"
                              + (f" and then any of {extra}, in order" if extra else "")))
                ok = False
            formed = form is not None and cols[:len(form)] == form
            for ln, row in table["rows"]:
                ident = [row[0]] if named or (name == "State Machine" and k == 0) or name == "DAG" else []
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
                    if formed and (v == "none" and (name, header[c]) not in NONE_COLUMNS or v == "-"):
                        found.append((DECLARING, r, ln, f"a cell holding {v} where its form does not give it: {header[c]}"))
                if len(row) != len(header):
                    found.append((DECLARING, r, ln, f"a row of {len(row)} cells under a header of {len(header)}"))
                    ok = False
        if not ok:
            continue
        check = {"State Machine": _machine, "Decision Table": _decision_table,
                 "Decision Tree": _tree, "DAG": _dag}.get(name)
        if name == "Decision Table":
            _decision_table(r, line, name, fields, tables, found, facts)
        elif name in ("Algorithm", "Constraint"):
            # its whole check runs across files, in algorithm_findings or constraint_findings
            continue
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
        elif key in LIST_FIELDS and inline and not (key in ("Inputs", "Output") and inline == "none"):
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


# ---------------------------------------------------------------- State Machine

def _machine(r, line, name, fields, tables, found):
    rule = f"{RULE} § {name}"
    states, transitions = tables
    # a Guard or an Effect column is written only where some cell of it is not none
    for col in ("Guard", "Effect"):
        if col in transitions["header"]:
            i = transitions["header"].index(col)
            if all(i < len(row) and row[i] == NONE_CELL for _, row in transitions["rows"]):
                found.append((rule, r, transitions["line"], f"a{'n' if col == 'Effect' else ''} {col} column every cell of which is none"))
    # a protocol machine runs no effect and takes no transition with no trigger
    if dict((k, v) for _, k, v in fields).get("Protocol") == "Yes":
        if "Effect" in transitions["header"]:
            found.append((rule, r, transitions["line"], "a protocol machine with an Effect column"))
        at = 1 if transitions["header"][:1] == ["Name"] else 0
        for ln, row in transitions["rows"]:
            if row[at + 2] == NONE_CELL:
                found.append((rule, r, ln, "a protocol machine's transition with no trigger"))
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
        for s in froms + tos:
            if s not in known:
                found.append((rule, r, ln, f"a From or To naming a state the States table does not hold: {s}"))
        if len(froms) > 1:
            joins.append((ln, frozenset(froms)))
        if len(tos) > 1:
            forks.append((ln, frozenset(tos)))
        for f in froms:
            outgoing.add(f)
            for t in tos:
                edges.append((f, t))
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


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine
# a guard's test of one fact, as a conjunct of its guard: a comparison, `in`, `between`, or a question alone or within
# `not(…)`; a value a literal FEEL writes, which the cell it becomes tests as itself
CONJUNCT = (
    ("cmp", re.compile(r'(?P<f>[^<>=!()"]+?)\s*(?P<op><=|>=|!=|<|>|=)\s*(?P<v>.+)')),
    ("in", re.compile(r'(?P<f>[^<>=!()"]+?) in (?P<v>[\[\]\(][^,]*\.\.[^,]*[\]\)\[])')),
    ("in", re.compile(r'(?P<f>[^<>=!()"]+?) in \((?P<v>.+)\)')),
    ("between", re.compile(r'(?P<f>[^<>=!()"]+?) between (?P<a>.+?) and (?P<b>.+)')),
    ("not", re.compile(r'not\((?P<f>[^<>=!()"]+)\)')),
    ("bare", re.compile(r'(?P<f>[^<>=!()"]+)')),
)
VALUE = re.compile(r'"[^"]*"|true|false|null')
# a guard of another of FEEL's forms, read and never decided: one test the checks set aside
GENERAL = ""


def _conjuncts(text):
    """A guard's conjuncts: split at each `and` outside quotes, brackets and braces, a `between`'s own `and` and the
    one in `date and time(…)` aside."""
    parts, cur, depth, quoted, between, i = [], "", 0, False, 0, 0
    while i < len(text):
        ch = text[i]
        if ch == '"':
            quoted = not quoted
        elif not quoted and ch in "[({":
            depth += 1
        elif not quoted and ch in "])}":
            depth -= 1
        if not quoted and depth == 0 and re.match(r'\bbetween\b', text[i:]) and (i == 0 or not text[i - 1].isalnum()):
            between += 1
        if not quoted and depth == 0 and text.startswith(" and ", i) and not text.startswith(" and time(", i):
            if between:
                between -= 1
            else:
                parts.append(cur.strip())
                cur, i = "", i + 5
                continue
        cur += ch
        i += 1
    return parts + [cur.strip()]


def _conjunct(part):
    """A conjunct -> (fact, its cell, whether it tests the fact as a boolean), or None where it is no test of one fact
    the checks read."""
    for kind, pattern in CONJUNCT:
        m = pattern.fullmatch(part)
        if not m:
            continue
        f = m["f"].strip()
        if not _is_name(f) or kept_words(f):
            return None
        if kind == "cmp":
            v, op = m["v"].strip(), m["op"]
            boolean = v in ("true", "false")
            if op == "=":
                cell = v if VALUE.fullmatch(v) or _value(v) else "= " + v
            elif op == "!=":
                cell = f"not({v})" if VALUE.fullmatch(v) or _value(v) else None
            else:
                cell = f"{op} {v}"
            return (f, cell, boolean) if cell else None
        if kind == "in":
            return f, m["v"].strip(), False
        if kind == "between":
            return f, f"[{m['a'].strip()}..{m['b'].strip()}]", False
        return f, "false" if kind == "not" else "true", True
    return None


def guard(text):
    """An exclusive choice's guard, a FEEL boolean expression -> {fact: cell} where it is a conjunction of tests of
    facts, each fact tested once, {GENERAL: a test set aside} for any other FEEL boolean, or None for one in no form
    FEEL has or giving no yes or no; `none` tests no fact."""
    if text.strip() == NONE_CELL:
        return {}
    kind, problems = expressions.check(text, {}, lambda n: True)
    if any("no form FEEL has" in p for p in problems) or kind not in (None, "boolean"):
        return None
    out = {}
    if _disjunctive(text):
        return {GENERAL: (False, [("sym", text, ())])}
    for part in _conjuncts(text):
        c = _conjunct(part)
        cell = feel(c[1]) if c else None
        if c is None or cell is None or c[0] in out:
            return {GENERAL: (False, [("sym", text, ())])}
        out[c[0]] = cell
    return out


def kept_words(name):
    """The words FEEL keeps that a name holds, which a fact a guard tests holds none of."""
    return [w for w in name.rstrip("?").split() if w in expressions.KEYWORDS]


def _disjunctive(text):
    """Whether a guard joins anything by `or` outside quotes, brackets and braces, and so is no conjunction."""
    depth, quoted = 0, False
    for i, ch in enumerate(text):
        if ch == '"':
            quoted = not quoted
        elif not quoted and ch in "[({":
            depth += 1
        elif not quoted and ch in "])}":
            depth -= 1
        elif not quoted and depth == 0 and text.startswith(" or ", i):
            return True
    return False


def kept_word_facts(text):
    """The facts a guard's conjuncts test whose names hold a word FEEL keeps."""
    out = []
    for part in _conjuncts(text) if text.strip() != NONE_CELL and not _disjunctive(text) else []:
        for _, pattern in CONJUNCT:
            m = pattern.fullmatch(part)
            if m and kept_words(m["f"].strip()) and _is_name(m["f"].strip()):
                out.append(m["f"].strip())
                break
    return out


def boolean_facts(text):
    """The facts a guard tests as booleans: alone, within `not(…)`, or against `true` or `false`."""
    if text.strip() == NONE_CELL or _disjunctive(text):
        return []
    return [c[0] for c in (_conjunct(p) for p in _conjuncts(text)) if c and c[2]]


def _choice_groups(transitions, off):
    """A machine's transitions by the state they leave and their trigger -> {(From, Trigger): [(line, guard)]}, a
    table with no Guard column guarding each transition by none."""
    gi = transitions["header"].index("Guard") if "Guard" in transitions["header"] else None
    groups = {}
    for ln, row in transitions["rows"]:
        trig = row[off + 2] or NONE_CELL
        groups.setdefault((row[off], trig), []).append((ln, row[gi] if gi is not None else NONE_CELL))
    return groups


def _choices(r, rule, transitions, off, found):
    """An exclusive choice: two or more transitions from one state on one trigger, or on none,
    whose guards, read as a Unique Decision Table over their facts where each is a conjunction of tests of facts,
    never both hold; the facts a guard compares a fact with are `guard_fact_findings`' across files."""
    groups = _choice_groups(transitions, off)
    for (frm, trig), rows in groups.items():
        if len(rows) < 2:
            continue
        parsed = []
        for ln, g in rows:
            p = guard(g)
            kept = kept_word_facts(g)
            for f in kept:
                found.append((rule, r, ln, f"a fact a guard tests whose name holds a word FEEL keeps: {f}"))
            for f in boolean_facts(g) if p is not None else ():
                if not QUESTION.fullmatch(f):
                    found.append((rule, r, ln, f"a boolean fact a guard tests whose name asks no question: {f}"))
            if p is None:
                if not kept:
                    found.append((rule, r, ln, f"an exclusive choice's guard in no form FEEL has, or giving no yes or no: {g}"))
            elif any(not symbolic(c) and not any(matches(c, x) for x in _points(c)) for c in p.values()):
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
                named = set(ga) | set(gb)
                if all(overlap(ga.get(f, feel("-")), gb.get(f, feel("-"))) for f in named):
                    found.append((rule, r, lb, f"two guards from {frm} on {trig} that can both hold"))


SUBMACHINE = "modeling-constructs.md § Constructs § State Machine § A Submachine State"
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State
# the words naming a state's governing machine, then its citations; and the guard naming the terminal state reached
GOVERNED = re.compile(r"governed by((?: *`[^`]+`(?:,? (?:and )?)?)*)", re.I)
EXIT = re.compile(r'exit = "([^"]+)"')


def _cell(row, i):
    return row[i] if i is not None and i < len(row) else NONE_CELL


def submachine_findings(text_of, found, sections, strip_fences, citation, resolve):
    """§ Constructs § State Machine § A Submachine State: what its form fixes. A state is governed by the State Machine
    its description names after the words `governed by`, which name a machine only, never a part of one, and never
    nothing; a description citing another machine's whole section names it so; one machine at most; no machine
    governing itself; no protocol machine's state governed; no governed state terminal; and a governed state left, of
    its transitions with no trigger, as its machine's exits have it. A transition with a trigger is UML's group
    Transition, which the form leaves free. `citation` and `resolve` are the citation check's own."""
    machines = {}
    for r, body in text_of.items():
        for line, name, fields, tables, lineage in declarations(strip_fences(body), sections(body)):
            if name == "State Machine" and len(tables) == 2:
                protocol = dict((k, v) for _, k, v in fields).get("Protocol") == "Yes"
                machines[(r, lineage)] = (protocol, tables)
    governs = {}
    for (r, lineage), (protocol, (states, transitions)) in machines.items():
        header = transitions["header"]
        off = 1 if header[:1] == ["Name"] else 0
        gi = header.index("Guard") if "Guard" in header else None
        rows = [(tl, t) for tl, t in transitions["rows"] if len(t) > off + 2]
        for ln, row in states["rows"]:
            if len(row) < 4:
                continue
            spans = [m.group(1) for m in GOVERNED.finditer(row[1])]
            if any(not citation.findall(s) for s in spans):
                found.append((SUBMACHINE, r, ln, f"the words governed by naming nothing: {row[0]}"))
            named = [c for s in spans for c in citation.findall(s)]
            for c in named:
                if "[" in c:
                    found.append((SUBMACHINE, r, ln, f"a part of a machine cited after the words governed by: {row[0]}"))
            keys = [resolve(c, r) for c in named if "[" not in c]
            for key in keys:
                if key not in machines:
                    found.append((SUBMACHINE, r, ln, f"the words governed by naming no State Machine: {row[0]}"))
            for c in citation.findall(row[1]):
                key = resolve(c, r)
                if "[" not in c and key in machines and key != (r, lineage) and c not in named:
                    found.append((SUBMACHINE, r, ln, f"a state citing a machine's whole section without the words governed by: {row[0]}"))
            governing = [key for key in keys if key in machines]
            if not governing:
                continue
            if protocol:
                found.append((SUBMACHINE, r, ln, f"a protocol machine's state governed by a machine: {row[0]}"))
            if len(set(governing)) > 1:
                found.append((SUBMACHINE, r, ln, f"a state governed by more than one machine: {row[0]}"))
            gov = governing[0]
            governs.setdefault((r, lineage), set()).add(gov)
            if row[3] == "Yes":
                found.append((SUBMACHINE, r, ln, f"a governed state that is terminal: {row[0]}"))
                continue
            exits = {s[0] for _, s in machines[gov][1][0]["rows"] if len(s) > 3 and s[3] == "Yes"}
            # its machine's end: the transitions with no trigger; one with a trigger is a group Transition
            ends = [(tl, t) for tl, t in rows if t[off] == row[0] and t[off + 2] == NONE_CELL]
            in_join = any(row[0] in t[off].split(" and ") for _, t in rows if " and " in t[off])
            # a machine with no terminal state is left on its triggers alone; one in a join's From, by the join alone
            if not exits or in_join:
                for tl, _ in ends:
                    why = "whose machine never ends" if not exits else "in a join's From"
                    found.append((SUBMACHINE, r, tl, f"a governed state {why}, left by a transition with no trigger: {row[0]}"))
                continue
            if len(exits) == 1:
                if len(ends) != 1 or _cell(ends[0][1], gi) != NONE_CELL:
                    found.append((SUBMACHINE, r, ln, f"a governed state whose machine has one terminal state, not left by one transition with no trigger and no guard: {row[0]}"))
                continue
            left = []
            for tl, t in ends:
                m = EXIT.fullmatch(_cell(t, gi))
                if not m or m.group(1) not in exits:
                    found.append((SUBMACHINE, r, tl, f"a transition from a governed state guarded by no terminal state of its machine: {_cell(t, gi)}"))
                else:
                    left.append(m.group(1))
            for x in sorted(exits - set(left)):
                found.append((SUBMACHINE, r, ln, f"a governed state left by no transition for its machine's terminal state: {x}"))
            for x in sorted({x for x in left if left.count(x) > 1}):
                found.append((SUBMACHINE, r, ln, f"a governed state left by two transitions for one terminal state: {x}"))
    # no machine governs itself, directly or through the machines it governs
    for start in governs:
        seen, todo = set(), list(governs[start])
        while todo:
            m = todo.pop()
            if m == start:
                found.append((SUBMACHINE, start[0], 1, f"a machine governing itself: § {start[1]}"))
                break
            if m not in seen:
                seen.add(m)
                todo.extend(governs.get(m, ()))


def effect_findings(text_of, found, sections, strip_fences, citation, resolve):
    """§ Constructs § State Machine: an Effect cell cites the Algorithm or the Decision Table its transition runs, or
    is `none`. `citation` and `resolve` are the citation check's own."""
    kinds = {}
    for r, body in text_of.items():
        for line, name, fields, tables, lineage in declarations(strip_fences(body), sections(body)):
            kinds[(r, lineage)] = name
    for r, body in text_of.items():
        for line, name, fields, tables, lineage in declarations(strip_fences(body), sections(body)):
            if name != "State Machine" or len(tables) != 2 or "Effect" not in tables[1]["header"]:
                continue
            e = tables[1]["header"].index("Effect")
            for ln, row in tables[1]["rows"]:
                cell = row[e].strip() if e < len(row) else ""
                if cell == NONE_CELL:
                    continue
                cites = citation.findall(cell)
                if (len(cites) != 1 or citation.sub("", cell).strip() or "[" in cites[0]
                        or kinds.get(resolve(cites[0], r)) not in ("Algorithm", "Decision Table")):
                    found.append((f"{RULE} § State Machine", r, ln, f"an Effect cell citing no Algorithm or Decision Table: {cell}"))


def guard_fact_findings(text_of, found, sections, strip_fences):
    """§ Constructs § State Machine: a fact an exclusive choice's guard compares a fact with, in a test the checks read,
    is one a guard of its choice tests, a Facts section of any file declares, or `exit`, of the kind of the fact it is
    compared with; a guard in any other of FEEL's forms is read."""
    declared = {}
    for r, body in text_of.items():
        live = strip_fences(body)
        for f, d in facts_of(fact_records(live, sections(body))).items():
            declared.setdefault(f, d)
    kind_of = {f: kind_of_type(t) for f, (t, _, _) in declared.items()}
    for r, body in text_of.items():
        for line, name, fields, tables, lineage in declarations(strip_fences(body), sections(body)):
            if name != "State Machine" or len(tables) != 2:
                continue
            off = 1 if tables[1]["header"][:1] == ["Name"] else 0
            for rows in _choice_groups(tables[1], off).values():
                if len(rows) < 2:
                    continue
                parsed = [(ln, guard(g) or {}) for ln, g in rows]
                tested = {f for _, p in parsed for f in p}
                seen = {}
                for _, p in parsed:
                    for f, c in p.items():
                        seen.setdefault(f, set()).update(_kind(c))
                kinds = dict(kind_of)
                kinds.update({f: next(iter(ks)) for f, ks in seen.items() if f not in kind_of and len(ks) == 1})
                scope = {f: kinds.get(f) for f in tested | set(declared) | {"exit"}}
                for ln, p in parsed:
                    for fact, c in p.items():
                        if fact == GENERAL:
                            continue
                        for t in c[1]:
                            if t[0] == "sym" and not t[2]:
                                # a test in another of FEEL's forms: each name it holds in scope
                                for m in expressions.check_tests(t[1], scope):
                                    found.append((f"{RULE} § State Machine", r, ln, f"{m}, in a guard testing {fact}"))
                        for f in {f for t in c[1] if t[0] == "sym" for f in t[2]}:
                            if f not in tested and f not in declared:
                                found.append((f"{RULE} § State Machine", r, ln, f"a guard comparing a fact with one no guard of its choice tests and no Facts record declares: {f}"))
                            elif kinds.get(f) and kinds.get(fact) and kinds[f] != kinds[fact]:
                                found.append((f"{RULE} § State Machine", r, ln, f"a guard comparing a {kinds[fact]} fact with a {kinds[f]} one: {f}"))


def recorded_in_findings(text_of, found, sections, strip_fences, citation, resolve):
    """§ Constructs § State Machine: a Recorded In field names the fact the entity records its state in, a fact's name,
    a colon and the citation of the Facts record declaring it, whose Values, a quoted list, hold each state's name.
    `citation` and `resolve` are the citation check's own."""
    rule = f"{RULE} § State Machine"
    records = {}
    for r, body in text_of.items():
        live, secs = strip_fences(body), sections(body)
        for lineage, span in secs.items():
            if lineage.rsplit(" § ", 1)[-1] == "Facts":
                for _, name, d in fact_records(live, {lineage: span}):
                    records[(r, lineage, name)] = d.get("Values", "none")
    for r, body in text_of.items():
        for line, name, fields, tables, lineage in declarations(strip_fences(body), sections(body)):
            value = dict((k, v) for _, k, v in fields).get("Recorded In")
            if name != "State Machine" or len(tables) != 2 or value in (None, "none"):
                continue
            mm, cites = READS_ITEM.fullmatch(value.strip()), citation.findall(value)
            named = re.search(r'\[Name: ([^\]]+)\]', value)
            if not mm or len(cites) != 1 or not named or named.group(1).strip() != mm.group(1).strip():
                found.append((rule, r, line, f"a Recorded In field that is not a fact's name, a colon and the citation of its Facts record: {value}"))
                continue
            path, section = resolve(cites[0], r)
            values = records.get((path, section, mm.group(1).strip()))
            if values is None:
                found.append((rule, r, line, f"a Recorded In field citing no Facts record: {value}"))
                continue
            listed = quoted_values(values)
            if listed is None:
                found.append((rule, r, line, f"a Recorded In field citing a Facts record whose Values are no quoted list: {value}"))
                continue
            for ln, row in tables[0]["rows"]:
                if row and row[0] not in listed:
                    found.append((rule, r, ln, f"a state not among the Values of the fact its machine is recorded in: {row[0]}"))


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


def kind_of_type(name):
    """A Facts record's Type -> the kind its values are, a cell's or an expression's; None where it names none."""
    if name in TYPE_KINDS:
        return TYPE_KINDS[name]
    try:
        return expressions.parse_type(name)
    except expressions.FeelError:
        return None


def multi_hit(policy):
    """Whether a hit policy takes the outcome of every row a case matches: Rule order, Output order, a Collect."""
    return policy in ("Rule order", "Output order") or policy.startswith("Collect")


def computing(header):
    """Whether a condition's header computes the value its column tests, a question never doing so."""
    return not header.endswith("?") and bool(expressions.COMPUTING.search(header))


def _outcome(v):
    """An outcome cell's value, a word quoted or plain alike; a quoted value that would read as another kind
    plain, `"5"`, stays quoted, a word and not that value."""
    if re.fullmatch(r'"[^"]*"', v) and _value(v[1:-1]) is None and v[1:-1] not in ("null", "-", "true", "false"):
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
        if d.get("Type") and d["Type"] not in TYPE_KINDS:
            try:
                expressions.parse_type(d["Type"])
            except expressions.FeelError as e:
                out.append((line, f"a Facts record's Type that is no type FEEL names: {name}: {e}"))
        places = d.get("Decimal Places", "none")
        if places != "none" and not (re.fullmatch(r'\d+', places) or places in {n for _, n, _ in records}):
            out.append((line, f"a Facts record's Decimal Places that is neither a whole number nor a fact its file declares: {name}"))
        if places != "none" and d.get("Type") != "number" and not re.search(r'->\s*number$', d.get("Type", "")):
            out.append((line, f"a Facts record's Decimal Places on a fact that is neither a number nor a function giving one: {name}"))
        derivation = d.get("Derivation", "none")
        if derivation != "none" and not d.get("Type", "").startswith("function"):
            out.append((line, f"a Facts record's Derivation on a fact that is no function: {name}"))
        elif derivation != "none":
            # judged with the file's facts in scope, its parameters bound by the function itself
            kind, problems = expressions.check(derivation, {n: kind_of_type(dd.get("Type", "")) for _, n, dd in records})
            if not derivation.startswith("function(") or kind != "function":
                out.append((line, f"a Facts record's Derivation in no form of a FEEL function: {name}"))
            for problem in problems:
                out.append((line, f"a Facts record's Derivation: {name}: {problem}"))
        initial = d.get("Initial Value", "none")
        if initial != "none":
            kind, problems = expressions.check(initial, {n: kind_of_type(dd.get("Type", "")) for _, n, dd in records})
            for problem in problems:
                out.append((line, f"a Facts record's Initial Value: {name}: {problem}"))
            if not problems and _differs(kind, kind_of_type(d.get("Type", ""))):
                out.append((line, f"a Facts record's Initial Value of another kind than its Type: {name}"))
        if name.split() and name.split()[0] in expressions.KEYWORDS:
            out.append((line, f"a fact's name opening with a word FEEL keeps: {name}"))

        out += [(line, m) for m in _value_list_problems(d.get("Values", "none"), f"the Facts record {name}'s Values")]
    return out


def _value_list_problems(text, what):
    """A value list, a Facts record's Values or an Input Values item, as FEEL's unary tests naming no fact -> [message],
    each problem once: a word written plain, which a list never holds, a name, and any other form FEEL does not have."""
    if text == "none":
        return []
    if not text.strip():
        return [f"{what} empty"]
    tests = _tests(text.strip())
    if not QUOTED_LIST.fullmatch(text) and tests == [("is", text.strip(), "word")]:
        return [f"{what} written plain, which a value list never is: {text}"]
    out = []
    for p in dict.fromkeys(expressions.check_tests(text, {})):
        name = re.match(r"a name no fact declares: (.+)", p)
        out.append(f"{what} naming a fact: {name.group(1)}" if name else f"{what} in no form FEEL's unary tests have: {p}")
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
    """Each condition's values: its Input Values item, a question's `true` and `false`, or its Facts record's Values,
    `null` among them where its fact may be absent -> {header: cell}."""
    given = values.get("Input Values", "")
    # an item in a form the checks do not read gives its column no values, so its coverage is read
    domains = {h: d for h, d in _named(given).items() if not symbolic(d)}
    for k in idx:
        h = header[k]
        if h.endswith("?"):
            domains[h] = (False, [("is", "true", "boolean"), ("is", "false", "boolean")])
        if h in facts:
            _, fvalues, absent = facts[h]
            dom = domains.get(h) or (feel(fvalues) if fvalues != "none" else None)
            if dom and symbolic(dom):
                dom = None  # Values naming a fact, or in a form the checks do not read, give the column none
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
        if not mm or not _is_name(mm.group(1).strip()):
            found.append((rule, r, line, f"a Reads item that is not a name, a colon and a citation: {item}"))
        elif named and named.group(1).strip() != mm.group(1).strip():
            found.append((rule, r, line, f"a Reads item named otherwise than the Facts record it cites: {item}"))
        else:
            reads.append(mm.group(1).strip())
    typed = {f: kind_of_type(t) for f, (t, _, _) in facts.items()}
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
            elif header[k] not in computed and header[k].endswith("?") and row[k] not in ("true", "false", "null"):
                found.append((rule, r, ln, f"a question's outcome cell neither true, false nor null: {row[k][:20]}"))
    cells = {}
    for ln, row in table["rows"]:
        for k in idx:
            cells[(ln, k)] = feel(row[k])
            if cells[(ln, k)] is None:
                found.append((rule, r, ln, f"a cell in no form FEEL has: {row[k]}"))
            else:
                for t in cells[(ln, k)][1]:
                    if t[0] == "eqv":
                        found.append((rule, r, ln, f"a value tested after `=`, which a cell writes alone: {t[1]}"))
                    if t[0] == "sym" and not t[2]:
                        for p in expressions.check_tests(t[1], known):
                            found.append((rule, r, ln, f"{p}, in the cell {row[k]}"))
                    for fact in (t[2] if t[0] == "sym" else ()):
                        if fact not in known:
                            found.append((rule, r, ln, f"a cell naming a fact no condition, Reads item or Facts record declares: {fact}"))
    if None in cells.values():
        return
    if values.get("Input Values", "none") != "none":
        for item in values["Input Values"].split("\n"):
            h, _, c = item.partition(":")
            problems = _value_list_problems(c.strip(), f"the Input Values item {h.strip()}") if h.strip() else [f"an Input Values item with no header: {item}"]
            for m in problems:
                found.append((rule, r, line, m))
            if problems:
                continue
            if h.strip() in facts:
                found.append((rule, r, line, f"Input Values given for a fact its Facts record declares: {h.strip()}"))
            elif h.strip().endswith("?"):
                found.append((rule, r, line, f"Input Values given for a question, whose values are true and false: {h.strip()}"))
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
            got = _kind(c)
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

# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Algorithm
# a step's forms, as the section writes them: a run's head, a loop over a list and its orders, and an End followed by
# words, a result named in the End rather than set
RUN_HEAD = re.compile(r'Run (?P<cite>`[^`]+`)(?P<rest>.*)')
FOR_EACH = re.compile(r'For each (?P<rest>.+): steps (?P<n>\d+) to (?P<m>\d+)')
GATHERING = re.compile(r'(?P<rest>.+), gathering (?P<fact>.+?) into (?P<into>.+)')
ORDER_KEY = re.compile(r'by (?P<expr>.+?) (?P<way>ascending|descending)')
ANY_ORDER, LEFT_OPEN, AT_ONCE = "in any order", "in an order the system leaves open", "at once"
END_WITH = re.compile(r'(?:^|[,.;] )' + END_WORD + r'\s+\w')
CONTINUE_WORD = "continue"
PART = re.compile(r'(?P<fact>[^.]+?)(?:\.(?P<path>.+))?')
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
# the rounding modes, as DMN's rounding functions name them
ROUNDING_MODES = ("half even", "half up", "half down", "up", "down", "ceiling", "floor")


def _names_in(text, declared=()):
    """The names a FEEL expression reads, its functions and the names it binds aside: each declared fact it holds,
    and each other name, read with the declared facts in scope, so a declared name holding a word FEEL keeps reads
    whole."""
    seen = []
    expressions.check(text, {n: None for n in declared}, lambda n: seen.append(n) or True, seen)
    return list(dict.fromkeys(seen))


def _set(body, names=None):
    """A computation -> (its fact, the part's path or None, its expression), split at the ` to ` whose sides read as
    a fact or its part and a FEEL expression; None for no computation in its form."""
    if not body.startswith("Set "):
        return None
    text = body[4:]
    found = []
    for m in re.finditer(r'(?= to )', text):
        lhs, rhs = text[:m.start()].strip(), text[m.start() + 4:].strip()
        part = PART.fullmatch(lhs)
        name = part["fact"].strip() if part else ""
        if _is_name(name) and rhs and _feel(rhs):
            found.append((name, part["path"], rhs))
    if names is not None:
        found.sort(key=lambda s: any("no fact declares" in p for p in expressions.check(s[2], dict(names))[1]))
    return found[0] if found else None


def _run(raw):
    """A run as written, its citation kept -> (citation, [each `with` item], [each item it gives]), the items as
    written, bound to the construct run's own names by `_bind`; None for no run in its form."""
    m = RUN_HEAD.fullmatch(raw.strip())
    if not m:
        return None
    rest, gives = m["rest"], []
    g = rest.rfind(", giving ")
    if g >= 0:
        gives = [x.strip() for x in rest[g + len(", giving "):].split(",")]
        rest = rest[:g]
    withs = []
    if rest.strip():
        if not rest.startswith(" with "):
            return None
        withs = [x.strip() for x in rest[len(" with "):].split(", with ")]
    return m["cite"], withs, gives


def _bind(item, names, argument):
    """A run's `with` item, `{input} as {expression}`, or what it gives, `{output}` or `{output} as {fact}` ->
    (the construct's name, the expression or the fact), split at the ` as ` whose left side is a name the construct
    run has, else at the first whose left side is a name and whose right side is FEEL or a name; None where none
    is."""
    if not argument and item in names:
        return item, item
    cuts = [(item[:m.start()].strip(), item[m.start() + 4:].strip()) for m in re.finditer(r'(?= as )', item)]
    fits = [(a, b) for a, b in cuts if _is_name(a) and b and (_feel(b) if argument else _is_name(b))]
    for a, b in fits:
        if a in names:
            return a, b
    if fits:
        return fits[0]
    return None if argument or not _is_name(item) else (item, item)


def _for_each(text, names=None):
    """A loop over a list -> {item, list, order, fact, into, n, m}, split at the ` of ` whose left side is a name and
    whose list is FEEL, preferring, where the names known are given, the cut whose list reads with no name unknown;
    None for no loop in its form."""
    m = FOR_EACH.fullmatch(text)
    if not m:
        return None
    whole = m["rest"]
    cuts = list(reversed([k.start() for k in re.finditer(r' of ', whole)]))
    if names is not None:
        def resolves(cut):
            lst = whole[cut + 4:].split(", by ")[0].split(", gathering ")[0].split(", in ")[0].split(", at once")[0]
            return not any("no fact declares" in p for p in expressions.check(lst, dict(names))[1])
        cuts = [c for c in cuts if resolves(c)] + [c for c in cuts if not resolves(c)]
    for cut in cuts:
        item, rest, fact, into = whole[:cut].strip(), whole[cut + 4:], None, None
        g = GATHERING.fullmatch(rest)
        if g:
            rest, fact, into = g["rest"], g["fact"].strip(), g["into"].strip()
        order = next((o for o in (ANY_ORDER, LEFT_OPEN, AT_ONCE) if rest.endswith(", " + o)), None)
        if order:
            lst = rest[:-len(order) - 2].strip()
        else:
            k = rest.find(", by ")
            lst, order = (rest.strip(), None) if k < 0 else (rest[:k].strip(), rest[k + 2:].strip())
        if _is_name(item) and _feel(lst):
            return dict(item=item, list=lst, order=order, fact=fact, into=into, n=int(m["n"]), m=int(m["m"]))
    return None


def _expression(rule, r, ln, text, known, found, bound=None):
    """A FEEL expression a step writes, judged with the facts the step may name in scope -> its kind."""
    names = dict(known)
    names.update(bound or {})
    kind, problems = expressions.check(text, names)
    for p in problems:
        found.append((rule, r, ln, f"{p}: {text}"))
    return kind


def _kind_name(kind):
    """A kind's name, a Facts record's `word` being FEEL's `string`."""
    name = kind if isinstance(kind, str) else kind[0] if isinstance(kind, tuple) else None
    return "string" if name == "word" else name


def _differs(a, b):
    """Whether two kinds, each known, differ: a list from a context, a number from a string, and so on."""
    x, y = _kind_name(a), _kind_name(b)
    return x is not None and y is not None and x not in ("function", "fn") and y not in ("function", "fn") and x != y


def _parts(text):
    """A step's text, its code spans blanked -> (its condition or None, [(each branch, where it starts)]). A
    comparison's condition is the longest text before a comma that FEEL reads as an expression."""
    if not text.startswith(COMPARISON_OPENING) or text.count(SEPARATOR_OF_BRANCHES) != 1:
        return None, [(text, 0)]
    head, second = text[len(COMPARISON_OPENING):].split(SEPARATOR_OF_BRANCHES)
    start = len(COMPARISON_OPENING)
    second_at = start + len(head) + len(SEPARATOR_OF_BRANCHES)
    cuts = [i for i in range(len(head)) if head.startswith(", ", i)]
    for i in reversed(cuts):
        if _feel(head[:i]):
            return head[:i], [(head[i + 2:], start + i + 2), (second, second_at)]
    if cuts:
        return head[:cuts[0]], [(head[cuts[0] + 2:], start + cuts[0] + 2), (second, second_at)]
    return head, [("", start + len(head)), (second, second_at)]


def _clause(branch, at):
    """A branch and where it starts -> (what it does, where that starts, how it ends: ('jump', n), ('end',) or
    ('next',))."""
    lead = len(branch) - len(branch.lstrip())
    text = branch.strip().rstrip(".")
    js = [j for j in jumps(text) if j[1]]
    if js and _ends_in_jump(text):
        body, end = text[:js[-1][2]], ("jump", js[-1][1])
    elif END_AT_TAIL.search(text):
        body, end = text[:len(text) - len(END_WORD)], ("end",)
    else:
        body, end = text, ("next",)
    body = body.strip().rstrip(",.").strip()
    body = re.sub(r'(?:,| and)\s*' + CONTINUE_WORD + r'$', "", body).strip()
    return ("" if body == CONTINUE_WORD else body), at + lead, end


def table_ready(table):
    """Whether an Algorithm's table is one its steps can be read from: headed Step and Action, each row as wide as its
    header; any other is reported by the checks of its form, each file's own."""
    header = table["header"]
    return header[:2] == ["Step", "Action"] and all(len(row) == len(header) for _, row in table["rows"])


def steps_of(table):
    """An Algorithm's table, numbered from 1 in order -> [(line, step, its text with code spans blanked, as written,
    condition, [(branch, body, body as written, end)])]."""
    out = []
    for k, (ln, row) in enumerate(table["rows"], 1):
        form, raw = _form_of(row[1]), row[1]
        cond, branches = _parts(form)
        done = []
        for b, at in branches:
            body, start, end = _clause(b, at)
            done.append((b, body, raw[start:start + len(body)], end))
        out.append((ln, k, form, raw, cond, done))
    return out


def io_items(values, key):
    """An Algorithm's Inputs or Output -> [(the item as written, the fact's name)], an Inputs item naming the record
    of another file read for its name."""
    out = []
    for item in [] if values.get(key, "none") == "none" else values[key].split("\n"):
        mm = READS_ITEM.fullmatch(item.strip())
        out.append((item.strip(), (mm.group(1) if mm and key == "Inputs" else item).strip()))
    return out


def _step_sets(form, done, bind, names=None):
    """What one step sets -> [(fact, kind, how)]: a computation's fact, its path None where it sets the whole fact; a
    run's given facts; a loop's gathered list. The one reading of setting the checks share."""
    out = []
    loop = _for_each(form.strip().rstrip("."), names)
    if loop and loop["into"]:
        out.append((loop["into"], None, "gathered"))
    for _, body, raw, _ in done:
        s, b = _set(body, names), bind(raw)
        if s:
            out.append((s[0], None, "computed" if s[1] is None else "part"))
        if b:
            out += [(fact, kind, "given") for _, fact, kind in b["gives"]]
    return out


def _known_names(values, steps, facts, bind):
    """The facts an Algorithm knows outside its loops -> {name: kind}: its Inputs and its Output, its file's facts,
    and each fact a step sets whole, a run gives or a loop gathers."""
    base = {f: kind_of_type(t) for f, (t, _, _) in (facts or {}).items()}
    for key in ("Inputs", "Output"):
        for _, n in io_items(values, key):
            base.setdefault(n, None)
    # each split read again with the names the last reading found, until the names hold, so a fact whose name holds
    # ` to ` is known by the cut whose names resolve
    names = None
    for _ in range(len(steps) + 2):
        known = dict(base)
        for _, _, form, _, _, done in steps:
            for fact, kind, how in _step_sets(form, done, bind, names):
                if how != "part":
                    known.setdefault(fact, kind)
        if names is not None and set(known) == set(names):
            break
        names = known
    return known


def _algorithm(rule, r, line, values, table, steps, facts, bind, found):
    """An Algorithm's own checks, its runs bound by `bind` (a run as written -> its target and bindings, or None)
    -> {step: whether it goes back}."""
    rows = table["rows"]
    for key in ("Inputs", "Output"):
        for item, n in io_items(values, key):
            if not _is_name(n):
                found.append((rule, r, line, f"an Inputs item that is neither a fact's name nor a name, a colon and a citation: {item}"
                              if key == "Inputs" else f"an Output item that is not a fact's name: {item}"))
    known = _known_names(values, steps, facts, bind)
    # each Output fact set on its paths, one its Inputs also name holding, where none sets it, what it was given
    made = {fact for _, _, form, _, _, done in steps for fact, _, _ in _step_sets(form, done, bind, known)}
    inputs = {n for _, n in io_items(values, "Inputs")}
    for item, n in io_items(values, "Output"):
        if n not in made and n not in inputs:
            found.append((rule, r, line, f"an Output fact nothing sets: {item}"))
    loops = [(step, _for_each(form.strip().rstrip("."), known)) for _, step, form, _, _, _ in steps]
    loops = [(step, lp) for step, lp in loops if lp]
    # each loop's body: the steps after it, to its last, inside any loop holding it, never the table's last step
    for step, lp in loops:
        if lp["n"] != step + 1 or lp["m"] < lp["n"] or lp["m"] >= len(rows):
            found.append((rule, r, steps[step - 1][0], f"a loop's body not the steps after it, ending before the last step: step {step}"))
    for a, la in loops:
        for b, lb in loops:
            if a < b <= la["m"] < lb["m"]:
                found.append((rule, r, steps[b - 1][0], f"a loop's body reaching past the body holding it: step {b}"))
    # each loop's item, judged outermost first with the items of the loops holding it in scope
    items = {}

    def scope_at(step):
        s = dict(known)
        for lstep, lp in loops:
            if lp["n"] <= step <= lp["m"] and lstep in items:
                s[items[lstep][0]] = items[lstep][1]
        return s
    for step, lp in loops:
        ln = steps[step - 1][0]
        kind = _expression(rule, r, ln, lp["list"], scope_at(step), found)
        if kind is not None and not (isinstance(kind, tuple) and kind[0] == "list"):
            found.append((rule, r, ln, f"a loop over what is no list: {lp['list']}"))
        items[step] = (lp["item"], kind[1] if isinstance(kind, tuple) and kind[0] == "list" else None)
        if lp["into"] and known.get(lp["into"]) is not None and _kind_name(known[lp["into"]]) != "list":
            found.append((rule, r, ln, f"a loop gathering into a fact that holds no list: {lp['into']}"))
        if lp["order"] is None or lp["order"] not in (ANY_ORDER, LEFT_OPEN, AT_ONCE) and not all(
                ORDER_KEY.fullmatch(k.strip()) for k in lp["order"].split(", then ")):
            found.append((rule, r, ln, f"a loop's order not written `by` an expression and `ascending` or `descending`, `{ANY_ORDER}`, `{LEFT_OPEN}` or `{AT_ONCE}`: step {step}"))
        elif lp["order"] not in (ANY_ORDER, LEFT_OPEN, AT_ONCE):
            for k in lp["order"].split(", then "):
                _expression(rule, r, ln, ORDER_KEY.fullmatch(k.strip())["expr"], scope_at(step), found, {lp["item"]: items[step][1]})
        # a pass at once sets only its item and what it gathers: by a computation, a run or a loop it holds
        if lp["order"] == AT_ONCE:
            for ln2, s2, form2, _, _, done in steps[lp["n"] - 1:lp["m"]]:
                for f in [fact for fact, _, _ in _step_sets(form2, done, bind, known)]:
                    if f not in (lp["item"], lp["fact"]):
                        found.append((rule, r, ln2, f"a pass at once setting a fact other than its item and what it gathers: {f}"))
    back_at = {}
    for ln, step, form, raw, cond, done in steps:
        scope = scope_at(step)
        comparison = form.startswith(COMPARISON_OPENING)
        if comparison and form.count(SEPARATOR_OF_BRANCHES) != 1:
            found.append((rule, r, ln, f"a comparison not written in its form: step {step}"))
            back_at[step] = False
            continue
        _jump_form(rule, r, ln, form, raw, found)
        if not comparison and SEPARATOR_MARK in form:
            found.append((rule, r, ln, f"a comparison's `{SEPARATOR_MARK}` in a step that is no comparison: step {step}"))
        loop = _for_each(form.strip().rstrip("."), known)
        if not loop and form.startswith("For each"):
            found.append((rule, r, ln, f"a loop over a list not written in its form: step {step}"))
            back_at[step] = False
            continue
        if comparison:
            kind = _expression(rule, r, ln, cond, scope, found)
            if kind is not None and kind != "boolean":
                found.append((rule, r, ln, f"a comparison's condition giving no yes or no: {cond}"))
        for b, body, braw, end in done:
            tail = b.rstrip(". ")
            if any(j[1] for j in jumps(b)) and not _ends_in_jump(b) or END.search(b) and not END_AT_TAIL.search(tail):
                found.append((rule, r, ln, f"a jump or an End that does not end its branch: step {step}"))
            # an End with words after it, outside a computation's or a run's own FEEL
            if not body.startswith(("Set ", "Run ")) and END_WITH.search(b):
                found.append((rule, r, ln, f"an End with words after it, a result set before it instead: step {step}"))
            if comparison and body.startswith("For each"):
                found.append((rule, r, ln, f"a loop folded into a comparison's branch: step {step}"))
            elif not loop:
                _action(rule, r, ln, step, body, braw, scope, bind, found)
        # a value a condition chooses: one computation, FEEL's if then else
        if comparison:
            sets = [_set(body, known) for _, body, _, _ in done]
            bodies = [body for _, body, _, _ in done]
            ends = [end for _, _, _, end in done]
            facts_set = {s[0] for s in sets if s}
            only_set = all(s or not body for s, body in zip(sets, bodies)) and len(facts_set) == 1
            if only_set and ends[0] == ends[1]:
                found.append((rule, r, ln, f"a comparison whose only work is setting one fact, an if then else: step {step}"))
        for target in [j[1] for j in jumps(form) if j[1]]:
            if not target.isdigit() or not 1 <= int(target) <= len(rows):
                found.append((rule, r, ln, f"a jump to a step the table does not hold: {target}"))
                continue
            t = int(target)
            if t <= step and not comparison:
                found.append((rule, r, ln, f"a step that is no comparison going back: step {step}"))
            for _, lp in loops:
                if lp["n"] <= step <= lp["m"] and not lp["n"] <= t <= lp["m"]:
                    found.append((rule, r, ln, f"a jump out of a loop's body: step {step} to step {t}"))
                elif lp["n"] <= t <= lp["m"] and not lp["n"] <= step <= lp["m"]:
                    found.append((rule, r, ln, f"a jump into a loop's body from outside it: step {step} to step {t}"))
        back = [b for b, _, _, _ in done if any(j[1] and j[1].isdigit() and int(j[1]) <= step for j in jumps(b))]
        if comparison and back and len(back) == len(done):
            found.append((rule, r, ln, f"a comparison going back on every branch, with none going forward: step {step}"))
        back_at[step] = bool(back)
        if step == len(rows):
            for b, _, _, _ in done:
                if not (b.rstrip(". ").endswith(END_WORD) or jumps(b)):
                    found.append((rule, r, ln, "a last step, or a branch of it, that neither ends nor jumps"))
    return back_at, scope_at


def _action(rule, r, ln, step, body, raw, known, bind, found):
    """A branch's or a step's action: a computation, a run, work in words, or nothing; a value written to a fact, a
    part or an Input of the kind it holds."""
    if not body:
        return
    if body.startswith("Set "):
        s = _set(body, known)
        if not s:
            found.append((rule, r, ln, f"a computation not written `Set` a fact or its part `to` a FEEL expression: step {step}"))
            return
        target_kind = known.get(s[0])
        if s[1]:
            # a part set by FEEL's context put: each step of its path a name, none of them reaching through a list
            steps_of_path = s[1].split(".")
            if not all(_is_name(p.strip()) for p in steps_of_path):
                found.append((rule, r, ln, f"a part set by a path that is not names joined by `.`: {s[0]}.{s[1]}"))
                target_kind = None
            elif any(_kind_name(expressions.check(".".join([s[0]] + steps_of_path[:k]), known)[0]) == "list"
                     for k in range(len(steps_of_path))):
                found.append((rule, r, ln, f"a part set through a list, which FEEL's context put does not reach: {s[0]}.{s[1]}"))
                target_kind = None
            else:
                target_kind = _expression(rule, r, ln, f"{s[0]}.{s[1]}", known, found)
        kind = _expression(rule, r, ln, s[2], known, found)
        if _differs(kind, target_kind):
            found.append((rule, r, ln, f"a value of another kind than the fact or part it is written to: step {step}"))
    elif re.match(r'(?i)set\b', body):
        found.append((rule, r, ln, f"a computation not written `Set` a fact or its part `to` a FEEL expression: step {step}"))
    elif body.startswith("Run "):
        b = bind(raw)
        if not b:
            found.append((rule, r, ln, f"a run not written `Run`, a citation, its arguments and the facts it gives: step {step}"))
            return
        for name, expr, kind_wanted in b["withs"]:
            kind = _expression(rule, r, ln, expr, known, found)
            if _differs(kind, kind_wanted):
                found.append((rule, r, ln, f"an argument of another kind than the Input it gives: {name}"))


def algorithm_findings(text_of, found, sections, strip_fences, citation, resolve):
    """§ Constructs § Algorithm, each Algorithm checked whole, once, across files: its own forms, by `_algorithm`; a
    Runs When citing each construct that runs it, and no other; work running no construct; a run citing an Algorithm
    or a Decision Table, its arguments naming what that construct takes, each one it takes given or known, and giving
    only what it gives; and a Terminates cell where a step goes back or a run recurs, and only there, judged on one
    graph of what runs what. `citation` and `resolve` are the citation check's own."""
    rule = f"{RULE} § Algorithm"
    decls, facts_in, places = {}, {}, set()
    for r, body in text_of.items():
        live, secs = strip_fences(body), sections(body)
        places.update((r, lineage) for lineage in secs)
        facts_in[r] = facts_of(fact_records(live, secs))
        for line, name, fields, tables, lineage in declarations(live, secs):
            decls[(r, lineage)] = (line, name, dict((k, v) for _, k, v in fields), tables)

    def kinds_in(r, names):
        return {n: kind_of_type(facts_in.get(r, {})[n][0]) if n in facts_in.get(r, {}) else None for n in names}

    def computed_columns(values, table):
        return [c.strip() for c in values.get("Computed", "").split(",") if c.strip() and c.strip() in table["header"]]

    def takes(key):
        """The facts a construct run takes and those it gives -> ({name: kind}, {name: kind}): an Algorithm's Inputs
        and Output; a Decision Table's conditions, the facts its computed headers and cells name, and its Reads, and its
        outcomes."""
        r = key[0]
        _, name, values, tables = decls[key]
        if name == "Algorithm":
            return (kinds_in(r, [n for _, n in io_items(values, "Inputs")]),
                    kinds_in(r, [n for _, n in io_items(values, "Output")]))
        header = tables[0]["header"] if tables else []
        conds = [c.strip() for c in values.get("Conditions", "").split(",") if c.strip()]
        notes = {c.strip() for c in values.get("Annotations", "").split(",") if c.strip()}
        wanted = []
        for c in conds:
            wanted += _names_in(c, facts_in.get(r, {})) if computing(c) else [c]
        for col in computed_columns(values, tables[0]) if tables else []:
            i = header.index(col)
            for _, row in tables[0]["rows"]:
                if i < len(row) and row[i].strip() not in ("-", ""):
                    wanted += _names_in(row[i], facts_in.get(r, {}))
        for item in [] if values.get("Reads", "none") == "none" else values["Reads"].split("\n"):
            mm = READS_ITEM.fullmatch(item.strip())
            wanted.append((mm.group(1) if mm else item).strip())
        gives = [h for h in header if h not in conds and h not in notes and h != "Name"]
        # a function fact the table's cells call is the table's own, never an input its run is given
        taken = {n: k for n, k in kinds_in(r, list(dict.fromkeys(wanted))).items() if _kind_name(k) != "function"}
        return taken, kinds_in(r, gives)

    def bind_in(r):
        def bind(raw):
            run = _run(raw)
            if not run:
                return None
            key = resolve(run[0].strip("`"), r)
            target = decls.get(key)
            out = dict(cite=run[0], key=key, kind=target[1] if target else None, withs=[], gives=[], unbound=[])
            if not target or target[1] not in ("Algorithm", "Decision Table"):
                out["gives"] = [(g, g, None) for g in run[2]]
                return out
            ins, outs = takes(key)
            for item in run[1]:
                b = _bind(item, ins, True)
                if b:
                    out["withs"].append((b[0], b[1], ins.get(b[0])))
                else:
                    out["unbound"].append(item)
            for item in run[2]:
                b = _bind(item, outs, False) or (item, item)
                out["gives"].append((b[0], b[1], outs.get(b[0])))
            return out
        return bind

    # every Algorithm's steps, read once
    algos, unread = {}, set()
    for key, (line, name, values, tables) in decls.items():
        if name == "Algorithm" and (not tables or not table_ready(tables[0])):
            unread.add(key)
        if name != "Algorithm" or not tables or not table_ready(tables[0]):
            continue
        rows = tables[0]["rows"]
        if [row[0] for _, row in rows] != [str(n) for n in range(1, len(rows) + 1)]:
            found.append((rule, key[0], tables[0]["line"], "steps not numbered from 1 in order"))
            unread.add(key)
            continue
        algos[key] = steps_of(tables[0])

    # what runs what: an Algorithm's run of a construct, a Decision Table's computed cell citing one; and the
    # constructs running an Algorithm: those, a State Machine's Effect and a state's work
    edges, runners = {}, {}
    for key, steps in algos.items():
        bind = bind_in(key[0])
        for _, step, _, _, _, done in steps:
            for _, body, braw, _ in done:
                b = bind(braw) if body.startswith("Run ") else None
                if b and b["kind"] in ("Algorithm", "Decision Table"):
                    edges.setdefault(key, set()).add(b["key"])
                    if b["key"] != key:
                        runners.setdefault(b["key"], set()).add(key)
    for key, (line, name, values, tables) in decls.items():
        cells = []
        if name == "State Machine" and len(tables) == 2:
            if "description" in tables[0]["header"]:
                d = tables[0]["header"].index("description")
                cells += [row[d] for _, row in tables[0]["rows"] if d < len(row)]
            if "Effect" in tables[1]["header"]:
                e = tables[1]["header"].index("Effect")
                cells += [row[e] for _, row in tables[1]["rows"] if e < len(row)]
        elif name == "Decision Table" and tables:
            for col in computed_columns(values, tables[0]):
                i = tables[0]["header"].index(col)
                cells += [row[i] for _, row in tables[0]["rows"] if i < len(row)]
        for cell in cells:
            for c in citation.findall(cell):
                if "[" in c:
                    continue
                target = resolve(c, key[0])
                if target != key and decls.get(target, (0, ""))[1] in ("Algorithm", "Decision Table"):
                    if decls[target][1] == "Algorithm":
                        runners.setdefault(target, set()).add(key)
                    if name == "Decision Table":
                        edges.setdefault(key, set()).add(target)

    def reaches(a, goal, seen):
        for b in sorted(edges.get(a, ())):
            if b == goal or b not in seen and (seen.add(b) or reaches(b, goal, seen)):
                return True
        return False

    for key, steps in algos.items():
        r = key[0]
        line, _, values, tables = decls[key]
        table = tables[0]
        bind = bind_in(r)
        back_at, scope_at = _algorithm(rule, r, line, values, table, steps, facts_in.get(r, {}), bind, found)
        # a Precision: the significant digits each operation keeps, a whole number above zero
        if "Precision" in values and not (re.fullmatch(r'[1-9]\d*', values["Precision"]) and int(values["Precision"]) < 34):
            found.append((rule, r, line, f"a Precision that is no whole number above zero and below FEEL's 34: {values['Precision']}"))
        # a Rounding Mode: one DMN's rounding functions round as, or a fact the Algorithm knows whose Values lie among them
        mode = values.get("Rounding Mode")
        if mode is not None and mode not in ROUNDING_MODES:
            named = [n for _, n in io_items(values, "Inputs")] + list(facts_in.get(r, {}))
            record = facts_in.get(r, {}).get(mode)
            if mode not in named:
                found.append((rule, r, line, f"a Rounding Mode that is neither a mode nor a fact the Algorithm knows: {mode}"))
            elif record and (record[1] == "none" or not set(re.findall(r'"([^"]*)"', record[1])) <= set(ROUNDING_MODES)):
                found.append((rule, r, line, f"a Rounding Mode naming a fact whose Values hold no mode: {mode}"))
        if "Runs When" in values:
            cited = {resolve(c, r) for c in citation.findall(values["Runs When"])}
            # a citation naming no construct is the citation check's to report
            # a construct cited that an unread Algorithm may run is not reported: its own table's finding stands
            for k in sorted(k for k in cited - runners.get(key, set()) if k in decls and k not in unread):
                found.append((rule, r, line, f"a Runs When citing a construct that does not run it: § {k[1]}"))
            for k in sorted(runners.get(key, set()) - cited):
                found.append((rule, r, line, f"a Runs When leaving out a construct that runs it: {k[0]} § {k[1]}"))
        ti = table["header"].index("Terminates") if "Terminates" in table["header"] else None
        for ln, step, form, raw, cond, done in steps:
            recurs = False
            for _, body, braw, _ in done:
                b = bind(braw) if body.startswith("Run ") else None
                if not b:
                    # work naming an Algorithm or a Decision Table whole runs it, in no run's form; a part's
                    # reference names a step or a row, and runs nothing
                    if body and not body.startswith(("Set ", "Run ", "For each")):
                        for c in citation.findall(braw):
                            if "[" not in c and decls.get(resolve(c, r), (0, ""))[1] in ("Algorithm", "Decision Table"):
                                found.append((rule, r, ln, f"work running a construct, a run not written in its form: {c}"))
                    continue
                if b["kind"] not in ("Algorithm", "Decision Table"):
                    if b["kind"] or b["key"] in places:
                        found.append((rule, r, ln, f"a run citing no Algorithm or Decision Table: {b['cite']}"))
                    continue
                recurs = recurs or b["key"] == key or reaches(b["key"], key, set())
                ins, outs = takes(b["key"])
                named = {n for n, _, _ in b["withs"]}
                for item in b["unbound"]:
                    found.append((rule, r, ln, f"a run naming as an argument no Input the construct run takes: {item}"))
                for n in sorted(n for n in named if n not in ins):
                    found.append((rule, r, ln, f"a run naming as an argument no Input the construct run takes: {n}"))
                for n in sorted(n for n in ins if n not in named and n not in scope_at(step)):
                    found.append((rule, r, ln, f"a run leaving an Input the construct run takes neither given nor known: {n}"))
                for out, fact, kind in b["gives"]:
                    if out not in outs:
                        found.append((rule, r, ln, f"a run giving a fact the construct run does not give: {out}"))
                    elif _differs(kind, scope_at(step).get(fact)):
                        found.append((rule, r, ln, f"a run giving a value of another kind than the fact it is written to: {fact}"))
            # a Terminates cell where a step goes back or a run recurs, and only there
            cell = table["rows"][step - 1][1][ti].strip() if ti is not None else NONE_CELL
            if cell == NONE_CELL:
                if back_at.get(step):
                    found.append((rule, r, ln, f"a step going back with no Terminates cell saying why it ends: step {step}"))
                elif recurs:
                    found.append((rule, r, ln, f"a run recurring with no Terminates cell saying why it ends: step {step}"))
            elif not (back_at.get(step) or recurs):
                found.append((rule, r, ln, f"a Terminates cell on a step that neither goes back nor recurs: step {step}"))
            elif CITATION.fullmatch(cell):
                # the Constraint its end rests on, one some construct enforces
                target = decls.get(resolve(CITATION.fullmatch(cell).group(1), r))
                if not target or target[1] != "Constraint" or not target[3]:
                    found.append((rule, r, ln, f"a Terminates cell citing no Constraint: {cell}"))
                    continue
                sel = re.search(r'\[Name: ([^\]]+)\]', cell)
                off = 1 if target[3][0]["header"][:1] == ["Name"] else 0
                for _, crow in target[3][0]["rows"]:
                    if (not sel or off and crow[0] == sel.group(1).strip()) and len(crow) > off + 2 \
                            and NOTHING_ENFORCES.match(_form_of(crow[off + 2])):
                        found.append((rule, r, ln, f"a Terminates cell citing a Constraint nothing enforces: {cell}"))
                        break
            else:
                # the number that shrinks with each pass, as FEEL computes it
                kind = _expression(rule, r, ln, cell, scope_at(step), found)
                if kind is not None and kind != "number":
                    found.append((rule, r, ln, f"a Terminates cell giving no number: step {step}"))
        if ti is not None and all(row[ti] == NONE_CELL for _, row in table["rows"]):
            found.append((rule, r, table["line"], "a Terminates column every cell of which is none"))


# ---------------------------------------------------------------- Constraint

# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation
# a citation: a section token and a title in one backtick span, after a file's path where it cites another file,
# never the token alone; the one copy of the form, which audit-specs.py reads as its own and an Enforced by names
# what enforces its rule by
CITATION = re.compile(r'`((?:[\w./-]+\.md\s*)?§\s+[^`]+)`')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
# an Enforced by whose value is that nothing keeps the rule, `nothing:` and words; the one copy of the form
NOTHING_ENFORCES = re.compile(r'nothing: \S')


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Constraint
# when a rule holds, as its Applies to writes it: `always`, or `after` or `before` the citation of an operation; the
# one copy of the form
APPLIES_TO = re.compile(r'always|(?P<when>after|before) (?P<cite>`[^`]+`)')
# a record section, which states no operation: its records under **Records:**
RECORDS_FIELD = "**Records:**"


def constraint_findings(text_of, found, warned, sections, strip_fences, citation, resolve):
    """§ Constructs § Constraint, each Constraint checked once, across files, its citations resolved: each rule a FEEL
    boolean judged with the facts in scope, its file's and, after or before an Algorithm, or a transition whose effect
    runs one, that Algorithm's; an Applies to in one of its forms, citing an operation whole; and an Enforced by that
    is citations joined by `and`, or `nothing:` and words, the latter appended to `warned`, never to `found`.
    `citation` and `resolve` are the citation check's own."""
    rule = f"{RULE} § Constraint"
    decls, facts_in, record_secs = {}, {}, set()
    for r, body in text_of.items():
        live, secs = strip_fences(body), sections(body)
        lines = live.split(chr(10))
        record_secs.update((r, lineage) for lineage, (h, end) in secs.items()
                           if any(l.strip() == RECORDS_FIELD for l in lines[h:end]))
        facts_in[r] = facts_of(fact_records(live, secs))
        for line, name, fields, tables, lineage in declarations(live, secs):
            decls[(r, lineage)] = (line, name, dict((k, v) for _, k, v in fields), tables)

    def kinds_in(r, names):
        return {n: kind_of_type(facts_in.get(r, {})[n][0]) if n in facts_in.get(r, {}) else None for n in names}

    def io_of(key, when, names):
        """The facts the Algorithm at `key` takes, and gives where `when` is after, added to `names`."""
        target = decls.get(key)
        if not target or target[1] != "Algorithm":
            return
        for k in ["Inputs"] + (["Output"] if when == "after" else []):
            for _, n in io_items(target[2], k):
                names.setdefault(n, kinds_in(key[0], [n])[n])

    def effect_of(key, cite):
        """The citation a transition's Effect cell holds, the transition named by `[Name: …]` in `cite`, or None."""
        _, _, _, tables = decls[key]
        m = re.search(r'\[Name: ([^\]]+)\]', cite)
        if not m or len(tables) < 2 or "Effect" not in tables[1]["header"]:
            return None
        header = tables[1]["header"]
        for _, row in tables[1]["rows"]:
            if row[0].strip() == m.group(1).strip() and len(row) == len(header):
                c = citation.search(row[header.index("Effect")])
                return c.group(0) if c else None
        return None

    for (r, lineage), (line, name, values, tables) in sorted(decls.items()):
        if name != "Constraint" or not tables:
            continue
        table = tables[0]
        header = table["header"]
        off = 1 if header[:1] == ["Name"] else 0
        if header[off:] != FORMS["Constraint"][0]:
            continue  # its form is the declaring check's to report
        scope = kinds_in(r, list(facts_in.get(r, {})))
        for ln, row in table["rows"]:
            if len(row) != len(header):
                continue
            text, applies, enforced = row[off], row[off + 1], row[off + 2]
            names = dict(scope)
            m = APPLIES_TO.fullmatch(applies.strip())
            if not m:
                found.append((rule, r, ln, f"an Applies to that is neither `always` nor `after` or `before` a citation: {applies}"))
            elif m["cite"] and not citation.fullmatch(m["cite"]):
                found.append((rule, r, ln, f"an Applies to citing a whole file, no operation: {m['cite']}"))
            elif m["cite"]:
                key = resolve(m["cite"].strip("`"), r)
                target = decls.get(key)
                # a citation resolving to no section is the citation checks' to report; a section declaring no
                # construct is an operation its own text states, read with the file's facts alone
                if key in record_secs:
                    found.append((rule, r, ln, f"an Applies to citing a record section, which states no operation: {m['cite']}"))
                elif target and target[1] == "Algorithm" and "[" in m["cite"]:
                    found.append((rule, r, ln, f"an Applies to citing a step of an Algorithm, not the Algorithm: {m['cite']}"))
                elif target and target[1] not in ("Algorithm", "State Machine"):
                    found.append((rule, r, ln, f"an Applies to citing what is no operation, {_a(target[1])}: {m['cite']}"))
                elif target and target[1] == "State Machine" and "[Name:" not in m["cite"]:
                    found.append((rule, r, ln, f"an Applies to citing a State Machine and no transition of it: {m['cite']}"))
                elif target and target[1] == "State Machine":
                    effect = effect_of(key, m["cite"])
                    if effect:
                        io_of(resolve(effect.strip("`"), key[0]), m["when"], names)
                elif target:
                    io_of(key, m["when"], names)
            kind, problems = expressions.check(text, names)
            for problem in problems:
                found.append((rule, r, ln, f"a rule: {problem}"))
            if kind not in (None, "boolean") and not problems:
                found.append((rule, r, ln, f"a rule giving no yes or no, a {_kind_name(kind)}: {text}"))
            form = _form_of(enforced)
            if NOTHING_ENFORCES.match(form):
                warned.append((rule, r, ln, f"a rule nothing keeps, its Enforced by opening `nothing:`: {text}"))
            elif re.match(r'(?i)\s*nothing\b', form):
                found.append((rule, r, ln, f"an Enforced by opening `nothing` in other than `nothing:` and words: {enforced}"))
            elif not citation.search(enforced):
                found.append((rule, r, ln, "a rule stated but enforced nowhere: its Enforced by cites nothing"))
            elif citation.sub(" ", enforced).replace("`", "").split() != ["and"] * (len(citation.findall(enforced)) - 1):
                found.append((rule, r, ln, f"an Enforced by that is neither citations joined by `and` nor `nothing:` and words: {enforced}"))


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
    """-> [(path, line, pattern, context)] for the Construct choice and form audit: a State
    Machine an exclusive choice's guard of which compares a fact with another or is in another of FEEL's forms, a
    Decision Table a cell of which tests against
    a fact, a Decision Table whose cells do not settle that every case is matched, a table shaped as a construct's
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
            if name == "State Machine" and len(tables) == 2 and _choice_against_a_fact(tables[1]):
                out.append((r, line, "an exclusive choice testing against a fact or in another of FEEL's forms",
                            f"§ {lineage}: whether two of its guards can hold at once is read"))
            if name == "Decision Table" and tables and _against_a_fact(fields, tables[0]):
                out.append((r, line, "cells testing against a fact or in another of FEEL's forms",
                            f"§ {lineage}: which rows a case reaches, and whether every case matches one, is read"))
            elif name == "Decision Table" and tables and not _settled(fields, tables[0], facts):
                out.append((r, line, "coverage the cells do not settle",
                            f"§ {lineage}: whether every case matches a row is read"))
            # wording a script cannot judge, listed for the reading audit to read: a step that is no comparison
            # holding a comparison's words, its separator aside, which the Algorithm's check reports
            if name == "Algorithm" and tables:
                runs_when = dict((k, v) for _, k, v in fields).get("Runs When", "")
                mode = dict((k, v) for _, k, v in fields).get("Rounding Mode")
                if mode and mode not in ROUNDING_MODES and mode not in facts:
                    out.append((r, line, "a Rounding Mode naming a fact known by name alone",
                                f"§ {lineage}: whether {mode}'s Values hold only the modes, the file holding no record of it, is read"))
                if re.sub(r'\band\b', "", CITATION.sub("", runs_when)).strip(" ,;.") :
                    out.append((r, line, "an Algorithm run on an occurrence in words",
                                f"§ {lineage}: whether something runs it on that occurrence, and for a job's run what a missed and a late run do, is read"))
                for ln, row in tables[0]["rows"]:
                    loop = _for_each(_form_of(row[1]).strip().rstrip("."))
                    if loop and loop["order"] in (ANY_ORDER, LEFT_OPEN):
                        out.append((r, ln, f"a loop {loop['order']}", f"§ {lineage}: whether its order changes what it gives, and a Constraint recording it where it does, is read"))
                    text = _form_of(row[1])
                    if not text.startswith(COMPARISON_OPENING) and SEPARATOR_MARK not in text \
                            and COMPARISON_WORDS.search(text) and not text.startswith(("Set ", "Run ", "For each ")):
                        out.append((r, ln, "a comparison a step may fold", f"§ {lineage}: {row[1][:100]}"))
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


def _choice_against_a_fact(transitions):
    """Whether an exclusive choice's guard compares a fact with another or is in another of FEEL's forms, which the
    script sets aside."""
    header = transitions["header"]
    if "Guard" not in header:
        return False
    off, gi = (1 if header[:1] == ["Name"] else 0), header.index("Guard")
    groups = {}
    for _, row in transitions["rows"]:
        if len(row) > gi:
            groups.setdefault((row[off], row[off + 2]), []).append(row[gi])
    return any((g := guard(x)) and any(symbolic(c) for c in g.values())
               for gs in groups.values() if len(gs) > 1 for x in gs)


def _against_a_fact(fields, table):
    """Whether a Decision Table holds a cell testing against a fact, or in another of FEEL's forms, which the script
    sets aside."""
    header = table["header"]
    values = dict((k, v) for _, k, v in fields)
    conds = [c.strip() for c in values.get("Conditions", "").split(",") if c.strip()]
    idx = [header.index(c) for c in conds if c in header]
    return any((c := feel(row[k])) is not None and symbolic(c) for _, row in table["rows"] for k in idx)


def _settled(fields, table, facts=None):
    """Whether a Decision Table's coverage is decided or settled: its values for every condition, an Input
    Values item, a question's true and false or a Facts record's Values, a Default Output, a hit policy taking every row
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
