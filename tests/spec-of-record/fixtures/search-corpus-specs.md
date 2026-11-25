**Records:**
  - **Fixture:** forms-spec \
    **Holds:** a Markdown file titled Forms that cites `specs/target.md` in many forms, plain, with a doubled space, broken across two lines, carrying a link, of a child section, of a keyed part and of the whole file, and holds a tilde fence, a fence indented in a list item, a fence nested in a longer one, a heading path standing twice with a record under each, one term in several written forms, and the word quillwort in running text, a keyed table, an unkeyed table, records, a fenced block, an indented code block and a heading \
    **Snippet:**

      `````markdown
      # Forms

      This file holds each form of heading, fenced block, table, keyed part and citation the search must read. Its faults are deliberate.

      ## Citations

      A plain citation: `specs/target.md § Target`.

      A citation with a doubled space: `specs/target.md §  Target`.

      A citation broken across lines: `specs/target.md §
      Target`.

      A citation carrying its link: [`specs/target.md § Target`](/specs/target.md#target).

      A citation of a section within it: `specs/target.md § Target § Child`.

      A citation of a part of it: `specs/target.md § Target [Name: first-record]`.

      A citation of its file: `specs/target.md`.

      A mention that is no citation: `Target`, and the words specs/target.md § Target outside any code span.

      ## Fences

      A tilde fence holds a heading and a citation:

      ~~~text
      ## Not A Heading In Tildes
      `specs/target.md § Target`
      ~~~

      A list item holds an indented fence:

      - An item.

        ```text
        ## Not A Heading In An Item
        ```

      A longer fence holds a shorter one:

      ````markdown
      ## Not A Heading In The Outer Fence

      ```text
      inner
      ```

      ## Still Not A Heading

      A same-file citation of the block's own file: `§ Still Not A Heading`.
      ````

      A backtick fence holds a citation in a code span and one written bare, as a brief writes one:

      ```text
      The span: `specs/target.md § Target`
      Do the work as specs/target.md § Target § Child sets it, then stop.
      ```

      A fenced annotation:

      ```python
      # @canon-spec specs/target.md § Target
      ```

      ## After The Fences

      A citation after every fenced block, placed at its own line: `specs/target.md § Table`.

      ## Twice

      The first section of this path.

      The keeper of the northern lighthouse trims the lamp wick each evening before dusk falls, as `specs/forms.md § Terms` words it.

      **Records:**
        - **Name:** lamp-first \
          **Holds:** the wick trimmed at dusk

      ## Twice

      The second section of this path.

      The ferry across the estuary carries no more than forty passengers when the spring tide is running, as `specs/forms.md § Terms` words it.

      **Records:**
        - **Name:** lamp-second \
          **Holds:** the ferry's forty passengers

      ## Terms

      The function append_entry posts one line.

      The flag --append-entry does the same.

      The class AppendEntry wraps it.

      They were appending entries all day.

      Nothing here appends an unrelated thing to an entry.

      A phrase broken across two lines: the clerk will append
      entry after entry to the book.

      The LE is posted once, and so is each journal line.

      ## Where A Place Stands

      Running text holding the word quillwort.

      A table declaring its key, each row a keyed part, one holding the word and one a citation:

      **Reference Key:** Form

      | Form | Holds |
      |---|---|
      | plain | a tabled quillwort |
      | cited | `specs/target.md § Table` |

      A table declaring no key, whose rows are no keyed parts:

      | Unkeyed | Holds |
      |---|---|
      | a row | an unkeyed quillwort |

      Records, each a keyed part, the second sharing its key with the first, so its citation would name the first, and the third keyed by a code span:

      **Records:**
        - **Name:** a-record \
          **Holds:** a recorded quillwort

        - **Name:** a-record \
          **Holds:** a second quillwort under the same key

        - **Name:** `coded-record` \
          **Holds:** a quillwort under a key no citation can write, since it holds a code span

      ```text
      A fenced line holding quillwort.
      ```

          An indented code block's line holding quillwort.

      ### A Heading Holding Quillwort

      The last of them, in running text again: quillwort.
      `````

  - **Fixture:** target-spec \
    **Holds:** a Markdown file titled Target File holding text before its first section, a section Target with two records and a child section, and a section Table with a named table of two states \
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
      ```

  - **Fixture:** promise-product-file \
    **Holds:** a Markdown file whose front matter names `specs/target.md` under `technical-specs`, with one section saying each posting is written exactly one time \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/target.md
      ---

      # Promise

      ## What Is Promised

      Each posting is written exactly one time.
      ```

  - **Fixture:** ledger-glossary \
    **Holds:** a glossary table of two terms, giving the term ledger entry the abbreviation LE and the other name journal line \
    **Snippet:**

      ```markdown
      ## Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Ledger entry | LE | A posted line of the ledger. Also called journal line. |
      | Posting |  | The act of writing a ledger entry. |
      ```
