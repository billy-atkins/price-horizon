**Records:**
  - **Fixture:** registry-of-one-skill \
    **Holds:** a registry of a bakery's skills, a title and a table of one row naming the skill `bake-bread` in backticks \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Does |
      |---|---|
      | `bake-bread` | Bakes the day's loaves |
      ```

  - **Fixture:** registry-of-two-skills \
    **Holds:** a registry of a bakery's skills, a title and a table of two rows naming the skills `bake-bread` and `ice-cakes` in backticks \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Does |
      |---|---|
      | `bake-bread` | Bakes the day's loaves |
      | `ice-cakes` | Ices the day's cakes |
      ```

  - **Fixture:** registry-of-no-skill \
    **Holds:** a registry of a bakery's skills, a title and a table's header and divider with no row beneath them \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Does |
      |---|---|
      ```

  - **Fixture:** registry-of-a-row-unnamed \
    **Holds:** a registry of a bakery's skills, a title and a table of two rows, the first, on line 5, naming the skill `bake-bread` in backticks and the second, on line 6, naming ice cakes in plain words \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Does |
      |---|---|
      | `bake-bread` | Bakes the day's loaves |
      | ice cakes | Ices the day's cakes |
      ```

  - **Fixture:** bread-skill-file \
    **Holds:** a skill's own file for baking bread, a title and one sentence \
    **Snippet:**

      ```markdown
      # Bake Bread

      Bakes the day's loaves before the shop opens.
      ```
