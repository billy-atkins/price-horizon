## Core Data Model

### Harmonized quantitative foundation

Syndicated retail data (pricing, volume, share), internal POS and trade history, elasticity models, tax and regulatory tables, and macroeconomic indicators land in a single harmonized environment, versioned and timestamped. Every metric has one canonical definition and one source of truth. This environment is a structured database, the counterpart to the vector database. It offers exact keys, joins, and aggregation, not semantic search. Nearly everything in this file other than the Driver Signal needs those. Exchange rates are ingested here too, as one more macroeconomic indicator. Each Data Vintage (`§ Core Data Model § Reference and Master Data § Data Vintage`) captures them the same way it captures every other input. `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization` states where and how a rate is used.

This file gathers in one place the structures that the query service, the materialization service, and the control plane reference. Each was defined in prose where it is first produced. This file is their one home, so a later reference cites a field here instead of restating it. Several structures nest inside others. A Positioning Candidate carries its own Rationale Record and Simulated Outcome. A Simulated Outcome carries its own Rationale Record in turn, and so does an Effective Price Forecast.

A field table states what an entity is made of. It states no rule, no process, and no state the entity moves through. The rules that govern these structures are modeled separately, in the constructs, elsewhere in these files: how an event type routes, how the business unit is resolved, how candidates consolidate. Those rules cite this file's tables for the shape of the data they operate on.

These structures live in separate stores, not one. The Driver Signal lives in the vector database (`§ Core Data Model § Vector Database Schema`). The vector database is partitioned into one namespace per business unit, keyed by the Business Unit's stable code. A query against it is scoped by the namespace the connection reaches, not by a filter applied after the fact to a shared index. Every other structure lives in the structured database this section describes: Signal Routing Rule, Rationale Record, Positioning Candidate, Simulated Outcome, Product and Geography Match, Effective Price Forecast, Realized Outcome, Answer Provenance, Delivered Answer, and Review Queue Item. These need exact-key lookups and aggregation rather than similarity search. A Rationale Record cites Driver Signals by reference instead of duplicating them, and that reference is the one place the two stores meet. The Question Intent is the exception to both stores. It lasts only for the life of a request. It is held in the question-intent cache described in `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations`, and neither store persists it.

Business Unit, Geography, and Competitor are reference tables, not per-instance records. Each carries separate identifiers that do different jobs. A sequential integer id serves foreign keys and join performance within the structured database, the normal relational pattern. A stable code serves wherever these entities cross into the vector database, or must be legible to a person or an agent reading them directly. The code is ISO 3166 for a geography where it applies, a public ticker symbol for a competitor that has one, and an assigned short code for a business unit. Structured-database tables reference these entities by integer id. The vector database has no join mechanism and no relationship to those integers. It references them by code, the one identifier both stores can use without translation.

A code contains only uppercase letters, digits, and hyphens. It holds no whitespace and nothing that would need URL encoding. That lets it go straight into a path segment, a query parameter, an API response, or a log line without transformation. Codes are validated and normalized to uppercase at entry. A code locks at its first use by ingested data, as `specs/application/technical/control-plane-service/control-plane.md § Control Plane` governs. First use means the first reference to the entity the code names, from a structured-database foreign key or a vector-store Driver Signal. The code locks because the vector database has no cheap way to cascade a code change across every chunk that already carries the code. In the structured database, only the reference table's row would need to change.

The structured database is a star schema. The Effective Price Forecast is the fact, and Business Unit, Geography, and Competitor are dimensions. This section's surrogate-id-plus-code pattern is what a dimension table is for. Geography stays a star rather than snowflaking into separate Country, State, and Metro tables. A self-referencing parent within the one table supports the country-to-state-to-metro rollup the drill-down needs. It avoids the extra joins a fully normalized hierarchy would add to every query. For an analytical workload, minimizing joins matters more than the storage a snowflake schema would save. The Rationale Record does not flatten into the fact row. Its variable-length fields belong in related tables hung off the fact by foreign key. Horizon has only a few fixed values, so it is a plain fact attribute, not a dimension. The data snapshot a forecast was computed against is a small dimension of its own. A Data Vintage table records when each data snapshot was taken and which source data refresh it holds. Many facts share one vintage, and repeating that metadata on every row would be pure redundancy.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`, `specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`, `specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

