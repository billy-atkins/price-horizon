## Architecture Overview

PriceHorizon is a versioned, self-hosted installation inside each customer's own environment. That topology is the primary security control. A customer's data stays inside the customer's own infrastructure by construction, and no shared store spans customers for the data to leak through. The one exception is what the client lets a frontier model provider see ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). Access control and audit logging are a governed second layer on top of that decision, not a substitute for it. Within an installation, the architecture is a shared foundation, computational layers built on it, and services that run those layers.

The foundation is common to every service, and the technical stack names each technology it relies on ([`specs/application/technical/stack.md § Technical Stack`](/specs/application/technical/stack.md#technical-stack)). The foundation holds one harmonized structured database (syndicated retail data, POS history, elasticity models, tax and macroeconomic data), and beside it one vector database (the qualitative corpus, chunked and embedded). It also holds a versioned registry of every callable model and weighting rubric, a secrets vault that issues one scoped credential per service, and a governed business glossary that every question resolves against before anything computes. Identity is federated from the customer's own IdP, which sits inside the customer's own environment. The customer's own people sign in through that IdP. Acme AI's own staff sign in through an account the client provisions in that same IdP. Only where the IdP cannot be reached do they sign in through local break-glass credentials drawn from that same vault. So no path needs a connection outside the customer's environment. Because every question resolves against the glossary, the language model reasoning over a question never computes a number itself. It calls versioned models and cites retrieved facts.

The layers run on that foundation. Knowledge embedding happens before any question is asked. Qualitative documents are extracted into driver signals, and competitor and Brand A catalogs are reconciled to a common product and geography reference. From that knowledge and the competitor's own price history, the batch path also computes and stores an effective price forecast for every combination a business unit tracks, so most questions become a lookup rather than a live computation.

Once a question is asked, the live path first retrieves the evidence that bears on it. Predict computation then turns that evidence into the forecast, the driver attribution behind it, and the confidence score attached to it. Predict computation runs across the whole grid on the batch path, or live for anything the grid does not already cover. The computation is identical either way, so a live answer and a materialized one never disagree over timing. Where a business unit's configuration changed between them, each records the configuration version it used ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`](/specs/application/technical/engineering-and-production-considerations.md#orchestration)).

Layered output synthesis then turns a Predict result into the full, final answer. It produces a bounded, deterministic set of positioning options, chosen by the kind of decision the question is asked for. That kind of decision is the Query user's session choice unless the question's own words say otherwise. Each option is simulated for its business outcome. The options are consolidated down to a real set of choices and rendered into plain language on demand. Drill-down cuts across the stages. It is available at each stage rather than a step of its own. The same granularity, geography, or metric pivot applies whether what is being explored is Predict's forecast, Position's options, or Simulate's outcomes.

Not every question reaches an answer. A question from an asker with no business unit access at all is denied. A question comes back as a clarifying question instead of a forecast when neither the question nor the session settles its business unit, when its entities do not resolve uniquely, or when its kind of decision is unsettled. Past that point, a stage that cannot complete returns what the earlier stages already produced, labeled as incomplete rather than quietly substituted for. Where no stage completed, the answer says that instead ([`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior)).

The evidence those layers work from has named origins, and each kind has one home. Market data, meaning the competitor's syndicated data and Brand A's own internal data, lands in the structured database alongside tax and macroeconomic data. Reconciliation then matches the two market views there. Reconciliation is also where a price reported in a currency other than its geography's own is converted, once, at the rate captured with that data. From then on, every price stays in its geography's own currency and is never converted or combined across currencies.

Qualitative documents arrive by ingestion path. The path sets whether a document is a regulatory filing, licensed third-party commentary, or an internal analyst note, and with that, how credible the document counts. Extraction reads each document first. A document stating no event in any driver category is skipped. Only a complete Driver Signal is stored, in its business unit's own namespace of the vector database. An extraction sent to the review queue is stored only once resolved, and a low-confidence match sent there is used only once settled. A figure a reviewer supplies or corrects takes the credibility of the document that states it. Where the figure comes from the reviewer's own knowledge, it takes the credibility of an internal analyst note. Predict computation reads both stores and the model registry. [`§ Architecture Overview § Diagrams § From Evidence to Answer`](#from-evidence-to-answer) pictures where each kind of evidence comes from and where it is stored.

Predict computation builds each forecast the same way, on the batch path or live. Each Driver Signal goes, by its event type, to exactly one consumer, so no signal is counted twice. The competitor's announced price change, or a change to its promotional calendar, adjusts the baseline. The baseline carries forward the competitor's own price trend, seasonality and promotional cadence. Every other signal goes to driver attribution. Driver attribution sizes each driver's correction from that driver's weight in a versioned rubric and from the magnitudes of the signals routed to that driver. For elasticity, a registered model's estimate stands in place of those magnitudes, and for competitor plans, a registered model's translation of the signal it was given. The forecast's move is exactly the baseline move plus those corrections.

Triangulation selects the signals routed to driver attribution that take effect inside the horizon. A selected signal may push price in a direction the baseline does not show, by enough to count as a move on its own. That signal still counts in its driver's correction. It is also flagged as a conflict, which is recorded and shown rather than averaged away silently. The confidence score weighs how credible the weakest source is, how current the data is, and whether a conflict was found. A conflict also caps the confidence score, however strong the rest is. The confidence band around the forecast comes from the forecasting models alone.

An answer is a set of records. Intent parsing turns a question into a Question Intent, which is not stored in either database. The records after it are stored in the structured database. A grid lookup, or Predict computed live, yields an Effective Price Forecast carrying its Rationale Record. The Rationale Record is what the forecast's baseline, drivers and confidence open to. The positioning engine produces Positioning Candidates, each carrying that same Rationale Record. The simulation engine produces a Simulated Outcome per candidate, and all of those outcomes share one Rationale Record, computed once for the question. A Delivered Answer records any answer for which Predict produced a forecast, whether or not Position and Simulate complete. It records the forecast the answer was built on, the candidates generated with their outcomes, the kind of decision the answer was given for, and the versions and data the answer was produced against. So the answer's positioning and simulation can be reproduced, as its forecast can. [`§ Architecture Overview § Diagrams § The Answer`](#the-answer) pictures this.

The services split along a different axis than the layers do. A query service runs the live path, which is request-driven and latency-sensitive. A materialization service runs the batch path, which is throughput-oriented and tolerant of long jobs. The materialization service runs its forecasts nightly, whenever competitor data refreshes, and on demand for one business unit. It runs its document extraction as the corpus refreshes. A control plane service is separated for a security reason, not a workload one. The control plane service alone holds write access to reference data and configuration. So a vulnerability in the far larger, far more exposed query surface can never reach the capability to change what a competitor's code means or what a business unit's threshold is.

The control plane service is also the client's own self-service surface. A Control plane admin tunes their own business unit there without Acme AI, while the forecasting mechanism itself stays with Acme AI. An Identity admin maps the customer's identity claims to business units and roles there. The control plane service also serves read-only views of the installation's pinned versions, audit retention and frontier model choice.

Across every service, the IdP-asserted claim is the enforcement boundary. The vector database is partitioned one namespace per business unit, with credentials issued per namespace. So a bug in application code cannot reach a namespace its credentials were never issued for. Every structured retrieval is filtered by that same claim at the query level. [`§ Architecture Overview § Diagrams § Trust Boundaries`](#trust-boundaries) pictures these boundaries: the services, the control plane's sole write path, and the claim checked at each.

[`§ Architecture Overview § Layer-to-Architecture Mapping`](#layer-to-architecture-mapping) is the row-by-row proof. It ties each piece of the product-facing answer to the mechanism that produces it, and cites the full detail behind each mechanism from that mechanism's own file.

[`§ Architecture Overview § Diagrams § Layer Composition`](#layer-composition) renders this composition, and [`§ Architecture Overview § Diagrams § Orchestration State Machine`](#orchestration-state-machine) renders the shape of a question's path through it. Both are for a reader who wants the picture before the proof.

### What Else These Services Run

Producing an answer is what the layers do, but it is not all these services run.

The same batch path that materializes forecasts also looks back at them, on the same cadence. Once a forecast's horizon has elapsed and real competitor data covers it, the materialization service computes how far the forecast was off and a verdict: Right, Right direction, or Wrong. Both are judged against what the forecast recorded when it was made. The materialization service stores both as a separate, later-arriving record, and never edits the original ([`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-tracking)).

The query service exposes one read-only report of every stored forecast with its evidence. Where a forecast's comparison with what happened has been computed, the report includes that comparison. The asker's existing claim scopes the report, and no new gating applies. The scope is a Control plane admin's own business unit, a Platform admin's escalated look at one, or every business unit an installation hosts. Run before any horizon has elapsed, that same report is the first health check after onboarding ([`specs/application/technical/query-service/evidence-and-accuracy-reporting.md § Bulk Evidence and Accuracy Report`](/specs/application/technical/query-service/evidence-and-accuracy-reporting.md#bulk-evidence-and-accuracy-report)).

Distinct kinds of record are kept alongside the answer path, and they are never folded together. An audit log of who did what is application data, not telemetry. The audit log is committed transactionally with the action it records, so an action and its record are never separated. It is retained for at least a year. A Platform admin can raise that period per a client's contractual requirement, and no routine path can lower it. The client reads the audit log on the control plane, each role reading the entries it may see. The audit log is exportable to someone with no access to the product. The export carries the record of what happened but never the answer content the record references.

The application's own telemetry, the logs, traces and metrics of how a request executed, is the opposite in almost every respect. Telemetry is kept for weeks. It carries none of the protected content the answer path handles: no forecast values, no document content, no credential material, no raw IdP claims. A forwarding agent ships telemetry to whatever observability platform the client already runs. Where the client runs none, the forwarding agent ships it to a viewer shipped alongside PriceHorizon. PriceHorizon needs no connection outside the client's environment to ship telemetry. It never sends telemetry to anything Acme AI hosts, and never combines it with another customer's.

An answer's own lineage, what produced one specific number, is neither. The lineage lives on the Effective Price Forecast and Delivered Answer rows the answer is made of ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance), [`specs/application/technical/data-model.md § Core Data Model § Audit Log`](/specs/application/technical/data-model.md#audit-log)).

Further mechanisms keep the design honest rather than serve a request. A golden-question harness runs in CI whenever a model, prompt template, or data pipeline version changes. The harness asserts that the structural rules this specification declares fire: a Decision Table row, an Algorithm step, a Constraint. Each rule carries at least one question written alongside it. The harness checks the declared rules, not whether a forecast came true. The realized outcomes are for that ([`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)). The upstream work feeding the grid may fail to resolve something confidently: a product match, or a document extraction that is ambiguous or incomplete. That item is flagged into a review queue for a Control plane admin rather than guessed at, before it ever reaches an answer ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Review Queue Item`](/specs/application/technical/data-model.md#review-queue-item)).

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
        RET --> PCL --> LOS
    end

    subgraph ControlPlane["Control plane service"]
        CFG["Reference data and configuration"]
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

**Caption:** The foundation, the layers, and the services this file describes. Predict computation appears in more than one service because it is one layer run on different cadences. Cadence is the axis on which layers and services differ.

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
        IDP["The customer's own IdP"]
        subgraph INST["PriceHorizon installation"]
            VAULT[("Secrets vault<br/>one scoped credential per service")]
            QS["Query service"]
            MS["Materialization service"]
            CP["Control plane service"]
            SDB[("Structured database")]
            VDB[("Vector database<br/>one namespace per business unit")]
        end
    end
    IDP -->|"a federated claim"| INST
    VAULT --> QS
    VAULT --> MS
    VAULT --> CP
    QS -->|"only the namespaces<br/>its credentials allow"| VDB
    QS -->|"every retrieval<br/>filtered by the claim"| SDB
    CP -->|"the only write path to<br/>reference data and configuration"| SDB
    QS -.-> FRONT(["A frontier model provider,<br/>seeing only what the client allows"])
    MS -.-> FRONT
```

**Caption:** The boundaries that keep each customer's data and configuration safe. The installation, and the customer's own IdP beside it, sit inside the customer's own environment, so signing in needs no connection outside it. A federated claim from the customer's own IdP is the enforcement boundary at every service. The customer's own people and Acme AI's own staff both reach that claim through accounts the client provisions. Local break-glass credentials in the vault, drawn dotted, apply only where that IdP cannot be reached. The vault issues each service its own credential. The vector database is reachable only through each namespace's own credentials. Every structured retrieval is filtered by the claim. The control plane is the only write path to reference data and configuration. A frontier model provider, drawn dotted, sits outside the customer's environment, and the query and materialization services reach it only with what the client lets it see.

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
    RECON -->|"low-confidence<br/>match"| RQ["Review queue"]
    EXT -->|"ambiguous<br/>or incomplete"| RQ
    RQ -->|"match settled"| SDB
    RQ -->|"extraction resolved"| VDB
    SDB --> PC["Predict computation"]
    VDB --> PC
    REG[("Model registry")] --> PC
    PC --> EPF["Effective Price Forecast with its Rationale Record<br/>stored in the structured database"]
```

**Caption:** Where evidence comes from, what keeps unhelpful or incomplete evidence out of a forecast, where each kind is stored, and the forecast record its baseline, drivers and confidence open to.

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
    QI -->|"grid lookup,<br/>or Predict computed live"| EPF
    subgraph STORED["Stored in the structured database"]
        EPF["Effective Price Forecast<br/>with its Rationale Record"]
        PC["Positioning Candidates<br/>each carrying the forecast's Rationale Record"]
        SO["A Simulated Outcome per candidate<br/>sharing one Rationale Record, computed once"]
        DA["Delivered Answer<br/>for any answer with a forecast"]
        EPF -->|"positioning engine"| PC
        PC -->|"simulation engine"| SO
        EPF -.->|"built on"| DA
        PC -.->|"the candidates generated,<br/>with their outcomes"| DA
    end
```

**Caption:** The records an answer is made of: which stage produces each, which are stored, and what a Delivered Answer records for any answer for which Predict produced a forecast, whether or not Position and Simulate complete.

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
- [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-packaging-extended)
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
    INTENT -->|"no business unit access"| DENIED(["Denied"])
    INTENT -->|"business unit unsettled,<br/>entities do not resolve uniquely,<br/>or the kind of decision is unsettled"| CLARIFY(["Clarifying question"])
    INTENT -->|"cannot complete"| PF(["No forecast; the answer<br/>says one could not be computed"])
    INTENT -->|"resolves"| PREDICT["Predict"]
    PREDICT -->|"cannot complete"| PF
    PREDICT --> POSITION["Position"]
    POSITION -->|"cannot complete"| POSF(["Forecast returned,<br/>labeled incomplete"])
    POSITION --> SIMULATE["Simulate"]
    SIMULATE -->|"cannot complete"| SIMF(["Forecast and options returned,<br/>labeled incomplete"])
    SIMULATE --> RENDER["Narrative rendering"] --> AP(["Answer produced"])

    classDef stop fill:#f4f4f4,stroke:#777,color:#222
    classDef done fill:#e8f2e8,stroke:#4a7,color:#222
    class DENIED,CLARIFY,PF,POSF,SIMF stop
    class AP done
```

**Caption:** The orchestration State Machine, collapsed to this file's own altitude. Each stage's internal states go unnamed here, as this file's prose leaves them. The full breakdown stays in the State Machine's States and Transitions tables.

**Sources:**
- [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`](/specs/application/technical/engineering-and-production-considerations.md#orchestration)

### Layer-to-Architecture Mapping

The seam between this file and the product's own Answer Engine domain ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do), [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit), [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business), [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage), [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context)). Every product-facing layer traces to one mechanism here. Nothing in the answer experience exists without a corresponding piece of this architecture. Predict's layers are typically served from the [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) materialized grid. The live [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation) mechanism is the fallback when a query falls outside that grid.

**Reference Key:** Product Layer

**Required:** Stage, Technical Mechanism

| Product Layer | Stage | Technical Mechanism |
|---|---|---|
| Scorecard / heatmap | Predict | Forecast materialization ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)), or, outside the grid, the same Predict computation run live ([`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation)); Brand A's current price is retrieved ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`](/specs/application/technical/query-service/intent-and-retrieval.md#parallel-evidence-retrieval)), not modeled |
| Plain-language narrative | Predict | Narrative rendering ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Narrative rendering`](/specs/application/technical/query-service/layered-output-synthesis.md#narrative-rendering)), generated live from the rationale record, constrained to its fields, not precomputed or stored |
| Geographic visualization | Predict | Materialized grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)) rendered directly as a map ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`](/specs/application/technical/query-service/layered-output-synthesis.md#layered-output-synthesis-producing-the-answer)); allocation below the grid's native geography ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Decomposition graph | Predict | Driver Attribution contribution breakdown ([`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution)), rendered as a driver chart, alongside the baseline and its evidence ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)); not available below the materialized grid's geography, where no causal signal was computed |
| Evidence view, per driver | Predict | driver_evidence in the Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), populated during Driver Attribution ([`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution)) from the same Driver Signal or model source the computation used |
| Confidence, per reason | Predict, Position, Simulate | `confidence_components` and `conflicts` in the Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), written by [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging`](/specs/application/technical/predict-computation.md#confidence-and-rationale-packaging) for Predict and Position, and by [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-packaging-extended) for a Simulated Outcome, whose record carries no `conflicts` |
| Options frame | Position | Positioning engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`](/specs/application/technical/query-service/layered-output-synthesis.md#positioning-engine)): fixed archetype rules applied to the Predict output and seeded by decision type ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Seeding`](/specs/application/technical/query-service/layered-output-synthesis.md#seeding)), not an optimizer, also taking Brand A's current price, margin targets and elasticity model, with candidates consolidated after simulation ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation`](/specs/application/technical/query-service/layered-output-synthesis.md#option-consolidation)) |
| Outcome comparison | Simulate | Simulation engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)): share, volume, and margin models run once per candidate; category growth aggregated from those outputs, revenue calculated directly as price times volume |
| Drill-down, granularity within the grid | All | Question Intent re-executed at narrower geographic scope inside the materialized grid, same model versions and weights ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Drill-down, granularity below the grid | All | Allocation of the same figure at the nearest grounded geography above it, by population or retail-footprint weighting, distinct confidence tier; decomposition graph unavailable, not inherited or recomputed ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Drill-down, metric pivot | All | Existing output re-projected onto a different metric field; new model call only if that metric was not already computed ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics)) |
| Decision context shown with every answer | All | Session context ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Session context`](/specs/application/technical/query-service/intent-and-retrieval.md#session-context)), carried on each question request; intent parsing settles the business unit and kind of decision each question is given for, its own words over the session's ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](/specs/application/technical/query-service/intent-and-retrieval.md#business-unit), [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](/specs/application/technical/query-service/intent-and-retrieval.md#decision-type)); every answer returns both, and the kind of decision seeds the positioning engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Seeding`](/specs/application/technical/query-service/layered-output-synthesis.md#seeding)) |
