**Records:**
  - **Fixture:** bold-at-line-openings \
    **Holds:** a Markdown file on a bakery holding a bold lead-in closing on a period, one closing on a question mark, one opening a list item, a field, a code span holding two asterisks either side of a word, and a fenced block holding bold in a line's middle \
    **Snippet:**

      ````markdown
      # The Bakery

      **Loaves are baked at dawn.** The ovens are lit an hour before.

      **Who shapes the loaves?** The second baker shapes them.

      - **Rye.** A dark loaf, baked on Tuesdays.

      **Oven:** Deck

      A loaf marked `**rye**` is set aside.

      ```text
      the rye is **dark**
      ```
      ````

  - **Fixture:** bold-in-a-line-middle \
    **Holds:** a Markdown file on a bakery whose paragraph holds a bold word in the middle of its line \
    **Snippet:**

      ```markdown
      # The Bakery

      The rye is **dark** and sour.
      ```

  - **Fixture:** bold-field-after-an-asterisk-marker \
    **Holds:** a Markdown file on a bakery holding a list item opened by an asterisk whose text is a key in bold closing on a colon, then a value \
    **Snippet:**

      ```markdown
      # The Bakery

      * **Oven:** Deck
      ```

  - **Fixture:** bold-opening-closing-on-a-word \
    **Holds:** a Markdown file on a bakery whose paragraph opens with bold closing on a word, the sentence running on after it \
    **Snippet:**

      ```markdown
      # The Bakery

      **Fresh bread** is sold at dawn.
      ```

  - **Fixture:** bold-prose-with-an-em-dash \
    **Holds:** a Markdown file on a bakery whose paragraph holds an em dash between two clauses \
    **Snippet:**

      ```markdown
      # The Bakery

      The loaf rests — then it is sliced.
      ```

  - **Fixture:** bold-italic-lead-in \
    **Holds:** a Markdown file on a bakery whose paragraph opens with a lead-in in three asterisks either side, closing on a period \
    **Snippet:**

      ```markdown
      # The Bakery

      ***Sourdough.*** The starter is fed each morning.
      ```

  - **Fixture:** bold-in-underscores \
    **Holds:** a Markdown file on a bakery whose paragraph holds a word between two underscores either side \
    **Snippet:**

      ```markdown
      # The Bakery

      The rye is __dark__ today.
      ```
