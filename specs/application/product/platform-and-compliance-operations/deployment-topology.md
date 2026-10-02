---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/identity-and-access.md
  - specs/application/technical/model-registry.md
  - specs/application/technical/secrets-management.md
---

## Deployment Topology

PriceHorizon deploys as a versioned, self-hosted installation inside each customer's own environment, co-located with their data. Competitor pricing intelligence and a brand's own internal pricing and margin data both carry real competitive sensitivity, and keeping that data inside the customer's own infrastructure, rather than in a shared service spanning multiple customers, is the primary protection against it ever leaving their control. An installation signs people in through the customer's own identity provider, which sits inside that same environment, and runs entirely within the customer's security boundary, needing no connection outside it unless the client lets some kinds of model call reach a frontier model provider (`§ Deployment Topology § Frontier Models`), and air-gapped where the customer requires. Acme AI, as the technology and service provider, retains the access needed to support, monitor, and upgrade each installation, governed by access control and audit logging rather than by being cut off from the data; the full capability, a client's own view of that access, is `specs/application/product/tenant-administration/audit-log-visibility.md`.

That access is the Platform admin role, per `specs/application/product/roles.md § Roles`, and it stays inside the customer's environment on either of its paths: ordinarily, accounts the client provisions and controls directly for named Acme AI staff in its own identity provider, so revocation never depends on Acme AI's cooperation; or, only where that identity provider cannot be reached, break-glass credentials held in the installation's own isolated vault. Whichever path is used, the client can disable this access entirely at any time from their own side. A client raises a support case through Acme AI's own support portal, which PriceHorizon never connects to.

Wherever PriceHorizon itself holds a credential, Acme AI's own break-glass access, the secret behind a federated identity integration, or a client's own data source connection provided through the self-service control plane (`specs/application/product/tenant-administration/data-source-connections.md § Data Source Connections`), it lives in an isolated, access-controlled vault, never in the same database as the installation's own configuration or reference data, so a vulnerability in ordinary application data can never expose the credentials that protect it.

Configuration is scoped to the business unit, not the customer as a whole. A single installation can host several business units side by side, each with its own brand, competitor set, category, and geography, since a large customer is rarely one competitive picture. Each business unit keeps its own glossary terms and thresholds without needing a separate installation. Day-to-day configuration, adding a business unit, retiring a competitor, reviewing a flagged case, is the client's own self-service surface, not something Acme AI should need to be paged for; the full capability is `specs/application/product/tenant-administration/reference-data-management.md`, `specs/application/product/tenant-administration/business-unit-settings.md` and `specs/application/product/tenant-administration/review-queues.md`.

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.

### Test Scenarios

```gherkin
Scenario: Competitively sensitive data stays inside the customer's own environment.
  Given North America Snacks' installation holds competitor pricing intelligence and Brand A's own internal pricing and margin data
  And its configuration lets no kind of model call reach a frontier model provider
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then every piece of that data stays inside the customer's own infrastructure to answer it
  And none of it is held in a shared store spanning more than one customer

Scenario: A client can disable Acme AI's access entirely from their own side.
  Given Acme AI's Platform admin staff holds support and monitoring access to North America Snacks' installation
  When the client disables that access from their own side
  Then Acme AI's access to the installation ends
  And ending it does not require Acme AI's cooperation

Scenario: Two business units in one installation keep their own configuration.
  Given a single installation hosts North America Snacks and Europe Beverages, each with its own brand, competitor set, category, and geography
  When a Control plane admin for North America Snacks changes a materiality threshold for North America Snacks
  Then Europe Beverages' own thresholds are unchanged
  And Europe Beverages' own glossary terms are unchanged

Scenario: A credential lives in an isolated vault regardless of whose it is.
  Given Acme AI provisions its own break-glass credential for a client's installation, and that same client's Control plane admin separately provides credentials connecting ScanTrack, a new data source
  When both credentials are stored
  Then both live in the same isolated, access-controlled vault
  And neither is stored in the same database as the installation's own configuration or reference data

Scenario: An installation can run entirely inside the customer's security boundary.
  Given North America Snacks' installation runs air-gapped inside the customer's own environment
  When a Query user signs in
  Then they are signed in through the customer's own identity provider inside that environment
  And when they ask where Competitor Brand's effective price will be in Texas in 6 months, they are answered

Scenario: Acme AI's staff sign in through the client's own identity provider.
  Given the client has provisioned an account in its own identity provider for a named Acme AI engineer holding the Platform admin role
  When that Platform admin signs in to support North America Snacks' installation
  Then their access comes through the client's own identity provider
  And the client can end it by revoking that account, without Acme AI's involvement

Scenario: Break-glass credentials are not used while the client's own identity provider can be reached.
  Given the client's own identity provider can be reached
  When a Platform admin signs in to support North America Snacks' installation
  Then they sign in through the client's own identity provider
  And break-glass credentials are not used

Scenario: Break-glass access stays inside the customer's environment.
  Given the client's own identity provider cannot be reached during an incident
  When a Platform admin must support North America Snacks' installation
  Then they sign in with break-glass credentials held in the installation's own vault
  And signing them in reaches nothing outside the customer's environment
  And that access is recorded

Scenario: Raising a support case needs no connection from the installation.
  Given a Control plane admin has a direct login to Acme AI's own support portal
  When they raise a support case about North America Snacks' installation there
  Then North America Snacks' installation makes no connection to the portal
```

