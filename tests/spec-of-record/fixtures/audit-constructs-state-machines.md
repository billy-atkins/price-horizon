**Records:**
  - **Fixture:** bakery-order \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order recorded in a fact whose Values list its four states, two transitions from placed on one trigger guarded by a question and its negation, a move to ready running an Algorithm as its effect, the Algorithm, and a Facts section declaring the order's status, whether it is paid and when it was baked \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected or cancelled.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Recorded In:** order status: `§ Facts [Name: order status]` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |
      | cancelled | given up before it was collected | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger | Guard | Effect |
      |---|---|---|---|---|
      | placed | ready | the baker takes it from the oven | paid? | `§ Bake Stamp` |
      | placed | cancelled | the baker takes it from the oven | not(paid?) | none |
      | ready | collected | the customer collects it | none | none |

      ## Bake Stamp

      The moment an order's bread comes out of the oven, recorded as it does.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:** none \
      **Output:**
        - baked at

      **Runs When:** `§ Bread Order`

      | Step | Action |
      |---|---|
      | 1 | Set baked at to now() |
      | 2 | End |

      ## Facts

      **Records:**
        - **Name:** order status \
          **Type:** string \
          **Values:** "placed", "ready", "collected", "cancelled" \
          **Means:** where the order stands

        - **Name:** paid? \
          **Type:** boolean \
          **Means:** whether the customer has paid for the order

        - **Name:** baked at \
          **Type:** date and time \
          **May Be Absent:** Yes \
          **Means:** when the order's bread came out of the oven
      ```

  - **Fixture:** bakery-order-effect-on-a-fact \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose move to ready gives as its Effect the citation of the Facts section, and a Facts section declaring when the order was baked \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger | Effect |
      |---|---|---|---|
      | placed | ready | the baker takes it from the oven | `§ Facts` |
      | ready | collected | the customer collects it | none |

      ## Facts

      **Records:**
        - **Name:** baked at \
          **Type:** date and time \
          **May Be Absent:** Yes \
          **Means:** when the order's bread came out of the oven
      ```

  - **Fixture:** bakery-order-guard-on-a-word \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose two transitions from placed on one trigger test the loaf's crust for "burnt" and for "golden", and a Facts section declaring the crust with the Values "pale" and "golden" \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected or cancelled.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |
      | cancelled | given up before it was collected | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger | Guard |
      |---|---|---|---|
      | placed | ready | the baker takes it from the oven | crust = "golden" |
      | placed | cancelled | the baker takes it from the oven | crust = "burnt" |
      | ready | collected | the customer collects it | none |

      ## Facts

      **Records:**
        - **Name:** crust \
          **Type:** string \
          **Values:** "pale", "golden" \
          **Means:** how the loaf's crust came out of the oven
      ```

  - **Fixture:** bakery-order-recorded-without-a-state \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order recorded in a fact whose Values list placed, ready and collected, its States table holding a fourth state, cancelled, and a Facts section declaring the order's status \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected or cancelled.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Recorded In:** order status: `§ Facts [Name: order status]` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |
      | cancelled | given up before it was collected | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | placed | ready | the baker takes it from the oven |
      | placed | cancelled | the customer calls it off |
      | ready | collected | the customer collects it |

      ## Facts

      **Records:**
        - **Name:** order status \
          **Type:** string \
          **Values:** "placed", "ready", "collected" \
          **Means:** where the order stands
      ```

  - **Fixture:** bakery-order-overlapping-guards \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose two transitions from placed on one trigger are guarded by loaves of 2 or more and loaves of 5 or more, and a Facts section declaring how many loaves the order holds \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to boxed or bagged.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | boxed | packed in a box | No | Yes |
      | bagged | packed in a bag | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger | Guard |
      |---|---|---|---|
      | placed | boxed | the baker packs it | loaves >= 5 |
      | placed | bagged | the baker packs it | loaves >= 2 |

      ## Facts

      **Records:**
        - **Name:** loaves \
          **Type:** number \
          **Means:** how many loaves the order holds
      ```
