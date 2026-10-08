"""FEEL expressions, in the subset a Decision Table writes: a computed header or a computed outcome, parsed and
given its kind, so a name no fact declares and values of two kinds combined are reported.

The audit's child script for expressions (specs/methodology/modeling-constructs.md § Constructs § Decision Table):
constructs.py reads a table's cells and hands it what is written in FEEL. It parses, it gives each expression its
kind, and it reports what it cannot; it evaluates nothing.
"""
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
# `/`, `<`, `>`, `=`, a bracket, a parenthesis, or a minus between spaces, and not a question
COMPUTING = re.compile(r'[()+*/<>=\[\]]| - ')
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
# the functions a FEEL expression may call, each with the kind it gives: a number, a list's items', or a yes or no
FUNCTIONS = {"count": "number", "sum": "number", "min": "item", "max": "item", "list contains": "boolean"}
KEYWORDS = {"and", "or", "not", "if", "then", "else", "some", "every", "in", "satisfies", "for", "return",
            "null", "true", "false"}
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
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
LITERALS = tuple(LITERAL.items())
TOKEN = re.compile(r'\s*(?:(?P<lit>' + "|".join(p.pattern for _, p in LITERALS) + r')|(?P<num>\d+(?:\.\d+)?|\.\d+)'
                   r'|(?P<str>"[^"]*")|(?P<op><=|>=|!=|[-+*/<>=()\[\],])|(?P<word>' + WORD + r'\??))')
KINDS = ("lit", "num", "str", "op", "word")
DURATIONS = ("days and time duration", "years and months duration")
TEMPORAL = ("date", "date and time", "time")


class FeelError(ValueError):
    pass


def _tokens(text):
    out, i = [], 0
    while i < len(text):
        m = TOKEN.match(text, i)
        if not m or m.end() == i:
            if text[i:].strip():
                raise FeelError(f"no FEEL token at: {text[i:i + 12]}")
            break
        kind = next(k for k in KINDS if m.group(k) is not None)
        val = m.group(kind)
        if kind == "lit":
            out.append(("lit", next(k for k, p in LITERALS if p.fullmatch(val))))
        elif kind == "num":
            out.append(("lit", "number"))
        elif kind == "str":
            out.append(("lit", "string"))
        else:
            out.append((kind, val))
        i = m.end()
    return out


