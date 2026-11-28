"""The answers the search keeps: given again while nothing changed, computed anew once anything did.

Each test writes its own small project: a spec whose section Target holds a sentence about a heron and is cited from
the spec's own file, code under the stack's one code root defining a class Heron and a function constructing it, code
beside that root, and two plans citing the section. A test committing it commits the specs and the code alone."""
import os

import pytest

from search_set import HERON, git, project, search

SECTION = "specs/target.md § Target"
KEPT = dict({k: p for k, p in HERON.items() if k not in ("heron-spec", "heron-function")},
            **{"heron-spec-cited-in-its-own-file": HERON["heron-spec"], "heron-class": HERON["heron-function"]})
pytestmark = pytest.mark.reads("search-heron-project.md", *KEPT)
SECOND_HERON = pytest.mark.reads("search-changed-files.md", "heron-spec-cited-in-its-own-file-with-a-second-heron")
WORKING = {"target": search.WORKING, "paths": [".ai/plans/design-specs"]}

# each kind of search whose answer the search keeps, as one question of it
KINDS = [pytest.param(ask, marks=pytest.mark.action(flag), id=kind) for kind, flag, ask in (
    ("citers", "--show-citers", lambda s: s.citers(SECTION)),
    ("cited-sections", "--show-cited-sections", lambda s: s.cited_sections()),
    ("lines", "--show-lines", lambda s: s.lines(SECTION)),
    ("terms", "--show-term-uses", lambda s: s.terms("heron")),
    ("code-structure", "--show-code-structure", lambda s: s.code_structure("defines", "heron")),
    ("pattern", "--show-pattern-matches", lambda s: s.pattern("heron +stands")))]


def heron(work, fixtures, committed=False):
    root = project(work / "project", fixtures, KEPT)
    if committed:
        git(root, "init", "-q")
        git(root, "add", "specs", "code")
        git(root, "commit", "-q", "-m", "first")
    return root


def same_answer(one, other):
    """-> whether two results give the same answer: the same body, places, notes and names of nothing."""
    def places(r):
        return [(str(p),) + tuple(getattr(p, name, None) for name in ("path", "first", "last", "lineage", "key", "stands")) for p in r.places]
    return one.body() == other.body() and places(one) == places(other) and one.notes == other.notes and one.names_nothing == other.names_nothing


@pytest.mark.passes
@pytest.mark.parametrize("ask", KINDS)
def test_an_answer_asked_first_is_computed_and_not_kept(fixtures, opened, work, ask):
    s = opened(heron(work, fixtures), scratch=work / "index")
    assert not ask(s).kept and s.computed == 1


@pytest.mark.passes
@pytest.mark.parametrize("ask", KINDS)
def test_an_answer_asked_again_while_the_files_stand_is_the_one_kept_computing_nothing_anew(fixtures, opened, work, ask):
    s = opened(heron(work, fixtures), scratch=work / "index")
    first, again = ask(s), ask(s)
    assert again.kept and s.computed == 1
    assert same_answer(first, again) and again.name == first.name and again.path.is_file()


@pytest.mark.passes
@pytest.mark.parametrize("ask", KINDS)
def test_a_later_search_gives_the_kept_answer_computing_nothing_and_the_same_as_an_index_built_anew_computes(fixtures, opened, work, ask):
    root = heron(work, fixtures)
    ask(opened(root, scratch=work / "index"))
    later = opened(root, scratch=work / "index")
    kept, fresh = ask(later), ask(opened(root, scratch=work / "index-fresh"))
    assert kept.kept and later.computed == 0
    assert not fresh.kept and same_answer(kept, fresh)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_a_kept_answer_is_no_result_s_file_and_is_given_with_every_result_s_file_gone_its_file_written_again(fixtures, opened, work):
    s = opened(heron(work, fixtures), scratch=work / "index")
    s.terms("heron")
    for written in (work / "index" / "results").glob("*.md"):
        written.unlink()
    again = s.terms("heron")
    assert again.kept and again.path.is_file()


@pytest.mark.action("--show-term-uses", "--show-pattern-matches")
@pytest.mark.passes
@pytest.mark.parametrize("ask", [lambda s: s.terms("egret"), lambda s: s.terms("reeds"), lambda s: s.terms("heron", ["specs"]), lambda s: s.pattern("heron")],
                         ids=["other-words", "other-words-again", "narrowed-to-other-paths", "of-another-kind"])
