"""Each action of the search's entry script, run as an agent runs it, as a process in a project: once where it
answers, and once where it refuses what it is given or has nothing to give. The actions on what the search requires
and on the snapshot code are held the same two ways by the tests of those subjects.

The file's tests share one small project, written and committed once in the file's folder; none changes a file of it."""
import re

import pytest

pytestmark = pytest.mark.reads("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
                               "plan-citing-the-heron", "follow-ups-naming-a-heron")
SECTION = "specs/target.md § Target"
WORKING = ("--target", "working-files", "--paths", ".ai/plans")


@pytest.fixture
def project(shared, fixtures, tools):
    """-> the project's root: a spec naming a heron, code under the stack's one code root, and two plans citing the
    spec's section, the spec and the code committed."""
    def build():
        root = tools.a_project(shared.folder / "project", fixtures)
        tools.git(root, "init", "-q")
        tools.git(root, "add", "specs", "code")
        tools.git(root, "commit", "-q", "-m", "first")
        return root
    return shared.once("project", build)


def places(printed):
    """-> the places a run printed, each on a line of its own beneath the result's name and its count."""
    return [line.strip() for line in printed.split("\n") if line.startswith("  `")]


def test_a_run_naming_no_action_or_one_the_script_does_not_state_prints_the_usage(project, search, script, check):
    for given in ([], ["--show-everything"], ["--show-citers"], ["--show-lines", SECTION, "and one value more"]):
        ran, printed = script(project, *given)
        check(f"given {' '.join(given) or 'nothing'}, the script prints its usage, naming each action it states, and exits 2",
              ran == 2 and printed.startswith("usage:") and all(flag in printed for flag, _, _, _ in search.FLAGS), (ran, printed[:200]))


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_show_citers_lists_the_places_citing_a_section(project, script, check):
    ran, printed = script(project, "--show-citers", SECTION, *WORKING)
    check("asked over the plans, the script lists the place in each plan citing the spec's section, says they are every place, and exits 0",
          ran == 0 and "2 places, complete: places to read, never findings" in printed
          and places(printed) == ["`.ai/plans/design-specs/a-design.md § The Problem` line 5", "`.ai/plans/other-plan.md § Notes` line 5"], (ran, printed))


@pytest.mark.action("--show-citers")
@pytest.mark.reports
def test_show_citers_refuses_a_target_that_is_none(project, script, check):
    ran, printed = script(project, "--show-citers", SECTION, "--target", "every-file")
    check("given a target that is none, the script says so, names the targets, and exits 2 with no place", ran == 2 and "no target `every-file`: a target is one of" in printed and not places(printed), (ran, printed))


@pytest.mark.action("--show-cited-sections")
@pytest.mark.passes
def test_show_cited_sections_lists_each_citing_place_with_what_it_cites(project, script, check):
    ran, printed = script(project, "--show-cited-sections", *WORKING)
    check("asked over the plans, the script lists each citing place followed by the section it cites, and exits 0",
          ran == 0 and places(printed) == [f"`.ai/plans/design-specs/a-design.md § The Problem` line 5 cites `{SECTION}`", f"`.ai/plans/other-plan.md § Notes` line 5 cites `{SECTION}`"], (ran, printed))


@pytest.mark.action("--show-cited-sections")
@pytest.mark.reports
def test_show_cited_sections_refuses_the_working_files_given_no_path(project, script, check):
    ran, printed = script(project, "--show-cited-sections", "--target", "working-files")
    check("asked over the working files and given no path, the script says it is given none, and exits 2 with no place", ran == 2 and "is given none: name them with --paths" in printed and not places(printed), (ran, printed))


@pytest.mark.action("--show-lines")
@pytest.mark.passes
def test_show_lines_gives_the_lines_a_citation_names(project, script, check):
    ran, printed = script(project, "--show-lines", SECTION)
    check("given a section's citation, the script gives the section with its lines, from its heading to the file's end, and exits 0",
          ran == 0 and places(printed) == [f"`{SECTION}` lines 3-6"], (ran, printed))


@pytest.mark.action("--show-lines")
@pytest.mark.reports
def test_show_lines_says_a_citation_names_no_place(project, search, script, check):
    ran, printed = script(project, "--show-lines", "specs/target.md § Egrets")
    check("given a citation of a section the spec does not hold, the script gives no place and says the question names nothing by that case",
          ran == 0 and "0 places, complete" in printed and not places(printed) and "the question names nothing to ask of: " + search.NO_PLACE in printed and "holds no section `Egrets`" in printed, (ran, printed))


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_show_term_uses_lists_each_place_using_a_word(project, script, check):
    ran, printed = script(project, "--show-term-uses", "heron")
    check("asked for a word, the script lists its uses in the spec and in the code under the stack's code root, and no use in other code or in a working file, and exits 0",
          ran == 0 and places(printed) == ["`code/sample.py` line 1", "`code/sample.py` line 2", f"`{SECTION}` line 5"], (ran, printed))


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
def test_show_term_uses_refuses_a_commit_named_for_the_files_as_they_stand(project, script, check):
    ran, printed = script(project, "--show-term-uses", "heron", "--commit", "HEAD")
    check("given a commit and no target of a commit's files, the script says a commit is named for those targets alone, and exits 2 with no place",
          ran == 2 and "a commit is named for a search of `committed-operative-files` or of `committed-fixture-files` alone" in printed and not places(printed), (ran, printed))


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
def test_show_code_structure_lists_the_unit_defining_a_name(project, script, check):
    ran, printed = script(project, "--show-code-structure", "defines", "heron")
    check("asked which unit defines a name, the script gives the function's file and line, and exits 0", ran == 0 and places(printed) == ["`code/sample.py` line 1"], (ran, printed))


