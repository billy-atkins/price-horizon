---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/evidence-and-accuracy-reporting.md
---

## Tracking Forecast Accuracy

Each forecast shows the dates it predicts and where its evidence came from. A forecast is pending until its observation period ends and complete comparable prices arrive. If its original comparison terms cannot be recovered, the report explains why it cannot be evaluated. Each scored forecast contributes once to the pattern of model accuracy, however many people received it.

Once comparable actuals are available, the report shows the signed error and judges the observed move against the forecast's original band, direction and stable-price threshold. Both ends of the band count as inside. Outside the band, an unchanged price is stable. A nonzero move from a zero starting price has no percentage direction. Later settings changes leave the original judgment intact.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Observed move inside original band?, Observed direction relative to forecast \
**Input Values:**
  - Observed direction relative to forecast: "matches", "differs", "undefined"

| Observed move inside original band? | Observed direction relative to forecast | What the report shows |
|---|---|---|
| true | - | Right |
| false | "matches" | Right direction |
| false | "differs" | Wrong |
| false | "undefined" | No verdict. The report explains that the zero starting price prevents a direction comparison. |

A Platform admin sees the forecasts across the installation, the driver signals each used, and any recorded verdict and signed error. Retained delivery counts show usage over the selected dates. The report identifies gaps when audit retention covers only part of that period.

The pattern across every business unit, not just one, is the feedback Acme AI tunes the platform's archetype rules, model versions, and weighting rubrics against. Acme AI delivers that tuning through the next application or model release. The pattern is diagnostic input to that engineering work. It is not a conversation with any Query user. [`specs/application/product/identity-and-access/using-and-administering-kept-apart.md § Using and Administering Kept Apart`](/specs/application/product/identity-and-access/using-and-administering-kept-apart.md#using-and-administering-kept-apart) keeps the same separation between using the product and administering it.

A Control plane admin sees the same forecasts, signals and accuracy within their own business unit. To raise a particular prediction with a Query user, the admin selects the retained question and its committed forecast, and sees whether the client confirmed receipt. The report distinguishes committed and confirmed counts over the same cohort and identifies the retained coverage of each. A scheduled forecast can appear here even when nobody has received it.

Sometimes a Control plane admin's review points to something that looks like the platform itself rather than their own business unit. That review lands in the same accuracy view: a Platform admin looks at that business unit's own records inside the view the Platform admin already has. These are the same underlying facts the Control plane admin was looking at, rather than a secondhand description of them.

