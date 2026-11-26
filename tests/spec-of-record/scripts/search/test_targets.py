"""The targets of a search: the operative files and the fixture files, each as they stand and as a commit held them,
and the working files a search is given the paths of.

Two small projects under git are written once in the file's folder, and no test changes a file of either. In the one
about herons, the spec gains the ibis with the second commit and the egret since then, and the stack has come to name
`src` as its code root in place of `code`. In the one of durable files, a commit holding no fixture file, whose
operative files hold a spec citing a section and a kept test's code, is followed by one holding two fixture files: a
text that shares a sentence with an operative spec and cites the same section, and code defining the name the kept
test's code defines. The fixture text has since gained the avocet.
"""
import pytest

from search_set import HERON, READS_HERON, ask, git, paths_of, printed_places, project, search

SECTION = "specs/target.md § Target"
CODE = search.code_checks.STACK
COMMITTED, WORKING = search.COMMITTED_OPERATIVE, search.WORKING
FIXTURE, FIXTURE_CODE = search.spec_text.FIXTURES + "/herons.md", search.spec_text.FIXTURES + "/herons.py"
KEPT_TEST = "tests/spec-of-record/scripts/heron-tests.py"
SAID = "A heron waits among the reeds at the water's edge for a fish."
PASSAGE = "specs/reeds.md § Herons"
OF_A_COMMIT = pytest.mark.reads("search-commits.md", "heron-spec-with-the-ibis", "heron-spec-with-the-ibis-and-the-egret", "stack-naming-the-code-root-src")
REEDS = pytest.mark.reads("search-heron-project.md", "reeds-spec", "heron-kept-test", "herons-text-holding-a-sentence-of-the-reeds")
AVOCET = pytest.mark.reads("search-commits.md", "herons-text-with-the-avocet", "marsh-spec-citing-the-target")
LISTING_KINDS = ("--show-term-uses", "--show-pattern-matches", "--show-citers", "--show-cited-sections", "--show-code-structure")
KINDS = {"terms": lambda s: s.terms("heron"), "pattern": lambda s: s.pattern("heron"), "citers": lambda s: s.citers(SECTION),
         "cited-sections": lambda s: s.cited_sections(), "code-structure": lambda s: s.code_structure("defines", "heron_test"),
         "meaning-of-words": lambda s: s.meaning(SAID), "meaning-of-a-passage": lambda s: s.meaning(PASSAGE)}
OPERATIVE_FINDS = {"terms": ["code/sample.py", "specs/reeds.md", "specs/target.md", KEPT_TEST], "pattern": ["code/sample.py", "specs/reeds.md", "specs/target.md", KEPT_TEST],
                   "citers": ["specs/marsh.md"], "cited-sections": ["specs/marsh.md"], "code-structure": [KEPT_TEST]}
FIXTURE_FINDS = {"terms": [FIXTURE, FIXTURE_CODE], "pattern": [FIXTURE, FIXTURE_CODE], "citers": [FIXTURE], "cited-sections": [FIXTURE], "code-structure": [FIXTURE_CODE]}


def commit(root, message, *paths):
    git(root, "add", *paths)
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def herons(shared, fixtures):
    """-> {root, first, second}: the project about herons under git, and its two commits."""
    def build():
        root = project(shared.folder / "herons", fixtures, HERON)
        git(root, "init", "-q")
        first = commit(root, "first", "specs", "code")
        project(root, fixtures, {"heron-spec-with-the-ibis": "specs/target.md"})
        second = commit(root, "second", "specs")
        project(root, fixtures, {"heron-spec-with-the-ibis-and-the-egret": "specs/target.md", "stack-naming-the-code-root-src": CODE})
        return {"root": root, "first": first, "second": second}
    return shared.once("herons", build)


@pytest.fixture
def durable(shared, fixtures):
    """-> {root, before, last}: the project of durable files under git, its commit holding no fixture file and its last."""
    def build():
        root = project(shared.folder / "durable", fixtures, HERON)
        project(root, fixtures, {"reeds-spec": "specs/reeds.md", "heron-kept-test": KEPT_TEST, "marsh-spec-citing-the-target": "specs/marsh.md"})
        git(root, "init", "-q")
        before = commit(root, "before the fixtures", "specs", "code", "tests")
        project(root, fixtures, {"herons-text-holding-a-sentence-of-the-reeds": FIXTURE, "heron-kept-test": FIXTURE_CODE})
        last = commit(root, "the fixtures", "tests")
        project(root, fixtures, {"herons-text-with-the-avocet": FIXTURE})
        return {"root": root, "before": before, "last": last}
    return shared.once("durable", build)