### Vector Database Schema

The one entity stored in the vector database, embedding and structured fields together. It is stored there because retrieving it needs semantic search.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` render this.

#### Driver Signal

Produced by extraction in `specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`, zero or more per ingested qualitative document. A Driver Signal is the durable record behind the qualitative guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`).

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| source_type | One of the bounded types: regulatory filing, licensed third-party commentary, or internal analyst note. The ingestion path the document arrived through sets it |
| credibility_tier | Derived directly from source_type, in the order `specs/application/product/answer-engine/predict.md § Predict: what will the competitor do` states, and never judged per document |
| driver_category | One of the qualitative drivers Driver Attribution scores: tax, competitor plans, input costs, or discretionary spending. Elasticity has no qualitative counterpart |
| entity | The competitor or business unit the signal concerns, by code. It is neither free text nor an internal id, since this record lives in the vector database |
| geography | The location the signal concerns, by code |
| business_unit | The Business Unit code this signal is scoped to, so retrieval never crosses business units sharing one installation |
| event_type | A bounded value within the driver category. Each value has a declared `routes_to` value in `§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule` |
| direction | Increase, decrease, or neutral, as the source document states it |
| magnitude | A numeric value or bracket. `specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction` holds back from forecasts a signal lacking what it needs to be sized |
| effective_date | When the event takes effect, distinct from the document's publish date |
| extraction_confidence | How confident the extraction step is that it parsed the document correctly, separate from credibility_tier |
| extraction_model_version | The version of the driver signal extraction model that produced this record |
| source_citation | A pointer to the underlying chunk in the vector database, the evidence behind the rationale trace |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

### Reference and Master Data

Reference tables and crosswalks, edited through the control plane's self-service surface. They change far less often, and far less independently, than the pipeline artifacts.

#### Business Unit

A reference table, not a per-instance record, with one row per business unit the installation hosts.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key, used for foreign keys from other structured-database tables |
| code | A short, stable code, set once during onboarding and never reused, even if the business unit is later renamed. It is the natural key in the vector database and anywhere legibility matters |
| name | Display name |

`§ Core Data Model § Reference and Master Data § IdP Claim Mapping` records which IdP claims map to this business unit, and with what role. That mapping is not a field here, since one business unit can have several claims mapping to it at different roles.

#### Geography

A reference table, with one row per geography the harmonized foundation or the materialized grid references. Every price, price gap, and revenue figure computed at a geography is denominated in that geography's resolved currency. `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization` converts any input reported in another currency, once. At query, aggregation, or reporting time, the system never blends a figure from one geography with a figure from another geography that uses a different currency, so a business unit spanning more than one country, or a country with more than one currency of its own, always sees each geography's figures in that geography's currency downstream. It never sees a converted or summed total.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | ISO 3166-1 for country, ISO 3166-2 for state or province, and an assigned code for the metro level, where no public standard applies |
| name | Display name |
| currency | ISO 4217 currency code. A geography's resolved currency is the geography's value here if set, otherwise its nearest ancestor's. A country-level row, one with no parent_geography_id, always has a non-null currency, enforced when the row is created (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`), so the walk up the hierarchy always terminates. In the ordinary case, a whole country shares one currency, set once at the country row and inherited by everything beneath it. The rare country that uses more than one currency across its regions overrides it at whichever level needs one. `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics` states how a below-grid drill-down allocation's currency is set |
| parent_geography_id | Self-referencing foreign key. A metro's parent is its state, and a state's parent is its country. This is the star schema's flattened hierarchy, used instead of separate tables per level |

#### Competitor

A reference table, with one row per competitor in scope for any business unit.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | A public ticker symbol where the competitor has one, an assigned code otherwise |
| name | Display name |

#### Entity Alias

