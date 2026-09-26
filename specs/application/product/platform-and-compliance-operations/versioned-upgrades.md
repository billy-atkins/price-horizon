---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/engineering-and-production-considerations.md
---

## Versioned Upgrades

Because the installation is versioned, an upgrade is a discrete, chosen event rather than a silent change underneath a customer. That is also what makes the repeatable-answer guarantee in `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` durable over time, not only within a single session: a customer can identify exactly which version produced a given answer and know that answer would reproduce again if nothing since has changed. The application and its underlying models are upgraded independently of each other, so a customer can take one without the other changing underneath them.

Under an Acme AI-managed upgrade, a Platform admin executes it, the same role already responsible for onboarding and diagnostic access. Under a self-managed upgrade, applying the release Acme AI ships is the responsibility of whoever already operates the infrastructure PriceHorizon is installed on, the client's own infrastructure team, since PriceHorizon deploys inside the customer's own environment rather than a shared, Acme-AI-hosted one (`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`). That team never uses the PriceHorizon product itself to do this, so it takes no role in PriceHorizon's own role model rather than needing a new role added for it.

The client elects each upgrade, and Acme AI never moves an installation to a version they have not elected. Whether an upgrade is Acme AI-managed or self-managed settles who carries it out, and is decided per upgrade rather than fixed once for the installation. Electing one is a client decision made with Acme AI rather than an action taken inside the product, so it adds no role here for the same reason applying a release does not.

A Control plane admin and a Platform admin can each see, through their own surface, the currently pinned application version, one version spanning the installation's services, and alongside it each model's own version, since models version independently of the application and of one another. Both views are read-only.

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
