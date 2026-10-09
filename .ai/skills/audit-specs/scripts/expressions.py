"""FEEL expressions, adopted whole: an expression or a cell's unary tests parsed and given its kind, so a name no fact
declares, values of two known kinds combined, and a call FEEL's built-in functions do not take are reported.

The audit's child script for expressions (specs/methodology/expressions.md § Expressions § FEEL): constructs.py reads
a construct's cells and hands it what is written in FEEL. It parses FEEL's whole grammar, gives each expression its
kind where it can be told, and reports only what it can decide; it evaluates nothing.
"""
import difflib
import re

# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct § A Fact
# a fact's name: words separated by single spaces, each opening with a letter and holding letters, digits and
# apostrophes, a hyphen joining two runs of them; and a boolean fact's, a question, any words ending in a question mark;
# the one copy, which constructs.py reads too
WORD = r"[A-Za-z][A-Za-z0-9']*(?:-[A-Za-z0-9']+)*"
NAME = re.compile(WORD + r"(?: " + WORD + r")*")
QUESTION = re.compile(r"[^,]*[^,\s]\?")
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# a header computing the value its column tests, DMN's input expression, and no fact's name: one holding `+`, `*`,
# `/`, `<`, `>`, `=`, a bracket, a parenthesis, a minus between spaces, or a dot between two words, and not a question
COMPUTING = re.compile(r'[()+*/<>=\[\]]| - |(?<=[^\W\d])\.(?=[^\W\d])')
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Values
# a value as FEEL writes one, each part a group: a date, a date and time to the second with its offset, a time of day,
# a duration of either kind; the one copy, which constructs.py reads too
LITERAL = {
    "date and time": re.compile(r'date and time\("(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})"\)'),
    "date": re.compile(r'date\("(\d{4})-(\d{2})-(\d{2})"\)'),
    "time": re.compile(r'time\("(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})?"\)'),
    "years and months duration": re.compile(r'duration\("(-?)P(?=\d)(?:(\d+)Y)?(?:(\d+)M)?"\)'),
    "days and time duration": re.compile(
        r'duration\("(-?)P(?=\d|T\d)(?:(\d+)D)?(?:T(?=\d)(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?"\)'),
}
# the string an `@` literal holds, each kind's, and which kind it is
AT_FORMS = (
    ("date and time", re.compile(r'-?\d{4,}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2}|@[\w/+-]+)?')),
    ("date", re.compile(r'-?\d{4,}-\d{2}-\d{2}')),
    ("time", re.compile(r'\d{2}:\d{2}:\d{2}(\.\d+)?(Z|z|[+-]\d{2}:\d{2}|@[\w/+-]+)?')),
    ("years and months duration", re.compile(r'-?P(?=\d)(\d+Y)?(\d+M)?')),
    ("days and time duration", re.compile(r'-?P(?=\d|T\d)(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?')),
)
DURATIONS = ("days and time duration", "years and months duration")
TEMPORAL = ("date", "date and time", "time")
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Names
# the words FEEL keeps for itself, which no name opens with; the one copy, held to the file's list by keyword_findings
KEYWORDS = {"and", "between", "else", "every", "external", "false", "for", "function", "if", "in", "instance", "not",
            "null", "of", "or", "return", "satisfies", "some", "then", "true"}
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Values
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions
# the types' names, the longest first, as `instance of` and a function's parameter name them
TYPE_NAMES = sorted(["number", "string", "boolean", "date", "time", "date and time", "days and time duration",
                     "years and months duration", "list", "context", "range", "function", "Any", "Null"],
                    key=lambda n: -len(n.split()))
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
# the parts a path names on a date, a time, a duration or a range, and the kind each gives
PROPERTIES = {
    "date": {"year": "number", "month": "number", "day": "number", "weekday": "number"},
    "date and time": {"year": "number", "month": "number", "day": "number", "weekday": "number", "hour": "number",
                      "minute": "number", "second": "number", "time offset": "days and time duration",
                      "timezone": "string"},
    "time": {"hour": "number", "minute": "number", "second": "number", "time offset": "days and time duration",
             "timezone": "string"},
    "years and months duration": {"years": "number", "months": "number"},
    "days and time duration": {"days": "number", "hours": "number", "minutes": "number", "seconds": "number"},
}
# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Functions
# every function FEEL builds in, as the file's table writes each: its name, what it takes and what it gives; and those
# also given a list's items as arguments; the one copy, held to the table on every run by function_table_findings
FUNCTION_TABLE = (
    ('date', 'from', 'date'),
    ('date', 'year, month, day', 'date'),
    ('date and time', 'date, time', 'date and time'),
    ('date and time', 'from', 'date and time'),
    ('time', 'from', 'time'),
    ('time', 'hour, minute, second, offset?', 'time'),
    ('number', 'from, grouping separator, decimal separator', 'number'),
    ('string', 'from', 'string'),
    ('duration', 'from', 'duration'),
    ('years and months duration', 'from, to', 'years and months duration'),
    ('range', 'from', 'range'),
    ('not', 'negand', 'boolean'),
    ('substring', 'string, start position, length?', 'string'),
    ('string length', 'string', 'number'),
    ('upper case', 'string', 'string'),
    ('lower case', 'string', 'string'),
    ('substring before', 'string, match', 'string'),
    ('substring after', 'string, match', 'string'),
    ('replace', 'input, pattern, replacement, flags?', 'string'),
    ('contains', 'string, match', 'boolean'),
    ('starts with', 'string, match', 'boolean'),
    ('ends with', 'string, match', 'boolean'),
    ('matches', 'input, pattern, flags?', 'boolean'),
    ('split', 'string, delimiter', 'list'),
    ('string join', 'list, delimiter?', 'string'),
    ('list contains', 'list, element', 'boolean'),
    ('count', 'list', 'number'),
    ('min', 'list', 'item'),
    ('max', 'list', 'item'),
    ('sum', 'list', 'number'),
    ('mean', 'list', 'number'),
    ('all', 'list', 'boolean'),
    ('any', 'list', 'boolean'),
    ('sublist', 'list, start position, length?', 'list'),
    ('append', 'list, item…', 'list'),
    ('concatenate', 'list…', 'list'),
    ('insert before', 'list, position, newItem', 'list'),
    ('remove', 'list, position', 'list'),
    ('list replace', 'list, position, newItem', 'list'),
    ('list replace', 'list, match, newItem', 'list'),
    ('reverse', 'list', 'list'),
    ('index of', 'list, match', 'list'),
    ('union', 'list…', 'list'),
    ('distinct values', 'list', 'list'),
    ('flatten', 'list', 'list'),
    ('product', 'list', 'number'),
    ('median', 'list', 'number'),
    ('stddev', 'list', 'number'),
    ('mode', 'list', 'list'),
    ('decimal', 'n, scale', 'number'),
    ('floor', 'n, scale?', 'number'),
    ('ceiling', 'n, scale?', 'number'),
    ('round up', 'n, scale', 'number'),
    ('round down', 'n, scale', 'number'),
    ('round half up', 'n, scale', 'number'),
    ('round half down', 'n, scale', 'number'),
    ('abs', 'n', "n's type"),
    ('modulo', 'dividend, divisor', 'number'),
    ('sqrt', 'number', 'number'),
    ('log', 'number', 'number'),
    ('exp', 'number', 'number'),
    ('odd', 'number', 'boolean'),
    ('even', 'number', 'boolean'),
    ('is', 'value1, value2', 'boolean'),
    ('before', 'point1, point2', 'boolean'),
    ('before', 'point, range', 'boolean'),
    ('before', 'range, point', 'boolean'),
    ('before', 'range1, range2', 'boolean'),
    ('after', 'point1, point2', 'boolean'),
    ('after', 'point, range', 'boolean'),
    ('after', 'range, point', 'boolean'),
    ('after', 'range1, range2', 'boolean'),
    ('meets', 'range1, range2', 'boolean'),
    ('met by', 'range1, range2', 'boolean'),
    ('overlaps', 'range1, range2', 'boolean'),
    ('overlaps before', 'range1, range2', 'boolean'),
    ('overlaps after', 'range1, range2', 'boolean'),
    ('finishes', 'point, range', 'boolean'),
    ('finishes', 'range1, range2', 'boolean'),
    ('finished by', 'range, point', 'boolean'),
    ('finished by', 'range1, range2', 'boolean'),
    ('includes', 'range, point', 'boolean'),
    ('includes', 'range1, range2', 'boolean'),
    ('during', 'point, range', 'boolean'),
    ('during', 'range1, range2', 'boolean'),
    ('starts', 'point, range', 'boolean'),
    ('starts', 'range1, range2', 'boolean'),
    ('started by', 'range, point', 'boolean'),
    ('started by', 'range1, range2', 'boolean'),
    ('coincides', 'point1, point2', 'boolean'),
    ('coincides', 'range1, range2', 'boolean'),
    ('day of year', 'date', 'number'),
    ('day of week', 'date', 'string'),
    ('month of year', 'date', 'string'),
    ('week of year', 'date', 'number'),
    ('sort', 'list, precedes', 'list'),
    ('get value', 'm, key', 'item'),
    ('get entries', 'm', 'list'),
    ('context', 'entries', 'context'),
    ('context put', 'context, key, value', 'context'),
    ('context put', 'context, keys, value', 'context'),
    ('context merge', 'contexts', 'context'),
    ('now', '', 'date and time'),
    ('today', '', 'date'),
)
ITEMS_AS_ARGUMENTS = {"min", "max", "sum", "mean", "all", "any", "product", "median", "stddev", "mode"}


