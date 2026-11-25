"""The index: what a run reads again, and which results a changed file clears."""
import pytest


@pytest.mark.action("--show-citers", "--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary")
@pytest.mark.reads("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")
def test_a_run_reads_again_only_the_files_that_changed_and_clears_the_results_written_before(fixtures, tools, opened, work, check):
    # the corpus of nine files, of which the test changes one: the target spec gains a sentence citing its own section
    root, scratch = tools.a_corpus(work / "project", fixtures), work / "index"
    files_under = tools.files_under
    first = opened(root, cover=files_under(root), scratch=scratch)
    check("the first use builds the whole index, reading every file", first.built and first.read_count == len(files_under(root)), first.read_count)
    name = first.citers("specs/target.md § Target").name
    other = first.terms("posting").name
    first.db.close()
    second = opened(root, cover=files_under(root), scratch=scratch)
    check("on unchanged files a run reads no file again", second.read_count == 0 and not second.built, second.read_count)
    check("and writes a result of the same name", second.citers("specs/target.md § Target").name == name)
    second.db.close()
    tools.put(root, "specs/target.md", fixtures["target-spec"] + "\nA line added, citing `specs/target.md § Target` from its own file.\n")
    third = opened(root, cover=files_under(root), scratch=scratch)
    check("after one file changes a run reads that file alone", third.read_count == 1, third.read_count)
    check("and clears every result written before the change, a result of a question not asked again among them",
          not (scratch / "results" / other).exists() and not list((scratch / "results").glob("*.md")), list((scratch / "results").glob("*.md")))
    changed = third.citers("specs/target.md § Target")
    check("and the result's name differs once its content does", changed.name != name and not (scratch / "results" / name).exists(), changed.name)
