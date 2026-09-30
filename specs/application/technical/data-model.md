## Core Data Model

### Harmonized quantitative foundation

Syndicated retail data (pricing, volume, share), internal POS and trade history, elasticity models, tax and regulatory tables, and macroeconomic indicators land in a single harmonized environment, versioned and timestamped. Every metric has one canonical definition and one source of truth. This environment is a structured database, the counterpart to the vector database: exact keys, joins, and aggregation, not semantic search, which is what nearly everything in this file other than the Driver Signal actually needs. Exchange rates are ingested here too, one more macroeconomic indicator captured as part of each Data Vintage (`§ Core Data Model § Reference and Master Data § Data Vintage`) the same way every other input is; where and how a rate is used is `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`.

The structures in this file are referenced throughout the query service, the materialization service, and the control plane, gathered into one place. Each was defined in prose where it is first produced; this file is their one home, so later references cite a field here rather than restating it. Several nest inside others, a Positioning Candidate carries its own Rationale Record and Simulated Outcome, a Simulated Outcome carries its own Rationale Record in turn, and an Effective Price Forecast carries its own Rationale Record.

A field table states what an entity is made of, not a rule, a process, or a state it moves through. The rules that govern these structures, how an event type routes, how business unit gets resolved, how candidates consolidate, are modeled separately, in the constructs, elsewhere in these files, and cite this file's tables for the shape of the data they operate on.

Separate stores hold these, not one. The Driver Signal lives in the vector database (`§ Core Data Model § Vector Database Schema`). The vector database is partitioned into one namespace per business unit, keyed by the Business Unit's own stable code, so a query against it is scoped by which namespace the connection reaches, not by a filter applied after the fact to a shared index. Every other structure, Signal Routing Rule, Rationale Record, Positioning Candidate, Simulated Outcome, Product and Geography Match, Effective Price Forecast, Realized Outcome, Answer Provenance, Delivered Answer, and Review Queue Item, lives in the structured database this section describes, exact-key lookups and aggregation rather than similarity search. A Rationale Record cites Driver Signals by reference rather than duplicating them, the one place the two stores meet. The Question Intent is the exception to both, ephemeral for the life of a request, held in the question-intent cache already described in `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations` rather than persisted in either store.

Business Unit, Geography, and Competitor are reference tables, not per-instance records, and each carries separate identifiers doing different jobs: a sequential integer id, used for foreign keys and join performance within the structured database, the normal relational pattern, and a stable code, ISO 3166 for geography where it applies, a public ticker symbol for a competitor that has one, an assigned short code for business unit, used wherever these entities cross into the vector database or need to be legible to a person or an agent reading them directly. Structured-database tables reference these by integer id. The vector database, which has no join mechanism and no relationship to those integers, references them by code, the one identifier both stores can use without translation.

A code contains only uppercase letters, digits, and hyphens, no whitespace and nothing that would need URL encoding, so it is safe to use directly in a path segment, a query parameter, an API response, or a log line without transformation. Codes are validated and normalized to uppercase at entry. A code locks at its first use by ingested data, as `specs/application/technical/control-plane-service/control-plane.md § Control Plane` governs, meaning the first reference to the entity it names from a structured-database foreign key or a vector-store Driver Signal, because the vector database has no cheap way to cascade a code change across every chunk that already carries it, unlike the structured database, where only the reference table's own row would need to change.

The structured database's shape is a star schema: the Effective Price Forecast is the fact, Business Unit, Geography, and Competitor are dimensions, this section's surrogate-id-plus-code pattern is exactly what a dimension table is for. Geography stays a star rather than snowflaking into separate Country, State, and Metro tables, a self-referencing parent within the one table supports the country-to-state-to-metro rollup the drill-down needs without the extra joins a fully normalized hierarchy would add to every query, worth it for an analytical workload where minimizing joins matters more than the storage a snowflake schema would save. The Rationale Record does not flatten into the fact row, its variable-length fields belong in related tables hung off the fact by foreign key. Horizon, with only a few fixed values, is a plain fact attribute, not a dimension. The data snapshot a forecast was computed against is its own small dimension, a Data Vintage table capturing when each data snapshot was taken and which source data refresh it holds, since many facts share one vintage and repeating that metadata per row would be pure redundancy.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`, `specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`, `specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