A many-to-one crosswalk: several aliases can resolve to one Competitor or Business Unit. It follows the same reconciliation pattern as Product and Geography Match, applied to names instead of catalog identifiers.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| alias_text | The name or code as it appears in a specific source, not yet resolved |
| entity_type | Competitor or Business Unit: the reference table this alias resolves against |
| entity_id | Foreign key to the matching row in that reference table |
| source_channel | The ingestion channel or source type that uses this alias, where known |

A rebrand, or a data vendor's own naming convention, is a new row here, not a change to the reference table's id or code. The reference table's name field is only the current display name, a convenience. Resolution always runs against this table, which holds every current and historical name, so a competitor's forecast history stays attached to one identity across a name change instead of fragmenting into two. An alias adds a row and changes no id or code that a Product and Geography Match or Effective Price Forecast already references, so adding one, a rebrand included, never invalidates a cell already materialized or a materialization run in flight. It only lets resolution find the same entity under one more name. alias_text is exempt from the code format rule `§ Core Data Model § Harmonized quantitative foundation` states. Its job is to capture a source's naming exactly as it appears, spaces, mixed case, punctuation and all. It is not a second code.

#### Glossary Term

Declared as a governed table (`specs/application/technical/glossary-and-grounding.md § Guaranteed grounding`), the same discipline `§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule` applies to a different bounded set. It has that table's shape too: its bounded name is the natural key, in place of a surrogate id. It is not per-business-unit data. It holds one entry per term the governed glossary defines.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| term | The bounded name: effective price, price gap, relative price index, category growth, and the rest of the governed vocabulary |
| resolves_to | The schema field or model endpoint this term maps to |

Adding a term here changes the governed vocabulary itself, so it is an application release. A business unit's alternate phrasing for a term already declared here belongs in `§ Core Data Model § Reference and Master Data § Glossary Alias` instead, never in a new row of this table.

#### Glossary Alias

A many-to-one crosswalk: several aliases can resolve to one Glossary Term. It follows the same reconciliation pattern as Entity Alias, applied to business vocabulary instead of entity names.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| alias_text | The phrasing as it appears in a business unit's usage, not yet resolved |
| term | The Glossary Term this alias resolves to, matched by the term's bounded name |
| business_unit_id | Foreign key to Business Unit. An alias is scoped to the business unit that registered it, unlike the governed term itself |

#### Data Vintage

A dimension, with one row per data snapshot the pipeline has ever computed against. `§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`, `§ Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`, and `§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance` reference it.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| computed_at | When this data snapshot was taken |
| source_data_snapshot | The identifier of the underlying competitor data refresh this vintage was computed against |

#### IdP Claim Mapping

A crosswalk, not a per-instance record, with one row per claim value the customer's IdP asserts.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| claim_value | The claim or group value the client's IdP asserts |
| business_unit_id | Foreign key to Business Unit. Null for identity admin and platform admin claims (`specs/application/technical/identity-and-access.md § Business unit access, federated`, `specs/application/technical/identity-and-access.md § Platform admin access`) |
| role | query_user, control_plane_admin, identity_admin, or platform_admin |

Identity admin is the role that can edit this table. An Identity admin claim is scoped as `specs/application/technical/identity-and-access.md § Business unit access, federated` states. Self-service management of that claim belongs to the client's identity team, not to any single business unit's data steward.

A query user claim that sees every business unit is not a separate case. It is the multi-business-unit claim `specs/application/technical/identity-and-access.md § Business unit access, federated` describes, with one mapping row per currently existing business unit instead of a wildcard. A new business unit does not extend an existing claim's reach on its own. Whoever manages a claim, identity admin for an org-wide one, adds the new mapping row, the same way any multi-business-unit claim gains a newly added business unit.

### Pipeline and Answer Artifacts

Structures the query and materialization services produce as they compute and package an answer. Each is defined in prose where it is first produced, and gathered here for its canonical field list.

#### Signal Routing Rule

Declared as a governed table (`specs/application/technical/predict-computation.md § Predict Computation § Signal routing`), not per-instance data, with one entry per bounded event type.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| event_type | The bounded name: announced price change, rate change, product launch, and so on |
| driver_category | Which of the qualitative drivers this event type belongs to |
| routes_to | Baseline (effective price forecasting) or driver attribution: the single downstream consumer of any signal carrying this event type |

#### Rationale Record

