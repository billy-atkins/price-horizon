---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/secrets-management.md
---

## Data Source Connections

The Control plane admin role (`specs/application/product/roles.md § Roles`) can self-service enable and provide credentials for any data source Acme AI has already built a connector for, without Acme AI needing to be paged for a routine integration; support for a genuinely new data source type is the one exception, that is connector engineering, not day-to-day configuration. Whatever credentials the client provides get the same vault-isolation guarantee stated for Acme AI's own credentials (`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`).

### Test Scenarios

```gherkin
Scenario: Enabling a data source connection is a self-service action.
  Given a Control plane admin provides credentials for ScanTrack, a syndicated point-of-sale data source Acme AI has already built a connector for
  When the connection is enabled
  Then ScanTrack begins feeding North America Snacks without Acme AI's involvement

Scenario: Support for a genuinely new data source type is not self-service.
  Given a Control plane admin wants to connect ShelfSense, an in-store shelf-sensor telemetry source Acme AI has not already built a connector for
  When that need is raised
  Then support for it happens through connector engineering and an application release, not as a self-service action
```