def _arities(takes):
    """What a function takes -> (fewest arguments, most, None for any number)."""
    params = [p.strip() for p in takes.split(",") if p.strip()]
    least = sum(1 for p in params if not p.endswith("?") and not p.endswith("…"))
    return least, None if any(p.endswith("…") for p in params) else len(params)


FUNCTIONS = {}
for _name, _takes, _gives in FUNCTION_TABLE:
    FUNCTIONS.setdefault(_name, []).append((_arities(_takes), _gives))
for _name in ITEMS_AS_ARGUMENTS:
    FUNCTIONS[_name].append(((1, None), FUNCTIONS[_name][0][1]))

TOKEN = re.compile(r'''\s*(?:(?P<comment>//[^\n]*|/\*.*?\*/)|(?P<at>@"(?:[^"\\]|\\.)*")|(?P<str>"(?:[^"\\]|\\.)*")
    |(?P<num>(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?)|(?P<op>\*\*|<=|>=|!=|\.\.|[-+*/<>=()\[\]{},.:?])
    |(?P<word>(?:[^\W\d]|[?'])[\w'?]*))''', re.X | re.S)


class FeelError(ValueError):
    pass


def _names_by_length(names):
    """Each name FEEL's tokens make, with its tokens, the longest first and then by name."""
    out = []
    for n in names:
        try:
            out.append((n, _tokens(n)))
        except FeelError:
            continue
    return sorted(out, key=lambda np: (-len(np[1]), np[0]))


