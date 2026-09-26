---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/glossary-and-grounding.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/model-registry.md
---

## Reference Data Management

The Control plane admin role (`specs/application/product/roles.md § Roles`) manages the day-to-day realities Acme AI should not need to be paged for: adding a business unit, retiring a competitor no longer worth tracking, recording a competitor's rebrand without losing the pricing history attached to who they used to be, and registering the business unit's own alternate phrasing for an already-established term in PriceHorizon's own governed vocabulary, effective price for instance, so their own analysts' internal jargon resolves the same way the term's own canonical phrasing already does. What stays with Acme AI is the underlying mechanism, the archetype price-setting rules, the model versions, the weighting rubrics behind every forecast, and the governed vocabulary itself, changed only through an application or model release, not the day-to-day facts about who competes with whom or what a business unit's own analysts happen to call something they already track.

### Test Scenarios

```gherkin
Scenario: Adding a business unit is a self-service action.
  Given a Control plane admin adds a new business unit, North America Snacks
  When the addition is complete
  Then North America Snacks exists on the installation as its own business unit, available for further configuration
  And no Acme AI involvement was required

Scenario: Retiring a competitor removes them from future forecasts.
  Given a Control plane admin retires Northern Rival, a competitor no longer worth tracking
  When the retirement is complete
  Then Northern Rival is no longer included in future forecasts

Scenario: Recording a rebrand preserves the competitor's pricing history.
  Given a Control plane admin records that Northern Rival has rebranded to Northern Group
  When the rebrand is recorded
  Then the pricing history attached to Northern Rival is preserved under Northern Group, not lost

Scenario: Self-service configuration stops at facts, not the forecasting mechanism itself.
  Given a Control plane admin has full self-service access to their own business unit's configuration
  When the archetype price-setting rules or a model's weighting rubric would need to change
  Then that change happens only through an application or model release, not as a self-service action

Scenario: Registering a glossary alias makes a business unit's own phrasing resolve.
  Given a Control plane admin registers "net price" as North America Snacks' own alias for the governed term effective price
  When a Query user in North America Snacks asks about Competitor Brand's net price
  Then the question resolves the same way it would if "effective price" had been asked instead

Scenario: A glossary alias can only be registered for an already-established term.
  Given a Control plane admin wants an alias registered for "shelf multiplier," a term PriceHorizon's own governed vocabulary does not already define
  When that request is made
  Then it is not possible as a self-service action, the same way a genuinely new governed term is never self-service
```