Produced by confidence and rationale packaging (`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging`) for the Predict output. Composition varies from there, as `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended` sets out. A Positioning Candidate's record is that same one. A Simulated Outcome has a record of its own. That record never carries driver_contribution_breakdown, driver_evidence, baseline, baseline_evidence or conflicts. Those fields are specific to the Predict computation and have no equivalent for a model-based simulation output. A Simulated Outcome's confidence_components are model confidence and model freshness, not the source-credibility, data-freshness, and triangulation-agreement set the Predict output and Positioning Candidate share.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| retrieval_trace | What was pulled, from where, and as of when, for every input this answer depended on |
| driver_contribution_breakdown | The full per-driver breakdown from Driver Attribution, covering every driver, not only the largest. These are the values the decomposition graph renders. Each contribution is in the resolved currency of the forecast's geography |
| driver_evidence | Per-driver evidence, one entry per driver in driver_contribution_breakdown. A signal-backed driver's entry references the Driver Signal(s) behind its magnitude. Elasticity is always model-only, so its entry holds the model name and the model's registry last-validated date (`specs/application/technical/model-registry.md § Model registry`) instead. The competitor plans entry holds both the Driver Signal reference and that same model detail, since the model only translates a signal it was given. A driver Driver Attribution scored at zero has an explicit no-signal marker |
| confidence_score | The overall confidence attached to this answer or candidate |
| confidence_components | The inputs the score is derived from. The set depends on which structure carries this record. The Predict output and a Positioning Candidate use source credibility, data freshness, and triangulation agreement. A Simulated Outcome uses model confidence and model freshness. Each component names what set it. For source credibility, that is the Driver Signals at the lowest credibility_tier. For data freshness, it is the data-as-of snapshot and each contributing Driver Signal's effective_date. For triangulation agreement, it is the entries in conflicts. For model confidence and model freshness, it is the model that set each. A Simulated Outcome's components also record whether the cap at the parent Positioning Candidate's score lowered the Simulated Outcome's own confidence_score |
| baseline | The baseline move and its direction, from `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting [Step: 5]` and `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting [Step: 6]`, in the resolved currency of the forecast's geography. The baseline and driver_contribution_breakdown together sum to the forecast's move |
| baseline_evidence | What the baseline was built from, which a Query user sees on opening the baseline (`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`). It holds the price-history snapshot, the forecasting models that carried it forward with each model's last-validated date, and every Driver Signal routed to the baseline that adjusted it |
| conflicts | Each conflict `specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution` flagged: the baseline's direction, the Driver Signal that disagrees with it, and that signal's contribution. Empty when none was flagged |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

#### Question Intent

Produced by intent parsing and decoupling (`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`).

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| metric | The quantity the question is about, price by default |
| business_unit | Resolved by the Decision Table in `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit` |
| entities | The competitor and brand the question concerns, resolved against the glossary, by code once resolved |
| geography | The location scope of the question, by code once resolved |
| horizon | The time window the forecast is asked for |
| decision_type | Strategic or tactical, settled by `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type` from the question's decision words or the kind of decision the request carries. It decides which archetypes the positioning engine seeds |
| granularity | The geographic or metric level implied by the question, validated against the glossary before anything executes |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Positioning Candidate

Produced by the positioning engine (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`), one per seeded archetype. Each candidate is held by one of the options `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation` leaves.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| archetype | Hold, Match, Close the Gap, or Diverge |
| resulting_effective_price | Brand A's price under this archetype's rule, at the query's geography and horizon, in that geography's resolved currency |
| price_gap | The absolute difference between resulting_effective_price and the competitor's forecast price, both already in the same geography's resolved currency |
| relative_price_index | The same comparison as a ratio, times 100 |
| rationale | The same Rationale Record produced for the Predict output (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended`). A copy is attached here, so this candidate's confidence and driver breakdown are visible without navigating back to Predict |
| simulated_outcome | A Simulated Outcome specific to this candidate. Null when simulation did not complete for this answer, the outcome `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: simulate_failed]`. The forecast and this candidate still stand on their own in that case |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Simulated Outcome

