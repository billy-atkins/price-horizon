---
technical-specs:
  - specs/application/technical/engineering-and-production-considerations.md
---

## Application Log Control

The application log itself, what it is and why it is kept separate from an audit log or an answer's own lineage, is `specs/application/product/logging-and-traceability.md § Logging and Traceability § Application Log`; this is the Control plane admin role's (`specs/application/product/roles.md § Roles`) own capability to raise its detail.

A Control plane admin can temporarily increase how much detail PriceHorizon's application logs capture for their business unit, without needing to ask first, when they're experiencing an issue and want it resolved faster; it reverts automatically rather than staying on indefinitely.

### Test Scenarios

```gherkin
Scenario: A Control plane admin can temporarily increase logging detail for their own business unit without asking first.
  Given a Control plane admin for North America Snacks is experiencing an issue they want resolved faster
  When they raise the application log level for North America Snacks
  Then PriceHorizon's application logs capture more detail for North America Snacks' own traffic
  And the elevated level reverts automatically after a bounded window, not staying on indefinitely
```
