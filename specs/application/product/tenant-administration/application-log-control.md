---
technical-specs:
  - specs/application/technical/engineering-and-production-considerations.md
---

## Application Log Control

[`specs/application/product/logging-and-traceability.md § Logging and Traceability § Application Log`](/specs/application/product/logging-and-traceability.md#application-log) describes the application log itself: what it is, and why it is kept separate from an audit log or an answer's own lineage. Raising the application log's detail is the Control plane admin role's ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) own capability.

When a Control plane admin is experiencing an issue and wants it resolved faster, the admin can temporarily increase how much detail PriceHorizon's application logs capture for their business unit, without needing to ask first. The increase reverts automatically rather than staying on indefinitely.

### Test Scenarios

```gherkin
Scenario: A Control plane admin can temporarily increase logging detail for their own business unit without asking first.
  Given a Control plane admin for North America Snacks is experiencing an issue they want resolved faster
  When they raise the application log level for North America Snacks
  Then PriceHorizon's application logs capture more detail for North America Snacks' own traffic
  And the elevated level reverts automatically after a bounded window, not staying on indefinitely
```
