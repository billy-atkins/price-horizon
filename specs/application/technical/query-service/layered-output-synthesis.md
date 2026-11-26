## Layered Output Synthesis (producing the answer)

This layer turns Predict's evidence into an answer a user can act on. It consumes the driver attribution output from [`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution). Predict's own layers (scorecard, narrative, map, decomposition) are direct renderings of that output and require no additional modeling. Position and Simulate do.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

### Price gap and relative price index, defined

Price gap is the absolute difference between Brand A's price and the competitor's forecast price, in currency terms, at whatever geography and horizon the query specifies. Both sides are always the same geography's own price, in that geography's own resolved currency ([`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`](/specs/application/technical/data-model.md#geography)). A cross-currency price gap never occurs, since the comparison is never made across geographies.

Relative price index is the same comparison expressed as a ratio: Brand A's price divided by the competitor's price, times 100. A value above 100 means Brand A sits at a premium, and a value below 100 means Brand A sits at a discount. Relative price index carries no currency at all, because a ratio of two same-currency figures cancels the unit. This is a property of the number, not a feature built on it. Nothing in this design compares one geography's relative price index against another's.

Both sides of the comparison are effective price, not list price. Comparing Brand A's list price against the competitor's forecast effective price would compare two different things, after all the work spent decomposing the competitor's side. Price gap and relative price index are both Position-stage outputs. The positioning engine computes both once per positioning candidate, so neither is an asserted number. Both belong in the governed glossary alongside effective price. The plain-language rendering of both, for a business reader, is in [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit).

### Positioning engine

The positioning engine takes the Predict output (the competitor's forecast move, its direction, confidence) together with Brand A's current price, margin targets, and elasticity model. From them, the engine generates a bounded set of named Positioning Candidates ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`](/specs/application/technical/data-model.md#positioning-candidate)). The engine scores each candidate for price gap and relative price index at the granularity the query specifies. The candidate set is small and named, not the output of an optimizer picking a single "best" answer. The candidates are framed for the user's judgment, not decided for the user. The engine runs in stages, seeding then collapsing, so the count stays deterministic and testable rather than a judgment call made per query.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Archetypes

The archetypes are canonical positioning strategies. They span the response spectrum, from full commitment to the current price to full divergence from the competitor. Each is defined by the exact rule that sets Brand A's resulting effective price at the horizon, not by a qualitative description alone:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Archetype

**Input Values:**
- Archetype: "Hold", "Match", "Close the Gap", "Diverge"

| Archetype | Brand A's resulting effective price at the horizon |
|---|---|
| Hold | Unchanged from Brand A's current effective price, regardless of the competitor's predicted move |
| Match | Moved by the same percentage change as the competitor's forecast move, so the relative price index stays exactly what it is today |
| Close the Gap | Moved half the percentage difference between Hold and Match |
| Diverge | Moved further in whatever direction Brand A already sits relative to the competitor, premium gets more premium, discount gets more discount, scaled to the size of the competitor's forecast move |

Each candidate's price gap and relative price index ([`§ Layered Output Synthesis (producing the answer) § Price gap and relative price index, defined`](#price-gap-and-relative-price-index-defined)) take Brand A's side from that candidate's resulting price, since each archetype implies a different one. The price gap is that resulting price minus the competitor's forecast effective price at the same geography and horizon. The plain-language rendering of these strategies, for a business reader, is in [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit § The Strategies`](/specs/application/product/answer-engine/position.md#the-strategies).

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

Option Consolidation is an Algorithm. It runs after the simulation engine ([`§ Layered Output Synthesis (producing the answer) § Simulation engine`](#simulation-engine)) has produced an outcome for every seeded candidate.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:** the seeded candidates' Positioning Candidates and Simulated Outcomes, and the business unit's materiality thresholds

**Output:** the options Position displays, each a candidate or candidates consolidated into one

| Step | Action |
|---|---|
| 1 | Sort the seeded candidates by price gap, ascending, those with the same price gap in the order [`§ Layered Output Synthesis (producing the answer) § Positioning engine § Archetypes`](#archetypes) lists them, each an option |
| 2 | Take as the pair the first two options in that order |
| 3 | Compute, for every decision-facing field of the Positioning Candidates ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`](/specs/application/technical/data-model.md#positioning-candidate)) and Simulated Outcomes ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Simulated Outcome`](/specs/application/technical/data-model.md#simulated-outcome)), price_gap, relative_price_index, share, volume, category_growth, revenue, and margin, the delta, the absolute difference, between each candidate one option of the pair holds and each candidate the other option holds; each structure's own rationale field, and the confidence and retrieval-trace data it carries, is never part of this comparison |
| 4 | If every one of those deltas falls at or under its own materiality threshold for the two values it compares, whose default is [`§ Open Questions [Name: Default Materiality Thresholds]`](#open-questions), continue; otherwise, the pair staying separate even if the rest agree, since a real difference on one dimension is still a real choice, Go to step 7 |
| 5 | Consolidate the pair into a single displayed option, labeled with the archetype name of every candidate it holds, in that order |
| 6 | If the set has reached a floor of two options, End; otherwise, continue |
| 7 | If an option lies directly above the pair in the order step 1 sorted them, take it and the option directly below it as the pair, Go to step 3; otherwise, End |

This keeps the option count deterministic and evaluable. [`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)'s golden-question harness can assert both the seeded set for a given decision type and the consolidation outcome for a given set of simulated results. Consolidation also avoids the false-choice failure mode: always forcing the same number of options, whether or not the underlying numbers differ.

A business unit's own materiality thresholds are set as [`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings) describes.

#### A choice, never one option

A Constraint on the consolidation Algorithm's output:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| Consolidation can thin the set, but never below two options, so it never reduces Position to a single recommendation | the options Position displays | [`§ Layered Output Synthesis (producing the answer) § Option Consolidation [Step: 6]`](#option-consolidation)'s floor, and the API and UI contract, which never exposes a single-option response |

A single option would break the guarantee that Position stays framed as a choice.

### Simulation engine

For each candidate from the positioning engine, the simulation engine calls the share-response, volume, and margin models in the registry, once per candidate. Category growth is the same share-response and volume output aggregated to the category level, not a separate model. Revenue is a direct calculation, price times volume, in the query's own geography's resolved currency. Revenue is deterministic tool arithmetic, not a model call, so it needs no registry entry of its own. Together these produce a Simulated Outcome ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Simulated Outcome`](/specs/application/technical/data-model.md#simulated-outcome)) per option. The engine simulates every seeded candidate, not a user-selected one, because this stage exists to make trade-offs visible before a choice is made, not to compute them after.

These calls run in parallel across candidates, for the same reason as parallel evidence retrieval in [`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`](/specs/application/technical/query-service/intent-and-retrieval.md#parallel-evidence-retrieval). Otherwise, a call to every simulation model for every candidate would add up before an answer is ever shown. Position and Simulate are meant to arrive as part of the first answer, not as a cost paid only after a user has already committed to drilling down. Every candidate is run through the same versioned models against the same as-of data. So the options are directly comparable to each other, not independently generated estimates that happen to be displayed side by side.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

### Confidence and rationale package, extended

The Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)) described in [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package) for the Predict output attaches to every Position option. Each option carries that same record, copied individually rather than recomputed. Positioning applies a fixed archetype rule to the forecast, so it introduces no new source of uncertainty the Predict-stage packaging could have missed. A positioning option is only as trustworthy as the forecast and elasticity model it is built on. If the underlying Predict confidence is low, every option downstream carries that same flag rather than presenting false certainty at a later stage.

Each Simulated Outcome carries the rationale computed for its question. The share-response, volume and margin models run for each candidate. Their versions, confidence intervals and validation dates are shared across the question, so the live simulation stage computes the rationale once and attaches it to every outcome. The model registry supplies the inputs ([`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)). A Query user can open the rationale from any outcome ([`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - model registry entries
  - retrieval trace
  - simulate confidence weighting rubric
  - parent confidence score

**Output:**
  - rationale on every Simulated Outcome

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)

| Step | Action |
|---|---|
| 1 | Set model confidence scores to for entry in model registry entries return model confidence score(entry.confidence_interval_upper - entry.confidence_interval_lower) |
| 2 | Set model freshness scores to for entry in model registry entries return model freshness score(entry.last_validated) |
| 3 | Set model confidence component to min(model confidence scores) |
| 4 | Set model freshness component to min(model freshness scores) |
| 5 | Set simulate confidence weights to {model confidence: simulate confidence weighting rubric.model confidence, model freshness: simulate confidence weighting rubric.model freshness} |
| 6 | Set Simulate confidence score to model confidence component * simulate confidence weights.model confidence + model freshness component * simulate confidence weights.model freshness |
| 7 | Set cap lowered? to Simulate confidence score > parent confidence score |
| 8 | Set Simulate confidence score to min(Simulate confidence score, parent confidence score) |
| 9 | Set limiting confidence models to model registry entries[model confidence score(item.confidence_interval_upper - item.confidence_interval_lower) = model confidence component] |
| 10 | Set limiting freshness models to model registry entries[model freshness score(item.last_validated) = model freshness component] |
| 11 | Set rationale on every Simulated Outcome to {confidence_score: Simulate confidence score, confidence_components: {model confidence: model confidence component, model freshness: model freshness component, confidence evidence: limiting confidence models, freshness evidence: limiting freshness models, cap lowered: cap lowered?}, retrieval_trace: retrieval trace} |
| 12 | End |

This Rationale Record carries none of the Predict computation's own fields ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)). category_growth and revenue inherit this same confidence_score by construction, because both derive from the same models' outputs rather than from a model call of their own ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Simulation engine`](/specs/application/technical/query-service/layered-output-synthesis.md#simulation-engine)). Predict's confidence does not read a model's last-validated date; that treatment remains provisional in [`specs/application/technical/model-registry.md § Open Questions [Name: Model Freshness in Predict]`](/specs/application/technical/model-registry.md#open-questions). Simulate reads it through this package, as the provisional answer's other side.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) renders this.

#### A Simulated Outcome's ceiling

A Constraint on the Algorithm's output:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| Simulate confidence score <= parent confidence score | after [`§ Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended`](#confidence-and-rationale-package-extended) | [`§ Layered Output Synthesis (producing the answer) § Confidence and rationale package, extended [Step: 8]`](#confidence-and-rationale-package-extended) |

A downstream figure can never look more certain than the forecast it is built on. [`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package)'s flagged-conflict ceiling applies the same discipline one stage earlier.

### Narrative rendering

Determinism is scoped to the structured facts, not to the prose describing them. The structured facts are the number, the direction, the magnitude, the price gap, the simulated margin and share outcomes, the confidence score, and the driver contribution breakdown. Those facts come out identical every time against unchanged data, application version, model versions, business unit configuration version, and kind of decision. The sentence describing a 2.3 percent increase may say "a modest increase" in one rendering and "a slight uptick" in another, without changing what the executive should do with it.

Rendering is a lightweight, on-demand step. It takes the rationale record, from the materialized grid or the live path, whichever applies. It generates prose from that record fresh every time an answer is served, rather than precomputing and storing text. The rendering model is constrained to the fields in that record and nothing else: no external knowledge, no invented values. Every statement in the rendered text has to map to a field in the record the rendering model was given. Rendering runs the same way for every stage. Predict, Position, and Simulate each have their own rationale, and each stage's text is rendered fresh from it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

### Drill-down mechanics

Drill-down runs along independent axes, the ones [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage) promises. Each axis reuses the existing question intent rather than constructing a new one:
- **Granularity change, within the grid.** It re-executes the driver attribution and, where applicable, the positioning and simulation calls, scoped to a narrower geography still inside the materialized grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)). It uses the same model versions and weights, so the city-level answer is provably consistent with the state-level one it was drilled from.
- **Granularity change, below the grid.** It applies once a drill-down goes finer than the syndicated competitor data's own reporting granularity, typically county or store. At that resolution, no competitor signal is left to re-forecast from. The price and outcome figures shown are an allocation of the same figure at the nearest grounded geography above it, apportioned by population or retail-footprint weighting. They are not an independent forecast. They carry a distinct, visibly lower confidence tier rather than inheriting the parent forecast's confidence, so a user cannot mistake an estimate for a sourced number. An allocation never resolves its own currency. The finer geography it allocates to may have its own row and currency in [`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`](/specs/application/technical/data-model.md#geography) for an unrelated reason, such as Brand A's own POS reporting reaching finer than the materialized grid's ceiling. Even then, the allocation takes its currency unchanged from the nearest grounded ancestor it was allocated from, since scaling a number by a population or footprint weight never changes what currency it is in. Each allocated figure is shown with the figure it was apportioned from and the weighting used, as [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage § What a granularity drill-down shows`](/specs/application/product/answer-engine/drill-down.md#what-a-granularity-drill-down-shows) requires. The weighting is also the reason the allocated figure's confidence is lower. The decomposition graph does not extend below the grid at all. An allocation redistributes a quantity. It does not manufacture a causal explanation that was never computed for that geography. So Driver Attribution stops at the grid boundary, and the interface should say so rather than silently reusing or hiding the parent's driver breakdown.
- **Metric pivot.** It re-projects the existing output onto a different metric field (price to volume to margin to share). If that metric was already computed as part of the Simulated Outcome, the pivot is a display-only operation with no new model call. If it was not, the pivot triggers a new call against the cached question intent rather than a fresh retrieval.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

## Facts

**Records:**
  - **Name:** model registry entries \
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>> \
    **Means:** the distinct name/version pairs actually used for this question, joined from the per-candidate call trace to the pinned registry entries

  - **Name:** simulate confidence weighting rubric \
    **Type:** context<model confidence: number, model freshness: number> \
    **Means:** the versioned rubric's weights for Simulate's model-confidence and model-freshness components

  - **Name:** parent confidence score \
    **Type:** number \
    **Means:** the parent Positioning Candidate's confidence score, inherited from its forecast, which caps every Simulated Outcome

  - **Name:** model confidence score \
    **Type:** function<number> -> number \
    **Means:** the rubric's score for one model's confidence-interval width

  - **Name:** model confidence scores \
    **Type:** list<number> \
    **Initial Value:** [] \
    **Means:** the confidence-interval-width score for each simulation model

  - **Name:** model freshness score \
    **Type:** function<date> -> number \
    **Means:** the rubric's staleness score for one model's last-validated date

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
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>> \
    **Means:** all pinned registry entries tied for the minimum confidence score for this question

  - **Name:** limiting freshness models \
    **Type:** list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>> \
    **Means:** all pinned registry entries tied for the minimum freshness score for this question

  - **Name:** cap lowered? \
    **Type:** boolean \
    **Means:** whether the parent forecast's confidence score lowered Simulate's score

  - **Name:** confidence components \
    **Type:** context<model confidence: number, model freshness: number, confidence evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>>, freshness evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>>, cap lowered: boolean> \
    **Means:** each minimum, every versioned model tied for it and whether the candidate confidence capped the result

  - **Name:** retrieval trace \
    **Type:** list<context<candidate: string, name: string, version: string, inputs: context>> \
    **Means:** each actual candidate call, identified by candidate, model, version and supplied input values

  - **Name:** rationale on every Simulated Outcome \
    **Type:** context<confidence_score: number, confidence_components: context<model confidence: number, model freshness: number, confidence evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>>, freshness evidence: list<context<name: string, version: string, confidence_interval_lower: number, confidence_interval_upper: number, last_validated: date>>, cap lowered: boolean>, retrieval_trace: list<context<candidate: string, name: string, version: string, inputs: context>>> \
    **Means:** the shared rationale with the limiting registry entries and all actual candidate calls

## Open Questions

**Records:**

- **Name:** Default Materiality Thresholds
  **Open Question:** What default materiality threshold, and what bounds, does Acme AI provide for each decision-facing field of a positioning option, until real data calibrates them?
  **Provisional Answer:** The default threshold is 1 point for share and for relative_price_index. For every other decision-facing field (price_gap, volume, category_growth, revenue and margin), the default threshold is 1% of the larger magnitude of the two values compared. A Control plane admin may set each anywhere from zero to twice its default. A field whose two values are identical never keeps a pair apart, since its delta of zero is at or under any threshold.
  **Impacts:** [`§ Layered Output Synthesis (producing the answer) § Option Consolidation [Step: 4]`](#option-consolidation), and the false-choice failure mode that section avoids; options with essentially the same outcome shown as one ([`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)); the bounds a Control plane admin sets each threshold within ([`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings)); and the control plane's self-service bounds for materiality thresholds ([`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path)).
