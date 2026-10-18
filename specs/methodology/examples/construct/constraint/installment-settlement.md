## Installment Settlement

A schedule's installments, a payment settling one, written whole as a file would hold it. It holds an invariant over every installment, a postcondition of the settlement reading its Output and a before-value, and a stored total the system derives and keeps only by a nightly job, which is a warning:

```markdown
## Installment Settlement

A payment received, settled against its installment up to what is due.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- installment
- payment

**Output:**

- installment

**Runs When:** a payment is received

| Step | Action |
|---|---|
| 1 | Set installment.paid to min(installment.paid + payment, installment.due) |
| 2 | End |

## Settlement Rules

What holds of a schedule's installments as payments settle them.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| every i in installments satisfies i.paid <= i.due | always | `§ Installment Settlement [Step: 1]` |
| installment.paid >= paid before | after `§ Installment Settlement` | `§ Installment Settlement [Step: 1]` |
| schedule.total paid = sum(for i in installments return i.paid) | always | nothing: the total is written by a nightly job and lags the installments between its runs |

## Facts

**Records:**

- **Name:** installments
  **Type:** list<context<due: number, paid: number>>
  **Means:** the schedule's installments, each with what it is due and what has been paid of it

- **Name:** installment
  **Type:** context<due: number, paid: number>
  **Means:** the installment a payment settles

- **Name:** payment
  **Type:** number
  **Means:** the amount received

- **Name:** paid before
  **Type:** number
  **Means:** what the installment had paid as the settlement began

- **Name:** schedule
  **Type:** context<total paid: number>
  **Means:** the schedule, with the total its nightly job writes
```
