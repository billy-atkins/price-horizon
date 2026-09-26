---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/glossary-and-grounding.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/forecast-materialization.md
  - specs/application/technical/model-registry.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
---

## Predict — what will the competitor do

Effective price is not list or shelf price, it's the net price actually realized: list price minus trade promotions and rebates, plus any surcharges, per unit, over the period being asked about. This is the number Predict's forecast is actually about, and it's why a competitor's price can move materially from one month to the next even when their sticker price hasn't changed, a bigger promotion moved it, not a change on the shelf tag.

The forecast, the direction and magnitude of the competitor's likely move in effective price, is built from a baseline and a set of corrections, and the answer keeps both visible, as `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` requires. The baseline is the move the competitor's own price trend and usual promotional calendar point to by the horizon, adjusted for any price change or promotion the competitor has already announced. Each driver in the decomposition graph then adds its own correction, sized by the evidence behind it and by that driver's weight in a versioned weighting rubric. The forecast is exactly the baseline plus those corrections, and the decomposition graph shows each of them, so the chart is an accounting of how the number was built rather than a story told after it. The baseline opens to what it was built from: the price history as of when it was taken, the forecasting models that carried it forward and when each was last validated, and any announcement that adjusted it.

Most of that evidence exists before anyone asks. As documents arrive, the facts in them that bear on price, a tax change, a competitor's stated plan, are read, tagged with how credible that type of source is, a regulator's filing above licensed third-party commentary and either above an internal analyst note, and recorded. A fact is used only once it is complete enough to size: when it takes effect, which way it pushes, and by how much, or, for a competitor's product launch or capacity change, enough for the model of their past reactions to judge. A stated range is used at its midpoint and shown as the range. What happens to a fact that is not complete enough is `specs/application/product/tenant-administration/review-queues.md § Review Queues`. The forecast itself, with its breakdown and its confidence, is computed on a schedule for every competitor and geography a business unit tracks, at a standard set of horizons, so a question inside that set retrieves a forecast already built. A question outside it, a 9-month horizon for example, has its forecast built when asked, the same way and from the same evidence. What is done with the forecast, the positioning options, their simulated outcomes, and the plain-language account, is computed when the question is asked either way.

The confidence band is a range around the forecast itself, built from how much uncertainty the underlying list-price and promotional-depth models each carry. The confidence score is a separate read of the evidence behind the forecast: how credible its weakest source is, since one poorly sourced fact is never averaged away by better ones; how current its data is; and whether the evidence agrees with itself. The two can diverge, a forecast can sit inside a narrow band while still carrying a lower confidence score, if the models are precise but a driver rests on a weakly sourced or stale fact, and that is not a contradiction: each answers a different question about the same forecast, and the answer shows both without flagging either as an error. The confidence score opens to each of those reasons, as `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` requires, and the evidence each reason opens to here is the weakest source itself, how old the data is and when each fact took effect, and any disagreement big enough to count as a price move. When the evidence does not agree, a document pointing to a change big enough to count as a price move on its own, in a direction the baseline does not show, it names both sides and shows that the disagreement is holding the score down.

| Layer | What it shows |
|---|---|
| Scorecard / heatmap | Competitor Brand's probabilistic price forecast, with a confidence band around it and a confidence score alongside, Brand A's current price shown alongside as a reference point, not yet a computed comparison |
| Plain-language narrative | The expected impact and KPI implications, explained in business language, with the rationale behind the forecast stated alongside it, not just a score |
| Geographic visualization | A map, country to state or province to major metro, matching how the competitor's own pricing data is reported, showing how the top-line figure breaks down regionally |
| Decomposition graph | The baseline and a chart of the underlying drivers (the competitor's own demand sensitivity, input cost, competitor strategy, consumer spending trends, and tax), with how much each contributes to the forecast |

Every price shown here, current or forecasted, is in the local currency of the geography being discussed, the same rule `specs/application/product/answer-engine/position.md § Position — where Brand A should sit` states in full.

Each driver in the decomposition graph, and each qualitative fact named in the plain-language narrative, can be opened, without leaving the analysis, to see the specific evidence behind it. Most show the qualitative document behind them: its source type, what it actually states, how credible that kind of source is, and when it took effect. Demand sensitivity has no document behind it at all, since it is estimated rather than reported; opening it shows which model produced the estimate and when that model was last validated instead. Competitor strategy shows both together, the document and the model that translated it into a magnitude, since one never appears in this forecast without the other. A driver that contributed nothing to a particular forecast still shows why, that no signal reached it for this query, not an empty or broken view. This is where the sourcing guarantee (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`) is made visible to a Query user, not just asserted, and it is this same evidence view that the answer's own lineage (`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`) refers to.

`specs/application/product/architecture.md § Diagrams § The Answer` and `specs/application/product/architecture.md § Diagrams § From Evidence to Answer` render this.

### Test Scenarios

```gherkin
Scenario: A resolvable question returns a confidence-scored forecast.
  Given a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  When the question is answered
  Then the answer includes a forecasted direction and magnitude for Competitor Brand's effective price, a confidence score, and a plain-language rationale stating what is driving the forecast
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

Scenario: A driver with no contribution to this forecast still shows why.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months, with consumer spending trends contributing nothing to this particular forecast
  When the Query user opens the evidence behind that driver
  Then the answer states that no signal reached this driver for this query
  And the view is not shown as empty or broken

Scenario: The forecast is exactly its baseline plus each driver's correction.
  Given a Query user has a Predict answer for Competitor Brand's effective price in Texas in 6 months
  When the answer is shown
  Then the decomposition graph shows the baseline and each driver's correction
  And the baseline plus those corrections equals the forecasted move

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
  Given a regulatory filing states that Texas's sales tax on snacks will rise by between 1 and 2 points within 6 months
  When a Query user opens the tax driver behind a Predict answer for Competitor Brand's effective price in Texas in 6 months
  Then it shows the range the filing states
  And the forecast uses a 1.5-point rise

Scenario: A fact with no stated size is not used in the forecast.
  Given a regulatory filing states that Texas's sales tax on snacks will rise within 6 months, without saying by how much
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the forecast's tax driver does not use that fact

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
```
