---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/identity-and-access.md
---

## Roles

PriceHorizon defines these roles, distinguishing everyday use from administration:

| Role | Description |
|---|---|
| Query user | Everyday use, asking questions and exploring the answer experience, scoped to whichever business units the person's identity grants |
| Control plane admin | Manages a business unit's own configuration, reference data, thresholds, and review queues, reviews forecast evidence and accuracy in bulk for that business unit, sees its audit log, Acme AI's own access included (`specs/application/product/tenant-administration/audit-log-visibility.md § Audit Log Visibility`), and can temporarily raise PriceHorizon's application logging detail for it (`specs/application/product/tenant-administration/application-log-control.md § Application Log Control`), scoped to that business unit alone, and can see which application and model versions the installation as a whole currently runs (`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades`) |
| Identity admin | Manages the mapping between the customer's own identity system and PriceHorizon's business units and roles, and sees the record of every change to it, not scoped to any single business unit, since a mistake here could affect access across all of them |
| Platform admin | Acme AI's own staff, onboarding an installation, executing an Acme AI-managed upgrade for a customer (a self-managed upgrade's own execution is described in `specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades` instead), diagnostic support access, seeing which application and model versions an installation currently runs (`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades`), and reviewing evidence and forecast accuracy in bulk across every business unit an installation hosts to tune the platform, never the client's business configuration itself |

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

### Identity Federation

Access follows the customer's own identity system rather than a separate one PriceHorizon maintains. The installation federates with the customer's identity provider using OIDC or SAML, whichever the customer already runs, so integration adds no new login system for their users to learn and no new identity infrastructure for their team to stand up. Which business units a person can see and query is asserted by that same identity provider, a large customer's own layers of management, a leader working across several business units, another working inside just one, are reflected automatically rather than re-modeled inside PriceHorizon. Which of the roles above a person holds is asserted through this same federation, Acme AI's own staff included, as `specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology` describes.

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

#### Test Scenarios

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

### Identity Administration

The Identity admin role manages the mapping between the customer's own identity system and PriceHorizon's business units and roles. Adding or correcting a mapping is what grants a person the access it names; before a mapping exists, the claim exists on the customer's side but grants nothing on PriceHorizon's.

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

#### Test Scenarios

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
