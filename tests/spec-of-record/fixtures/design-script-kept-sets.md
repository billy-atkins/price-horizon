**Records:**
  - **Fixture:** guide-script \
    **Holds:** a Python script stating one action, `--show-guide`, in a tuple named FLAGS at its top level, and printing two words \
    **Snippet:**

      ```python
      """Shows the island's guide."""
      FLAGS = (
          ("--show-guide", "", None, "show the guide"),
      )
      print("the guide")
      ```

  - **Fixture:** guide-set-conftest \
    **Holds:** the conftest.py of a set of kept tests, naming one file of code, `tools/guide.py`, one file a form is read from, `docs/guide.md`, and `tools/guide.py` as the file stating the script's actions \
    **Snippet:**

      ```python
      SCRIPT_FILES = ("tools/guide.py",)
      FORM_FILES = ("docs/guide.md",)
      ACTIONS_IN = "tools/guide.py"
      ```

  - **Fixture:** guide-set-tests \
    **Holds:** a file of two tests written for pytest, each naming the action `--show-guide`: one marked passes, reading the fixture quay-line of the fixture file guide.md and checking that it names a quay, and one marked reports, checking a sum \
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
          check("two and two make four", 2 + 2 == 4)
      ```

  - **Fixture:** fixture-file-of-one-line \
    **Holds:** a fixture file holding one fixture, quay-line, whose snippet is one Markdown sentence naming the north quay \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** index-listing-one-file \
    **Holds:** the index of a fixtures folder, a title and a table listing one file, guide.md, with its description \
    **Snippet:**

      ```markdown
      # The Kept Tests' Fixtures

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `guide.md` | One sentence naming the quay a ferry leaves from |
      ```

  - **Fixture:** tides-script \
    **Holds:** a Python script stating one action, `--show-tides`, in a tuple named FLAGS at its top level \
    **Snippet:**

      ```python
      """Shows the island's tides."""
      FLAGS = (
          ("--show-tides", "", None, "show the tides"),
      )
      ```

  - **Fixture:** tides-set-conftest \
    **Holds:** the conftest.py of a set of kept tests, naming one file of code, `tools/tides.py`, no file a form is read from, and `tools/tides.py` as the file stating the script's actions \
    **Snippet:**

      ```python
      SCRIPT_FILES = ("tools/tides.py",)
      FORM_FILES = ()
      ACTIONS_IN = "tools/tides.py"
      ```

  - **Fixture:** tides-set-tests \
    **Holds:** a file of two tests written for pytest, each naming the action `--show-tides` and reading no fixture: one marked passes and one marked reports, each checking a sum \
    **Snippet:**

      ```python
      import pytest


      @pytest.mark.action("--show-tides")
      @pytest.mark.passes
      def test_the_tide_comes_in(check):
          check("one and one make two", 1 + 1 == 2)


      @pytest.mark.action("--show-tides")
      @pytest.mark.reports
      def test_the_tide_goes_out(check):
          check("two less one leaves one", 2 - 1 == 1)
      ```

  - **Fixture:** comparison-listing-one-design \
    **Holds:** a Python script printing one line naming a design, `design .ai/plans/design-specs/other-design.md`, then a line counting one design read differently \
    **Snippet:**

      ```python
      print("design .ai/plans/design-specs/other-design.md")
      print("")
      print("1 design read differently, of 1")
      ```

  - **Fixture:** test-ending-its-process \
    **Holds:** a file of one test written for pytest, which ends the process running it at once, with exit status 3 \
    **Snippet:**

      ```python
      import os


      def test_ends_the_process():
          os._exit(3)
      ```

  - **Fixture:** test-recording-a-property \
    **Holds:** a file of one test written for pytest, which records a property named ferry within its own entry of the run's report \
    **Snippet:**

      ```python
      def test_records_a_property(record_property):
          record_property("ferry", "north quay")
      ```

  - **Fixture:** test-standing-in \
    **Holds:** a file of one test written for pytest, naming no action and reading no fixture, which passes \
    **Snippet:**

      ```python
      def test_stands_in():
          assert True
      ```

  - **Fixture:** canon-of-the-tide-tables \
    **Holds:** the files of a project's canon, one path to a line: a spec of the tides and the code reading its tables \
    **Snippet:**

      ```text
      specs/methodology/tides.md
      .ai/skills/lib/tide_tables.py
      ```

  - **Fixture:** code-naming-the-canon-in-annotations-alone \
    **Holds:** a Python file about the tides naming the canon of the tide tables in a spec annotation alone, its other comments and its docstrings naming none of its files and no section, though a docstring names files whose names hold a canon file's name, and a string holds a section sign \
    **Snippet:**

      ```python
      """Reads the hours of the tides from the table kept beside the harbor."""
      import re

      # @canon-spec specs/methodology/tides.md § Tides § High Water
      HIGH = re.compile(r"high")  # the hour the water stands highest


      def hours(text):
          """-> each hour the table gives; tides.mdx and old_tide_tables.py are no files of the canon."""
          sign = "§ Tides"  # a string, which no reading takes as a comment
          return HIGH.findall(text), sign
      ```

  - **Fixture:** code-naming-a-section-after-code \
    **Holds:** a line of Python about the tides whose comment after its code names a section by a section sign \
    **Snippet:**

      ```python
      HIGH = "high"  # the hour § Tides § High Water gives
      ```

  - **Fixture:** code-naming-a-canon-file-by-its-name \
    **Holds:** a Python function about the tides whose docstring names a file of the canon of the tide tables by its file name alone \
    **Snippet:**

      ```python
      def hours(text):
          """-> each hour the table gives, read as tide_tables.py reads it."""
          return text.split()
      ```

  - **Fixture:** code-naming-a-canon-path-on-a-line-of-its-own \
    **Holds:** a Python comment on a line of its own, which is no spec annotation, naming a file of the canon of the tide tables by its path \
    **Snippet:**

      ```python
      # the hours, as specs/methodology/tides.md has them read
      HIGH = "high"
      ```
