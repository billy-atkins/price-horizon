## Architecture Overview

PriceHorizon is a versioned, self-hosted installation inside each customer's own environment. That topology is the primary security control. Each installation has its own data stores. With local processing, workload data stays inside the customer's infrastructure. If the client authorizes a workload to use a frontier provider, that workload sends its specified payload to the provider. For external document extraction, the payload includes the document and the codes used to resolve its entities and geographies. The registry specifies each workload’s payload ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). Access control and audit logging are a governed second layer on top of that decision, not a substitute for it. Within an installation, the architecture is a shared foundation, computational layers built on it, and services that run those layers.

The foundation is common to every service, and the technical stack names each technology it relies on ([`specs/application/technical/stack.md § Technical Stack`](/specs/application/technical/stack.md#technical-stack)). The foundation holds one harmonized structured database (syndicated retail data, POS history, elasticity models, tax and macroeconomic data), and beside it one vector database (the qualitative corpus, chunked and embedded). It also holds a versioned registry of every callable model and weighting rubric, a secrets vault that issues one scoped credential per service, and a governed business glossary that every question resolves against before anything computes. Identity is federated from the customer's own IdP, which sits inside the customer's own environment. The customer's own people sign in through that IdP. Acme AI's own staff sign in through an account the client provisions in that same IdP. Only where the IdP cannot be reached do they sign in through local break-glass credentials drawn from that same vault. So no path needs a connection outside the customer's environment. The workflow determines which stage runs. The stage’s algorithm invokes its quantitative models. The language model interprets terms and explains retrieved facts and computed figures.

The layers run on that foundation. Knowledge embedding happens before any question is asked. Qualitative documents are extracted into driver signals, and competitor and Brand A catalogs are reconciled to a common product and geography reference. From that knowledge and the competitor's own price history, the batch path also computes and stores an effective price forecast for every combination a business unit tracks, so most questions become a lookup rather than a live computation.

After intent resolution, the query service captures the unit’s last complete publication. Before its first publication, the service explains why a forecast is unavailable. The captured publication supplies scheduled forecasts. For an eligible live request, the query service reuses an exact committed forecast and rationale or stages a new forecast from the publication’s pinned inputs before Position. The audited answer commit makes it reusable. [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`](/specs/application/technical/query-service/intent-and-retrieval.md#parallel-evidence-retrieval) specifies selection.

Layered output synthesis then turns a Predict result into the full, final answer. It produces a bounded, deterministic set of positioning options, chosen by the kind of decision the question is asked for. That kind of decision is the Query user's session choice unless the question's own words say otherwise. Each option is simulated for its business outcome. The options are consolidated down to a real set of choices and rendered into plain language on demand. Drill-down cuts across the stages. It is available at each stage rather than a step of its own. The same granularity, geography, or metric pivot applies whether what is being explored is Predict's forecast, Position's options, or Simulate's outcomes.

Not every question reaches an answer. A question from an asker with no unit in which they hold the Query user role is denied. A question comes back as a clarifying question instead of a forecast when neither the question nor the session settles its business unit, when its entities do not resolve uniquely, or when its kind of decision is unsettled. Past that point, a stage that cannot complete returns what the earlier stages already produced, labeled as incomplete rather than quietly substituted for. Where no stage completed, the answer says that instead ([`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior)).

The evidence those layers work from has named origins, and each kind has one home. Market data, meaning the competitor's syndicated data and Brand A's own internal data, lands in the structured database alongside tax and macroeconomic data. Reconciliation then matches the two market views there. Reconciliation is also where a price reported in a currency other than its geography's own is converted, once, at the rate captured with that data. From then on, every price stays in its geography's own currency and is never converted or combined across currencies.

Qualitative documents arrive by ingestion path. The path sets whether a document is a regulatory filing, licensed third-party commentary, or an internal analyst note, and with that, how credible the document counts. Extraction reads each document first. A document stating no event in any driver category is skipped. Only a complete Driver Signal is stored, in its business unit's own namespace of the vector database. An extraction sent to the review queue is stored only once resolved, and a product or geography match under review becomes usable only after resolution. A figure a reviewer supplies or corrects takes the credibility of the document that states it. Where the figure comes from the reviewer's own knowledge, it takes the credibility of an internal analyst note. Predict computation reads both stores and the model registry. [`§ Architecture Overview § Diagrams § From Evidence to Answer`](#from-evidence-to-answer) pictures where each kind of evidence comes from and where it is stored.

Predict computation builds each forecast the same way, on the batch path or live. Each Driver Signal goes, by its event type, to exactly one consumer, so no signal is counted twice. The competitor's announced price change, or a change to its promotional calendar, adjusts the baseline. The baseline carries forward the competitor's own price trend, seasonality and promotional cadence. Every other signal goes to driver attribution. Driver attribution sizes each driver's correction from that driver's weight in a versioned rubric and from the magnitudes of the signals routed to that driver. For elasticity, a registered model's estimate stands in place of those magnitudes, and for competitor plans, a registered model's translation of the signal it was given. The forecast's move is exactly the baseline move plus those corrections.

Triangulation selects the signals routed to driver attribution that take effect inside the horizon. A selected signal may push price in a direction the baseline does not show, by enough to count as a move on its own. That signal still counts in its driver's correction. It is also flagged as a conflict, which is recorded and shown rather than averaged away silently. When qualitative signals contribute, confidence reflects the weakest source, the freshness of the evidence and any flagged conflict. With market and model data alone, the score reflects the age of the data snapshot. A conflict also caps the confidence score, however strong the rest is. The rationale retains model validation dates. Their role in Predict is governed by [`specs/application/technical/model-registry.md § Open Questions [Name: Model Freshness in Predict]`](/specs/application/technical/model-registry.md#open-questions). Simulate accounts for the freshness of its models. The confidence band around the forecast comes from the forecasting models alone.

An answer is a set of records. Intent parsing turns a question into a Question Intent, which is not stored in either database. The records after it are stored in the structured database. A grid lookup, a reused live bundle or a new live computation yields an Effective Price Forecast carrying its Rationale Record. The Rationale Record is what the forecast's baseline, drivers and confidence open to. The positioning engine produces Positioning Candidates, each carrying that same Rationale Record. The simulation engine produces a Simulated Outcome per candidate, and all of those outcomes share one Rationale Record, computed once for the question. A Delivered Answer records any answer for which Predict produced a forecast, whether or not Position and Simulate complete. It records the forecast the answer was built on, the candidates generated with their outcomes, their visible group membership, order and labels, the kind of decision the answer was given for, and the versions and data the answer was produced against. So the answer's positioning and simulation can be reproduced, as its forecast can. [`§ Architecture Overview § Diagrams § The Answer`](#the-answer) pictures this.

The services split along a different axis than the layers do. A query service runs the live path, which is request-driven and latency-sensitive. A materialization service runs the batch path, which is throughput-oriented and tolerant of long jobs. The materialization service runs its forecasts nightly, whenever competitor data refreshes, and on demand for one business unit. It runs its document extraction as the corpus refreshes. A control plane service is separated for a security reason, not a workload one. The control plane service alone writes application-managed reference data and settings. The client’s infrastructure team controls installation support permission and external model destinations. The installation checks support permission on both sign-in paths and throughout each privileged session. So a vulnerability in the far larger, far more exposed query surface can never reach the capability to change what a competitor's code means or what a business unit's threshold is.

The control plane service is also the client's own self-service surface. A Control plane admin tunes their own business unit there without Acme AI, while the forecasting mechanism itself stays with Acme AI. An Identity admin maps the customer's identity claims to business units and roles there. The control plane service also serves read-only views of the installation's pinned versions, audit retention and frontier model choice.

PriceHorizon resolves authenticated claims against current role and scope mappings. Each question uses the combined grants from its mapped claims. Vector credentials confine retrieval to authorized business-unit namespaces, and every structured retrieval filters by authorized unit. Acme AI support also requires the client’s current installation permission at sign-in and for subsequent privileged actions. During an identity-provider outage the installation can authenticate a support operator locally with a vault credential. The same permission governs that session ([`specs/application/technical/identity-and-access.md § Platform admin access`](/specs/application/technical/identity-and-access.md#platform-admin-access)). [`§ Architecture Overview § Diagrams § Trust Boundaries`](#trust-boundaries) shows both support paths and the service credentials.

[`§ Architecture Overview § Layer-to-Architecture Mapping`](#layer-to-architecture-mapping) is the row-by-row proof. It ties each piece of the product-facing answer to the mechanism that produces it, and cites the full detail behind each mechanism from that mechanism's own file.

[`§ Architecture Overview § Diagrams § Layer Composition`](#layer-composition) renders this composition. [`§ Architecture Overview § Diagrams § Orchestration State Machine`](#orchestration-state-machine) renders the shape of a question's path through it. Both are for a reader who wants the picture before the proof.

### What Else These Services Run

Producing an answer is what the layers do, but it is not all these services run.

The materialization service checks published and live forecasts against their original target windows. It records a comparison once complete matching actuals arrive. [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome check`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-check) sets the verdict, signed error and pending or unevaluable dispositions.

The query service exposes one accuracy report across the administrator’s permitted units. Each forecast appears once with its evidence and comparison status. The report counts committed answers and confirmed receipts separately by original question time, including before comparable actuals exist. A disconnect after commitment can leave one prepared answer and zero receipts. Only the first matching authenticated acknowledgement counts, and each count carries its own retention coverage ([`specs/application/technical/query-service/evidence-and-accuracy-reporting.md § Bulk Evidence and Accuracy Report`](/specs/application/technical/query-service/evidence-and-accuracy-reporting.md#bulk-evidence-and-accuracy-report)).

Distinct kinds of record are kept alongside the answer path, and they are never folded together. An audit log of who did what is application data, not telemetry. The audit log is committed transactionally with the action it records, so an action and its record are never separated. It is retained for at least a year. A Platform admin can raise that period per a client's contractual requirement, and no routine path can lower it. The client reads the audit log on the control plane, each role reading the entries it may see. The audit log is exportable to someone with no access to the product. The export carries the record of what happened but never the answer content the record references.

The application's own telemetry, the logs, traces and metrics of how a request executed, is the opposite in almost every respect. Telemetry is kept for weeks. It carries none of the protected content the answer path handles: no forecast values, no document content, no credential material, no raw IdP claims. A forwarding agent ships telemetry to whatever observability platform the client already runs. Where the client runs none, the forwarding agent ships it to a viewer shipped alongside PriceHorizon. PriceHorizon needs no connection outside the client's environment to ship telemetry. It never sends telemetry to anything Acme AI hosts, and never combines it with another customer's.

An answer's own lineage, what produced one specific number, is neither. The lineage lives on the Effective Price Forecast and Delivered Answer rows the answer is made of ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance), [`specs/application/technical/data-model.md § Core Data Model § Audit Log`](/specs/application/technical/data-model.md#audit-log)).

Further mechanisms keep the design honest rather than serve a request. A golden-question harness runs in CI whenever a model, prompt template, or data pipeline version changes. The harness asserts that the structural rules this specification declares fire: a Decision Table row, an Algorithm step, a Constraint. Each rule carries at least one question written alongside it. The harness checks the declared rules, not whether a forecast came true. The realized outcomes are for that ([`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)). The upstream work feeding the grid may fail to resolve something confidently: a low-confidence product match, an unresolved source geography, or an ambiguous or incomplete document extraction. That item is flagged into a review queue for a Control plane admin rather than guessed at, before it ever reaches an answer ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Review Queue Item`](/specs/application/technical/data-model.md#review-queue-item)).

The product states guarantees: a repeatable answer, every number traced to a versioned source, qualitative context weighed in rather than appended afterward, and an answer that shows how it was built. Beneath them all sits a guardrail: flag uncertainty rather than guess. The guarantees and the guardrail are not another layer. Each is assembled from mechanisms this file names, and one file gathers how each is built ([`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`](/specs/application/technical/guarantees-mechanics.md#how-the-guarantees-are-achieved-mechanically)).

One REST API serves both the answer surface and the control plane, with one authentication model and one set of client libraries for both. The service boundary separates the two, not the API surface ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations`](/specs/application/technical/engineering-and-production-considerations.md#engineering-and-production-considerations)).

### Diagrams

#### Layer Composition

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    FOUND["Shared foundation<br/>structured database · vector database<br/>model registry · secrets vault<br/>governed glossary · federated identity"]

    subgraph Materialization["Materialization service: batch path"]
        KE["Knowledge embedding"]
        PCN["Predict computation"]
        GRID[("Materialized grid")]
        KE --> PCN --> GRID
    end

    subgraph QueryService["Query service: live path"]
        RET["Evidence retrieval"]
        PCL["Predict computation"]
        LOS["Layered output synthesis<br/>Position, Simulate, narrative rendering"]
        RET -->|"eligible live miss"| PCL --> LOS
        RET -->|"eligible live match"| LOS
    end

    subgraph ControlPlane["Control plane service"]
        CFG["Application-managed reference data<br/>and settings"]
    end

    DRILL["Drill-down: cross-cutting"]

    FOUND --> Materialization
    FOUND --> QueryService
    FOUND --> ControlPlane
    CFG -. "written only through<br/>the control plane" .-> FOUND
    GRID -. "grid lookup" .-> LOS
    DRILL -.- PCL
    DRILL -.- LOS
```

**Caption:** The foundation, the layers, and the services this file describes. Predict computation appears in more than one service because it is one layer run on different cadences. Cadence is the axis on which layers and services differ. \
**Sources:**
  - [`specs/application/technical/control-plane-service/control-plane.md § Control Plane`](/specs/application/technical/control-plane-service/control-plane.md#control-plane)
  - [`specs/application/technical/data-model.md § Core Data Model § Harmonized quantitative foundation`](/specs/application/technical/data-model.md#harmonized-quantitative-foundation)
  - [`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema`](/specs/application/technical/data-model.md#vector-database-schema)
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Service boundaries`](/specs/application/technical/engineering-and-production-considerations.md#service-boundaries)
  - [`specs/application/technical/glossary-and-grounding.md § Guaranteed grounding`](/specs/application/technical/glossary-and-grounding.md#guaranteed-grounding)
  - [`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated)
  - [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)
  - [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)
  - [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation)
  - [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`](/specs/application/technical/query-service/intent-and-retrieval.md#parallel-evidence-retrieval)
  - [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval § Forecast source`](/specs/application/technical/query-service/intent-and-retrieval.md#forecast-source)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`](/specs/application/technical/query-service/layered-output-synthesis.md#layered-output-synthesis-producing-the-answer)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Narrative rendering`](/specs/application/technical/query-service/layered-output-synthesis.md#narrative-rendering)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`](/specs/application/technical/query-service/layered-output-synthesis.md#positioning-engine)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)
  - [`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management)
  - [`§ Architecture Overview`](#architecture-overview)

#### Trust Boundaries

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    USERS(["The customer's own people"]) --> IDP
    ACME(["Acme AI's own staff"]) -->|"an account<br/>the client provisions"| IDP
    ACME -.->|"local break-glass credentials,<br/>where the IdP cannot be reached"| VAULT
    subgraph ENV["The customer's own environment"]
        OPS(["Client infrastructure team"])
        IDP["The customer's own IdP"]
        subgraph INST["PriceHorizon installation"]
            MAP["Current role and scope mappings"]
            PERM["Installation support permission"]
            CHECK["Support authorization"]
            SUPPORT["Support and monitoring"]
            VAULT[("Secrets vault<br/>one scoped credential per service")]
            QS["Query service"]
            MS["Materialization service"]
            CP["Control plane service"]
            SDB[("Structured database")]
            VDB[("Vector database<br/>one namespace per business unit")]
        end
    end
    IDP -->|"authenticated claims"| MAP
    MAP -->|"authorized units and roles"| QS
    MAP -->|"administrative grants"| CP
    OPS -->|"sets or withdraws"| PERM
    PERM -->|"current permission"| CHECK
    MAP -->|"mapped Platform admin role"| CHECK
    VAULT -.->|"emergency identity during IdP outage"| CHECK
    CHECK --> SUPPORT
    VAULT --> QS
    VAULT --> MS
    VAULT --> CP
    QS -->|"only the namespaces<br/>its credentials allow"| VDB
    QS -->|"filter by authorized unit"| SDB
    CP -->|"writes application-managed<br/>reference data and settings"| SDB
    QS -.-> FRONT(["A frontier model provider,<br/>seeing only what the client allows"])
    MS -.-> FRONT
```

**Caption:** The customer administers support permission inside its environment. The installation checks that permission on federated and emergency support access, including actions in existing sessions. Current mappings turn the identity provider’s claims into roles and scope. Every structured read filters by authorized unit. Service credentials confine vector retrieval to authorized namespaces. The control plane writes application-managed reference data and settings. The client’s infrastructure team owns installation settings, including support permission and permitted external model destinations. \
**Sources:**
  - [`specs/application/technical/data-model.md § Core Data Model § Harmonized quantitative foundation`](/specs/application/technical/data-model.md#harmonized-quantitative-foundation)
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance)
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Service boundaries`](/specs/application/technical/engineering-and-production-considerations.md#service-boundaries)
  - [`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated)
  - [`specs/application/technical/identity-and-access.md § Platform admin access`](/specs/application/technical/identity-and-access.md#platform-admin-access)
  - [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)
  - [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`](/specs/application/technical/query-service/intent-and-retrieval.md#intent-parsing-and-decoupling)
  - [`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management)
  - [`§ Architecture Overview`](#architecture-overview)

#### From Evidence to Answer

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    MKT["Market data<br/>the competitor's syndicated data · Brand A's internal data"]
    TAX["Tax and macroeconomic data"]
    DOCS["Qualitative documents, by ingestion path<br/>regulatory filings · licensed third-party commentary<br/>internal analyst notes"]
    MKT --> SDB[("Structured database")]
    TAX --> SDB
    RECON["Reconciliation<br/>matches products and geographies<br/>to one reference,<br/>converts currency once"]
    SDB -.- RECON
    DOCS --> EXT["Extraction<br/>a document stating no driver event is skipped"]
    EXT -->|"complete Driver Signal"| VDB[("Vector database<br/>one namespace per business unit")]
    RECON -->|"unresolved<br/>match"| RQ["Review queue"]
    EXT -->|"ambiguous<br/>or incomplete"| RQ
    RQ -->|"match settled"| SDB
    RQ -->|"extraction resolved"| VDB
    SDB --> PC["Predict computation"]
    VDB --> PC
    REG[("Model registry")] --> PC
    PC --> EPF["Effective Price Forecast with its Rationale Record<br/>stored in the structured database"]
```

**Caption:** Where evidence comes from, what keeps unhelpful or incomplete evidence out of a forecast, where each kind is stored, and the forecast record its baseline, drivers and confidence open to. \
**Sources:**
  - [`specs/application/technical/data-model.md § Core Data Model § Harmonized quantitative foundation`](/specs/application/technical/data-model.md#harmonized-quantitative-foundation)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`](/specs/application/technical/data-model.md#product-and-geography-match)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Review Queue Item`](/specs/application/technical/data-model.md#review-queue-item)
  - [`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema`](/specs/application/technical/data-model.md#vector-database-schema)
  - [`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)
  - [`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`](/specs/application/technical/materialization-service/driver-signal-extraction.md#vector-and-semantic-mapping-with-structured-extraction)
  - [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation`](/specs/application/technical/materialization-service/reconciliation.md#product-and-geography-reconciliation)
  - [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`](/specs/application/technical/materialization-service/reconciliation.md#currency-normalization)
  - [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)
  - [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation)

#### The Answer

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    Q(["Question asked"]) -->|"intent parsing"| QI["Question Intent<br/>not stored in either database"]
    QI -->|"published cell or eligible live forecast<br/>(reused or computed)"| EPF
    subgraph STORED["Stored in the structured database"]
        EPF["Effective Price Forecast<br/>with its Rationale Record"]
        PC["Positioning Candidates<br/>each carrying the forecast's Rationale Record"]
        SO["A Simulated Outcome per candidate<br/>individual metric evidence and shared confidence rationale"]
        DA["Delivered Answer<br/>visible groups, order and labels<br/>for the stages delivered"]
        EPF -->|"positioning engine"| PC
        PC -->|"simulation engine"| SO
        EPF -.->|"built on"| DA
        PC -.->|"candidate IDs and prices"| DA
        SO -.->|"member outcomes and evidence"| DA
    end
```

**Caption:** The records an answer is made of: which stage produces each, which are stored, and what a Delivered Answer records for any answer for which Predict produced a forecast, whether or not Position and Simulate complete. \
**Sources:**
  - [`specs/application/technical/data-model.md § Core Data Model § Harmonized quantitative foundation`](/specs/application/technical/data-model.md#harmonized-quantitative-foundation)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Delivered Answer`](/specs/application/technical/data-model.md#delivered-answer)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`](/specs/application/technical/data-model.md#positioning-candidate)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`](/specs/application/technical/data-model.md#question-intent)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)
  - [`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Simulated Outcome`](/specs/application/technical/data-model.md#simulated-outcome)
  - [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)
  - [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation)
  - [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`](/specs/application/technical/query-service/intent-and-retrieval.md#intent-parsing-and-decoupling)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-package-extended)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`](/specs/application/technical/query-service/layered-output-synthesis.md#positioning-engine)
  - [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)

#### Orchestration State Machine

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    START(["Question asked"]) --> INTENT["Question intent"]
    INTENT -->|"no queryable unit"| DENIED(["Denied"])
    INTENT -->|"business unit unsettled,<br/>entities do not resolve uniquely,<br/>or the kind of decision is unsettled"| CLARIFY(["Clarifying question"])
    INTENT -->|"cannot complete"| PF(["No forecast; the answer<br/>says one could not be computed"])
    INTENT -->|"resolves"| LOOKUP["Retrieve forecast bundle"]
    LOOKUP -->|"published cell or eligible live match"| POSITION["Position"]
    LOOKUP -->|"eligible live key, no matching bundle"| PREDICT["Compute and stage forecast"]
    LOOKUP -->|"unavailable or retrieval fails"| PF
    PREDICT -->|"cannot complete"| PF
    PREDICT --> POSITION
    POSITION -->|"cannot complete"| POSF(["Forecast returned,<br/>labeled incomplete"])
    POSITION --> SIMULATE["Simulate"]
    SIMULATE -->|"cannot complete"| SIMF(["Forecast and options returned,<br/>labeled incomplete"])
    SIMULATE --> GROUP["Option consolidation"]
    GROUP -->|"grouped outcomes"| RENDER["Narrative rendering"]
    GROUP -->|"retries exhausted: individual outcomes"| RENDER
    RENDER --> AP(["Answer produced"])

    classDef stop fill:#f4f4f4,stroke:#777,color:#222
    classDef done fill:#e8f2e8,stroke:#4a7,color:#222
    class DENIED,CLARIFY,PF,POSF,SIMF stop
    class AP done
```

**Caption:** The Question run State Machine, collapsed to this file's own altitude. Each stage's internal states go unnamed here, as this file's prose leaves them. The full breakdown stays in the State Machine's States and Transitions tables. \
**Sources:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)

### Layer-to-Architecture Mapping

The seam between this file and the product's own Answer Engine domain ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do), [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit), [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business), [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage), [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context)). Every product-facing layer traces to one mechanism here. Nothing in the answer experience exists without a corresponding piece of this architecture. Predict's layers are typically served from the [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) materialized grid. The live [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation) mechanism runs only for an eligible live key without a matching stored bundle. Finer geographies use the parent route, and unsupported requests remain unavailable.

**Reference Key:** Product Layer \
**Required:** Stage, Technical Mechanism

| Product Layer | Stage | Technical Mechanism |
|---|---|---|
| Scorecard / heatmap | Predict | Forecast materialization ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)), or, for an eligible live request, its matching stored bundle or the same Predict computation on a miss ([`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation)); Brand A's current price is retrieved ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`](/specs/application/technical/query-service/intent-and-retrieval.md#parallel-evidence-retrieval)), not modeled |
| Plain-language narrative | Predict, Position and Simulate | Narrative rendering ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Narrative rendering`](/specs/application/technical/query-service/layered-output-synthesis.md#narrative-rendering)), renders forecast prose from its rationale. The installation adds Position and Simulate clauses from the delivered member records and saves the exact assembled wording for audit |
| Geographic visualization | Predict | Materialized grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)) rendered directly as a map ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`](/specs/application/technical/query-service/layered-output-synthesis.md#layered-output-synthesis-producing-the-answer)); supported estimates and labeled rate references from an available parent forecast below the grid ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Decomposition graph | Predict | Driver Attribution contribution breakdown ([`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution)), rendered as a driver chart, alongside the baseline and its evidence ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)); not available below the materialized grid's geography, where no causal signal was computed |
| Evidence view, per driver | Predict | driver_evidence in the Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), populated during Driver Attribution ([`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution)) from the same Driver Signal or model source the computation used |
| Confidence, per reason | Predict, Position, Simulate | `confidence_components` and `conflicts` in the Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), written by [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package) for Predict and Position, and by [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-package-extended) for a Simulated Outcome, whose record carries no `conflicts` |
| Options frame | Position | Positioning engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`](/specs/application/technical/query-service/layered-output-synthesis.md#positioning-engine)): fixed archetype rules applied to the Predict output and seeded by decision type ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Archetype seeds`](/specs/application/technical/query-service/layered-output-synthesis.md#archetype-seeds)), not an optimizer, using same-market origin effective prices and the selected competitor target, with candidates consolidated after simulation ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation`](/specs/application/technical/query-service/layered-output-synthesis.md#option-consolidation)) |
| Outcome comparison | Simulate | Simulation engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)): share, volume, and margin models run once per candidate; category growth compares category units implied by brand volume and volume share with the comparable observed category volume, revenue calculated directly as price times volume |
| Drill-down, granularity within the grid | All | Resolve the narrower scope through the same selector as a direct question. Read its published cell. An eligible live request reuses its matching forecast and rationale or computes on a miss ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Drill-down, granularity below the grid | All | An available parent forecast can support a local estimate or supply a labeled rate for reference. An unavailable local figure carries its reason, including the parent’s reason when its forecast is unavailable. Estimates have no local decomposition ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Drill-down, metric pivot | All | Existing output re-projected onto a different metric field; new model call only if that metric was not already computed ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Decision context shown with every answer | All | Session context ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Session context`](/specs/application/technical/query-service/intent-and-retrieval.md#session-context)), carried on each question request; intent parsing settles the business unit and kind of decision each question is given for, its own words over the session's ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](/specs/application/technical/query-service/intent-and-retrieval.md#business-unit), [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](/specs/application/technical/query-service/intent-and-retrieval.md#decision-type)); every answer returns both, and the kind of decision seeds the positioning engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Archetype seeds`](/specs/application/technical/query-service/layered-output-synthesis.md#archetype-seeds)) |
