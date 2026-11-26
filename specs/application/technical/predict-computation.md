## Predict Computation

Predict computation is the mechanism that turns retrieved evidence into a forecast effective price, a driver-by-driver correction, and a confidence score. The materialization service and the query service both invoke this same computation. The materialization service invokes it in batch, across the configured grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)). The query service invokes it for an outside-grid query only when no live forecast matches the pinned key ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked)`](/specs/application/technical/query-service/intent-and-retrieval.md#dynamic-retrieval-and-weighting-when-the-question-is-asked)). The live path runs on the terms [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) sets for falling back to it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition), [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

### Signal route

Each Driver Signal feeds exactly one downstream consumer, which its event type decides. No signal feeds both, so no signal's effect on the forecast is counted twice. Each consumer reads a signal's magnitude signed by its direction, and a bracket at its midpoint. [`specs/application/technical/control-plane-service/control-plane.md § Control Plane § Configuration change path`](/specs/application/technical/control-plane-service/control-plane.md#configuration-change-path) decides who may change the routing rule. The complete membership is the closed set in the [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do § Event Type Taxonomy`](/specs/application/product/answer-engine/predict.md#event-type-taxonomy). This table applies the route: a signal stating a fact about the exact thing being forecast, the competitor's own list price or promotional depth, goes to Baseline; every other event type goes to Driver Attribution.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** States a fact about what is forecast? \
**Annotations:** Its Event Types

| States a fact about what is forecast? | routes_to | Its Event Types |
|---|---|---|
| true | Baseline, the baseline forecast Algorithm ([`§ Predict Computation § Baseline forecast`](#baseline-forecast)) | announced price change and promotional calendar change |
| false | Driver Attribution | product launch, capacity change, rate change, tax change, input cost change, and discretionary spending change |

### Baseline forecast

Forecast materialization in [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) computes the baseline across its configured grid. A live lookup miss runs the same baseline calculation. The baseline is an Algorithm. Both the scheduled cell and the live caller resolve rebate and surcharge separately from the same pinned commercial terms and dated observations. Each supplies the amount and evidence used for each adjustment. Steps 2 and 3 call the trend-and-seasonality baseline and the promotional depth cadence model, each a registered forecasting model documented in [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry), with its own declared confidence interval and last-validated date.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - component price observations
  - rebate at horizon
  - surcharge at horizon
  - forecast window
  - current effective price
  - signals routed here
  - dead-zone threshold

**Output:**
  - baseline forecast effective price
  - baseline move
  - baseline direction
  - baseline interval offsets

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)
  - [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)

| Step | Action |
|---|---|
| 1 | Set net commercial adjustment to surcharge at horizon - rebate at horizon |
| 2 | Set baseline list price to trend and seasonality forecast(component price observations, forecast window, signals routed here[item.event_type = "announced price change"]) |
| 3 | Set promotional depth to promotional depth cadence forecast(component price observations, forecast window, signals routed here[item.event_type = "promotional calendar change"]) |
| 4 | Set baseline forecast effective price to baseline list price.forecast list price - promotional depth.promotional depth + net commercial adjustment |
| 5 | Set baseline move to baseline forecast effective price - current effective price |
| 6 | Set baseline direction to if abs(baseline move) / current effective price < dead-zone threshold then "stable" else if baseline move > 0 then "increase" else "decrease" |
| 7 | Set baseline interval offsets to {lower bound offset: baseline list price.lower bound offset + promotional depth.upper bound offset, upper bound offset: baseline list price.upper bound offset + promotional depth.lower bound offset} |
| 8 | End |

A business unit's own dead-zone threshold is set as [`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings) describes. Promotion depth is a deduction. The low net endpoint pairs the low list price with the high deduction; the high endpoint pairs the high list price with the low deduction. Rebate and surcharge are fixed for this calculation. The offsets are already in the forecast geography's resolved currency and no conversion is needed before combining them. Summing offsets directly, rather than a statistical convolution, makes no assumption about either model's underlying distribution, which neither model's registry entry declares; it is a conservative bound on the combined uncertainty, not a precise calculation neither declared interval alone supports.

### Triangulation and conflict checks

The Driver Signal records ([`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)) retrieved alongside the baseline are read by their structured fields, not as raw text re-interpreted on the spot. Triangulation finds each retrieved Driver Signal that is routed to Driver Attribution and takes effect inside the horizon. These are the signals that could disagree with the baseline. Driver Attribution works out each signal's own effect on price. It flags as a conflict each signal that pushes price, by enough to count as a price move on its own ([`§ Predict Computation § Driver Attribution`](#driver-attribution)), in a direction the baseline does not show: the baseline is stable or moving the other way. The common case is a tax increase of that size, taking effect within the horizon against a stable baseline. A flagged conflict is surfaced, never averaged away. It is recorded with the baseline's direction and the disagreeing signal, and a Query user sees it on opening the confidence score ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). A smaller or agreeing signal still enters the forecast as its driver's contribution, shown in the decomposition graph.

### Driver Attribution

Driver Attribution is an Algorithm that computes the correction and sizes each signal triangulation found. It draws on every Driver Signal ([`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)) routed here rather than to the baseline.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - signals routed here
  - baseline
  - driver attribution weighting rubric
  - triangulated signals
  - current effective price
  - dead-zone threshold

**Output:**
  - forecast move
  - forecast direction
  - forecast magnitude
  - forecast band
  - driver contributions
  - flagged conflicts

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)
  - [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)

| Step | Action |
|---|---|
| 1 | For each signal of signals routed here, in any order, gathering sized signal into sized signals: steps 2 to 3 |
| 2 | Set signed effect to if signal.driver_category = "competitor plans" then competitor price response(signal) else signal.reported magnitudes[1] * signal.currency factors[1] |
| 3 | Set sized signal to {signal: signal, effect: signed effect, contribution: signed effect * driver weight(driver attribution weighting rubric, signal.driver_category)} |
| 4 | For each driver of ["elasticity", "input costs", "discretionary spending", "competitor plans", "tax"], in any order, gathering driver contribution into driver contributions: steps 5 to 6 |
| 5 | Set magnitude to if driver = "elasticity" then elasticity estimate(current effective price) else if count(sized signals[item.signal.driver_category = driver]) = 0 then 0 else sum(for sized in sized signals[item.signal.driver_category = driver] return sized.effect) |
| 6 | Set driver contribution to {contribution: magnitude * driver weight(driver attribution weighting rubric, driver), magnitude: magnitude, driver: driver} |
| 7 | Set total correction to sum(for contribution in driver contributions return contribution.contribution) |
| 8 | Set forecast move to baseline.move + total correction |
| 9 | Set forecast direction to if abs(forecast move) / current effective price < dead-zone threshold then "stable" else if forecast move > 0 then "increase" else "decrease" |
| 10 | Set forecast magnitude to abs(forecast move) |
| 11 | Set forecast band to {lower: forecast move - baseline.interval offsets.lower bound offset, upper: forecast move + baseline.interval offsets.upper bound offset} |
| 12 | Set flagged conflicts to for sized in sized signals[list contains(triangulated signals, item.signal) and item.contribution != 0 and abs(item.contribution) / current effective price >= dead-zone threshold and (if item.contribution > 0 then "increase" else "decrease") != baseline.direction] return {baseline direction: baseline.direction, signal: sized.signal, contribution: sized.contribution} |
| 13 | End |

Direct effects enter the correction in resolved currency per unit. Retain the source range, its unit and the pinned evidence for the conversion basis with each signal reference. Take the signed midpoint before conversion. For an amount already in resolved currency per unit the conversion factor is 1. For a percentage-point change the factor is the applicable documented monetary base per unit divided by 100. Convert foreign monetary amounts at the pinned reconciliation rate. Other units require a documented conversion into price per unit. A direct signal without an applicable basis remains in the existing review queue. The response model sizes an eligible competitor-plan trigger directly in resolved currency per unit. Driver weights are dimensionless and apply once to monetary effects.

The decomposition shows the baseline move and each driver's weighted contribution. Together they sum to the published forecast move. A conflict records the same signed contribution that its signal made to the correction, so surfacing it preserves that accounting. The weighting rubric version identifies the weights used.

Elasticity's magnitude always comes from the named model alone. No document ever backs it. Competitor plans is different. The competitor price-response model estimates how this competitor has historically reacted to comparable triggers, trained and validated against [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome check`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-check) rather than asserted. Its recalibration is [`specs/application/technical/materialization-service/forecast-materialization.md § Open Questions [Name: Recalibration]`](/specs/application/technical/materialization-service/forecast-materialization.md#open-questions)'s subject. The model only translates a Driver Signal's trigger into a magnitude, and does not estimate one without a signal to translate. Whenever competitor plans contributes anything, the signal and the model back it together. When no signal exists for competitor plans in this query, neither backs it, and it contributes zero. For a given driver, driver_evidence ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)) records a signal, a model, both together, or neither. The evidence a Query user sees for a driver ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)) is therefore the same source the computation used, never a description assembled after the fact.

### Confidence and rationale package

Rationale here means a Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), the structured fields it defines rather than prose. With those fields, the answer can show how the number was built and why its confidence sits where it does. Nothing reaches the output layer unaccompanied by this record. confidence_score is a declared, versioned formula rather than a learned model, by the same reasoning as the driver attribution weighting rubric. There is no labeled history of real outcomes yet to train a calibrated model against ([`specs/application/technical/materialization-service/forecast-materialization.md § Open Questions [Name: Recalibration]`](/specs/application/technical/materialization-service/forecast-materialization.md#open-questions)). A declared formula is also explainable to a customer questioning a number, in a way a trained model is not. An Algorithm computes confidence_score.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - Driver Signals used in this answer
  - snapshot age
  - Rationale Record's conflicts
  - confidence scoring weighting rubric

**Output:**
  - confidence score
  - source credibility score
  - data freshness score
  - triangulation agreement score
  - confidence component weights

**Runs When:**
  - [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Orchestration § Question run`](/specs/application/technical/engineering-and-production-considerations.md#question-run)
  - [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)

| Step | Action |
|---|---|
| 1 | Set source credibility score to if count(Driver Signals used in this answer) = 0 then null else source credibility(Driver Signals used in this answer) |
| 2 | Set data freshness score to if count(Driver Signals used in this answer) = 0 then data freshness(snapshot age) else min(data freshness(snapshot age), data freshness signals(Driver Signals used in this answer)) |
| 3 | Set triangulation agreement score to if count(Driver Signals used in this answer) = 0 then null else triangulation agreement(Rationale Record's conflicts) |
| 4 | Set confidence component weights to if count(Driver Signals used in this answer) = 0 then {source credibility: 0, data freshness: 1, triangulation agreement: 0} else {source credibility: confidence scoring weighting rubric.source credibility, data freshness: confidence scoring weighting rubric.data freshness, triangulation agreement: confidence scoring weighting rubric.triangulation agreement} |
| 5 | Set confidence score to if count(Driver Signals used in this answer) = 0 then data freshness score else source credibility score * confidence component weights.source credibility + data freshness score * confidence component weights.data freshness + triangulation agreement score * confidence component weights.triangulation agreement |
| 6 | Set confidence score to if count(Rationale Record's conflicts) > 0 then min(confidence score, confidence scoring weighting rubric.flagged conflict ceiling) else confidence score |
| 7 | End |

Predict excludes model validation dates from its score under the provisional Model Freshness in Predict decision ([`specs/application/technical/model-registry.md § Open Questions [Name: Model Freshness in Predict]`](/specs/application/technical/model-registry.md#open-questions)). The baseline evidence retains those dates.

For a query inside the materialized grid, the whole record is retrieved as materialized rather than recomputed. This packaging step runs live only for a query that falls outside the grid. When it does, the resulting Effective Price Forecast ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)) is persisted the same way as a materialization run's own output, with computed_via live rather than batch. It is not returned and discarded. Everything that reads the grid sees it afterward, [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome check`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-check) and [`specs/application/technical/query-service/evidence-and-accuracy-reporting.md § Bulk Evidence and Accuracy Report`](/specs/application/technical/query-service/evidence-and-accuracy-reporting.md#bulk-evidence-and-accuracy-report) alike. This is the mechanism behind [`specs/application/product/platform-and-compliance-operations/onboarding-verification.md § Onboarding Verification`](/specs/application/product/platform-and-compliance-operations/onboarding-verification.md#onboarding-verification) and [`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy) both seeing real, question-triggered activity rather than only the grid. Rendering a sentence for the user is a separate, later step ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`](/specs/application/technical/query-service/layered-output-synthesis.md#layered-output-synthesis-producing-the-answer)). This record is the fact base rendering draws from, not the sentence itself.

#### A flagged conflict's ceiling

A Constraint on the packaging Algorithm's output:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| count(Rationale Record's conflicts) = 0 or confidence score <= confidence scoring weighting rubric.flagged conflict ceiling | after [`§ Predict Computation § Confidence and rationale package`](#confidence-and-rationale-package) | [`§ Predict Computation § Confidence and rationale package [Step: 6]`](#confidence-and-rationale-package) |

Because step 6 enforces the Constraint, the other, unrelated inputs that happen to look good can never outvote a real, surfaced disagreement. The same discipline already keeps triangulation from averaging a conflict away silently ([`specs/application/technical/predict-computation.md § Predict Computation § Triangulation and conflict checks`](/specs/application/technical/predict-computation.md#triangulation-and-conflict-checks)).

## Facts

**Records:**
  - **Name:** States a fact about what is forecast? \
    **Type:** boolean \
    **Means:** whether the event states a fact about the competitor's own list price or promotional depth rather than requiring inference about how the event translates into a price effect

  - **Name:** forecast window \
    **Type:** context<start date: date, end date: date> \
    **Means:** the time window from the scheduled grid key or resolved question at the pinned data vintage

  - **Name:** component price observations \
    **Type:** list<context<effective date: date, list price: number, promotional depth: number, rebate: number, surcharge: number, currency: string>> \
    **Means:** separately observed per-unit amounts on the same dates and currency, pinned to the data vintage; equal historical net prices need not have equal components

  - **Name:** rebate at horizon \
    **Type:** number \
    **Means:** the rebate per unit in the period from terms known at the data vintage, carrying forward the latest observed per-unit rebate where a future term is unspecified

  - **Name:** surcharge at horizon \
    **Type:** number \
    **Means:** the surcharge per unit in the period from terms known at the data vintage, carrying forward the latest observed per-unit surcharge where a future term is unspecified

  - **Name:** net commercial adjustment \
    **Type:** number \
    **Means:** surcharge less rebate per unit for the target period

  - **Name:** current effective price \
    **Type:** number \
    **Means:** the competitor's current effective price in the forecast geography's resolved currency

  - **Name:** signals routed here \
    **Type:** list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>> \
    **Means:** the routed Driver Signals, each retaining its durable record reference in the business unit namespace and source_citation pointing to the supporting chunk. Sizing and conflict records carry that same signal. Entity type and code identify the subject. For a direct effect the singleton currency factors list stores resolved currency per unit per reported unit; a model-sized trigger needs no conversion factor. A stated magnitude is a singleton list containing its signed value, including [0]. A qualifying competitor-plan trigger with no magnitude has an empty list. Only the model-sized route admits that absence. Other unsized events remain in review.

  - **Name:** dead-zone threshold \
    **Type:** number \
    **Unit:** ratio \
    **Means:** the business unit's dead-zone threshold as a share of current effective price

  - **Name:** baseline list price \
    **Type:** context<forecast list price: number, lower bound offset: number, upper bound offset: number> \
    **Means:** the trend-and-seasonality baseline model's forecast list price and declared offsets

  - **Name:** promotional depth \
    **Type:** context<promotional depth: number, lower bound offset: number, upper bound offset: number> \
    **Means:** the promotional-depth cadence model's forecast depth and declared offsets

  - **Name:** trend and seasonality forecast \
    **Type:** function<list<context<effective date: date, list price: number, promotional depth: number, rebate: number, surcharge: number, currency: string>>, context<start date: date, end date: date>, list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>>> -> context<forecast list price: number, lower bound offset: number, upper bound offset: number> \
    **Means:** the trend-and-seasonality baseline model's forecast and declared offsets

  - **Name:** promotional depth cadence forecast \
    **Type:** function<list<context<effective date: date, list price: number, promotional depth: number, rebate: number, surcharge: number, currency: string>>, context<start date: date, end date: date>, list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>>> -> context<promotional depth: number, lower bound offset: number, upper bound offset: number> \
    **Means:** the promotional-depth cadence model's forecast and declared offsets

  - **Name:** baseline forecast effective price \
    **Type:** number \
    **Means:** the baseline's forecast effective price at the horizon

  - **Name:** baseline move \
    **Type:** number \
    **Means:** the baseline forecast effective price less current effective price

  - **Name:** baseline direction \
    **Type:** string \
    **Values:** "increase", "decrease", "stable" \
    **Means:** the direction of the baseline move under the dead-zone test

  - **Name:** baseline interval offsets \
    **Type:** context<lower bound offset: number, upper bound offset: number> \
    **Means:** the independently summed lower and upper offsets from the two forecasting models

  - **Name:** baseline \
    **Type:** context<move: number, direction: string, interval offsets: context<lower bound offset: number, upper bound offset: number>> \
    **Means:** the completed baseline passed to Driver Attribution

  - **Name:** driver attribution weighting rubric \
    **Type:** context<version: string, entries: list<context<driver: string, weight: number>>> \
    **Means:** the pinned attribution version and exactly one numeric weight for each of the five named drivers

  - **Name:** driver weight \
    **Type:** function<context<version: string, entries: list<context<driver: string, weight: number>>>, string> -> number \
    **Derivation:** function(rubric, driver name) rubric.entries[item.driver = driver name][1].weight \
    **Means:** the unique weight for the given driver in the supplied attribution rubric

  - **Name:** elasticity estimate \
    **Type:** function<number> -> number \
    **Means:** the elasticity model's estimate for the current effective price

  - **Name:** competitor price response \
    **Type:** function<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>> -> number \
    **Means:** the model's signed price effect for one competitor-plan event, including an event with no stated magnitude

  - **Name:** signed effect \
    **Type:** number \
    **Means:** the single signal's signed price effect before weighting

  - **Name:** sized signal \
    **Type:** context<signal: context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>, effect: number, contribution: number> \
    **Means:** one routed signal with its signed effect and weighted contribution

  - **Name:** sized signals \
    **Type:** list<context<signal: context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>, effect: number, contribution: number>> \
    **Means:** the effects and contributions gathered for this forecast

  - **Name:** magnitude \
    **Type:** number \
    **Means:** the magnitude retrieved or estimated for the current driver

  - **Name:** driver contribution \
    **Type:** context<driver: string, magnitude: number, contribution: number> \
    **Means:** the current driver, its magnitude, and its magnitude times its rubric weight

  - **Name:** driver contributions \
    **Type:** list<context<driver: string, magnitude: number, contribution: number>> \
    **Initial Value:** [] \
    **Means:** each driver's magnitude and weighted contribution

  - **Name:** total correction \
    **Type:** number \
    **Means:** the sum of all driver contributions

  - **Name:** forecast move \
    **Type:** number \
    **Means:** the baseline move plus the total correction

  - **Name:** forecast direction \
    **Type:** string \
    **Values:** "increase", "decrease", "stable" \
    **Means:** the direction of the completed forecast under the dead-zone test

  - **Name:** forecast magnitude \
    **Type:** number \
    **Means:** the absolute size of the forecast move

  - **Name:** forecast band \
    **Type:** context<lower: number, upper: number> \
    **Means:** the completed forecast's baseline interval offsets placed around its move

  - **Name:** triangulated signals \
    **Type:** list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>> \
    **Means:** the signals selected by triangulation for conflict checking

  - **Name:** flagged conflicts \
    **Type:** list<context<baseline direction: string, signal: context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>, contribution: number>> \
    **Initial Value:** [] \
    **Means:** each conflict recorded with the baseline's direction, the disagreeing signal, and its contribution

  - **Name:** Driver Signals used in this answer \
    **Type:** list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>> \
    **Means:** every Driver Signal whose evidence contributes to the answer

  - **Name:** snapshot age \
    **Type:** days and time duration \
    **Means:** the age of the data-as-of snapshot used by this answer

  - **Name:** Rationale Record's conflicts \
    **Type:** list<context<baseline direction: string, signal: context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>, contribution: number>> \
    **Means:** the conflicts already recorded in the Rationale Record

  - **Name:** confidence scoring weighting rubric \
    **Type:** context<source credibility: number, data freshness: number, triangulation agreement: number, flagged conflict ceiling: number> \
    **Means:** the versioned rubric that weights the confidence components and sets the flagged-conflict ceiling

  - **Name:** source credibility \
    **Type:** function<list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>>> -> number \
    **Means:** the rubric's score for the lowest credibility tier among a set of Driver Signals

  - **Name:** data freshness \
    **Type:** function<days and time duration> -> number \
    **Means:** the rubric's score for a snapshot's age

  - **Name:** data freshness signals \
    **Type:** function<list<context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>>> -> number \
    **Means:** the rubric's score for the contributing Driver Signals' effective dates

  - **Name:** triangulation agreement \
    **Type:** function<list<context<baseline direction: string, signal: context<signal reference: string, source_citation: string, entity type: string, entity code: string, reported unit: string, currency factors: list<number>, driver_category: string, event_type: string, direction: string, reported magnitudes: list<number>, effective_date: date, source_type: string, extraction_model_version: string, credibility_tier: string>, contribution: number>>> -> number \
    **Means:** the rubric's full score when no conflict is present and its reduced score when one is present

  - **Name:** source credibility score \
    **Type:** number \
    **May Be Absent:** Yes \
    **Means:** the rubric score for the weakest contributing source, absent when no Driver Signal contributed

  - **Name:** data freshness score \
    **Type:** number \
    **Means:** the score for data freshness under the rubric's declared staleness bands

  - **Name:** triangulation agreement score \
    **Type:** number \
    **May Be Absent:** Yes \
    **Means:** the agreement score for a forecast using Driver Signals, absent when none contributed

  - **Name:** confidence component weights \
    **Type:** context<source credibility: number, data freshness: number, triangulation agreement: number> \
    **Means:** the effective weights applied to this forecast under the confidence calculation

  - **Name:** confidence score \
    **Type:** number \
    **Means:** the completed confidence score
