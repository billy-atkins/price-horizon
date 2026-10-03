## Layered Output Synthesis (producing the answer)

Where Predict's evidence becomes an answer a user can act on. This layer consumes the driver attribution output from `specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`. Predict's own layers (scorecard, narrative, map, decomposition) are direct renderings of that output and require no additional modeling. Position and Simulate do.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.

### Price gap and relative price index, defined

Price gap is the absolute difference between Brand A's price and the competitor's forecasted price, in currency terms, at whatever geography and horizon the query specifies. Both sides are always the same geography's own price, in that geography's own resolved currency (`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`), a cross-currency price gap never occurs since the comparison is never made across geographies. Relative price index is the same comparison expressed as a ratio, Brand A's price divided by the competitor's price, times 100, so a value above 100 means Brand A sits at a premium and below 100 means Brand A sits at a discount. Relative price index carries no currency at all, a ratio of two same-currency figures cancels the unit; nothing in this design compares one geography's relative price index against another's, this is a property of the number, not a feature built on it. Both sides of the comparison are effective price, not list price, comparing Brand A's list price against the competitor's forecasted effective price would be comparing two different things after all the work spent decomposing the competitor's side. Both are Position-stage outputs, computed once per positioning candidate by the positioning engine, not asserted numbers, and both belong in the governed glossary alongside effective price. The plain-language rendering of both, for a business reader, is in `specs/application/product/answer-engine/position.md § Position — where Brand A should sit`.

### Positioning engine