def searched(shared, durable, target):
    """-> the search of a target over the project of durable files, opened once for the file's tests."""
    return shared.once("search-" + target, lambda: shared.opened(durable["root"], scratch=shared.folder / ("index-" + target), target=target))


def files_of(result):
    """-> the files a result's places stand in, in the order its places first name them: a listing of cited sections
    by its citing places."""
    found = [str(p).split("`")[1].split(" § ")[0] for p in result.places]
    return list(dict.fromkeys(found))


# The targets of the operative files and of the working files, over the project about herons

@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("given, word, paths", [
    ({}, "heron", ["specs/target.md", "src/other.py"]),
    ({}, "egret", ["specs/target.md", "src/other.py"]),
    ({"target": COMMITTED}, "heron", ["code/sample.py", "specs/target.md"]),
    ({"target": COMMITTED}, "egret", []),
    ({"target": COMMITTED}, "ibis", ["specs/target.md"]),
    ({"target": COMMITTED, "commit": "first"}, "heron", ["code/sample.py", "specs/target.md"]),
    ({"target": COMMITTED, "commit": "first"}, "ibis", []),
], ids=["as-they-stand", "as-they-stand-a-line-not-committed", "committed", "committed-a-line-written-since", "committed-the-last-commit-s-line",
        "a-commit-named", "a-commit-named-a-line-it-does-not-hold"])
def test_a_search_answers_over_the_operative_files_of_its_target_the_code_by_the_stack_its_target_holds(herons, opened, work, given, word, paths):
    given = dict(given, **({"commit": herons[given["commit"]]} if "commit" in given else {}))
    assert paths_of(opened(herons["root"], scratch=work / "index", **given).terms(word)) == paths


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("given, target, named, last", [
    ({}, search.CURRENT_OPERATIVE, None, None),
    ({"target": COMMITTED}, COMMITTED, None, "second"),
    ({"target": COMMITTED, "commit": "second"}, COMMITTED, "second", None),
    ({"target": COMMITTED, "commit": "first"}, COMMITTED, "first", None),
], ids=["as-they-stand", "committed", "the-last-commit-named", "another-commit-named"])
def test_a_result_names_its_target_and_a_commit_its_asker_named_or_else_the_last_commit_it_read(herons, opened, work, given, target, named, last):
    given = dict(given, **({"commit": herons[given["commit"]]} if "commit" in given else {}))
    r = opened(herons["root"], scratch=work / "index", **given).terms("heron")
    assert (r.target, r.commit, r.last_commit) == (target, herons.get(named), herons.get(last))


@pytest.mark.action("--show-lines")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("given, lines", [({}, (3, 10)), ({"target": COMMITTED}, (3, 8)), ({"target": COMMITTED, "commit": "first"}, (3, 6))],
                         ids=["as-they-stand", "committed", "a-commit-named"])
def test_the_lines_a_citation_names_are_those_of_the_files_of_its_target(herons, opened, work, given, lines):
    given = dict(given, **({"commit": herons[given["commit"]]} if "commit" in given else {}))
    assert [(p.first, p.last) for p in opened(herons["root"], scratch=work / "index", **given).lines(SECTION).places] == [lines]


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("given, said", [({}, "is given none"), ({"paths": ["specs"]}, "is no working file")], ids=["no-path", "a-path-that-is-no-working-file"])
def test_a_search_of_the_working_files_given_no_path_of_one_is_refused(herons, opened, work, given, said):
    with pytest.raises(ValueError, match=said):
        opened(herons["root"], scratch=work / "index", target=WORKING, **given)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("paths, found", [
    ([".ai/plans/design-specs"], [".ai/plans/design-specs/a-design.md"]),
    ([".ai/plans", ".ai/follow-ups.md"], [".ai/follow-ups.md", ".ai/plans/design-specs/a-design.md", ".ai/plans/other-plan.md"]),
], ids=["a-folder", "a-folder-and-a-file"])
def test_a_search_of_the_working_files_answers_over_the_paths_it_is_given_alone(herons, opened, work, paths, found):
    r = opened(herons["root"], scratch=work / "index", target=WORKING, paths=paths).terms("heron")
    assert paths_of(r) == found and r.target == WORKING and r.narrowed == paths


