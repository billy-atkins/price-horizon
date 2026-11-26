**Records:**
  - **Fixture:** index-of-a-harbor-methodology \
    **Holds:** an index titled How the Harbor Works, a table of two rows naming the files `tides.md` and `moorings.md` \
    **Snippet:**

      ```markdown
      # How the Harbor Works

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `tides.md` | When the water rises |
      | `moorings.md` | Where a boat lies |
      ```

  - **Fixture:** harbor-tides-of-two-sections \
    **Holds:** a Markdown file titled Tides of a section Tides holding one sentence and, under it, a section Springs holding one sentence \
    **Snippet:**

      ```markdown
      # Tides

      ## Tides

      The harbor keeps a table of tides.

      ### Springs

      A spring tide rises highest.
      ```

  - **Fixture:** harbor-tides-with-neap-tides \
    **Holds:** a Markdown file titled Tides of a section Tides holding one sentence and, under it, a section Springs holding one sentence, then a section Neap Tides holding one sentence \
    **Snippet:**

      ```markdown
      # Tides

      ## Tides

      The harbor keeps a table of tides.

      ### Springs

      A spring tide rises highest.

      ## Neap Tides

      A neap tide rises least.
      ```

  - **Fixture:** harbor-moorings-section \
    **Holds:** a Markdown file titled Moorings of one section, Moorings, holding one sentence \
    **Snippet:**

      ```markdown
      # Moorings

      ## Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** harbor-audits-naming-tides \
    **Holds:** a Markdown file titled Audit the Harbor whose section The audits holds a table with the header Audit and Enforces and one row, its Enforces cell citing `specs/methodology/tides.md § Tides` \
    **Snippet:**

      ```markdown
      # Audit the Harbor

      ## The audits

      | Audit | Enforces |
      |---|---|
      | Tide table | `specs/methodology/tides.md § Tides` |
      ```

  - **Fixture:** harbor-audits-without-enforces \
    **Holds:** a Markdown file titled Audit the Harbor whose section The audits holds a table with the header Audit and Reads and one row, its Reads cell citing `specs/methodology/tides.md § Tides` \
    **Snippet:**

      ```markdown
      # Audit the Harbor

      ## The audits

      | Audit | Reads |
      |---|---|
      | Tide table | `specs/methodology/tides.md § Tides` |
      ```

  - **Fixture:** harbor-skipped-steps \
    **Holds:** a Markdown file titled Rules and Skills whose section Rules and Skills holds a section Skipped Steps of one record, a boat left unmoored, its Sections citing `specs/methodology/moorings.md § Moorings` \
    **Snippet:**

      ```markdown
      # Rules and Skills

      ## Rules and Skills

      ### Skipped Steps

      **Records:**
        - **Failure:** a boat left unmoored \
          **Sections:**
            - `specs/methodology/moorings.md § Moorings`

          **Rule:** `specs/methodology/moorings.md § Moorings` \
          **Leaves:** a boat adrift by its mooring \
          **Caught By:**
            - the user
      ```

  - **Fixture:** registry-of-a-mooring-skill \
    **Holds:** a Markdown file titled Registered Skills, a table with the header Skill and Purpose and one row naming the skill `moor-a-boat` \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Purpose |
      |---|---|
      | `moor-a-boat` | Moors a boat |
      ```

  - **Fixture:** mooring-skill \
    **Holds:** a skill file opening with front matter naming `moor-a-boat`, then a title and a Workflow section of one step citing `specs/methodology/moorings.md § Moorings` \
    **Snippet:**

      ```markdown
      ---
      name: moor-a-boat
      description: Moor a boat. Use when a boat comes in.
      ---

      # Moor a Boat

      ## Workflow

      **Tie the line.** Tie it as `specs/methodology/moorings.md § Moorings` has it.
      ```

  - **Fixture:** harbor-code-checks \
    **Holds:** a Markdown file titled Verify the Harbor's Code whose section The checks holds a table with the header Check and Enforces and one row, its Enforces cell citing `specs/methodology/moorings.md § Moorings` \
    **Snippet:**

      ```markdown
      # Verify the Harbor's Code

      ## The checks

      | Check | Enforces |
      |---|---|
      | Moorings laid | `specs/methodology/moorings.md § Moorings` |
      ```
