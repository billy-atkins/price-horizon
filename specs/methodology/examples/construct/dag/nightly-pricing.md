## Nightly Pricing Run

A nightly pricing run, written whole as a file would hold it. Two extracts are free at once. A check of the margins they give has a timeout. A person makes a review only where a margin is flagged. A load waits for the check and the review. A report runs however the load ended, and the run tolerates the report's own failure:

```markdown
## Nightly Pricing

The nightly pricing run: prices and costs extracted, margins checked and reviewed, then loaded and reported.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG`

**Runs When:** the nightly pricing run, at 02:00 on each business date, a missed run caught up on the next and a late run taken when it comes

| Task | Work | Depends On | Guard | Timeout | Tolerated |
|---|---|---|---|---|---|
| extract prices | `§ Price Extraction` | none | none | none | No |
| extract costs | `§ Cost Extraction` | none | none | none | No |
| check margins | `§ Margin Check` | extract prices, extract costs | none | @"PT30M" | No |
| review flagged | none, leaving margins | check margins | some m in margins satisfies m.flagged? | none | No |
| load | `§ Margin Load` | check margins, review flagged | none | none | No |
| report | `§ Report Run` | load ended | none | none | Yes |

Review flagged is the pricing analyst's: each flagged margin is confirmed or corrected in the margins list, done when the analyst marks the review complete.

## Price Extraction

The night's valid prices, taken from the price feed.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- price feed

**Output:**

- prices

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set prices to price feed[valid?] |
| 2 | End |

## Cost Extraction

The night's valid costs, taken from the cost feed.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- cost feed

**Output:**

- costs

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set costs to cost feed[valid?] |
| 2 | End |

## Margin Check

Each sku's margin, flagged where it falls below the floor.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- prices
- costs
- floor

**Output:**

- margins

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set margins to for p in prices return {sku: p.sku, margin: p.price - costs[sku = p.sku][1].cost, flagged?: p.price - costs[sku = p.sku][1].cost < floor} |
| 2 | End |

## Margin Load

The load of the reviewed margins, giving how many were written.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- margins

**Output:**

- loaded

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set loaded to count(margins) |
| 2 | End |

## Report Run

The run's report of what it loaded for the business date.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- loaded
- business date

**Output:**

- report

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set report to {loaded: loaded, for: business date} |
| 2 | End |

## Facts

**Records:**

- **Name:** business date
  **Type:** date
  **Means:** the date the run prices, the business date the nightly run is launched for, in the trading desk's zone

- **Name:** price feed
  **Type:** list<context<sku: string, price: number, valid?: boolean>>
  **Means:** the night's prices as the feed delivers them

- **Name:** cost feed
  **Type:** list<context<sku: string, cost: number, valid?: boolean>>
  **Means:** the night's costs as the feed delivers them

- **Name:** prices
  **Type:** list<context<sku: string, price: number>>
  **Means:** the valid prices

- **Name:** costs
  **Type:** list<context<sku: string, cost: number>>
  **Means:** the valid costs

- **Name:** floor
  **Type:** number
  **Means:** the margin below which a sku is flagged

- **Name:** margins
  **Type:** list<context<sku: string, margin: number, flagged?: boolean>>
  **Means:** each sku's margin, flagged where it is below the floor, as the review left it

- **Name:** loaded
  **Type:** number
  **May Be Absent:** Yes
  **Means:** how many margins the load wrote, absent where the load failed

- **Name:** report
  **Type:** context<loaded: number, for: date>
  **Means:** the run's report, what it loaded and the business date it priced
```
