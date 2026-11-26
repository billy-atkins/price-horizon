#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment, since a script never
decides one. `--check-scope` runs the checks, and
`--list-candidates` lists places for a reading audit to look, printed apart from any
finding and never affecting the exit status.

Standard library and the code the skills share in .ai/skills/lib/ only: every check and candidate list it runs, one
copy of each; the checks of a block of fields and of a blank line it runs over a file it is given; the reading of a
spec's text; and the kind of change a file is of, which a run's sub-scopes are read by. See the skill's own file.
"""

import argparse
import sys
from pathlib import Path

# the shared code, found from the script's own place, so the script runs the same from any working directory and
# under an interpreter that leaves the script's directory off the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import code_checks  # noqa: E402
import design_documents  # noqa: E402
import layout  # noqa: E402
import spec_checks  # noqa: E402
from record_types import block_findings  # noqa: E402
from spec_text import md_files, read, skill_dirs  # noqa: E402
# the sub-scope names, one copy in the shared code, annotated there to the canon's table of sub-scopes
from design_documents import SUB_SCOPES  # noqa: E402


def in_sub_scope(scope, path, kind):
    """Whether a file, of the kind design_documents.file_kind gives it, lies in the sub-scope a run is given, as
    design_documents.sub_scope_of gives a file its sub-scope."""
    return design_documents.sub_scope_of(path, kind) == scope


def kind_of_file(root):
    """-> a function giving a path's kind of change, the code roots and the registered skills read once."""
    skills, code = skill_dirs(root), code_checks.code_roots(root) or ([], [])
    return lambda path: design_documents.file_kind(path, skills, code)


def check_layout(args, root, keep, files):
    """The layout check and the reader's checks of a block, over the given Markdown files alone -> the exit status."""
    table, problems = layout.rules()
    # the table's own problems, gathered in a list of the action's own, so no finding enters the rules read once
    found = list(problems)
    for value in files:
        path = Path(value)
        if not path.is_file():
            raise SystemExit(f"audit-specs.py: error: --check-layout names no file: {value}")
        body = read(path)
        rel = path.resolve().relative_to(root).as_posix() if path.resolve().is_relative_to(root) else value
        found += [(rule, rel, line, msg) for rule, line, msg in layout.findings(body, table) + block_findings(body)]
    for rule, path, line, msg in sorted(found):
        print(f"{path}:{line}  {rule}\n  {msg}")
    n = len(found)
    print(f"\n{n} finding{'' if n == 1 else 's'} over {len(files)} file{'' if len(files) == 1 else 's'}")
    return 1 if n else 0


def check_scope(args, root, keep, _):
    """Every check of the scope, each finding under its rule, then the warnings apart -> the exit status."""
    warned = []
    found = [f for f in spec_checks.check(root, warned) if keep(f[1])]
    warned = [w for w in warned if keep(w[1])]
    files = [f for f in md_files(root) if keep(f.relative_to(root).as_posix())]
    by_rule = {}
    for rule, path, line, msg in found:
        by_rule.setdefault(rule, []).append((path, line, msg))
    for rule in sorted(by_rule):
        print(f"\n{rule}")
        for path, line, msg in sorted(by_rule[rule]):
            where = f"{path}:{line}" if line else path
            print(f"  {where}\n    {msg}")
    n = len(found)
    print(f"\n{n} finding{'' if n == 1 else 's'} across {len(files)} files")
    if warned:
        # a warning is what the specs record as the system's gap: listed on every run, and never a finding
        print(f"\nWarnings, {len(warned)} rule{'' if len(warned) == 1 else 's'} the specs record as kept by nothing; listed, not findings")
        for rule, path, line, msg in sorted(warned):
            print(f"  {path}:{line}\n    {msg}")
    return 1 if n else 0


def list_candidates(args, root, keep, _):
    """The places for the reading audits to look, apart from any finding -> 0, since a candidate is never one."""
    for heading, listed, counted in spec_checks.candidate_groups(root):
        listed = [c for c in listed if keep(c[0])]
        if not counted or args.detail:
            print(f"\n{heading}")
            for path, line, name, context in listed:
                print(f"  {path}:{line}  [{name}]\n    {context}")
            continue
        print(f"\n{heading}; counts for each file, --detail listing each")
        counts = {}
        for path, _, name, _ in listed:
            group = name.split(":")[0]
            counts.setdefault(path, {}).setdefault(group, 0)
            counts[path][group] += 1
        for path in sorted(counts):
            print(f"  {path}: {sum(counts[path].values())}  " + "; ".join(f"{k} {v}" for k, v in sorted(counts[path].items())))
    return 0


FLAGS = (
    ("--check-scope", None, check_scope,
     "check the files Spec of Record governs against every rule the files alone decide, each finding named for "
     "the rule it breaks; exits 1 on any finding"),
    ("--list-candidates", None, list_candidates,
     "list places for the reading audits to look, printed apart from any finding, and never itself a finding"),
    ("--check-layout", "FILE", check_layout,
     "run the layout check and the reader's checks of a block over the given Markdown files alone, as the "
     "Working-file form audit runs them over the follow-ups; exits 1 on any finding"),
)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    parser = argparse.ArgumentParser(prog="audit-specs.py", description=__doc__.split("\n\n")[0], allow_abbrev=False)
    for flag, metavar, _, help_text in FLAGS:
        if metavar:
            parser.add_argument(flag, nargs="+", metavar=metavar, help=help_text)
        else:
            parser.add_argument(flag, action="store_true", help=help_text)
    parser.add_argument("--detail", action="store_true",
                        help="with --list-candidates, list every word and construction Clear Prose has a reader test, "
                             "rather than their count for each file")
    parser.add_argument("--sub-scope", nargs="+", choices=SUB_SCOPES,
                        help="with --check-scope or --list-candidates, report only the findings, warnings or "
                             "candidates in the files of the sub-scopes given, the checks still run over the whole of "
                             "Spec of Record's scope; every one unless given")
    parser.add_argument("--root", metavar="DIR", default=".",
                        help="the project root the scope is read from; the current directory unless given")
    args = parser.parse_args(argv[1:])
    chosen = [(run, getattr(args, flag[2:].replace("-", "_"))) for flag, _, run, _ in FLAGS]
    chosen = [(run, value) for run, value in chosen if value]
    if not chosen:
        parser.print_usage(sys.stderr)
        return 2
    root = Path(args.root).resolve()
    if not (root / "specs").is_dir():
        parser.error(f"--root {args.root} holds no specs/ directory")
    # a test of a path, true of every path where no sub-scope is given
    if args.sub_scope:
        kind = kind_of_file(root)
        keep = lambda path: any(in_sub_scope(s, path, kind(path)) for s in args.sub_scope)  # noqa: E731
    else:
        keep = lambda path: True  # noqa: E731
    return max(run(args, root, keep, value) for run, value in chosen)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
