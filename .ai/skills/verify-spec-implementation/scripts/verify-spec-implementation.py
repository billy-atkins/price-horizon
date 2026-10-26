#!/usr/bin/env python3
"""verify-spec-implementation's entry script: checks the app-spec annotations in the application's code
against specs/methodology/code.md § Citing the Specs From Code and the form it cites, and lists places
for the reading to look.

The application's code is the code roots, less what is excluded, that the technical specs' stack.md
names, per specs/methodology/spec-placement.md § The Technical Stack. Standard library only, and the
code the skills share. Exit 0 when nothing is found, 1 when something is, 2 for a usage error.

The code the skills share that it imports: code_checks.py, the check and the candidate list, one copy of each, read
through spec_text.py.
"""

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no cache beside the shared code, untracked in the checkout
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from code_checks import check_annotations, list_candidates  # noqa: E402


def report(heading, found):
    print("== " + heading)
    for rel, n, what in found:
        print("%s:%s  %s" % (rel, n, what))
    print("%d found\n" % len(found))
    return 1 if found else 0


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # help and findings may hold a character the console's code page lacks
    parser = argparse.ArgumentParser(prog=Path(argv[0]).name, description=__doc__.rsplit("\n\n", 1)[0] + "\n", formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
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
