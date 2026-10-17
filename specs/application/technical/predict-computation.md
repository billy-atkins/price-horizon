## Predict Computation

Predict computation is the mechanism that turns retrieved evidence into a forecast effective price, a driver-by-driver correction, and a confidence score. The materialization service and the query service both invoke this same computation. The materialization service invokes it in batch, across the configured grid ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)). The query service invokes it live, for a query falling outside that grid ([`specs/application/technical/query-service/intent-and-retrieval.md § Dynamic Retrieval and Weighting (when the question is asked)`](/specs/application/technical/query-service/intent-and-retrieval.md#dynamic-retrieval-and-weighting-when-the-question-is-asked)). The live path runs on the terms [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) sets for falling back to it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition), [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

### Signal routing

Each Driver Signal feeds exactly one downstream consumer, which its event type decides. No signal feeds both, so no signal's effect on the forecast is counted twice. Each consumer reads a signal's magnitude signed by its direction, and a bracket at its midpoint. [`specs/application/technical/control-plane-service/control-plane.md § Control Plane`](/specs/application/technical/control-plane-service/control-plane.md#control-plane) decides who may change the routing rule. The rule that decides `routes_to` for every event type is a Decision Table, and there is no other case. The table asks whether the event type states a fact about the exact thing being forecast, the competitor's own list price or promotional depth, or requires inference about how the event translates into a price effect:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** States a fact about what is forecast?

**Annotations:** Its Event Types

| States a fact about what is forecast? | routes_to | Its Event Types |
|---|---|---|
| Yes | Baseline, the effective price forecasting Algorithm ([`§ Predict Computation § Effective price forecasting`](#effective-price-forecasting)) | competitor plans' announced price change and promotional calendar change |
| No | Driver Attribution | every other event type, across every driver category: competitor plans' own product launch and capacity change, every tax event type, and every input cost and discretionary spending event type |

Event types are a bounded, governed set, under the same discipline as the driver categories and source types ([`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)). They are declared as a versioned Event Type Taxonomy ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Signal Routing Rule`](/specs/application/technical/data-model.md#signal-routing-rule)), not left implicit in application logic. Both consumers therefore read a declared field, and the mapping is not written as conditional logic somewhere in the codebase. The routing stays inspectable by reading the taxonomy, not only by reading source. The taxonomy also lets [`specs/application/technical/evaluation-and-monitoring.md § Evaluation and monitoring`](/specs/application/technical/evaluation-and-monitoring.md#evaluation-and-monitoring)'s golden-question harness assert directly that every event type has exactly one declared consumer. Adding a new event type is a deliberate, versioned change to that table. The change sets the event type's driver category and its routing together, in one governed artifact. It is not a runtime classification decision, and it is not a set of separate changes that can drift apart.

### Effective price forecasting

Forecast materialization in [`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization) computes the baseline across its configured grid. This computation computes it live when a query falls outside that grid. The baseline is an Algorithm. Its step 2 calls the trend-and-seasonality baseline, and its step 3 calls the promotional depth cadence model. Each is a registered forecasting model, documented in [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry) the same way every other model is, with its own declared confidence interval and last-validated date.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:** the competitor's historical effective price series and current effective price, the signals routed here, and the business unit's dead-zone threshold

**Output:** the baseline: its forecast effective price, its move and direction, and its lower- and upper-bound offsets

| Step | Action |
|---|---|
| 1 | Decompose the competitor's historical effective price series into its list price and promotional depth components |
| 2 | Forecast list price on a trend-and-seasonality baseline, adjusted for any signal routed here with event type announced price change |
| 3 | Forecast promotional depth on a cadence model calibrated to the competitor's own historical promotional calendar, adjusted for any signal routed here with event type promotional calendar change |
| 4 | Recombine both forecasts into a forecast effective price at the horizon, the baseline's, whose move and direction steps 5 and 6 set |
| 5 | Compute the baseline move as step 4's forecast effective price minus current effective price |
| 6 | If the size of the baseline move, as a share of current effective price, falls under the dead-zone threshold, roughly half a percent, set the baseline's direction to stable; otherwise, set it to the sign of the baseline move |
| 7 | Combine both models' own declared confidence intervals into the baseline's lower- and upper-bound offsets: sum both models' own lower-bound offsets from their respective point estimates to get the baseline's lower-bound offset, and separately sum their own upper-bound offsets to get the upper-bound offset, computed independently on each side so an asymmetric model interval, a wider upside than downside, carries through correctly rather than being averaged into a symmetric one. Both offsets are already in the same resolved currency step 1 decomposed them from, list price and promotional depth are components of one currency-denominated effective price series, so no conversion is needed before combining them. Summing offsets directly, rather than a statistical convolution, makes no assumption about either model's own underlying distribution, something neither model's registry entry declares; it is a defensible, if conservative, upper bound on the combined uncertainty, not a precise calculation neither declared interval alone actually supports. End |

A business unit's own dead-zone threshold is set as [`specs/application/product/tenant-administration/business-unit-settings.md § Business Unit Settings`](/specs/application/product/tenant-administration/business-unit-settings.md#business-unit-settings) describes.

### Triangulation and conflict checks

The Driver Signal records ([`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)) retrieved alongside the baseline are read by their structured fields, not as raw text re-interpreted on the spot. Triangulation finds each retrieved Driver Signal that is routed to Driver Attribution and takes effect inside the horizon. These are the signals that could disagree with the baseline. Driver Attribution works out each signal's own effect on price. It flags as a conflict each signal that pushes price, by enough to count as a price move on its own ([`§ Predict Computation § Driver Attribution`](#driver-attribution)), in a direction the baseline does not show: the baseline is stable or moving the other way. The common case is a tax increase of that size, taking effect within the horizon against a stable baseline. A flagged conflict is surfaced, never averaged away. It is recorded with the baseline's direction and the disagreeing signal, and a Query user sees it on opening the confidence score ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). A smaller or agreeing signal still enters the forecast as its driver's contribution, shown in the decomposition graph.

### Driver Attribution

Driver Attribution is an Algorithm that computes the correction and sizes each signal triangulation found. It draws on every Driver Signal ([`specs/application/technical/data-model.md § Core Data Model § Vector Database Schema § Driver Signal`](/specs/application/technical/data-model.md#driver-signal)) routed here rather than to the baseline.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:** the Driver Signals routed here, the baseline ([`§ Predict Computation § Effective price forecasting`](#effective-price-forecasting)), the driver attribution weighting rubric, the named models, and the signals triangulation found ([`§ Predict Computation § Triangulation and conflict checks`](#triangulation-and-conflict-checks))

**Output:** the forecast's move, direction, magnitude and band, each driver's contribution, and each flagged conflict

| Step | Action |
|---|---|
| 1 | Take the next named driver: the competitor's own elasticity (how sensitive their category demand is to a price move, and so how much they stand to lose by moving it, distinct from Brand A's elasticity used later in Position), input costs, a discretionary spending index, competitor plans (drawing on both the Driver Signals extracted by [`specs/application/technical/materialization-service/driver-signal-extraction.md § Vector and semantic mapping, with structured extraction`](/specs/application/technical/materialization-service/driver-signal-extraction.md#vector-and-semantic-mapping-with-structured-extraction) and the competitor price-response model in the registry, an estimate of how this competitor has historically reacted to comparable triggers, trained and validated against [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-tracking), not asserted; how it is recalibrated is [`specs/application/technical/materialization-service/forecast-materialization.md § Open Questions [Name: Recalibration]`](/specs/application/technical/materialization-service/forecast-materialization.md#open-questions)), and tax changes |
| 2 | Retrieve that driver's magnitude for this query, from the routed Driver Signals, or from the named model where the driver is elasticity or competitor plans; a driver other than elasticity with no routed signal for this query has a magnitude of zero rather than being skipped, so every driver is always accounted for |
| 3 | Look up that driver's weight in the driver attribution weighting rubric |
| 4 | Multiply the magnitude by the weight to get that driver's contribution |
| 5 | If a named driver is left, Go to step 1; otherwise, continue |
| 6 | Sum the contributions to get the total correction |
| 7 | Add the correction to the baseline move from [`§ Predict Computation § Effective price forecasting [Step: 5]`](#effective-price-forecasting) to get the forecast's move |
| 8 | Set the forecast's direction from its move by the dead-zone test of [`§ Predict Computation § Effective price forecasting [Step: 6]`](#effective-price-forecasting), and its magnitude as the size of that move |
| 9 | Place the offsets [`§ Predict Computation § Effective price forecasting [Step: 7]`](#effective-price-forecasting) combines around the forecast's move; the band carries the forecasting models' declared uncertainty, and a driver model's own interval is not added to it |
| 10 | If triangulation found no signal to check, End; otherwise, continue |
| 11 | Take the next signal triangulation found |
| 12 | Compute that signal's own contribution: the price effect this step derives from it alone, its magnitude, read as [`§ Predict Computation § Signal routing`](#signal-routing) states, or for competitor plans the price-response model's translation of it, times its driver's weight from step 3; its sign is the direction it pushes price |
| 13 | If that direction is not one the baseline shows, and the contribution would count as a move by the dead-zone test of [`§ Predict Computation § Effective price forecasting [Step: 6]`](#effective-price-forecasting), record the signal and its contribution as a flagged conflict, which packaging carries into the Rationale Record's conflicts; otherwise, continue |
| 14 | If a signal triangulation found is left, Go to step 11; otherwise, End |

An unflagged signal's contribution is already part of step 4's. Each driver's contribution from step 4 is part of the correction applied in step 7. It is also the exact value rendered as that driver's slice of the decomposition graph. The graph is therefore a true accounting of how the number was built, not a plausible story assembled after the fact. The forecast's move is exactly the baseline move plus the drivers' contributions, and the decomposition graph shows every term of that sum. That is the accounting [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) promises. The weighting rubric is versioned, so the same inputs against the same rubric version always produce the same breakdown.

Elasticity's magnitude always comes from the named model alone. No document ever backs it. Competitor plans is different. The model only translates a Driver Signal's trigger into a magnitude, and does not estimate one without a signal to translate. Whenever competitor plans contributes anything, the signal and the model back it together. When no signal exists for competitor plans in this query, neither backs it, and it contributes zero. For a given driver, driver_evidence ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)) records a signal, a model, both together, or neither. Step 2 and this section's account of elasticity and competitor plans already determine which. The evidence a Query user sees for a driver ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)) is therefore the same source the computation used, never a description assembled after the fact.

### Confidence and rationale packaging

Rationale here means a Rationale Record ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Rationale Record`](/specs/application/technical/data-model.md#rationale-record)), the structured fields it defines rather than prose. With those fields, the answer can show how the number was built and why its confidence sits where it does. Nothing reaches the output layer unaccompanied by this record. confidence_score is a declared, versioned formula rather than a learned model, by the same reasoning as the driver attribution weighting rubric. There is no labeled history of real outcomes yet to train a calibrated model against ([`specs/application/technical/materialization-service/forecast-materialization.md § Open Questions [Name: Recalibration]`](/specs/application/technical/materialization-service/forecast-materialization.md#open-questions)). A declared formula is also explainable to a customer questioning a number, in a way a trained model is not. An Algorithm computes confidence_score.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:** the Driver Signals used in this answer, the data-as-of snapshot's age, the Rationale Record's conflicts, and the confidence scoring weighting rubric

**Output:** confidence_score

| Step | Action |
|---|---|
| 1 | Score source credibility as the lowest credibility_tier among the Driver Signals used in this answer, not an average, so one poorly-sourced signal is never diluted by better ones |
| 2 | Score data freshness against the confidence scoring weighting rubric's declared staleness bands, using the data-as-of snapshot's age and, where a Driver Signal contributed, its own effective_date |
| 3 | If the Rationale Record's conflicts is empty, score triangulation agreement at its full value; otherwise, score it at the rubric's declared reduced value |
| 4 | Look up each score's weight in the confidence scoring weighting rubric |
| 5 | Multiply each score by its weight and sum them to get confidence_score |
| 6 | If conflicts holds a flagged conflict, cap confidence_score at the rubric's declared ceiling for a flagged conflict, regardless of what step 5 produced; otherwise, continue |
| 7 | Return confidence_score. End |

For a query inside the materialized grid, the whole record is retrieved as materialized rather than recomputed. This packaging step runs live only for a query that falls outside the grid. When it does, the resulting Effective Price Forecast ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Effective Price Forecast`](/specs/application/technical/data-model.md#effective-price-forecast)) is persisted the same way as a materialization run's own output, with computed_via live rather than batch. It is not returned and discarded. Everything that reads the grid sees it afterward, [`specs/application/technical/materialization-service/forecast-materialization.md § Realized outcome tracking`](/specs/application/technical/materialization-service/forecast-materialization.md#realized-outcome-tracking) and [`specs/application/technical/query-service/evidence-and-accuracy-reporting.md § Bulk Evidence and Accuracy Report`](/specs/application/technical/query-service/evidence-and-accuracy-reporting.md#bulk-evidence-and-accuracy-report) alike. This is the mechanism behind [`specs/application/product/platform-and-compliance-operations/onboarding-verification.md § Onboarding Verification`](/specs/application/product/platform-and-compliance-operations/onboarding-verification.md#onboarding-verification) and [`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy) both seeing real, question-triggered activity rather than only the grid. Rendering a sentence for the user is a separate, later step ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer)`](/specs/application/technical/query-service/layered-output-synthesis.md#layered-output-synthesis-producing-the-answer)). This record is the fact base rendering draws from, not the sentence itself.

#### A flagged conflict's ceiling

A Constraint on the packaging Algorithm's output:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| A forecast with a flagged conflict is never assigned a confidence_score above the rubric's flagged-conflict ceiling, however strong source credibility or data freshness are on their own | confidence_score | [`§ Predict Computation § Confidence and rationale packaging [Step: 6]`](#confidence-and-rationale-packaging) |

Because step 6 enforces the Constraint, the other, unrelated inputs that happen to look good can never outvote a real, surfaced disagreement. The same discipline already keeps triangulation from averaging a conflict away silently ([`§ Predict Computation § Triangulation and conflict checks`](#triangulation-and-conflict-checks)).
