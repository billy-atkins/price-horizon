**Records:**
  - **Fixture:** bakery-working-files \
    **Holds:** a Markdown file titled Working Files whose section The Working Files holds a table of two rows naming the folder `.bakery/drafts/` and the file `.bakery/oven-log.md` \
    **Snippet:**

      ```markdown
      # Working Files

      ## The Working Files

      | File | Holds |
      |---|---|
      | `.bakery/drafts/` | recipes being tried |
      | `.bakery/oven-log.md` | each bake's temperatures |
      ```

  - **Fixture:** bakery-working-files-untabled \
    **Holds:** a Markdown file titled Working Files whose section The Working Files holds one sentence and no table \
    **Snippet:**

      ```markdown
      # Working Files

      ## The Working Files

      The bakery keeps its drafts apart.
      ```

  - **Fixture:** ignore-the-bakery-folder \
    **Holds:** an ignore file of a comment line and one line naming the folder `.bakery/` \
    **Snippet:**

      ```gitignore
      # what the bakery keeps out of version control
      .bakery/
      ```

  - **Fixture:** ignore-the-drafts-alone \
    **Holds:** an ignore file of one line naming the folder `.bakery/drafts/` \
    **Snippet:**

      ```gitignore
      .bakery/drafts/
      ```

  - **Fixture:** ignore-the-bakery-folder-but-its-log \
    **Holds:** an ignore file of a line naming the folder `.bakery/` and a line opening with `!` naming `.bakery/oven-log.md` \
    **Snippet:**

      ```gitignore
      .bakery/
      !.bakery/oven-log.md
      ```

  - **Fixture:** ignore-the-log-as-a-folder \
    **Holds:** an ignore file of a line naming the folder `.bakery/drafts/` and a line naming `.bakery/oven-log.md/`, ending in a slash \
    **Snippet:**

      ```gitignore
      .bakery/drafts/
      .bakery/oven-log.md/
      ```
