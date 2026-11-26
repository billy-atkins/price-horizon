---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/model-registry.md
---

## Versioned Upgrades

Because the installation is versioned, an upgrade is a discrete, chosen event rather than a silent change underneath a customer. Versioning also makes the repeatable-answer guarantee in [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) durable over time, not only within a single session. A customer can identify exactly which version produced a given answer. The customer can also know that the answer would reproduce again if nothing has changed since. The application and its underlying models are upgraded independently of each other, so a customer can take one without the other changing underneath them.

A Platform admin executes an Acme AI-managed upgrade. The Platform admin is the same role already responsible for onboarding and diagnostic access. Under a self-managed upgrade, applying the release Acme AI ships is the responsibility of whoever already operates the infrastructure PriceHorizon is installed on: the client's own infrastructure team. That team holds the responsibility because PriceHorizon deploys inside the customer's own environment rather than a shared, Acme-AI-hosted one ([`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology)). The infrastructure team never uses the PriceHorizon product to apply a release. So the team takes no role in PriceHorizon's own role model, and needs no new role added for it.

The client elects each upgrade. Acme AI never moves an installation to a version the client has not elected. Whether an upgrade is Acme AI-managed or self-managed settles who carries it out. That choice is made per upgrade rather than fixed once for the installation. Electing an upgrade is a client decision made with Acme AI rather than an action taken inside the product, so electing adds no role here, for the same reason applying a release does not.

A Control plane admin and a Platform admin can each see the installation's versions through their own surface. Each sees the currently pinned application version, one version spanning the installation's services. Alongside it is each model's own version, because models version independently of the application and of one another. Both views are read-only.

The client can read each completed upgrade in the installation-wide audit history throughout its retention period. Each event identifies who applied it and shows the application and every effective model version at activation, even after another release. A model-only release has its own event. Historical records identify any uncaptured versions as unknown.

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

Scenario: Successive upgrades by different operators remain distinguishable in installation history.
  Given the client elected application 4.3 for Acme AI to apply with forecast model F7 and rendering model R2
  And Acme AI applied 4.3 before the client separately elected its own team to activate forecast model F8 on 4.3
  When the client's infrastructure team applies the next elected release 4.4 with rendering still at R2
  Then the client sees three upgrade events: Acme AI applied 4.3 with F7 and R2, the client applied F8 with 4.3 and R2, and the client applied 4.4 with F8 and R2
  And reading the first upgrade after the second still shows its original versions

Scenario: A model-only release is visible before any later application release.
  Given the client is running application 4.3 with forecast model F7 and rendering model R2
  When its infrastructure team activates the elected forecast model F8
  Then the client's audit view identifies that operator and shows 4.3, F8 and R2 for the completed upgrade
  And replaying the same activation leaves one completed upgrade in that history

Scenario: A retained legacy upgrade shows which versions the installation captured.
  Given the audit history retains a completed application 4.2 upgrade whose model versions were never captured
  And the current installation runs application 4.4 with forecast model F8
  When a Control plane admin opens the retained 4.2 event
  Then the event shows the recorded application version 4.2 and identifies its historical model versions as unknown
  And F8 appears only in records that captured it

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