### Vector Database Schema

The one entity actually stored in the vector database, embedding and structured fields together, because retrieval there needs semantic search.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` render this.

#### Driver Signal

Produced by extraction in `specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`, zero or more per ingested qualitative document, the durable record behind the qualitative guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`).

| Field | Description |
|---|---|
| source_type | One of the bounded types, regulatory filing, licensed third-party commentary, or internal analyst note, set by which ingestion path the document arrived through |
| credibility_tier | Derived directly from source_type, never judged per document, in the order `specs/application/product/answer-engine/predict.md § Predict — what will the competitor do` states |
| driver_category | One of the qualitative drivers Driver Attribution scores, tax, competitor plans, input costs, or discretionary spending; elasticity has no qualitative counterpart |
| entity | The competitor or business unit the signal concerns, by code, not free text and not an internal id, since this record lives in the vector database |
| geography | The location the signal concerns, by code |
| business_unit | The Business Unit code this signal is scoped to, so retrieval never crosses business units sharing one installation |
| event_type | A bounded value within the driver category, each with a declared `routes_to` value in `§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule` |
| direction | Increase, decrease, or neutral, as the source document states it |
| magnitude | A numeric value or bracket; a signal lacking what it needs to be sized is held back from forecasts by `specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction` |
| effective_date | When the event takes effect, distinct from the document's publish date |
| extraction_confidence | How confident the extraction step is that it parsed the document correctly, separate from credibility_tier |
| extraction_model_version | The version of the driver signal extraction model that produced this record |
| source_citation | A pointer to the underlying chunk in the vector database, the evidentiary backing behind the rationale trace |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

### Reference and Master Data

Reference tables and crosswalks, edited through the control plane's self-service surface, changing far less often and far less independently than the pipeline artifacts.

#### Business Unit

A reference table, not a per-instance record, one row per business unit the installation hosts.

| Field | Description |
|---|---|
| id | Sequential integer primary key, used for foreign keys from other structured-database tables |
| code | A short, stable code, set once during onboarding and never reused even if the business unit is later renamed, the natural key used in the vector database and anywhere legibility matters |
| name | Display name |

Which IdP claims map to this business unit, and with what role, lives in `§ Core Data Model § Reference and Master Data § IdP Claim Mapping`, not as a field here, since one business unit can have several claims mapping to it at different roles.

#### Geography

