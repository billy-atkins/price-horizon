"""The script check and candidate list of the code, one copy of each, that .ai/skills/verify-spec-implementation/ runs
over the application's code and .ai/skills/design-specs/' and .ai/skills/implement-specs/' scripts run over a design's
work: the app-spec annotations checked against the canon's rule for citing the specs from code and the form it cites,
and places listed for the reading to look.

The application's code is the code roots, less what is excluded, that the technical specs' stack document names, its
stack.md or the files of a folder named for it. A check reads the tree it is given as its root, the working tree or the
last commit read through spec_text.CommitTree. Standard library only, and the shared reading of a spec's text.
"""
import ast
import io
import re
import tokenize

import reading
from spec_text import indexed, lineages

STACK = "specs/application/technical/stack.md"
# the stack document laid out as a folder, its code roots in whichever of its files holds them, its main file
# where it holds one among them
STACK_FOLDER = "specs/application/technical/stack/"
# @canon-spec specs/methodology/code.md § Citing the Specs From Code
SPECS = ("specs/application/product/", "specs/application/technical/")
RULE = "code.md § Citing the Specs From Code"
STACK_RULE = "spec-placement/technical-stack.md § The Technical Stack"
# a line naming the tag at all; then the form the canon sets for it
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
TAG = re.compile(r"@app-spec\b")
# a plain comment line only: a documentation comment, /// or //! or /** or /*!, is never one
FORM = re.compile(reading.COMMENT + r"@app-spec (\S.*?)" + reading.COMMENT_END)  # the comment an annotation is, the one reading's form


def code_roots(root):
    """-> ([code roots], [excluded paths]) from the stack document's table, read from stack.md or across the files of
    the folder named for it, or None without one."""
    f, folder = root / STACK, root / STACK_FOLDER
    if f.is_file():
        files = [f]
    elif folder.is_dir():
        files = sorted(folder.rglob("*.md"), key=lambda p: (p.name != "main.md", p.as_posix()))
    else:
        return None
    tables, cur = [], []
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines() + [""]:
            if line.startswith("|"):
                cur.append(line)
            elif cur:
                tables.append(cur)
                cur = []
    rows = next((t for t in tables if "Code Roots" in [c.strip() for c in t[0].strip("|").split("|")]), None)
    if not rows:
        return None
    head = [c.strip() for c in rows[0].strip("|").split("|")]
    r, x = head.index("Code Roots"), head.index("Excluded") if "Excluded" in head else None
    roots, excluded = [], []
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        roots += re.findall(r"`([^`]+)`", cells[r] if r < len(cells) else "")
        if x is not None and x < len(cells):
            excluded += re.findall(r"`([^`]+)`", cells[x])
    roots = [p.rstrip("/") for p in roots]
    return (roots, [p.rstrip("/") for p in excluded]) if roots else None


def missing_roots(root, roots, excluded):
    return [("stack.md", 0, "names a code root that does not exist: " + r) for r in roots if not (root / r).exists()]


def code_files(root, roots, excluded):
    for r in roots:
        base = root / r
        for f in sorted(base.rglob("*")) if base.is_dir() else ([base] if base.is_file() else []):
            rel = f.relative_to(root).as_posix()
            if f.is_file() and not any(rel == e or rel.startswith(e + "/") for e in excluded):
                yield f, rel


def annotations(f):
    """-> [(line number, line)] of every line naming the tag."""
    try:
        text = f.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return []
    return [(n, line) for n, line in enumerate(text.split("\n"), 1) if TAG.search(line)]


def rule_of(finding):
    """-> the section a finding of check_annotations enforces: the technical stack's for a finding on the stack
    file, the annotations' rule for any other."""
    return STACK_RULE if finding[0] == "stack.md" else RULE


