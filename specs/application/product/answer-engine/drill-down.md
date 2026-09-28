---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Drill-down — cross-cutting, available at every stage

Independent axes, and a user can move along either one without leaving the analysis:

- **Granularity —** country to state or province to major metro, matching how the competitor's own pricing data is actually reported.

| Granularity | Figure shown | Decomposition graph |
|---|---|---|
| Within that range (country, state or province, major metro) | The same analysis re-run at a narrower filter, guaranteed consistent with the broader figure it was drilled from | Available |
| Below that range (county, store) | An allocation of the major metro number, or the state's where no metro is reported, labeled as an estimate, not shown with the confidence of a directly sourced forecast, and opening to the forecast it was allocated from and the weighting used, population or retail footprint | Not available, an allocated figure has no causal story of its own to tell |

That boundary reflects which competitor data is currently licensed and ingested, not a permanent limit, a more granular data source would move it.
- **Metric —** price is the default lens, but a user can pivot the same drill-down to volume, margin, or share without re-asking the question.

The narrative layer's job throughout every stage (`specs/application/product/answer-engine/predict.md § Predict — what will the competitor do`, `specs/application/product/answer-engine/position.md § Position — where Brand A should sit`, `specs/application/product/answer-engine/simulate.md § Simulate — what follows for the business`) is fluent explanation of numbers that already exist, not generation of new ones. That distinction is what keeps the answer defensible in front of a retailer or a CFO.

`specs/application/product/architecture.md § Diagrams § The Answer` renders this.

### Test Scenarios

```gherkin
Scenario: Drilling down within the licensed range stays consistent and keeps the decomposition graph.
  Given a Query user has an existing Predict answer for Competitor Brand's effective price in Texas in 6 months, at the state or province granularity
  When the Query user drills down to major metro, within that same licensed range
  Then the answer is re-run at major metro granularity and is guaranteed consistent with the state-or-province figure it was drilled from
  And the decomposition graph remains available

Scenario: Drilling down below the licensed range produces a labeled allocation, not a sourced forecast.
  Given a Query user has an existing Predict answer for Competitor Brand's effective price in Texas in 6 months, at major metro, the most granular level the competitor's own pricing data supports
  When the Query user drills down below major metro, to a county or store
  Then the figure shown is an allocation of the major metro number, labeled as an estimate, not shown with the confidence of a directly sourced forecast
  And opening the figure shows the major metro forecast it was allocated from and the weighting used
  And the decomposition graph is not available

Scenario: Pivoting the metric does not require re-asking the question.
  Given a Query user has an existing Predict answer for Competitor Brand's effective price in Texas in 6 months
  When the Query user pivots the metric from price to volume
  Then the same drill-down is re-projected onto volume without needing to re-ask the question

Scenario: Where no major metro is reported, an allocation comes from the state.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months, and Competitor Brand's own pricing data reports no major metro containing Loving County
  When the Query user drills down to Loving County
  Then the figure shown is an allocation of the Texas number, labeled as an estimate
  And opening the figure shows the Texas forecast it was allocated from and the weighting used
```
