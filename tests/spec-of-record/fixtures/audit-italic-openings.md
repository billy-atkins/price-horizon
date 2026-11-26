**Records:**
  - **Fixture:** italic-inside-lines \
    **Holds:** a Markdown file on a garden holding italic in the middle of a line, a list item opened by an asterisk marker, a line opening with a code span holding an asterisk, and a fenced block holding a line opening with italic \
    **Snippet:**

      ````markdown
      # The Garden

      The roses are *pruned* in March.

      * Tulips are lifted in June.

      `*.txt` notes hang in the shed.

      ```text
      *Mint* spreads fast
      ```
      ````

  - **Fixture:** italic-opening-a-paragraph \
    **Holds:** a Markdown file on a garden whose paragraph opens with an italic word \
    **Snippet:**

      ```markdown
      # The Garden

      *Mint* spreads fast in a damp bed.
      ```

  - **Fixture:** italic-opening-a-list-item \
    **Holds:** a Markdown file on a garden whose list item opens with an italic word after a hyphen marker \
    **Snippet:**

      ```markdown
      # The Garden

      - *Mint* spreads fast in a damp bed.
      ```

  - **Fixture:** italic-opening-a-quote \
    **Holds:** a Markdown file on a garden whose quoted line opens with an italic word after the quote marker \
    **Snippet:**

      ```markdown
      # The Garden

      > *Mint* spreads fast in a damp bed.
      ```
