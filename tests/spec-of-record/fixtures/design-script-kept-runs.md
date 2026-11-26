**Records:**
  - **Fixture:** kept-runner-settings \
    **Holds:** the settings of a runner of kept tests written for pytest: its tests under scripts in files named test_, each module imported by its path, no cache, the report in the xunit2 form, and four markers declared, action, passes, reports and reads \
    **Snippet:**

      ```ini
      [pytest]
      testpaths = scripts
      python_files = test_*.py
      junit_family = xunit2
      addopts = -p no:cacheprovider --import-mode=importlib
      markers =
          action: an action of its script the test holds
          passes: the test holds what it names where that passes
          reports: the test holds what it names where that reports
          reads: the fixtures the test takes
      ```

  - **Fixture:** kept-runner-conftest \
    **Holds:** the conftest.py of a runner of kept tests written for pytest, standing beside its settings: it takes the folder of its run from the variable SPEC_OF_RECORD_KEPT_RUN, or the project's .ai/tmp/kept-tests, and puts the runner's temporary folders there; given --kept-links and a file, it writes into that file, as JSON, a row of each test found, its node id, its file from the project's root, the actions it names, no Script Check, the ways its markers give with the names each holds, and the fixtures its reads markers name; and it hands a test work, a folder of its own in the run's folder, fixtures, the whole text of each fixture file the test names under each key the test names of it, and check, a function asserting that what it is given holds \
    **Snippet:**

      ```python
      """Hands each kept test of a project its folder, its fixtures and a check, and writes what each test names where
      asked."""
      import json
      import os
      from pathlib import Path

      import pytest

      TESTS = Path(__file__).resolve().parent
      ROOT = TESTS.parent.parent
      RUN = Path(os.environ.get("SPEC_OF_RECORD_KEPT_RUN") or ROOT / ".ai" / "tmp" / "kept-tests")


      def pytest_addoption(parser):
          parser.addoption("--kept-links", default=None)


      def pytest_configure(config):
          if not config.option.basetemp:
              config.option.basetemp = str(RUN / "runner")


      def named(item, marker):
          return [str(a) for m in item.iter_markers(marker) for a in m.args]


      def pytest_collection_modifyitems(config, items):
          links = config.getoption("--kept-links")
          if links:
              rows = [{"test": item.nodeid, "file": Path(str(item.path)).resolve().relative_to(ROOT).as_posix(),
                       "actions": named(item, "action"), "script_checks": [],
                       "ways": {way: named(item, way) for way in ("passes", "reports") if item.get_closest_marker(way)},
                       "reads": [[str(m.args[0]), str(key)] for m in item.iter_markers("reads") for key in m.args[1:]]}
                      for item in items]
              Path(links).parent.mkdir(parents=True, exist_ok=True)
              Path(links).write_text(json.dumps(rows), encoding="utf-8")


      @pytest.fixture
      def work(request):
          folder = RUN / "work" / request.node.name
          folder.mkdir(parents=True, exist_ok=True)
          return folder


      @pytest.fixture
      def fixtures(request):
          return {str(key): (TESTS / "fixtures" / str(m.args[0])).read_text(encoding="utf-8")
                  for m in request.node.iter_markers("reads") for key in m.args[1:]}


      @pytest.fixture
      def check():
          def holds(what, held, detail=""):
              assert held, what
          return holds
      ```

  - **Fixture:** guide-set-tests-one-failing \
    **Holds:** a file of two tests written for pytest, each naming the action `--show-guide`: one marked passes, reading the fixture quay-line of the fixture file guide.md and checking that it names a quay, and one marked reports, checking that two and two make five \
    **Snippet:**

      ```python
      import pytest


      @pytest.mark.action("--show-guide")
      @pytest.mark.passes
      @pytest.mark.reads("guide.md", "quay-line")
      def test_the_quay_is_named(fixtures, check):
          check("the line names the quay", "quay" in fixtures["quay-line"], fixtures["quay-line"])


      @pytest.mark.action("--show-guide")
      @pytest.mark.reports
      def test_no_pier_is_named(check):
          check("two and two make four", 2 + 2 == 5)
      ```

  - **Fixture:** guide-set-tests-holding-no-test-where-it-reports \
    **Holds:** a file of two tests written for pytest, each naming the action `--show-guide`: one marked passes, reading the fixture quay-line of the fixture file guide.md and checking that it names a quay, and one marked neither passes nor reports, checking a sum \
    **Snippet:**

      ```python
      import pytest


      @pytest.mark.action("--show-guide")
      @pytest.mark.passes
      @pytest.mark.reads("guide.md", "quay-line")
      def test_the_quay_is_named(fixtures, check):
          check("the line names the quay", "quay" in fixtures["quay-line"], fixtures["quay-line"])


      @pytest.mark.action("--show-guide")
      def test_no_pier_is_named(check):
          check("two and two make four", 2 + 2 == 4)
      ```

  - **Fixture:** guide-set-tests-citing-a-script-check \
    **Holds:** a file of two tests written for pytest, the first under a comment of its own and then two canon-spec annotations, one citing the section Proving of specs/methodology/loaves.md and one its Script Check record loaf-proved-an-hour, above its decorators, and the second under no annotation \
    **Snippet:**

      ```python
      import pytest


      # the quay, as the guide names it
      # @canon-spec specs/methodology/loaves.md § Proving
      # @canon-spec specs/methodology/loaves.md § Proving § Script Checks [Name: loaf-proved-an-hour]
      @pytest.mark.action("--show-guide")
      @pytest.mark.passes
      def test_the_quay_is_named(check):
          check("the guide names the quay", True)


      @pytest.mark.action("--show-guide")
      @pytest.mark.reports
      def test_no_pier_is_named(check):
          check("two and two make four", 2 + 2 == 4)
      ```

  - **Fixture:** ledger-set-conftest-naming-its-code-as-one-path \
    **Holds:** the conftest.py of a set of kept tests naming the file of its script's code, `tools/ledger.py`, as one path and not as a tuple of paths, no file a form is read from, and `tools/ledger.py` as the file stating the script's actions \
    **Snippet:**

      ```python
      SCRIPT_FILES = "tools/ledger.py"
      FORM_FILES = ()
      ACTIONS_IN = "tools/ledger.py"
      ```

  - **Fixture:** tests-file-holding-no-test \
    **Holds:** a Python file importing pytest and holding nothing else \
    **Snippet:**

      ```python
      import pytest
      ```

  - **Fixture:** tests-file-of-no-python \
    **Holds:** a line opening a Python function whose parameters are never closed, so the file is no Python \
    **Snippet:**

      ```python
      def test_broken(:
      ```

  - **Fixture:** comparison-that-cannot-be-made \
    **Holds:** a Python script printing one line naming a design, `design .ai/plans/design-specs/other-design.md`, and then ending with exit status 2 \
    **Snippet:**

      ```python
      print("design .ai/plans/design-specs/other-design.md")
      raise SystemExit(2)
      ```

  - **Fixture:** comparison-listing-no-design \
    **Holds:** a Python script printing an empty line, then a line counting no design read differently, of one \
    **Snippet:**

      ```python
      print("")
      print("0 designs read differently, of 1")
      ```

  - **Fixture:** guide-script-stating-two-actions \
    **Holds:** a Python script stating two actions, `--show-guide` and `--check-guide`, in a tuple named FLAGS at its top level, and printing two words \
    **Snippet:**

      ```python
      """Shows the island's guide, and checks it."""
      FLAGS = (
          ("--show-guide", "", None, "show the guide"),
          ("--check-guide", "", None, "check the guide"),
      )
      print("the guide")
      ```

  - **Fixture:** guide-script-stating-its-actions-under-another-name \
    **Holds:** a Python script stating one action, `--show-guide`, in a tuple named ACTIONS at its top level, and no tuple named FLAGS \
    **Snippet:**

      ```python
      """Shows the island's guide."""
      ACTIONS = (
          ("--show-guide", "", None, "show the guide"),
      )
      print("the guide")
      ```

  - **Fixture:** kept-report-of-two-tests \
    **Holds:** a run's report in the JUnit XML form of one suite of two tests of scripts.guide.test_guide: test_the_quay_is_named, passed in 0.010 seconds, and test_no_pier_is_named, failed in 0.030 seconds with an assertion that two and two make four \
    **Snippet:**

      ```xml
      <?xml version="1.0" encoding="utf-8"?>
      <testsuites name="pytest tests">
        <testsuite name="pytest" errors="0" failures="1" skipped="0" tests="2" time="0.050" timestamp="2026-11-25T10:00:00.000000+00:00" hostname="harbor">
          <testcase classname="scripts.guide.test_guide" name="test_the_quay_is_named" time="0.010" />
          <testcase classname="scripts.guide.test_guide" name="test_no_pier_is_named" time="0.030">
            <failure message="AssertionError: two and two make four">AssertionError: two and two make four</failure>
          </testcase>
        </testsuite>
      </testsuites>
      ```

  - **Fixture:** kept-report-holding-an-undeclared-attribute \
    **Holds:** a run's report in the JUnit XML form of one suite of one passed test, whose testcase holds an attribute ferry beside its own \
    **Snippet:**

      ```xml
      <?xml version="1.0" encoding="utf-8"?>
      <testsuites name="pytest tests">
        <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="0.010">
          <testcase classname="scripts.guide.test_guide" name="test_the_quay_is_named" time="0.010" ferry="north quay" />
        </testsuite>
      </testsuites>
      ```

  - **Fixture:** kept-report-holding-an-undeclared-element \
    **Holds:** a run's report in the JUnit XML form of one suite of one passed test, whose testcase holds an element crossing \
    **Snippet:**

      ```xml
      <?xml version="1.0" encoding="utf-8"?>
      <testsuites name="pytest tests">
        <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="0.010">
          <testcase classname="scripts.guide.test_guide" name="test_the_quay_is_named" time="0.010">
            <crossing />
          </testcase>
        </testsuite>
      </testsuites>
      ```

  - **Fixture:** kept-report-of-a-test-lacking-its-name \
    **Holds:** a run's report in the JUnit XML form of one suite of one passed test, whose testcase holds a classname and a time and no name \
    **Snippet:**

      ```xml
      <?xml version="1.0" encoding="utf-8"?>
      <testsuites name="pytest tests">
        <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="0.010">
          <testcase classname="scripts.guide.test_guide" time="0.010" />
        </testsuite>
      </testsuites>
      ```

  - **Fixture:** kept-report-that-is-no-xml \
    **Holds:** the opening of a run's report in the JUnit XML form, cut off within its second element, so it is no XML \
    **Snippet:**

      ```xml
      <?xml version="1.0" encoding="utf-8"?>
      <testsuites name="pytest tests">
        <testsuite name="pytest" errors="0" fail
      ```

  - **Fixture:** ferry-self-review-report-judging-the-other-design \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, four Builder Checks, of steers against the user's messages, of linked work, of the problem's re-evaluation and a differential test whose Places Checked name the design other-design, and a Settlement naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
        - `docs/guide.md`

      ## Builder Checks

      **Records:**
        - **Check:** steers-read-against-the-messages \
          **Kind:** steers against the user's messages \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Result:** The design records no steer, and the user gave none.

        - **Check:** work-handed-on \
          **Kind:** linked work \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Out of Scope`

          **Result:** The design hands no work on.

        - **Check:** problem-read-against-the-guide \
          **Kind:** problem re-evaluation \
          **Places Checked:**
            - `docs/guide.md § The Ferry`

          **Result:** The section still names the ferry and gives no time.

        - **Check:** comparison-judged \
          **Kind:** differential test \
          **Places Checked:**
            - `.ai/plans/design-specs/other-design.md`

          **Result:** The other design reads differently as the change meant it to.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** ferry-self-review-report-judging-its-own-design \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, four Builder Checks, of steers against the user's messages, of linked work, of the problem's re-evaluation and a differential test whose Places Checked name the design ferry-times-in-the-guide itself, and a Settlement naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
        - `docs/guide.md`

      ## Builder Checks

      **Records:**
        - **Check:** steers-read-against-the-messages \
          **Kind:** steers against the user's messages \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Result:** The design records no steer, and the user gave none.

        - **Check:** work-handed-on \
          **Kind:** linked work \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Out of Scope`

          **Result:** The design hands no work on.

        - **Check:** problem-read-against-the-guide \
          **Kind:** problem re-evaluation \
          **Places Checked:**
            - `docs/guide.md § The Ferry`

          **Result:** The section still names the ferry and gives no time.

        - **Check:** comparison-judged \
          **Kind:** differential test \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Result:** The design reads differently as the change meant it to.

      ## Settlement

      **Earlier Reports:**
        - none
      ```
