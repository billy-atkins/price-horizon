**Records:**
  - **Fixture:** watering-need \
    **Holds:** a file titled Watering of one section, Watering Need, opening with a sentence and declaring a Decision Table by the citation of its definition, with a Conditions field naming soil and season, an Input Values list beneath its key giving soil "clay" and "sand" and season "summer" and "winter", and a table headed soil, season and water of four rows, one for each soil in each season \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | winter | little |
      | sand | summer | heavy |
      | sand | winter | light |
      ```

  - **Fixture:** watering-need-two-rows-for-clay-in-summer \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with no Hit Policy field, a Conditions field naming soil and season, and an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", whose table's second row, on line 16, tests clay in "summer", "winter" beside a first row testing clay in summer \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | "summer", "winter" | little |
      | sand | summer | heavy |
      | sand | winter | light |
      ```

  - **Fixture:** watering-need-without-sand-in-winter \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming soil and season and an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", whose table, headed on line 13, holds three rows: clay in summer, clay in winter and sand in summer \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | winter | little |
      | sand | summer | heavy |
      ```

  - **Fixture:** watering-need-hit-policy-highest \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table whose Hit Policy field, on line 8, holds Highest, before a Conditions field naming soil and season, an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", and a table of four rows, one for each soil in each season \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** Highest \
      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | winter | little |
      | sand | summer | heavy |
      | sand | winter | light |
      ```

  - **Fixture:** watering-need-a-loam-row \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming soil and season and an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", whose table's last row, on line 18, tests loam in winter \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | winter | little |
      | sand | summer | heavy |
      | loam | winter | light |
      ```

  - **Fixture:** watering-need-reads-rainfall-bare \
    **Holds:** a file titled Watering of one section, Watering Need, declaring, on line 7, a Decision Table whose Reads list beneath its key holds one item, rainfall, with no colon and no citation, then a Conditions field naming soil and season, an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", and a table of four rows, one for each soil in each season \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil and the season.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Reads:**
        - rainfall

      **Conditions:** soil, season \
      **Input Values:**
        - soil: "clay", "sand"
        - season: "summer", "winter"

      | soil | season | water |
      |---|---|---|
      | clay | summer | light |
      | clay | winter | little |
      | sand | summer | heavy |
      | sand | winter | light |
      ```

  - **Fixture:** watering-by-questions \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming two questions, dry soil? and summer?, and a table headed dry soil?, summer? and water of four rows, one for each pair of true and false \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by whether its soil is dry and whether it is summer.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** dry soil?, summer?

      | dry soil? | summer? | water |
      |---|---|---|
      | true | true | heavy |
      | true | false | light |
      | false | true | light |
      | false | false | little |
      ```

  - **Fixture:** watering-need-input-values-on-the-key-line \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming soil and, on line 9, an Input Values field whose one item, soil "clay" and "sand", stands on its key's line, and a table headed soil and water of two rows, clay and sand \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil \
      **Input Values:** soil: "clay", "sand"

      | soil | water |
      |---|---|
      | clay | light |
      | sand | heavy |
      ```

  - **Fixture:** watering-need-default-output-one-item \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming soil, an Input Values list giving soil "clay", "sand" and "loam", a Default Output field on line 12 with one item beneath its key, water: light, and a table headed soil and water of two rows, clay and sand \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil \
      **Input Values:**
        - soil: "clay", "sand", "loam"

      **Default Output:**
        - water: light

      | soil | water |
      |---|---|
      | clay | little |
      | sand | heavy |
      ```

  - **Fixture:** watering-need-default-output-on-the-key-line \
    **Holds:** a file titled Watering of one section, Watering Need, declaring a Decision Table with a Conditions field naming soil, an Input Values list giving soil "clay", "sand" and "loam", a Default Output field holding light on its key's line, and a table headed soil and water of two rows, clay and sand \
    **Snippet:**

      ```markdown
      # Watering

      ## Watering Need

      How much water a garden bed is given, by its soil.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Conditions:** soil \
      **Input Values:**
        - soil: "clay", "sand", "loam"

      **Default Output:** light

      | soil | water |
      |---|---|
      | clay | little |
      | sand | heavy |
      ```
