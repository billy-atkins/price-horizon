---
technical-specs:
  - specs/application/technical/identity-and-access.md
---

## Identity Federation

Access follows the customer's own identity system rather than a separate one PriceHorizon maintains. The installation federates with the customer's identity provider using OIDC or SAML, whichever the customer already runs. So integration adds no new login system for the customer's users to learn, and no new identity infrastructure for the customer's team to stand up.

The provider authenticates the person and supplies their claims. PriceHorizon uses the Identity admin’s current mappings to determine which roles and business units those claims grant. A person who works across units receives the combined grants. Federated Acme AI support also requires installation support permission, as [`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology) describes.

[`specs/application/product/architecture.md § Diagrams § Using and Administering`](/specs/application/product/architecture.md#using-and-administering) renders this.

### Test Scenarios

```gherkin
Scenario: Access follows the customer's own identity provider, adding no new login.
  Given a customer already runs SAML as their identity provider
  When the installation federates with it
  Then a Query user signs in through that same identity provider
  And no separate PriceHorizon login is created for them

Scenario: Two mapped groups grant access across business units.
  Given the provider asserts two groups mapped to Query user access in North America Snacks and Europe Beverages
  When the person asks a question
  Then they can query both units and cannot query APAC Confectionery

Scenario: An authenticated administrator receives the role in the current mapping.
  Given the provider authenticates a person and asserts a group mapped to Control plane admin for North America Snacks
  When the person opens the control plane
  Then they have that role in North America Snacks
  And authenticating with only unmapped claims grants no role
```
