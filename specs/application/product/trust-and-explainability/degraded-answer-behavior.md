---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Degraded Answer Behavior

If the system cannot complete a forecast at all once retries are exhausted, the system says so plainly. No forecast is shown. The answer shows instead that a forecast could not be computed, and the Query user is told to try again.

If the forecast completes but positioning cannot, the forecast, its confidence, and its rationale are still shown, clearly labeled as missing Position and Simulate. If the forecast and positioning both complete but simulation cannot, the forecast and the positioning options are still shown, clearly labeled as missing Simulate.

When narrative generation exhausts its retries, the Query user receives the completed stages as labeled figures with their evidence. Each missing stage is identified. Only figures computed for this answer are shown. The retained delivery preserves the fallback text and the results as displayed.

[`specs/application/product/architecture.md § Diagrams § When an Answer Falls Short`](/specs/application/product/architecture.md#when-an-answer-falls-short) renders this.

### Test Scenarios

```gherkin
Scenario: A forecast that cannot be computed at all is reported honestly, not silently backfilled.
  Given the system cannot compute Competitor Brand's effective price forecast in Texas in 6 months after exhausting its retries
  When a Query user asks the question
  Then the answer states that a forecast could not be computed
  And no stale or placeholder figure is shown in its place
  And the Query user is told to try again

Scenario: A completed forecast is still shown even when positioning cannot be completed.
  Given Competitor Brand's effective price forecast in Texas in 6 months has been computed, but positioning cannot be completed after exhausting its retries
  When a Query user asks the question
  Then the answer shows the completed forecast, its confidence score, and its rationale
  And the answer is clearly labeled as missing Position and Simulate

Scenario: A completed forecast and positioning are still shown even when simulation cannot be completed.
  Given Competitor Brand's effective price forecast and positioning options in Texas in 6 months have both been computed, but simulation cannot be completed after exhausting its retries
  When a Query user asks the question
  Then the answer shows the completed forecast and positioning options
  And the answer is clearly labeled as missing Simulate

Scenario: Narrative failure leaves the completed figures and their evidence available.
  Given Predict, Position and Simulate have completed for a North America Snacks Query user
  When narrative generation exhausts its retries
  Then the user sees the labeled forecast, confidence, options and simulated outcomes and can open the evidence behind their figures
  And the unit’s Control plane admin reopening that delivery sees the same fallback text and figures
```
