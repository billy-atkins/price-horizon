---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/query-service/layered-output-synthesis.md
---

## Simulate — what follows for the business

Each Position option (`specs/application/product/answer-engine/position.md § Position — where Brand A should sit`) carries its own projected outcome: share, volume, category growth, revenue, and margin implications, shown side by side so the trade-off between options is visible before a decision is made, not discovered afterward. Every simulated outcome in an answer carries a confidence figure, drawn from the models that produced it rather than inherited unchanged from the forecast, since projecting a business outcome introduces uncertainty the forecast itself never carried; `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` holds it to never being shown as more certain than the forecast behind it. That figure opens the same way a forecast's confidence does, as `specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes` requires, to show how confident and how recently validated the models behind the outcome are, naming whichever model set each, and whether the figure was held down to the forecast's own confidence. A margin-protecting option and a share-protecting option should look visibly different here — that difference is the point of this stage. Each outcome carries its own brief explanation of what is driving it, not just the figures side by side.

`specs/application/product/architecture.md § Diagrams § The Answer` and `specs/application/product/architecture.md § Diagrams § From Evidence to Answer` render this.

### Test Scenarios

```gherkin
Scenario: Every option's outcome is projected and shown side by side.
  Given a Query user has generated positioning options for Competitor Brand's effective price in Texas in 6 months
  When the options are simulated
  Then each option shows its own projected share, volume, category growth, revenue, and margin implications
  And all options' outcomes are shown side by side

Scenario: Different strategies produce visibly different outcomes.
  Given a Query user has generated Hold and Diverge as two of the positioning options for Competitor Brand's effective price in Texas in 6 months, for a brand pricing decision
  When the options are simulated
  Then Hold's and Diverge's projected share, volume, and margin outcomes are visibly different from each other

Scenario: Every simulated outcome carries a confidence figure.
  Given a Query user has simulated outcomes for Competitor Brand's effective price in Texas in 6 months, for a brand pricing decision, across the Hold, Match, Close the Gap, and Diverge options
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
```