# @canon-spec specs/methodology/code.md § Citing the Specs From Code
def check_annotations(root):
    stack = code_roots(root)
    if stack is None:
        return [("stack.md", 0, "no stack file naming a code root: " + STACK)]
    found, heads = missing_roots(root, *stack), {}
    for f, rel in code_files(root, *stack):
        run = []
        for n, line in annotations(f) + [(None, None)]:
            m = FORM.match(line) if line is not None else None
            if line is not None and not m:
                found.append((rel, n, "not an annotation in the form the rule sets: " + line.strip()))
            if m and run and run[-1][0] == n - 1:
                run.append((n, m.group(1)))
            else:
                if len(run) > 1 and [c for _, c in run] != sorted(c for _, c in run):
                    found.append((rel, run[0][0], "annotations not in plain character order"))
                run = [(n, m.group(1))] if m else []
            if not m:
                continue
            path, _, target = (s.strip() for s in m.group(1).partition(" § "))
            if not path.startswith(SPECS) or not path.endswith(".md"):
                found.append((rel, n, "cites no product or technical spec: " + m.group(1)))
                continue
            if path not in heads:
                spec = root / path
                heads[path] = lineages(spec.read_text(encoding="utf-8")) if spec.is_file() else None
            if heads[path] is None:
                found.append((rel, n, "names no file that exists: " + path))
            elif target and target not in heads[path]:
                found.append((rel, n, "names no section that exists: " + m.group(1)))
    return found


def list_candidates(root):
    stack = code_roots(root)
    if stack is None:
        return [("stack.md", 0, "no stack file naming a code root: " + STACK)]
    cited, out = set(), []
    for f, rel in code_files(root, *stack):
        marks = [FORM.match(line) for _, line in annotations(f)]
        marks = [m.group(1) for m in marks if m]
        if not marks:
            out.append((rel, 0, "a file citing no spec: wiring, or governed code missing its annotations"))
        cited.update(marks)
    whole = {c for c in cited if " § " not in c}
    for base in SPECS:
        for spec in sorted(indexed(root, base.rstrip("/"))):
            rel = spec.relative_to(root).as_posix()
            if spec.name == "index.md" or rel in whole:
                continue
            own = [c.split(" § ", 1)[1] for c in cited if c.startswith(rel + " § ")]
            for lin in sorted(lineages(spec.read_text(encoding="utf-8"))):
                # a section is covered by its own citation, or by one of the section it sits under
                # or of one beneath it; a Test Scenarios section, which a test cites, only by its own
                if lin in own:
                    continue
                if not lin.endswith("Test Scenarios") and any(lin.startswith(c + " § ") or c.startswith(lin + " § ") for c in own):
                    continue
                out.append((rel, 0, "a section no annotation cites: § " + lin))
    return out


def canon_names(canon):
    """-> one pattern matching each of the canon's files by its path and by its file name, standing apart from the
    characters a path is made of on each side."""
    names = sorted({n for p in canon for n in (p, p.rsplit("/", 1)[-1])}, key=len, reverse=True)
    return re.compile(r"(?<![\w./-])/?(?:" + "|".join(re.escape(n) for n in names) + r")(?![\w-])") if names else None


def docstring_lines(text):
    """-> the numbers of the lines a docstring stands on, of the module, of each class and of each function."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return set()
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                out.update(range(first.lineno, first.end_lineno + 1))
    return out


def comment_lines(text):
    """-> {line number: the comment} of each comment the tokenizer finds, on a line of its own or after code."""
    out = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                out[tok.start[0]] = tok.string
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return out


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
def canon_named_outside_an_annotation(path, text, canon):
    """Each line of a Python file naming a section of the canon by a section sign, or a file of the canon by its path
    or its file name, in a comment or a docstring that is no spec annotation -> [(line number, the line)]. A comment
    is read by the standard library's tokenizer, after code on its line or on a line of its own, and a docstring by
    its parser. A comment is an annotation only where the one reading's form reads one, a comment on a line of its
    own, which stays as it is. canon is the canon's files by path from the project's root, each matched by its path
    and by its file name; path names the file checked, read as Python only where it is a Python file."""
    if not path.endswith(".py"):
        return []
    lines, names = text.split("\n"), canon_names(canon)
    def names_canon(s):
        return "§" in s or bool(names and names.search(s))
    found = {}
    for n, comment in comment_lines(text).items():
        line = lines[n - 1]
        if line.strip().startswith("#") and reading.ANNOTATION.match(line):
            continue
        if names_canon(comment):
            found[n] = line
    for n in docstring_lines(text):
        if n <= len(lines) and names_canon(lines[n - 1]):
            found[n] = lines[n - 1]
    return sorted(found.items())
