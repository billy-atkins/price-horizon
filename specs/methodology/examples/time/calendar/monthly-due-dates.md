## Monthly Due Dates

A loan's monthly due dates by three rules, written whole as a file would hold it. Each rule is exact, and which one a loan follows is the lender's to say. Chained, each date is a month after the one before, so a day a short month lacks is pinned there and the series stays on the pinned day. Anchored, each date is the first date and a month's multiple, so each is pinned against the first date alone. Kept at the month's end, each date is its month's last day:

```markdown
## Due Dates

A loan's installments' due dates, a month apart, by each of the rules a lender may hold.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - first due date
  - term

**Output:**
  - chained due dates
  - anchored due dates
  - month-end due dates

**Runs When:** the loan is disbursed

| Step | Action |
|---|---|
| 1 | Set chained due dates to for i in 1..term return if i = 1 then first due date else partial[-1] + @"P1M" |
| 2 | Set anchored due dates to for i in 0..term - 1 return first due date + @"P1M" * i |
| 3 | Set month-end due dates to for i in 0..term - 1 return last day of month(first due date + @"P1M" * i) |
| 4 | End |

## Facts

**Records:**
  - **Name:** first due date \
    **Type:** date \
    **Means:** the first installment's due date

  - **Name:** term \
    **Type:** number \
    **Means:** how many installments the loan has

  - **Name:** chained due dates \
    **Type:** list<date> \
    **Means:** each installment's due date, a month after the one before

  - **Name:** anchored due dates \
    **Type:** list<date> \
    **Means:** each installment's due date, on the first due date's day of its month, or its month's last day where the month lacks that day

  - **Name:** month-end due dates \
    **Type:** list<date> \
    **Means:** each installment's due date, its month's last day
```

The dates each rule gives over a term of 4:

| First Due Date | Rule | Due Dates |
|---|---|---|
| `@"2024-01-31"` | chained | 2024-01-31, 2024-02-29, 2024-03-29, 2024-04-29 |
| `@"2024-01-31"` | anchored | 2024-01-31, 2024-02-29, 2024-03-31, 2024-04-30 |
| `@"2024-01-31"` | month-end | 2024-01-31, 2024-02-29, 2024-03-31, 2024-04-30 |
| `@"2024-02-29"` | chained | 2024-02-29, 2024-03-29, 2024-04-29, 2024-05-29 |
| `@"2024-02-29"` | anchored | 2024-02-29, 2024-03-29, 2024-04-29, 2024-05-29 |
| `@"2024-02-29"` | month-end | 2024-02-29, 2024-03-31, 2024-04-30, 2024-05-31 |

From January 31 the chained series stays on the 29th after February, each addition pinned against its own result, where the anchored series returns to each month's last. From February 29 the anchored series has the 29th as its day, and only the month-end rule keeps each date at its month's end. A loop adding a month to the last date, as a program writes one, follows the chained rule, so a spec meaning another rule says which.
