**Records:**
  - **Fixture:** harbor-tides \
    **Holds:** a Markdown file titled Tides of one section, Springs, holding one sentence \
    **Snippet:**

      ```markdown
      # Tides

      ## Springs

      A spring tide rises highest.
      ```

  - **Fixture:** harbor-readme-citing-by-link \
    **Holds:** a Markdown file titled The Harbor whose third line cites `docs/tides.md § Springs` in a code span carrying the link `/docs/tides.md#springs` \
    **Snippet:**

      ```markdown
      # The Harbor

      A boat leaves at high water ([`docs/tides.md § Springs`](/docs/tides.md#springs)).
      ```

  - **Fixture:** harbor-readme-citing-bare \
    **Holds:** a Markdown file titled The Harbor whose third line cites `docs/tides.md § Springs` in a code span carrying no link \
    **Snippet:**

      ```markdown
      # The Harbor

      A boat leaves at high water (`docs/tides.md § Springs`).
      ```

  - **Fixture:** harbor-readme-citing-by-a-stale-link \
    **Holds:** a Markdown file titled The Harbor whose third line cites `docs/tides.md § Springs` in a code span carrying the link `/docs/tides.md#neaps` \
    **Snippet:**

      ```markdown
      # The Harbor

      A boat leaves at high water ([`docs/tides.md § Springs`](/docs/tides.md#neaps)).
      ```
