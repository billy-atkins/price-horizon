# PriceHorizon — Technical Specifications

| File | Description |
|---|---|
| `architecture.md` | A self-contained overview of the self-hosted deployment topology, the shared foundation, the layers, and the services, what else those services run beyond producing an answer, the diagrams of how they compose and the trust boundaries around them, where an answer's evidence comes from and is stored, the records an answer is made of, and how a question moves through them, and the Layer-to-Architecture Mapping, the seam to the product spec |
| `data-model.md` | The full Core Data Model: the harmonized quantitative foundation, the vector database schema, reference and master data, pipeline and answer artifacts, and the audit log |
| `model-registry.md` | The versioned, callable models and weighting rubrics every service calls into |
| `secrets-management.md` | The credential vault: where break-glass and every other credential live, what the vault provides for them, and the scoped credential each service draws from it |
| `glossary-and-grounding.md` | The governed business glossary and the effective-price definition it grounds |
| `identity-and-access.md` | Federated business unit access and Acme AI's own platform admin access |
| `predict-computation.md` | The shared signal routing, forecasting, triangulation, driver attribution, and confidence mechanism the query and materialization services both invoke |
| `guarantees-mechanics.md` | How each product guarantee is actually built |
| `evaluation-and-monitoring.md` | The golden-question harness that checks the design's own declared rules |
| `engineering-and-production-considerations.md` | Data pipeline cadence, the latency and cost budget, orchestration, service boundaries, API shape, deployment and versioning, and security and governance, including the audit log's mechanics and application telemetry |
| `delivery-approach.md` | The staged delivery plan |
| `risks-and-mitigations.md` | Every safeguard in the design, gathered into one Constraint table |
| `query-service/` | The query-service-only parts of the live path, from intent parsing and retrieval to layered output synthesis, plus the bulk evidence and accuracy report it also serves. See `query-service/index.md`. |
| `materialization-service/` | The batch path: forecast materialization, reconciliation, driver signal extraction, and realized outcome tracking. See `materialization-service/index.md`. |
| `control-plane-service/` | The self-service configuration surface and its governance table, and the read-only views of the installation's pinned versions and audit retention. See `control-plane-service/index.md`. |
