**Records:**
  - **Fixture:** bed-waterings-held-as-data \
    **Holds:** a file titled Watering of two sections: Facts, a Records list of one fact, bed waterings, of Type list<context<soil: string, season: string, water: string>>; and Watering Need, declaring a Decision Table on line 14 whose Held In list beneath its key holds one item, bed waterings: `§ Facts [Name: bed waterings]`, with a Conditions field naming soil and season, an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", and a table headed soil, season and water of four rows \
    **Snippet:**

      ```markdown
      # Watering

      ## Facts

      **Records:**
        - **Name:** bed waterings \
          **Type:** list<context<soil: string, season: string, water: string>> \
          **Means:** the watering each kind of bed is given, as the gardeners set it

      ## Watering Need

      How much water a garden bed is given, the gardeners setting each row.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Held In:**
        - bed waterings: `§ Facts [Name: bed waterings]`

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

  - **Fixture:** bed-waterings-held-in-an-undeclared-fact \
    **Holds:** a file titled Watering of two sections: Facts, a Records list of one fact, bed waterings, of Type list<context<soil: string, season: string, water: string>>; and Watering Need, declaring a Decision Table on line 14 whose Held In list holds one item, bed feeds: `§ Facts [Name: bed feeds]`, with a Conditions field naming soil and season, an Input Values list, and a table headed soil, season and water of four rows \
    **Snippet:**

      ```markdown
      # Watering

      ## Facts

      **Records:**
        - **Name:** bed waterings \
          **Type:** list<context<soil: string, season: string, water: string>> \
          **Means:** the watering each kind of bed is given, as the gardeners set it

      ## Watering Need

      How much water a garden bed is given, the gardeners setting each row.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Held In:**
        - bed feeds: `§ Facts [Name: bed feeds]`

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

  - **Fixture:** bed-waterings-of-type-string \
    **Holds:** a file titled Watering of two sections: Facts, a Records list of one fact, bed waterings, of Type string; and Watering Need, declaring a Decision Table on line 14 whose Held In list holds one item, bed waterings: `§ Facts [Name: bed waterings]`, with a Conditions field naming soil and season, an Input Values list, and a table headed soil, season and water of four rows \
    **Snippet:**

      ```markdown
      # Watering

      ## Facts

      **Records:**
        - **Name:** bed waterings \
          **Type:** string \
          **Means:** the watering each kind of bed is given, as the gardeners set it

      ## Watering Need

      How much water a garden bed is given, the gardeners setting each row.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Held In:**
        - bed waterings: `§ Facts [Name: bed waterings]`

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

  - **Fixture:** bed-waterings-without-a-season \
    **Holds:** a file titled Watering of two sections: Facts, a Records list of one fact, bed waterings, of Type list<context<soil: string, water: string>>; and Watering Need, declaring a Decision Table on line 14 whose Held In list holds one item, bed waterings: `§ Facts [Name: bed waterings]`, with a Conditions field naming soil and season, an Input Values list, and a table headed soil, season and water of four rows \
    **Snippet:**

      ```markdown
      # Watering

      ## Facts

      **Records:**
        - **Name:** bed waterings \
          **Type:** list<context<soil: string, water: string>> \
          **Means:** the watering each kind of bed is given, as the gardeners set it

      ## Watering Need

      How much water a garden bed is given, the gardeners setting each row.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Held In:**
        - bed waterings: `§ Facts [Name: bed waterings]`

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

  - **Fixture:** bed-waterings-held-twice \
    **Holds:** a file titled Watering of two sections: Facts, a Records list of one fact, bed waterings, of Type list<context<soil: string, season: string, water: string>>; and Watering Need, declaring a Decision Table on line 14 whose Held In list holds two items, each bed waterings: `§ Facts [Name: bed waterings]`, with a Conditions field naming soil and season, an Input Values list, and a table headed soil, season and water of four rows \
    **Snippet:**

      ```markdown
      # Watering

      ## Facts

      **Records:**
        - **Name:** bed waterings \
          **Type:** list<context<soil: string, season: string, water: string>> \
          **Means:** the watering each kind of bed is given, as the gardeners set it

      ## Watering Need

      How much water a garden bed is given, the gardeners setting each row.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Held In:**
        - bed waterings: `§ Facts [Name: bed waterings]`
        - bed waterings: `§ Facts [Name: bed waterings]`

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
