**Records:**
  - **Fixture:** style-specs-index \
    **Holds:** an index of the specifications titled The Bakery, a table of one row naming the folder `methodology/` \
    **Snippet:**

      ```markdown
      # The Bakery

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `methodology/` | How the bakery's specs are written |
      ```

  - **Fixture:** style-methodology-index \
    **Holds:** an index titled Writing the Specs, a table of one row naming the folder `spec-style/` \
    **Snippet:**

      ```markdown
      # Writing the Specs

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `spec-style/` | How a spec is laid out |
      ```

  - **Fixture:** style-folder-index \
    **Holds:** an index titled Spec Style, a table of one row naming a file `markdown.md` \
    **Snippet:**

      ```markdown
      # Spec Style

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `markdown.md` | Where a blank line stands |
      ```

  - **Fixture:** blank-line-table-naming-each-element \
    **Holds:** a section titled Blank Lines holding a Decision Table of where a blank line stands, its conditions The element above, The element below, Ends a list item? and Nested beneath the field above?, its Input Values naming front matter, a heading, a paragraph, a field, a record, a list item, a table, a code block and a thematic break, and one row giving true for every case \
    **Snippet:**

      ```markdown
      ## Blank Lines

      A blank line separates groups that differ.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** First \
      **Conditions:** The element above, The element below, Ends a list item?, Nested beneath the field above? \
      **Annotations:** Why \
      **Input Values:**
        - The element above: "front matter", "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break"
        - The element below: "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break"

      | The element above | The element below | Ends a list item? | Nested beneath the field above? | A blank line between? | Why |
      |---|---|---|---|---|---|
      | - | - | - | - | true | groups that differ |
      ```

  - **Fixture:** blank-line-table-naming-a-quote \
    **Holds:** the same section titled Blank Lines and Decision Table, its Input Values naming a quote among the elements below as well \
    **Snippet:**

      ```markdown
      ## Blank Lines

      A blank line separates groups that differ.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** First \
      **Conditions:** The element above, The element below, Ends a list item?, Nested beneath the field above? \
      **Annotations:** Why \
      **Input Values:**
        - The element above: "front matter", "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break"
        - The element below: "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break", "a quote"

      | The element above | The element below | Ends a list item? | Nested beneath the field above? | A blank line between? | Why |
      |---|---|---|---|---|---|
      | - | - | - | - | true | groups that differ |
      ```
