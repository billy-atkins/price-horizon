---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/engineering-and-production-considerations.md
---

## Versioned Upgrades

Because the installation is versioned, an upgrade is a discrete, chosen event rather than a silent change underneath a customer. Versioning also makes the repeatable-answer guarantee in [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) durable over time, not only within a single session. A customer can identify exactly which version produced a given answer. The customer can also know that the answer would reproduce again if nothing has changed since. The application and its underlying models are upgraded independently of each other, so a customer can take one without the other changing underneath them.

A Platform admin executes an Acme AI-managed upgrade. The Platform admin is the same role already responsible for onboarding and diagnostic access. Under a self-managed upgrade, applying the release Acme AI ships is the responsibility of whoever already operates the infrastructure PriceHorizon is installed on: the client's own infrastructure team. That team holds the responsibility because PriceHorizon deploys inside the customer's own environment rather than a shared, Acme-AI-hosted one ([`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology)). The infrastructure team never uses the PriceHorizon product to apply a release. So the team takes no role in PriceHorizon's own role model, and needs no new role added for it.

The client elects each upgrade. Acme AI never moves an installation to a version the client has not elected. Whether an upgrade is Acme AI-managed or self-managed settles who carries it out. That choice is made per upgrade rather than fixed once for the installation. Electing an upgrade is a client decision made with Acme AI rather than an action taken inside the product, so electing adds no role here, for the same reason applying a release does not.

A Control plane admin and a Platform admin can each see the installation's versions through their own surface. Each sees the currently pinned application version, one version spanning the installation's services. Alongside it is each model's own version, because models version independently of the application and of one another. Both views are read-only.

### Test Scenarios

```gherkin
Scenario: An upgrade is a discrete, chosen event, not a silent change.
  Given a client's installation is running application version 4.2 and Acme AI has released application version 4.3
  When a Platform admin has not yet executed the upgrade to version 4.3
  Then the installation continues running application version 4.2 unchanged

Scenario: The application and its models upgrade independently.
  Given a Platform admin executes the upgrade to application version 4.3 while every model the installation calls stays on its own current registry version
  When the application upgrade completes
  Then none of those model versions change as a result

Scenario: A Control plane admin can see current version information at any time.
  Given a client's installation is running application version 4.3 with every model pinned to its own current registry version
  When a Control plane admin checks the installation's current versions
  Then they see application version 4.3 and each model's own current version

Scenario: Acme AI executes an elected upgrade.
  Given a client has elected an Acme AI-managed upgrade to application version 4.3, which Acme AI has released
  When a Platform admin executes the upgrade
  Then the installation moves to application version 4.3

Scenario: Acme AI does not apply a released version the client has not elected.
  Given a client's installation is running application version 4.2
  And Acme AI has released application version 4.3
  And the client has not elected an upgrade to version 4.3
  When the release remains available and unelected
  Then the installation continues running application version 4.2 unchanged
  And Acme AI does not execute an upgrade to version 4.3 on its own initiative

Scenario: A Platform admin can see current version information at any time.
  Given a client's installation is running application version 4.3 with every model pinned to its own current registry version
  When a Platform admin checks the installation's current versions
  Then they see application version 4.3 and each model's own current version
```
