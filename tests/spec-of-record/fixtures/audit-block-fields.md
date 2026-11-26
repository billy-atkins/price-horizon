**Records:**
  - **Fixture:** block-fields-in-form \
    **Holds:** a Markdown file on a bakery holding a block of fields with a list beneath one key and a block nested beneath another key's text, each line a key directly follows ending in one space and a backslash, and a fenced Markdown block holding a block of two fields written the same way \
    **Snippet:**

      ````markdown
      # The Bakery

      **Name:** Rye Loaf \
      **Oven:** Deck \
      **Fillings:**
        - caraway
        - sunflower seeds

      **Starter:** a sour culture kept in the cool room

        **Fed:** each morning \
        **Flour:** rye

      A card on the counter reads:

      ```markdown
      **Loaf:** Spelt \
      **Price:** three coins
      ```
      ````

  - **Fixture:** block-field-line-without-backslash \
    **Holds:** a Markdown file on a bakery holding a block of two fields whose first line ends with no backslash \
    **Snippet:**

      ```markdown
      # The Bakery

      **Name:** Rye Loaf
      **Oven:** Deck
      ```

  - **Fixture:** block-field-line-with-two-spaces-before-backslash \
    **Holds:** a Markdown file on a bakery holding a block of two fields whose first line ends with two spaces and a backslash \
    **Snippet:**

      ```markdown
      # The Bakery

      **Name:** Rye Loaf  \
      **Oven:** Deck
      ```

  - **Fixture:** block-field-last-line-with-backslash \
    **Holds:** a Markdown file on a bakery holding a block of two fields whose last line ends with a space and a backslash, a paragraph of prose following after a blank line \
    **Snippet:**

      ```markdown
      # The Bakery

      **Name:** Rye Loaf \
      **Oven:** Deck \

      A loaf is cooled before it is sliced.
      ```

  - **Fixture:** block-field-list-indented-four-spaces \
    **Holds:** a Markdown file on a bakery holding a field whose list of two items stands four spaces beyond its key \
    **Snippet:**

      ```markdown
      # The Bakery

      **Name:** Rye Loaf \
      **Fillings:**
          - caraway
          - sunflower seeds
      ```

  - **Fixture:** block-field-nested-line-without-backslash \
    **Holds:** a Markdown file on a bakery holding a block nested beneath a field's text whose first line ends with no backslash before the next key \
    **Snippet:**

      ```markdown
      # The Bakery

      **Starter:** a sour culture kept in the cool room

        **Fed:** each morning
        **Flour:** rye
      ```

  - **Fixture:** block-field-in-markdown-block-without-backslash \
    **Holds:** a Markdown file on a bakery holding a fenced Markdown block whose block of two fields has a first line ending with no backslash \
    **Snippet:**

      ````markdown
      # The Bakery

      A card on the counter reads:

      ```markdown
      **Loaf:** Spelt
      **Price:** three coins
      ```
      ````