A reference table, one row per geography the harmonized foundation or the materialized grid references. Every price, price gap, and revenue figure computed at a geography is denominated in that geography's own resolved currency, any input reported in another converted once by `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization`; the system never blends a figure from one geography with a figure from another that uses a different currency at query, aggregation, or reporting time, so a business unit spanning more than one country, or one country with more than one currency of its own, always sees each geography's own figures in that geography's own currency downstream, never a converted or summed total.

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | ISO 3166-1 for country, ISO 3166-2 for state or province, an assigned code for the metro level, where no public standard applies |
| name | Display name |
| currency | ISO 4217 currency code; a geography's own resolved currency is its own value here if set, otherwise its nearest ancestor's. A country-level row, one with no parent_geography_id, always has a non-null currency, enforced when it is created (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`), so the walk up the hierarchy always terminates; the ordinary case, a whole country sharing one currency, is set once there and inherited by everything beneath it, and the rare country that genuinely uses more than one currency across its own regions overrides it at whichever level actually needs one. How a below-grid drill-down allocation's currency is set is `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`'s |
| parent_geography_id | Self-referencing foreign key, a metro's parent is its state, a state's parent is its country, the star schema's flattened hierarchy rather than separate tables per level |

#### Competitor

A reference table, one row per competitor in scope for any business unit.

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| code | A public ticker symbol where the competitor has one, an assigned code otherwise |
| name | Display name |

#### Entity Alias

A many-to-one crosswalk, several aliases can resolve to one Competitor or Business Unit, the same reconciliation pattern as Product and Geography Match, applied to names instead of catalog identifiers.

| Field | Description |
|---|---|
| alias_text | The name or code as it actually appears in a specific source, not yet resolved |
| entity_type | Competitor or Business Unit, which reference table this alias resolves against |
| entity_id | Foreign key to the matching row in that reference table |
| source_channel | The ingestion channel or source type that uses this alias, where known |

A rebrand, or a data vendor's own naming convention, is a new row here, not a change to the reference table's id or code. The reference table's name field is only the current display name, a convenience, resolution always runs against this table, which is where every current and historical name actually lives, so a competitor's forecast history stays attached to one identity across a name change instead of fragmenting into two. alias_text is exempt from the code format rule `§ Core Data Model § Harmonized quantitative foundation` states, its job is capturing a source's actual naming exactly as it appears, spaces, mixed case, punctuation and all, not serving as a second code.

#### Glossary Term

Declared as a governed table (`specs/application/technical/glossary-and-grounding.md § Guaranteed grounding`), the same discipline `§ Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule` already applies to a different bounded set, its own bounded name the natural key rather than a surrogate id, the same shape, not per-business-unit data, one entry per term the governed glossary defines.

| Field | Description |
|---|---|
| term | The bounded name, effective price, price gap, relative price index, category growth, and the rest of the governed vocabulary |
| resolves_to | The schema field or model endpoint this term maps to |

Adding a term here is a change to the governed vocabulary itself, an application release; a business unit's own alternate phrasing for a term already declared here is `§ Core Data Model § Reference and Master Data § Glossary Alias` instead, never a new row in this table.

#### Glossary Alias

A many-to-one crosswalk, several aliases can resolve to one Glossary Term, the same reconciliation pattern as Entity Alias, applied to business vocabulary instead of entity names.

| Field | Description |
|---|---|
| alias_text | The phrasing as it actually appears in a business unit's own usage, not yet resolved |
| term | The Glossary Term this alias resolves to, matched by its own bounded name |
| business_unit_id | Foreign key to Business Unit; unlike the governed term itself, an alias is scoped to the business unit that registered it |

#### Data Vintage

A dimension, one row per data snapshot the pipeline has ever computed against, referenced by `§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`, `§ Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`, and `§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`.

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| computed_at | When this data snapshot was taken |
| source_data_snapshot | The identifier of the underlying competitor data refresh this vintage was computed against |

#### IdP Claim Mapping

A crosswalk, not a per-instance record, one row per claim value the customer's IdP asserts.

| Field | Description |
|---|---|
| claim_value | The claim or group value as asserted by the client's IdP |
| business_unit_id | Foreign key to Business Unit, null for identity admin and platform admin claims (`specs/application/technical/identity-and-access.md § Business unit access, federated`, `specs/application/technical/identity-and-access.md § Platform admin access`) |
| role | query_user, control_plane_admin, identity_admin, or platform_admin |

An Identity admin claim, the role that can edit this table itself, is scoped as `specs/application/technical/identity-and-access.md § Business unit access, federated` states, and self-service management of it belongs to the client's identity team, not any single business unit's data steward.

A query user claim that sees every business unit is not a separate case, it is the same multi-business-unit claim `specs/application/technical/identity-and-access.md § Business unit access, federated` already describes, with one mapping row per currently existing business unit rather than a wildcard. A new business unit does not extend an existing claim's reach on its own, whoever manages a claim, identity admin for an org-wide one, adds its new mapping row the same way any multi-business-unit claim gains a newly added business unit.

### Pipeline and Answer Artifacts

Structures produced by the query and materialization services as they compute and package an answer, each defined in prose where it is first produced and gathered here for its canonical field list.

#### Signal Routing Rule

Declared as a governed table (`specs/application/technical/predict-computation.md § Predict Computation § Signal routing`), not per-instance data, one entry per bounded event type.

| Field | Description |
|---|---|
| event_type | The bounded name, announced price change, rate change, product launch, and so on |
| driver_category | Which of the qualitative drivers this event type belongs to |
| routes_to | Baseline (effective price forecasting) or driver attribution, the single downstream consumer for any signal carrying this event type |

#### Rationale Record

Produced by confidence and rationale packaging (`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging`) for the Predict output. Composition varies from there, as `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended` sets out: a Positioning Candidate's own record is that same one, and a Simulated Outcome's is its own, which never carries a driver_contribution_breakdown, driver_evidence, baseline, baseline_evidence or conflicts, all fields specific to the Predict computation with no equivalent for a model-based simulation output; its own confidence_components are model confidence and model freshness, not the source-credibility, data-freshness, and triangulation-agreement set the Predict output and Positioning Candidate share.

| Field | Description |
|---|---|
| retrieval_trace | What was pulled, from where, and as of when, for every input this answer depended on |
| driver_contribution_breakdown | The full per-driver breakdown from Driver Attribution, every driver, not only the largest, the same values rendered as the decomposition graph, each contribution in the forecast's own geography's resolved currency |
| driver_evidence | Per-driver evidence backing, one entry per driver in driver_contribution_breakdown: a reference to the Driver Signal(s) behind a signal-backed driver's magnitude; for elasticity, always model-only, the model name and its registry last-validated date (`specs/application/technical/model-registry.md § Model registry`) instead; for competitor plans, both the Driver Signal reference and that same model detail together, since the model only translates a signal it was given; or an explicit no-signal marker for a driver Driver Attribution scored at zero |
| confidence_score | The overall confidence attached to this answer or candidate |
| confidence_components | The inputs the score is derived from, which set depends on which structure carries this record: source credibility, data freshness, and triangulation agreement for the Predict output and a Positioning Candidate; model confidence and model freshness for a Simulated Outcome. Each component names what set it: for source credibility, the Driver Signals at the lowest credibility_tier; for data freshness, the data-as-of snapshot and each contributing Driver Signal's effective_date; for triangulation agreement, the entries in conflicts; for model confidence and model freshness, the model that set each. A Simulated Outcome's also records whether the cap at the parent Positioning Candidate's score lowered it |
| baseline | The baseline move and its direction, from `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`'s steps 5 to 7, in the forecast's own geography's resolved currency; with driver_contribution_breakdown it sums to the forecast's move |
| baseline_evidence | What the baseline was built from, which a Query user sees on opening it (`specs/application/product/answer-engine/predict.md § Predict — what will the competitor do`): the price-history snapshot, the forecasting models that carried it forward with each one's last-validated date, and every Driver Signal routed to the baseline that adjusted it |
| conflicts | Each conflict `specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution` flagged: the baseline's direction, the Driver Signal that disagrees with it, and that signal's own contribution; empty when none was flagged |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

#### Question Intent

Produced by intent parsing and decoupling (`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`).

| Field | Description |
|---|---|
| metric | The quantity the question is actually about, price by default |
| business_unit | Resolved by `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling`'s business unit Decision Tree |
| entities | The competitor and brand the question concerns, resolved against the glossary, by code once resolved |
| geography | The location scope of the question, by code once resolved |
| horizon | The time window the forecast is asked for |
| decision_type | Strategic or tactical, settled by `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling` from the question's own decision words or the kind of decision the request carries; it decides which archetypes the positioning engine seeds |
| granularity | The geographic or metric level implied by the question, validated against the glossary before anything executes |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Positioning Candidate

Produced by the positioning engine (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`), one per seeded archetype surviving `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Option Consolidation`.

