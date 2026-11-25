"""The checks made with a run of the kept tests, where each reports: what a script's tests hold, and the tests' folder
as a whole; and the two showings of the kept tests, --show-test-coverage and --show-kept-test-times.

Each test gives a project the guide's set of kept tests, as test_kept.py does, changes one thing of it, and holds what
the design script then says. Where each of these checks passes is held by test_kept.py's first test.
"""
import pytest

from design_script_set import (GUIDE_SET, GUIDE_TESTS, KEPT, KEPT_RUN, Project, RULE, kept_tests, passes, reports, run_holds, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-kept-sets.md", "guide-script", "guide-set-conftest", "guide-set-tests", "fixture-file-of-one-line", "index-listing-one-file")]
HELD = RULE % "each-script-check-and-action-held-by-a-test"
ONE_ACTION = "    (\"--show-guide\", \"\", None, \"show the guide\"),\n"
SECOND_ACTION = "    (\"--check-guide\", \"\", None, \"check the guide\"),\n"
GUIDE_FIXTURES, INDEX = KEPT + "/fixtures/guide.md", KEPT + "/fixtures/index.md"
# the Script Check the spec written for these tests holds, as a test's annotation cites it: the line is put together
# here, so no line of this file reads as an annotation of its own
MARK = "@canon-spec"
CITED = "# " + MARK + " specs/guide-checks.md § Script Checks [Name: guide-names-the-quay]"


def checked(p, changed="docs/guide.md"):
    return p.run("--check-kept-tests", changed)


def a_spec_of_one_check(p, fixtures):
    """Give a project a spec holding one Script Check record, which its specs' index names, carried out by a skill
    whose scripts the guide's set names among its script's files."""
    p.put("specs/guide-checks.md", fixtures["spec-of-one-script-check"])
    p.put("specs/index.md", p.read("specs/index.md").rstrip("\n") + "\n| `guide-checks.md` | The checks of the guide |\n")
    p.put(GUIDE_SET + "/conftest.py", swap(fixtures["guide-set-conftest"], "(\"tools/guide.py\",)", "(\"tools/guide.py\", \".ai/skills/show-guide/scripts/\")"))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
def test_action_no_test_holds_both_ways_is_reported(check, fixtures):
    p = Project("unheld-action")
    kept_tests(p)
    # the script states a second action, which no test names
    p.put("tools/guide.py", swap(fixtures["guide-script"], ONE_ACTION, ONE_ACTION + SECOND_ACTION))
    got = checked(p)
    check("--check-kept-tests reports an action its script states that no kept test holds, once for where it passes and once for where it reports",
          reports(got, "== check-kept-tests", ["the action --check-guide of guide is held by no kept test where it passes", "the action --check-guide of guide is held by no kept test where it reports",
                                               HELD, "2 problems"]), shown(got))
    p = Project("held-one-way")
    # the one test holding the action where it reports no longer says so
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.reports\n", ""))
    got = checked(p)
    check("--check-kept-tests reports an action held where it passes and by no test where it reports",
          reports(got, "== check-kept-tests", ["the action --show-guide of guide is held by no kept test where it reports", "1 problem"]) and "where it passes" not in got[1], shown(got))
    p = Project("held-by-name")
    # the test holding the action where it passes says it holds another name so, and so not this one
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.passes\n", "@pytest.mark.passes(\"--show-harbour\")\n"))
    got = checked(p)
    check("--check-kept-tests reads a way's marker given names as holding those names alone",
          reports(got, "== check-kept-tests", ["the action --show-guide of guide is held by no kept test where it passes", "1 problem"]), shown(got))
    p = Project("action-not-stated")
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.action(\"--show-guide\")\n@pytest.mark.reports", "@pytest.mark.action(\"--show-guide\", \"--show-harbour\")\n@pytest.mark.reports"))
    got = checked(p)
    check("--check-kept-tests reports a test naming an action its script does not state",
          reports(got, "== check-kept-tests", ["test_guide.py::test_no_pier_is_named names the action --show-harbour, which its script does not state", HELD, "1 problem"]), shown(got))
    p = Project("no-actions-stated")
    kept_tests(p)
    # the script's actions stand under another name than the form gives
    p.put("tools/guide.py", swap(fixtures["guide-script"], "FLAGS = (", "ACTIONS = ("))
    got = checked(p)
    check("--check-kept-tests reports a script holding kept tests that states no actions in the form",
          reports(got, "== check-kept-tests", ["%s/conftest.py names no file stating its script's actions under ACTIONS_IN, or the file it names, tools/guide.py, holds no tuple named FLAGS" % GUIDE_SET,
                                               "so its actions cannot be read", HELD, "1 problem"]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "spec-of-one-script-check")
def test_script_check_is_held_by_a_test_citing_it(check, fixtures):
    p = Project("unheld-script-check")
    kept_tests(p)
    a_spec_of_one_check(p, fixtures)
    got = checked(p)
    check("--check-kept-tests reports a Script Check its script carries out, as a record of the specs names the script's skill, that no kept test cites",
          reports(got, "== check-kept-tests", ["the Script Check guide-names-the-quay of guide is held by no kept test where it passes",
                                               "the Script Check guide-names-the-quay of guide is held by no kept test where it reports", HELD, "2 problems"]), shown(got))
    # each test of the set cites the check, in a comment line directly above it
    p.put(GUIDE_TESTS, fixtures["guide-set-tests"].replace("@pytest.mark.action", CITED + "\n@pytest.mark.action"))
    got = checked(p)
    check("--check-kept-tests passes once a test citing the check holds it where it passes and one where it reports", passes(got, "== check-kept-tests", "0 problems"), shown(got))
    p = Project("script-check-not-carried-out")
    kept_tests(p, tests=fixtures["guide-set-tests"].replace("@pytest.mark.action", CITED + "\n@pytest.mark.action"))
    got = checked(p)
    check("--check-kept-tests reports a test citing a Script Check its script does not carry out",
          reports(got, "== check-kept-tests", ["test_guide.py::test_the_quay_is_named cites the Script Check guide-names-the-quay, which its script does not carry out", HELD, "2 problems"]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
def test_file_named_as_agent_instructions_under_the_tests_is_reported(check, fixtures):
    for place in (GUIDE_SET + "/AGENTS.md", KEPT + "/fixtures/notes/agents.md"):
        p = Project("instructions-name")
        kept_tests(p)
        p.put(place, fixtures["notes-citing-nothing"])
        got = checked(p)
        check("--check-kept-tests reports a file kept under the tests at %s, which carries the name of an agent instructions file" % place,
              reports(got, "== check-kept-tests", ["%s carries the name of an agent instructions file" % place, RULE % "no-instructions-name-kept-under-the-tests"]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixtures-index-lists-its-folder]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
def test_index_out_of_step_with_its_folder_is_reported(check, fixtures):
    rule = RULE % "fixtures-index-lists-its-folder"
    p = Project("index-leaves-out")
    kept_tests(p)
    p.put(KEPT + "/fixtures/harbour.md", fixtures["fixture-file-of-one-line"])  # a second fixture file, which the index does not list
    got = checked(p, INDEX)
    check("--check-kept-tests reports a file standing in the fixtures' folder that the index does not list",
          reports(got, "== check-kept-tests", ["%s does not list harbour.md, which stands in its folder" % INDEX, rule]), shown(got))
    p = Project("index-lists-none")
    kept_tests(p)
    p.put(INDEX, fixtures["index-listing-one-file"] + "| `harbour.md` | One sentence naming a harbour |\n")
    got = checked(p, INDEX)
    check("--check-kept-tests reports a file the index lists that does not stand in the fixtures' folder",
          reports(got, "== check-kept-tests", ["%s lists harbour.md, which does not stand in its folder" % INDEX, rule, "1 problem"]), shown(got))
    p = Project("no-index")
    kept_tests(p)
    (p.root / INDEX).unlink()
    got = checked(p)
    check("--check-kept-tests reports a fixtures' folder holding no index", reports(got, "== check-kept-tests", ["%s/fixtures holds no index.md" % KEPT, rule]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
def test_fixture_file_out_of_its_form_is_reported(check, fixtures):
    rule, whole = RULE % "fixture-file-holds-fixtures-in-their-form", fixtures["fixture-file-of-one-line"]
    for label, text, said in (
            ("holding text that is no part of a fixture", whole + "\nA line written beside the fixtures.\n", "%s line 10: text that is no part of a fixture: A line written beside the fixtures." % GUIDE_FIXTURES),
            ("whose fixture lacks its Holds", swap(whole, "    **Holds:** one sentence naming the quay the ferry leaves from \\\n", ""), "%s line 2: the fixture quay-line lacks its Holds, what the snippet holds" % GUIDE_FIXTURES),
            ("whose fixture lacks its Snippet", whole.split("    **Snippet:**")[0], "%s line 2: the fixture quay-line lacks its Snippet" % GUIDE_FIXTURES),
            ("whose fixture's fenced block names no language", swap(whole, "      ```markdown\n", "      ```\n"), "%s line 6: the fenced block of the fixture quay-line names no language" % GUIDE_FIXTURES),
            ("whose fixture's key is no lower-case words joined by hyphens", whole.replace("quay-line", "Quay Line"), "the fixture's key, Quay Line, is not lower-case words joined by hyphens"),
            ("that does not open with its Records field", "# Fixtures\n\n" + whole, "%s line 1: the file does not open with **Records:**, so it holds no fixture in its form" % GUIDE_FIXTURES)):
        p = Project("fixture-form")
        kept_tests(p)
        p.put(GUIDE_FIXTURES, text)
        got = checked(p, GUIDE_FIXTURES)
        check("--check-kept-tests reports a fixture file " + label, reports(got, "== check-kept-tests", [said, rule]), shown(got))
    p = Project("fixture-not-markdown")
    kept_tests(p)
    p.put(KEPT + "/fixtures/notes.txt", fixtures["notes-citing-nothing"])
    p.put(INDEX, fixtures["index-listing-one-file"] + "| `notes.txt` | A page of notes |\n")
    got = checked(p, INDEX)
    check("--check-kept-tests reports a file of the fixtures' folder that is neither its index nor a Markdown file of fixtures",
          reports(got, "== check-kept-tests", ["%s/fixtures/notes.txt is neither the folder's index nor a Markdown file of fixtures" % KEPT, rule, "1 problem"]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: each-fixture-read-by-a-kept-test]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
def test_fixture_no_test_reads_is_reported(check, fixtures):
    rule = RULE % "each-fixture-read-by-a-kept-test"
    p = Project("fixture-unread")
    kept_tests(p)
    # the fixture file given a second fixture, the first under another key, which no test names
    second = fixtures["fixture-file-of-one-line"].split("**Records:**\n")[1].replace("quay-line", "harbour-line")
    p.put(GUIDE_FIXTURES, fixtures["fixture-file-of-one-line"] + "\n" + second)
    got = checked(p)
    check("--check-kept-tests reports a fixture no kept test reads, by its key and its file",
          reports(got, "== check-kept-tests", ["the fixture harbour-line of %s is read by no kept test" % GUIDE_FIXTURES, rule, "1 problem"]), shown(got))
    p = Project("fixture-not-standing")
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.reads(\"guide.md\", \"quay-line\")", "@pytest.mark.reads(\"guide.md\", \"pier-line\")"))
    got = checked(p, KEPT + "/fixtures/index.md")
    check("--check-kept-tests reports a test naming a fixture that does not stand, and the fixture it leaves unread",
          reports(got, "== check-kept-tests", ["test_guide.py::test_the_quay_is_named names the fixture pier-line of guide.md, which does not stand",
                                               "the fixture quay-line of %s is read by no kept test" % GUIDE_FIXTURES, rule, "2 problems"]), shown(got))


@pytest.mark.action("--show-test-coverage")
@pytest.mark.passes
def test_coverage_is_shown_for_every_script(check, fixtures):
    p = Project("coverage-shown")
    kept_tests(p)
    # a registered skill's entry script, which no set of kept tests names: it states the one action, held by no test
    p.put(".ai/skills/audit-specs/scripts/audit-specs.py", fixtures["guide-script"])
    p.run("--check-kept-tests", "docs/guide.md")
    before = p.held(".")
    got = p.run("--show-test-coverage")
    check("--show-test-coverage shows a script whose every action a kept test holds both ways as holding a set of kept tests and nothing unheld, and a script of a skill "
          "holding no kept tests with each action it states as unheld, and fails nothing",
          passes(got, "== show-test-coverage\nguide: a set of kept tests, 2 tests\naudit-specs: no kept tests, 0 tests\n  action --show-guide: held by no kept test where it passes\n"
                      "  action --show-guide: held by no kept test where it reports\n") and " not held\n" in got[1], shown(got))
    check("and it runs no test and writes nothing: the project stands as it was, the last run's report among it", p.held(".") == before and run_holds(p) == ["report.xml"], run_holds(p))


@pytest.mark.action("--show-test-coverage")
@pytest.mark.reports
def test_coverage_shows_what_is_unheld_and_refuses_tests_it_cannot_find(check, fixtures):
    p = Project("coverage-unheld")
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "@pytest.mark.reports\n", ""))
    got = p.run("--show-test-coverage")
    check("--show-test-coverage shows an action of a script holding kept tests that no test holds where it reports, counts it, and fails nothing for it",
          passes(got, "== show-test-coverage\nguide: a set of kept tests, 2 tests\n  action --show-guide: held by no kept test where it reports\n1 not held"), shown(got))
    p.put("tools/guide.py", swap(fixtures["guide-script"], "FLAGS = (", "ACTIONS = ("))
    got = p.run("--show-test-coverage")
    check("--show-test-coverage says of a script stating no actions in the form that its actions cannot be read",
          passes(got, "== show-test-coverage", "guide: a set of kept tests, 2 tests\n  its actions cannot be read: tools/guide.py states none in the form of FLAGS\n0 not held"), shown(got))
    p.put(GUIDE_SET + "/test_broken.py", "def test_broken(:\n")
    got = p.run("--show-test-coverage")
    check("--show-test-coverage refuses where the runner cannot find the tests, exit 2",
          got[0] == 2 and "--show-test-coverage: the runner could not find the kept tests, exit 2" in got[1] and "== show-test-coverage" not in got[1], shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--show-kept-test-times")
@pytest.mark.passes
def test_times_of_the_last_run_are_shown(check, fixtures):
    p = Project("times-shown")
    kept_tests(p, tests=swap(fixtures["guide-set-tests"], "2 + 2 == 4", "2 + 2 == 5"))
    p.run("--check-kept-tests", "docs/guide.md")
    got = p.run("--show-kept-test-times")
    rows = [line.split() for line in got[1].split("\n") if " s  " in line]
    check("--show-kept-test-times shows each test of the last run with its result and its time, read from the run's report, the slowest first",
          passes(got, "== show-kept-test-times, 2 tests") and sorted((row[2], row[3]) for row in rows) == [("failed", "scripts.guide.test_guide::test_no_pier_is_named"),
                                                                                                            ("passed", "scripts.guide.test_guide::test_the_quay_is_named")]
          and [float(row[0]) for row in rows] == sorted((float(row[0]) for row in rows), reverse=True), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-test-results-read-from-the-report]
@pytest.mark.action("--show-kept-test-times")
@pytest.mark.reports
def test_times_are_refused_where_no_report_in_the_schema_stands(check, fixtures):
    p = Project("times-refused")
    kept_tests(p)
    got = p.run("--show-kept-test-times")
    check("--show-kept-test-times refuses where no run has left a report, exit 2",
          got[0] == 2 and "--show-kept-test-times reads %s/report.xml: the run left no report at report.xml" % KEPT_RUN in got[1], shown(got))
    p.run("--check-kept-tests", "docs/guide.md")
    report = p.read(KEPT_RUN + "/report.xml")
    p.put(KEPT_RUN + "/report.xml", swap(report, "<testcase ", "<testcase ferry=\"north quay\" "))  # an attribute the schema declares of no test
    got = p.run("--show-kept-test-times")
    check("--show-kept-test-times refuses a report out of the registered schema, exit 2",
          got[0] == 2 and "the run's report is out of the registered schema: testcase holds the attribute ferry" in got[1], shown(got))
    p.put(KEPT_RUN + "/report.xml", report.split("<testcase")[0])
    got = p.run("--show-kept-test-times")
    check("--show-kept-test-times refuses a report that is no XML, exit 2", got[0] == 2 and "the run's report is no XML" in got[1], shown(got))