@pytest.mark.action("--show-citers")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_the_citers_among_the_working_files_are_read_against_the_operative_file_they_cite(herons, opened, work):
    r = opened(herons["root"], scratch=work / "index", target=WORKING, paths=[".ai/plans/design-specs"]).citers(SECTION)
    assert paths_of(r) == [".ai/plans/design-specs/a-design.md"] and not any("does not resolve" in n for n in r.notes)


@pytest.mark.action("--show-cited-sections")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_the_cited_sections_of_the_working_files_hold_their_citing_places_alone(herons, opened, work):
    r = opened(herons["root"], scratch=work / "index", target=WORKING, paths=[".ai/plans/design-specs"]).cited_sections()
    assert [str(p) for p in r.places] == [f"`.ai/plans/design-specs/a-design.md § The Problem` line 5 cites `{SECTION}`"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_a_search_of_the_working_files_given_more_paths_reads_the_files_added_alone(herons, opened, work):
    opened(herons["root"], scratch=work / "index", target=WORKING, paths=[".ai/plans/design-specs"]).db.close()
    assert opened(herons["root"], scratch=work / "index", target=WORKING, paths=[".ai/plans", ".ai/follow-ups.md"]).read_count == 2


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_a_search_of_the_working_files_given_fewer_paths_reads_no_file_and_gives_no_place_of_a_path_left_out(herons, opened, work):
    for paths in ([".ai/plans/design-specs"], [".ai/plans", ".ai/follow-ups.md"]):
        opened(herons["root"], scratch=work / "index", target=WORKING, paths=paths).db.close()
    s = opened(herons["root"], scratch=work / "index", target=WORKING, paths=[".ai/plans/design-specs"])
    assert s.read_count == 0 and paths_of(s.terms("heron")) == [".ai/plans/design-specs/a-design.md"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_a_search_of_the_operative_files_after_the_other_targets_reads_none_and_gives_no_file_of_theirs(herons, opened, work):
    for given in ({}, {"target": COMMITTED}, {"target": COMMITTED, "commit": herons["first"]}, {"target": WORKING, "paths": [".ai/plans", ".ai/follow-ups.md"]}):
        opened(herons["root"], scratch=work / "index", **given).db.close()
    s = opened(herons["root"], scratch=work / "index")
    assert s.read_count == 0 and paths_of(s.terms("heron")) == ["specs/target.md", "src/other.py"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
def test_a_search_of_a_commit_reads_again_only_the_file_it_holds_otherwise_than_the_commit_searched_before_it(herons, opened, work):
    opened(herons["root"], scratch=work / "index", target=COMMITTED, commit=herons["first"]).db.close()
    s = opened(herons["root"], scratch=work / "index", target=COMMITTED)
    assert s.read_count == 1 and paths_of(s.terms("ibis")) == ["specs/target.md"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@OF_A_COMMIT
@pytest.mark.parametrize("named, places", [(True, 0), (False, 1)], ids=["the-first-commit-named", "none-named"])
def test_the_entry_script_s_main_takes_the_target_and_the_commit(herons, capsys, named, places):
    argv = ["--show-term-uses", "ibis", "--target", COMMITTED] + (["--commit", herons["first"]] if named else [])
    assert ask(herons["root"], *argv) == 0
    assert len(printed_places(capsys.readouterr().out)) == places


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads("search-heron-project.md", "bittern-spec")
@pytest.mark.reads("search-commits.md", "bittern-spec-with-the-crane")
def test_a_project_in_a_folder_of_a_larger_repository_is_read_as_under_git_by_its_paths_from_its_own_root(fixtures, opened, work):
    root = project(work / "outer", fixtures, {"bittern-spec": "inner/specs/target.md"})
    git(root, "init", "-q")
    commit(root, "the inner project", "inner")
    project(root, fixtures, {"bittern-spec-with-the-crane": "inner/specs/target.md"})
    s = opened(root / "inner", scratch=work / "index", target=COMMITTED)
    assert search.version_control(root / "inner") == search.GIT
    assert paths_of(s.terms("bittern")) == ["specs/target.md"] and not s.terms("crane").places


# The operative files and the fixture files, each listed, read and ranked apart, over the project of durable files

@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("committed", [False, True], ids=["as-they-stand", "committed"])
def test_the_listing_of_the_operative_files_holds_no_fixture_file_and_the_kept_tests_own_code(durable, committed):
    listed = search.operative_files(durable["root"], committed=committed)
    assert KEPT_TEST in listed and not [f for f in listed if f.startswith(search.spec_text.FIXTURES + "/")]


@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("committed", [False, True], ids=["as-they-stand", "committed"])
def test_the_listing_of_the_fixture_files_holds_the_fixture_files_alone(durable, committed):
    assert search.fixture_files(durable["root"], committed=committed) == [FIXTURE, FIXTURE_CODE]


@pytest.mark.reads("audit-whole-project.md", "project-registry-of-one-skill", "project-skill-file")
@pytest.mark.parametrize("skill, listed", [("harbor-guide", True), ("lighthouse-guide", False)], ids=["registered", "unregistered"])
def test_the_listing_of_the_operative_files_reads_the_project_s_own_registry_of_skills(fixtures, work, skill, listed):
    # the project's registry registers the harbor guide alone; the skill's file stands at the folder named
    placed = ".ai/skills/%s/SKILL.md" % skill
    root = project(work / "project", fixtures, {"project-registry-of-one-skill": search.spec_text.REGISTRY, "project-skill-file": placed})
    assert (placed in search.operative_files(root)) == listed


@pytest.mark.action(*LISTING_KINDS)
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target", [search.CURRENT_OPERATIVE, COMMITTED])
@pytest.mark.parametrize("kind", list(OPERATIVE_FINDS))
def test_a_search_of_the_operative_files_finds_its_places_in_the_operative_files_alone_whatever_its_kind(shared, durable, target, kind):
    # a fixture file holds a place each of these searches would find: the word, the citation and the name defined
    assert files_of(KINDS[kind](searched(shared, durable, target))) == OPERATIVE_FINDS[kind]


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target, kind, first", [
    (search.CURRENT_OPERATIVE, "meaning-of-words", "specs/reeds.md"), (COMMITTED, "meaning-of-words", "specs/reeds.md"),
    (search.CURRENT_OPERATIVE, "meaning-of-a-passage", "specs/reeds.md"), (COMMITTED, "meaning-of-a-passage", "specs/reeds.md"),
    (search.CURRENT_FIXTURE, "meaning-of-words", FIXTURE), (search.COMMITTED_FIXTURE, "meaning-of-words", FIXTURE),
])
def test_a_ranking_by_meaning_ranks_the_passages_of_its_target_s_kind_of_file_alone(shared, durable, target, kind, first):
    found = files_of(KINDS[kind](searched(shared, durable, target)))
    assert found[0] == first and {search.spec_text.durable_kind(f) for f in found} == {search.spec_text.durable_kind(first)}


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target", [search.CURRENT_FIXTURE, search.COMMITTED_FIXTURE])
def test_a_ranking_of_the_fixture_files_by_a_passage_of_an_operative_file_names_no_place(shared, durable, target):
    r = KINDS["meaning-of-a-passage"](searched(shared, durable, target))
    assert not r.places and r.names_nothing == [search.NO_PLACE]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
def test_the_index_of_the_operative_files_holds_no_word_and_no_place_of_a_fixture_file(shared, durable):
    s = searched(shared, durable, search.CURRENT_OPERATIVE)
    assert not s.terms("spoonbill").places and not s.db.execute("select count(*) from terms where terms match 'spoonbill'").fetchone()[0]
    assert not s.db.execute("select count(*) from placed where path like ?", (search.spec_text.FIXTURES + "/%",)).fetchone()[0]


@pytest.mark.action("--show-lines")
@pytest.mark.reports
@READS_HERON[0]
@REEDS
@AVOCET
def test_a_citation_of_a_fixture_file_s_section_names_no_place_among_the_operative_files(shared, durable):
    r = searched(shared, durable, search.CURRENT_OPERATIVE).lines(FIXTURE + " § Herons")
    assert not r.places and r.names_nothing == [search.NO_PLACE]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
def test_a_search_of_the_operative_files_reads_no_fixture_file_added(fixtures, opened, work):
    root = project(work / "project", fixtures, dict(HERON, **{"reeds-spec": "specs/reeds.md", "heron-kept-test": KEPT_TEST}))
    opened(root, scratch=work / "index").db.close()
    project(root, fixtures, {"herons-text-holding-a-sentence-of-the-reeds": FIXTURE})
    assert opened(root, scratch=work / "index").read_count == 0


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
def test_a_ranking_by_meaning_of_the_operative_files_is_unchanged_by_a_fixture_file_holding_a_passage_of_it_word_for_word(fixtures, opened, work):
    root = project(work / "project", fixtures, dict(HERON, **{"reeds-spec": "specs/reeds.md", "heron-kept-test": KEPT_TEST}))
    first = opened(root, scratch=work / "index")
    ranked = [str(p) for p in first.meaning(SAID).places]
    first.db.close()
    project(root, fixtures, {"herons-text-holding-a-sentence-of-the-reeds": FIXTURE})
    assert len(ranked) > 1 and [str(p) for p in opened(root, scratch=work / "index").meaning(SAID).places] == ranked


@pytest.mark.action(*LISTING_KINDS)
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target", [search.CURRENT_FIXTURE, search.COMMITTED_FIXTURE])
@pytest.mark.parametrize("kind", list(FIXTURE_FINDS))
def test_a_search_of_the_fixture_files_finds_its_places_in_the_fixture_files_alone_whatever_its_kind(shared, durable, target, kind):
    # an operative file holds a place each of these searches would find: the word, the citation and the name defined
    assert files_of(KINDS[kind](searched(shared, durable, target))) == FIXTURE_FINDS[kind]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target, word, paths", [
    (search.CURRENT_FIXTURE, "avocet", [FIXTURE]),
    (search.COMMITTED_FIXTURE, "avocet", []),
    (search.COMMITTED_FIXTURE, "spoonbill", [FIXTURE]),
    (search.COMMITTED_FIXTURE, "heron", [FIXTURE, FIXTURE_CODE]),
], ids=["as-they-stand-a-line-not-committed", "committed-a-line-written-since", "committed-a-line-of-the-commit", "committed-a-word-operative-files-hold-too"])
def test_a_search_of_the_fixture_files_answers_over_the_fixture_files_of_its_target(shared, durable, target, word, paths):
    assert paths_of(searched(shared, durable, target).terms(word)) == paths


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
def test_the_index_of_the_fixture_files_holds_no_word_standing_in_an_operative_file_alone(shared, durable):
    assert not searched(shared, durable, search.CURRENT_FIXTURE).db.execute("select count(*) from terms where terms match 'egret'").fetchone()[0]


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target, named, last", [(search.CURRENT_FIXTURE, None, None), (search.COMMITTED_FIXTURE, None, "last")], ids=["as-they-stand", "committed"])
def test_a_result_of_the_fixture_files_names_its_target_and_the_last_commit_it_read(shared, durable, target, named, last):
    r = searched(shared, durable, target).terms("heron")
    assert (r.target, r.commit, r.last_commit) == (target, durable.get(named), durable.get(last))


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
def test_a_search_of_the_fixture_files_naming_a_commit_that_held_none_gives_no_place_and_holds_the_commit_named(durable, opened, work):
    r = opened(durable["root"], scratch=work / "index", target=search.COMMITTED_FIXTURE, commit=durable["before"]).terms("heron")
    assert not r.places and r.commit == durable["before"]


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@READS_HERON[0]
@REEDS
@AVOCET
def test_a_search_of_the_fixture_files_as_they_stand_naming_a_commit_is_refused(durable, opened, work):
    with pytest.raises(ValueError, match="a commit is named"):
        opened(durable["root"], scratch=work / "index", target=search.CURRENT_FIXTURE, commit=durable["last"])


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
@pytest.mark.parametrize("target", [search.CURRENT_FIXTURE, search.COMMITTED_FIXTURE])
def test_the_entry_script_s_main_takes_each_target_of_the_fixture_files(durable, capsys, target):
    assert ask(durable["root"], "--show-term-uses", "heron", "--target", target) == 0
    printed = printed_places(capsys.readouterr().out)
    assert printed and all(p.startswith("`" + search.spec_text.FIXTURES + "/") for p in printed)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
@REEDS
@AVOCET
def test_the_entry_script_s_main_naming_no_target_gives_no_fixture_file(durable, capsys):
    assert ask(durable["root"], "--show-term-uses", "heron") == 0
    printed = printed_places(capsys.readouterr().out)
    assert printed and not [p for p in printed if search.spec_text.FIXTURES in p]
