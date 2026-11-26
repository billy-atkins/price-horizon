## Layered Output Synthesis (producing the answer)

This layer turns Predict's evidence into an answer a user can act on. It consumes the driver attribution output from [`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution). Predict's own layers (scorecard, narrative, map, decomposition) are direct renderings of that output and require no additional modeling. Position and Simulate do.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

### Price gap and relative price index, defined

Price gap is the absolute difference between Brand A's price and the competitor's forecast price, in currency terms, at whatever geography and horizon the query specifies. Both sides are always the same geography's own price, in that geography's own resolved currency ([`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`](/specs/application/technical/data-model.md#geography)). A cross-currency price gap never occurs, since the comparison is never made across geographies.

Relative price index is the same comparison expressed as a ratio: Brand A's price divided by the competitor's price, times 100. A value above 100 means Brand A sits at a premium, and a value below 100 means Brand A sits at a discount. Relative price index carries no currency at all, because a ratio of two same-currency figures cancels the unit. This is a property of the number, not a feature built on it. Nothing in this design compares one geography's relative price index against another's.

Both sides of the comparison are effective price, not list price. Comparing Brand A's list price against the competitor's forecast effective price would compare two different things, after all the work spent decomposing the competitor's side. Price gap and relative price index are both Position-stage outputs. The positioning engine computes both once per positioning candidate, so neither is an asserted number. Both belong in the governed glossary alongside effective price. The plain-language rendering of both, for a business reader, is in [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit).

For a resolved match, compute the currency gap as the absolute distance between the two effective prices. For example, 9 against 10 and 11 against 10 both yield a gap of 1. Their indices are 90 and 110. A flagged match withholds both comparisons until resolution ([`specs/application/technical/materialization-service/reconciliation.md § Open Questions [Name: Flagged Matches]`](/specs/application/technical/materialization-service/reconciliation.md#open-questions)).

### Positioning engine

The positioning engine takes the Predict output (the competitor's forecast move, its direction, confidence) together with the resolved origin effective prices, selected market and decision type. From them, the engine generates a bounded set of named Positioning Candidates ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`](/specs/application/technical/data-model.md#positioning-candidate)). The engine scores each candidate for price gap and relative price index at the granularity the query specifies. The candidate set is small and named, not the output of an optimizer picking a single "best" answer. The candidates are framed for the user's judgment, not decided for the user. The engine runs in stages, seeding then collapsing, so the count stays deterministic and testable rather than a judgment call made per query.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Archetypes

Use the competitor’s percentage change from origin to target. Match preserves Brand A’s starting index. Diverge moves one further increment of the same size, measured on Brand A’s starting price, in the direction of its existing premium or discount. At parity its price coincides with Match. A zero move yields the current price for every eligible strategy.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** strategy name \
**Computed:** candidate price

| strategy name | candidate price |
|---|---|
| "Hold" | if own price = null or own price < 0 then null else own price |
| "Match" | if own price = null or own price < 0 or match resolved? != true or competitor start = null or competitor start <= 0 or competitor target = null or competitor target < 0 then null else own price * competitor target / competitor start |
| "Close the Gap" | if own price = null or own price < 0 or match resolved? != true or competitor start = null or competitor start <= 0 or competitor target = null or competitor target < 0 then null else (own price + own price * competitor target / competitor start) / 2 |
| "Diverge" | if own price = null or own price < 0 or match resolved? != true or competitor start = null or competitor start <= 0 or competitor target = null or competitor target < 0 then null else max([0, own price * competitor target / competitor start + (if own price > competitor start then 1 else if own price < competitor start then -1 else 0) * own price * abs(competitor target - competitor start) / competitor start]) |

Prices are calculated before display rounding. The engine requires a resolved match and a positive competitor starting price before it evaluates a percentage-based strategy. Brand A’s current price and the target price must be present and nonnegative. For target zero Match and Close the Gap remain price calculations; cap Diverge at zero as well when the target is zero and its rule would go negative. A zero target allows a currency gap but leaves the relative index unavailable. A missing input, an invalid price or an unresolved match suppresses each dependent value and identifies the reason; an independently available Hold price remains visible. A match still in review follows [`specs/application/technical/materialization-service/reconciliation.md § Open Questions [Name: Flagged Matches]`](/specs/application/technical/materialization-service/reconciliation.md#open-questions). No unavailable comparison is used to merge two options. Candidate metrics use the resulting effective price and the selected competitor forecast for the same geography, currency and horizon.

#### Archetype seeds

The decision type the Question Intent carries ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`](/specs/application/technical/data-model.md#question-intent)) decides which archetypes are generated as candidates, before any simulation runs:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Decision type

**Annotations:** The Decision It Is

**Input Values:**
- Decision type: "Strategic", "Tactical"

| Decision type | Seeded candidates | The Decision It Is |
|---|---|---|
| Strategic | Hold, Match, Close the Gap, Diverge | a brand pricing decision on list price or price position |
| Tactical | Hold, Match, Close the Gap | a retailer or promotional decision |

Diverge is withheld from a tactical decision because it moves the brand's price position, which a retailer or promotional decision does not own.

### Option Consolidation

Apply the business unit’s pinned materiality settings after every eligible candidate has its outcome. Seed order resolves equal gaps. Place unavailable gaps last. In the field vector, express share as percentage points; the model’s volume-share fraction of 0.2 is 20 points. Convert compared quantities to the same unit. Use absolute point differences for share and relative price index and the configured relative tolerance times the larger absolute value for a relative field. A pair at the threshold qualifies. The provisional defaults are in [`§ Open Questions [Name: Default Materiality Thresholds]`](#open-questions).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - ordered candidates
  - comparison rules

**Output:**
  - visible groups

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)

| Step | Action |
|---|---|
| 1 | Set visible groups to [] |
| 2 | For each candidate of ordered candidates, by candidate.rank ascending: steps 3 to 5 |
| 3 | Set previous members to if count(visible groups) = 0 then [] else visible groups[-1] |
| 4 | Set pair comparable? to count(previous members) > 0 and (every member in previous members satisfies (every rule in comparison rules satisfies (member.values[rule.slot] != null and candidate.values[rule.slot] != null and abs(member.values[rule.slot] - candidate.values[rule.slot]) <= (if rule.relative then rule.limit * max([abs(member.values[rule.slot]), abs(candidate.values[rule.slot])]) else rule.limit)))) |
| 5 | Set visible groups to if pair comparable? and (count(visible groups) > 1 or candidate.rank < count(ordered candidates)) then append(remove(visible groups, count(visible groups)), append(previous members, candidate)) else append(visible groups, [candidate]) |
| 6 | End |

Each displayed group carries its ordered member IDs, their delivered strategy labels and their original prices and outcome metrics. A member ID is the stable canonical archetype code scoped to this delivery. Show a common value once when it is identical. Where group members differ, show their labeled values on inspection. A group never averages away a difference or acquires a synthetic candidate price. A tied pair retained at the two-choice floor explicitly shows its equal results. A missing comparison keeps its candidate separate. If simulation fails before outcomes can be delivered, show the positioned candidates individually, in seed order, and record that Simulate is unavailable. The grouping pass reads the settings described in [`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings).

#### A choice, never one option

A completed strategic or tactical presentation retains at least two options even when all candidates give the same outcome.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint` \
**Table Name:** Choice Floor

| Constraint | Applies To | Enforced By |
|---|---|---|
| count(visible groups) >= 2 | after [`§ Layered Output Synthesis (producing the answer) § Option Consolidation`](#option-consolidation) | [`§ Layered Output Synthesis (producing the answer) § Option Consolidation [Step: 5]`](#option-consolidation) |

### Simulation engine

For each eligible candidate, pin the forecast, category, market, period, business-unit settings, model versions and input snapshot. Run the registered share-response, volume and margin models for that candidate with its resulting price and the market and cost inputs declared by the pinned model versions. Save each call’s inputs, unit, version and result under that candidate’s identity. The share used here is volume share. Convert a percentage output to a fraction and convert physical volumes to a common per-unit basis before doing arithmetic. Margin is the registered margin model’s margin result with its declared unit. Report that unit alongside its value.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - candidate price
  - unit volume
  - unit share
  - reference category volume

**Output:**
  - projected category units
  - category volume growth
  - projected revenue

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)

| Step | Action |
|---|---|
| 1 | Set projected category units to if unit share = null or unit share <= 0 or unit share > 1 or unit volume = null or unit volume <= 0 then null else unit volume / unit share |
| 2 | Set category volume growth to if projected category units = null or reference category volume = null or reference category volume <= 0 then null else 100 * (projected category units - reference category volume) / reference category volume |
| 3 | Set projected revenue to if candidate price = null or unit volume = null or unit volume < 0 then null else candidate price * unit volume |
| 4 | End |

Use actual historical total category volume from the pinned snapshot for the comparable prior-year period. The projection and its reference must have the same category coverage, geography, unit and seasonal duration. If that comparison is unavailable, record the missing input on category growth. Zero projected brand units and a positive volume share are incompatible. Mark implied category units and growth unavailable with that reason. A valid zero volume still yields zero revenue at a known price. An unavailable dependency affects only the outputs that require it. A delivery whose simulation stage fails as a whole follows the Question run’s existing failure path. Calls for different candidates may run in parallel; their identities and evidence stay attached to the correct outcomes.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

Each model call identifies the question’s business unit, brand, category, geography, forecast version and target period; the candidate ID and per-unit price; the competitor forecast effective price; and the versioned demand, promotion and cost inputs required by that model’s registry entry. Share returns Brand A’s fraction of category units, volume returns Brand A units, and margin returns margin on the declared basis. Snapshot and call references travel with each result. A grouped answer exposes these same member records.

### Confidence and rationale package, extended

The Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)) described in [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package) for the Predict output attaches to every Position option. Each option carries that same record, copied individually rather than recomputed. Positioning applies a fixed archetype rule to the forecast, so it introduces no new source of uncertainty the Predict-stage packaging could have missed. The candidate inherits forecast confidence. Its availability separately reflects whether the matched prices support the calculation. If the underlying Predict confidence is low, every option downstream carries that same flag rather than presenting false certainty at a later stage.

Each Simulated Outcome carries the rationale computed for its question. The share-response, volume and margin models run for each candidate. Their versions, confidence intervals and validation dates are shared across the question, so the live simulation stage computes the rationale once and attaches it to every outcome. The model registry supplies the inputs ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). A Query user can open the rationale from any outcome ([`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - model registry entries
  - scoring date
  - retrieval trace
  - simulate confidence weighting rubric
  - parent confidence score

**Output:**
  - rationale on every Simulated Outcome

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)

| Step | Action |
|---|---|
| 1 | Set confidence input issues to for entry in model registry entries return {name: entry.name, version: entry.version, reason: if entry.confidence_interval_lower = null or entry.confidence_interval_upper = null or entry.confidence_interval_upper < entry.confidence_interval_lower then "invalid interval" else if entry.calibration version = null or entry.reference width = null or entry.reference width <= 0 then "missing or invalid calibration" else if entry.coverage = null or entry.coverage <= 0 or entry.coverage > 1 or entry.reference coverage != entry.coverage then "coverage mismatch" else if entry.interval unit = null or entry.reference unit != entry.interval unit or entry.interval period = null or entry.reference period != entry.interval period then "unit or period mismatch" else if entry.last_validated = null then "missing validation date" else if scoring date != null and entry.last_validated > scoring date then "validation postdates scoring date" else ""} |
| 2 | If count(model registry entries) = 0 or scoring date = null or parent confidence score = null or (some issue in confidence input issues satisfies issue.reason != ""), Go to step 15; otherwise, continue |
| 3 | Set model confidence scores to for entry in model registry entries return model confidence score((entry.confidence_interval_upper - entry.confidence_interval_lower) / entry.reference width) |
| 4 | Set model freshness scores to for entry in model registry entries return model freshness score(entry.last_validated, scoring date) |
| 5 | Set model confidence component to min(model confidence scores) |
| 6 | Set model freshness component to min(model freshness scores) |
| 7 | Set simulate confidence weights to {model confidence: simulate confidence weighting rubric.model confidence, model freshness: simulate confidence weighting rubric.model freshness} |
| 8 | Set Simulate confidence score to model confidence component * simulate confidence weights.model confidence + model freshness component * simulate confidence weights.model freshness |
| 9 | Set cap lowered? to Simulate confidence score > parent confidence score |
| 10 | Set Simulate confidence score to min(Simulate confidence score, parent confidence score) |
| 11 | Set limiting confidence models to model registry entries[model confidence score((item.confidence_interval_upper - item.confidence_interval_lower) / item.reference width) = model confidence component] |
| 12 | Set limiting freshness models to model registry entries[model freshness score(item.last_validated, scoring date) = model freshness component] |
| 13 | Set rationale on every Simulated Outcome to {scoring date: scoring date, unavailable reason: "", input issues: [], confidence_score: Simulate confidence score, confidence_components: {model confidence: model confidence component, model freshness: model freshness component, confidence evidence: limiting confidence models, freshness evidence: limiting freshness models, cap lowered: cap lowered?}, retrieval_trace: retrieval trace} |
| 14 | End |
| 15 | Set rationale on every Simulated Outcome to {scoring date: scoring date, unavailable reason: if count(model registry entries) = 0 then "no invoked model versions" else if scoring date = null then "missing scoring date" else if parent confidence score = null then "missing parent confidence" else "model evidence unavailable", input issues: confidence input issues[item.reason != ""], confidence_score: null, confidence_components: null, retrieval_trace: retrieval trace} |
| 16 | End |

This Rationale Record carries none of the Predict computation's own fields ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)). category_growth and revenue inherit this same confidence_score by construction, because both derive from the same models' outputs rather than from a model call of their own ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)). Predict's confidence does not read a model's last-validated date; that treatment remains provisional in [`specs/application/technical/model-registry.md § Open Questions [Name: Model Freshness in Predict]`](/specs/application/technical/model-registry.md#open-questions). Simulate reads it through this package, as the provisional answer's other side.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

Each invoked model version supplies a positive calibration reference width from a fixed validation population at the same coverage probability as its declared interval. Both widths use the same output unit and aggregation period. Divide the interval width by that model’s reference width before scoring. Changing the representation from units to thousands scales both widths together. The calibration version, reference width, unit, interval endpoints, coverage and scoring-rubric version are evidence for the answer. A missing or invalid width, interval, coverage match, validation date or calibration for an invoked model makes the shared score unavailable with the model and reason recorded. Never drop that model from the minimum. Evaluate the scoring algorithm only on a valid nonempty model set and a known parent confidence. All candidates retain their individual model-call traces.

#### A Simulated Outcome's ceiling

A Constraint on the Algorithm's output:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| rationale on every Simulated Outcome.confidence_score = null or rationale on every Simulated Outcome.confidence_score <= parent confidence score | after [`§ Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](#confidence-and-rationale-package-extended) | [`§ Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended [Step: 10]`](#confidence-and-rationale-package-extended) |

A downstream figure can never look more certain than the forecast it is built on. [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package)'s flagged-conflict ceiling applies the same discipline one stage earlier.

### Narrative rendering

Render the delivered stage records on demand. Predict supplies its forecast and rationale. Position supplies the delivered groups and their candidate prices, comparisons, trade-offs and inherited forecast evidence. Simulate supplies each member’s outcomes, call inputs and outputs, derived arithmetic and shared confidence evidence. A forecast-wide claim identifies the forecast or forecast rationale and field. A candidate claim identifies its delivery-scoped candidate and field. A group claim identifies its displayed group and the contributing members and fields. A derived value leads back to its inputs and versions. Restrict the renderer to this projection of the delivered records. If a value is unavailable, state its recorded reason. In a partial answer, describe only delivered stages and identify the missing ones.

Save the exact rendered wording, displayed order, membership and delivered labels on the Delivered Answer. Reopening a past answer reads these records. A fresh answer may regenerate the prose from its own pinned figures.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

A configured external rendering model receives only the forecast rationale. The installation composes the Position and Simulate clauses locally from the delivered fields and evidence references, then saves the assembled wording. After exhausted grouping retries it delivers completed outcomes with each candidate individually in canonical seed order and records why grouping was unavailable.

### Drill-down mechanics

Drill-down runs along independent axes, the ones [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage) promises. Each axis reuses the existing question intent rather than constructing a new one:
- **Granularity change, within the grid.** It re-executes the driver attribution and, where applicable, the positioning and simulation calls, scoped to a narrower geography still inside the materialized grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)). It uses the same model versions and weights, so the city-level answer is provably consistent with the state-level one it was drilled from.
- **Granularity change, below the grid.** It applies once a drill-down goes finer than the syndicated competitor data's own reporting granularity, typically county or store. At that resolution, no competitor signal is left to re-forecast from. The price and outcome figures shown are an allocation of the same figure at the nearest grounded geography above it, apportioned by population or retail-footprint weighting. They are not an independent forecast. They carry a distinct, visibly lower confidence tier rather than inheriting the parent forecast's confidence, so a user cannot mistake an estimate for a sourced number. An allocation never resolves its own currency. The finer geography it allocates to may have its own row and currency in [`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`](/specs/application/technical/data-model.md#geography) for an unrelated reason, such as Brand A's own POS reporting reaching finer than the materialized grid's ceiling. Even then, the allocation takes its currency unchanged from the nearest grounded ancestor it was allocated from, since scaling a number by a population or footprint weight never changes what currency it is in. Each allocated figure is shown with the figure it was apportioned from and the weighting used, as [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage § What a granularity drill-down shows`](/specs/application/product/answer-engine/drill-down.md#what-a-granularity-drill-down-shows) requires. The weighting is also the reason the allocated figure's confidence is lower. The decomposition graph does not extend below the grid at all. An allocation redistributes a quantity. It does not manufacture a causal explanation that was never computed for that geography. So Driver Attribution stops at the grid boundary, and the interface should say so rather than silently reusing or hiding the parent's driver breakdown.
- **Metric pivot.** It re-projects the existing output onto a different metric field (price to volume to margin to share). If that metric was already computed as part of the Simulated Outcome, the pivot is a display-only operation with no new model call. If it was not, the pivot triggers a new call against the cached question intent rather than a fresh retrieval.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

## Facts

**Records:**
  - **Name:** confidence input issues \
    **Type:** list<context<name: string, version: string, reason: string>> \
    **Means:** one check per invoked model version, with its identity and the first unusable calibration input, or an empty reason for a usable version

  - **Name:** model registry entries \
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>> \
    **Means:** the distinct name/version pairs actually used for this question, joined from the per-candidate call trace to the pinned registry entries

  - **Name:** simulate confidence weighting rubric \
    **Type:** context<model confidence: number, model freshness: number> \
    **Means:** the versioned rubric's weights for Simulate's model-confidence and model-freshness components

  - **Name:** parent confidence score \
    **Type:** number \
    **Means:** the parent Positioning Candidate's confidence score, inherited from its forecast, which caps every Simulated Outcome

  - **Name:** model confidence score \
    **Type:** function<number> -> number \
    **Means:** the pinned rubric’s common score for a dimensionless interval width, using the same versioned scoring bands for every model

  - **Name:** model confidence scores \
    **Type:** list<number> \
    **Initial Value:** [] \
    **Means:** the confidence-interval-width score for each simulation model

  - **Name:** scoring date \
    **Type:** date \
    **Means:** UTC calendar date of computed_at on the forecast’s pinned Data Vintage, retained on the simulation confidence evidence and used again at replay

  - **Name:** model freshness score \
    **Type:** function<date, date> -> number \
    **Means:** the pinned rubric’s score for elapsed calendar days from the validation date to the scoring date, each in UTC

  - **Name:** model freshness scores \
    **Type:** list<number> \
    **Initial Value:** [] \
    **Means:** the freshness score for each simulation model

  - **Name:** model confidence component \
    **Type:** number \
    **Means:** the lowest confidence-interval-width score among the simulation models

  - **Name:** model freshness component \
    **Type:** number \
    **Means:** the lowest freshness score among the simulation models

  - **Name:** simulate confidence weights \
    **Type:** context<model confidence: number, model freshness: number> \
    **Means:** the two component weights read from the simulate confidence weighting rubric

  - **Name:** Simulate confidence score \
    **Type:** number \
    **Means:** the completed confidence score for Simulate

  - **Name:** limiting confidence models \
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>> \
    **Means:** all pinned registry entries tied for the minimum confidence score for this question

  - **Name:** limiting freshness models \
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>> \
    **Means:** all pinned registry entries tied for the minimum freshness score for this question

  - **Name:** cap lowered? \
    **Type:** boolean \
    **Means:** whether the parent forecast's confidence score lowered Simulate's score

  - **Name:** confidence components \
    **Type:** context<model confidence: number, model freshness: number, confidence evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>>, freshness evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>>, cap lowered: boolean> \
    **Means:** each minimum, every versioned model tied for it and whether the candidate confidence capped the result

  - **Name:** retrieval trace \
    **Type:** list<context<candidate: string, name: string, version: string, inputs: context>> \
    **Means:** each actual candidate call, identified by candidate, model, version and supplied input values

  - **Name:** rationale on every Simulated Outcome \
    **Type:** context<scoring date: date, unavailable reason: string, input issues: list<context<name: string, version: string, reason: string>>, confidence_score: number, confidence_components: context<model confidence: number, model freshness: number, confidence evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>>, freshness evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, reference width: number, interval unit: string, calibration version: string, coverage: number, reference coverage: number, reference unit: string, interval period: string, reference period: string, last_validated: date>>, cap lowered: boolean>, retrieval_trace: list<context<candidate: string, name: string, version: string, inputs: context>>> \
    **Means:** the shared rationale with the limiting registry entries and all actual candidate calls

  - **Name:** match resolved? \
    **Type:** boolean \
    **Means:** true only if both product and geography match the candidate to the competitor at the selected level; unresolved or missing matches are false

  - **Name:** strategy name \
    **Type:** string \
    **Values:** "Hold", "Match", "Close the Gap", "Diverge" \
    **Means:** the strategy of the seeded candidate

  - **Name:** own price \
    **Type:** number \
    **Means:** Brand A’s effective price per unit at the forecast origin in the selected geography

  - **Name:** competitor start \
    **Type:** number \
    **Means:** the competitor’s effective price at that same origin in the same currency and per-unit basis

  - **Name:** competitor target \
    **Type:** number \
    **Means:** the forecast target effective price on the selected forecast, including its signed move

  - **Name:** candidate price \
    **Type:** number \
    **Means:** the candidate’s full-precision effective price per unit, or unavailable if a required input is unavailable

  - **Name:** unit volume \
    **Type:** number \
    **Means:** the projected number of Brand A units for this candidate and target period in the pinned volume unit

  - **Name:** unit share \
    **Type:** number \
    **Means:** projected Brand A volume divided by total category volume, a fraction in (0,1] for a valid category projection

  - **Name:** reference category volume \
    **Type:** number \
    **Means:** positive historical category units in the comparable prior-year period of the same length, seasonal alignment, category, geography and unit, from the pinned snapshot

  - **Name:** projected category units \
    **Type:** number \
    **Means:** the implied target-period units for the whole category, or null when its inputs are unavailable

  - **Name:** category volume growth \
    **Type:** number \
    **Means:** percentage change in physical category volume relative to the comparable historical period, or null when unavailable

  - **Name:** projected revenue \
    **Type:** number \
    **Means:** candidate effective price per unit times projected units on the same unit basis, in local currency for the period

  - **Name:** ordered candidates \
    **Type:** list<context<id: string, rank: number, values: list<number>>> \
    **Means:** positioned and simulated candidates sorted by ascending absolute price gap, unavailable gaps last, then the canonical Hold, Match, Close the Gap, Diverge order; rank is the one-based position in this sorted list

  - **Name:** comparison rules \
    **Type:** list<context<slot: number, relative: boolean, limit: number>> \
    **Means:** the pinned materiality settings for price gap, relative price index, share in percentage points, physical volume, category growth in percent, revenue and margin in its declared unit, one slot per field in that order; limit is in points for an absolute rule or a fraction for a relative rule

  - **Name:** visible groups \
    **Type:** list<list<context<id: string, rank: number, values: list<number>>>> \
    **Means:** ordered, nonempty groups of original ordered candidates shown on delivery

  - **Name:** previous members \
    **Type:** list<context<id: string, rank: number, values: list<number>>> \
    **Means:** the last visible group before the next candidate is considered, or an empty list at the start

  - **Name:** pair comparable? \
    **Type:** boolean \
    **Means:** whether the candidate and every member of the last group have all required values within their field thresholds

## Open Questions

**Records:**

- **Name:** Default Materiality Thresholds
  **Open Question:** What default materiality threshold, and what bounds, does Acme AI provide for each decision-facing field of a positioning option, until real data calibrates them?
  **Provisional Answer:** The default threshold is 1 point for share and for relative_price_index. For every other decision-facing field (price_gap, volume, category_growth, revenue and margin), the default threshold is 1% of the larger magnitude of the two values compared. A Control plane admin may set each anywhere from zero to twice its default. A field whose two values are identical never keeps a pair apart, since its delta of zero is at or under any threshold.
  **Impacts:** [`§ Layered Output Synthesis (producing the answer) § Option Consolidation [Step: 4]`](#option-consolidation), and the false-choice failure mode that section avoids; options with essentially the same outcome shown as one ([`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)); the bounds a Control plane admin sets each threshold within ([`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings)); and the control plane's self-service bounds for materiality thresholds ([`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path)).