Takes the Predict output (the competitor's forecasted move, its direction, confidence) together with Brand A's current price, margin targets, and elasticity model, and generates a bounded set of named Positioning Candidates (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`), each scored for price gap and relative price index at the granularity the query specifies. The candidate set is deliberately small and named, not the output of an optimizer picking a single "best" answer — these are meant to be framed for judgment, not decided for the user. The engine runs in stages, seeding then collapsing, so the count stays deterministic and testable rather than a judgment call made per query.

**Archetypes, a Decision Table —** canonical positioning strategies, spanning the response spectrum from full commitment to the current price to full divergence from the competitor, each defined by the exact rule that sets Brand A's resulting effective price at the horizon, not just a qualitative description:

| Archetype | Brand A's resulting effective price at the horizon |
|---|---|
| Hold | Unchanged from Brand A's current effective price, regardless of the competitor's predicted move |
| Match | Moved by the same percentage change as the competitor's forecasted move, so the relative price index stays exactly what it is today |
| Close the gap | Moved half the percentage difference between Hold and Match |
| Diverge | Moved further in whatever direction Brand A already sits relative to the competitor, premium gets more premium, discount gets more discount, scaled to the size of the competitor's forecasted move |

Each candidate's price gap and relative price index (`§ Layered Output Synthesis (producing the answer) § Price gap and relative price index, defined`) take Brand A's side from that candidate's resulting price, since each archetype implies a different one, the price gap being that resulting price minus the competitor's forecasted effective price at the same geography and horizon. The plain-language rendering of these strategies, for a business reader, is in `specs/application/product/answer-engine/position.md § Position — where Brand A should sit`.

**Seeding, a Decision Table —** which archetypes are generated as candidates, decided before any simulation runs, by the decision type the Question Intent carries (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`):

| Decision type | Seeded candidates |
|---|---|
| Strategic, a brand pricing decision on list price or price position | Hold, Match, Close the Gap, Diverge |
| Tactical, a retailer or promotional decision | Hold, Match, Close the Gap |

Diverge is withheld from a tactical decision because it moves the brand's price position, which a retailer or promotional decision does not own.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

### Option Consolidation

An Algorithm, applied after the simulation engine (`§ Layered Output Synthesis (producing the answer) § Simulation engine`) has produced an outcome for every seeded candidate.

| Step | Action |
|---|---|
| 1 | Sort seeded candidates by price gap, ascending |
| 2 | Walk adjacent pairs. For each pair, compute the delta across every decision-facing field of that candidate's Positioning Candidate (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Positioning Candidate`) and Simulated Outcome (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Simulated Outcome`), price_gap, relative_price_index, share, volume, category_growth, revenue, and margin; each structure's own rationale field, and the confidence and retrieval-trace data it carries, is never part of this comparison |
| 3 | If every one of those deltas falls at or under its own materiality threshold, whose default is `§ Open Questions [Name: Default Materiality Thresholds]`, consolidate the pair into a single displayed option, labeled with both archetype names |
| 4 | If any single metric exceeds its threshold, the pair stays separate even if the rest agree, a real difference on one dimension is still a real choice |
| 5 | Repeat from step 2 until no adjacent pair is at or under threshold, or the set reaches a floor of two options, whichever comes first |

A Constraint on this Algorithm's output: the floor is two, not one. Consolidation can thin the set, it can never reduce Position to a single recommendation, that would violate the guarantee that Position stays framed as a choice. Enforced by step 5's floor, and by the API and UI contract, which never exposes a single-option response.

This keeps the option count deterministic and evaluable, `specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`'s golden-question harness can assert both the seeded set for a given decision type and the consolidation outcome for a given pair of simulated results, while avoiding the false-choice failure mode of always forcing the same number of options regardless of whether the underlying numbers actually differ.

A business unit's own materiality thresholds are set as `specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings` describes.

### Simulation engine

For each candidate from the positioning engine, calls the share-response, volume, and margin models in the registry once per candidate. Category growth is the same share-response and volume output aggregated to the category level rather than a separate model, and revenue is a direct calculation, price times volume, in the query's own geography's resolved currency, not a model call, deterministic tool arithmetic rather than something requiring its own registry entry. Together these produce a Simulated Outcome (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Simulated Outcome`) per option. Every seeded candidate is simulated, not a user-selected one, since the whole point of this stage is trade-offs visible before a choice is made, not computed after. These calls run in parallel across candidates, the same reasoning as parallel evidence retrieval in `specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval`, a call to every simulation model for every candidate would otherwise add up before an answer is ever shown, and Position and Simulate are meant to arrive as part of the first answer, not a cost paid only after a user has already committed to drilling down. Because every candidate is run through the same versioned models against the same as-of data, the options are directly comparable to each other, not independently generated estimates that happen to be displayed side by side.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

### Confidence and rationale packaging, extended

The Rationale Record (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`) described in `specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging` for the Predict output attaches to every Position option as that same record, individually copied rather than recomputed: positioning applies a fixed archetype rule to the forecast, it introduces no new source of uncertainty the Predict-stage packaging could have missed. A positioning option is only as trustworthy as the forecast and elasticity model it is built on: if the underlying Predict confidence is low, every option downstream carries that same flag rather than presenting false certainty at a later stage.

Every Simulated Outcome for a given query instead carries its own Rationale Record, since the share-response, volume, and margin models it calls are a genuinely different source of uncertainty, one the Model registry (`specs/application/technical/model-registry.md § Model registry`) already documents with a confidence interval and a last-validated date of its own. That record is computed once per query, not once per candidate: the same model versions are called for every seeded candidate, so nothing in this section's Algorithm varies across the candidates in one answer, only across queries, or over time as models are revalidated. A Query user opens these reasons from the outcome itself (`specs/application/product/answer-engine/simulate.md § Simulate — what follows for the business`). Computed by an Algorithm.

| Step | Action |
|---|---|
| 1 | For the share-response model, retrieve its declared confidence interval and last-validated date |
| 2 | Repeat step 1 for the volume and margin models |
| 3 | For each model, compute its confidence interval's width (upper bound minus lower bound) and score that width against the simulate confidence weighting rubric's declared confidence-interval-width bands |
| 4 | Score the model confidence component as the lowest of the scores from step 3, not an average, so one under-validated model is never diluted by the strong ones, the same weakest-link principle already applied to source credibility in `specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging` |
| 5 | For each model, score model freshness against the simulate confidence weighting rubric's own declared staleness bands, using that model's last-validated date; distinct bands from the ones data freshness uses elsewhere, a model's revalidation cadence is a materially different order of magnitude from the data pipeline's daily-or-weekly cadence |
| 6 | Score the model freshness component as the lowest of the scores from step 5, the same weakest-link principle as step 4 |
| 7 | Look up the model confidence and model freshness components' weights in the simulate confidence weighting rubric |
| 8 | Multiply each component by its weight and sum them to get this query's confidence_score for Simulate |
| 9 | Cap confidence_score at the parent Positioning Candidate's own rationale.confidence_score, regardless of what step 8 produced, and record in confidence_components whether the cap lowered it |
| 10 | Attach this same confidence_score, its confidence_components, and a retrieval_trace naming the models and the inputs each was called with, as the rationale on every Simulated Outcome in this query's answer, computed once here and copied, not recomputed per candidate |

A Constraint on this Algorithm's output: a Simulated Outcome's confidence_score is never higher than its parent Positioning Candidate's. Enforced by step 9, so a downstream figure can never look more certain than the forecast it is built on, the same discipline `specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale packaging`'s flagged-conflict ceiling already applies one stage earlier.

This Rationale Record carries none of the Predict computation's own fields (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`). category_growth and revenue inherit this same confidence_score by construction, both derive from the same models' outputs rather than a model call of their own (`§ Layered Output Synthesis (producing the answer) § Simulation engine`).

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` renders this.

### Narrative rendering

Determinism is scoped to the structured facts, the number, the direction, the magnitude, the price gap, the simulated margin and share outcomes, the confidence score, the driver contribution breakdown, not to the prose describing them: those facts come out identical every time against unchanged data, application version, model versions, business unit configuration version, and kind of decision, but the sentence describing a 2.3 percent increase may say "a modest increase" in one rendering and "a slight uptick" in another without changing what the executive should do with it. Rendering is a lightweight, on-demand step: it takes the rationale record, from the materialized grid or the live path, whichever applies, and generates prose from it fresh every time an answer is served, rather than precomputing and storing text. The rendering model is constrained to the fields in that record and nothing else, no external knowledge, no invented values, every statement in the rendered text has to map to a field in the record it was given. This runs the same way for every stage, Predict, Position, and Simulate each have their own rationale, rendered fresh from it.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.

### Drill-down mechanics

Independent axes, the ones `specs/application/product/answer-engine/drill-down.md § Drill-down — cross-cutting, available at every stage` promises, each reusing the existing question intent rather than constructing a new one:
- **Granularity change, within the grid —** it re-executes the driver attribution and, where applicable, the positioning and simulation calls, scoped to a narrower geography still inside the materialized grid (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`), using the same model versions and weights, so the city-level answer is provably consistent with the state-level one it was drilled from.
- **Granularity change, below the grid —** it applies once a drill-down goes finer than the syndicated competitor data's own reporting granularity, county or store, typically. There is no competitor signal left to re-forecast from at that resolution. The price and outcome figures shown are an allocation of the same figure at the nearest grounded geography above it, apportioned by population or retail-footprint weighting, not an independent forecast, and they carry a distinct, visibly lower confidence tier rather than inheriting the parent forecast's confidence, so a user cannot mistake an estimate for a sourced number. An allocation never resolves its own currency, even if the finer geography it allocates to has its own row and currency in `specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography` for an unrelated reason, such as Brand A's own POS reporting reaching finer than the materialized grid's ceiling; it takes its currency unchanged from the nearest grounded ancestor it was allocated from, since scaling a number by a population or footprint weight never changes what currency it's in. Each allocated figure is shown with the figure it was apportioned from and the weighting used, which is also the reason its confidence is lower, as `specs/application/product/answer-engine/drill-down.md § Drill-down — cross-cutting, available at every stage` requires. The decomposition graph does not extend below the grid at all, an allocation redistributes a quantity, it does not manufacture a causal explanation that was never computed for that geography, so Driver Attribution stops at the grid boundary and the interface should say so rather than silently reusing or hiding the parent's driver breakdown.
- **Metric pivot —** it re-projects the existing output onto a different metric field (price to volume to margin to share). If that metric was already computed as part of the Simulated Outcome, this is a display-only operation with no new model call; if it was not, it triggers a new call against the cached question intent rather than a fresh retrieval.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.

## Open Questions

**Records:**

- **Name:** Default Materiality Thresholds
  **Open Question:** What default materiality threshold, and what bounds, does Acme AI provide for each decision-facing field of a positioning option, until real data calibrates them?
  **Provisional Answer:** The default threshold is 1 point for share and for relative_price_index, and, for every other decision-facing field, price_gap, volume, category_growth, revenue and margin, 1% of the larger magnitude of the two values compared. A Control plane admin may set each anywhere from zero to twice its default. A field whose two values are identical never keeps a pair apart, since its delta of zero is at or under any threshold.
  **Impacts:** step 3 of the Algorithm in `§ Layered Output Synthesis (producing the answer) § Option Consolidation`, and the false-choice failure mode that section avoids; options with essentially the same outcome shown as one (`specs/application/product/answer-engine/position.md § Position — where Brand A should sit`); the bounds a Control plane admin sets each threshold within (`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`); and the control plane's self-service bounds for materiality thresholds (`specs/application/technical/control-plane-service/control-plane.md § Control Plane`).
