---
technical-specs:
  - specs/application/technical/identity-and-access.md
---

## Identity Administration

The Identity admin role manages the mapping between the customer's own identity system and PriceHorizon's business units and roles. Adding or correcting a mapping is what grants a person the access it names; before a mapping exists, the claim exists on the customer's side but grants nothing on PriceHorizon's.

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

### Test Scenarios

```gherkin
Scenario: Adding a claim mapping grants the business unit and role it names.
  Given an Identity admin adds a mapping from the customer's IdP group claim "NA-Snacks-Users" to the North America Snacks business unit and the Query user role
  When a person asserting that claim next asks a question
  Then they are granted Query user access scoped to North America Snacks

Scenario: An unmapped claim grants no access.
  Given no Identity admin has mapped the customer's IdP group claim "APAC-Users" to any business unit or role
  When a person asserting that claim asks a question
  Then they are granted no access on PriceHorizon
```