Produced by the simulation engine (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`), once per positioning candidate, in parallel across candidates.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| share | Projected share impact of this candidate, from the share-response model |
| volume | Projected volume impact, from the volume model |
| category_growth | Aggregated from the share and volume outputs at the category level, not a separate model |
| revenue | Calculated directly as price times volume, not a model call, in the resolved currency of the query's geography |
| margin | Projected margin impact, from the margin model |
| rationale | A Rationale Record scoped to Simulate, computed by `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended` |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Product and Geography Match

Produced by reconciliation (`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation`). The two are related but distinct structures.

**Table Name:** Product Match

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| competitor_product_id | The competitor's own product identifier, as reported in syndicated data |
| brand_a_product_id | Brand A's corresponding internal product identifier. Nullable when no counterpart exists, the whitespace case |
| match_confidence | How confident the match is. A low-confidence match is flagged for review rather than forced through |
| match_method | Structured attribute matching or semantic matching, whichever produced the match |

**Table Name:** Geography Crosswalk

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| source_region_code | The competitor data provider's own regional code |
| geography_id | Foreign key to the Geography reference table entry the source region normalizes to. This normalization sets the materialized grid's geography ceiling |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

#### Effective Price Forecast

Produced by forecast materialization (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`), or live by `specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging` for a query the grid does not yet cover. There is one row per computation, whichever path produced it. A live-path computation is checked against this key before it runs, not after: competitor, business unit, geography, horizon, data_vintage_id, application_version, model_versions, and business_unit_configuration_version. If a row already matches every one of these, the row is retrieved instead of recomputed. The repeatable-answer guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`) covers unchanged data, application version, model versions, and business unit configuration together, so data_vintage_id alone is never enough to call two computations identical. Only a match on all of them together is. Once an off-grid query has been asked and answered, a repeat of it behaves like an in-grid query: a lookup, not a live computation. If nothing matches, the computation runs and its output is persisted as a new row.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| competitor_id / business_unit_id | Foreign keys to the Competitor and Business Unit reference tables, not codes. This record lives in the structured database and is queried by exact key |
| geography_id | Foreign key to the Geography reference table. For a batch row, it is one entry in the organic grid set by reconciliation. For a live row, it is whatever geography the question asked for |
| horizon | For a batch row, one of the standard set the grid materializes (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`). A live row carries whatever horizon the question asked for, inside or outside that set |
| computed_via | Which path produced this row: batch (a materialization run) or live (a live-path query, `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked)`). It lets a bulk reviewer tell a real, question-triggered answer from routine eager pre-computation |
| data_vintage_id | Foreign key to the Data Vintage dimension (`§ Core Data Model § Reference and Master Data § Data Vintage`), the data snapshot this forecast was computed against |
| application_version | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`). Captured once when this row is produced, at materialization time for a batch row or at query time for a live row. It is never updated afterward, the same non-mutation discipline applied to the forecast itself |
| model_versions | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured when this row is produced. Scoped to only the forecasting and driver attribution models this row's Predict computation invoked, never the positioning or simulation models a live answer might also invoke on top of it |
| business_unit_configuration_version | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured when this row is produced. A stale cell, batch or live, can then report the configuration version it was produced under, instead of silently reflecting whatever configuration is current when it is later read |
| forecast | Direction of the effective price move, and the move itself, signed. The size of the move is its magnitude. Magnitude is denominated in geography_id's resolved currency (`§ Core Data Model § Reference and Master Data § Geography`), already normalized in `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`, whatever currency the underlying data feed originally reported |
| confidence_interval_lower / confidence_interval_upper | This forecast's confidence interval around the forecast's move, placed by `specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution [Step: 9]` from the forecasting models' combined offsets, in the same resolved currency as magnitude. It lives alongside the forecast's value and model_versions, since it is a property of what the named forecasting models produce, not of the qualitative evidence trail behind the forecast. The confidence_score and confidence_components on the attached Rationale Record instead summarize how much to trust the number overall, weighing source credibility, data freshness and triangulation agreement. That is why the interval and the score can diverge. Precise models can still sit behind a lower-confidence answer if a driver rests on a weakly sourced or stale fact |
| starting_effective_price | The competitor's current effective price this forecast's move starts from, as `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting [Step: 5]` takes it, in geography_id's resolved currency. It is kept so the realized move can be measured from the same start |
| dead_zone_threshold | The business unit's dead-zone threshold in effect when this row was produced, the one `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting [Step: 6]` applied. It is kept so this forecast is always judged by that threshold |
| rationale | A Rationale Record for this forecast, retrieved as a lookup rather than recomputed for any query landing inside the grid |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

#### Delivered Answer

Produced by the query service as the final step of assembling any answer that reaches at least Predict. That holds whether Predict was a grid lookup or a live computation, and whether or not Position and Simulate also complete (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`). There is one row per question answered, in full or in degraded form. Every question_asked reaching Predict gets one, not only the off-grid case. A Delivered Answer exists only when a forecast was produced. It is created for a question_asked outcome of `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: answer_produced]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: position_failed]`, or `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: simulate_failed]`. It is never created for `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: query_denied]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: clarification_needed]`, or `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: predict_failed]`, where there is nothing yet to have lineage over.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| effective_price_forecast_id | Foreign key to the Effective Price Forecast (`§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`) this answer was built on. Always populated, since a Delivered Answer exists only once Predict has completed |
| positioning_candidates | The set of Positioning Candidates (`§ Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`) generated, each already carrying its own Rationale Record per the Positioning Candidate definition. A candidate's `simulated_outcome` field is null when the outcome was `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: simulate_failed]`. This whole field is empty when the outcome was `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: position_failed]` |
| decision_type | The kind of decision this answer was given for, the session's or the question's. It is shown with the answer, and it is the one the answer's candidates were seeded by |
| rendered_narrative | The complete natural-language text delivered, across whichever stages were reached. `specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior` covers a partial answer's labeling text as part of this. Captured directly because the repeatability guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`) explicitly allows this wording to vary between runs, unlike everything else on this row |
| application_version | This delivery's own Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured directly when this row is produced |
| model_versions | Same Answer Provenance capture: every model this delivery invoked, Predict's, Position's, and Simulate's alike, not only Predict's |
| language_model_versions | Same Answer Provenance capture: every language model this delivery called |
| business_unit_configuration_version | Same Answer Provenance capture |
| data_vintage_id | Same Answer Provenance capture: the Data Vintage (`§ Core Data Model § Reference and Master Data § Data Vintage`) this delivery's computation ran against |
| produced_at | When this row was created |

