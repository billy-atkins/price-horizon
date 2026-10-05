---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Position — where Brand A should sit

Not a single recommendation. A small, named set of positioning options, each stated as a price gap and relative price index against the predicted competitor outcome, evaluated at the granularity the decision actually requires.

Price gap is the plain currency difference between Brand A's price and the competitor's forecasted price. Relative price index is the same comparison as a ratio, Brand A's price divided by the competitor's, times 100, so a value above 100 means Brand A sits at a premium and a value below 100 means a discount. Both compare effective price (`specs/application/product/answer-engine/predict.md § Predict — what will the competitor do`), not sticker price, so a promotion running on either side is already accounted for before the comparison is made. Price gap is shown in the local currency of the geography being discussed, never the Query user's own, and a business unit spanning more than one country never blends it into one converted total, each country's own figures stay in that country's own currency; the answer is about a specific market, and a number someone in that market could actually act on has to be priced the way that market is. Relative price index carries no currency at all, a ratio, not an amount, so it needs none.

Every option carries the forecast's own confidence and its own rationale unchanged, rather than computing a score of its own: applying a positioning strategy to a forecast introduces no uncertainty the forecast did not already carry, so an option built on a low-confidence forecast is flagged exactly as low-confidence, with the same explanation behind it. Opening an option's confidence shows the forecast's own reasons, since it is the same score. `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` is where that sits alongside the other stages.

If two options would produce essentially the same outcome, they are shown as one rather than manufacturing a choice that is not really there, though the set never shrinks to a single option, since avoiding exactly that is what this stage is built for. Options are framed for judgment: the answer surfaces the choice, it does not make it. Each option carries its own brief explanation of the trade-off it represents, not just the numbers, the same discipline as the Predict narrative.

`specs/application/product/architecture.md § Diagrams § The Answer` and `specs/application/product/architecture.md § Diagrams § From Evidence to Answer` render this.

### Test Scenarios

```gherkin
Scenario: A price gap and relative price index compare net price, not sticker price.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months
  And a promotion is currently running on Brand A's price
  When the positioning options are generated
  Then each option's price gap and relative price index are computed against actual net price paid, not sticker price

Scenario: Position inherits Predict's confidence rather than computing its own.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months, flagged as low-confidence
  When the positioning options are generated
  Then every option carries that same low-confidence flag, the identical rationale, not a freshly computed score of its own
  And opening an option's confidence shows the same reasons the forecast's does

Scenario: Each option carries its own trade-off explanation.
  Given a Query user has generated positioning options for Competitor Brand's effective price in Texas in 6 months
  When the options are shown
  Then each option includes its own brief explanation of the trade-off it represents, not just its price gap and relative price index

Scenario: Options with the same outcome are consolidated, but never down to one.
  Given a Query user has a brand pricing decision for Competitor Brand's effective price in Texas in 6 months, where Hold and Match would produce essentially the same outcome for Brand A
  When the positioning options are generated
  Then Hold and Match are shown as one consolidated option
  And the answer still shows more than one option overall

Scenario: The system frames the choice without making it.
  Given a Query user has generated positioning options for Competitor Brand's effective price in Texas in 6 months
  When the options are shown
  Then no option is marked as the system's own recommendation
  And the choice among the options is left to the Query user

Scenario: Price gap stays in the geography's own local currency; relative price index has no currency to leak in the first place.
  Given a Query user has Predict forecasts for Competitor Brand's effective price in both Texas, in US dollars, and Ontario, in Canadian dollars, within the same business unit
  When the Query user generates positioning options for the Ontario forecast
  Then each option's price gap is expressed in Canadian dollars
  And no figure from the Texas forecast, in US dollars, is blended into it
  And each option's relative price index is a plain ratio, with no currency attached at all
```

### Options by Kind of Decision