def _tokens(text):
    out, i = [], 0
    while i < len(text):
        m = TOKEN.match(text, i)
        if not m or m.end() == i:
            if text[i:].strip():
                raise FeelError(f"no FEEL token at: {text[i:i + 12]}")
            break
        i = m.end()
        kind = next(k for k in ("comment", "at", "str", "num", "op", "word") if m.group(k) is not None)
        if kind != "comment":
            out.append((kind, m.group(kind)))
    return out


def _at_kind(text):
    body = text[2:-1]
    return next((k for k, p in AT_FORMS if p.fullmatch(body)), None)


def _shown(k):
    if isinstance(k, tuple):
        return f"{k[0]} of {k[1] or 'values'}"
    return k


def _flat(k):
    """A context's kind, its entries set aside, so it is compared as a context; any other kind as it is."""
    return "context" if isinstance(k, tuple) and k[0] == "ctx" else k


class _Parser:
    """A recursive descent over FEEL's tokens, giving each expression its kind: a name's its fact's, None where it
    cannot be told; each problem it can decide appended to `problems`."""

    def __init__(self, text, facts, known=None, used=None):
        self.toks, self.i, self.problems = _tokens(text), 0, []
        self.used = used  # a list each fact the parse resolves is appended to, or None
        self.facts = {k: ("string" if v == "word" else v) for k, v in dict(facts).items()}
        self.known = known  # a name the caller knows though no fact is named it, or None
        self.bound = []  # names bound by a loop, a quantifier, a filter or a function, innermost last
        self.open = 0  # how many filters over items of unknown shape enclose the parse, their entries unnamed

    # -- tokens
    def peek(self, k=0):
        return self.toks[self.i + k] if self.i + k < len(self.toks) else (None, None)

    def at(self, *vals):
        return self.peek()[1] in vals and self.peek()[0] in ("op", "word")

    def take(self, val=None):
        tok = self.peek()
        if tok == (None, None) or val is not None and tok[1] != val:
            raise FeelError(f"expected {val or 'more'}, found {tok[1] or 'the end'}")
        self.i += 1
        return tok

    def scoped(self, names, body):
        self.bound.extend(names)
        try:
            return body()
        finally:
            del self.bound[len(self.bound) - len(names):]

    # -- grammar, loosest first (DMN 10.3.1.2, rules 2 and 4)
    def expr(self):
        if self.at("for"):
            self.take()
            binds = []
            while True:
                var = self._variable()
                items = self.disjunction()
                if self.at(".."):
                    self.take()
                    self.disjunction()
                    items = ("list", items if items in ("number",) + TEMPORAL else None)
                binds.append((var, items[1] if isinstance(items, tuple) else None))
                if not self.at(","):
                    break
                self.take()
            self.take("return")
            return ("list", self.scoped(binds + [("partial", ("list", None))], self.expr))
        if self.at("if"):
            self.take()
            self._want(self.expr(), "boolean", "an if's condition")
            self.take("then")
            a = self.expr()
            self.take("else")
            return self._same(a, self.expr(), "an if's two outcomes")
        if self.at("some", "every"):
            self.take()
            binds = []
            while True:
                var = self._variable()
                items = self.disjunction()
                binds.append((var, items[1] if isinstance(items, tuple) else None))
                if not self.at(","):
                    break
                self.take()
            self.take("satisfies")
            self._want(self.scoped(binds, self.expr), "boolean", "a quantifier's test")
            return "boolean"
        return self.disjunction()

    def _variable(self):
        """A loop's or a quantifier's variable, its words up to `in`, and the `in` taken."""
        words = []
        while self.peek()[0] == "word" and not (words and self.at("in")):
            words.append(self.take()[1])
        if not words:
            raise FeelError(f"no variable at: {self.peek()[1] or 'the end'}")
        self.take("in")
        return " ".join(words)

    def disjunction(self):
        a = self.conjunction()
        while self.at("or"):
            self.take()
            self._want(a, "boolean", "an or")
            self._want(self.conjunction(), "boolean", "an or")
            a = "boolean"
        return a

    def conjunction(self):
        a = self.comparison()
        while self.at("and"):
            self.take()
            self._want(a, "boolean", "an and")
            self._want(self.comparison(), "boolean", "an and")
            a = "boolean"
        return a

    def comparison(self):
        a = self.additive()
        if self.at("=", "!=", "<", "<=", ">", ">="):
            self.take()
            self._same(a, self.additive(), "a comparison")
            return "boolean"
        if self.at("between"):
            self.take()
            b = self.additive()
            self.take("and")
            self._same(a, self._same(b, self.additive(), "a between's ends"), "a between")
            return "boolean"
        if self.at("in"):
            self.take()
            if self.at("(") and self._parenthesized_tests():
                self.take("(")
                self.positive_tests(a)
                self.take(")")
            else:
                self.positive_test(a)
            return "boolean"
        return a

    def _parenthesized_tests(self):
        """Whether `( … )` after `in` holds several tests, a comma at its own depth, rather than one expression."""
        depth, k = 0, self.i
        while k < len(self.toks):
            v = self.toks[k][1]
            if v in "([{" and self.toks[k][0] == "op":
                depth += 1
            elif v in ")]}" and self.toks[k][0] == "op":
                depth -= 1
                if depth == 0:
                    return False
            elif v == "," and depth == 1:
                return True
            k += 1
        return False

    def additive(self):
        a = self.multiplicative()
        while self.at("+", "-"):
            op = self.take()[1]
            a = self._arith(a, self.multiplicative(), op)
        return a

    def multiplicative(self):
        a = self.power()
        while self.at("*", "/"):
            op = self.take()[1]
            a = self._arith(a, self.power(), op)
        return a

    def power(self):
        a = self.negation()
        while self.at("**"):
            self.take()
            b = self.negation()
            self._want(a, "number", "a power")
            self._want(b, "number", "a power")
            a = "number" if a is not None else None
        return a

    def negation(self):
        if self.at("-"):
            self.take()
            a = self.negation()
            if a is not None and a != "number" and a not in DURATIONS:
                self.problems.append(f"a minus sign before a {_shown(a)}")
            return a
        return self.instance_of()

    def instance_of(self):
        a = self.postfix()
        if self.at("instance"):
            self.take()
            self.take("of")
            self.type_()
            return "boolean"
        return a

    def type_(self):
        # the type's text, to the expression's end or, outside a type name, a closing bracket or brace, a comma or a
        # word ending it, read as parse_type reads a Type: a type name holding `and` taken whole, the longest first,
        # and `-` then `>` one arrow
        names = sorted((n.split() for n in TYPE_NAMES), key=len, reverse=True)
        k, depth, words = self.i, 0, []
        while k < len(self.toks):
            v = self.toks[k][1]
            n = next((p for p in names if [t[1] for t in self.toks[k:k + len(p)]] == p), None)
            if n:
                words += n
                k += len(n)
                continue
            if depth == 0 and v in (")", "]", "}", ",", "and", "or", "then", "else", "return", "satisfies"):
                break
            if v == "-" and k + 1 < len(self.toks) and self.toks[k + 1][1] == ">":
                words.append("->")
                k += 2
                continue
            depth += {"<": 1, ">": -1}.get(v, 0)
            words.append(v)
            k += 1
        text = " ".join(words).replace(" < ", "<").replace("< ", "<").replace(" >", ">")
        try:
            parse_type(text.replace(" : ", ": ").replace(" ,", ","))
        except FeelError as e:
            self.problems.append(str(e))
        self.i = k

    def postfix(self):
        a = self.primary()
        while True:
            if self.at("."):
                self.take()
                part = self._name_words()
                a = self._property(a, part)
            elif self.at("[") and self.peek(1)[1] not in (None, ",", ")", "]"):
                # a `[` closing a range `]a..b[` opens no filter
                self.take()
                a = self._filter(a)
                self.take("]")
            elif self.at("(") and isinstance(a, tuple) and a[0] == "fn":
                a = self.call(a[1])
            elif self.at("("):
                self.take("(")
                self._arguments()
                self.take(")")
                a = None
            else:
                return a[2] if isinstance(a, tuple) and a[0] == "fn" else a

    def _name_words(self):
        words = []
        while self.peek()[0] == "word" and not (words and self.peek()[1] in KEYWORDS):
            words.append(self.take()[1])
        if not words:
            raise FeelError(f"no name after a dot at: {self.peek()[1] or 'the end'}")
        return " ".join(words)

    def _property(self, a, part):
        if isinstance(a, tuple) and a[0] == "fn":
            a = a[2]
        if a in PROPERTIES:
            if part not in PROPERTIES[a]:
                self.problems.append(f"a {a} holding no part named {part}")
                return None
            return PROPERTIES[a][part]
        if isinstance(a, tuple) and a[0] == "ctx":
            entries = dict(a[1])
            if entries and part not in entries:
                self.problems.append(f"a context holding no entry named {part}")
            return entries.get(part)
        if isinstance(a, tuple) and a[0] == "list":
            inner = a[1]
            if isinstance(inner, tuple) and inner[0] == "ctx":
                entries = dict(inner[1])
                if entries and part not in entries:
                    self.problems.append(f"a context holding no entry named {part}")
                return ("list", entries.get(part))
            return ("list", None)
        if isinstance(a, tuple) and a[0] == "range":
            return {"start included": "boolean", "end included": "boolean"}.get(part, a[1])
        if a is not None:
            self.problems.append(f"a path into a {_shown(a)}, which holds no parts: {part}")
        return None

    def _filter(self, a):
        """A filter or an index: `item` and, where items are contexts, their entries in scope (DMN 10.3.2.5)."""
        item = a[1] if isinstance(a, tuple) and a[0] == "list" else (None if isinstance(a, tuple) else a)
        entries = list(item[1]) if isinstance(item, tuple) and item[0] == "ctx" else []
        self.open += 0 if entries else 1
        try:
            test = self.scoped([("item", item)] + entries, self.expr)
        finally:
            self.open -= 0 if entries else 1
        if test == "number":
            return item
        if test is None:
            return None
        if test != "boolean":
            self.problems.append(f"a filter whose test is a {_shown(test)}, neither a yes or no nor a place")
        return a if isinstance(a, tuple) else ("list", a)

    def _arguments(self):
        args, named = [], False
        while not self.at(")"):
            # a parameter's name, its words up to the colon
            k = 0
            while self.peek(k)[0] == "word":
                k += 1
            if k and self.peek(k) == ("op", ":"):
                self.i += k
                self.take(":")
                named = True
            args.append(self.expr())
            if self.at(","):
                self.take()
        return args, named

    def call(self, fn):
        self.take("(")
        args, named = self._arguments()
        self.take(")")
        sigs = FUNCTIONS[fn]
        if not named and not any(lo <= len(args) and (hi is None or len(args) <= hi) for (lo, hi), _ in sigs):
            self.problems.append(f"a call giving {fn} {len(args)} argument{'s' if len(args) != 1 else ''}, which it does not take")
        gives = next((g for (lo, hi), g in sigs if lo <= len(args) and (hi is None or len(args) <= hi)), sigs[0][1])
        if gives == "item" and fn in ITEMS_AS_ARGUMENTS:
            first = args[0] if args else None
            return first[1] if isinstance(first, tuple) and len(args) == 1 else (first if len(args) > 1 else None)
        if gives == "item":
            return None
        if gives.endswith("'s type"):
            first = args[0] if args else None
            return first if not isinstance(first, tuple) else None
        if gives == "list":
            return ("list", None)
        if gives == "duration":
            return None
        if gives == "range":
            return ("range", None)
        return gives

    def primary(self):
        kind, val = self.peek()
        if kind == "num":
            self.take()
            return "number"
        if kind == "str":
            self.take()
            return "string"
        if kind == "at":
            self.take()
            k = _at_kind(val)
            if k is None:
                self.problems.append(f"an @ value in no form a date, a time or a duration has: {val}")
            return k
        if kind == "op" and val in ("<", "<=", ">", ">=", "=", "!="):
            # a range of one end and a comparison (DMN 10.3.2.7)
            self.take()
            return ("range", self.additive())
        if kind == "op" and val == "(":
            self.take()
            if self.at(".."):
                raise FeelError("a range open at one end written `(..`, which only `range` reads from a string")
            a = self.expr()
            if self.at(".."):
                return self._range_tail(a)
            self.take(")")
            return a
        if kind == "op" and val in ("[", "]"):
            self.take()
            if val == "[" and self.at("]"):
                self.take()
                return ("list", None)
            if self.at(".."):
                raise FeelError("a range open at one end written `[..`, which only `range` reads from a string")
            a = self.expr()
            if self.at(".."):
                return self._range_tail(a)
            if val == "]":
                raise FeelError("a range opening `]` with no `..`")
            items = [a]
            while self.at(","):
                self.take()
                items.append(self.expr())
            self.take("]")
            known = {k for k in items if k is not None and not isinstance(k, tuple)}
            return ("list", known.pop() if len(known) == 1 and None not in items else None)
        if kind == "op" and val == "{":
            self.take()
            entries = []
            while not self.at("}"):
                key = self.take()
                if key[0] == "word":
                    while self.peek()[0] == "word":
                        key = ("word", key[1] + " " + self.take()[1])
                self.take(":")
                entries.append((key[1].strip('"'), self.scoped(list(entries), self.expr)))
                if self.at(","):
                    self.take()
            self.take("}")
            return ("ctx", tuple(entries))
        if kind == "op" and val == "?":
            self.take()
            return self._bound("?")
        if kind == "word" and val in ("if", "for", "some", "every"):
            return self.expr()
        if kind == "word":
            if val == "null":
                self.take()
                return None
            if val in ("true", "false"):
                self.take()
                return "boolean"
            if val == "function":
                return self.function_definition()
            if val == "not" and self.peek(1) == ("op", "("):
                self.take()
                self.take("(")
                self._want(self.expr(), "boolean", "a not")
                self.take(")")
                return "boolean"
            return self.name()
        raise FeelError(f"no FEEL expression at: {val or 'the end'}")

    def _range_tail(self, start):
        self.take("..")
        if self.at(")", "]", "["):
            raise FeelError("a range open at one end written `..)`, which only `range` reads from a string")
        end = self.additive()
        if not self.at(")", "]", "["):
            raise FeelError(f"a range with no closing bracket at: {self.peek()[1] or 'the end'}")
        self.take()
        return ("range", self._same(start, end, "a range's ends"))

    def function_definition(self):
        self.take("function")
        self.take("(")
        params = []
        while not self.at(")"):
            words = [self.take()[1]]
            while self.peek()[0] == "word":
                words.append(self.take()[1])
            if self.at(":"):
                self.take()
                self.type_()
            params.append((" ".join(words), None))
            if self.at(","):
                self.take()
        self.take(")")
        if self.at("external"):
            self.take()
        self.scoped(params, self.expr)
        return "function"

    def _bound(self, name):
        for var, k in reversed(self.bound):
            if var == name:
                return k
        return None

    def name(self):
        """A name: a bound one, innermost first; then a declared fact or a built-in function, the longest matching
        run of words winning (DMN 10.3.1.6)."""
        for var, kind in reversed(self.bound):
            parts = var.split()
            if all(self.peek(k) == ("word", p) for k, p in enumerate(parts)):
                self.i += len(parts)
                return kind
        for n, parts in _names_by_length(set(self.facts) | set(FUNCTIONS)):
            if all(self.peek(k)[1] == p[1] for k, p in enumerate(parts)):
                if n in self.facts:
                    self.i += len(parts)
                    if self.used is not None:
                        self.used.append(n)
                    return self.facts[n]
                if self.peek(len(parts)) == ("op", "("):
                    self.i += len(parts)
                    return ("fn", n, None)
                if not self.open and self.peek(len(parts))[0] != "word":
                    self.i += len(parts)
                    return "function"
        if self.peek()[0] == "word" and self.peek()[1] in KEYWORDS:
            raise FeelError(f"a name opening with a word FEEL keeps: {self.peek()[1]}")
        words = []
        # a later word of a name may be one FEEL keeps; `of`, which FEEL writes only after `instance`, runs on
        while self.peek()[0] == "word" and (not words or self.peek()[1] not in KEYWORDS
                                            or self.peek()[1] == "of" and words[-1] != "instance"):
            words.append(self.take()[1])
        if not words:
            raise FeelError(f"no FEEL expression at: {self.peek()[1] or 'the end'}")
        name = " ".join(words)
        if self.at("("):
            self.problems.append(f"a call of a function FEEL does not build in: {name}")
        elif not self.open and not (self.known and self.known(name)):
            self.problems.append(f"a name no fact declares: {name}")
        return None

    # -- tests: a cell's unary tests (DMN 10.3.1.2, rules 7, 8 and 13 to 15)
    def unary_tests(self, value=None):
        if self.at("-") and self.peek(1) == (None, None):
            self.take()
            return
        if self.at("not") and self.peek(1) == ("op", "("):
            self.take()
            self.take("(")
            self.positive_tests(value)
            self.take(")")
            return
        self.positive_tests(value)

    def positive_tests(self, value=None):
        self.positive_test(value)
        while self.at(","):
            self.take()
            self.positive_test(value)

    def positive_test(self, value=None):
        if self.at("<", "<=", ">", ">=", "=", "!="):
            self.take()
            self._same(value, self.additive(), "a comparison")
            return
        self.scoped([("?", value)], self.expr)

    # -- kinds
    def _want(self, a, kind, where):
        a = _flat(a)
        if a is not None and a != kind and not isinstance(a, tuple):
            self.problems.append(f"{where} given a {a}, not a {kind}")

    def _same(self, a, b, where):
        ka = _flat(a[1] if isinstance(a, tuple) and a[0] == "range" else a)
        kb = _flat(b[1] if isinstance(b, tuple) and b[0] == "range" else b)
        if ka is not None and kb is not None and not isinstance(ka, tuple) and not isinstance(kb, tuple) and ka != kb \
                and {ka, kb} != {"date", "date and time"}:
            self.problems.append(f"{where} of a {_shown(ka)} and a {_shown(kb)}")
            return None
        return a if a is not None else b

    def _arith(self, a, b, op):
        a, b = _flat(a), _flat(b)
        if a is None or b is None or isinstance(a, tuple) or isinstance(b, tuple):
            return None
        if a == b == "number":
            return "number"
        if op == "+" and a == b == "string":
            return "string"
        if op in "+-" and a in TEMPORAL and b in DURATIONS and (a, b) != ("time", "years and months duration"):
            return a
        if op == "+" and a in DURATIONS and b in TEMPORAL and (b, a) != ("time", "years and months duration"):
            return b
        if op == "-" and a in TEMPORAL and b in TEMPORAL and (a == b or {a, b} == {"date", "date and time"}):
            return "days and time duration"
        if op in "+-" and a == b and a in DURATIONS:
            return a
        if op == "*" and {a, b} <= set(DURATIONS) | {"number"} and "number" in (a, b):
            return a if a in DURATIONS else b
        if op == "/" and a in DURATIONS and b == "number":
            return a
        if op == "/" and a == b and a in DURATIONS:
            return "number"
        self.problems.append(f"a {op} of a {_shown(a)} and a {_shown(b)}")
        return None


