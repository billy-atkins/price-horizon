---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/evidence-and-accuracy-reporting.md
---

## Onboarding Verification

A Platform admin checks onboarding in the bulk view ([`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy)). A published forecast with its evidence and confidence verifies forecast production. A committed answer verifies that the service prepared a response. A receipt verifies client use only when it matches the authenticated recipient, unit, question and committed delivery. Repeated acknowledgements for the same delivery count once. The admin can confirm both before comparable actual prices exist.

### Test Scenarios

```gherkin
Scenario: Publication verifies forecast production and authenticated receipt verifies use.
  Given a recently onboarded business unit has published a forecast with signal evidence and confidence
  When the Platform admin inspects it before any question has been answered
  Then the forecast verifies production and the fully retained interval has no committed answers or receipts
  When a Query user asks for that forecast and the service commits the answer
  Then the report shows one prepared answer and zero confirmed receipts
  When the intended user’s authenticated client receives the answer and acknowledges that unit, question and delivery
  Then the first matching receipt verifies use while the forecast still awaits comparable actual prices

Scenario: A gap in retention limits the onboarding evidence.
  Given a published forecast has no linked deliveries remaining for a partly purged interval
  When the Platform admin reviews that interval
  Then the report states the certified period for committed answers and for confirmed receipts, and labels each incomplete count as retained only

Scenario: A disconnected client leaves a committed answer unconfirmed.
  Given a forecast-bearing answer has committed for the unit and the client disconnects before receipt
  When a Platform admin inspects the fully retained question interval
  Then the report shows one committed answer and zero confirmed receipts
  When the same authenticated client receives the answer and acknowledges that delivery twice
  Then the report shows one committed answer and one confirmed receipt
  And an acknowledgement for a different question or unit cannot confirm the delivery
```