Each of a Delivered Answer's Answer Provenance fields can differ from the referenced Effective Price Forecast's pinned value of the same name. A query served from the grid can reuse an Effective Price Forecast row computed days or weeks earlier. Position and Simulate still run fresh, against whatever versions and data vintage are current at this later moment, so the forecast's provenance and this delivery's provenance are different facts, not one fact restated. This row is what makes `specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`'s claim, that a live answer is "reproducible against an Answer Provenance... logged alongside it", true for Position and Simulate. Nothing on this row duplicates protected content that already has a canonical home. The forecast's substance stays behind effective_price_forecast_id and is never restated here.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Realized Outcome

Produced by realized outcome tracking (`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking`), at most one per Effective Price Forecast, once the forecast's horizon has passed and real data exists to check it against. The forecast it evaluates is never edited to match. An Effective Price Forecast stays exactly what was forecast at the time. A Realized Outcome is a separate, later-arriving record of what happened.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| effective_price_forecast_id | Foreign key to the Effective Price Forecast this outcome evaluates |
| actual_effective_price | The competitor's effective price observed for that combination once the horizon passed. It is decomposed the same way the original forecast was, in the same resolved currency as the forecast it is compared against |
| forecast_error | The forecast's move less the realized move, both measured from the forecast's starting_effective_price, in the same resolved currency as the forecast it evaluates. It is not an absolute value, so an over-forecast and an under-forecast can be told apart |
| verdict | Right, Right direction, or Wrong, set by `specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking` |
| realized_data_vintage_id | Foreign key to the Data Vintage the actual figure came from, distinct from the vintage the original forecast used |
| computed_at | When this comparison was computed |

