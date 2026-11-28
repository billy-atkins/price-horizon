#!/usr/bin/env python3
"""search-spec-of-record-scope's entry script: the search the skills share, over the files of Spec of Record's scope
and the code. Its actions are in its usage, printed by a run naming none."""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no cache beside the shared code, untracked in the project
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from search import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv))
