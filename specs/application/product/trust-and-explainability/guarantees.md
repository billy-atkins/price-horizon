---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/evaluation-and-monitoring.md
  - specs/application/technical/guarantees-mechanics.md
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Guarantees This Answer Engine Makes

Every answer PriceHorizon produces is built to satisfy these requirements. The technical specification holds the mechanics behind each one. The guarantees themselves are what make the output trustworthy enough to act on. They hold across every stage of the answer. A positioning option and its simulated outcome are held to the same standard as the underlying forecast, not treated as softer, downstream commentary. One consequence is visible in every answer: no later stage is ever shown as more certain than the stage it was built on. Each stage arrives there differently, and each states how ([`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit), [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)).
- **A repeatable answer.** For the same resolved question and decision, the numeric results repeat when each layer uses the same data, versions, settings and forecast scoring date. Reusing a forecast preserves its original confidence. A newly calculated forecast can have a different confidence score when the same evidence falls in an older freshness band. A fresh explanation can phrase those figures differently. A reader opening the retained answer sees its original wording, figures, order, labels and supporting evidence as delivered. The answer’s lineage identifies the versions behind each figure ([`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`](/specs/application/product/logging-and-traceability.md#answer-lineage)).
- **An answer enriched by quantitative data.** Every number in the output traces back to a named, versioned model or dataset. Nothing is asserted without a source behind it. This traceability is the answer's own lineage, whose section also says how a Query user sees it ([`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`](/specs/application/product/logging-and-traceability.md#answer-lineage)).
- **An answer grounded in qualitative information.** The forecast uses eligible evidence through the route assigned in [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do § Event Type Taxonomy`](/specs/application/product/answer-engine/predict.md#event-type-taxonomy). A tax change can contribute when its amount and documented conversion support an effect per unit. Incomplete tax evidence goes to review. A qualifying competitor launch or capacity change can contribute through its response model even when its source provides no magnitude.
- **An answer that shows how it was built.** No number in an answer is a magic number. A forecast is its baseline plus each driver's correction ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). The answer shows every part of that sum, and each part opens to what it was built from. Below the supported geography, an estimate identifies the evidence used for the local figure. A regional reference identifies its own geography. What an estimate opens to is stated in [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage § What a granularity drill-down shows`](/specs/application/product/answer-engine/drill-down.md#what-a-granularity-drill-down-shows). Every confidence figure, whether on a forecast, a positioning option, or a simulated outcome, opens to the reasons it sits where it does. Each reason opens to the evidence behind it, without leaving the analysis. An executive sees not just the number but why to believe it, or why not yet.

If the forecast score falls below the threshold that applies to that forecast, the answer labels the forecast as low confidence. A Query user reopening the delivery sees the original assessment if it was saved or can be recovered from that forecast’s score and threshold. If an older delivery lacks that evidence, the answer marks its historical assessment unavailable. The figures and their assessment remain accessible when narrative wording is unavailable. When a term in the question itself cannot be resolved, or it is unclear which business unit or kind of decision the question is about, the system asks a clarifying question rather than guessing. It computes nothing for that question. A clearly labeled uncertain answer is worth more than a confident wrong one, particularly for a number an executive might act on. A related but separate guarantee covers what happens when the system cannot complete an answer at all, or only part of one ([`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior)).

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer), [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) and [`specs/application/product/architecture.md § Diagrams § When an Answer Falls Short`](/specs/application/product/architecture.md#when-an-answer-falls-short) render this.

### Test Scenarios

```gherkin
Scenario: The same question, asked twice with nothing changed in between, returns the same substance.
  Given a Query user has already asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer
  When the Query user asks for the same target period and retrieves the same forecast, with unchanged data, versions, settings and decision context
  Then the forecast, confidence score, and every numeric figure in the answer are identical to the first answer
  And the narrative's exact wording may differ without affecting this guarantee

Scenario: Recalculation can change confidence as the same evidence ages.
  Given a Query user received a forecast based on a November 1 snapshot and no qualitative signals
  And the forecast was calculated on November 3 and its confidence reflected a two-day-old snapshot
  When a new publication calculates the same forecast on November 8 with the same evidence and versions, and seven days falls in a lower freshness band
  Then the new forecast shows the lower confidence and its scoring date
  And reopening the earlier delivery still shows its original confidence

Scenario: A settings change leaves the original answer available as delivered.
  Given a Query user in North America Snacks received a forecast of 4.20 and a "Close the Gap" option with a simulated share of 18%
  And the business unit later renamed the option "Narrow the Spread"
  When its Control plane admin opens the original question in audit detail
  Then the original wording, option order, "Close the Gap" label, 4.20 forecast and 18% share are available as delivered
  And the figures open to the evidence and versions used for that answer

Scenario: A model version bumped between two asks explains a legitimate difference rather than a defect.
  Given a Query user has already asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer
  And the effective price model has since been upgraded to a new version, with the underlying data unchanged
  When the Query user asks the identical question again
  Then the forecast may legitimately differ from the first answer
  And opening the evidence behind the forecast names the model version that produced it

Scenario: A known regulatory signal is folded into the forecast, not appended as commentary.
  Given a Query user’s unit has a regulatory filing documenting an in-horizon Texas tax increase and the taxable base for converting it to an amount per unit
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the decomposition and the plain-language rationale name the tax change as a contributing driver to the forecast

Scenario: A known competitor plan is folded into the forecast, not appended as commentary.
  Given a Query user’s unit has a document announcing Competitor Brand’s qualifying Texas product launch within the forecast horizon, with no stated price effect
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the rationale identifies the launch document and the response model that sized its contribution
  And the forecast reflects that plan

Scenario: Every number in the answer names the model or dataset behind it.
  Given a Query user has asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer with positioning options
  When the Query user opens the evidence behind a forecast driver and behind a positioning option
  Then each names the model or dataset that produced it, at the version used
  And no figure is shown without a source behind it

Scenario: Simulate is never shown as more certain than the forecast it is built on.
  Given a Query user has a Predict forecast for Competitor Brand's effective price in Texas in 6 months, flagged as low-confidence
  When Simulate generates its outcomes from the resulting Position options
  Then no Simulated Outcome is shown with a confidence score higher than that low-confidence forecast

Scenario: A low-confidence answer is flagged, not hidden behind false certainty.
  Given the evidence behind Competitor Brand's effective price forecast in Texas in 6 months falls below the confidence threshold
  When a Query user asks the question
  Then the answer states that its confidence is low
  And the answer does not present a fluent, unsupported figure as though it were certain

Scenario: A question unclear about its business unit gets a clarifying question.
  Given a Query user whose access holds North America Snacks and Europe Beverages, both of which track Competitor Brand, has not yet chosen a business unit
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, for Brand A's list price
  Then they get a clarifying question about which business unit it is for
  And nothing is computed for that question

Scenario: A question unclear about its kind of decision gets a clarifying question.
  Given a Query user's session is set to a brand pricing decision for North America Snacks
  When they ask whether Brand A's list price or its next promotion should respond to Competitor Brand's effective price in Texas in 6 months
  Then they get a clarifying question about which kind of decision it is
  And nothing is computed for that question

Scenario: An unresolvable competitor stops the pipeline rather than guessing.
  Given a Query user asks where Southern Rival's effective price will be in Texas in 6 months
  And Southern Rival does not resolve uniquely against the business unit's governed glossary
  When the question is asked
  Then the system asks a clarifying question
  And no forecast, confidence score, or rationale is computed for that query

Scenario: The forecast shows how it was built.
  Given a Query user has asked where Competitor Brand's effective price will be in Texas in 6 months
  When the answer is shown
  Then it shows the forecast as its baseline plus each driver's correction
  And the baseline and each driver open to what they were built from

Scenario: Every confidence figure in the answer opens to why it sits where it does.
  Given a Query user has an answer for Competitor Brand's effective price in Texas in 6 months, with positioning options and their simulated outcomes
  When the Query user opens the confidence on the forecast, on a positioning option, and on a simulated outcome
  Then each shows the reasons it sits where it does
  And each reason opens to the evidence behind it without leaving the analysis

Scenario: A forecast keeps its original warning after recalibration.
  Given a Query user received a forecast labeled low confidence
  And the current scoring rubric would clear that warning at the same score
  When the Query user reopens the delivery while its narrative is unavailable
  Then the forecast figures still show the original low-confidence warning

Scenario: An older forecast lacks evidence for its original warning.
  Given a Query user received a forecast whose original score is available but whose warning and original threshold were not retained and cannot be recovered
  When the Query user reopens the delivery after a new threshold takes effect
  Then the forecast still shows its recorded score and marks the historical warning assessment unavailable
```
