**Records:**
  - **Fixture:** index-of-the-loaf-card \
    **Holds:** an index of a bakery's specifications, a title and a table of two rows naming the files `loaf-card.md` and `loaf-card-form-template.md` \
    **Snippet:**

      ```markdown
      # The Bakery's Specifications

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `loaf-card.md` | The form of the day's loaf card |
      | `loaf-card-form-template.md` | A loaf card to copy and fill |
      ```

  - **Fixture:** loaf-card-form \
    **Holds:** a spec on a bakery's loaf card of two sections: Loaf Card, holding a table keyed by Part of three parts whose Heading cells give `# Loaf Card`, `## Loaves` and `## Notes` in that order; and Loaf, declaring a record type Loaf, Plural Name Loaves, of the fields Name, Weight and Crust in that order \
    **Snippet:**

      ```markdown
      # The Bakery's Cards

      ## Loaf Card

      A loaf card is laid out in these parts:

      | Part | Heading | Holds |
      |---|---|---|
      | Title | `# Loaf Card` | the day the card is for |
      | Loaves | `## Loaves` | each loaf baked that day |
      | Notes | `## Notes` | what the baker noticed |

      ## Loaf

      A loaf on the card is a record of this type:

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
      **Plural Name:** Loaves \
      **Reference Key:** Name

      | Field | Unique | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Name | yes | yes | | text | the loaf's name |
      | Weight | no | yes | | text | what the loaf weighs |
      | Crust | no | no | none | text | how dark its crust is |
      ```

  - **Fixture:** loaf-card-template-in-its-form \
    **Holds:** a template of a loaf card whose first placeholder cites `specs/loaf-card.md § Loaf Card`, laying out the headings `# Loaf Card`, `## Loaves` and `## Notes` in that order, and under Loaves one record of the fields Name, Weight and Crust in that order, each a placeholder citing `specs/loaf-card.md § Loaf` \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for (`specs/loaf-card.md § Loaf Card`)}

      ## Loaves

      **Records:**
        - **Name:** {the loaf's name (`specs/loaf-card.md § Loaf`)} \
          **Weight:** {what it weighs (`specs/loaf-card.md § Loaf`)} \
          **Crust:** {how dark its crust is (`specs/loaf-card.md § Loaf`)}

      ## Notes

      {what the baker noticed}
      ```

  - **Fixture:** loaf-card-template-citing-no-form \
    **Holds:** a template of a loaf card whose first placeholder, on line 3, cites nothing, laying out the headings `# Loaf Card`, `## Loaves` and `## Notes` \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for}

      ## Loaves

      {each loaf baked that day}

      ## Notes

      {what the baker noticed}
      ```

  - **Fixture:** loaf-card-template-of-a-rolls-heading \
    **Holds:** a template of a loaf card whose first placeholder cites `specs/loaf-card.md § Loaf Card`, laying out the headings `# Loaf Card`, `## Loaves`, `## Rolls` on line 9, and `## Notes` \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for (`specs/loaf-card.md § Loaf Card`)}

      ## Loaves

      {each loaf baked that day}

      ## Rolls

      {each roll baked that day}

      ## Notes

      {what the baker noticed}
      ```

  - **Fixture:** loaf-card-template-of-notes-first \
    **Holds:** a template of a loaf card whose first placeholder cites `specs/loaf-card.md § Loaf Card`, laying out the headings `# Loaf Card`, `## Notes`, and `## Loaves` on line 9 \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for (`specs/loaf-card.md § Loaf Card`)}

      ## Notes

      {what the baker noticed}

      ## Loaves

      {each loaf baked that day}
      ```

  - **Fixture:** loaf-card-template-of-a-shape-field \
    **Holds:** a template of a loaf card whose first placeholder cites `specs/loaf-card.md § Loaf Card`, laying out the headings `# Loaf Card`, `## Loaves` and `## Notes`, and under Loaves one record of the fields Name, Weight and, on line 10, Shape, each a placeholder citing `specs/loaf-card.md § Loaf` \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for (`specs/loaf-card.md § Loaf Card`)}

      ## Loaves

      **Records:**
        - **Name:** {the loaf's name (`specs/loaf-card.md § Loaf`)} \
          **Weight:** {what it weighs (`specs/loaf-card.md § Loaf`)} \
          **Shape:** {how it is shaped (`specs/loaf-card.md § Loaf`)}

      ## Notes

      {what the baker noticed}
      ```

  - **Fixture:** loaf-card-template-of-crust-before-weight \
    **Holds:** a template of a loaf card whose first placeholder cites `specs/loaf-card.md § Loaf Card`, laying out the headings `# Loaf Card`, `## Loaves` and `## Notes`, and under Loaves one record of the fields Name, Crust and, on line 10, Weight, each a placeholder citing `specs/loaf-card.md § Loaf` \
    **Snippet:**

      ```markdown
      # Loaf Card

      **Day:** {the day the card is for (`specs/loaf-card.md § Loaf Card`)}

      ## Loaves

      **Records:**
        - **Name:** {the loaf's name (`specs/loaf-card.md § Loaf`)} \
          **Crust:** {how dark its crust is (`specs/loaf-card.md § Loaf`)} \
          **Weight:** {what it weighs (`specs/loaf-card.md § Loaf`)}

      ## Notes

      {what the baker noticed}
      ```
