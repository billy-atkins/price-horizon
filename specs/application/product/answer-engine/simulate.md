---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Simulate: what follows for the business

Each Position option ([`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)) carries its own projected outcome: share, volume, category growth, revenue, and margin implications. The outcomes are shown side by side, so the trade-off between options is visible before a decision is made, not discovered afterward.

Every simulated outcome shows its confidence figure when the inputs to confidence are available. Missing calibration or other required confidence evidence yields an unavailable figure and names the missing input. The figure is drawn from the models that produced the outcome rather than inherited unchanged from the forecast, because projecting a business outcome introduces uncertainty the forecast never carried. [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) holds the figure to never being shown as more certain than the forecast behind it.

The confidence figure opens the same way a forecast's confidence does, as [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes) requires. Opened, it shows how confident and how recently validated the models behind the outcome are, naming whichever model set each. It also shows whether the figure was held down to the forecast's own confidence.

A margin-protecting option and a share-protecting option should look visibly different here, since that difference is the point of this stage. Each outcome carries its own brief explanation of what is driving it, not just the figures side by side.

[`specs/application/product/architecture.md § Diagrams § The Answer`](/specs/application/product/architecture.md#the-answer) and [`specs/application/product/architecture.md § Diagrams § From Evidence to Answer`](/specs/application/product/architecture.md#from-evidence-to-answer) render this.

Share is Brand A’s share of category volume in the market and period asked about. Category growth compares total projected category units with observed units for the comparable prior-year period in that market. If that historical reference or a usable volume share is missing, the category-growth field opens to the reason. All outcomes in a question share the confidence assessment of the simulation models used and the same ceiling from Predict. Prices, projected results and the inputs explaining each candidate stay distinct.

### Test Scenarios

```gherkin
Scenario: Every option's outcome is projected and shown side by side.
  Given a Query user has generated positioning options for Competitor Brand's effective price in Texas in 6 months
  When the options are simulated
  Then each option shows its own projected share, volume, category growth, revenue, and margin implications
  And all options' outcomes are shown side by side

Scenario: Different strategies produce visibly different outcomes.
  Given a Query user has generated Hold and Diverge as two of the positioning options for Competitor Brand's effective price in Texas in 6 months, for a brand pricing decision
  And their prices differ and the pinned share, volume and margin models project materially different values for the two prices
  When the options are simulated
  Then Hold's and Diverge's projected share, volume, and margin outcomes are visibly different from each other

Scenario: Simulated outcomes with valid calibration carry a confidence figure.
  Given a Query user has simulated outcomes for Competitor Brand's effective price in Texas in 6 months, for a brand pricing decision, across the Hold, Match, Close the Gap, and Diverge options
  And every invoked version has a usable interval, matching calibration and validation date, and the parent forecast has a score
  When the outcomes are shown
  Then every outcome shows a confidence figure alongside its projected share, volume, category growth, revenue, and margin
  And that figure is the same for every option in this answer, since the same models produced all of them

Scenario: Each outcome carries its own driver explanation.
  Given a Query user has simulated outcomes for Competitor Brand's effective price in Texas in 6 months
  When the outcomes are shown
  Then each outcome includes its own brief explanation of what is driving it, not just its figures

Scenario: A simulated outcome's confidence opens to the reasons behind it.
  Given a Query user has simulated outcomes for positioning options against Competitor Brand's effective price in Texas in 6 months
  When the Query user opens one outcome's confidence figure
  Then the answer shows how confident, and how recently validated, the models behind that outcome are, naming whichever model set each
  And it shows whether the figure was held down to the forecast's own confidence
  And the Query user has not left the analysis to see it

Scenario: A user can trace category growth to comparable units.
  Given a candidate projects 120 brand units and a 20 percent volume share
  And the comparable prior-year category volume is 500 units
  When the Query user opens category growth
  Then the projection shows 600 category units and 20 percent growth
  And the explanation identifies the reference period and the candidate inputs

Scenario: Missing historical category volume leaves other projections visible.
  Given a candidate priced at 9 projects 120 brand units and a 20 percent volume share
  And the selected geography has no comparable prior-year category volume in the pinned snapshot
  When the user opens category growth
  Then the answer identifies the missing historical reference and shows category growth as unavailable
  And it still shows 120 units and revenue of 1,080 in local currency

Scenario: Zero volume share cannot support an implied category total.
  Given the share model projects zero share and the volume model projects 120 brand units at a candidate price of 9
  When the user opens the simulation
  Then category growth is unavailable with the unusable share identified
  And the answer shows 120 projected units and revenue of 1,080 in local currency

Scenario: Changing the volume display unit preserves confidence.
  Given the same volume model interval and its calibration width are converted from units to thousands
  And the same model versions, rubric and parent forecast are used
  When the user compares the confidence explanations
  Then both show the same limiting models, component scores and final confidence

Scenario: A downstream score is capped by the forecast.
  Given an uncapped simulation score of 0.8 and a parent forecast score of 0.6
  When the Query user opens either candidate’s confidence
  Then the displayed score is 0.6 and the explanation names the forecast ceiling

Scenario: Missing calibration leaves the projections visible.
  Given a candidate has simulated volume of 120 units and the volume model has no registered calibration for its interval
  When the user opens the outcome
  Then the answer shows 120 units and identifies the volume model and missing calibration in place of a confidence figure

Scenario: Choices kept at the floor can have equal outcomes.
  Given all four eligible strategies have the same price and identical simulated figures
  When the Query user inspects the two displayed choices
  Then the figures are equal and all four original strategy labels and their member prices are accessible
```