[`specs/application/product/architecture.md § Diagrams § Using and Administering`](/specs/application/product/architecture.md#using-and-administering) renders this.

### Test Scenarios

```gherkin
Scenario: A Control plane admin distinguishes missing prices from an ambiguous forecast period.
  Given one forecast for the unit covers September and its price observations stop on September 29
  And an older forecast has its original comparison terms but no evidence identifying a single target interval
  When the Control plane admin opens the report after September ends
  Then the September forecast is pending because comparable observations are incomplete
  And the older forecast is unevaluable because its original target window cannot be resolved
  And neither forecast has a verdict
Scenario: A forecast is checked against what actually happened once its horizon passes.
  Given a forecast for Competitor Brand's effective price in Texas at a 6-month horizon
  When that 6-month horizon passes and Competitor Brand's actual effective price in Texas is observed
  Then the forecast is checked against that actual price

Scenario: A forecast whose actual price lands inside its confidence band is Right.
  Given a forecast that Competitor Brand's effective price in Texas will rise 3% in 6 months, with a confidence band of a 2% to 4% rise
  When the horizon passes and Competitor Brand's actual effective price in Texas has risen 2.5%
  Then the forecast's verdict is Right
  And how far off it was is shown alongside

Scenario: A forecast that missed its band but called the direction is Right direction.
  Given a forecast that Competitor Brand's effective price in Texas will rise 3% in 6 months, with a confidence band of a 2% to 4% rise
  When the horizon passes and the actual price has risen 6%
  Then the forecast's verdict is Right direction

Scenario: A forecast that missed its band and the direction is Wrong.
  Given a forecast that Competitor Brand's effective price in Texas will rise 3% in 6 months, with a confidence band of a 2% to 4% rise
  When the horizon passes and the actual price has fallen 1%
  Then the forecast's verdict is Wrong

Scenario: A forecast of a stable price is Right direction when the price leaves its band but stays within the stable-price threshold.
  Given North America Snacks' stable-price threshold is 0.5% of today's price, and a forecast that Competitor Brand's effective price in Texas will stay stable over 6 months, with a confidence band of a 0.2% fall to a 0.2% rise
  When the horizon passes and the actual price has risen 0.4%
  Then the forecast's verdict is Right direction

Scenario: A forecast is judged by the stable-price threshold in effect when it was made.
  Given North America Snacks' stable-price threshold was 0.5% of today's price when a forecast that Competitor Brand's effective price in Texas will rise 2% in 6 months was made, with a confidence band of a 1.5% to 2.5% rise
  And a Control plane admin for North America Snacks has since raised the stable-price threshold to 1% of today's price
  When the horizon passes and the actual price has risen 0.8%
  Then the forecast's verdict is Right direction

Scenario: Checking a forecast against what happened tracks model drift, not the executive's past decision.
  Given a forecast for Competitor Brand's effective price in Texas at a 6-month horizon has been checked against the actual price once the horizon passed
  When that check finds a difference between the forecast and the actual price
  Then the difference is tracked as a signal of whether the underlying models are drifting
  And no grade or flag is attached to the answer the executive already acted on

Scenario: A Platform admin reviews evidence and accuracy in bulk across every business unit an installation hosts.
  Given a Platform admin has a September forecast for North America Snacks that used a Texas tax filing and a September forecast for Europe Beverages that used a German input-cost bulletin
  And the Texas price move is inside its forecast band while the German forecast still lacks complete comparable prices
  When the admin opens the installation’s September forecast report
  Then the North America Snacks row shows the Texas filing and the verdict Right
  And the Europe Beverages row shows the German bulletin and a pending comparison because the prices are incomplete

Scenario: A Control plane admin's escalation gives a Platform admin the same business unit's evidence.
  Given a Control plane admin reviewing North America Snacks in bulk suspects the platform itself, not their own business unit, is behind a pattern they are seeing
  When the Control plane admin escalates to a Platform admin
  Then the Platform admin looks at North America Snacks' own evidence and accuracy inside the view they already have, the same records the Control plane admin was looking at

Scenario: A Control plane admin reviews forecast evidence and accuracy in bulk for their own business unit.
  Given the Control plane admin for North America Snacks has forecasts and driver signals to review, including forecasts whose horizons have passed
  When a Control plane admin reviews North America Snacks in bulk
  Then the Control plane admin sees the unit’s driver signals and forecasts, with each recorded verdict or reason a verdict is unavailable
  And this view is not limited to a single forecast
Scenario: A Control plane admin follows up on one delivery of a reused forecast.
  Given the Control plane admin for North America Snacks can see deliveries of the same scheduled forecast to its Query users Maya and Luis
  And another forecast has no deliveries during the fully retained interval
  When their Control plane admin opens Luis’s delivery in the report
  Then the report shows two forecasts with delivery counts of two and zero
  And the admin can identify Luis’s question and raise that prediction with Luis
  And the detail contains only activity for North America Snacks

Scenario: A zero starting price can yield a known error without a verdict.
  Given a Control plane admin has two retained forecasts with a starting price of zero and a predicted move of 2
  And the original band for each move is 1 to 3 in local currency per unit
  When comparable actuals show moves of 2 and 4 respectively
  Then the first forecast is Right with signed error zero
  And the second has signed error −2 and explains that the zero starting price prevents a direction verdict

Scenario: Receipt status follows the selected delivery.
  Given a Control plane admin sees two committed deliveries of the same forecast in the unit
  And the client has acknowledged only the first delivery
  When the Control plane admin opens the second delivery
  Then its receipt is unconfirmed
  When the client acknowledges that delivery and the Control plane admin opens it again
  Then the second delivery shows confirmed receipt
```
