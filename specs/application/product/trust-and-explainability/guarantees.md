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

- **A repeatable answer.** The same question, asked twice with nothing changed in between, returns the same answer both times. Nothing changed means that none of these has changed: the data behind the answer, the application version, the model versions, the business unit's own configuration, and the kind of decision the question is asked for ([`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context)). Repeatability is not automatic in an AI system. It has to be engineered in. The guarantee covers the substance: the forecast, the confidence score, and the numbers behind every layer. It does not cover the exact wording of the sentence explaining them. Two runs might phrase an explanation slightly differently while stating the identical figure. When one of those inputs has changed, two answers to the same question may legitimately differ. That difference is the consequence of a known change, not an unexplained result. The answer's own lineage shows which model, at which version, produced a given number ([`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`](/specs/application/product/logging-and-traceability.md#answer-lineage)).
- **An answer enriched by quantitative data.** Every number in the output traces back to a named, versioned model or dataset. Nothing is asserted without a source behind it. This traceability is the answer's own lineage, whose section also says how a Query user sees it ([`specs/application/product/logging-and-traceability.md § Logging and Traceability § Answer Lineage`](/specs/application/product/logging-and-traceability.md#answer-lineage)).
- **An answer grounded in qualitative information.** Regulatory changes, strategic plans, and competitive intelligence are weighed alongside the numbers, not appended afterward as commentary. A price forecast that ignores a known tax change is not a forecast. It is a math error waiting to happen.
- **An answer that shows how it was built.** No number in an answer is a magic number. A forecast is its baseline plus each driver's correction ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). The answer shows every part of that sum, and each part opens to what it was built from. An estimate is a figure allocated below the geography the competitor's data reports. What an estimate opens to is stated in [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage). Every confidence figure, whether on a forecast, a positioning option, or a simulated outcome, opens to the reasons it sits where it does. Each reason opens to the evidence behind it, without leaving the analysis. An executive sees not just the number but why to believe it, or why not yet.

Underneath every guarantee, when the evidence behind a number falls below a confidence threshold, the system says so, rather than producing a fluent, unsupported answer. When a term in the question itself cannot be resolved, or it is unclear which business unit or kind of decision the question is about, the system asks a clarifying question rather than guessing. It computes nothing for that question. A clearly labeled uncertain answer is worth more than a confident wrong one, particularly for a number an executive might act on. A related but separate guarantee covers what happens when the system cannot complete an answer at all, or only part of one ([`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior)).

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer), [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) and [`specs/application/product/architecture.md § Diagrams § When an Answer Falls Short`](/specs/application/product/architecture.md#when-an-answer-falls-short) render this.

### Test Scenarios

```gherkin
Scenario: The same question, asked twice with nothing changed in between, returns the same substance.
  Given a Query user has already asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer
  When the Query user asks the identical question again, with none of the underlying data, the application version, the model versions, the business unit's configuration, or the kind of decision it is asked for having changed
  Then the forecast, confidence score, and every numeric figure in the answer are identical to the first answer
  And the narrative's exact wording may differ without affecting this guarantee

Scenario: A model version bumped between two asks explains a legitimate difference rather than a defect.
  Given a Query user has already asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer
  And the effective price model has since been upgraded to a new version, with the underlying data unchanged
  When the Query user asks the identical question again
  Then the forecast may legitimately differ from the first answer
  And opening the evidence behind the forecast names the model version that produced it

Scenario: A known regulatory signal is folded into the forecast, not appended as commentary.
  Given a known tax change affecting Texas is documented within the 6-month horizon
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the decomposition and the plain-language rationale name the tax change as a contributing driver to the forecast

Scenario: A known competitor plan is folded into the forecast, not appended as commentary.
  Given a known pricing plan for Competitor Brand in Texas is documented within the 6-month horizon
  When a Query user asks where Competitor Brand's effective price will be in Texas in 6 months
  Then the plain-language rationale names that competitor plan
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
```