class _Parser:
    """A recursive descent over the tokens, giving each expression its kind: a name's kind its fact's, `None`
    where it cannot be told; each problem appended to `problems`."""

    def __init__(self, text, facts):
        self.toks, self.i, self.facts, self.problems = _tokens(text), 0, dict(facts), []
        self.bound = []  # the names a quantifier, a `for` or a filter binds, innermost last

    def peek(self, k=0):
        return self.toks[self.i + k] if self.i + k < len(self.toks) else (None, None)

    def take(self, val=None):
        tok = self.peek()
        if tok == (None, None) or val is not None and tok[1] != val:
            raise FeelError(f"expected {val or 'more'}, found {tok[1] or 'the end'}")
        self.i += 1
        return tok

    def word_is(self, w):
        return self.peek() == ("word", w)

    def scoped(self, var, kind, body):
        """`body` parsed with `var` bound to `kind`, the binding gone after it."""
        self.bound.append((var, kind))
        try:
            return body()
        finally:
            self.bound.pop()

    def expr(self):
        if self.word_is("if"):
            self.take()
            self._want(self.expr(), "boolean", "an if's condition")
            self.take("then")
            a = self.expr()
            self.take("else")
            return self._same(a, self.expr(), "an if's two outcomes")
        if self.word_is("some") or self.word_is("every") or self.word_is("for"):
            word = self.take()[1]
            var = self.take()[1]
            self.take("in")
            items = self.expr()
            kind = items[1] if isinstance(items, tuple) else None
            if word == "for":
                self.take("return")
                return ("list", self.scoped(var, kind, self.expr))
            self.take("satisfies")
            self._want(self.scoped(var, kind, self.expr), "boolean", "a quantifier's test")
            return "boolean"
        return self.disjunction()

    def disjunction(self):
        a = self.conjunction()
        while self.word_is("or"):
            self.take()
            self._want(a, "boolean", "an or")
            self._want(self.conjunction(), "boolean", "an or")
            a = "boolean"
        return a

    def conjunction(self):
        a = self.comparison()
        while self.word_is("and"):
            self.take()
            self._want(a, "boolean", "an and")
            self._want(self.comparison(), "boolean", "an and")
            a = "boolean"
        return a

    def comparison(self):
        a = self.additive()
        if self.peek()[1] in ("=", "!=", "<", "<=", ">", ">="):
            self.take()
            self._same(a, self.additive(), "a comparison")
            return "boolean"
        return a

    def additive(self):
        a = self.multiplicative()
        while self.peek()[1] in ("+", "-"):
            op = self.take()[1]
            a = self._arith(a, self.multiplicative(), op)
        return a

    def multiplicative(self):
        a = self.unary()
        while self.peek()[1] in ("*", "/"):
            op = self.take()[1]
            a = self._arith(a, self.unary(), op)
        return a

    def unary(self):
        if self.peek()[1] == "-":
            self.take()
            a = self.unary()
            if a is not None and a != "number" and a not in DURATIONS:
                self.problems.append(f"a minus sign before a {_shown(a)}")
            return a
        return self.filtered()

    def filtered(self):
        a = self.primary()
        while self.peek()[1] == "[":
            # a filter, its test reading `item`; an index is no part of the subset
            self.take()
            test = self.scoped("item", a[1] if isinstance(a, tuple) else None, self.expr)
            self.take("]")
            if test is not None and test != "boolean":
                self.problems.append(f"a filter whose test is a {_shown(test)}, not a yes or no")
        return a

    def primary(self):
        kind, val = self.peek()
        if kind == "lit":
            self.take()
            return val
        if kind == "op" and val == "(":
            self.take()
            a = self.expr()
            self.take(")")
            return a
        if kind == "op" and val == "[":
            self.take()
            items = []
            while self.peek()[1] != "]":
                items.append(self.expr())
                if self.peek()[1] == ",":
                    self.take()
            self.take("]")
            known = {k for k in items if k}
            return ("list", known.pop() if len(known) == 1 else None)
        if kind == "word":
            if val == "null":
                self.take()
                return None
            if val in ("true", "false"):
                self.take()
                return "boolean"
            if val == "not" and self.peek(1)[1] == "(":
                self.take()
                self.take("(")
                self._want(self.expr(), "boolean", "a not")
                self.take(")")
                return "boolean"
            return self.name()
        raise FeelError(f"no FEEL expression at: {val or 'the end'}")

    def name(self):
        # a bound name first, innermost first; then a declared name or a function, longest first, a name holding a
        # word FEEL keeps, as `days in arrears` does
        for var, kind in reversed(self.bound):
            if self.peek() == ("word", var):
                self.take()
                return kind
        for n in sorted(set(self.facts) | set(FUNCTIONS), key=lambda n: -len(n.split())):
            parts = n.split()
            if all(self.peek(k) == ("word", p) for k, p in enumerate(parts)):
                self.i += len(parts)
                if n in FUNCTIONS:
                    if self.peek()[1] != "(":
                        self.problems.append(f"a function named without its arguments: {n}")
                        return None
                    return self.call(n)
                return self.facts.get(n)
        words = []
        while self.peek()[0] == "word" and self.peek()[1] not in KEYWORDS:
            words.append(self.take()[1])
        if not words:
            raise FeelError(f"no FEEL expression at: {self.peek()[1] or 'the end'}")
        self.problems.append(f"a name no fact declares: {' '.join(words)}")
        return None

    def call(self, fn):
        self.take("(")
        args = []
        while self.peek()[1] != ")":
            args.append(self.expr())
            if self.peek()[1] == ",":
                self.take()
        self.take(")")
        out = FUNCTIONS[fn]
        if out == "item":
            first = args[0] if args else None
            return first[1] if isinstance(first, tuple) else first
        return out

    def _want(self, a, kind, where):
        if a is not None and a != kind and not isinstance(a, tuple):
            self.problems.append(f"{where} given a {a}, not a {kind}")

    def _same(self, a, b, where):
        if a is not None and b is not None and a != b:
            self.problems.append(f"{where} of a {_shown(a)} and a {_shown(b)}")
            return None
        return a if a is not None else b

    def _arith(self, a, b, op):
        if a is None or b is None:
            return None
        if a == b == "number":
            return "number"
        if op == "+" and a == b == "string":
            return "string"
        if op in "+-" and a in TEMPORAL and b in DURATIONS:
            return a
        if op == "+" and a in DURATIONS and b in TEMPORAL:
            return b
        if op == "-" and a == b and a in TEMPORAL:
            return "days and time duration"
        if op in "+-" and a == b and a in DURATIONS:
            return a
        if op in "*/" and {a, b} <= set(DURATIONS) | {"number"} and "number" in (a, b):
            return a if a in DURATIONS else b
        self.problems.append(f"a {op} of a {_shown(a)} and a {_shown(b)}")
        return None


def _shown(k):
    return f"list of {k[1] or 'values'}" if isinstance(k, tuple) else k


def check(text, facts):
    """A FEEL expression, and each fact it may name with its kind or None -> (its kind or None, [problem])."""
    try:
        p = _Parser(text, facts)
        kind = p.expr()
        if p.i != len(p.toks):
            raise FeelError(f"more after the expression: {p.peek()[1]}")
        return kind, p.problems
    except FeelError as e:
        return None, [f"an expression in no form FEEL has: {e}"]
