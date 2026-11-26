**Records:**
  - **Fixture:** fixture-file-holding-text-beside-its-fixture \
    **Holds:** a fixture file holding one fixture, quay-line, whose snippet is one Markdown sentence naming the north quay, and after it, on its tenth line, a line of prose that is no part of a fixture \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```

      A line written beside the fixtures.
      ````

  - **Fixture:** fixture-file-whose-fixture-lacks-its-holds \
    **Holds:** a fixture file of one fixture, quay-line, opened on its second line, holding a Snippet and no Holds \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** quay-line \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** fixture-file-whose-fixture-lacks-its-snippet \
    **Holds:** a fixture file of one fixture, quay-line, opened on its second line, holding a Holds and no Snippet \
    **Snippet:**

      ```markdown
      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
      ```

  - **Fixture:** fixture-file-whose-block-names-no-language \
    **Holds:** a fixture file of one fixture, quay-line, whose snippet's fenced block, opening on the file's sixth line, names no language \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** fixture-file-whose-key-is-not-hyphened-words \
    **Holds:** a fixture file of one fixture whose key is Quay Line, two capitalised words apart, whose snippet is one Markdown sentence naming the north quay \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** Quay Line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** fixture-file-not-opening-with-its-records \
    **Holds:** a fixture file opening with a title, Fixtures, above the Records field of one fixture, quay-line \
    **Snippet:**

      ````markdown
      # Fixtures

      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** fixture-file-of-two-fixtures \
    **Holds:** a fixture file holding two fixtures, quay-line and harbor-line, each a Markdown sentence naming the north quay \
    **Snippet:**

      ````markdown
      **Records:**
        - **Fixture:** quay-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```

        - **Fixture:** harbor-line \
          **Holds:** one sentence naming the quay the ferry leaves from \
          **Snippet:**

            ```markdown
            The ferry leaves from the north quay.
            ```
      ````

  - **Fixture:** index-listing-two-files \
    **Holds:** the index of a fixtures folder, a title and a table listing two files with their descriptions, guide.md and harbor.md \
    **Snippet:**

      ```markdown
      # The Kept Tests' Fixtures

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `guide.md` | One sentence naming the quay a ferry leaves from |
      | `harbor.md` | One sentence naming a harbor |
      ```

  - **Fixture:** bread-skill-of-a-table-of-checks \
    **Holds:** the file of a skill baking bread whose section Checks holds a table headed Check and Enforces of one row, a check of shaping enforcing the section Shaping of `specs/methodology/loaves.md` \
    **Snippet:**

      ```markdown
      # Bake Bread

      ## Checks

      | Check | Enforces |
      |---|---|
      | Shaped by hand | `specs/methodology/loaves.md § Shaping` |
      ```
