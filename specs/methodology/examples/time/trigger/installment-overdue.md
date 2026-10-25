## Installment Overdue

An installment of a loan from due to paid or written off, written whole as a file would hold it, each kind of time trigger moving it. It falls overdue at an absolute instant, the close of its due date in New York. It goes to collection once 30 days pass in overdue, relative time. It is written off once 60 business days pass in collection, a condition on the business date, a clock other than the wall clock, counted from the business date the move to collection records. It is paid once its balance reaches zero, a condition:

```markdown
## Installment

An installment of a loan, from due to paid or written off.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| due | owed, its due date not yet closed | Yes | No |
| overdue | owed past the close of its due date | No | No |
| in collection | handed to collection, owed 30 days past due | No | No |
| paid | paid in full | No | Yes |
| written off | written off unpaid | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Effect |
|---|---|---|---|
| due | paid | when balance <= 0 | none |
| due | overdue | at date and time(due date, @"17:00:00@America/New_York") | none |
| overdue | paid | when balance <= 0 | none |
| overdue | in collection | after @"P30D" | `§ Collection Start` |
| in collection | paid | when balance <= 0 | none |
| in collection | written off | when business date >= add business days(collection began, 60, trading calendar) | none |

## Collection Start

The business date an installment goes to collection, recorded as it goes.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - business date

**Output:**
  - collection began

**Runs When:** `§ Installment`

| Step | Action |
|---|---|
| 1 | Set collection began to business date |
| 2 | End |

## Facts

**Records:**
  - **Name:** balance \
    **Type:** number \
    **Unit:** USD \
    **Means:** what is still owed on the installment

  - **Name:** due date \
    **Type:** date \
    **Means:** the installment's due date

  - **Name:** business date \
    **Type:** date \
    **Means:** the business date the lender's close of business last closed, a clock its job advances, in New York

  - **Name:** trading calendar \
    **Type:** context<weekend: list<number>, holidays: list<date>> \
    **Means:** the lender's business days, its weekend Saturday and Sunday and its holidays the bank holidays it keeps

  - **Name:** collection began \
    **Type:** date \
    **May Be Absent:** Yes \
    **Means:** the business date the installment went to collection
```

The fall overdue reads the wall clock at 17:00 in New York, a date and time in that zone, where the due date alone would stand for its midnight UTC. The 30 days are counted from entering overdue. The write-off counts business days from entering collection, so the move to collection records its business date by its effect, and the write-off is a condition on the business date, taken the moment that clock reaches the 60th business day after it. A payment clearing the balance pays the installment from any state it is owed in.