| Field | Description |
|---|---|
| archetype | Hold, Match, Close the Gap, or Diverge |
| resulting_effective_price | Brand A's price under this archetype's rule, at the query's geography and horizon, in that geography's own resolved currency |
| price_gap | The absolute difference between resulting_effective_price and the competitor's forecasted price, both already in the same geography's resolved currency |
| relative_price_index | The same comparison as a ratio, times 100 |
| rationale | The same Rationale Record produced for the Predict output (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended`), attached here as its own copy so this candidate's confidence and driver breakdown are visible without navigating back to Predict |
| simulated_outcome | A Simulated Outcome specific to this candidate; null when simulation did not complete for this answer (a simulate_failed outcome), the forecast and this candidate still stand on their own in that case |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Simulated Outcome

Produced by the simulation engine (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`), once per positioning candidate, in parallel across candidates.

| Field | Description |
|---|---|
| share | Projected share impact of this candidate, from the share-response model |
| volume | Projected volume impact, from the volume model |
| category_growth | Aggregated from the share and volume outputs at the category level, not a separate model |
| revenue | Calculated directly as price times volume, not a model call, in the query's own geography's resolved currency |
| margin | Projected margin impact, from the margin model |
| rationale | A Rationale Record scoped to Simulate, computed by `specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Confidence and rationale packaging, extended` |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Product and Geography Match

