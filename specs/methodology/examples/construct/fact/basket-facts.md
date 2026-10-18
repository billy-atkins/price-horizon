## Basket Facts

A basket's facts, written whole as a file would hold them. They are a list of contexts, a value derived from it and held to cents, a percentage that starts at zero, and a code the buyer may leave out:

```markdown
## Facts

**Records:**

- **Name:** basket lines
  **Type:** list<context<sku: string, quantity: number, unit price: number>>
  **Means:** the lines of a buyer's basket, each an item, how many and its price in euros

- **Name:** basket total
  **Type:** function<list<context<sku: string, quantity: number, unit price: number>>> -> number
  **Decimal Places:** 2
  **Derivation:** function(lines) if count(lines) = 0 then 0 else sum(for line in lines return line.quantity * line.unit price)
  **Means:** what a basket's lines come to in euros, before any discount

- **Name:** discount rate
  **Type:** number
  **Values:** [0..100]
  **Unit:** percent
  **Initial Value:** 0
  **Means:** the share of the basket total a coupon takes off

- **Name:** coupon code
  **Type:** string
  **May Be Absent:** Yes
  **Means:** the code the buyer entered, where they entered one
```

The fact basket total is a function of the basket's lines. Its Derivation is the FEEL function giving it. An empty basket comes to 0, since FEEL's sum of an empty list is null. A step reads it by a call given the current lines, `basket total(basket lines)`, as [`specs/methodology/modeling-constructs.md § Constructs § Algorithm`](/specs/methodology/modeling-constructs.md#algorithm) has a derived value read. Its Decimal Places hold the value it gives to cents. The fact discount rate is counted in percent, bounded by its Values, and starts at 0 by its Initial Value. The fact coupon code may be absent.
