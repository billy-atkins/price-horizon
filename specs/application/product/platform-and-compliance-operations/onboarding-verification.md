---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/evidence-and-accuracy-reporting.md
---

## Onboarding Verification

A Platform admin checks onboarding in the bulk view ([`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy)). A published forecast with its evidence and confidence verifies forecast production. A retained question linked to the delivered forecast verifies that someone received an answer. The admin can confirm both before comparable actual prices exist.

### Test Scenarios

```gherkin
Scenario: A scheduled forecast verifies production and its first delivery verifies use.
  Given a recently onboarded business unit has published a forecast with signal evidence and confidence
  When the Platform admin inspects it before any question has been answered
  Then the forecast verifies production and the report shows no deliveries in the fully retained interval
  When a Query user receives that forecast in an answer
  Then its retained delivery verifies use while the forecast is still pending

Scenario: A gap in retention limits the onboarding evidence.
  Given a published forecast has no linked deliveries remaining for a partly purged interval
  When the Platform admin reviews that interval
  Then the report labels the delivery count as retained only and identifies the gap
```
