**Records:**
  - **Fixture:** bakery-ovens \
    **Holds:** a Markdown file on a bakery's ovens of a title and two sections, Proving, of one sentence, and Open Questions, holding one record named Oven Count \
    **Snippet:**

      ```markdown
      # Ovens

      ## Proving

      Dough proves overnight.

      ## Open Questions

      **Records:**
        - **Name:** Oven Count \
          **Open Question:** Does the bakery need a second oven? \
          **Provisional Answer:** The bakery bakes in one oven. \
          **Impacts:** the proving of the dough, `§ Proving`
      ```

  - **Fixture:** bakery-citing-its-ovens \
    **Holds:** a Markdown file on a bakery of a title and one sentence citing the section Proving of `docs/ovens.md` by its path from the root, and the record of that file's Open Questions named Oven Count \
    **Snippet:**

      ```markdown
      # The Bakery

      Bread is proved as `docs/ovens.md § Proving` has it, in the one oven `docs/ovens.md § Open Questions [Name: Oven Count]` holds to.
      ```

  - **Fixture:** bakery-citing-a-flour-file \
    **Holds:** a Markdown file on a bakery whose one sentence cites a section of `docs/flour.md` \
    **Snippet:**

      ```markdown
      # The Bakery

      Flour is kept dry, as `docs/flour.md § Storage` has it.
      ```

  - **Fixture:** bakery-citing-ovens-from-its-folder \
    **Holds:** a Markdown file on a bakery whose one sentence cites the section Proving of `ovens.md`, a path from the file's own folder \
    **Snippet:**

      ```markdown
      # The Bakery

      Bread is proved as `ovens.md § Proving` has it.
      ```

  - **Fixture:** bakery-citing-a-baking-section \
    **Holds:** a Markdown file on a bakery whose one sentence cites the section Baking of `docs/ovens.md` \
    **Snippet:**

      ```markdown
      # The Bakery

      Bread is baked as `docs/ovens.md § Baking` has it.
      ```

  - **Fixture:** bakery-citing-a-flour-stock-record \
    **Holds:** a Markdown file on a bakery whose one sentence cites the record named Flour Stock of the Open Questions of `docs/ovens.md` \
    **Snippet:**

      ```markdown
      # The Bakery

      Flour is bought weekly, as `docs/ovens.md § Open Questions [Name: Flour Stock]` holds.
      ```

  - **Fixture:** index-of-a-bakery-guide \
    **Holds:** an index of the specifications titled The Bakery Guide, of one section, Rooms, holding a table of one row naming a file `ovens.md` \
    **Snippet:**

      ```markdown
      # The Bakery Guide

      ## Rooms

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `ovens.md` | Where the bread is baked |
      ```

  - **Fixture:** bakery-citing-its-guide \
    **Holds:** a Markdown file on a bakery whose one sentence cites the section Rooms of `specs/index.md` \
    **Snippet:**

      ```markdown
      # The Bakery

      The rooms are listed in `specs/index.md § Rooms`.
      ```

  - **Fixture:** registry-of-two-skills \
    **Holds:** a registry of skills titled Registered Skills, a table of two rows naming the skills `bake-bread` and `read-tides` in backticks \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Does |
      |---|---|
      | `bake-bread` | Bakes the day's bread |
      | `read-tides` | Reads the day's tides |
      ```

  - **Fixture:** bake-bread-citing-its-reference \
    **Holds:** a skill's file titled Bake Bread whose one sentence cites the section Shaping of `.ai/skills/bake-bread/references/proving.md` \
    **Snippet:**

      ```markdown
      # Bake Bread

      Shape the dough as `.ai/skills/bake-bread/references/proving.md § Shaping` has it.
      ```

  - **Fixture:** bake-bread-citing-read-tides \
    **Holds:** a skill's file titled Bake Bread whose one sentence cites the section Low Water of `.ai/skills/read-tides/SKILL.md` \
    **Snippet:**

      ```markdown
      # Bake Bread

      Bake before the tide turns, as `.ai/skills/read-tides/SKILL.md § Low Water` has it.
      ```

  - **Fixture:** bake-bread-proving-reference \
    **Holds:** a reference file on proving dough of a title and one section, Shaping, of one sentence \
    **Snippet:**

      ```markdown
      # Proving

      ## Shaping

      The dough is shaped before its last prove.
      ```

  - **Fixture:** read-tides-skill \
    **Holds:** a skill's file titled Read Tides of one section, Low Water, of one sentence \
    **Snippet:**

      ```markdown
      # Read Tides

      ## Low Water

      Read the hour of low water from the day's table.
      ```
