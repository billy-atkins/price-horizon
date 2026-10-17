---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/evidence-and-accuracy-reporting.md
---

## Onboarding Verification

A Platform admin tunes the platform over time from a bulk view ([`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy)). The same view also does the first real check right after onboarding. In those first days, even the shortest horizon, one month, has not yet elapsed, so there is no accuracy to check. A Platform admin can still confirm that the integrations are producing driver signals and forecasts for the real questions being asked, with real evidence and confidence behind them, before treating onboarding as done. Connected integrations alone do not show that it is.

### Test Scenarios

```gherkin
Scenario: A Platform admin checks a newly onboarded installation before any forecast's horizon has passed.
  Given an installation was recently onboarded and its integrations have started producing driver signals and forecasts for real questions
  When a Platform admin reviews the installation
  Then the Platform admin sees the driver signals being ingested and the forecasts being produced, with their evidence and confidence
  And this check does not require any forecast's horizon to have passed yet
```
