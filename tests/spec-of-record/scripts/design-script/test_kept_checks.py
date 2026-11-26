"""The checks made with a run of the kept tests, each held by calling its unit: what a script's tests hold, read from
what the runner gives of each test, the script's actions read from its file and its check units by their annotations,
a section a skill's table enforces among them; and the tests' folder as a whole. And --show-test-coverage, which
shows what the first check finds of every script and runs no test."""
import pytest

from design_script_set import (GUIDE_SET, KEPT, KEPT_FIXTURES, KEPT_RUN, KEPT_SET_READS, acted, design_documents as dd, held, kept_set,
                               project, spec_text)

BREAD = ".ai/skills/bake-bread/scripts/"
SHAPING = "specs/methodology/loaves.md § Shaping"
PROVED = "loaf-proved-an-hour"
# the bakery's project: a skill registered, its table of checks enforcing the section Shaping, its entry script stating
# --show-guide, a unit of its code citing the Script Check record its specs hold and that section, and the specs
BAKERY = {"registry-of-one-skill": "specs/methodology/skills/registered-skills.md", "index-of-the-bakery-specs": "specs/index.md",
          "loaves-spec-of-a-script-check": "specs/loaves.md", "bread-skill-of-a-table-of-checks": ".ai/skills/bake-bread/SKILL.md",
          "guide-script": BREAD + "bake-bread.py", "bread-script-annotated-in-form": BREAD + "proving.py"}
BAKERY_READS = [pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill"),
                pytest.mark.reads("audit-script-checks-carried-out.md", "index-of-the-bakery-specs"),
                pytest.mark.reads("audit-canon-spec-annotations.md", "loaves-spec-of-a-script-check", "bread-script-annotated-in-form"),
                pytest.mark.reads("design-script-kept-coverage.md", "bread-skill-of-a-table-of-checks"),
                pytest.mark.reads("design-script-kept-sets.md", "guide-script")]
BREAD_SET = {"script": "bread", "folder": KEPT + "/scripts/bread", "files": (BREAD,), "actions_in": BREAD + "bake-bread.py"}


def row(test, actions=("--show-guide",), checks=(), ways=("passes",), named=(), reads=(), folder=KEPT + "/scripts/bread"):
    """-> what the runner gives of one test of a set: its name and file, the actions and checks it names, each way its
    markers give, holding the names given, and the fixtures it reads."""
    return {"test": "scripts/%s/test_x.py::%s" % (folder.rsplit("/", 1)[1], test), "file": folder + "/test_x.py", "actions": list(actions),
            "script_checks": list(checks), "ways": {way: list(named) for way in ways}, "reads": [list(r) for r in reads]}


def bakery(work, fixtures):
    return project(work, fixtures, BAKERY)


EACH_HELD = [row("test_bakes", checks=(PROVED, SHAPING)), row("test_burns", checks=(PROVED, SHAPING), ways=("reports",))]


def with_bakery(test):
    for mark in reversed(BAKERY_READS):
        test = mark(test)
    return test


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@with_bakery
def test_script_whose_every_action_check_and_section_a_test_holds_both_ways_passes(fixtures, work):
    root = bakery(work, fixtures)
    assert dd.coverage_problems(root, BREAD_SET, EACH_HELD, dd.script_check_records(root)) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@with_bakery
@pytest.mark.parametrize("rows, said", [
    ([row("test_bakes"), row("test_burns", ways=("reports",))],
     ["the Script Check %s of bread is held by no kept test where it passes" % PROVED, "the Script Check %s of bread is held by no kept test where it reports" % PROVED,
      "the section %s of bread is held by no kept test where it passes" % SHAPING, "the section %s of bread is held by no kept test where it reports" % SHAPING]),
    ([row("test_bakes", checks=(PROVED, SHAPING))],
     ["the action --show-guide of bread is held by no kept test where it reports", "the Script Check %s of bread is held by no kept test where it reports" % PROVED,
      "the section %s of bread is held by no kept test where it reports" % SHAPING]),
    ([row("test_bakes", checks=(PROVED, SHAPING), named=("--show-harbor",))] + EACH_HELD[1:],
     ["the action --show-guide of bread is held by no kept test where it passes", "the Script Check %s of bread is held by no kept test where it passes" % PROVED,
      "the section %s of bread is held by no kept test where it passes" % SHAPING]),
    (EACH_HELD + [row("test_moors", actions=("--show-harbor",))], ["scripts/bread/test_x.py::test_moors names the action --show-harbor, which its script does not state"]),
    (EACH_HELD + [row("test_moors", checks=("specs/harbor.md § Moorings",))],
     ["scripts/bread/test_x.py::test_moors cites the section specs/harbor.md § Moorings, which no check unit of its script cites"]),
    (EACH_HELD + [row("test_moors", checks=("boat-moored",))], ["scripts/bread/test_x.py::test_moors cites the Script Check boat-moored, which its script does not carry out"]),
])
def test_name_no_test_holds_both_ways_or_a_test_names_beyond_its_script_is_reported(fixtures, work, rows, said):
    root = bakery(work, fixtures)
    assert dd.coverage_problems(root, BREAD_SET, rows, dd.script_check_records(root)) == [(dd.KEPT_HELD_RULE, s) for s in said]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@with_bakery
