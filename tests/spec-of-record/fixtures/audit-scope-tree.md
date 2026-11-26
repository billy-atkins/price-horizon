**Records:**
  - **Fixture:** bakery-scope-drawn-whole \
    **Holds:** a Markdown file titled The Scope of a Bakery, whose section The Shape of the Scope holds a tree in a fenced block naming `specs/`, `methodology/` under it, and under that `index.md`, `loaves.md` and `scope/` \
    **Snippet:**

      ````markdown
      # The Scope of a Bakery

      ## The Shape of the Scope

      ```
      specs/
      └── methodology/
          ├── index.md
          ├── loaves.md
          └── scope/
      ```
      ````

  - **Fixture:** bakery-scope-drawn-without-loaves \
    **Holds:** a Markdown file titled The Scope of a Bakery, whose section The Shape of the Scope holds a tree in a fenced block naming `specs/`, `methodology/` under it, and under that `index.md` and `scope/` \
    **Snippet:**

      ````markdown
      # The Scope of a Bakery

      ## The Shape of the Scope

      ```
      specs/
      └── methodology/
          ├── index.md
          └── scope/
      ```
      ````

  - **Fixture:** bakery-scope-drawn-into-its-folder \
    **Holds:** a Markdown file titled The Scope of a Bakery, whose section The Shape of the Scope holds a tree in a fenced block naming `specs/`, `methodology/` under it, under that `index.md`, `loaves.md` and `scope/`, and under `scope/` the file `what-spec-of-record-governs.md` \
    **Snippet:**

      ````markdown
      # The Scope of a Bakery

      ## The Shape of the Scope

      ```
      specs/
      └── methodology/
          ├── index.md
          ├── loaves.md
          └── scope/
              └── what-spec-of-record-governs.md
      ```
      ````

  - **Fixture:** bakery-scope-with-no-tree \
    **Holds:** a Markdown file titled The Scope of a Bakery, whose section The Shape of the Scope holds one sentence and no fenced block \
    **Snippet:**

      ```markdown
      # The Scope of a Bakery

      ## The Shape of the Scope

      The bakery keeps its recipes in one folder.
      ```

  - **Fixture:** index-of-a-bakery-methodology \
    **Holds:** an index titled The Bakery's Methods, a table of two rows naming a file `loaves.md` and a folder `scope/` \
    **Snippet:**

      ```markdown
      # The Bakery's Methods

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `loaves.md` | How a loaf is shaped |
      | `scope/` | What the bakery's methods cover |
      ```

  - **Fixture:** bakery-loaves \
    **Holds:** a Markdown file on shaping loaves of a title and one sentence \
    **Snippet:**

      ```markdown
      # Loaves

      Each loaf is shaped by hand.
      ```
