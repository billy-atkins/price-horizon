## Bulk Evidence and Accuracy Report

One report, not one per scope, since a Control plane admin's own business unit, a Platform admin's escalated look at one business unit, and a Platform admin's installation-wide view are the same underlying join at different scopes, all stated together in `specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`, which the onboarding health check `specs/application/product/platform-and-compliance-operations/onboarding-verification.md` also reuses. Access to each scope follows the query service's own existing claim-based model, no new gating mechanism: a Control plane admin's claim is already scoped to one business unit, a Platform admin's is not (`specs/application/technical/identity-and-access.md § Platform admin access`), so the existing claim model already produces the right scope for each.

| Role | Business units in scope |
|---|---|
| Control plane admin | Their own single business unit |
| Platform admin | One specific business unit, on escalation from a Control plane admin, or every business unit the installation hosts |

| Step | Action |
|---|---|
| 1 | Determine the business units in scope for the requesting role, per the table above |
| 2 | If no business unit remains in scope, stop |
| 3 | Take the next business unit in scope |
| 4 | Select every Effective Price Forecast (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`) for that business unit |
| 5 | For each, retrieve its Rationale Record's retrieval_trace (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`), naming the Driver Signals and other inputs it depended on |
| 6 | Left join each forecast to its Realized Outcome (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`), if its horizon has elapsed and one exists |
| 7 | Return each forecast alongside its evidence and, where present, its Realized Outcome's verdict and forecast_error |
| 8 | Return to step 2 |

A forecast whose horizon has not yet elapsed always produces nothing from step 6, this is what makes the same report also the onboarding health check `specs/application/product/platform-and-compliance-operations/onboarding-verification.md` describes, not a special case handled separately.

The verdict step 7 returns is the judgment `specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy` promises, whether each completed forecast turned out to be right, set once by `specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking` and never recomputed here. This report surfaces every Effective Price Forecast row regardless of which path produced it, computed_via batch or live (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`); a live-path answer for a query falling outside the grid, common in an installation's first days before the grid has filled in, is one such row (`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging`), so the onboarding health check that `specs/application/product/platform-and-compliance-operations/onboarding-verification.md` describes has something to show before the grid does.
