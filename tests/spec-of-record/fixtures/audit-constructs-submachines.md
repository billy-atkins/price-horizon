**Records:**
  - **Fixture:** bread-order-baked-in-one-batch \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose state baking is governed by the file's second machine, an oven batch with one terminal state, and is left by one transition with no trigger and no guard \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | baking | in the oven, governed by `§ Oven Batch` | No | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | placed | baking | the baker loads the oven |
      | baking | ready | none |
      | ready | collected | the customer collects it |

      ## Oven Batch

      One batch of loaves in the oven, from loaded to baked.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | loaded | the loaves in the hot oven | Yes | No |
      | baked | the loaves done | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | loaded | baked | the oven timer rings |
      ```

  - **Fixture:** bread-order-baked-in-a-batch-of-two-ends \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose state baking is governed by the file's second machine, an oven batch with two terminal states, baked and burnt, and is left by one transition with no trigger and no guard \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | baking | in the oven, governed by `§ Oven Batch` | No | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | placed | baking | the baker loads the oven |
      | baking | ready | none |
      | ready | collected | the customer collects it |

      ## Oven Batch

      One batch of loaves in the oven, from loaded to baked or burnt.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | loaded | the loaves in the hot oven | Yes | No |
      | baked | the loaves done | No | Yes |
      | burnt | the loaves left in too long | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | loaded | baked | the oven timer rings |
      | loaded | burnt | the oven timer is missed |
      ```

  - **Fixture:** bread-order-governed-by-its-facts \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order whose state baking's description says governed by and cites the file's Facts section, which declares the oven's heat \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread placed at a bakery, from placed to collected.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | placed | ordered, not yet baked | Yes | No |
      | baking | in the oven, governed by `§ Facts` | No | No |
      | ready | baked and waiting on the shelf | No | No |
      | collected | taken home by the customer | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | placed | baking | the baker loads the oven |
      | baking | ready | none |
      | ready | collected | the customer collects it |

      ## Facts

      **Records:**
        - **Name:** oven heat \
          **Type:** number \
          **Unit:** degrees Celsius \
          **Means:** how hot the oven is
      ```
