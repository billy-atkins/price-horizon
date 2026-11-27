**Records:**
  - **Fixture:** read-again-and-read-against \
    **Holds:** a Markdown file of two sections, one sentence holding the words read against and the other the words read again \
    **Snippet:**

      ```markdown
      # Reading

      ## Reading a Report

      Each place a report names is read against the files as they stand, and never from memory.

      ## Reading It Twice

      A report changed since it was checked is read again before its entry is appended.
      ```

  - **Fixture:** run-again-together-and-apart \
    **Holds:** a Markdown file of three sections: one sentence holding the words runs and again with other words between them, one holding the words run again together, and two sentences of one line, the first ending on the word run and the second opening with the word again \
    **Snippet:**

      ```markdown
      # Running

      ## A Check's Runs

      The script checks a report by the same checks it made before, and runs each Search again.

      ## A Second Run

      Where a file has changed since, the search is run again.

      ## Two Sentences

      Each report waits until its checks have run. Again, its entry waits until they pass.
      ```

  - **Fixture:** identifier-together-and-its-words-apart \
    **Holds:** a Markdown file of two sections, one sentence naming the identifier TypeScript and the other holding the words type and script with other words between them \
    **Snippet:**

      ```markdown
      # Building

      ## The Web UI

      The Web UI is written in TypeScript and compiled before it ships.

      ## A Check

      The type of each value is read before the script checks it.
      ```

  - **Fixture:** run-and-again-in-rows-cells-and-fields \
    **Holds:** a Markdown file of a table and a record, the word run ending one table row and the word again opening the next, the two words in two cells of one row, and the two words in two fields of one record, with no sentence holding both \
    **Snippet:**

      ```markdown
      # Checks

      | Check | What it does |
      |---|---|
      | first | the builder runs |
      | second | the reviewer looks again |
      | runs | again |

      **Records:**
        - **Name:** a check the builder runs \
          **When:** again at each round
      ```

  - **Fixture:** run-again-apart-in-a-cell-a-field-and-a-wrapped-paragraph \
    **Holds:** a Markdown file holding the words runs and again with other words between them in one table cell, in one field's value of a record, and in one sentence of a paragraph wrapped across two lines \
    **Snippet:**

      ```markdown
      # Rounds

      | Round | What happens |
      |---|---|
      | second | the builder runs each check again |

      **Records:**
        - **Name:** a later round \
          **When:** the reviewer runs every Search once again

      A report handed back late is held while the script runs
      each of its Searches again over the files.
      ```

  - **Fixture:** run-again-apart-in-fences-and-a-heading \
    **Holds:** a Markdown file holding the words runs and again with other words between them in a heading, in a fenced block holding Markdown, and in a fenced block holding plain text \
    **Snippet:**

      ```markdown
      # Fences

      ## The Script Runs Each Search Again

      An example of a report's prose:

      ~~~markdown
      The checker runs each Search again before it passes.
      ~~~

      An example of a log line:

      ~~~text
      the checker runs each Search again before it passes
      ~~~
      ```

  - **Fixture:** run-again-apart-in-code-fences \
    **Holds:** a Markdown file holding a fenced block of Python, one of TypeScript and one of C#, each with a comment holding the words runs and again with other words between them and code naming run again together \
    **Snippet:**

      ```markdown
      # Examples

      A checker in Python:

      ~~~python
      # The checker runs each Search again.
      ran = run_again(report)
      ~~~

      A checker in TypeScript:

      ~~~ts
      // The reviewer runs every check again.
      const ran = runAgain(report);
      ~~~

      A checker in C#:

      ~~~csharp
      // The auditor runs one check again.
      var ran = RunAgain(report);
      ~~~
      ```

  - **Fixture:** run-again-apart-in-python-comments-docstrings-and-code \
    **Holds:** a Python file holding the words runs and again with other words between them in a comment wrapped over two lines, in a docstring, and in a string the code holds, with the words run and again together in a comment, in a function's name a comment follows on the next line, and in code a comment follows on its own line \
    **Snippet:**

      ```python
      """A checker of reports, which runs each Search again before it passes a report."""


      def check(report):
          # The checker runs
          # each Search again.
          said = "the checker runs each Search again"
          return said  # it is run again here


      def run_again(report):
          # each report is read once
          ran = run_again_later(report)  # read once more
          return ran
      ```