@pytest.mark.reads("design-script-kept-runs.md", "guide-script-stating-its-actions-under-another-name")
def test_script_stating_no_actions_in_the_form_is_reported(fixtures, work):
    root = project(work, fixtures, dict(BAKERY, **{"guide-script-stating-its-actions-under-another-name": BREAD + "bake-bread.py"}))
    [(rule, said)] = dd.coverage_problems(root, BREAD_SET, EACH_HELD, dd.script_check_records(root))
    assert rule == dd.KEPT_HELD_RULE and said.startswith("%s/scripts/bread/conftest.py names no file stating its script's actions under ACTIONS_IN, "
                                                         "or the file it names, %sbake-bread.py, holds no tuple named FLAGS" % (KEPT, BREAD))


@pytest.mark.action("--check-kept-tests")
@pytest.mark.parametrize("names, rows, unheld", [
    (["--show-guide"], [row("a"), row("b", ways=("reports",))], []),
    (["--show-guide"], [row("a", ways=("passes", "reports"))], []),
    (["--show-guide", PROVED], [row("a", checks=(PROVED,), ways=("passes", "reports"), named=(PROVED,))],
     [("--show-guide", "passes"), ("--show-guide", "reports")]),
    (["--show-guide"], [row("a", actions=())], [("--show-guide", "passes"), ("--show-guide", "reports")]),
])
def test_name_is_held_each_way_a_test_naming_it_holds_it(names, rows, unheld):
    assert dd.held_both_ways(names, rows) == unheld


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-kept-sets.md", "guide-script")
@pytest.mark.reads("design-script-kept-runs.md", "guide-script-stating-two-actions", "guide-script-stating-its-actions-under-another-name", "tests-file-of-no-python")
@pytest.mark.parametrize("script, actions", [
    ("guide-script", ["--show-guide"]),
    ("guide-script-stating-two-actions", ["--show-guide", "--check-guide"]),
    ("guide-script-stating-its-actions-under-another-name", None),
    ("tests-file-of-no-python", None),
    (None, None),
])
def test_actions_are_read_from_the_tuple_its_script_states_them_in(fixtures, work, script, actions):
    root = project(work, fixtures, {script: "tools/guide.py"} if script else {})
    assert dd.stated_actions(root, "tools/guide.py") == actions


@pytest.mark.action("--check-kept-tests")
@with_bakery
@pytest.mark.parametrize("left_out, files, enforced", [
    ((), (BREAD,), {SHAPING}),
    ((), ("tools/guide.py",), set()),
    (("registry-of-one-skill",), (BREAD,), set()),
])
def test_sections_a_table_enforces_are_read_of_each_registered_skill_whose_entry_script_is_the_scripts(fixtures, work, left_out, files, enforced):
    root = project(work, fixtures, {key: path for key, path in BAKERY.items() if key not in left_out})
    assert dd.table_enforced(root, files) == enforced


@pytest.mark.action("--check-kept-tests")
@with_bakery
@pytest.mark.parametrize("enforced, units", [
    ({SHAPING}, {PROVED: (BREAD + "proving.py", 4), SHAPING: (BREAD + "proving.py", 4)}),
    (set(), {PROVED: (BREAD + "proving.py", 4)}),
])
def test_check_units_are_read_by_the_place_their_annotations_cite(fixtures, work, enforced, units):
    assert dd.check_units(bakery(work, fixtures), (BREAD,), enforced) == units


@pytest.mark.action("--check-kept-tests")
@with_bakery
@pytest.mark.parametrize("files, carried", [((BREAD,), [PROVED]), (("tools/guide.py",), [])])
def test_script_carries_out_each_script_check_whose_record_names_a_skill_whose_scripts_are_its(fixtures, work, files, carried):
    records = dd.script_check_records(bakery(work, fixtures))
    assert records == {PROVED: {"bake-bread"}} and dd.held_by_script(files, records) == carried