#### Answer Provenance

Attached to every answer, per the repeatability guarantee in `specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`. For a live-path answer, it is assembled fresh from whatever application, model, and configuration state is current. For a query served from the materialized grid, the forecast's values are the ones `§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast` captured when that row was produced. The Delivered Answer built on that row captures its own at delivery, since Position applies the configuration current when the question is asked.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| application_version | The orchestration and logic version that produced this answer |
| model_versions | The version of every model invoked whose output is part of the numeric-determinism contract, one entry per model called. The narrative rendering model's version is recorded in language_model_versions instead, since that model's prose is not required to be identical across calls |
| language_model_versions | The provider and dated version of each language model that served this answer, one entry per kind of call it made, reasoning over the question and narrative rendering among them. Each is Acme AI's own hosted model or a frontier provider's (`specs/application/technical/model-registry.md § Model registry`). Kept apart from model_versions because these calls' output is not part of the numeric-determinism contract. So the record shows which model served an answer without making its prose a repeatability promise |
| business_unit_configuration_version | The version of this business unit's settings that shape an answer, keyed by business unit code for legibility in an audit trail, and raised as `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance` describes. The installation-wide governed vocabulary and archetype rules change only with application_version (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`) |
| data_vintage_id | Foreign key to the Data Vintage dimension (`§ Core Data Model § Reference and Master Data § Data Vintage`), the data snapshot everything was computed against |

#### Review Queue Item

The status of a single flagged item: a low-confidence product match (`§ Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`) or an ambiguous or incomplete document extraction (`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`). These are the cases `specs/application/product/tenant-administration/review-queues.md` commits to the client reviewing. Each is a durable record, and resolving one produces a corrected record that every future query benefits from. A low-confidence answer is not another such case. It is the output of one query at one moment, not a record with anything to correct. The confidence guarantee itself (`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`) handles it, and it is surfaced to the user directly, not queued for review.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| flagged | Flagged at the point of computation, by a confidence threshold or an incomplete extraction. No reviewer has seen it yet | Yes | No |
| under_review | A Control plane admin has opened the item | No | No |
| resolved | A reviewer has confirmed the underlying record needed no change, corrected it, or supplied the figure it was missing. The record is used | No | Yes |
| dismissed | A reviewer has found the underlying record cannot be made usable, such as an incomplete extraction whose missing fact no source states. The record stays unused | No | Yes |

**Table Name:** Transitions

| From | To | Trigger |
|---|---|---|
| flagged | under_review | A Control plane admin opens the item |
| under_review | resolved | The reviewer confirms the match or extraction needed no change |
| under_review | resolved | The reviewer corrects the match or extraction |
| under_review | resolved | The reviewer supplies the figure the extraction is missing |
| under_review | dismissed | The reviewer finds the match or extraction cannot be made usable |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

### Audit Log

#### Audit Log Entry

Produced by every action that the populations this entry covers take:

- Acme AI's Platform admin access against an installation, whether through a federated claim or break-glass credentials;
- a Query user's question, the system's core activity, not an afterthought sharing a mechanism built for someone else;
- a Control plane admin's or an Identity admin's change to what they govern;
- an installation's record of a change to the kinds of model call it lets reach a frontier model provider (`specs/application/technical/model-registry.md § Model registry`).

All are governed the same way, per `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`. Break-glass retrieval also has its own vault-native audit trail (`specs/application/technical/secrets-management.md § Secrets management`). This entry covers the broader case: every other Platform admin action, alongside every Query user question and every Control plane admin's and Identity admin's change. Those Platform admin actions include accessing the application logs and traces that `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance` describes separately.

**Reference Key:** Field

