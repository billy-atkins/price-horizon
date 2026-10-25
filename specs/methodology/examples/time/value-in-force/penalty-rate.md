## Penalty Rate

A penalty rate that changes from a date on, and the penalty accrued over a period it changes within, written whole as a file would hold it. The rate in force is a function of the day, read only by a call naming the day. The penalty is accrued day by day, each day at that day's rate, so a period a change falls within is split at the change:

```markdown
## Period Penalty

The penalty an overdue balance accrues over a period, each day at the penalty rate in force that day.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - balance
  - period start
  - period end
  - penalty rate

**Output:**
  - period penalty

**Runs When:** a period is closed

| Step | Action |
|---|---|
| 1 | Set period penalty to if period end > period start then sum(for i in 0..(period end - period start).days - 1 return balance * penalty rate(period start + @"P1D" * i) / 365) else 0 |
| 2 | End |

## Facts

**Records:**
  - **Name:** balance \
    **Type:** number \
    **Unit:** USD \
    **Means:** the overdue balance, unchanged over the period

  - **Name:** period start \
    **Type:** date \
    **Means:** the period's first day

  - **Name:** period end \
    **Type:** date \
    **Means:** the day after the period's last day

  - **Name:** penalty rates \
    **Type:** list<context<from: date, rate: number>> \
    **Means:** each yearly penalty rate and the date it took force from, in the order of those dates

  - **Name:** penalty rate \
    **Type:** function<date> -> number \
    **Derivation:** function(day) penalty rates[from <= day][-1].rate \
    **Means:** the yearly penalty rate in force on a day

  - **Name:** period penalty \
    **Type:** number \
    **Unit:** USD \
    **Decimal Places:** 2 \
    **Means:** the penalty the period accrues
```

From a balance of 1,000.00 over a period from `@"2024-03-01"` to `@"2024-04-01"`, the rate 7.3% to March 15 and 10.95% from March 16:

| Days | Rate | Penalty |
|---|---|---|
| March 1 to 15, 15 days | 0.073 | 3.00 |
| March 16 to 31, 16 days | 0.1095 | 4.80 |
| the period, 31 days | | 7.80 |

A period whose end is its start accrues nothing. Read at the period's start alone, as `penalty rate(period start)` would, the whole period would take 0.073 and accrue 6.20. Which one a spec writes is the rule the business holds, and the instant each read names says it.