Produced by reconciliation (`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation`), related but distinct structures.

**Product Match —**

| Field | Description |
|---|---|
| competitor_product_id | The competitor's own product identifier, as reported in syndicated data |
| brand_a_product_id | Brand A's corresponding internal product identifier, nullable when no counterpart exists, the whitespace case |
| match_confidence | How confident the match is, low-confidence matches are flagged for review rather than forced through |
| match_method | Structured attribute matching or semantic matching, whichever produced the match |

**Geography Crosswalk —**

| Field | Description |
|---|---|
| source_region_code | The competitor data provider's own regional code |
| geography_id | Foreign key to the Geography reference table entry it normalizes to, this is what sets the materialized grid's geography ceiling |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

#### Effective Price Forecast

Produced by forecast materialization (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`), or live by `specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging` for a query the grid does not yet cover, one row per computation regardless of which path produced it. A live-path computation is checked against this key before it runs, not after: competitor, business unit, geography, horizon, data_vintage_id, application_version, model_versions, and business_unit_configuration_version. If a row already matches every one of these, it is retrieved rather than recomputed, the repeatable-answer guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`) covering unchanged data, application version, model versions, and business unit configuration together, so data_vintage_id alone is never enough to call two computations identical, only a match on all of these together is; this makes a repeated off-grid query behave exactly like an in-grid one once it has been asked and answered once, a lookup, not a live computation. If nothing matches, the computation runs and its output is persisted as a new row.

