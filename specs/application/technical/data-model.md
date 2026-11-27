## Core Data Model

### Harmonized quantitative foundation

Syndicated retail data (pricing, volume, share), internal POS and trade history, elasticity models, tax and regulatory tables, and macroeconomic indicators land in a single harmonized environment, versioned and timestamped. Every metric has one canonical definition and one source of truth. This environment is a structured database, the counterpart to the vector database. It offers exact keys, joins, and aggregation, not semantic search. Nearly everything in this file other than the Driver Signal needs those. Exchange rates are ingested here too, as one more macroeconomic indicator. Each Data Vintage ([`§ Core Data Model § Reference and Master Data § Data Vintage`](#data-vintage)) captures them the same way it captures every other input. [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`](/specs/application/technical/materialization-service/reconciliation.md#currency-normalization) states where and how a rate is used.

This file gathers in one place the structures that the query service, the materialization service, and the control plane reference. Each is defined in prose where it is first produced. This file is their one home, so a later reference cites a field here instead of restating it. Several structures nest inside others. A Positioning Candidate carries its own Rationale Record and Simulated Outcome. A Simulated Outcome carries its own Rationale Record in turn, and so does an Effective Price Forecast.

Field tables define the stored data. Event routing belongs to [`specs/application/technical/predict-computation.md § Predict Computation § Signal route`](/specs/application/technical/predict-computation.md#signal-route), unit resolution to [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](/specs/application/technical/query-service/intent-and-retrieval.md#business-unit), and candidate grouping to [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation`](/specs/application/technical/query-service/layered-output-synthesis.md#option-consolidation).

These structures live in separate stores, not one. The Driver Signal lives in the vector database ([`§ Core Data Model § Vector Database Schema`](#vector-database-schema)). The vector database is partitioned into one namespace per business unit, keyed by the Business Unit's stable code. A query against it is scoped by the namespace the connection reaches, not by a filter applied after the fact to a shared index. Every other structure lives in the structured database this section describes: Signal Routing Rule, Rationale Record, Positioning Candidate, Simulated Outcome, Product and Geography Match, Effective Price Forecast, Realized Outcome, Answer Provenance, Delivered Answer, and Review Queue Item. These need exact-key lookups and aggregation rather than similarity search. A Rationale Record cites Driver Signals by reference instead of duplicating them, and that reference is the one place the two stores meet. The Question Intent is the exception to both stores. Each request resolves its own authorized intent. A short-lived cache may reuse the parsing result under the isolation rules in [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations`](/specs/application/technical/engineering-and-production-considerations.md#engineering-and-production-considerations), and neither store persists it.

Business Unit, Geography, and Competitor are reference tables, not per-instance records. Each carries separate identifiers that do different jobs. A sequential integer id serves foreign keys and join performance within the structured database, the normal relational pattern. A stable code serves wherever these entities cross into the vector database, or must be legible to a person or an agent reading them directly. The code is ISO 3166 for a geography where it applies, a public ticker symbol for a competitor that has one, and an assigned short code for a business unit. Structured-database tables reference these entities by integer id. The vector database has no join mechanism and no relationship to those integers. It references them by code, the one identifier both stores can use without translation.

A code contains only uppercase letters, digits, and hyphens. It holds no whitespace and nothing that would need URL encoding. That lets it go straight into a path segment, a query parameter, an API response, or a log line without transformation. Codes are validated and normalized to uppercase at entry. A code locks at its first use by ingested data, as [`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path) governs. First use means the first reference to the entity the code names, from a structured-database foreign key or a vector-store Driver Signal. The code locks because the vector database has no cheap way to cascade a code change across every chunk that already carries the code. In the structured database, only the reference table's row would need to change.

The structured database is a star schema. The Effective Price Forecast is the fact, and Business Unit, Geography, and Competitor are dimensions. This section's surrogate-id-plus-code pattern is what a dimension table is for. Geography stays a star rather than snowflaking into separate Country, State, and Metro tables. A self-referencing parent within the one table supports the country-to-state-to-metro rollup the drill-down needs. It avoids the extra joins a fully normalized hierarchy would add to every query. For an analytical workload, minimizing joins matters more than the storage a snowflake schema would save. The Rationale Record does not flatten into the fact row. Its variable-length fields belong in related tables hung off the fact by foreign key. Horizon has only a few fixed values, so it is a plain fact attribute, not a dimension. The data snapshot a forecast was computed against is a small dimension of its own. A Data Vintage table records when each data snapshot was taken and which source data refresh it holds. Many facts share one vintage, and repeating that metadata on every row would be pure redundancy.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition), [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`](/specs/application/technical/architecture.md#trust-boundaries), [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

### Vector Database Schema

The one entity stored in the vector database, embedding and structured fields together. It is stored there because retrieving it needs semantic search.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) render this.

#### Driver Signal

Produced by extraction in [`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`](/specs/application/technical/materialization-service/driver-signal-extraction.md#vector-and-semantic-mapping-with-structured-extraction), zero or more per ingested qualitative document. A Driver Signal is the durable record behind the qualitative guarantee ([`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)).

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| source_type | One of the bounded types: regulatory filing, licensed third-party commentary, or internal analyst note. The ingestion path the document arrived through sets it |
| credibility_tier | Derived directly from source_type, in the order [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do) states, and never judged per document |
| driver_category | One of the qualitative drivers Driver Attribution scores: tax, competitor plans, input costs, or discretionary spending. Elasticity has no qualitative counterpart |
| entity | The competitor or business unit the signal concerns, by code. It is neither free text nor an internal id, since this record lives in the vector database |
| product_scope | The products covered by the source for this event. Record the resolved brand codes when it names brands, or explicit coverage of the entire competitor portfolio or business-unit market when the source says so. An unresolved scope is held for review |
| geography | The location the signal concerns, by code |
| business_unit | The Business Unit code this signal is scoped to, so retrieval never crosses business units sharing one installation |
| event_type | A bounded value within the driver category. Each value has a declared `routes_to` value in [`§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule`](#signal-routing-rule) |
| direction | Increase, decrease, or neutral, as the source document states it |
| magnitude | A numeric value or bracket. [`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`](/specs/application/technical/materialization-service/driver-signal-extraction.md#vector-and-semantic-mapping-with-structured-extraction) holds back from forecasts a signal lacking what it needs to be sized |
| reported_unit | The source unit for a reported amount or bracket, including whether the change is in percentage points or currency per unit |
| measurement_basis | The documented base and its source for converting a direct effect to the forecast currency per unit. A direct rate without the applicable base cannot be sized and goes to review |
| effective_date | When the event takes effect, distinct from the document's publish date |
| extraction_confidence | How confident the extraction step is that it parsed the document correctly, separate from credibility_tier |
| extraction_model_version | The version of the driver signal extraction model that produced this record |
| source_citation | A pointer to the underlying chunk in the vector database, the evidence behind the rationale trace |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) renders this.

### Reference and Master Data

Reference tables and crosswalks, edited through the control plane's self-service surface. They change far less often, and far less independently, than the pipeline artifacts.

#### Business Unit

A reference table, not a per-instance record, with one row per business unit the installation hosts.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key, used for foreign keys from other structured-database tables |
| code | A short code assigned at registration and locked at first use under the foundation’s code rule. Renaming a unit preserves its locked code, and a retired code cannot be reused. It is the natural key in the vector database and anywhere legibility matters |
| name | Display name |

[`§ Core Data Model § Reference and Master Data § IdP Claim Mapping`](#idp-claim-mapping) records which IdP claims map to this business unit, and with what role. That mapping is not a field here, since one business unit can have several claims mapping to it at different roles.

#### Geography

A reference table, with one row per geography the harmonized foundation or the materialized grid references. Every price, price gap, and revenue figure computed at a geography is denominated in that geography's resolved currency. [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`](/specs/application/technical/materialization-service/reconciliation.md#currency-normalization) converts any input reported in another currency, once. Queries and reports keep figures in each geography’s resolved currency. Across geographies with different currencies, the report shows separate figures and omits a combined total.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | ISO 3166-1 for country, ISO 3166-2 for state or province, and an assigned code for the metro level, where no public standard applies |
| name | Display name |
| currency | ISO 4217 currency code. A geography's resolved currency is the geography's value here if set, otherwise its nearest ancestor's. A country-level row, one with no parent_geography_id, always has a non-null currency, enforced when the row is created ([`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path)), so the walk up the hierarchy always terminates. In the ordinary case, a whole country shares one currency, set once at the country row and inherited by everything beneath it. The rare country that uses more than one currency across its regions overrides it at whichever level needs one. [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics) states how a below-grid drill-down allocation's currency is set |
| parent_geography_id | Self-referencing foreign key. A metro's parent is its state, and a state's parent is its country. This is the star schema's flattened hierarchy, used instead of separate tables per level |

#### Competitor

A reference table, with one row per competitor in scope for any business unit.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | A public ticker symbol where the competitor has one, an assigned code otherwise |
| name | Display name |

#### Tracked brand membership

The governed reference set identifies the brands each business unit tracks. A membership revision is an immutable set for one unit. Resolve the revision effective at the run’s start and retain its identifier on the publication.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| business_unit_id / revision | The unit and revision owning this set. Effective intervals for successive revisions in one unit are disjoint, with an inclusive UTC start and exclusive end |
| competitor_id / brand_code | The competitor reference and stable brand code, unique together within the revision. Removing the pair from a later revision preserves earlier membership |

#### Entity Alias

A many-to-one crosswalk: several aliases can resolve to one Competitor or Business Unit. It follows the same reconciliation pattern as Product and Geography Match, applied to names instead of catalog identifiers.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| alias_text | The name or code as it appears in a specific source, not yet resolved |
| entity_type | Competitor or Business Unit: the reference table this alias resolves against |
| entity_id | Foreign key to the matching row in that reference table |
| source_channel | The ingestion channel or source type that uses this alias, where known |

A rebrand, or a data vendor's own naming convention, is a new row here, not a change to the reference table's id or code. The reference table's name field is only the current display name, a convenience. Resolution always runs against this table, which holds every current and historical name, so a competitor's forecast history stays attached to one identity across a name change instead of fragmenting into two. An alias adds a row and changes no id or code that a Product and Geography Match or Effective Price Forecast already references, so adding one, a rebrand included, never invalidates a cell already materialized or a materialization run in flight. It only lets resolution find the same entity under one more name. alias_text is exempt from the code format rule [`§ Core Data Model § Harmonized quantitative foundation`](#harmonized-quantitative-foundation) states. Its job is to capture a source's naming exactly as it appears, spaces, mixed case, punctuation and all. It is not a second code.

#### Glossary Term

Declared as a governed table ([`specs/application/technical/glossary-and-grounding.md § Guaranteed grounding`](/specs/application/technical/glossary-and-grounding.md#guaranteed-grounding)), the same discipline [`§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule`](#signal-routing-rule) applies to a different bounded set. It has that table's shape too: its bounded name is the natural key, in place of a surrogate id. It is not per-business-unit data. It holds one entry per term the governed glossary defines.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| term | The bounded name: effective price, price gap, relative price index, category growth, and the rest of the governed vocabulary |
| resolves_to | The schema field or model endpoint this term maps to |

Adding a term here changes the governed vocabulary itself, so it is an application release. A business unit's alternate phrasing for a term already declared here belongs in [`§ Core Data Model § Reference and Master Data § Glossary Alias`](#glossary-alias) instead, never in a new row of this table.

#### Glossary Alias

A many-to-one crosswalk: several aliases can resolve to one Glossary Term. It follows the same reconciliation pattern as Entity Alias, applied to business vocabulary instead of entity names.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| alias_text | The phrasing as it appears in a business unit's usage, not yet resolved |
| term | The Glossary Term this alias resolves to, matched by the term's bounded name |
| business_unit_id | Foreign key to Business Unit. An alias is scoped to the business unit that registered it, unlike the governed term itself |

#### Data Vintage

A dimension, with one row per data snapshot the pipeline has ever computed against. [`§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](#effective-price-forecast), [`§ Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`](#realized-outcome), and [`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`](#answer-provenance) reference it.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| computed_at | When this data snapshot was taken |
| source_data_snapshot | The identifier of the underlying competitor data refresh this vintage was computed against |

#### IdP Claim Mapping

Each unique combination of IdP claim value, role and scope has one mapping. A unit grant names an existing unit. Installation grants name their individual permission, including authorization for a client Control plane admin to register a business unit. An installation creation grant confers no unit role.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| claim_value | The claim or group value the client's IdP asserts |
| business_unit_id | Foreign key to Business Unit. Null for installation-scoped grants ([`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated), [`specs/application/technical/identity-and-access.md § Platform admin access`](/specs/application/technical/identity-and-access.md#platform-admin-access)) |
| role | query_user, control_plane_admin, identity_admin, or platform_admin |
| installation_permission | For a unit creation grant, register_business_unit with control_plane_admin and a null business_unit_id. Absent for ordinary unit grants |

Identity admin is the role that can edit this table. An Identity admin claim is scoped as [`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated) states. Self-service management of that claim belongs to the client's identity team, not to any single business unit's data steward.

A query user claim that sees every business unit is not a separate case. It is the multi-business-unit claim [`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated) describes, with one mapping row per currently existing business unit instead of a wildcard. A new business unit does not extend an existing claim’s reach on its own. The client-facing capability is [`specs/application/product/identity-and-access/identity-administration.md § Identity Administration`](/specs/application/product/identity-and-access/identity-administration.md#identity-administration). Whoever manages a claim, identity admin for an org-wide one, adds the new mapping row, the same way any multi-business-unit claim gains a newly added business unit.

### Pipeline and Answer Artifacts

Structures the query and materialization services produce as they compute and package an answer. Each is defined in prose where it is first produced, and gathered here for its canonical field list.

#### Signal Routing Rule

Declared as a governed table, not per-instance data, with one entry per bounded event type in the [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do § Event Type Taxonomy`](/specs/application/product/answer-engine/predict.md#event-type-taxonomy). The product section is the complete membership and routing contract; this schema states only the fields each stored rule carries.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| event_type | The bounded name of an event type declared in the [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do § Event Type Taxonomy`](/specs/application/product/answer-engine/predict.md#event-type-taxonomy) |
| driver_category | The event type's category, as declared there: competitor plans, tax, input costs, or discretionary spending |
| routes_to | The single downstream consumer declared there: Baseline for announced price change and promotional calendar change, or Driver Attribution for every other event type |

#### Rationale Record

Produced by the confidence and rationale package ([`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package)) for the Predict output. Composition varies from there, as [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-package-extended) sets out. A Positioning Candidate's record is that same one. A Simulated Outcome has a record of its own. That record never carries driver_contribution_breakdown, driver_evidence, baseline, baseline_evidence or conflicts. Those fields are specific to the Predict computation and have no equivalent for a model-based simulation output. A Simulated Outcome's confidence_components are model confidence and model freshness, not the source-credibility, data-freshness, and triangulation-agreement set the Predict output and Positioning Candidate share ([`specs/application/technical/model-registry.md § Open Questions [Name: Model Freshness in Predict]`](/specs/application/technical/model-registry.md#open-questions)).

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| retrieval_trace | What was pulled, from where, and as of when, for every input this answer depended on |
| driver_contribution_breakdown | The full per-driver breakdown from Driver Attribution, covering every driver, not only the largest. These are the values the decomposition graph renders. Each contribution is in the resolved currency of the forecast's geography |
| driver_evidence | For each driver retain the signals and model calls actually used, even when its net contribution is zero. Elasticity records its model and version. Competitor plans with a qualifying trigger records the trigger and the response model that sized it. Without a trigger it records no call and explains the absence. For a reported zero, zero model estimate, zero rubric weight or offsetting effects, retain the references, signed effects and weight that explain the result. |
| confidence_score | The overall confidence attached to this answer or candidate |
| confidence_components | Predict records the applicability, score, effective weight and supporting evidence for each component. For a forecast using qualitative signals, the evidence identifies the lowest-tier contributing sources, the snapshot and signal dates used for freshness, and any flagged conflicts. With no contributing signals, the record identifies snapshot freshness as the sole basis of the score and carries the reason "No qualitative signals contributed" for the two inapplicable components. A Positioning Candidate inherits this record. A Simulated Outcome identifies the models that determined model confidence and model freshness and records whether the parent candidate's score lowered its score. |
| baseline | The baseline move and its direction, from [`specs/application/technical/predict-computation.md § Predict Computation § Baseline forecast [Step: 5]`](/specs/application/technical/predict-computation.md#baseline-forecast) and [`specs/application/technical/predict-computation.md § Predict Computation § Baseline forecast [Step: 6]`](/specs/application/technical/predict-computation.md#baseline-forecast), in the resolved currency of the forecast's geography. The baseline and driver_contribution_breakdown together sum to the forecast's move |
| baseline_evidence | What the baseline was built from, which a Query user sees on opening the baseline ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). It holds the pinned component history, forecast window, list-price and promotional-depth model versions and validation dates, and the baseline Driver Signals. For the rebate and surcharge, it identifies the applicable term or the dated observation carried forward and the per-unit amount used |
| conflicts | Each conflict [`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution) flagged: the baseline's direction, the Driver Signal that disagrees with it, and that signal's contribution. Empty when none was flagged |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Question Intent

Produced by intent parsing and decoupling ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`](/specs/application/technical/query-service/intent-and-retrieval.md#intent-parsing-and-decoupling)).

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| metric | The quantity the question is about, price by default |
| business_unit | Resolved by the Decision Table in [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](/specs/application/technical/query-service/intent-and-retrieval.md#business-unit) |
| entities | The competitor and brand the question concerns, resolved against the glossary, by code once resolved |
| geography | The location scope of the question, by code once resolved |
| horizon | The time window the forecast is asked for |
| decision_type | Strategic or tactical, settled by [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](/specs/application/technical/query-service/intent-and-retrieval.md#decision-type) from the question's decision words or the kind of decision the request carries. It decides which archetypes the positioning engine seeds |
| granularity | The geographic or metric level implied by the question, validated against the glossary before anything executes |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

#### Positioning Candidate

Produced by the positioning engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`](/specs/application/technical/query-service/layered-output-synthesis.md#positioning-engine)), one per seeded archetype. Each candidate is held by one of the options [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation`](/specs/application/technical/query-service/layered-output-synthesis.md#option-consolidation) leaves.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| archetype | Hold, Match, Close the Gap, or Diverge |
| candidate_id | Stable within this Delivered Answer and equal to the canonical archetype code (Hold, Match, Close the Gap, or Diverge), once per seed. All membership, call and evidence references use this code scoped by the delivery ID, including when simulation is unavailable. Display labels are recorded separately |
| comparison_status | For each price or comparison, its availability and reason, including an unresolved product or geography match or an unusable price base. Available values are calculated before presentation rounding |
| resulting_effective_price | Brand A's price under this archetype's rule, at the query's geography and horizon, in that geography's resolved currency |
| price_gap | The absolute difference between resulting_effective_price and the competitor's forecast price, both already in the same geography's resolved currency |
| relative_price_index | The same comparison as a ratio, times 100 |
| rationale | The same Rationale Record produced for the Predict output ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-package-extended)). A copy is attached here, so this candidate's confidence and driver breakdown are visible without navigating back to Predict |
| simulated_outcome | A Simulated Outcome specific to this candidate. Null when simulation did not complete for this answer, the outcome [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: simulate_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run). The forecast and this candidate still stand on their own in that case |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

#### Simulated Outcome

Produced by the simulation engine ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)), once per positioning candidate, in parallel across candidates.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| share | Projected Brand A volume share, expressed as a fraction of category units in the candidate’s market and target period, from the pinned share-response model |
| volume | Projected Brand A physical units for this candidate and target period, from the pinned volume model |
| category_growth | Percent change in total category units from the comparable prior-year category volume; carries the projected brand volume, volume-share fraction, implied category units and reference vintage, market, period and physical unit, or an unavailable reason. |
| metric_evidence | For each projected field, the candidate ID, value, availability, unit, period and referenced source inputs or versioned model call. For a derived figure preserve the input values and the derivation; for a model output preserve the pinned model version, inputs and output |
| revenue | Calculated directly as price times volume, not a model call, in the resolved currency of the query's geography |
| margin | Projected margin impact, from the margin model |
| rationale | A Rationale Record scoped to Simulate, computed by [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](/specs/application/technical/query-service/layered-output-synthesis.md#confidence-and-rationale-package-extended) |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

#### Product and Geography Match

Produced by reconciliation ([`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation`](/specs/application/technical/materialization-service/reconciliation.md#product-and-geography-reconciliation)). The two are related but distinct structures.

**Table Name:** Product Match \
**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| competitor_product_id | The competitor's own product identifier, as reported in syndicated data |
| brand_a_product_id | Brand A's corresponding internal product identifier. Nullable when no counterpart exists, the whitespace case |
| match_confidence | How confident the match is. A low-confidence match is flagged for review rather than forced through |
| match_method | Structured attribute matching or semantic matching, whichever produced the match |

**Table Name:** Geography Crosswalk \
**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| source_region_code | The competitor data provider's own regional code |
| geography_id | Foreign key to the Geography reference table entry the source region normalizes to. This normalization sets the materialized grid's geography ceiling |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) renders this.

#### Effective Price Forecast

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id / publication_id | Immutable forecast identifier and the manifest that supplied its membership, vintage and model pins |
| competitor_id / business_unit_id | Foreign keys to the Competitor and Business Unit reference tables. Both belong to the exact lookup key |
| brand_code | The resolved brand from Question Intent or the scheduled cell. Include this code in the stored key, lookup, and repeatability trace so two grid cells differing only by brand remain distinct |
| geography_id | Foreign key to the grounded geography whose prices this forecast models. An estimate allocated to a finer geography references the forecast for the grounded parent |
| horizon | Supported horizon actually computed at the pinned vintage. A scheduled cell takes its horizon from the publication manifest. An eligible live miss uses the resolved horizon of the question |
| computed_via | Origin of computation, batch or live. Retained deliveries identify which questions used the forecast |
| origin_date / target_date / window_start / window_end | Dates resolved by [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization § Forecast period`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-period). Both batch and live forecasts preserve the exact interval |
| measurement_basis | Effective-price series, metric, resolved currency, physical unit, period aggregation and pinned observation calendar used for that interval |
| data_vintage_id | Foreign key to the Data Vintage dimension ([`§ Core Data Model § Reference and Master Data § Data Vintage`](#data-vintage)), the data snapshot this forecast was computed against |
| application_version | Same meaning as in Answer Provenance ([`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`](#answer-provenance)). Captured once when this row is produced, at materialization time for a batch row or at query time for a live row. It is never updated afterward, the same non-mutation discipline applied to the forecast itself |
| forecast_model_versions | The complete map of Predict model names to versions pinned for the grid publication, including conditional models. The publication and each live or scheduled forecast store the same map. It is the model component of the exact lookup and uniqueness key |
| model_versions | Same meaning as in Answer Provenance ([`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`](#answer-provenance)), captured when this row is produced. This is the execution trace. Scoped to only the forecasting and driver attribution models this row's Predict computation invoked, never the positioning or simulation models a live answer might also invoke on top of it |
| business_unit_configuration_version | Same meaning as in Answer Provenance ([`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`](#answer-provenance)), captured when this row is produced. A stale cell, batch or live, can then report the configuration version it was produced under, instead of silently reflecting whatever configuration is current when it is later read |
| forecast | Direction of the effective price move, and the move itself, signed. The size of the move is its magnitude. Magnitude is denominated in geography_id's resolved currency ([`§ Core Data Model § Reference and Master Data § Geography`](#geography)), already normalized in [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`](/specs/application/technical/materialization-service/reconciliation.md#currency-normalization), whatever currency the underlying data feed originally reported |
| confidence_interval_lower / confidence_interval_upper | Lower and upper bounds on the forecast move, expressed in the geography’s resolved currency. Driver Attribution places the forecasting models’ combined offsets around the move ([`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution [Step: 11]`](/specs/application/technical/predict-computation.md#driver-attribution)). The attached Rationale Record explains the forecast’s confidence score ([`§ Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](#rationale-record)). |
| starting_effective_price | The competitor's current effective price this forecast's move starts from, as [`specs/application/technical/predict-computation.md § Predict Computation § Baseline forecast [Step: 5]`](/specs/application/technical/predict-computation.md#baseline-forecast) takes it, in geography_id's resolved currency. It is kept so the realized move can be measured from the same start |
| dead_zone_threshold | The business unit's dead-zone threshold in effect when this row was produced, the one [`specs/application/technical/predict-computation.md § Predict Computation § Baseline forecast [Step: 6]`](/specs/application/technical/predict-computation.md#baseline-forecast) applied. It is kept so this forecast is always judged by that threshold |
| rationale | A Rationale Record for this forecast, retrieved as a lookup rather than recomputed for any query landing inside the grid |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Delivered Answer

The query service commits one Delivered Answer for a question whose response includes a completed forecast. The forecast may come from a published cell, a reused live bundle or a new live computation. A partial response retains only the stages completed for this question. The qualifying question_asked outcomes are [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: answer_produced]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: position_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), or [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: simulate_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run). It is never created for [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: query_denied]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: clarification_needed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), or [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: predict_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), where there is nothing yet to have lineage over.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| effective_price_forecast_id | Foreign key to the Effective Price Forecast ([`§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](#effective-price-forecast)) this answer was built on. Always populated, since a Delivered Answer exists only once Predict has completed |
| positioning_candidates | The set of Positioning Candidates ([`§ Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`](#positioning-candidate)) generated, each already carrying its own Rationale Record per the Positioning Candidate definition. A candidate's `simulated_outcome` field is null when the outcome was [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: simulate_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run). This whole field is empty when the outcome was [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: position_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run) |
| decision_type | The kind of decision this answer was given for, the session's or the question's. It is shown with the answer, and it is the one the answer's candidates were seeded by |
| client_received_at | First accepted authenticated receipt for this delivery. Null until confirmed. The committed delivery alone establishes no receipt |
| requested_geography_id / allocation_basis | Requested geography, grounded parent, and the basis for each local quantity or ratio. Preserve numerator, denominator, sources and units for estimated rates, and identify values shown solely as parent references. Mark an unknown legacy scope unavailable |
| submitted_question | The text the Query user submitted for this delivery. The retained question_asked audit entry supplies the actor and authorizes access to this text through its Delivered Answer. Purge the text with that answer. For an older delivery without this field, show that the original wording is unavailable |
| rendered_narrative | The complete natural-language text delivered, across whichever stages were reached. [`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior) covers a partial answer's labeling text as part of this. Captured directly because the repeatability guarantee ([`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)) explicitly allows this wording to vary between runs, unlike everything else on this row |
| displayed_options | The ordered groups actually delivered. Each group holds its ordered candidate IDs and the strategy labels shown at delivery. Each member refers to the immutable delivered candidate and its outcome where available. Predict-only deliveries store an empty list. Deliveries with Position and unavailable Simulate store individually labeled candidates in their delivered order |
| narrative_evidence | Each delivered numeric claim identifies its source record and field and retains the wording shown. A forecast claim references the forecast or its rationale. A candidate claim references its delivery-scoped candidate ID. A group claim references the displayed group and contributing member IDs. Forecast-only claims require no candidate. Stored figures stay in the candidate, outcome and rationale records |
| application_version | This delivery's own Answer Provenance ([`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`](#answer-provenance)), captured directly when this row is produced |
| model_versions | Same Answer Provenance capture: every model this delivery invoked, Predict's, Position's, and Simulate's alike, not only Predict's |
| language_model_versions | Same Answer Provenance capture: every language model this delivery called |
| business_unit_configuration_version | Same Answer Provenance capture |
| data_vintage_id | Same Answer Provenance capture: the Data Vintage ([`§ Core Data Model § Reference and Master Data § Data Vintage`](#data-vintage)) this delivery's computation ran against |
| produced_at | When this row was created |

Each of a Delivered Answer's Answer Provenance fields can differ from the referenced Effective Price Forecast's pinned value of the same name. A query served from the grid can reuse an Effective Price Forecast row computed days or weeks earlier. Position and Simulate still run fresh, against whatever versions and data vintage are current at this later moment, so the forecast's provenance and this delivery's provenance are different facts, not one fact restated. This row is what makes [`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`](/specs/application/technical/guarantees-mechanics.md#how-the-guarantees-are-achieved-mechanically)'s claim, that a live answer is "reproducible against an Answer Provenance... logged alongside it", true for Position and Simulate. Nothing on this row duplicates protected content that already has a canonical home. The forecast's substance stays behind effective_price_forecast_id and is never restated here.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

#### Realized Outcome

An immutable scored comparison produced by [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome check`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-check). Pending and unevaluable comparisons expose their disposition and reason separately from a scored outcome.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| effective_price_forecast_id | Unique foreign key to the forecast. Concurrent insertions return the stored winner |
| window_start / window_end / source_references | Compared interval and the observations used from the selected actuals vintage |
| actual_effective_price / realized_move | Observed price on the forecast’s measurement basis and its difference from the original starting price |
| forecast_error | The forecast's move less the realized move, both measured from the forecast's starting_effective_price, in the same resolved currency as the forecast it evaluates. It is not an absolute value, so an over-forecast and an under-forecast can be told apart |
| verdict | Right, Right direction, or Wrong, set by [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome check`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-check) |
| realized_data_vintage_id | Foreign key to the Data Vintage the actual figure came from, distinct from the vintage the original forecast used |
| computed_at | When this comparison was computed |

#### Answer Provenance

Attached to every answer, per the repeatability guarantee in [`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`](/specs/application/technical/guarantees-mechanics.md#how-the-guarantees-are-achieved-mechanically). For a live-path answer, it is assembled fresh from whatever application, model, and configuration state is current. For a query served from the materialized grid, the forecast's values are the ones [`§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](#effective-price-forecast) captured when that row was produced. The Delivered Answer built on that row captures its own at delivery, since Position applies the configuration current when the question is asked.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| application_version | The orchestration and logic version that produced this answer |
| model_versions | The version of every model invoked whose output is part of the numeric-determinism contract, one entry per model called. The narrative rendering model's version is recorded in language_model_versions instead, since that model's prose is not required to be identical across calls |
| language_model_versions | The provider and dated version of each language model that served this answer, one entry per kind of call it made, reasoning over the question and narrative rendering among them. Each is Acme AI's own hosted model or a frontier provider's ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). Kept apart from model_versions because these calls' output is not part of the numeric-determinism contract, so the record shows which model served an answer without making its prose a repeatability promise |
| business_unit_configuration_version | The version of this business unit's settings that shape an answer, keyed by business unit code for legibility in an audit trail, and raised as [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance) describes. The installation-wide governed vocabulary and archetype rules change only with application_version ([`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path)) |
| data_vintage_id | Foreign key to the Data Vintage dimension ([`§ Core Data Model § Reference and Master Data § Data Vintage`](#data-vintage)), the data snapshot everything was computed against |

#### Review Queue Item

The status of a single flagged item: a low-confidence product match ([`§ Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`](#product-and-geography-match)) or an ambiguous or incomplete document extraction ([`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`](/specs/application/technical/materialization-service/driver-signal-extraction.md#vector-and-semantic-mapping-with-structured-extraction)). These are the cases [`specs/application/product/tenant-administration/review-queues.md`](/specs/application/product/tenant-administration/review-queues.md) commits to the client reviewing. Each is a durable record, and resolving one produces a corrected record that every future query benefits from. A low-confidence answer is not another such case. It is the output of one query at one moment, not a record with anything to correct. The confidence guarantee itself ([`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`](/specs/application/technical/guarantees-mechanics.md#how-the-guarantees-are-achieved-mechanically)) handles it, and it is surfaced to the user directly, not queued for review.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
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

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) renders this.

### Audit Log

#### Audit Log Entry

Produced by every action that the populations this entry covers take:
- Acme AI's Platform admin access against an installation, whether through a federated claim or break-glass credentials;
- a Query user's question, the system's core activity, not an afterthought sharing a mechanism built for someone else;
- a Control plane admin's or an Identity admin's change to what they govern;
- an elected installation release applied by either a named Platform admin or the client infrastructure team;
- an installation's record of its effective external model destinations ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)).

All are governed the same way, per [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance). Break-glass retrieval also has its own vault-native audit trail ([`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management)). This entry covers the broader case: every other Platform admin action, alongside every Query user question and every Control plane admin's and Identity admin's change. Those Platform admin actions include accessing the application logs and traces that [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance) describes separately.

**Reference Key:** Field \
**Required:** Description

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| actor | The identity selected by [`§ Core Data Model § Audit Log § Audit Log Entry § Audit attribution`](#audit-attribution). |
| actor_role | The responsible role paired with actor by [`§ Core Data Model § Audit Log § Audit Log Entry § Audit attribution`](#audit-attribution). |
| purge_cutoff | The UTC cutoff applied by this retention_purge run ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance § Audit log purge`](/specs/application/technical/engineering-and-production-considerations.md#audit-log-purge)). Reports read the greatest applied cutoff and retained activity at one consistent snapshot |
| action_type | A closed, governed set, not an extensible category: onboarding, upgrade, diagnostic support session, diagnostic log access, pinned_versions_viewed, question_asked, configuration_changed, retention_purge, frontier_models_changed, nothing else. pinned_versions_viewed is a Platform admin's read of the installation's pinned versions ([`specs/application/technical/control-plane-service/control-plane.md § Control Plane`](/specs/application/technical/control-plane-service/control-plane.md#control-plane)). frontier_models_changed is an installation's record of a change to effective call kinds, providers or dated versions, or its first provider-qualified baseline after migration ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). An installation that never names one never records it. Every capability any of these roles has is already enumerated elsewhere in this system. [`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path) covers every self-service and governed configuration surface, and [`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles) covers what each role can do, so no action outside this set would ever need auditing. Adding one is a real change to this schema, decided deliberately, never a runtime category left open for a future action to fall into on its own |
| business_unit_id | Foreign key to Business Unit where the action was scoped to one. Null wherever none was: an upgrade by either operator, another installation-wide Platform admin action, a governed configuration_changed edit such as the retention period itself, a retention_purge or frontier_models_changed entry, or a question_asked entry that ended before any business unit was resolved. A configuration_changed entry against a business-unit-scoped setting carries that business unit. One against an IdP claim mapping carries the business unit its mapping row names, before or after the change. Such a change has one entry for each business unit it touches. Where the row names no business unit, as for a Platform admin or Identity admin mapping, it has a single entry with business_unit_id null |
| occurred_at | When the action took place |
| outcome | Whether the action succeeded: success or failure, for every action_type except question_asked. For a question_asked entry, it is the Question run State Machine's terminal state: [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: answer_produced]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: query_denied]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: clarification_needed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: predict_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: position_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), or [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: simulate_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run) |
| delivered_answer_id | For a question_asked entry whose outcome was [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: answer_produced]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: position_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), or [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: simulate_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), a foreign key to the Delivered Answer ([`§ Core Data Model § Pipeline and Answer Artifacts § Delivered Answer`](#delivered-answer)) that answer produced. The Delivered Answer is the complete record of what was shown and what produced it. Null for [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: query_denied]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: clarification_needed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), and [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run [States.State: predict_failed]`](/specs/application/technical/engineering-and-production-considerations.md#question-run), where no forecast was ever produced, and null for every action_type other than question_asked |
| changed_field | For a configuration_changed entry only, the configuration surface edited, self-service or governed alike. [`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path) names the bounded set, including the installation-wide audit log retention period itself. Null otherwise |
| previous_value / new_value | For a configuration_changed or frontier_models_changed entry only, the setting's value before and after the change, as a plain comparable string whatever the underlying field's type. For a frontier_models_changed entry, the value is the sorted tuples of call kind, provider and dated version. An empty set records withdrawal of all routes. On migration the prior value preserves known kinds and versions with unknown providers, or marks the entire prior state unknown where its history is unavailable. Both are null for a change to a data source's credentials: the fact of the rotation is logged, never the credential material, as required by [`specs/application/product/tenant-administration/data-source-connections.md § Data Source Connections`](/specs/application/product/tenant-administration/data-source-connections.md#data-source-connections) and [`specs/application/technical/secrets-management.md § Secrets management`](/specs/application/technical/secrets-management.md#secrets-management). Null for every other action_type. For an IdP claim mapping entry, only that entry's business unit's side of the change: the mapping as it stood there before and after, never the business unit on the other side of a move |
| upgrade_attempt_id | For an upgrade, the installation’s unique identifier of the elected deployment attempt. At most one terminal upgrade entry per attempt. Absent on legacy entries and other actions. |
| upgrade_versions | For a successful upgrade, the observed application version and the complete effective model pins keyed by model or call kind, with provider-qualified external versions. Captured once at activation for [`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md § Versioned Upgrades`](/specs/application/product/platform-and-compliance-operations/versioned-upgrades.md#versioned-upgrades). Absent for failures, other actions and historical entries where the versions were never captured. |
| routing_revision | Installation configuration revision acknowledged by this frontier_models_changed entry. Unique within the installation. Absent on legacy entries and other actions. |

##### Audit attribution

The installation attributes an upgrade to the authenticated deployment operator and its own automated actions to a fixed system identity. For other actions it records the identity asserted on the access path and the role used, including the local break-glass identity for emergency support. A signed-in person can submit a question before any role is mapped. If that question is refused for lack of a mapped role, the record retains the authenticated identity and leaves actor_role null.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Action type, Upgrade operator, Question refused for lack of a mapped role?

| Action type | Upgrade operator | Question refused for lack of a mapped role? | actor | actor_role |
|---|---|---|---|---|
| upgrade | Acme AI | - | Authenticated named Platform admin | platform_admin |
| upgrade | Client infrastructure | - | Authenticated client deployment principal | client_infrastructure |
| retention_purge | - | - | Fixed system identity | platform_admin |
| frontier_models_changed | - | - | Fixed system identity | client_infrastructure |
| question_asked | - | true | Authenticated identity | null |
| question_asked | - | false | Authenticated identity | Mapped role used for the request |
| "onboarding", "diagnostic support session", "diagnostic log access", "pinned_versions_viewed", "configuration_changed" | - | - | Identity asserted by the authorized access path | Role used for the action |

Configuration and routing entries carry the change in previous_value and new_value. A successful upgrade records its version snapshot at activation. Readers show uncaptured historical versions as unknown and never fill them from today’s pins. An audited question references its Delivered Answer. A retention_purge entry records the applied cutoff so a reader can establish which records were eligible.