def check(text, facts, known=None, used=None):
    """A FEEL expression, and each fact it may name with its kind or None -> (its kind or None, [problem]); `known`,
    where given, tells whether a name no fact is named is one the caller knows."""
    try:
        p = _Parser(text, facts, known, used)
        kind = p.expr()
        if p.i != len(p.toks):
            raise FeelError(f"more after the expression: {p.peek()[1]}")
        if isinstance(kind, tuple) and kind[0] == "fn":
            kind = None
        return kind, p.problems
    except FeelError as e:
        return None, [f"an expression in no form FEEL has: {e}"]


def check_tests(text, facts, value=None, known=None):
    """A cell's unary tests, the value they test of kind `value` -> [problem]."""
    try:
        p = _Parser(text, facts, known)
        p.unary_tests(value)
        if p.i != len(p.toks):
            raise FeelError(f"more after the tests: {p.peek()[1]}")
        return p.problems
    except FeelError as e:
        return [f"a cell in no form FEEL has: {e}"]


def function_table_findings(text):
    """The file's table of FEEL's built-in functions against FUNCTION_TABLE and ITEMS_AS_ARGUMENTS, this script's
    copy: each row's Function, Takes and Gives, in order, and which are also given a list's items -> [(line, message)]."""
    lines, out, rows = text.split("\n"), [], []
    for i, l in enumerate(lines):
        if l.startswith("| Function | Takes | Gives | Does |"):
            for j in range(i + 2, len(lines)):
                if not lines[j].startswith("|"):
                    break
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                rows.append((j + 1, cells))
            break
    if not rows:
        return [(0, "no table of FEEL's built-in functions headed Function, Takes, Gives and Does")]
    copy, table = list(FUNCTION_TABLE), [tuple(cells[:3]) for _, cells in rows]
    # the two compared as a diff, so a row added or left out is reported once, not as every row after it
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, table, copy, autojunk=False).get_opcodes():
        for k in range(i1, i2) if tag in ("replace", "delete") else ():
            out.append((rows[k][0], f"a function row the script's copy does not hold: {list(table[k])}"))
        for k in range(j1, j2) if tag in ("replace", "insert") else ():
            at = rows[min(i1, len(rows) - 1)][0]
            out.append((at, f"a function row the table does not hold, of the script's copy: {list(copy[k])}"))
    for ln, cells in rows:
        items = "also given its items as arguments" in (cells[3] if len(cells) > 3 else "")
        if items != (cells[0] in ITEMS_AS_ARGUMENTS):
            out.append((ln, f"a function the script's copy gives its items as arguments otherwise: {cells[0]}"))
    return out


