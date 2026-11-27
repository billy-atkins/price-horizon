---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/glossary-and-grounding.md
  - specs/application/technical/identity-and-access.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/materialization-service/reconciliation.md
  - specs/application/technical/model-registry.md
---

## Reference Data Management

The Control plane admin role ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) manages the day-to-day realities Acme AI should not need to be paged for:
- Registering a new business unit when the client has granted the separate installation-level creation permission.
- Retiring a competitor no longer worth tracking.
- Renaming a competitor for every brand tracked in this unit while preserving its pricing history.
- Registering an incoming code for an existing geography. The registration applies to future observations from that source in the admin's business unit. Registering the same mapping again preserves it. If the code already identifies a different geography for that unit and source, PriceHorizon rejects the correction and keeps the original mapping. Earlier answers keep their original geography.
- Registering the business unit's own alternate phrasing for an already-established term in PriceHorizon's governed vocabulary, such as effective price. The business unit's analysts' internal jargon then resolves the same way the term's canonical phrasing already does.

Registering a unit grants its creator no access to its data or administration. Retirement takes effect for a unit when its first complete forecast publication excludes the competitor. Until then, including after a failed refresh, new requests still use that unit's current published membership. Historical deliveries remain available by identifier.

The underlying mechanism stays with Acme AI: the archetype price-setting rules, the model versions, the weighting rubrics behind every forecast, and the governed vocabulary itself. The mechanism changes only through an application or model release. The day-to-day facts stay with the business unit: who competes with whom, and what the business unit's own analysts happen to call something they already track.

### Test Scenarios

```gherkin
Scenario: Adding a business unit is a self-service action.
  Given a client Control plane admin authorized to create business units registers a new business unit, North America Snacks
  When the addition is complete
  Then North America Snacks exists on the installation as its own business unit, available for further configuration
  And no Acme AI involvement was required

Scenario: Retiring a competitor removes them from future forecasts.
  Given a Control plane admin retires Northern Rival, a competitor no longer worth tracking
  When the retirement is complete
  Then Northern Rival is no longer included in future forecasts

Scenario: Recording a rebrand preserves the competitor's pricing history.
  Given West’s Control plane admin manages two brands of Northern Rival and East tracks the same competitor
  When West’s Control plane admin renames Northern Rival to Northern Group
  Then new West answers show Northern Group for both brands and retain the competitor’s pricing history
  And East keeps its previous label and configuration version
  And the rename appears in West’s audit history and earlier deliveries keep their original wording

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

Scenario: A creator can register a business unit without gaining access.
  Given a client Control plane admin can administer East and lacks installation-level creation permission
  Then a request to register West is denied
  When the same admin with explicit creation permission successfully registers West
  Then West exists and the creation is auditable
  And the creator cannot read or administer West through that action
  When an Identity admin explicitly grants query access to West
  Then the creator can query West and still lacks administrative access there

Scenario: A failed refresh leaves a retirement pending for the business unit.
  Given the unit’s Control plane admin requests retirement of a competitor in its current publication
  When the first refresh fails before it can publish a complete replacement
  Then new requests still select the competitor from the preceding publication
  When the next complete publication excluding the competitor becomes current
  Then a new request cannot select it or compute a forecast for it outside the grid
  And the earlier delivery remains retrievable by its original identifier

Scenario: Two units correct the same source code independently.
  Given a Control plane admin for North America Snacks registers METRO from its vendor for Dallas
  And a Control plane admin for South America Snacks registers METRO from the same vendor for São Paulo
  When each unit receives a new observation using that code
  Then North America Snacks sees the observation for Dallas and South America Snacks sees its observation for São Paulo
  And reopening a delivery made before either correction shows its original geography
  When the North America Snacks admin repeats the Dallas registration for the same vendor and code
  Then the existing mapping remains in effect and a new observation still resolves to Dallas
  When the North America Snacks admin attempts to register METRO from that vendor for Boston
  Then the conflicting correction is rejected and the North America Snacks mapping still resolves to Dallas
```
