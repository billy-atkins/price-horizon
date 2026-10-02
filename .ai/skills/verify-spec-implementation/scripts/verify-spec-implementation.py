#!/usr/bin/env python3
"""verify-spec-implementation's entry script: checks the app-spec annotations in the application's code
against specs/methodology/code.md § Citing the Specs From Code, and lists places for the reading to look.

The application's code is the code roots, less what is excluded, that the technical specs' stack.md
names, per specs/methodology/spec-placement.md § The Technical Stack. Standard library only, and the
code the skills share. Exit 0 when nothing is found, 1 when something is, 2 for a usage error.
"""

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no cache beside the shared code, untracked in the checkout
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from design_documents import lineages  # noqa: E402

STACK = "specs/application/technical/stack.md"
SPECS = ("specs/application/product/", "specs/application/technical/")
RULE = "code.md § Citing the Specs From Code"
# a line naming the tag at all; then the form § Citing the Specs From Code sets for it
TAG = re.compile(r"@app-spec\b")
# a plain comment line only: a documentation comment, /// or //! or /** or /*!, is never one
FORM = re.compile(r"^\s*(?://(?![/!])|#+|--|;+|%+|<!--|/\*(?![*!]))\s*@app-spec (\S.*?)\s*(?:-->|\*/)?\s*$")


def code_roots(root):
    """-> ([code roots], [excluded paths]) from the stack file's table, or None without one."""
    f = root / STACK
    if not f.is_file():
        return None
    tables, cur = [], []
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
        for spec in sorted((root / base).rglob("*.md")):
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


def report(heading, found):
    print("== " + heading)
    for rel, n, what in found:
        print("%s:%s  %s" % (rel, n, what))
    print("%d found\n" % len(found))
    return 1 if found else 0


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # help and findings may hold a character the console's code page lacks
    parser = argparse.ArgumentParser(prog=Path(argv[0]).name, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    parser.add_argument("--check-annotations", action="store_true", help="report each annotation in the code roots that does not follow the rule: malformed, naming nothing that exists, citing no product or technical spec, or out of order; and each code root the stack names that does not exist")
    parser.add_argument("--list-candidates", action="store_true", help="list the spec sections no annotation cites and the files citing none, places for the reading to look; never findings")
    args = parser.parse_args(argv[1:])
    root = Path.cwd()
    if not (args.check_annotations or args.list_candidates):
        parser.print_usage(sys.stderr)
        return 2
    status = 0
    if args.check_annotations:
        status = max(status, report("check-annotations", check_annotations(root)))
    if args.list_candidates:
        report("list-candidates", list_candidates(root))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
