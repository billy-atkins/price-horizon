---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/identity-and-access.md
---

## Roles

PriceHorizon's roles distinguish everyday use from administration:

| Role | Description |
|---|---|
| Query user | Everyday use, asking questions and exploring the answer experience, scoped to whichever business units the person's identity grants |
| Control plane admin | Manages a business unit's own configuration, reference data, thresholds, and review queues, reviews forecast evidence and accuracy in bulk for that business unit, sees its audit log, Acme AI's own access included (`specs/application/product/tenant-administration/audit-log-visibility.md § Audit Log Visibility`), and can temporarily raise PriceHorizon's application logging detail for it (`specs/application/product/tenant-administration/application-log-control.md § Application Log Control`), scoped to that business unit alone, and can see which application and model versions the installation as a whole currently runs (`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades`) |
| Identity admin | Manages the mapping between the customer's own identity system and PriceHorizon's business units and roles, and sees the record of every change to it, not scoped to any single business unit, since a mistake here could affect access across all of them |
| Platform admin | Acme AI's own staff, onboarding an installation, executing an Acme AI-managed upgrade for a customer (a self-managed upgrade's own execution is described in `specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades` instead), diagnostic support access, seeing which application and model versions an installation currently runs (`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades`), and reviewing evidence and forecast accuracy in bulk across every business unit an installation hosts to tune the platform, never the client's business configuration itself |

`specs/application/product/architecture.md § Diagrams § Using and Administering` renders this.
