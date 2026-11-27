---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Drill-down: cross-cutting, available at every stage

Drill-down has independent axes. A user can move along either one without leaving the analysis:
- **Granularity.** Country to state or province to major metro, matching how the competitor's own pricing data is reported.
- **Metric.** Price is the default lens. A user can pivot the same drill-down to volume, margin, or share without asking the question again.

Throughout every stage ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do), [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit), [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)), the narrative layer gives a fluent explanation of numbers that already exist. It does not generate new ones. That distinction keeps the answer defensible in front of a retailer or a CFO.

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer) renders this.

### What a granularity drill-down shows

What a granularity drill-down shows depends on the geographic level supported by the evidence. A reported competitor observation supports that side of the analysis. A matched Position or Simulate value also requires reliable product and geography alignment at the selected level. When alignment is unresolved, show the available sourced facts and the reason the dependent value is unavailable:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Granularity \
**Annotations:** Such As \
**Input Values:**
  - Granularity: "Within the reported range", "Below the reported range"

| Granularity | Figure shown | Decomposition graph | Such As |
|---|---|---|---|
| Within the reported range | The forecast and evidence for the selected geography, resolved just as for a direct question | Available where attribution was computed | country, state or province, major metro |
| Below the reported range | A qualified local quantity or recomputed rate, labeled as estimated. Without local rate inputs show the labeled parent reference and mark the local rate unavailable | Unavailable for estimated figures | county, store |

That boundary reflects which competitor data is currently licensed and ingested. It is not a permanent limit. A more granular data source would move it. [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) shows when the user receives a local estimate or a regional reference.

### Test Scenarios

```gherkin
Scenario: Drilling down within the licensed range stays consistent and keeps the decomposition graph.
  Given a Query user has an existing Predict answer for Competitor Brand's effective price in Texas in 6 months, at the state or province granularity
  When the Query user drills down to major metro, within that same licensed range
  Then the answer uses the published metro forecast and evidence a direct question would retrieve
  And the decomposition graph remains available

Scenario: A supported local allocation opens to its source.
  Given a grounded metro volume of 1,000 units and a supported county retail-footprint weight of 0.1
  When a Query user drills down to the county volume
  Then the estimate is 100 units and opens to the metro observation and the dated weight
  And the answer shows no county-level decomposition

Scenario: Pivoting the metric does not require re-asking the question.
  Given a Query user has an existing Predict answer for Competitor Brand's effective price in Texas in 6 months
  When the Query user pivots the metric from price to volume
  Then the same drill-down is re-projected onto volume without needing to re-ask the question

Scenario: A state price is the nearest available reference.
  Given Texas has a sourced price and no metro or compatible local price inputs cover Loving County
  When the Query user asks for the county price
  Then the answer identifies the price as the Texas reference and marks the county price unavailable

Scenario: A share of regional volume cannot establish a county price.
  Given a Query user sees a regional price of USD 10 per unit and the county has 10 percent of the regional population
  When the Query user asks for the county price
  Then the answer labels USD 10 per unit as the regional reference and the county price as unavailable
  When compatible county revenue of USD 240 and volume of 20 units are available for the same window
  Then the county estimate is USD 12 per unit and opens to the two local inputs

Scenario: A local competitor price remains visible while the comparison lacks a reliable match.
  Given a Query user has a sourced metro competitor forecast price of USD 10 per unit and the Brand A product match at that level is unresolved
  When they open the metro drill-down in Predict, Position and Simulate
  Then the local price opens to its source, and any regional reference is labeled with its region
  And the answer explains the missing match and withholds the local gap, index and dependent simulation figures
  And the narrative at each stage uses only numbers already shown for that stage and scope
  When the metro match is resolved, the aligned Brand A Hold price is USD 8 per unit and the required simulation inputs are available
  Then Hold shows a gap of USD 2 per unit and an index of 80, and the simulation narrative uses the resulting local candidate figures
```
