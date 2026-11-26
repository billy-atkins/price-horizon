**Records:**
  - **Fixture:** target-spec-citing-its-own-section \
    **Holds:** a Markdown file titled Target File holding text before its first section, a section Target with two records and a child section, and a section Table with a named table of two states, then a last line citing `specs/target.md § Target` \
    **Snippet:**

      ```markdown
      # Target File

      Text before the first section.

      ## Target

      The target section's own text. A ledger entry is posted once.

      **Records:**
        - **Name:** first-record \
          **Holds:** the first record

        - **Name:** second-record \
          **Holds:** the second record

      ### Child

      The child section's text.

      ## Table

      **Table Name:** States

      | State | Means |
      |---|---|
      | open | it is open |
      | closed | it is closed |

      A line added, citing `specs/target.md § Target` from its own file.
      ```

  - **Fixture:** heron-spec-cited-in-its-own-file-with-a-second-heron \
    **Holds:** a Markdown file titled Target File with a section Target of one sentence about a heron, and a section Citing that cites `specs/target.md § Target` and then says a second heron came \
    **Snippet:**

      ```markdown
      # Target File

      ## Target

      The heron stands in the reeds.

      ## Citing

      The reeds are cited as `specs/target.md § Target`.

      A second heron came.
      ```

  - **Fixture:** heron-spec-retitled \
    **Holds:** a Markdown file titled Target File with one section, Retitled, of one sentence about a heron in the reeds, and no section Target \
    **Snippet:**

      ```markdown
      # Target File

      ## Retitled

      The heron stands in the reeds.
      ```

  - **Fixture:** heron-spec-with-an-egret-not-yet-committed \
    **Holds:** a Markdown file titled Target File with one section, Target, of a sentence about a heron in the reeds and a sentence saying the egret is not yet committed \
    **Snippet:**

      ```markdown
      # Target File

      ## Target

      The heron stands in the reeds.

      The egret is not yet committed.
      ```

  - **Fixture:** heron-spec-changed-in-the-reeds \
    **Holds:** a Markdown file titled Target File with one section, Target, of one sentence saying a heron stands in the reeds, changed \
    **Snippet:**

      ```markdown
      # Target File

      ## Target

      The heron stands in the reeds, changed.
      ```

  - **Fixture:** plan-naming-the-heron-changed \
    **Holds:** a Markdown file titled Another Plan whose one section, Notes, names a heron, says it is changed, and cites nothing \
    **Snippet:**

      ```markdown
      # Another Plan

      ## Notes

      A heron in another plan, changed.
      ```

  - **Fixture:** design-naming-the-heron-changed \
    **Holds:** a Markdown file titled Design Document whose one section, The Problem, names a heron, says it is changed, and cites nothing \
    **Snippet:**

      ```markdown
      # Design Document

      ## The Problem

      The heron, changed.
      ```