@pytest.mark.action("--check-kept-tests")
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-citing-a-script-check")
def test_runner_reads_the_checks_a_test_cites_from_the_annotations_above_it(fixtures):
    cited = spec_text.test_annotations(fixtures["guide-set-tests-citing-a-script-check"])
    assert cited == {"test_the_quay_is_named": ["specs/methodology/loaves.md § Proving", "specs/methodology/loaves.md § Proving § Script Checks [Name: %s]" % PROVED]}
    assert [spec_text.check_named(c) for c in cited["test_the_quay_is_named"]] == ["specs/methodology/loaves.md § Proving", PROVED]


QUAY_READ = [row("test_the_quay_is_named", reads=(("guide.md", "quay-line"),), folder=GUIDE_SET)]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-fixture-read-by-a-kept-test]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixtures-index-lists-its-folder]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
def test_tests_folder_in_order_passes(fixtures, work):
    assert dd.tests_folder_problems(kept_set(work, fixtures), QUAY_READ) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-fixture-read-by-a-kept-test]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixtures-index-lists-its-folder]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.reads("design-script-kept-coverage.md", "fixture-file-of-two-fixtures", "index-listing-two-files", "fixture-file-holding-text-beside-its-fixture")
@pytest.mark.parametrize("placed, left_out, rows, record, said", [
    ({"notes-citing-nothing": GUIDE_SET + "/AGENTS.md"}, (), QUAY_READ, "no-instructions-name-kept-under-the-tests",
     GUIDE_SET + "/AGENTS.md carries the name of an agent instructions file"),
    ({"notes-citing-nothing": KEPT_FIXTURES + "/notes/agents.md"}, (), QUAY_READ, "no-instructions-name-kept-under-the-tests",
     KEPT_FIXTURES + "/notes/agents.md carries the name of an agent instructions file"),
    ({"fixture-file-of-two-fixtures": KEPT_FIXTURES + "/harbor.md"}, (), QUAY_READ, "fixtures-index-lists-its-folder",
     KEPT_FIXTURES + "/index.md does not list harbor.md, which stands in its folder"),
    ({"index-listing-two-files": KEPT_FIXTURES + "/index.md"}, (), QUAY_READ, "fixtures-index-lists-its-folder",
     KEPT_FIXTURES + "/index.md lists harbor.md, which does not stand in its folder"),
    ({}, ("index-listing-one-file",), QUAY_READ, "fixtures-index-lists-its-folder", KEPT_FIXTURES + " holds no index.md"),
    ({"fixture-file-holding-text-beside-its-fixture": KEPT_FIXTURES + "/guide.md"}, (), QUAY_READ, "fixture-file-holds-fixtures-in-their-form",
     KEPT_FIXTURES + "/guide.md line 10: text that is no part of a fixture: A line written beside the fixtures."),
    ({"notes-citing-nothing": KEPT_FIXTURES + "/notes.txt"}, (), QUAY_READ, "fixture-file-holds-fixtures-in-their-form",
     KEPT_FIXTURES + "/notes.txt is neither the folder's index nor a Markdown file of fixtures"),
    ({"fixture-file-of-two-fixtures": KEPT_FIXTURES + "/guide.md"}, (), QUAY_READ, "each-fixture-read-by-a-kept-test",
     "the fixture harbor-line of %s/guide.md is read by no kept test" % KEPT_FIXTURES),
    ({}, (), [row("test_the_quay_is_named", reads=(("guide.md", "pier-line"),), folder=GUIDE_SET)], "each-fixture-read-by-a-kept-test",
     "scripts/guide/test_x.py::test_the_quay_is_named names the fixture pier-line of guide.md, which does not stand"),
])
def test_tests_folder_out_of_order_is_reported(fixtures, work, placed, left_out, rows, record, said):
    found = dd.tests_folder_problems(kept_set(work, fixtures, placed, left_out=left_out), rows)
    assert (dd.KEPT_CHECKS % record, said) in found


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line")
def test_fixture_file_in_its_form_gives_each_fixture_its_snippet(fixtures):
    found, problems = spec_text.fixtures_of(fixtures["fixture-file-of-one-line"])
    assert problems == [] and [(f["key"], f["language"], f["snippet"]) for f in found] == [("quay-line", "markdown", "The ferry leaves from the north quay.\n")]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-coverage.md", "fixture-file-holding-text-beside-its-fixture", "fixture-file-whose-fixture-lacks-its-holds",
                   "fixture-file-whose-fixture-lacks-its-snippet", "fixture-file-whose-block-names-no-language", "fixture-file-whose-key-is-not-hyphened-words",
                   "fixture-file-not-opening-with-its-records")
