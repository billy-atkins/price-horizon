---
technical-specs:
  - specs/application/technical/identity-and-access.md
---

## Identity Federation

Access follows the customer's own identity system rather than a separate one PriceHorizon maintains. The installation federates with the customer's identity provider using OIDC or SAML, whichever the customer already runs, so integration adds no new login system for their users to learn and no new identity infrastructure for their team to stand up. Which business units a person can see and query is asserted by that same identity provider, a large customer's own layers of management, a leader working across several business units, another working inside just one, are reflected automatically rather than re-modeled inside PriceHorizon. Which roles a person holds is asserted through this same federation, Acme AI's own staff included, as `specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology` describes.

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

### Test Scenarios

```gherkin
Scenario: Access follows the customer's own identity provider, adding no new login.
  Given a customer already runs SAML as their identity provider
  When the installation federates with it
  Then a Query user signs in through that same identity provider
  And no separate PriceHorizon login is created for them

Scenario: Which business units a person can see is asserted by the customer's own identity provider.
  Given the customer's identity provider asserts that a person's access covers North America Snacks and Europe Beverages, and not APAC Confectionery
  When that person asks a question as a Query user
  Then they can query North America Snacks and Europe Beverages
  And they cannot query APAC Confectionery

Scenario: Which role a person holds is asserted through the same federation.
  Given the customer's identity provider asserts the Control plane admin role for a person in North America Snacks
  When that person signs in
  Then they hold Control plane admin access scoped to North America Snacks
  And no role is assigned inside PriceHorizon separately from that assertion
```
