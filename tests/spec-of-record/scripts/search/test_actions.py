"""Each action of the search's entry script, asked of `main` over a small project of fixtures: once where it answers,
and once where it refuses what it is given or has nothing to give; and the entry script's wiring, run as a process.
The actions on what the search requires and on the snapshot code are held the same two ways by the tests of those
subjects.

The file's tests share one small project, written once in the file's folder; none changes a file of it."""
import pytest

from search_set import HERON, READS_HERON, ask, printed_places, project, result_file, run_entry, search

pytestmark = READS_HERON
SECTION = "specs/target.md § Target"
WORKING = ("--target", search.WORKING, "--paths", ".ai/plans")


@pytest.fixture
def heron(shared, fixtures):
    """-> the root of the small project: a spec naming a heron, code under the stack's one code root and code beside
    it, and two plans citing the spec's section."""
    return shared.once("heron", lambda: project(shared.folder / "heron", fixtures, HERON))


@pytest.mark.parametrize("argv", [[], ["--show-everything"], ["--show-citers"], ["--show-lines", SECTION, "and one value more"]])
def test_a_run_naming_no_action_one_not_stated_or_the_wrong_values_prints_the_usage(heron, capsys, argv):
    assert ask(heron, *argv) == 2
    printed = capsys.readouterr().out
    assert printed.startswith("usage:") and all(flag in printed for flag, _, _, _ in search.FLAGS)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_show_citers_lists_the_places_citing_a_section(heron, capsys):
    assert ask(heron, "--show-citers", SECTION, *WORKING) == 0
    printed = capsys.readouterr().out
    assert "2 places, complete: places to read, never findings" in printed
    assert printed_places(printed) == ["`.ai/plans/design-specs/a-design.md § The Problem` line 5", "`.ai/plans/other-plan.md § Notes` line 5"]


@pytest.mark.action("--show-citers")
@pytest.mark.reports
def test_show_citers_refuses_a_target_that_is_none(heron, capsys):
    assert ask(heron, "--show-citers", SECTION, "--target", "every-file") == 2
    printed = capsys.readouterr().out
    assert "no target `every-file`: a target is one of" in printed and not printed_places(printed)


@pytest.mark.action("--show-cited-sections")
@pytest.mark.passes
def test_show_cited_sections_lists_each_citing_place_with_what_it_cites(heron, capsys):
    assert ask(heron, "--show-cited-sections", *WORKING) == 0
    assert printed_places(capsys.readouterr().out) == [f"`.ai/plans/design-specs/a-design.md § The Problem` line 5 cites `{SECTION}`",
                                                       f"`.ai/plans/other-plan.md § Notes` line 5 cites `{SECTION}`"]


@pytest.mark.action("--show-cited-sections")
@pytest.mark.reports
def test_show_cited_sections_refuses_the_working_files_given_no_path(heron, capsys):
    assert ask(heron, "--show-cited-sections", "--target", search.WORKING) == 2
    printed = capsys.readouterr().out
    assert "is given none: name them with --paths" in printed and not printed_places(printed)


@pytest.mark.action("--show-lines")
@pytest.mark.passes
def test_show_lines_gives_the_lines_a_citation_names(heron, capsys):
    assert ask(heron, "--show-lines", SECTION) == 0
    assert printed_places(capsys.readouterr().out) == [f"`{SECTION}` lines 3-6"]


