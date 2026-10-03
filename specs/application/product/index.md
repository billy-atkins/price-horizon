# PriceHorizon — Product Specifications

| File | Description |
|---|---|
| `vision.md` | The RGM vision: the narrative destination this product delivers |
| `architecture.md` | The product as a whole: every domain PriceHorizon's capabilities are organized around and how they compose, and the diagrams of how the answer composes, how it is built from evidence, how using and administering stay apart, and what an answer shows when it falls short |
| `roles.md` | The roles PriceHorizon defines, distinguishing everyday use from administration, which every domain relies on and no domain holds |
| `answer-engine/` | Predict, Position, Simulate, Drill-down, and the decision context they are asked in: the core answer capability. See `answer-engine/index.md`. |
| `trust-and-explainability/` | The guarantees this answer engine makes, and what an answer shows when a stage cannot complete. See `trust-and-explainability/index.md`. |
| `accuracy-governance.md` | How forecast accuracy is tracked against what actually happened, and reviewed in bulk by both a Platform admin and a Control plane admin |
| `tenant-administration/` | The client's own self-service configuration, review, and record-visibility surface. See `tenant-administration/index.md`. |
| `identity-and-access/` | How using and administering are kept apart, how access federates to the customer's own identity provider, and how an Identity admin grants it. See `identity-and-access/index.md`. |
| `platform-and-compliance-operations/` | Deployment, versioning, and onboarding verification. See `platform-and-compliance-operations/index.md`. |
| `logging-and-traceability.md` | The different records PriceHorizon keeps about itself, audit log, application log, and answer lineage, what each answers and for whom, and why they are kept apart |
