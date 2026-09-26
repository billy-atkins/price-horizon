---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/evidence-and-accuracy-reporting.md
---

## Onboarding Verification

The same bulk view a Platform admin uses to tune the platform over time (`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`) also does the first real check right after onboarding. In the days right after onboarding, before even the shortest, one-month horizon has had a chance to elapse, there is nothing yet to check for accuracy, but a Platform admin can still confirm the integrations are actually producing driver signals and forecasts, with real evidence and confidence behind them, for the real questions being asked, before treating onboarding as done just because the integrations are connected.

### Test Scenarios

```gherkin
Scenario: A Platform admin checks a newly onboarded installation before any forecast's horizon has passed.
  Given an installation was recently onboarded and its integrations have started producing driver signals and forecasts for real questions
  When a Platform admin reviews the installation
  Then the Platform admin sees the driver signals being ingested and the forecasts being produced, with their evidence and confidence
  And this check does not require any forecast's horizon to have passed yet
```
