**Records:**
  - **Fixture:** headings-titled-plainly \
    **Holds:** a Markdown file on a harbor of a title and three sections, one of them holding two sections of its own, each heading a plain title unlike its siblings' \
    **Snippet:**

      ```markdown
      # The Harbor

      ## Moorings

      Each boat takes one mooring.

      ### Swinging Moorings

      A swinging mooring is laid in deep water.

      ### Pontoon Berths

      A berth on a pontoon is let by the season.

      ## Tides

      The harbor dries at low water.

      ## Fees

      A visiting boat pays by the night.
      ```

  - **Fixture:** heading-numbered \
    **Holds:** a Markdown file on a harbor whose second section's heading opens with a number and a period \
    **Snippet:**

      ```markdown
      # The Harbor

      ## Moorings

      Each boat takes one mooring.

      ## 2. Tides

      The harbor dries at low water.
      ```

  - **Fixture:** heading-holding-a-section-sign \
    **Holds:** a Markdown file on a harbor whose second section's heading holds a section sign between two words \
    **Snippet:**

      ```markdown
      # The Harbor

      ## Moorings

      Each boat takes one mooring.

      ## Tides § Springs

      The harbor dries at low water.
      ```

  - **Fixture:** heading-holding-a-bracket \
    **Holds:** a Markdown file on a harbor whose second section's heading ends in a word in square brackets \
    **Snippet:**

      ```markdown
      # The Harbor

      ## Moorings

      Each boat takes one mooring.

      ## Tides [Springs]

      The harbor dries at low water.
      ```

  - **Fixture:** headings-twice-among-siblings \
    **Holds:** a Markdown file on a harbor of two sections both headed Moorings \
    **Snippet:**

      ```markdown
      # The Harbor

      ## Moorings

      Each boat takes one mooring.

      ## Moorings

      A mooring is laid each spring.
      ```
