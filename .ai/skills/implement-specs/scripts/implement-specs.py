#!/usr/bin/env python3
"""implement-specs' entry script: the design document tooling in .ai/skills/lib/design_documents.py,
reading the design documents that change code, under .ai/plans/implement-specs/. Its actions
are in its --help; --check-constructs among them is design-specs' to run, a code design stating no
construct; --check-work runs the script checks of the code and of the specs in .ai/skills/lib/code_checks.py and
spec_checks.py over the code a design changing it writes."""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no cache beside the shared code, untracked in the checkout
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from design_documents import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv, plans=".ai/plans/implement-specs"))
