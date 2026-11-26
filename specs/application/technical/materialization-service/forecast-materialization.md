## Forecast materialization

The Predict computation in [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation) does not wait for a question to be asked. It produces the prepared forecast that [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do) describes a question retrieving. The computation runs nightly, whenever the underlying competitor data refreshes, or on demand when a control plane admin triggers it for their own business unit. Each run covers a grid of competitor, brand, geography, and horizon, with horizons of 1, 3, 6, and 12 months. For each combination, the run computes and stores an Effective Price Forecast ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)): the forecast and its rationale together, as facts. A rendered sentence about those facts is not stored here. [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Narrative rendering`](/specs/application/technical/query-service/layered-output-synthesis.md#narrative-rendering) produces it separately.

The geography axis of that grid is not independently curated. [`specs/application/technical/materialization-service/reconciliation.md § Product and Geography Reconciliation`](/specs/application/technical/materialization-service/reconciliation.md#product-and-geography-reconciliation) sets it, typically to country, state or province, and major metro. That reconciled boundary is the coarsest input in the whole chain, and it determines what can be forecast rather than estimated. Brand A's internal POS data is available far finer, down to individual stores, but that never buys back resolution on the competitor side. Position and Simulate both depend on the competitor forecast as an input, so the entire answer inherits this same geographic ceiling, not only Predict.

For each run, read one effective revision of [`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Tracked brand membership`](/specs/application/technical/data-model.md#tracked-brand-membership) and pin the reconciled markets, standard horizons, data vintage, full forecast model map, business-unit configuration and application version in an immutable publication manifest. Stage the forecast and rationale for each required key under the run ID. If any key lacks a single supported measurement window or a completed bundle, the run fails and the unit keeps its preceding publication, or remains unavailable on its first run. Switch the unit’s current publication in one transaction only when every required key has a complete bundle and the run still owns the expected predecessor. A failed or superseded run cannot expose staged rows. Readers capture one published manifest per request. For forecast selection in a business unit, retirement takes effect when the first complete publication excluding the competitor replaces the previous one. A requested retirement stays pending for that unit through a failed refresh. From the switch onward new requests can neither select a retired brand nor compute an outside-grid forecast for it. Earlier published forecasts and deliveries stay addressable by ID.

Materializing the full grid eagerly, rather than computing narrower slices on demand, trades infrastructure cost for response time by design. The primary user is a time-constrained executive, who reacts to a slow or clunky tool by switching to a competing one, not by tolerating it. For that user, a search-box-fast answer across the whole grid a business unit tracks matters more than the compute spent on combinations a given query never touches. Storage and compute are the cheaper side of that trade.

The dead-zone threshold is the part of a business unit's own configuration that a forecast depends on. A self-service edit to it does not retroactively touch a cell already computed under whatever configuration was in effect when that cell ran. The edit takes effect starting at that cell's next materialization, whether nightly, on a data refresh, or on demand. A cell's business_unit_configuration_version ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)) records which configuration the cell was produced under.

At most one materialization run is in flight per business unit at a time, and at most one more waits behind it. If the nightly schedule, a data refresh, and an on-demand trigger all land close together, the first to start runs to completion. One further trigger queues to run immediately after, and that queued run picks up whatever data and configuration are current by then. Any trigger beyond that is a no-op, because the queued run will reflect it anyway. The limit is keyed per business unit, not per installation, so one business unit's runs never wait on another's. The same orchestration engine ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations`](/specs/application/technical/engineering-and-production-considerations.md#engineering-and-production-considerations)) that runs the job enforces the limit. No separate scheduling layer has to be kept in sync with it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

A Control plane admin's on-demand run is the one [`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings) describes.

### Forecast period

Persist the origin date, horizon, target date, measurement basis, inclusive window start and exclusive end with both scheduled and live forecasts. Resolve a relative month horizon by adding calendar months to the UTC date of the data vintage, clipping to the destination month’s last day. Preserve the requested unit for other supported horizons. The target measurement interval is the single declared observation period for that forecast’s effective-price series that contains the target date. Use the pinned source calendar and price basis for that series; an ambiguous or unsupported basis makes that forecast unavailable. Do not average prices over the whole lead time. A daily series with a March 1 origin and a six-month horizon has window [September 1, September 2); a monthly series has [September 1, October 1). Both computation and comparison take those exact boundaries.

## Realized outcome check

On every materialization cadence, consider each successfully published batch forecast and each committed live forecast, including those with no deliveries. Recover legacy periods only from the original pinned grid key or question, vintage and measurement calendar when they yield exactly one interval. Irrecoverable original comparison terms or an ambiguous interval give an unevaluable reason. A valid interval whose exclusive end is later than the check cutoff is pending period. Once elapsed, use the first complete comparable actuals vintage available at the check cutoff, in ingestion order with the immutable vintage ID breaking ties. Insufficient coverage is pending actuals and is retried. Compare the same unit, competitor brand, geography, currency, physical unit, price basis and interval. Reconstruct the effective observation with the same period aggregation and net components as Predict. A zero starting price leaves percentage direction undefined for a nonzero move; if that direction is required to decide an out-of-band verdict, mark the comparison unevaluable and retain the reason. Zero move is stable; an in-band move can still be judged without dividing by the starting price.

Only a scored result creates a Realized Outcome. In one transaction insert against a unique forecast ID, recording the compared window, observed effective price, actuals vintage and source references, move, error and verdict. A concurrent or retried check returns the winning stored result. Later observations cannot rewrite it. For each unscored forecast retain the latest check’s cutoff, state and reason together, separately from the immutable forecast. An older check cannot replace a newer disposition. A scored outcome takes precedence over every unscored check. Report the recorded reason verbatim with the state.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - forecast comparison
  - observation eligibility
  - observed price
  - existing comparison

**Output:**
  - comparison result

**Runs When:**
  - the scheduled outcome-check job considers one persisted forecast

| Step | Action |
|---|---|
| 1 | If existing comparison != null, Set comparison result to existing comparison, End; otherwise, continue |
| 2 | If observation eligibility.state != "ready", Set comparison result to {state: observation eligibility.state, reason: observation eligibility.reason, move: null, error: null, verdict: null}, End; otherwise, continue |
| 3 | Set actual move to observed price - forecast comparison.start |
| 4 | If forecast comparison.start = 0 and actual move != 0 and (actual move < forecast comparison.lower or actual move > forecast comparison.upper), Set comparison result to {state: "unevaluable", reason: "zero starting price prevents direction comparison", move: actual move, error: forecast comparison.move - actual move, verdict: null}, End; otherwise, continue |
| 5 | Set signed error to forecast comparison.move - actual move |
| 6 | Set actual direction to if actual move = 0 then "stable" else if forecast comparison.start > 0 and abs(actual move) < forecast comparison.threshold * forecast comparison.start then "stable" else if actual move > 0 then "increase" else "decrease" |
| 7 | Set comparison result to {state: "scored", reason: null, move: actual move, error: signed error, verdict: if forecast comparison.lower <= actual move and actual move <= forecast comparison.upper then "Right" else if forecast comparison.direction = actual direction then "Right direction" else "Wrong"} |
| 8 | End |

The driver attribution weighting rubric and the confidence scoring weighting rubric were declared and versioned rather than learned ([`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package)). Accumulated Realized Outcomes are the labeled data those rubrics are to be calibrated against eventually. They are also the data the competitor price-response model's historical-reaction estimate needs to be trained and validated against, not asserted. [`§ Open Questions [Name: Recalibration]`](#open-questions) holds how that recalibration works.

### Comparison eligibility

Resolve the observation state for each forecast without an existing outcome, using the check’s captured cutoff.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Original terms recoverable?, Single target window?, Window closed?, Comparable actuals available? \
**Computed:** Observation eligibility

| Original terms recoverable? | Single target window? | Window closed? | Comparable actuals available? | Observation eligibility |
|---|---|---|---|---|
| false | - | - | - | {state: "unevaluable", reason: "original comparison terms unavailable"} |
| true | false | - | - | {state: "unevaluable", reason: "original target window unresolved"} |
| true | true | false | - | {state: "pending period", reason: "target window still open"} |
| true | true | true | false | {state: "pending actuals", reason: "comparable observations incomplete"} |
| true | true | true | true | {state: "ready", reason: null} |

## Facts

**Records:**
  - **Name:** original terms recoverable? \
    **Type:** boolean \
    **Means:** whether the forecast’s original price, move, band, direction, threshold and price basis can be established from pinned evidence

  - **Name:** single target window? \
    **Type:** boolean \
    **Means:** whether the stored interval or the original vintage, horizon and measurement calendar identify exactly one target window

  - **Name:** window closed? \
    **Type:** boolean \
    **Means:** whether the exclusive end is at or before the captured check cutoff

  - **Name:** comparable actuals available? \
    **Type:** boolean \
    **Means:** whether an eligible vintage at the cutoff provides complete matching observations for the entire window

  - **Name:** forecast comparison \
    **Type:** context<start: number, move: number, lower: number, upper: number, direction: string, threshold: number> \
    **Means:** the original forecast’s starting effective price, predicted move, inclusive move bounds, predicted direction and original fractional stable-price threshold

  - **Name:** observation eligibility \
    **Type:** context<state: string, reason: string> \
    **Means:** the comparison disposition and its reason from the eligibility decision at the pinned cutoff

  - **Name:** observed price \
    **Type:** number \
    **May Be Absent:** Yes \
    **Means:** the comparable effective price for the whole target window from the selected actuals vintage; present whenever ready

  - **Name:** actual move \
    **Type:** number \
    **Means:** observed effective price minus the forecast’s starting price

  - **Name:** signed error \
    **Type:** number \
    **Means:** forecast move minus actual move

  - **Name:** actual direction \
    **Type:** string \
    **Values:** "stable", "increase", "decrease" \
    **Means:** realized direction under the original threshold

  - **Name:** existing comparison \
    **Type:** context<state: string, reason: string, move: number, error: number, verdict: string> \
    **May Be Absent:** Yes \
    **Means:** the immutable scored result already stored for this forecast ID, or null

  - **Name:** comparison result \
    **Type:** context<state: string, reason: string, move: number, error: number, verdict: string> \
    **Means:** the comparison disposition and numerical values where scored

## Open Questions

**Records:**

- **Name:** Recalibration
  **Open Question:** What trend in Realized Outcomes counts as drift worth acting on, and how are the driver attribution weighting rubric, the confidence scoring weighting rubric, and the competitor price-response model recalibrated against them, once enough Realized Outcomes have accumulated to judge?
  **Provisional Answer:** No trend is defined as drift, and nothing is recalibrated automatically: Acme AI judges the pattern a Platform admin sees across business units, and each rubric and model stays at the version the installation pins until a model release replaces it.
  **Impacts:** what accumulated Realized Outcomes are for, in [`§ Realized outcome check`](#realized-outcome-check); the competitor price-response model's training and validation, in [`specs/application/technical/predict-computation.md § Predict Computation § Driver Attribution`](/specs/application/technical/predict-computation.md#driver-attribution); the confidence scoring rubric's reason for being a declared formula, that there is no labeled history of real outcomes yet ([`specs/application/technical/predict-computation.md § Predict Computation § Confidence and rationale package`](/specs/application/technical/predict-computation.md#confidence-and-rationale-package)); a recalibrated model reaching a customer without an application upgrade ([`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations`](/specs/application/technical/engineering-and-production-considerations.md#engineering-and-production-considerations)); drift monitoring's watch on the trend in forecast_error ([`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)); and how the pattern a Platform admin sees reaches the platform ([`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy)).
