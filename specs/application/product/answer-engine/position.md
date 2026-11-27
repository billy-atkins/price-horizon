---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Position: where Brand A should sit

Position offers a small, named set of positioning options, not a single recommendation. Each option shows the available price gap and relative price index against the predicted competitor outcome. Each is evaluated at the granularity the decision requires.

Price gap is the absolute currency difference between Brand A's price and the competitor's forecast price. Relative price index is the same comparison as a ratio: Brand A's price divided by the competitor's, times 100. A value above 100 means Brand A sits at a premium, and a value below 100 means a discount. Both compare effective price ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)), not sticker price, so a promotion running on either side is already accounted for before the comparison is made.

Price gap is shown in the local currency of the geography being discussed, never the Query user's own. A business unit spanning more than one country never blends price gap into one converted total. Each country's figures stay in that country's currency. The answer is about a specific market, and a number someone in that market could act on has to be priced the way that market is. Relative price index is a ratio, not an amount, so it carries no currency at all.

Every option carries the forecast's confidence and rationale unchanged. Position computes no score of its own. Applying a positioning strategy to a forecast introduces no uncertainty the forecast did not already carry. An option built on a low-confidence forecast is therefore flagged low-confidence, as the forecast is, with the same explanation behind it. Opening an option's confidence shows the forecast's reasons, since it is the same score. [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) is where that sits alongside the other stages.