def test_a_question_differing_in_what_was_asked_its_paths_or_its_kind_is_computed_anew_and_kept_as_one_of_its_own(fixtures, opened, work, ask):
    s = opened(heron(work, fixtures), scratch=work / "index")
    s.terms("heron")
    assert not ask(s).kept and s.computed == 2
    assert ask(s).kept and s.terms("heron").kept and s.computed == 2


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_an_answer_kept_for_the_files_as_they_stand_is_none_for_the_committed_files(fixtures, opened, work):
    root = heron(work, fixtures, committed=True)
    opened(root, scratch=work / "index").terms("heron")
    committed = opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE)
    assert not committed.terms("heron").kept and committed.terms("heron").kept


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_an_answer_kept_for_the_last_commit_is_none_for_a_search_naming_that_commit(fixtures, opened, work):
    root = heron(work, fixtures, committed=True)
    last = opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE)
    last.terms("heron")
    named = opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE, commit=last.commit).terms("heron")
    assert not named.kept and named.commit == last.commit


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_a_file_whose_time_of_change_alone_moved_leaves_the_kept_answer_standing(fixtures, opened, work):
    root = heron(work, fixtures)
    opened(root, scratch=work / "index").terms("heron")
    held = (root / "specs" / "target.md").stat()
    os.utime(root / "specs" / "target.md", ns=(held.st_atime_ns + 5_000_000_000, held.st_mtime_ns + 5_000_000_000))
    s = opened(root, scratch=work / "index")
    assert s.read_count == 1 and s.terms("heron").kept


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.passes
@SECOND_HERON
def test_once_a_file_of_the_target_holds_something_new_each_answer_is_computed_anew_and_then_kept(fixtures, opened, work):
    root = heron(work, fixtures)
    before = opened(root, scratch=work / "index")
    before.terms("heron"), before.citers(SECTION)
    project(root, fixtures, {"heron-spec-cited-in-its-own-file-with-a-second-heron": "specs/target.md"})
    s = opened(root, scratch=work / "index")
    terms = s.terms("heron")
    assert not terms.kept and len([p for p in terms.places if p.path == "specs/target.md"]) == 2 and not s.citers(SECTION).kept
    assert s.terms("heron").kept


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@SECOND_HERON
def test_an_answer_kept_for_the_committed_files_stands_while_no_commit_changed_them_whatever_the_files_as_they_stand_hold(fixtures, opened, work):
    root = heron(work, fixtures, committed=True)
    opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE).terms("heron")
    project(root, fixtures, {"heron-spec-cited-in-its-own-file-with-a-second-heron": "specs/target.md"})
    assert opened(root, scratch=work / "index", target=search.COMMITTED_OPERATIVE).terms("heron").kept


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_once_the_search_s_own_code_changed_a_kept_answer_is_not_given(fixtures, opened, work, monkeypatch):
    s = opened(heron(work, fixtures), scratch=work / "index")
    s.terms("heron")
    monkeypatch.setattr(search, "_OWN_READING", "0" * 16)   # the search's own code as another copy of it holds it
    assert not s.terms("heron").kept


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_an_answer_another_code_of_the_search_computed_is_not_given_by_this_code_which_computes_its_own_and_keeps_it(fixtures, opened, work, monkeypatch):
    s = opened(heron(work, fixtures), scratch=work / "index")
    with monkeypatch.context() as another_copy:
        another_copy.setattr(search, "_OWN_READING", "0" * 16)
        s.terms("heron")
    assert not s.terms("heron").kept and s.terms("heron").kept


def test_the_code_of_the_search_s_own_reading_is_built_again_the_same_from_its_script_and_the_shared_modules_it_imports(monkeypatch):
    held = search.own_reading()
    monkeypatch.setattr(search, "_OWN_READING", None)
    assert search.own_reading() == held and search.SNAPSHOT.fullmatch(held)


@pytest.mark.action("--show-similar-passages", "--show-code-structure")
@pytest.mark.passes
@pytest.mark.parametrize("ask", [lambda s: s.meaning("The heron stands in the reeds."), lambda s: s.code_structure("constructs", "Heron")],
                         ids=["by-meaning", "for-constructions"])
def test_no_answer_is_kept_of_a_search_by_meaning_or_of_one_for_constructions(fixtures, opened, work, ask):
    s = opened(heron(work, fixtures), scratch=work / "index")
    first, again = ask(s), ask(s)
    assert first.places and not first.kept and not again.kept and s.computed == 2


@pytest.mark.action("--show-term-uses", "--show-similar-passages", "--show-code-structure")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "plan-holding-a-class-line")
def test_after_another_target_s_files_changed_a_kept_kind_gives_what_it_kept_and_the_others_are_computed_anew(fixtures, opened, work):
    root = heron(work, fixtures)
    first = opened(root, scratch=work / "index")
    first.terms("heron"), first.meaning("The heron stands in the reeds."), first.code_structure("constructs", "Heron")
    project(root, fixtures, {"plan-holding-a-class-line": HERON["plan-citing-the-heron"]})
    opened(root, scratch=work / "index", target=search.WORKING, paths=[".ai/plans"]).terms("heron")
    s = opened(root, scratch=work / "index")
    meaning, constructs = s.meaning("The heron stands in the reeds."), s.code_structure("constructs", "Heron")
    assert not meaning.kept and not constructs.kept and s.terms("heron").kept and s.computed == 2


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_an_answer_of_a_search_of_the_working_files_is_kept(fixtures, opened, work):
    s = opened(heron(work, fixtures), scratch=work / "index", **WORKING)
    first = s.citers(SECTION)
    assert not first.kept and len(first.places) == 1 and s.citers(SECTION).kept


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@pytest.mark.reads("search-changed-files.md", "heron-spec-retitled")
def test_an_answer_of_the_working_files_is_computed_anew_once_an_operative_file_it_reads_citations_against_changed(fixtures, opened, work):
    root = heron(work, fixtures)
    opened(root, scratch=work / "index", **WORKING).citers(SECTION)
    project(root, fixtures, {"heron-spec-retitled": HERON["heron-spec"]})
    s = opened(root, scratch=work / "index", **WORKING)
    answer = s.citers(SECTION)
    assert s.read_count == 1 and not answer.kept and any("does not resolve" in n for n in answer.notes)