def keyword_findings(text):
    """The file's list of the words FEEL keeps for itself against KEYWORDS, this script's copy -> [(line, message)]."""
    for i, l in enumerate(text.split("\n"), 1):
        m = re.search(r"A name never opens with one of the words FEEL keeps for itself: (.*?);", l)
        if m:
            listed = set(re.findall(r"`([^`]+)`", m.group(1)))
            out = [(i, f"a word FEEL keeps the script's copy does not hold: {w}") for w in sorted(listed - KEYWORDS)]
            return out + [(i, f"a word the script keeps the file does not list: {w}") for w in sorted(KEYWORDS - listed)]
    return [(0, "no list of the words FEEL keeps for itself")]


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions
# a type as FEEL names it, a Facts record's Type among them
SIMPLE_TYPES = {n: {"Any": None, "Null": None, "context": ("ctx", ()), "list": ("list", None),
                    "range": ("range", None)}.get(n, n) for n in TYPE_NAMES}


def _split_top(text):
    parts, depth, cur = [], 0, ""
    for k, ch in enumerate(text):
        depth += {"<": 1, ">": -1}.get(ch, 0) if not (ch == ">" and text[k - 1:k] == "-") else 0
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return parts + [cur.strip()]


def parse_type(text):
    """A type as FEEL names it -> its kind: a simple type's, ("list", the items'), ("ctx", ((entry, its kind), …)),
    ("range", its ends'), "function", or None for Any and Null; FeelError for no type FEEL names."""
    t = text.strip()
    if t in SIMPLE_TYPES:
        return SIMPLE_TYPES[t]
    m = re.fullmatch(r'(list|range)\s*<(.+)>', t)
    if m:
        return (m.group(1), parse_type(m.group(2)))
    m = re.fullmatch(r'context\s*<(.+)>', t)
    if m:
        out = {}
        for entry in _split_top(m.group(1)):
            name, colon, kind = entry.partition(":")
            if not colon or not name.strip():
                raise FeelError(f"a context's entry with no name and type: {entry}")
            out[name.strip()] = parse_type(kind)
        return ("ctx", tuple(out.items()))
    if re.fullmatch(r'function\s*<.*>\s*->\s*.+', t):
        return "function"
    raise FeelError(f"no type FEEL names: {t}")
