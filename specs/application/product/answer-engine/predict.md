---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/glossary-and-grounding.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/model-registry.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Predict: what will the competitor do

Effective price is the net price realized per unit over the period asked about: list price minus trade promotions and rebates, plus any surcharges. It is neither the list price nor the shelf price. A competitor's effective price can therefore move significantly from one month to the next while its sticker price stays the same, because a bigger promotion moved it. Predict forecasts this number.

The forecast gives the direction and size of the competitor's likely move in effective price. It is built from a baseline and a set of corrections, and the answer keeps both visible, as [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) requires. The baseline is the move the competitor's own price trend and usual promotional calendar point to by the horizon, adjusted for any price change or promotion the competitor has already announced. Each driver in the decomposition graph then adds a correction, sized by the evidence behind it and by the driver's weight in a versioned weighting rubric. The forecast is exactly the baseline plus those corrections. The decomposition graph shows each one, so the chart accounts for how the number was built instead of explaining it afterward. The baseline opens to what it was built from: the price history as of when it was taken, the forecasting models that carried it forward and when each was last validated, and any announcement that adjusted it.

Most of that evidence exists before anyone asks. As documents arrive, the system reads the facts in them that bear on price, such as a tax change or a competitor's stated plan. It tags each fact with how credible its type of source is, and records it. A regulator's filing ranks above licensed third-party commentary, and both rank above an internal analyst note. A fact is used only once it is complete enough to size: when it takes effect, which way it pushes, and by how much. For a competitor's product launch or capacity change, it needs only enough for the model of the competitor's past reactions to judge. A stated range is used at its midpoint and shown as the range. [`specs/application/product/tenant-administration/review-queues.md § Review Queues`](/specs/application/product/tenant-administration/review-queues.md#review-queues) covers a fact that is not complete enough.

The forecast, with its breakdown and its confidence, is computed on a schedule for each tracked competitor brand and geography in a business unit, at 1, 3, 6 and 12 months. A question inside that set retrieves a forecast already built. For a supported live request, such as a nine-month horizon at a grounded market for a tracked brand, the system reuses the matching forecast or builds it on a miss. Below the grid, it shows a grounded parent reference or a supported estimate. An untracked brand, unsupported request or unit awaiting publication receives an explanation of unavailability. Either way, what is done with the forecast is computed when the question is asked: the positioning options, their simulated outcomes and the plain-language account.

The confidence band is a range around the forecast. Its width comes from the uncertainty each of the underlying list-price and promotional-depth models carries. The confidence score is a separate reading of the evidence behind the forecast. It weighs how credible the weakest source is, since better sources never average away one poorly sourced fact. It also weighs how current the data is, and whether the evidence agrees with itself. If no qualitative signal contributes, snapshot freshness alone sets the score. The explanation identifies source credibility and agreement as inapplicable.

The two can diverge. A forecast can sit inside a narrow band and still carry a lower confidence score, when the models are precise but a driver rests on a weakly sourced or stale fact. That is not a contradiction. Each answers a different question about the same forecast, and the answer shows both without flagging either as an error. The confidence score opens to each of its reasons, as [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) requires. Here each reason opens to its evidence: the weakest source itself, how old the data is and when each fact took effect, and any disagreement big enough to count as a price move. When a document points to a change big enough to count as a price move on its own, in a direction the baseline does not show, the answer names both sides and shows that the disagreement is holding the score down.

**Reference Key:** Layer \
**Required:** What It Shows

| Layer | What It Shows |
|---|---|
| Scorecard / heatmap | Competitor Brand's probabilistic price forecast, with a confidence band around it and a confidence score beside it, and Brand A's current price shown as a reference point, not yet a computed comparison |
| Plain-language narrative | The expected impact and its KPI implications in business language, with the rationale behind the forecast, not just a score |
| Geographic visualization | A map from country to state or province to major metro, matching how the competitor's own pricing data is reported, showing how the top-line figure breaks down by region |
| Decomposition graph | The baseline and a chart of the underlying drivers (the competitor's own demand sensitivity, input cost, competitor strategy, consumer spending trends, and tax), with how much each contributes to the forecast |

Predict shows the current and forecast effective price per unit in the local currency of the forecast geography. A Query user viewing another market sees that market’s currency.

A Query user can open each driver in the decomposition graph, and each qualitative fact the narrative names, to see the evidence behind it without leaving the analysis. Most show the qualitative document behind them: its source type, what it states, how credible that kind of source is, and when it took effect. Demand sensitivity has no document behind it, because it is estimated, not reported. Opening it shows the model that produced the estimate and when that model was last validated. Competitor strategy shows both the document and the model that turned it into a magnitude, when a qualifying competitor plan contributes. A zero contribution opens to its cause. If no qualifying signal reached a signal-driven driver, the view says so. If effects cancel, the view shows each signed effect and its source. A measured or modeled zero retains its evidence. It never shows an empty or broken view. Here the sourcing guarantee ([`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)) becomes visible to a Query user instead of only being asserted. The answer's own lineage ([`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`](/specs/application/product/logging-and-traceability.md#answer-lineage)) refers to this same evidence view.

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer) and [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) render this.

### Event Type Taxonomy

The governed event types form a closed set. Every event type is declared here exactly once, with its driver category and its single downstream consumer. An event outside this set is sent to the review queue rather than being classified at runtime.

**Table Name:** Event Type Taxonomy \
**Reference Key:** Event Type \
**Required:** Driver Category, Route

| Event Type | Driver Category | Route |
|---|---|---|
| announced price change | competitor plans | Baseline |
| promotional calendar change | competitor plans | Baseline |
| product launch | competitor plans | Driver Attribution |
| capacity change | competitor plans | Driver Attribution |
| rate change | tax | Driver Attribution |
| tax change | tax | Driver Attribution |
| input cost change | input costs | Driver Attribution |
| discretionary spending change | discretionary spending | Driver Attribution |

### Test Scenarios

```gherkin
Scenario: A sized competitor plan outside the governed event types awaits review.
  Given the unit’s Control plane admin has a competitor filing that announces a distribution contract change with a stated price effect of USD 0.20 per unit
  And the evidence identifies the competitor, geography and effective date, but the plan fits none of the accepted competitor-plan event types
  When a Control plane admin opens the unit’s review queue
  Then the event is awaiting review and contributes nothing to the forecast

Scenario: A resolvable question returns a confidence-scored forecast.
  Given a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  When the question is answered
  Then the answer includes a forecast direction and magnitude for Competitor Brand's effective price, a confidence score, and a plain-language rationale stating what is driving the forecast
  And the answer includes a confidence band around the forecast
  And the answer includes a geographic breakdown of that forecast, down to the granularity the competitor's own pricing data supports
  And the answer includes a decomposition of the named drivers behind the forecast

Scenario: A confidence band and a confidence score can diverge without contradicting each other.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months, where the underlying list-price and promotional-depth models are both precise but the only fact behind input cost comes from an internal analyst note
  When the answer is shown
  Then the confidence band is narrow, reflecting the underlying models' own precision
  And the confidence score is lower, reflecting that weakly sourced fact
  And the answer shows both without flagging either as an error

Scenario: The forecast moves with effective price, not list price, when only promotional depth changes.
  Given Competitor Brand's list price in Texas is not expected to change within the 6-month horizon, but a promotional depth change is documented within it
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the forecast reflects the promotional depth change even though list price itself is unchanged
  And opening the baseline shows the promotional change as what adjusted it, not a list price change

Scenario: A document-backed driver's evidence can be viewed without leaving the analysis.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months, with a tax change named as a contributing driver
  When the Query user opens the evidence behind that driver
  Then the answer shows the kind of source it came from, what it states, how credible that kind of source is, and when it took effect
  And the Query user has not left the analysis to see it

Scenario: A model-backed driver shows which model produced it, not a document that does not exist.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months, with demand sensitivity named as a contributing driver
  When the Query user opens the evidence behind that driver
  Then the answer names the model that produced it and when it was last validated
  And no document citation is shown, since none exists for this driver

Scenario: The forecast is exactly its baseline plus each driver's correction.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months
  When the answer is shown
  Then the decomposition graph shows the baseline and each driver's correction
  And the baseline plus those corrections equals the forecast move

Scenario: The baseline opens to what it was built from.
  Given Competitor Brand has announced a list price increase in Texas taking effect within 6 months
  When a Query user opens the baseline behind a Predict answer for Competitor Brand's effective price in Texas in 6 months
  Then the answer shows the price history the baseline was carried forward from, and as of when
  And it names the forecasting models that carried it forward, and when each was last validated
  And it shows the announcement that adjusted the baseline

Scenario: A question outside the standard horizons is built when asked, with the full answer.
  Given a Query user asks where Competitor Brand's effective price will be in Texas in 9 months
  When the question is answered
  Then the answer includes the forecast, its confidence score, the decomposition graph, and the evidence behind each driver

Scenario: The confidence score opens to the reasons behind it, naming the weakest source.
  Given the facts behind a Predict answer for Competitor Brand's effective price in Texas in 6 months come from a regulatory filing and from an internal analyst note
  When the Query user opens the confidence score
  Then source credibility reflects the internal analyst note, and names it
  And the answer shows how current the data is and whether the evidence agrees
  And each of those reasons can be opened to the evidence behind it without leaving the analysis

Scenario: A stated range is used at its midpoint and shown as the range.
  Given a Query user’s evidence includes a Texas filing raising the snacks tax by 1 to 2 percentage points within six months and a documented taxable base of USD 20 per unit
  When a Query user opens the tax driver behind a Predict answer for Competitor Brand's effective price in Texas in 6 months
  Then it shows the range the filing states
  And the driver evidence shows a midpoint increase of 1.5 percentage points and an effect of +USD 0.30 per unit before weighting

Scenario: A tax change with no stated size is held out of the forecast.
  Given a Query user’s unit has a filing that says the Texas sales tax on snacks will rise within six months and gives no rate
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the tax driver shows no contribution from the filing
  When the unit’s Control plane admin opens the review queue
  Then the filing is awaiting a usable rate

Scenario: A stated tax rate without a usable conversion stays in review.
  Given a Query user’s unit has a filing that gives the applicable in-horizon Texas tax rate while the taxable base per unit is unavailable
  When a Query user opens the forecast rationale
  Then the forecast shows no contribution from the filing
  When the unit’s Control plane admin opens the review item
  Then the item identifies the missing taxable base per unit

Scenario: Evidence that disagrees holds the confidence score down, and is shown rather than averaged away.
  Given Competitor Brand's price history in Texas points to a stable effective price, but a documented tax increase large enough to move it takes effect within the 6-month horizon
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then opening the confidence score shows the disagreement as a reason it is held down
  And it names the tax document on one side and the stable baseline on the other

Scenario: A competitor's product launch is used without a stated size.
  Given a document records Competitor Brand's launch of a new product in Texas taking effect within 6 months, without stating any price effect
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then competitor strategy contributes a correction sized by the model of Competitor Brand's past reactions
  And opening that driver shows both the document and the model

Scenario: A forecast based on market and model data explains its confidence.
  Given a competitor price forecast uses market and model data and no qualitative signal contributed
  When the Query user opens the confidence score
  Then the explanation states "No qualitative signals contributed"
  And source credibility and triangulation agreement are shown as not applicable
  And the score equals the freshness score of the data snapshot

Scenario: A contributing signal makes the ordinary confidence weights observable.
  Given the same snapshot and horizon as the forecast without qualitative evidence
  And one licensed commentary signal contributes, agrees with the baseline, and has a credibility score below snapshot freshness
  And the ordinary rubric gives credibility a positive weight and the other component scores equal snapshot freshness
  When the Query user opens the confidence explanation
  Then credibility, freshness and agreement each show their applicable score and rubric weight
  And the weighted score is lower than the freshness-only score

Scenario: The evidence view distinguishes all three source ranks.
  Given three otherwise identical forecasts with one contributing signal each
  And the signal comes from a regulatory filing, licensed commentary or an internal analyst note
  When the Query user opens each source's credibility assessment
  Then the filing ranks above the commentary and the commentary ranks above the note

Scenario: A spending driver with no qualifying signal explains its zero.
  Given no spending signal qualifies for the competitor, geography and forecast window
  When the Query user opens the zero spending contribution
  Then the explanation identifies the missing signal

Scenario: Measured spending effects can cancel.
  Given two qualifying spending signals with equal and opposite signed effects and a nonzero driver weight
  When the Query user opens the zero spending contribution
  Then both signed effects and both source citations are visible
  And the explanation attributes the zero to their cancellation

Scenario: Competitor plans have no contribution without a qualifying signal.
  Given an available competitor-response model and no competitor-plans signal for the question
  When the Query user opens competitor plans in the decomposition
  Then its contribution is zero and the explanation identifies the missing signal
  And the evidence view attributes no estimate to the model for that driver

Scenario: Brand A's current price is a reference in Predict.
  Given two questions with identical competitor evidence and forecast versions
  And only Brand A's current reference price differs
  When the Query user compares the Predict scorecards
  Then each shows its own Brand A reference price alongside the same competitor forecast
  And neither Predict scorecard reports a computed price gap or relative price index

Scenario: A brand-specific promotion does not alter a sibling brand's forecast.
  Given a competitor sells two brands in the same market
  And it announces deeper promotions only for the first brand
  When the Query user opens each brand's baseline evidence for that period
  Then only the first brand's baseline cites the promotion
  And a later announcement explicitly covering both brands appears in both baselines for its effective period

Scenario: Scheduled forecasts remain available when fresh computation is unavailable.
  Given the business unit published forecasts for two tracked competitors, their two brands each, two geographies and the 1-, 3-, 6- and 12-month horizons
  And the forecast models are temporarily unavailable after publication
  When the Query user asks about each of those 32 combinations
  Then each answer shows the selected brand's published forecast and confidence
  And its baseline opens to the evidence from that publication

Scenario: A previously answered nine-month question retains its forecast and evidence.
  Given the Query user received a committed nine-month forecast outside the scheduled grid
  And the published data, models, application and applicable settings have stayed the same
  When the forecast models become unavailable and the user repeats the question
  Then the nine-month forecast and its original rationale are still available
  And a first nine-month question for another tracked brand with no stored forecast reports that its forecast could not be produced


Scenario: Equal and opposite effects remain visible in a published forecast.
  Given a Query user has a published forecast where two eligible signals for the same driver contribute +0.20 and -0.20 per unit after weighting
  When the Query user opens that driver's evidence for the published forecast
  Then its net contribution is zero and both signals, their signed effects and the applied weight are shown
  And retrieving that forecast again identifies the same sources and model versions

Scenario: A scheduled drill-down remains available when live Predict is offline.
  Given the active publication contains a state forecast and a metro forecast with its own evidence
  And live Predict is unavailable
  When a Query user drills from the state to the metro and then asks for the same metro directly
  Then both responses show the same published metro forecast and evidence
```
