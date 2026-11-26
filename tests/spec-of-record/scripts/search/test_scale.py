"""Scale: the memory a search by meaning holds as it computes the vectors its index holds none of, on a body of files
and on ten times as many. The files are copies of the invented library, each copy's files followed by a sentence of
their own, so ten times the copies give ten times the passages without a vector. Each body is searched in a process
of its own, since the most memory a process held never falls again. The test takes a minute or more."""
import json
import subprocess
import sys

import pytest

from search_set import LIB, LIBRARY, READS_LIBRARY, search


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_LIBRARY[0]
@READS_LIBRARY[1]
@pytest.mark.reads("search-scale.md", "measure-a-search-by-meaning")
@pytest.mark.parametrize("copies", [20, 200])
def test_a_search_by_meaning_computing_every_vector_missing_holds_no_more_memory_than_a_process_holding_the_model_is_counted_at(fixtures, work, copies):
    program, texts = work / "measure.py", work / "texts.json"
    work.mkdir(parents=True, exist_ok=True)
    program.write_text(fixtures["measure-a-search-by-meaning"], encoding="utf-8", newline="\n")
    texts.write_text(json.dumps({path: fixtures[key] for key, path in LIBRARY.items()}), encoding="utf-8")
    done = subprocess.run([sys.executable, "-B", str(program), str(LIB), str(work / "files"), str(work / "index"), str(texts), str(copies)],
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, done.stderr
    vectors, memory = done.stdout.split()
    # each copy's file holds a sentence no other file holds, a passage of its own, so the vectors grow with the copies
    assert int(vectors) > copies * len(LIBRARY) and float(memory) <= search.MODEL_MEMORY / 2 ** 30
