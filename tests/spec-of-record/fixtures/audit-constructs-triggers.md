**Records:**
  - **Fixture:** bread-order-on-the-shelf \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order taken from ready on three triggers written in FEEL, `when` loaves left reaches 0, `at` the day after its pickup day, and `after` two days, and a Facts section declaring the loaves left and the pickup day \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread waiting on a bakery's shelf, from ready to collected or given away.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | ready | baked and waiting on the shelf | Yes | No |
      | collected | every loaf taken home by the customer | No | Yes |
      | given away | handed to the food bank | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | ready | collected | when loaves left <= 0 |
      | ready | given away | at pickup day + @"P1D" |
      | ready | given away | after @"P2D" |

      ## Facts

      **Records:**
        - **Name:** loaves left \
          **Type:** number \
          **Means:** how many of the order's loaves are still on the shelf

        - **Name:** pickup day \
          **Type:** date \
          **Means:** the day the customer said they would collect the order
      ```

  - **Fixture:** bread-order-after-a-date \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order taken from ready on a trigger written `after pickup day`, and a Facts section declaring the pickup day, a date \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread waiting on a bakery's shelf, from ready to collected or given away.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | ready | baked and waiting on the shelf | Yes | No |
      | collected | taken home by the customer | No | Yes |
      | given away | handed to the food bank | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | ready | collected | the customer collects it |
      | ready | given away | after pickup day |

      ## Facts

      **Records:**
        - **Name:** pickup day \
          **Type:** date \
          **Means:** the day the customer said they would collect the order
      ```

  - **Fixture:** bread-order-when-a-count \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order taken from ready on a trigger written `when loaves left`, and a Facts section declaring the loaves left, a number \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread waiting on a bakery's shelf, from ready to collected or given away.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | ready | baked and waiting on the shelf | Yes | No |
      | collected | taken home by the customer | No | Yes |
      | given away | handed to the food bank | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | ready | collected | the customer collects it |
      | ready | given away | when loaves left |

      ## Facts

      **Records:**
        - **Name:** loaves left \
          **Type:** number \
          **Means:** how many of the order's loaves are still on the shelf
      ```

  - **Fixture:** bread-order-at-tomorrow \
    **Holds:** a file on a bakery's bread orders: a State Machine of an order taken from ready on a trigger written `at today() + @"P1D"` \
    **Snippet:**

      ```markdown
      ## Bread Order

      An order for bread waiting on a bakery's shelf, from ready to collected or given away.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
      **Table Name:** States

      | State | Description | Initial | Terminal |
      |---|---|---|---|
      | ready | baked and waiting on the shelf | Yes | No |
      | collected | taken home by the customer | No | Yes |
      | given away | handed to the food bank | No | Yes |

      **Table Name:** Transitions

      | From | To | Trigger |
      |---|---|---|
      | ready | collected | the customer collects it |
      | ready | given away | at today() + @"P1D" |
      ```