@pytest.mark.action("--show-lines")
@pytest.mark.reports
def test_show_lines_says_a_citation_names_no_place(heron, capsys):
    assert ask(heron, "--show-lines", "specs/target.md § Egrets") == 0
    printed = capsys.readouterr().out
    assert "0 places, complete" in printed and not printed_places(printed)
    assert "the question names nothing to ask of: " + search.NO_PLACE in printed and "holds no section `Egrets`" in printed


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_show_term_uses_lists_each_place_using_a_word_in_the_specs_and_the_code_under_its_root(heron, capsys):
    assert ask(heron, "--show-term-uses", "heron") == 0
    assert printed_places(capsys.readouterr().out) == ["`code/sample.py` line 1", "`code/sample.py` line 2", f"`{SECTION}` line 5"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
def test_show_term_uses_refuses_a_commit_named_for_the_files_as_they_stand(heron, capsys):
    assert ask(heron, "--show-term-uses", "heron", "--commit", "HEAD") == 2
    printed = capsys.readouterr().out
    assert "a commit is named for a search of `committed-operative-files` or of `committed-fixture-files` alone" in printed and not printed_places(printed)


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
def test_show_code_structure_lists_the_unit_defining_a_name(heron, capsys):
    assert ask(heron, "--show-code-structure", "defines", "heron") == 0
    assert printed_places(capsys.readouterr().out) == ["`code/sample.py` line 1"]


@pytest.mark.action("--show-code-structure")
@pytest.mark.reports
def test_show_code_structure_refuses_a_structure_that_is_none(heron, capsys):
    assert ask(heron, "--show-code-structure", "owns", "heron") == 2
    printed = capsys.readouterr().out
    assert "no structure `owns`: a structure is one of " + ", ".join(search.STRUCTURES) in printed and not printed_places(printed)


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "seven-wading-birds")
def test_show_similar_passages_ranks_the_passages_saying_the_same(fixtures, work, capsys):
    # a project of its own, since the shared one holds no sentence long enough to be ranked: seven sections, each one
    # sentence about a wading bird in the reeds at dusk
    root = project(work / "birds", fixtures, {"seven-wading-birds": "specs/birds.md"})
    assert ask(root, "--show-similar-passages", "As evening falls a wading bird waits among the reeds until the tide turns.", "--limit", "7") == 0
    printed = capsys.readouterr().out
    assert "7 places, ranked: places to read, never findings" in printed
    assert len(printed_places(printed)) == 7 and all(p.startswith("`specs/birds.md § The ") for p in printed_places(printed))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
def test_show_similar_passages_says_a_citation_names_no_place(heron, capsys):
    assert ask(heron, "--show-similar-passages", "specs/target.md § Egrets") == 0
    printed = capsys.readouterr().out
    assert "0 places, ranked" in printed and not printed_places(printed) and "the question names nothing to ask of: " + search.NO_PLACE in printed


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
def test_show_pattern_matches_lists_the_place_an_expression_matches(heron, capsys):
    assert ask(heron, "--show-pattern-matches", "heron +stands") == 0
    assert printed_places(capsys.readouterr().out) == [f"`{SECTION}` line 5"]


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.reports
def test_show_pattern_matches_refuses_an_expression_that_is_none(heron, capsys):
    assert ask(heron, "--show-pattern-matches", "heron (stands") == 2
    printed = capsys.readouterr().out
    assert printed.startswith("search-spec-of-record-scope: ") and "position" in printed and not printed_places(printed)


@pytest.mark.action("--check-result")
@pytest.mark.passes
def test_check_result_passes_a_result_as_the_search_wrote_it(heron, opened, work, capsys):
    result = opened(heron, scratch=work / "index").terms("reeds")
    assert ask(heron, "--check-result", result.path) == 0
    assert capsys.readouterr().out.strip() == f"{result.name}: a search's result in its form, its content as the search wrote it"


@pytest.mark.action("--check-result")
@pytest.mark.reports
@pytest.mark.reads("search-results.md", "result-whose-place-was-changed")
def test_check_result_reports_a_result_whose_content_was_changed(fixtures, work, capsys):
    # the fixture is a result the search wrote of the word reeds, its one place since changed to name another line
    assert ask(work, "--check-result", result_file(work, fixtures["result-whose-place-was-changed"])) == 1
    assert "its content was changed" in capsys.readouterr().out


@pytest.mark.action("--check-result")
@pytest.mark.reports
def test_check_result_refuses_a_path_that_is_no_file(work, capsys):
    assert ask(work, "--check-result", work / "no-such-result.md") == 2
    printed = capsys.readouterr().out
    assert "no file " in printed and "no-such-result.md" in printed


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_the_entry_script_takes_a_flag_reaches_its_action_and_prints_what_it_gives(fixtures, work):
    ran, printed = run_entry(project(work / "heron", fixtures, HERON), "--show-term-uses", "heron")
    assert ran == 0 and f"`{SECTION}` line 5" in printed_places(printed)


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.reports
def test_the_entry_script_exits_as_its_action_says_and_with_no_traceback(fixtures, work):
    ran, printed = run_entry(project(work / "heron", fixtures, HERON), "--show-pattern-matches", "heron (stands")
    assert ran == 2 and "search-spec-of-record-scope: " in printed and "Traceback" not in printed