### Frontier Models

Every model an installation calls runs inside the customer's own infrastructure by default: Acme AI provides the models, and the installation hosts them. The client can choose to let some kinds of model call reach a frontier model provider outside it instead, a choice its own infrastructure team makes in the installation's configuration, never Acme AI, never any role inside PriceHorizon and never an upgrade, and one an installation that must stay air-gapped never makes. The kinds that can be chosen each send something different: reasoning over a question sends the question and the facts and model results it cites, the forecasts and Brand A's own targets among them; reading the qualitative corpus sends the documents read; and rendering an explanation sends the rationale it explains. Searching the qualitative corpus and matching product catalogs always stay inside the installation. Only the kinds the client names leave it, each carrying only what it sends, and each is served by a model version the client pins; every answer records the version of each language model that served it, Acme AI's own or a frontier provider's. Every forecast and simulated outcome is computed inside the installation by Acme AI's own models; where the client names reading the qualitative corpus, what a frontier model reads from documents feeds those forecasts as any reading does. A Control plane admin can see which kinds are named, without being able to change them, and every change to the choice is recorded in the audit log, with the kinds named before and after it, as the client's own, never Acme AI's.

#### Test Scenarios

```gherkin
Scenario: By default every model call stays inside the customer's environment.
  Given North America Snacks' installation configuration names no kind of model call for a frontier model provider
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then every model call answering it runs inside the customer's own infrastructure

Scenario: Only the kinds of model call the client names reach a frontier model provider.
  Given North America Snacks' installation configuration names only rendering an explanation for a frontier model provider
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then only the rationale being explained reaches the frontier model provider
  And the question itself, and the documents read for it, stay inside the customer's own infrastructure

Scenario: Searching the qualitative corpus never reaches a frontier model provider.
  Given North America Snacks' installation configuration names every kind of model call it can for a frontier model provider
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the search of the qualitative corpus for it runs inside the customer's own infrastructure

Scenario: Matching product catalogs never reaches a frontier model provider.
  Given North America Snacks' installation configuration names every kind of model call it can for a frontier model provider
  When a new product in Competitor Brand's catalog is matched to North America Snacks' own
  Then the matching runs inside the customer's own infrastructure

Scenario: Forecasts are computed inside the installation whatever the client names.
  Given North America Snacks' installation configuration names every kind of model call it can for a frontier model provider
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the forecast, its confidence, and the simulated outcomes are computed inside the installation

Scenario: An answer shows which frontier model served it.
  Given North America Snacks' installation configuration names rendering an explanation for a frontier model provider, pinned to one model version
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the record of how the answer was built names that model version

Scenario: Only the client's own infrastructure team can name a kind of model call for a frontier model provider.
  Given North America Snacks' installation configuration names no kind of model call for a frontier model provider
  When a Control plane admin, an Identity admin, or a Platform admin looks for a way to name one
  Then none of them can

Scenario: An upgrade leaves the client's choice unchanged.
  Given North America Snacks' installation configuration names only rendering an explanation for a frontier model provider
  When Acme AI's staff apply an upgrade the client elected
  Then the installation still names only rendering an explanation
  And the audit log records no change to the choice

Scenario: A Control plane admin sees which kinds of model call reach a frontier model provider.
  Given North America Snacks' installation configuration names rendering an explanation for a frontier model provider
  When a Control plane admin views the installation's settings
  Then they see that rendering an explanation is named
  And they cannot change it

Scenario: A change to the choice is recorded as the client's own.
  Given the client's own infrastructure team names rendering an explanation for a frontier model provider in North America Snacks' installation configuration
  When the installation next starts
  Then the audit log records the change, with the kinds named before and after it
  And the change is recorded as the client's own, not Acme AI's
```
