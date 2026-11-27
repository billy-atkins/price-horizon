---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/secrets-management.md
---

## Data Source Connections

The Control plane admin role ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) can enable any data source Acme AI has already built a connector for, and provide the credentials for it, as a self-service action. Acme AI does not need to be paged for a routine integration. The one exception is support for a new data source type, which is connector engineering, not day-to-day configuration. Whatever credentials the client provides get the same vault-isolation guarantee stated for Acme AI's own credentials ([`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology)).

A unit admin can rotate a connector credential. Each successful change takes effect on the next retrieval and has a redacted audit record. If activation fails, the previous credential remains effective. Retrying a committed rotation preserves its result. Neither secret appears in ordinary installation data.

### Test Scenarios

```gherkin
Scenario: Enabling a data source connection is a self-service action.
  Given a Control plane admin provides credentials for ScanTrack, a syndicated point-of-sale data source Acme AI has already built a connector for
  When the connection is enabled
  Then ScanTrack begins feeding North America Snacks without Acme AI's involvement

Scenario: Using and rotating a connector credential leaves ordinary installation data free of the secret.
  Given North America Snacks has enabled the existing ScanTrack connector with a client-supplied credential
  When its Control plane admin replaces the credential and the connector next retrieves ScanTrack data
  Then the source accepts the replacement credential and data arrives for North America Snacks
  And a reader of ordinary configuration, reference data, application logs and the rotation audit record can retrieve neither credential
  And the rotation is visible in that record

Scenario: Support for a genuinely new data source type is not self-service.
  Given a Control plane admin wants to connect ShelfSense, an in-store shelf-sensor telemetry source Acme AI has not already built a connector for
  When that need is raised
  Then support for it happens through connector engineering and an application release, not as a self-service action

Scenario: A failed audit write leaves the previous credential effective.
  Given a connector uses a working credential and its replacement has been staged
  When the activation transaction fails to record its audit entry
  Then the connector still uses the previous credential for its next retrieval
  When the same rotation later commits and its response is retried
  Then the connector uses the replacement and the unit sees one rotation event
  And neither credential value appears in that event or its export
```
