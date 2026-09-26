---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Business Unit Settings

A Control plane admin (`specs/application/product/roles.md § Roles`) sets how their own business unit's answers come out, without Acme AI being paged for it, each threshold within bounds Acme AI provides as defaults. The stable-price threshold is how small a forecast move, as a share of today's price, has to be before the competitor's price is called stable rather than moving; the same threshold decides when evidence disagreeing with the forecast's baseline is big enough to be flagged as a disagreement that holds the confidence score down, rather than only entering the forecast through its driver's correction. The materiality thresholds are how close two positioning options next to each other in price have to be, on each measure the answer shows for them, each measure with its own threshold, before they are shown as one, the consolidation `specs/application/product/answer-engine/position.md § Position — where Brand A should sit` promises. The admin can also rename how the positioning options are labeled for their own analysts, without changing the rule each one stands for.

A change to the materiality thresholds or the labels reaches the business unit's very next answer, since positioning is worked out when a question is asked, and so does a change to the stable-price threshold for a forecast built when asked, outside the standard horizons. A scheduled forecast picks up a stable-price threshold change only when it is next computed, so the admin can ask for the business unit's scheduled forecasts to be computed again rather than waiting for the next run the schedule or a data refresh would start. Changes to these settings appear in the business unit's own audit record (`specs/application/product/tenant-administration/audit-log-visibility.md § Audit Log Visibility`). The forecasting mechanism these settings tune stays with Acme AI, as `specs/application/product/tenant-administration/reference-data-management.md § Reference Data Management` describes, and each business unit's settings are its own, per `specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`.

### Test Scenarios

```gherkin
Scenario: A stable-price threshold change waits for a scheduled forecast's next computation.
  Given Competitor Brand's scheduled forecast for Texas in 6 months shows a 0.8% move as an increase
  And a Control plane admin for North America Snacks has since raised the stable-price threshold from 0.5% to 1% of today's price
  When a Query user in North America Snacks asks where Competitor Brand's effective price will be in Texas in 6 months, before that forecast is computed again
  Then the answer still shows the 0.8% move as an increase

Scenario: Computing scheduled forecasts again applies a stable-price threshold change.
  Given a Control plane admin for North America Snacks has raised the stable-price threshold from 0.5% to 1% of today's price
  And Competitor Brand's scheduled forecast for Texas in 6 months shows a 0.8% move as an increase, with the data behind it unchanged since
  When the admin asks for North America Snacks' scheduled forecasts to be computed again, and that run completes
  Then that forecast shows Competitor Brand's price as stable

Scenario: A forecast built when asked applies a stable-price threshold change at once.
  Given a Control plane admin for North America Snacks has raised the stable-price threshold from 0.5% to 1% of today's price
  And Competitor Brand's forecast for Texas in 9 months, outside the standard horizons, points to a 0.8% move
  When a Query user in North America Snacks asks where Competitor Brand's effective price will be in Texas in 9 months
  Then the answer shows Competitor Brand's price as stable

Scenario: Disagreeing evidence below the stable-price threshold enters the forecast without being flagged.
  Given North America Snacks' stable-price threshold has been 1% of today's price since before Competitor Brand's forecast for Texas in 6 months was last computed
  And Competitor Brand's baseline in Texas for the next 6 months is stable
  And a documented tax increase taking effect within those 6 months contributes a correction of 0.7% of today's price
  When a Query user in North America Snacks asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the tax increase's correction is part of the forecast
  And it is not flagged as a disagreement holding the confidence score down

Scenario: A materiality threshold change reaches the next answer.
  Given a Control plane admin for North America Snacks raises the materiality threshold for simulated share from 0.5 to 1 point
  And Close the Gap and Match, next to each other in price, would differ by 0.8 points of simulated share and by less than their thresholds on every other measure
  And Hold and Close the Gap would differ by 1.5 points of simulated share
  When a Query user in North America Snacks next asks where Competitor Brand's effective price will be in Texas in 6 months
  Then Close the Gap and Match are shown as one option

Scenario: A threshold cannot be set outside the bounds Acme AI provides.
  Given Acme AI's default bounds allow North America Snacks' materiality threshold for simulated share to be no more than 2 points
  When a Control plane admin for North America Snacks tries to set it to 3 points
  Then the change is refused
  And the threshold stays at its previous value

Scenario: Renaming an option's label leaves the rule behind it unchanged.
  Given a Control plane admin for North America Snacks renames the Close the Gap option to "Narrow the Spread" for their own analysts
  When a Query user in North America Snacks asks where Competitor Brand's effective price will be in Texas in 6 months and receives positioning options
  Then the option appears as "Narrow the Spread"
  And its price still splits the difference between Hold and Match, as Close the Gap does
```
