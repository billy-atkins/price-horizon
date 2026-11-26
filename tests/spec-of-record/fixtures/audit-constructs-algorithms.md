**Records:**
  - **Fixture:** watering-ration \
    **Holds:** a file on a garden's watering: an Algorithm taking the bed's area and the week's rain and giving the water to pour, rounded half up, its one comparison going to an End or on to a last step, and a Facts section declaring the area, the rain and the water \
    **Snippet:**

      ```markdown
      ## Watering Ration

      How much water a garden bed takes in a week, less what the rain gave it.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - bed area
        - rain

      **Output:**
        - water

      **Runs When:** the gardener plans the week's watering \
      **Rounding Mode:** half up

      | Step | Action |
      |---|---|
      | 1 | Set water to 0 |
      | 2 | If rain >= bed area * 25; otherwise, Go to step 4 |
      | 3 | End |
      | 4 | Set water to bed area * 25 - rain |
      | 5 | End |

      ## Facts

      **Records:**
        - **Name:** bed area \
          **Type:** number \
          **Unit:** square metre \
          **Means:** the area of the bed

        - **Name:** rain \
          **Type:** number \
          **Unit:** litre \
          **Means:** the rain the bed took this week

        - **Name:** water \
          **Type:** number \
          **Unit:** litre \
          **Means:** the water to pour on the bed this week
      ```

  - **Fixture:** watering-ration-never-set \
    **Holds:** a file on a garden's watering: an Algorithm whose Output names the water and whose one step before its End sets the rain, and a Facts section declaring the rain and the water \
    **Snippet:**

      ```markdown
      ## Watering Ration

      How much water a garden bed takes in a week.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:** none \
      **Output:**
        - water

      **Runs When:** the gardener plans the week's watering

      | Step | Action |
      |---|---|
      | 1 | Set rain to 0 |
      | 2 | End |

      ## Facts

      **Records:**
        - **Name:** rain \
          **Type:** number \
          **Means:** the rain the bed took this week

        - **Name:** water \
          **Type:** number \
          **Means:** the water to pour on the bed this week
      ```

  - **Fixture:** watering-ration-jumping-past-its-end \
    **Holds:** a file on a garden's watering: an Algorithm of three steps whose comparison goes to step 7, and a Facts section declaring the rain and the water \
    **Snippet:**

      ```markdown
      ## Watering Ration

      How much water a garden bed takes in a week.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - rain

      **Output:**
        - water

      **Runs When:** the gardener plans the week's watering

      | Step | Action |
      |---|---|
      | 1 | Set water to 10 |
      | 2 | If rain > 10, End; otherwise, Go to step 7 |
      | 3 | End |

      ## Facts

      **Records:**
        - **Name:** rain \
          **Type:** number \
          **Means:** the rain the bed took this week

        - **Name:** water \
          **Type:** number \
          **Means:** the water to pour on the bed this week
      ```

  - **Fixture:** watering-ration-without-an-end \
    **Holds:** a file on a garden's watering: an Algorithm of one step setting the water and no End, and a Facts section declaring the water \
    **Snippet:**

      ```markdown
      ## Watering Ration

      How much water a garden bed takes in a week.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:** none \
      **Output:**
        - water

      **Runs When:** the gardener plans the week's watering

      | Step | Action |
      |---|---|
      | 1 | Set water to 10 |

      ## Facts

      **Records:**
        - **Name:** water \
          **Type:** number \
          **Means:** the water to pour on the bed this week
      ```

  - **Fixture:** watering-ration-rounded-to-nearest \
    **Holds:** a file on a garden's watering: an Algorithm whose Rounding Mode is nearest, and a Facts section declaring the bed's area and the water \
    **Snippet:**

      ```markdown
      ## Watering Ration

      How much water a garden bed takes in a week.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - bed area

      **Output:**
        - water

      **Runs When:** the gardener plans the week's watering \
      **Rounding Mode:** nearest

      | Step | Action |
      |---|---|
      | 1 | Set water to bed area * 25 |
      | 2 | End |

      ## Facts

      **Records:**
        - **Name:** bed area \
          **Type:** number \
          **Means:** the area of the bed

        - **Name:** water \
          **Type:** number \
          **Means:** the water to pour on the bed this week
      ```