@pytest.mark.parametrize("text, problem", [
    ("fixture-file-holding-text-beside-its-fixture", (10, "text that is no part of a fixture: A line written beside the fixtures.")),
    ("fixture-file-whose-fixture-lacks-its-holds", (2, "the fixture quay-line lacks its Holds, what the snippet holds")),
    ("fixture-file-whose-fixture-lacks-its-snippet", (2, "the fixture quay-line lacks its Snippet")),
    ("fixture-file-whose-block-names-no-language", (6, "the fenced block of the fixture quay-line names no language")),
    ("fixture-file-whose-key-is-not-hyphened-words", (2, "the fixture's key, Quay Line, is not lower-case words joined by hyphens")),
    ("fixture-file-not-opening-with-its-records", (1, "the file does not open with **Records:**, so it holds no fixture in its form")),
])
def test_fixture_file_out_of_its_form_is_reported_on_its_line(fixtures, text, problem):
    assert problem in spec_text.fixtures_of(fixtures[text])[1]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-holding-no-test-where-it-reports")
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
@pytest.mark.parametrize("tests, placed, changed, record, said", [
    ("guide-set-tests-holding-no-test-where-it-reports", {}, "docs/guide.md", "each-script-check-and-action-held-by-a-test",
     "the action --show-guide of guide is held by no kept test where it reports"),
    ("guide-set-tests", {"notes-citing-nothing": GUIDE_SET + "/AGENTS.md"}, KEPT_FIXTURES + "/index.md", "no-instructions-name-kept-under-the-tests",
     GUIDE_SET + "/AGENTS.md carries the name of an agent instructions file"),
])
def test_checks_made_with_a_run_report_where_its_tests_pass(fixtures, work, tests, placed, changed, record, said):
    output, problems, _ = dd.kept_tests_run(kept_set(work, fixtures, placed, tests=tests), [changed])
    assert problems == [(dd.KEPT_CHECKS % record, said)] and " failed\n" not in output.replace(", 0 failed\n", "")


BAKE_BREAD_UNHELD = "bake-bread: no kept tests, 0 tests\n  action --show-tides: held by no kept test where it passes\n  action --show-tides: held by no kept test where it reports\n"


@pytest.mark.action("--show-test-coverage")
@pytest.mark.passes
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests", "tides-script")
@pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill")
def test_coverage_is_shown_of_every_script_and_nothing_is_run_or_written(fixtures, work, monkeypatch, capsys):
    root = kept_set(work, fixtures, {"registry-of-one-skill": "specs/methodology/skills/registered-skills.md", "tides-script": BREAD + "bake-bread.py"})
    before = held(root)
    assert acted(monkeypatch, root, dd.show_test_coverage, None) == 0
    assert capsys.readouterr().out == "== show-test-coverage\nguide: a set of kept tests, 2 tests\n%s2 not held\n\n" % BAKE_BREAD_UNHELD
    assert held(root) == before and not list((root / KEPT_RUN).rglob("report.xml"))


@pytest.mark.action("--show-test-coverage")
@pytest.mark.reports
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "guide-set-tests-holding-no-test-where-it-reports", "guide-script-stating-its-actions-under-another-name")
@pytest.mark.parametrize("tests, placed, said", [
    ("guide-set-tests-holding-no-test-where-it-reports", {}, "guide: a set of kept tests, 2 tests\n  action --show-guide: held by no kept test where it reports\n1 not held\n"),
    ("guide-set-tests", {"guide-script-stating-its-actions-under-another-name": "tools/guide.py"},
     "guide: a set of kept tests, 2 tests\n  its actions cannot be read: tools/guide.py states none in the form of FLAGS\n0 not held\n"),
])
def test_coverage_shows_what_is_unheld_and_fails_nothing_for_it(fixtures, work, monkeypatch, capsys, tests, placed, said):
    assert acted(monkeypatch, kept_set(work, fixtures, placed, tests=tests), dd.show_test_coverage, None) == 0
    assert capsys.readouterr().out == "== show-test-coverage\n" + said + "\n"


@pytest.mark.action("--show-test-coverage")
@pytest.mark.reports
@KEPT_SET_READS[0]
@KEPT_SET_READS[1]
@pytest.mark.reads("design-script-kept-sets.md", "guide-set-tests")
@pytest.mark.reads("design-script-kept-runs.md", "tests-file-of-no-python")
def test_coverage_is_refused_where_the_runner_cannot_find_the_tests(fixtures, work, monkeypatch, capsys):
    root = kept_set(work, fixtures, {"tests-file-of-no-python": GUIDE_SET + "/test_broken.py"})
    assert acted(monkeypatch, root, dd.show_test_coverage, None) == 2
    got = capsys.readouterr()
    assert got.err.startswith("--show-test-coverage: the runner could not find the kept tests, exit 2") and "== show-test-coverage" not in got.out
