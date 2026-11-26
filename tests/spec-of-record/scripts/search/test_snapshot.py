"""The snapshot code: the state of a target's files, on every result and on request.

Each test writes its own small project: a spec naming a heron, code under the stack's one code root and code beside
it, and two plans citing the spec's section. A test committing it commits the specs and the code alone, so the files
as they stand and the files the last commit held hold the same until the test writes a file over."""
import os

import pytest

from search_set import HERON, READS_HERON, ask, git, project, search

pytestmark = READS_HERON
SECTION = "specs/target.md § Target"
DESIGNS = [".ai/plans/design-specs"]


def heron(work, fixtures, committed=False):
    root = project(work / "project", fixtures, HERON)
    if committed:
        git(root, "init", "-q")
        git(root, "add", "specs", "code")
        git(root, "commit", "-q", "-m", "first")
    return root


def code_of(root, work, **given):
    """-> the snapshot code the search gives on request, from the test's own index."""
    return search.snapshot(root, scratch=work / "index", **given)


def result_code(opened, root, work):
    """-> the snapshot code a result of the files as they stand carries, its index closed after."""
    s = opened(root, scratch=work / "index")
    code = s.terms("heron").snapshot
    s.db.close()
    return code


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_every_result_carries_a_snapshot_code_of_sixteen_hexadecimal_digits(fixtures, opened, work):
    assert search.SNAPSHOT.fullmatch(opened(heron(work, fixtures), scratch=work / "index").terms("heron").snapshot or "")


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.passes
def test_one_code_stands_for_the_whole_target_whatever_a_search_was_narrowed_to_and_whatever_its_kind(fixtures, opened, work):
    s = opened(heron(work, fixtures), scratch=work / "index")
    narrow = s.terms("heron", ["specs"])
    assert narrow.narrowed == ["specs"] and s.terms("heron").snapshot == narrow.snapshot == s.citers(SECTION).snapshot


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
def test_the_code_given_on_request_is_a_result_s_while_no_file_of_the_target_holds_anything_new(fixtures, opened, work):
    root = heron(work, fixtures)
    assert code_of(root, work) == result_code(opened, root, work)


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
def test_show_snapshot_code_prints_the_code_built_from_the_files_by_an_index_of_its_own(fixtures, work, capsys):
    root = heron(work, fixtures)
    code = code_of(root, work)
    assert ask(root, "--show-snapshot-code") == 0
    assert code in capsys.readouterr().out.split("\n")


@pytest.mark.action("--show-snapshot-code", "--show-term-uses")
@pytest.mark.passes
def test_the_files_the_last_commit_held_take_the_code_the_files_as_they_stand_take_each_file_holding_the_same(fixtures, opened, work):
    root = heron(work, fixtures, committed=True)
    code = code_of(root, work)
    committed = opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE).terms("heron").snapshot
    assert committed == code == code_of(root, work, target=search.COMMITTED_OPERATIVE)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_a_file_whose_time_of_change_alone_moved_is_read_again_and_leaves_the_code_as_it_was(fixtures, opened, work):
    root = heron(work, fixtures)
    code = result_code(opened, root, work)
    held = (root / "specs" / "target.md").stat()
    os.utime(root / "specs" / "target.md", ns=(held.st_atime_ns + 5_000_000_000, held.st_mtime_ns + 5_000_000_000))
    s = opened(root, scratch=work / "index")
    assert s.read_count == 1 and s.terms("heron").snapshot == code


@pytest.mark.action("--show-snapshot-code", "--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "heron-spec-with-an-egret-not-yet-committed")
def test_once_a_file_of_the_target_holds_something_new_the_code_differs_on_a_result_and_on_request(fixtures, opened, work):
    root = heron(work, fixtures)
    code = result_code(opened, root, work)
    project(root, fixtures, {"heron-spec-with-an-egret-not-yet-committed": HERON["heron-spec"]})
    after = result_code(opened, root, work)
    assert after != code and code_of(root, work) == after


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "heron-spec-with-an-egret-not-yet-committed")
def test_the_code_of_the_committed_files_stands_while_no_commit_changed_them(fixtures, work):
    root = heron(work, fixtures, committed=True)
    code = code_of(root, work, target=search.COMMITTED_OPERATIVE)
    project(root, fixtures, {"heron-spec-with-an-egret-not-yet-committed": HERON["heron-spec"]})
    assert code_of(root, work, target=search.COMMITTED_OPERATIVE) == code


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "heron-spec-with-an-egret-not-yet-committed")
def test_a_file_brought_back_to_what_it_held_brings_the_code_back(fixtures, work):
    root = heron(work, fixtures)
    code = code_of(root, work)
    project(root, fixtures, {"heron-spec-with-an-egret-not-yet-committed": HERON["heron-spec"]})
    code_of(root, work)
    project(root, fixtures, {"heron-spec": HERON["heron-spec"]})
    assert code_of(root, work) == code


@pytest.mark.action("--show-snapshot-code", "--show-term-uses")
@pytest.mark.passes
def test_a_result_of_the_working_files_holds_the_code_of_the_paths_it_names_which_the_search_gives_on_request_for_them(fixtures, opened, work):
    root = heron(work, fixtures)
    s = opened(root, scratch=work / "index", target=search.WORKING, paths=DESIGNS)
    one = s.terms("heron").snapshot
    s.db.close()
    assert search.SNAPSHOT.fullmatch(one) and one != code_of(root, work)
    assert code_of(root, work, target=search.WORKING, paths=DESIGNS) == one


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
def test_other_paths_of_the_working_files_take_another_code(fixtures, work):
    root = heron(work, fixtures)
    assert code_of(root, work, target=search.WORKING, paths=[".ai/plans"]) != code_of(root, work, target=search.WORKING, paths=DESIGNS)


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "plan-naming-the-heron-changed", "heron-spec-changed-in-the-reeds")
@pytest.mark.parametrize("key, path", [("plan-naming-the-heron-changed", HERON["plan-citing-the-heron"]), ("heron-spec-changed-in-the-reeds", HERON["heron-spec"])],
                         ids=["a-working-file-outside-the-paths", "an-operative-file"])
def test_a_file_changed_outside_the_paths_named_leaves_the_code_of_the_working_files_as_it_was(fixtures, work, key, path):
    root = heron(work, fixtures)
    one = code_of(root, work, target=search.WORKING, paths=DESIGNS)
    project(root, fixtures, {key: path})
    assert code_of(root, work, target=search.WORKING, paths=DESIGNS) == one


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "design-naming-the-heron-changed")
def test_a_working_file_changed_under_the_paths_named_changes_their_code(fixtures, work):
    root = heron(work, fixtures)
    one = code_of(root, work, target=search.WORKING, paths=DESIGNS)
    project(root, fixtures, {"design-naming-the-heron-changed": HERON["design-citing-the-heron"]})
    assert code_of(root, work, target=search.WORKING, paths=DESIGNS) != one


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.reports
def test_show_snapshot_code_refuses_the_committed_files_of_a_project_under_no_version_control_leaving_no_index(fixtures, work, capsys):
    # the project stands below the run's folder, above which git is kept from looking, and holds no repository
    root = heron(work, fixtures)
    assert ask(root, "--show-snapshot-code", "--target", search.COMMITTED_OPERATIVE) == 1
    printed = capsys.readouterr().out
    assert "under no version control the search reads" in printed and not any(search.SNAPSHOT.fullmatch(line) for line in printed.split("\n"))
    assert not (root / search.SCRATCH).exists()