Which kind of decision an answer serves is the Query user's session choice, or the question's own words where they say, per `specs/application/product/answer-engine/decision-context.md § Decision Context`. How far out the forecast looks never changes which options appear.

**Construct:** Decision Table

**Conditions:** Kind of decision

**Input Values:**
- Kind of decision: "A brand pricing decision, on list price or price position", "A retailer or promotional decision"

| Kind of decision | Options shown |
|---|---|
| A brand pricing decision, on list price or price position | The full set: Hold, Match, Close the Gap, and Diverge |
| A retailer or promotional decision | Hold, Match, and Close the Gap |

Diverge is left out of a retailer or promotional decision because it moves the brand's price position, which such a decision does not own.

`specs/application/product/architecture.md § Diagrams § The Answer` renders this.

#### Test Scenarios

```gherkin
Scenario: A brand pricing decision shows the full set of positioning options.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months
  And the decision is a brand pricing decision for Brand A
  When the positioning options are generated
  Then the answer shows the full set: Hold, Match, Close the Gap, and Diverge

Scenario: A retailer or promotional decision excludes Diverge.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months
  And the decision is a retailer or promotional decision for Brand A
  When the positioning options are generated
  Then the answer shows three options: Hold, Match, and Close the Gap
  And Diverge is not offered

Scenario: How far out the forecast looks does not change which options appear.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 1 month
  And the decision is a brand pricing decision for Brand A
  When the positioning options are generated
  Then the answer shows the full set: Hold, Match, Close the Gap, and Diverge
```

### The Strategies

Each option follows one of the defined strategies:

**Construct:** Decision Table

**Conditions:** Option

**Input Values:**
- Option: "Hold", "Match", "Close the Gap", "Diverge"

| Option | What it means for Brand A's price |
|---|---|
| Hold | Stay at today's price, regardless of what the competitor does |
| Match | Move by the same percentage the competitor is expected to move, so the relative price index holds steady at today's level |
| Close the Gap | Split the difference, half the percentage change between Hold and Match |
| Diverge | Lean further into whatever position Brand A already holds against the competitor, more premium if already at a premium, a deeper discount if already discounting, sized to the competitor's expected move |

A business unit may show its own labels for these options, each still standing for the same strategy (`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`).

`specs/application/product/architecture.md § Diagrams § The Answer` renders this.

#### Test Scenarios

```gherkin
Scenario: Hold keeps Brand A at today's price.
  Given a Query user has a brand pricing decision for Brand A, whose effective price in Texas is $4.00, and a Predict forecast that Competitor Brand's effective price in Texas rises 2% in 6 months
  And no two of the positioning options would produce essentially the same outcome
  When the positioning options are generated
  Then the Hold option prices Brand A at $4.00

Scenario: Match moves Brand A by the competitor's expected percentage.
  Given a Query user has a brand pricing decision for Brand A, whose effective price in Texas is $4.00, and a Predict forecast that Competitor Brand's effective price in Texas rises 2% in 6 months
  And no two of the positioning options would produce essentially the same outcome
  When the positioning options are generated
  Then the Match option prices Brand A at $4.08
  And its relative price index is today's

Scenario: Close the Gap splits the difference between Hold and Match.
  Given a Query user has a brand pricing decision for Brand A, whose effective price in Texas is $4.00, and a Predict forecast that Competitor Brand's effective price in Texas rises 2% in 6 months
  And no two of the positioning options would produce essentially the same outcome
  When the positioning options are generated
  Then the Close the Gap option prices Brand A at $4.04

Scenario: Diverge leans further into Brand A's existing position.
  Given a Query user has a brand pricing decision for Brand A, whose effective price in Texas sits at a premium to Competitor Brand's, and a Predict forecast that Competitor Brand's effective price in Texas rises 2% in 6 months
  And no two of the positioning options would produce essentially the same outcome
  When the positioning options are generated
  Then the Diverge option prices Brand A higher than the Match option does
  And its relative price index rises above today's
```
