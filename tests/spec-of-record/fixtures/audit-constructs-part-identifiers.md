**Records:**
  - **Fixture:** watering-need-named-and-cited \
    **Holds:** a file titled Watering of two sections: Watering Need, declaring a Decision Table with a Conditions field naming soil and season, an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", and a table headed Name, soil, season and water of four rows named Wet Clay, Cold Clay, Dry Sand and Cold Sand; and Hose Times, a sentence citing `§ Watering Need [Name: Dry Sand]` \
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

      | Name | soil | season | water |
      |---|---|---|---|
      | Wet Clay | clay | summer | light |
      | Cold Clay | clay | winter | little |
      | Dry Sand | sand | summer | heavy |
      | Cold Sand | sand | winter | light |

      ## Hose Times

      A bed of sand in summer is watered at dawn, as `§ Watering Need [Name: Dry Sand]` has it.
      ```

  - **Fixture:** watering-need-named-uncited \
    **Holds:** a file titled Watering of one section, Watering Need, declaring on line 7 a Decision Table with a Conditions field naming soil and season, an Input Values list giving soil "clay" and "sand" and season "summer" and "winter", and a table headed Name, soil, season and water of four rows named Wet Clay, Cold Clay, Dry Sand and Cold Sand; no text cites a row of it \
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

      | Name | soil | season | water |
      |---|---|---|---|
      | Wet Clay | clay | summer | light |
      | Cold Clay | clay | winter | little |
      | Dry Sand | sand | summer | heavy |
      | Cold Sand | sand | winter | light |
      ```

  - **Fixture:** watering-need-name-second \
    **Holds:** a file titled Watering of two sections: Watering Need, declaring a Decision Table with a Conditions field naming soil and season, an Input Values list, and, on line 13, a table headed soil, Name, season and water of four rows; and Hose Times, a sentence citing `§ Watering Need [Name: Dry Sand]` \
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

      | soil | Name | season | water |
      |---|---|---|---|
      | clay | Wet Clay | summer | light |
      | clay | Cold Clay | winter | little |
      | sand | Dry Sand | summer | heavy |
      | sand | Cold Sand | winter | light |

      ## Hose Times

      A bed of sand in summer is watered at dawn, as `§ Watering Need [Name: Dry Sand]` has it.
      ```

  - **Fixture:** watering-need-two-rows-named-cold \
    **Holds:** a file titled Watering of two sections: Watering Need, declaring a Decision Table with a Conditions field naming soil and season, an Input Values list, and, on line 13, a table headed Name, soil, season and water of four rows named Wet Clay, Cold, Dry Sand and Cold; and Hose Times, a sentence citing `§ Watering Need [Name: Dry Sand]` \
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

      | Name | soil | season | water |
      |---|---|---|---|
      | Wet Clay | clay | summer | light |
      | Cold | clay | winter | little |
      | Dry Sand | sand | summer | heavy |
      | Cold | sand | winter | light |

      ## Hose Times

      A bed of sand in summer is watered at dawn, as `§ Watering Need [Name: Dry Sand]` has it.
      ```
