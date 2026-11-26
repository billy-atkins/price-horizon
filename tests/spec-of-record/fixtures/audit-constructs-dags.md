**Records:**
  - **Fixture:** morning-bake \
    **Holds:** a file on a bakery's morning bake: a DAG of three tasks, a dough mixed by an Algorithm and an oven heated outside the specs, free at once, then the loaves baked by an Algorithm once both are done; the two Algorithms, each run when the DAG runs; and a Facts section declaring the flour, the dough, the oven's heat and the loaves \
    **Snippet:**

      ```markdown
      ## Morning Bake

      The bakery's morning bake: the dough mixed and the oven heated, then the loaves baked.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG` \
      **Runs When:** the morning bake, at 04:00 each day the bakery opens

      | Task | Work | Depends On |
      |---|---|---|
      | mix dough | `§ Dough Mix` | none |
      | heat oven | none, leaving oven heat | none |
      | bake loaves | `§ Loaf Bake` | mix dough, heat oven |

      ## Dough Mix

      The dough the morning's flour makes.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - flour

      **Output:**
        - dough

      **Runs When:** `§ Morning Bake`

      | Step | Action |
      |---|---|
      | 1 | Set dough to flour * 1.6 |
      | 2 | End |

      ## Loaf Bake

      The loaves the dough makes in the heated oven.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - dough
        - oven heat

      **Output:**
        - loaves

      **Runs When:** `§ Morning Bake`

      | Step | Action |
      |---|---|
      | 1 | Set loaves to floor(dough / 0.5) |
      | 2 | End |

      ## Facts

      **Records:**
        - **Name:** flour \
          **Type:** number \
          **Unit:** kilogram \
          **Means:** the flour weighed out for the morning

        - **Name:** dough \
          **Type:** number \
          **Unit:** kilogram \
          **Means:** the dough mixed from the flour

        - **Name:** oven heat \
          **Type:** number \
          **Unit:** degrees Celsius \
          **Means:** how hot the oven is once heated

        - **Name:** loaves \
          **Type:** number \
          **Means:** how many loaves the morning baked
      ```

  - **Fixture:** morning-bake-waiting-on-a-missing-task \
    **Holds:** a file on a bakery's morning bake: a DAG of two tasks done outside the specs, the second depending on a task named proof dough that its table does not hold, and a Facts section declaring the dough and the loaves \
    **Snippet:**

      ```markdown
      ## Morning Bake

      The bakery's morning bake: the dough mixed, then the loaves baked.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG` \
      **Runs When:** the morning bake, at 04:00 each day the bakery opens

      | Task | Work | Depends On |
      |---|---|---|
      | mix dough | none, leaving dough | none |
      | bake loaves | none, leaving loaves | proof dough |

      ## Facts

      **Records:**
        - **Name:** dough \
          **Type:** number \
          **Means:** the dough mixed for the morning

        - **Name:** loaves \
          **Type:** number \
          **Means:** how many loaves the morning baked
      ```

  - **Fixture:** morning-bake-in-a-circle \
    **Holds:** a file on a bakery's morning bake: a DAG of two tasks done outside the specs, each depending on the other, and a Facts section declaring the dough and the loaves \
    **Snippet:**

      ```markdown
      ## Morning Bake

      The bakery's morning bake: the dough mixed and the loaves baked.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG` \
      **Runs When:** the morning bake, at 04:00 each day the bakery opens

      | Task | Work | Depends On |
      |---|---|---|
      | mix dough | none, leaving dough | bake loaves |
      | bake loaves | none, leaving loaves | mix dough |

      ## Facts

      **Records:**
        - **Name:** dough \
          **Type:** number \
          **Means:** the dough mixed for the morning

        - **Name:** loaves \
          **Type:** number \
          **Means:** how many loaves the morning baked
      ```

  - **Fixture:** morning-bake-two-mixers \
    **Holds:** a file on a bakery's morning bake: a DAG of two tasks free at once, each done outside the specs and each leaving the dough, and a Facts section declaring the dough \
    **Snippet:**

      ```markdown
      ## Morning Bake

      The bakery's morning bake: the dough mixed by hand and by machine.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG` \
      **Runs When:** the morning bake, at 04:00 each day the bakery opens

      | Task | Work | Depends On |
      |---|---|---|
      | mix by hand | none, leaving dough | none |
      | mix by machine | none, leaving dough | none |

      ## Facts

      **Records:**
        - **Name:** dough \
          **Type:** number \
          **Means:** the dough mixed for the morning
      ```