| Field | Description |
|---|---|
| competitor_id / business_unit_id | Foreign keys to the Competitor and Business Unit reference tables, not codes, this record lives in the structured database and is queried by exact key |
| geography_id | Foreign key to the Geography reference table; for a batch row, one entry in the organic grid set by reconciliation, for a live row, whatever geography the question actually asked for |
| horizon | For a batch row, one of the standard set the grid materializes (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`); a live row carries whatever horizon the question actually asked for, inside or outside that set |
| computed_via | Which path produced this row, batch (a materialization run) or live (a live-path query, `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked)`), so a bulk reviewer can tell a real, question-triggered answer from routine eager pre-computation |
| data_vintage_id | Foreign key to the Data Vintage dimension (`§ Core Data Model § Reference and Master Data § Data Vintage`), the data snapshot this forecast was computed against |
| application_version | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured once when this row is produced, at materialization time for a batch row or at query time for a live row, and never updated afterward, the same non-mutation discipline already applied to the forecast itself |
| model_versions | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), scoped to only the forecasting and driver attribution models this row's own Predict computation actually invoked, never the positioning or simulation models a live answer might also invoke on top of it, captured when this row is produced |
| business_unit_configuration_version | Same meaning as in Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured when this row is produced so a stale cell, batch or live, can honestly report the configuration version it was produced under rather than silently reflecting whatever configuration is current when it's later read |
| forecast | Direction of the effective price move and the move itself, signed, whose size is its magnitude, magnitude denominated in geography_id's own resolved currency (`§ Core Data Model § Reference and Master Data § Geography`), already normalized in `specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation § Currency normalization` regardless of what currency the underlying data feed originally reported |
| confidence_interval_lower / confidence_interval_upper | This forecast's own confidence interval around the forecast's move, placed by `specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`'s step 8 from the forecasting models' combined offsets, in the same resolved currency as magnitude. Lives alongside the forecast's own value and model_versions, since it is a property of what the named forecasting models themselves produce, not of the qualitative evidence trail behind the forecast; confidence_score and confidence_components on the attached Rationale Record instead summarize how much to trust the number overall, weighing source credibility, data freshness and triangulation agreement, so the two can genuinely diverge, precise models can still sit behind a lower-confidence answer if a driver rests on a weakly sourced or stale fact |
| starting_effective_price | The competitor's current effective price this forecast's move starts from, as `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`'s step 5 takes it, in geography_id's own resolved currency; kept so the move actually realized can be measured from the same start |
| dead_zone_threshold | The business unit's dead-zone threshold in effect when this row was produced, the one `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`'s steps 6 and 7 applied; kept so this forecast is always judged by it |
| rationale | A Rationale Record for this forecast, retrieved as a lookup rather than recomputed for any query landing inside the grid |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

#### Delivered Answer

Produced by the query service as the final step of assembling any answer that reaches at least Predict, whether Predict itself was a grid lookup or a live computation, and whether or not Position and Simulate also complete (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`), one row per question actually answered, in full or in degraded form; every question_asked reaching Predict gets one, not only the off-grid case. Exists only when a forecast was actually produced: created for a question_asked outcome of answer_produced, position_failed, or simulate_failed (`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`), never for query_denied, clarification_needed, or predict_failed, where there is nothing yet to have lineage over.

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| effective_price_forecast_id | Foreign key to the Effective Price Forecast (`§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`) this answer was built on; always populated, since a Delivered Answer only exists once Predict has completed |
| positioning_candidates | The set of Positioning Candidates (`§ Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`) actually generated, each already carrying its own Rationale Record per their existing definition; a candidate's own `simulated_outcome` field is null when the outcome was simulate_failed; this whole field is empty when the outcome was position_failed |
| decision_type | The kind of decision this answer was given for, the session's or the question's own, shown with the answer and the one its candidates were seeded by |
| rendered_narrative | The complete natural-language text actually delivered, across whichever stages were reached (`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior` covers a partial answer's own labeling text as part of this); captured directly because the repeatability guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`) explicitly allows this wording to vary between runs, unlike everything else on this row |
| application_version | This specific delivery's own Answer Provenance (`§ Core Data Model § Pipeline and Answer Artifacts § Answer Provenance`), captured directly at the moment this row is produced |
| model_versions | Same Answer Provenance capture, every model this specific delivery actually invoked, Predict's, Position's, and Simulate's alike, not only Predict's |
| business_unit_configuration_version | Same Answer Provenance capture |
| data_vintage_id | Same Answer Provenance capture, the Data Vintage (`§ Core Data Model § Reference and Master Data § Data Vintage`) this delivery's own computation actually ran against |
| produced_at | When this row was created |

A Delivered Answer's Answer Provenance fields can each differ from the referenced Effective Price Forecast's own pinned values of the same name: a query served from the grid can reuse an EPF row computed days or weeks earlier, while Position and Simulate still run fresh against whatever versions and data vintage are current at this later moment, so the forecast's own provenance and this delivery's own provenance are different facts, not one restated twice. This is where `specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`'s own claim that a live answer is "reproducible against an Answer Provenance... logged alongside it" is actually true for Position and Simulate. Nothing on this row duplicates protected content that already has a canonical home: the forecast's own substance stays behind effective_price_forecast_id, never restated here.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

#### Realized Outcome

Produced by realized outcome tracking (`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking`), at most one per Effective Price Forecast, once its horizon has actually passed and real data exists to check it against. The forecast it evaluates is never edited to match, an Effective Price Forecast stays exactly what was forecast at the time, this is a separate, later-arriving record of what actually happened.

| Field | Description |
|---|---|
| effective_price_forecast_id | Foreign key to the Effective Price Forecast this outcome evaluates |
| actual_effective_price | The competitor's effective price actually observed for that combination once the horizon passed, decomposed the same way the original forecast was, in the same resolved currency as the forecast it's compared against |
| forecast_error | The forecast's move less the move actually realized, both measured from the forecast's starting_effective_price, in the same resolved currency as the forecast it evaluates, not an absolute value, so an over-forecast and an under-forecast can be told apart |
| verdict | Right, Right direction, or Wrong, set by `specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking` |
| realized_data_vintage_id | Foreign key to the Data Vintage the actual figure came from, distinct from the vintage the original forecast used |
| computed_at | When this comparison was computed |

#### Answer Provenance

Attached to every answer, per the repeatability guarantee in `specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`. Assembled fresh, from whatever application, model, and configuration state is current, for a live-path answer. For a query served from the materialized grid, the forecast's own values are the ones `§ Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast` captured when that row was produced; the Delivered Answer built on it captures its own, at delivery, since Position applies the configuration current when the question is asked.

| Field | Description |
|---|---|
| application_version | The orchestration and logic version that produced this answer |
| model_versions | The specific version of every model actually invoked whose output is part of the numeric-determinism contract, one entry per model called; the narrative rendering model's version is tracked separately in the model registry (`specs/application/technical/model-registry.md § Model registry`) for operational purposes but is not part of this record, since its prose is not required to be identical across calls |
| business_unit_configuration_version | The version, keyed by business unit code for legibility in an audit trail, of this business unit's own settings that shape an answer, raised as `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance` describes; the installation-wide governed vocabulary and archetype rules change only with application_version (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`) |
| data_vintage_id | Foreign key to the Data Vintage dimension (`§ Core Data Model § Reference and Master Data § Data Vintage`), the data snapshot everything was computed against |

#### Review Queue Item, a Lifecycle

The status of a single flagged item, a low-confidence product match (`§ Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`) or an ambiguous or incomplete document extraction (`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`), the cases `specs/application/product/tenant-administration/review-queues.md` commits to the client reviewing. Each is a durable record: resolving one produces a corrected record that every future query benefits from. A low-confidence answer is not another such case here, it is the output of one query at one moment, not a record with anything to correct, and it is handled by the confidence guarantee itself (`specs/application/technical/guarantees-mechanics.md § How the Guarantees Are Achieved Mechanically`), surfaced to the user directly, not queued for review.

| state | description | terminal |
|---|---|---|
| flagged | Flagged at the point of computation, by a confidence threshold or an incomplete extraction; not yet seen by a reviewer | No |
| under_review | A control plane admin has opened the item | No |
| resolved | A reviewer has confirmed or corrected the underlying record | Yes |
| dismissed | A reviewer has confirmed no change is needed or possible; an incomplete extraction stays unused | Yes |

| From | To | Trigger or condition |
|---|---|---|
| flagged | under_review | A control plane admin opens the item |
| under_review | resolved | The reviewer confirms or corrects the match or extraction |
| under_review | dismissed | The reviewer confirms no change is needed or possible |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

### Audit Log

#### Audit Log Entry

Produced by every action the populations this entry covers take: Acme AI's Platform admin access against an installation, whether through a federated claim or break-glass credentials; a Query user's own question, the system's own core activity, not an afterthought sharing a mechanism built for someone else; and a Control plane admin's or an Identity admin's change to what they govern. All are governed the same way, per `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`. Break-glass retrieval specifically also has its own vault-native audit trail (`specs/application/technical/secrets-management.md § Secrets management`); this entry covers the broader case, every other Platform admin action, including accessing the application logs and traces `specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance` separately describes, alongside every Query user question and every Control plane admin's and Identity admin's change.

| Field | Description |
|---|---|
| id | Sequential integer primary key |
| actor | The identity that performed the action, a Platform admin's, by whatever access path, federated claim or break-glass, actually asserts it, a Query user's, Control plane admin's or Identity admin's own IdP-asserted claim, or, for a retention_purge entry only, a fixed system identity, since no human initiates that run |
| actor_role | query_user, control_plane_admin, identity_admin or platform_admin, the role whose claim authorized this action, so entries from every population, sharing one table, are never confused with each other; a retention_purge entry is platform_admin, the same automated-mechanism-belongs-to-Acme-AI reasoning already applied to every other installation-wide governed action |
| action_type | A closed, governed set, not an extensible category: onboarding, upgrade, diagnostic support session, diagnostic log access, pinned_versions_viewed, question_asked, configuration_changed, retention_purge, nothing else. pinned_versions_viewed is a Platform admin's read of the installation's pinned versions (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`). Every actual capability any of these roles has is already enumerated elsewhere in this system, `specs/application/technical/control-plane-service/control-plane.md § Control Plane`'s own Constraint table for every self-service and governed configuration surface, `specs/application/product/roles.md § Roles` for what each role can do, so there is no scenario in which an action outside this set would ever need auditing; adding one is a real change to this schema, decided deliberately, never a runtime category left open for a future action to fall into on its own |
| business_unit_id | Foreign key to Business Unit, where the action was scoped to one, and null wherever none was: an installation-wide Platform admin action such as an upgrade, a governed configuration_changed edit such as the retention period itself, a retention_purge entry, or a question_asked entry that ended before any business unit was resolved. A configuration_changed entry against a business-unit-scoped setting carries that business unit, and one against an IdP claim mapping carries the business unit its mapping row names, before or after the change, with one entry for each business unit a change touches, and a single entry with business_unit_id null where the row names no business unit, as for a Platform admin or Identity admin mapping |
| occurred_at | When the action took place |
| outcome | Whether the action succeeded, success or failure for every action_type except question_asked; for a question_asked entry specifically, the Orchestration State Machine's own terminal state, answer_produced, query_denied, clarification_needed, predict_failed, position_failed, or simulate_failed (`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration`) |
| delivered_answer_id | For a question_asked entry whose outcome was answer_produced, position_failed, or simulate_failed, a foreign key to the Delivered Answer (`§ Core Data Model § Pipeline and Answer Artifacts § Delivered Answer`) that answer produced, the complete record of what was actually shown and what produced it; null for query_denied, clarification_needed, and predict_failed, where no forecast was ever produced, and null for every action_type other than question_asked |
| changed_field | For a configuration_changed entry only, which configuration surface was edited, self-service or governed alike (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`'s own Constraint table names the bounded set, including the installation-wide audit log retention period itself); null otherwise |
| previous_value / new_value | For a configuration_changed entry only, the setting's value before and after the change, as a plain comparable string regardless of the underlying field's own type; both null for a change to a data source's own credentials, the fact of the rotation is logged, never the credential material, the same standing rule `specs/application/technical/secrets-management.md § Secrets management` applies everywhere else; null for every other action_type; for an IdP claim mapping entry, only its own business unit's side of the change, the mapping as it stood there before and after, never the business unit on the other side of a move |

Only `previous_value` / `new_value`, for a configuration_changed entry, carries content directly, and it is legitimately audit content, a record of what a human changed, not a record of what produced an answer. Every other field on Audit Log Entry, including `delivered_answer_id`, only ever records that an access occurred or references the one row elsewhere that actually holds the substance. A retention_purge entry carries no count of what was removed, deliberately: what a defensible record needs to prove is that the process ran, on schedule, and that nothing eligible was skipped, not exactly how many rows happened to qualify that day, a number with no lasting significance of its own.
