---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/reconciliation.md
---

## Review Queues

The Control plane admin role (`specs/application/product/roles.md § Roles`) reviews the handful of cases where the system flags something it is not confident about, an uncertain product match, an ambiguous document, a fact missing what it needs to be sized, since the client's own analysts know their catalog and their market better than anyone outside the business unit. A figure a reviewer supplies or corrects cites a document that states it, or, from the admin's own market knowledge, is recorded as an internal analyst note, so a Query user always sees where it came from, and it is weighed at that source's credibility. A document with no bearing on price is not flagged at all, and nothing it contains reaches a forecast. This sits alongside the same role's other self-service work (`specs/application/product/tenant-administration/reference-data-management.md`), a different kind of review, not a routine configuration change.

### Test Scenarios

```gherkin
Scenario: An uncertain product match is resolved using the client's own catalog knowledge.
  Given the system has flagged an uncertain match between a newly listed Northern Rival product and an existing catalog entry
  When a Control plane admin reviews the flagged match
  Then the admin either confirms the match needed no change or corrects it, using their own knowledge of the catalog

Scenario: An ambiguous document extraction is resolved using the client's own market knowledge.
  Given the system has flagged an ambiguous extraction from a newly ingested document about Northern Rival
  When a Control plane admin reviews the flagged extraction
  Then the admin either confirms the extraction needed no change or corrects it, using their own knowledge of the market

Scenario: A fact missing its size waits for review before any forecast uses it.
  Given a newly ingested regulatory filing states that Texas's sales tax on snacks will rise, without saying by how much
  When the filing is ingested
  Then no forecast uses that fact
  And it is flagged for a Control plane admin to resolve

Scenario: A figure supplied from a document is shown with that document.
  Given the system has flagged a regulatory filing's Texas sales tax increase on snacks for its missing rate
  When a Control plane admin supplies the rate by citing the state's published rate schedule
  Then the fact reaches forecasts weighed as that schedule's type of source
  And opening the driver shows the schedule that states the rate

Scenario: A figure supplied from an admin's own knowledge is shown as theirs.
  Given the system has flagged a regulatory filing's Texas sales tax increase on snacks for its missing rate
  When a Control plane admin supplies the rate from their own market knowledge
  Then the fact reaches forecasts as an internal analyst note, weighed as one
  And opening the driver shows the rate came from the admin's note, not the filing

Scenario: A document with no bearing on price is never used and never flagged.
  Given a newly ingested internal analyst note is a research paper on wasps
  When the note is ingested
  Then nothing it contains reaches a forecast
  And it is not flagged for review
```
