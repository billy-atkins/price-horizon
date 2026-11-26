**Records:**
  - **Fixture:** literal-text-in-single-backticks \
    **Holds:** a Markdown file on a bakery holding code spans of one backtick, a citation of a section in one backtick, a citation in two backticks of a heading holding a backtick, a fenced block and an indented code block each holding a run of two backticks \
    **Snippet:**

      ````markdown
      # The Bakery

      The oven is set to `200` degrees, as `specs/bakery.md § Ovens` says.

      The rye's own section is ``specs/bakery.md § The `Rye` Loaf``.

      ```text
      a label reads ``rye``
      ```

      Each label is printed as:

          ``spelt``
      ````

  - **Fixture:** literal-text-in-double-backticks \
    **Holds:** a Markdown file on a bakery whose second paragraph holds a code span of two backticks holding no backtick \
    **Snippet:**

      ```markdown
      # The Bakery

      Each loaf is weighed.

      The oven is set to ``200`` degrees.
      ```

  - **Fixture:** literal-text-citation-in-double-backticks \
    **Holds:** a Markdown file on a bakery whose second paragraph holds a citation of a section in two backticks, its text holding no backtick \
    **Snippet:**

      ```markdown
      # The Bakery

      Each loaf is weighed.

      The ovens are set as ``specs/bakery.md § Ovens`` says.
      ```