After simulation, options close on every displayed comparison may be shown together. Every member must qualify against every other member of its group. Two choices remain even when every outcome is equal. Each group opens to the original strategy labels and individual figures. If grouping is unavailable, the answer shows individual options and preserves completed outcomes. Options are framed for judgment: the answer surfaces the choice and does not make it. Each option carries a brief explanation of the trade-off it represents, alongside its numbers. This is the same discipline as the Predict narrative.

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer), [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) and [`specs/application/product/architecture.md § Diagrams § When an Answer Falls Short`](/specs/application/product/architecture.md#when-an-answer-falls-short) render this.

At 9 against a competitor forecast of 10, the gap is 1 in local currency and the index is 90. At 11 against 10, the gap is also 1 and the index is 110. A product or geographic match under review leaves the dependent comparison unavailable until resolution. A zero competitor target leaves the index unavailable. A missing percentage base leaves the dependent strategies unavailable; independently supported information such as today’s Hold price remains accessible.

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
  Then every option carries that same low-confidence flag and the identical rationale, not a freshly computed score of its own
  And opening an option's confidence shows the same reasons the forecast's does

Scenario: Each option carries its own trade-off explanation.
  Given a Query user has generated positioning options for Competitor Brand's effective price in Texas in 6 months
  When the options are shown
  Then each option includes its own brief explanation of the trade-off it represents, not just its price gap and relative price index

Scenario: Options with the same outcome are consolidated, but never down to one.
  Given a strategic decision where the competitor price stays unchanged and all four candidates have identical prices and complete, identical projected outcomes
  When the user opens the positioning choices
  Then Hold, Match and Close the Gap appear as members of the first option in that order
  And Diverge appears separately with its equal figures as the second option

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

Scenario: A discount and an equal premium have different indices.
  Given two candidate prices of 9 and 11 in local currency against the same competitor forecast of 10
  When the Query user opens the positioned prices
  Then both gaps are 1 and the indices are 90 and 110 respectively

Scenario: At parity Diverge has the same price as Match.
  Given both brands start at 10 and the competitor is forecast to reach 11
  When a Query user asks a strategic pricing question
  Then Match and Diverge each have a candidate price of 11 before grouping

Scenario: A flagged comparison remains unavailable.
  Given the product match for a proposed price comparison awaits review
  When a Query user opens Position
  Then the price gap and relative price index show that the match awaits review
  And the current Hold price remains visible if its own evidence is available

Scenario: The original grouping survives a settings change.
  Given a delivered answer showed Hold and Match as one option with two member prices
  And a Control plane admin later renamed Hold and changed the materiality thresholds
  When the original delivery is opened by an authorized reader
  Then it shows the original label, group order and both original member prices

Scenario: The requested geography supplies the positioned comparison.
  Given a resolved state comparison with a candidate price of 12 against 10
  And the same candidate at a grounded metro has a price of 12 against 11
  When a Query user drills down to that metro
  Then the option shows the metro gap of 1 in its local currency and identifies its metro forecast

Scenario: Failure to group completed outcomes preserves each result.
  Given simulation completed for all three tactical options and grouping retries were exhausted
  When the user opens the delivered answer
  Then it shows Hold, Match and Close the Gap separately in that order with their completed projections
  And it identifies grouping as unavailable

Scenario: A zero target preserves the gap and withholds the index.
  Given Brand A starts at 9 and a resolved competitor starts at 10 and is forecast to reach zero
  When the user opens Hold
  Then its price is 9 and its currency gap is 9
  And the index is unavailable because the target denominator is zero

Scenario: A zero starting competitor price leaves the independent Hold price visible.
  Given Brand A starts at 9 and the matched competitor starts at zero and is forecast to reach 10
  When the user opens a strategic positioning answer
  Then Hold shows 9 with a gap of 1 and an index of 90
  And Match, Close the Gap and Diverge show that the starting competitor price cannot support a percentage move
```

### Options by Kind of Decision

The kind of decision an answer serves is the one the Query user chose for the session, or the one the question's own words name where they name one, per [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context). The horizon leaves the eligible strategies unchanged. Their computed prices and outcomes can change with the horizon, so different strategies can end up grouped.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind of decision \
**Input Values:**
  - Kind of decision: "A brand pricing decision, on list price or price position", "A retailer or promotional decision"

| Kind of decision | Eligible options |
|---|---|
| A brand pricing decision, on list price or price position | Hold, Match, Close the Gap, and Diverge |
| A retailer or promotional decision | Hold, Match, and Close the Gap |

Diverge is left out of a retailer or promotional decision because it moves the brand's price position, which such a decision does not own.

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer) renders this.

#### Test Scenarios

```gherkin
Scenario: A brand pricing decision shows the full set of positioning options.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months
  And the decision is a brand pricing decision for Brand A
  And the eligible options have materially different outcomes
  When the positioning options are generated
  Then the answer shows the full set: Hold, Match, Close the Gap, and Diverge

Scenario: A retailer or promotional decision excludes Diverge.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months
  And the decision is a retailer or promotional decision for Brand A
  And the eligible options have materially different outcomes
  When the positioning options are generated
  Then the answer shows three options: Hold, Match, and Close the Gap
  And Diverge is not offered

Scenario: A short horizon keeps every eligible strategic option.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 1 month
  And the decision is a brand pricing decision for Brand A
  And the eligible options have materially different outcomes
  When the positioning options are generated
  Then the answer shows the full set: Hold, Match, Close the Gap, and Diverge
```

### The Strategies

Each option follows one of the defined strategies:

**Reference Key:** Option \
**Required:** Brand A Price Move

| Option | Brand A Price Move |
|---|---|
| Hold | Stay at today's price, regardless of what the competitor does |
| Match | Move by the same percentage the competitor is expected to move, so the relative price index holds steady at today's level |
| Close the Gap | Split the difference: half the percentage change between Hold and Match |
| Diverge | Lean further into whatever position Brand A already holds against the competitor (more premium if already at a premium, a deeper discount if already discounting), by adding one more move of the competitor’s percentage size, measured on Brand A’s starting price, to Match for a premium or subtracting it for a discount. At parity use Match; a discount price floors at zero |

A business unit may show its own labels for these options, each still standing for the same strategy ([`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings)).

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer) renders this.

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

Scenario: Two matching neighbors cannot pull a nonmatching pair into one group.
  Given four eligible candidates A, B, C and D in increasing absolute price-gap order
  And their projected shares are 18.0%, 18.7%, 19.4% and 23.0% with a one-point threshold
  And every other required measure is available and within its threshold
  When the Query user opens the positioning choices
  Then A and B appear together, C appears separately, and D appears separately
  And opening the first group identifies A and B and their individual delivered figures
```
