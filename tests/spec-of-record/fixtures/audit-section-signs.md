**Records:**
  - **Fixture:** section-signs-in-backticks \
    **Holds:** a Markdown file on a harbor holding a citation of a section, a code span holding a section sign alone, and a fenced block holding a section sign outside any backticks \
    **Snippet:**

      ````markdown
      # The Harbor

      Moorings are let as `specs/harbor.md § Moorings` says.

      The sign `§` marks a section.

      ```text
      see Moorings § Pontoons
      ```
      ````

  - **Fixture:** section-sign-in-prose \
    **Holds:** a Markdown file on a harbor whose second paragraph names a section with a section sign outside any backticks \
    **Snippet:**

      ```markdown
      # The Harbor

      Each boat takes one mooring.

      See Moorings § Pontoons for the berths.
      ```

  - **Fixture:** section-sign-in-a-table-cell \
    **Holds:** a Markdown file on a harbor holding a table whose one row has a cell naming a section with a section sign outside any backticks \
    **Snippet:**

      ```markdown
      # The Harbor

      | Berth | Rule |
      |---|---|
      | Pontoon | Moorings § Pontoons |
      ```
