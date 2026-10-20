#!/usr/bin/env python3
"""design-specs' entry script: the design document tooling in .ai/skills/lib/design_documents.py,
reading the design documents that change the specs, under .ai/plans/design-specs/. Its actions
are in its --help."""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no cache beside the shared code, untracked in the checkout
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from design_documents import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv, plans=".ai/plans/design-specs"))
