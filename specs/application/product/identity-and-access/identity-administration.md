---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/identity-and-access.md
---

## Identity Administration

The Identity admin grants, corrects or withdraws access by mapping the customer’s identity claims to PriceHorizon business units and roles. On each question PriceHorizon combines the grants from all current mappings for the person’s asserted claims. An unmapped claim supplies no grant.

[`specs/application/product/architecture.md § Diagrams § Using and Administering`](/specs/application/product/architecture.md#using-and-administering) renders this.

### Test Scenarios

```gherkin
Scenario: Adding a claim mapping grants the business unit and role it names.
  Given an Identity admin adds a mapping from the customer's IdP group claim "NA-Snacks-Users" to the North America Snacks business unit and the Query user role
  When a person asserting that claim next asks a question
  Then they are granted Query user access scoped to North America Snacks

Scenario: Correcting a mapping changes access on the next question.
  Given a person’s only asserted group grants Query user access to North America Snacks
  When the Identity admin corrects its mapping to Europe Beverages and the person next asks a question with the same claim
  Then they can query Europe Beverages and have no access to North America Snacks

Scenario: Removing one mapping preserves independent grants.
  Given a person asserts two groups granting Query user access to North America Snacks and Europe Beverages respectively
  When the Identity admin removes the North America Snacks mapping and the person next asks a question
  Then they retain access to Europe Beverages and have no access to North America Snacks

Scenario: An unmapped claim grants no access.
  Given no Identity admin has mapped the customer's IdP group claim "APAC-Users" to any business unit or role
  When a person whose only asserted group is "APAC-Users" asks a question
  Then they are granted no access on PriceHorizon
```