**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| actor | The identity that performed the action. For a Platform admin, it is the identity that the access path, federated claim or break-glass, asserts. For a Query user, Control plane admin or Identity admin, it is that person's IdP-asserted claim. For a retention_purge or frontier_models_changed entry only, it is a fixed system identity, since no claim initiates either. A retention_purge run is automated, and a frontier_models_changed entry records a change the client's own infrastructure team made in the installation's configuration |
| actor_role | query_user, control_plane_admin, identity_admin, platform_admin or client_infrastructure. It is the role whose claim authorized this action, or, for an entry no claim initiated, the party responsible for it. Entries from every population share one table, and this field keeps them from being confused with each other. A retention_purge entry is platform_admin, by the same automated-mechanism-belongs-to-Acme-AI reasoning applied to every other installation-wide governed action. A frontier_models_changed entry is client_infrastructure, since the change is the client's own and never Acme AI's |
| action_type | A closed, governed set, not an extensible category: onboarding, upgrade, diagnostic support session, diagnostic log access, pinned_versions_viewed, question_asked, configuration_changed, retention_purge, frontier_models_changed, nothing else. pinned_versions_viewed is a Platform admin's read of the installation's pinned versions (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`). frontier_models_changed is an installation's record, made as the installation starts, of a change to the kinds of model call its configuration lets reach a frontier model provider (`specs/application/technical/model-registry.md § Model registry`). An installation that never names one never records it. Every capability any of these roles has is already enumerated elsewhere in this system. `specs/application/technical/control-plane-service/control-plane.md § Control Plane`'s Decision Table covers every self-service and governed configuration surface, and `specs/application/product/roles.md § Roles` covers what each role can do, so no action outside this set would ever need auditing. Adding one is a real change to this schema, decided deliberately, never a runtime category left open for a future action to fall into on its own |
| business_unit_id | Foreign key to Business Unit where the action was scoped to one. Null wherever none was: an installation-wide Platform admin action such as an upgrade, a governed configuration_changed edit such as the retention period itself, a retention_purge or frontier_models_changed entry, or a question_asked entry that ended before any business unit was resolved. A configuration_changed entry against a business-unit-scoped setting carries that business unit. One against an IdP claim mapping carries the business unit its mapping row names, before or after the change. Such a change has one entry for each business unit it touches. Where the row names no business unit, as for a Platform admin or Identity admin mapping, it has a single entry with business_unit_id null |
| occurred_at | When the action took place |
| outcome | Whether the action succeeded: success or failure, for every action_type except question_asked. For a question_asked entry, it is the Orchestration State Machine's terminal state: `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: answer_produced]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: query_denied]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: clarification_needed]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: predict_failed]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: position_failed]`, or `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: simulate_failed]` |
| delivered_answer_id | For a question_asked entry whose outcome was `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: answer_produced]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: position_failed]`, or `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: simulate_failed]`, a foreign key to the Delivered Answer (`§ Core Data Model § Pipeline and Answer Artifacts § Delivered Answer`) that answer produced. The Delivered Answer is the complete record of what was shown and what produced it. Null for `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: query_denied]`, `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: clarification_needed]`, and `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration [States.State: predict_failed]`, where no forecast was ever produced, and null for every action_type other than question_asked |
| changed_field | For a configuration_changed entry only, the configuration surface edited, self-service or governed alike. `specs/application/technical/control-plane-service/control-plane.md § Control Plane`'s Decision Table names the bounded set, including the installation-wide audit log retention period itself. Null otherwise |
| previous_value / new_value | For a configuration_changed or frontier_models_changed entry only, the setting's value before and after the change, as a plain comparable string whatever the underlying field's type. For a frontier_models_changed entry, the value is the kinds of model call named, each with its pinned version, sorted. Both are null for a change to a data source's credentials: the fact of the rotation is logged, never the credential material, the same standing rule `specs/application/technical/secrets-management.md § Secrets management` applies everywhere else. Null for every other action_type. For an IdP claim mapping entry, only that entry's business unit's side of the change: the mapping as it stood there before and after, never the business unit on the other side of a move |

Only `previous_value` / `new_value`, for a configuration_changed or frontier_models_changed entry, carries content directly. That content is legitimate audit content: a record of what a human changed, not a record of what produced an answer. Every other field on Audit Log Entry, including `delivered_answer_id`, only ever records that an access occurred, or references the one row elsewhere that holds the substance. A retention_purge entry carries no count of what was removed, by design. A defensible record needs to prove that the process ran, on schedule, and that nothing eligible was skipped. It need not prove how many rows happened to qualify that day, a number with no lasting significance of its own.
