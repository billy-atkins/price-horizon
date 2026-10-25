## Installment Schedule

A schedule's installments, each period given its share of the rate by a Decision Table, in a system holding 19 significant digits and rounding money half up, written whole as a file would hold it:

```markdown
### Installments

A schedule's installments, each period's share of the rate applied to its balance, and the total still due.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - periods
  - rate

**Output:**
  - periods
  - total due

**Runs When:** `§ Schedule Build` \
**Precision:** 19 \
**Rounding Mode:** half up

| Step | Action |
|---|---|
| 1 | For each period of periods, by period.number ascending, gathering period into periods: steps 2 to 4 |
| 2 | Run `§ Period Share` with Days as (period.due date - period.from date).days, with Annual rate as rate, giving Share as share |
| 3 | Set installment to balance(period) * share |
| 4 | Set period.installment to installment |
| 5 | Set total due to sum(for p in periods[not(settled(item))] return p.installment) |
| 6 | End |

#### Facts

**Records:**
  - **Name:** periods \
    **Type:** list<context<number: number, from date: date, due date: date, installment: number>> \
    **Means:** the schedule's periods, in order

  - **Name:** installment \
    **Type:** number \
    **Decimal Places:** 2 \
    **Means:** a period's installment, held to cents

  - **Name:** balance \
    **Type:** function<context> -> number \
    **Decimal Places:** 2 \
    **Means:** a period's opening balance, as the ledger computes it

  - **Name:** settled \
    **Type:** function<context> -> boolean \
    **Derivation:** function(period) period.installment = 0 \
    **Means:** whether a period has nothing left to pay
```

Step 1 walks the list in its keys' order and gathers each updated item back into it, and the list is set once the loop ends. Step 2 runs a Decision Table. It gives each fact the table takes by `with`, and writes the table's outcome `Share` to a fact of another name by `as`. Step 3 multiplies money, so it writes to a fact holding decimal places, rounded to cents half up, with each operation first held to 19 digits. Step 3 also reads a value the ledger computes, by a call. Step 4 sets a part from that fact, a part holding no decimal places of its own. Step 5 reads a value the specs derive, by a call given each current period, and its `settled` is defined once, by its Derivation.