@pytest.mark.action("--show-code-structure")
@pytest.mark.reports
def test_show_code_structure_refuses_a_structure_that_is_none(project, search, script, check):
    ran, printed = script(project, "--show-code-structure", "owns", "heron")
    check("given a structure that is none, the script says so, names the structures, and exits 2 with no place",
          ran == 2 and "no structure `owns`: a structure is one of " + ", ".join(search.STRUCTURES) in printed and not places(printed), (ran, printed))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "seven-wading-birds")
def test_show_similar_passages_ranks_the_passages_saying_the_same(fixtures, tools, script, work, check):
    # a project of this test's own, since the shared one holds no sentence long enough to be ranked: the small
    # project with one spec more, of seven sections each one sentence about a wading bird in the reeds at dusk
    root = tools.a_project(work / "project", fixtures)
    tools.put(root, "specs/birds.md", fixtures["seven-wading-birds"])
    ran, printed = script(root, "--show-similar-passages", "As evening falls a wading bird waits among the reeds until the tide turns.", "--limit", "7")
    check("asked with a sentence in other words, the script gives the seven sentences saying it of seven birds, says its places are ranked, and exits 0",
          ran == 0 and "7 places, ranked: places to read, never findings" in printed and len(places(printed)) == 7 and all(p.startswith("`specs/birds.md § The ") for p in places(printed)), (ran, printed))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
def test_show_similar_passages_says_a_citation_names_no_place(project, search, script, check):
    ran, printed = script(project, "--show-similar-passages", "specs/target.md § Egrets")
    check("asked by a citation of a section the spec does not hold, the script gives no place and says the question names nothing by that case",
          ran == 0 and "0 places, ranked" in printed and not places(printed) and "the question names nothing to ask of: " + search.NO_PLACE in printed, (ran, printed))


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
def test_show_pattern_matches_lists_the_place_an_expression_matches(project, script, check):
    ran, printed = script(project, "--show-pattern-matches", "heron +stands")
    check("given an expression, the script lists the one place it matches, and exits 0", ran == 0 and places(printed) == [f"`{SECTION}` line 5"], (ran, printed))


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.reports
def test_show_pattern_matches_refuses_an_expression_that_is_none(project, script, check):
    ran, printed = script(project, "--show-pattern-matches", "heron (stands")
    check("given an expression that cannot be read as one, the script says why, and exits 2 with no place and no traceback",
          ran == 2 and "search-spec-of-record-scope: " in printed and "position" in printed and not places(printed) and "Traceback" not in printed, (ran, printed))


@pytest.mark.action("--check-result", "--show-term-uses")
@pytest.mark.passes
def test_check_result_passes_a_result_as_the_search_wrote_it(project, script, check):
    ran, printed = script(project, "--show-term-uses", "reeds")
    result = project / printed.split("\n")[0].strip()
    ran, printed = script(project, "--check-result", result)
    check("given a result's file as a search wrote it, the script says it is in its form with its content as written, and exits 0",
          ran == 0 and printed.strip() == f"{result.name}: a search's result in its form, its content as the search wrote it", (ran, printed))


@pytest.mark.action("--check-result", "--show-term-uses")
@pytest.mark.reports
def test_check_result_reports_a_result_changed_by_hand_and_refuses_a_file_that_is_none(project, script, work, check):
    ran, printed = script(project, "--show-term-uses", "reeds")
    result = project / printed.split("\n")[0].strip()
    # the test's variant of a result: a copy under the same name whose one place names another line
    changed = work / "changed" / result.name
    changed.parent.mkdir(parents=True)
    changed.write_text(re.sub(r"` line 5\b", "` line 4", result.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    ran, printed = script(project, "--check-result", changed)
    check("given a result whose content was changed, the script reports that its name no longer gives its content's hash, and exits 1",
          ran == 1 and "its content was changed" in printed and changed.read_text(encoding="utf-8") != result.read_text(encoding="utf-8"), (ran, printed))
    ran, printed = script(project, "--check-result", work / "changed" / "no-such-result.md")
    check("given a path that is no file, the script says so and exits 2", ran == 2 and "no file " in printed and "no-such-result.md" in printed, (ran, printed))
