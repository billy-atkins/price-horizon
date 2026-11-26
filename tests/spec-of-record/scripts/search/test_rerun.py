"""The index: built whole on a first search, read again only for the files that changed, and every result written
before a change cleared with it."""
import pytest

from search_set import CORPUS, READS_CORPUS, every_file, project

pytestmark = READS_CORPUS
CITED = "specs/target.md § Target"
CHANGED = pytest.mark.reads("search-changed-files.md", "target-spec-citing-its-own-section")


def corpus(work, fixtures):
    return project(work / "project", fixtures, CORPUS)


def changed(root, fixtures):
    """The corpus's target spec changed: it gains a line citing its own section."""
    project(root, fixtures, {"target-spec-citing-its-own-section": CORPUS["target-spec"]})


def test_a_first_search_builds_the_index_whole_reading_every_file(fixtures, opened, work):
    root = corpus(work, fixtures)
    s = opened(root, cover=every_file(root), scratch=work / "index")
    assert s.built and s.read_count == len(CORPUS)


def test_a_search_over_files_unchanged_since_the_last_reads_no_file_again(fixtures, opened, work):
    root = corpus(work, fixtures)
    opened(root, cover=every_file(root), scratch=work / "index").db.close()
    s = opened(root, cover=every_file(root), scratch=work / "index")
    assert not s.built and s.read_count == 0


@CHANGED
def test_a_search_after_one_file_changed_reads_that_file_alone(fixtures, opened, work):
    root = corpus(work, fixtures)
    opened(root, cover=every_file(root), scratch=work / "index").db.close()
    changed(root, fixtures)
    assert opened(root, cover=every_file(root), scratch=work / "index").read_count == 1


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@CHANGED
def test_a_file_changed_clears_every_result_written_before_one_of_a_question_not_asked_again_among_them(fixtures, opened, work):
    root = corpus(work, fixtures)
    first = opened(root, cover=every_file(root), scratch=work / "index")
    asked = first.terms("posting").path
    first.db.close()
    changed(root, fixtures)
    opened(root, cover=every_file(root), scratch=work / "index")
    assert asked.parent.is_dir() and not asked.exists() and not list(asked.parent.glob("*.md"))


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@CHANGED
def test_a_result_keeps_its_name_while_its_content_stands_and_takes_another_once_it_changes(fixtures, opened, work):
    root = corpus(work, fixtures)
    first = opened(root, cover=every_file(root), scratch=work / "index")
    name = first.citers(CITED).name
    first.db.close()
    again = opened(root, cover=every_file(root), scratch=work / "index")
    assert again.citers(CITED).name == name
    again.db.close()
    changed(root, fixtures)
    assert opened(root, cover=every_file(root), scratch=work / "index").citers(CITED).name != name
