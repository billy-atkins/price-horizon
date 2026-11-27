---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/engineering-and-production-considerations.md
---

## Application Log Control

[`specs/application/product/logging-and-traceability.md § Logging and Traceability § Application Log`](/specs/application/product/logging-and-traceability.md#application-log) describes the application log itself: what it is, and why it is kept separate from an audit log or an answer's own lineage. Raising the application log's detail is the Control plane admin role's ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) own capability.

A Control plane admin can raise logging detail for their own business unit. When the increase takes effect, the admin sees its end time, 30 minutes later. At that time the unit returns to its applicable logging level. Continuing diagnostics beyond that deadline requires a fresh authorized request.

### Test Scenarios

```gherkin
Scenario: A diagnostic window keeps its deadline across a restart.
  Given a Control plane admin for North America Snacks raises its logging detail at 14:00 UTC and sees an end time of 14:30 UTC
  When PriceHorizon restarts at 14:20 UTC
  Then North America Snacks still receives the increased detail at 14:29 UTC and returns to its applicable level at 14:30 UTC
  And Europe Beverages keeps its own logging level throughout
```
