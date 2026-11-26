**Records:**
  - **Fixture:** allotment-rules \
    **Holds:** a file on a garden's allotments: an Algorithm letting a plot to a tenant, a Constraint of two rules, one holding always and one after the letting, each enforced by the letting's step, and a Facts section declaring the plots, the plot let and its tenant \
    **Snippet:**

      ```markdown
      ## Plot Letting

      A plot let to a tenant on the waiting list.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
      **Inputs:**
        - plot
        - tenant

      **Output:**
        - plot

      **Runs When:** a plot falls vacant

      | Step | Action |
      |---|---|
      | 1 | Set plot.tenant to tenant |
      | 2 | End |

      ## Allotment Rules

      What holds of the garden's plots as they are let.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

      | Constraint | Applies To | Enforced By |
      |---|---|---|
      | every p in plots satisfies p.size <= 250 | always | `§ Plot Letting [Step: 1]` |
      | plot.tenant = tenant | after `§ Plot Letting` | `§ Plot Letting [Step: 1]` |

      ## Facts

      **Records:**
        - **Name:** plots \
          **Type:** list<context<size: number, tenant: string>> \
          **Means:** the garden's plots, each with its size and its tenant

        - **Name:** plot \
          **Type:** context<size: number, tenant: string> \
          **Means:** the plot let

        - **Name:** tenant \
          **Type:** string \
          **Means:** the tenant the plot is let to
      ```

  - **Fixture:** allotment-rules-held-sometimes \
    **Holds:** a file on a garden's allotments: a Constraint of one rule on the plots' sizes whose Applies To is sometimes and whose Enforced By cites the file's Facts section, and a Facts section declaring the plots \
    **Snippet:**

      ```markdown
      ## Allotment Rules

      What holds of the garden's plots.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

      | Constraint | Applies To | Enforced By |
      |---|---|---|
      | every p in plots satisfies p.size <= 250 | sometimes | `§ Facts` |

      ## Facts

      **Records:**
        - **Name:** plots \
          **Type:** list<context<size: number>> \
          **Means:** the garden's plots, each with its size
      ```

  - **Fixture:** allotment-rules-kept-by-the-committee \
    **Holds:** a file on a garden's allotments: a Constraint of one rule on the plots' sizes, holding always, whose Enforced By is the words the committee, and a Facts section declaring the plots \
    **Snippet:**

      ```markdown
      ## Allotment Rules

      What holds of the garden's plots.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

      | Constraint | Applies To | Enforced By |
      |---|---|---|
      | every p in plots satisfies p.size <= 250 | always | the committee |

      ## Facts

      **Records:**
        - **Name:** plots \
          **Type:** list<context<size: number>> \
          **Means:** the garden's plots, each with its size
      ```

  - **Fixture:** allotment-rules-counting-plots \
    **Holds:** a file on a garden's allotments: a Constraint of one rule, holding always, written as the count of the plots, enforced by the citation of the file's Facts section, and a Facts section declaring the plots \
    **Snippet:**

      ```markdown
      ## Allotment Rules

      What holds of the garden's plots.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

      | Constraint | Applies To | Enforced By |
      |---|---|---|
      | count(plots) | always | `§ Facts` |

      ## Facts

      **Records:**
        - **Name:** plots \
          **Type:** list<context<size: number>> \
          **Means:** the garden's plots, each with its size
      ```
