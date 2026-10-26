#!/usr/bin/env python3
"""Checks the project against the rules that govern it, mechanically.

Every check enforces one stated rule and names it, so a failure points at the rule
rather than only at a line. Nothing here needs judgment, per
specs/methodology/scope.md § Rules and Skills. `--check-scope` runs the checks, and
`--list-candidates` lists places for a reading audit to look, printed apart from any
finding and never affecting the exit status.

Standard library and the code the skills share in .ai/skills/lib/ only: spec_checks.py, every check and candidate
list it runs, one copy of each; layout.py and record_types.py, the checks of a block of fields and of a blank line it
runs over a file it is given; and spec_text.py, the reading of a spec's text. See SKILL.md.
"""

import argparse
import sys
from pathlib import Path

# the shared code, found from the script's own place, so the script runs the same from any working directory and
# under an interpreter that leaves the script's directory off the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
import layout  # noqa: E402
import spec_checks  # noqa: E402
from record_types import block_findings  # noqa: E402
from spec_text import md_files, read  # noqa: E402


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    # Actions are flags per specs/methodology/skills.md § Authoring a Skill.
    parser = argparse.ArgumentParser(prog="audit-specs.py", description=__doc__.split("\n\n")[0], allow_abbrev=False)
    parser.add_argument("--check-scope", action="store_true",
                        help="check the files Spec of Record governs against every rule the files alone decide, "
                             "each finding named for the rule it breaks; exits 1 on any finding")
    parser.add_argument("--list-candidates", action="store_true",
                        help="list places for the reading audits to look, printed apart from any finding, "
                             "and never itself a finding")
    parser.add_argument("--detail", action="store_true",
                        help="with --list-candidates, list every word and construction Clear Prose has a reader test, "
                             "rather than their count for each file")
    parser.add_argument("--check-layout", nargs="+", metavar="FILE",
                        help="run the layout check and the reader's checks of a block over the given Markdown files alone, "
                             "as the Working-file form audit runs them over .ai/follow-ups.md; exits 1 on any finding")
    parser.add_argument("--root", metavar="DIR", default=".",
                        help="the project root the scope is read from; the current directory unless given")
    args = parser.parse_args(argv[1:])
    if not (args.check_scope or args.list_candidates or args.check_layout):
        parser.print_usage(sys.stderr)
        return 2
    root = Path(args.root).resolve()
    if not (root / "specs").is_dir():
        parser.error(f"--root {args.root} holds no specs/ directory")
    status = 0

    if args.check_layout:
        table, found = layout.rules(root)
        for value in args.check_layout:
            path = Path(value)
            if not path.is_file():
                parser.error(f"--check-layout names no file: {value}")
            body = read(path)
            rel = path.resolve().relative_to(root).as_posix() if path.resolve().is_relative_to(root) else value
            found += [(rule, rel, line, msg) for rule, line, msg in layout.findings(body, table) + block_findings(body)]
        for rule, path, line, msg in sorted(found):
            print(f"{path}:{line}  {rule}\n  {msg}")
        n = len(found)
        print(f"\n{n} finding{'' if n == 1 else 's'} over {len(args.check_layout)} file{'' if len(args.check_layout) == 1 else 's'}")
        status = 1 if n else 0

    if args.check_scope:
        warned = []
        found = spec_checks.check(root, warned)
        by_rule = {}
        for rule, path, line, msg in found:
            by_rule.setdefault(rule, []).append((path, line, msg))
        for rule in sorted(by_rule):
            print(f"\n{rule}")
            for path, line, msg in sorted(by_rule[rule]):
                where = f"{path}:{line}" if line else path
                print(f"  {where}\n    {msg}")
        n = len(found)
        print(f"\n{n} finding{'' if n == 1 else 's'} across {len(md_files(root))} files")
        status = 1 if n else 0
        if warned:
            # a warning is what the specs record as the system's gap: listed on every run, and never a finding
            print(f"\nWarnings, {len(warned)} rule{'' if len(warned) == 1 else 's'} the specs record as kept by nothing; listed, not findings")
            for rule, path, line, msg in sorted(warned):
                print(f"  {path}:{line}\n    {msg}")

    if args.list_candidates:
        for heading, listed, counted in spec_checks.candidate_groups(root):
            if not counted or args.detail:
                print(f"\n{heading}")
                for path, line, name, context in listed:
                    print(f"  {path}:{line}  [{name}]\n    {context}")
                continue
            print(f"\n{heading}; counts for each file, --detail listing each")
            counts = {}
            for path, _, name, _ in listed:
                kind = name.split(":")[0]
                counts.setdefault(path, {}).setdefault(kind, 0)
                counts[path][kind] += 1
            for path in sorted(counts):
                print(f"  {path}: {sum(counts[path].values())}  " + "; ".join(f"{k} {v}" for k, v in sorted(counts[path].items())))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
