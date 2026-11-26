**Records:**
  - **Fixture:** beds-holding-plantings \
    **Holds:** a file titled Beds of two sections, each declaring a record type: Planting, of Plural Name Plantings, keyed by Crop, a table of record fields of one row, Crop; and Bed, of Plural Name Beds, keyed by Bed, a table of record fields of two rows, Bed, of Values text, and Plantings, of Values a list of `§ Planting` \
    **Snippet:**

      ```markdown
      # Beds

      ## Planting

      A crop set in a bed.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
      **Plural Name:** Plantings \
      **Reference Key:** Crop

      | Field | Unique | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Crop | yes | yes | | text | what is grown |

      ## Bed

      A bed of the garden.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
      **Plural Name:** Beds \
      **Reference Key:** Bed

      | Field | Unique | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Bed | yes | yes | | text | the bed's name |
      | Plantings | no | no | none | a list of `§ Planting` | what grows in it |
      ```

  - **Fixture:** beds-holding-plantings-in-words \
    **Holds:** a file titled Beds of two sections, each declaring a record type: Planting, of Plural Name Plantings, keyed by Crop, a table of record fields of one row, Crop; and Bed, of Plural Name Beds, keyed by Bed, a table of record fields of two rows, Bed, of Values text, and, on line 26, Plantings, of Values a list of plantings, with no citation \
    **Snippet:**

      ```markdown
      # Beds

      ## Planting

      A crop set in a bed.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
      **Plural Name:** Plantings \
      **Reference Key:** Crop

      | Field | Unique | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Crop | yes | yes | | text | what is grown |

      ## Bed

      A bed of the garden.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
      **Plural Name:** Beds \
      **Reference Key:** Bed

      | Field | Unique | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Bed | yes | yes | | text | the bed's name |
      | Plantings | no | no | none | a list of plantings | what grows in it |
      ```
