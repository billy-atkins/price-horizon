**Records:**
  - **Fixture:** registry-of-a-bread-skill \
    **Holds:** a Markdown file titled Registered Skills, a table with the header Skill and Purpose and one row naming the skill `bake-bread` \
    **Snippet:**

      ```markdown
      # Registered Skills

      | Skill | Purpose |
      |---|---|
      | `bake-bread` | Bakes a loaf |
      ```

  - **Fixture:** bread-skill-in-its-form \
    **Holds:** a skill file opening with front matter whose name is `bake-bread` and whose description is one sentence, then a title and a Workflow section of one step \
    **Snippet:**

      ```markdown
      ---
      name: bake-bread
      description: Bake a loaf of bread. Use when the bakery needs a loaf.
      ---

      # Bake Bread

      ## Workflow

      **Knead the dough.** Knead it for ten minutes.
      ```

  - **Fixture:** bread-skill-named-otherwise \
    **Holds:** a skill file opening with front matter whose name is `bake-cake` and whose description is one sentence, then a title and a Workflow section of one step \
    **Snippet:**

      ```markdown
      ---
      name: bake-cake
      description: Bake a loaf of bread. Use when the bakery needs a loaf.
      ---

      # Bake Bread

      ## Workflow

      **Knead the dough.** Knead it for ten minutes.
      ```

  - **Fixture:** bread-skill-undescribed \
    **Holds:** a skill file opening with front matter whose name is `bake-bread` and which holds no description, then a title and a Workflow section of one step \
    **Snippet:**

      ```markdown
      ---
      name: bake-bread
      ---

      # Bake Bread

      ## Workflow

      **Knead the dough.** Knead it for ten minutes.
      ```

  - **Fixture:** bread-skill-without-a-workflow \
    **Holds:** a skill file opening with front matter whose name is `bake-bread` and whose description is one sentence, then a title and a section titled Steps of one step \
    **Snippet:**

      ```markdown
      ---
      name: bake-bread
      description: Bake a loaf of bread. Use when the bakery needs a loaf.
      ---

      # Bake Bread

      ## Steps

      **Knead the dough.** Knead it for ten minutes.
      ```

  - **Fixture:** bread-skill-without-front-matter \
    **Holds:** a skill file of a title and a Workflow section of one step, with no front matter \
    **Snippet:**

      ```markdown
      # Bake Bread

      ## Workflow

      **Knead the dough.** Knead it for ten minutes.
      ```

  - **Fixture:** bread-script \
    **Holds:** a Python script of one function printing that the loaf is baked \
    **Snippet:**

      ```python
      def main():
          print("the loaf is baked")
      ```
