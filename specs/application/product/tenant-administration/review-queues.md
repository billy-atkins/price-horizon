---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/materialization-service/driver-signal-extraction.md
  - specs/application/technical/materialization-service/reconciliation.md
---

## Review Queues

The Control plane admin role ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) reviews the handful of cases where the system flags something it is not confident about: an uncertain product match, an unresolved source geography, an ambiguous document, or a fact missing what it needs to be sized. The review falls to this role because the client's own analysts know their catalog and their market better than anyone outside the business unit.

A source observation whose geography cannot be reliably identified at its reported level appears once for the unit, even on a retry. The unit’s Control plane admin can confirm a supported geography, correct the mapping, or dismiss unusable evidence. A conflict leaves the original mapping in force and the item open. Until resolution, the dependent comparison is unavailable. A successful resolution reaches future computations and publications, and an earlier delivery keeps its original geography.

A figure a reviewer supplies or corrects either cites a document that states it or, when the figure comes from the admin's own market knowledge, is recorded as an internal analyst note. So a Query user always sees where the figure came from, and the figure is weighed at that source's credibility. A document with no bearing on price is not flagged at all, and nothing it contains reaches a forecast.

The review queues sit alongside the same role's other self-service work ([`specs/application/product/tenant-administration/reference-data-management.md`](/specs/application/product/tenant-administration/reference-data-management.md)). Resolving a flagged case is a different kind of review, not a routine configuration change.

### Test Scenarios

```gherkin
Scenario: The unit resolves a geography before the comparison becomes available.
  Given West’s Control plane admin reviews geography matches for a source code that also appears in East, where it has a reliable mapping
  When the West unit receives the same observation twice
  Then the West Control plane admin sees one geography item and its dependent comparison is unavailable
  When the admin confirms the supported West geography and a new forecast using that evidence is published
  Then the new comparison uses the West geography, East keeps its mapping, and an earlier West delivery still opens as delivered

Scenario: A conflicting geography correction keeps the case open.
  Given the unit’s Control plane admin has opened an unresolved geography observation
  And the proposed source code already identifies a different canonical geography in that unit
  When the admin attempts that correction
  Then the original mapping stays in effect, the item remains open and its dependent comparison is unavailable

Scenario: Dismissing an unresolved geography leaves its dependent comparison unavailable.
  Given the unit's Control plane admin has opened an observation with no supported geography at its reported level
  When the admin dismisses it and the observation is delivered again
  Then the item remains dismissed and the dependent comparison is unavailable
  And independently grounded prices remain accessible

Scenario: A reviewer corrects an uncertain catalog match.
  Given a flagged match pairs a Northern Rival six-pack with Brand A's single pack
  When the unit's Control plane admin corrects the match to Brand A's six-pack
  Then the resolved match identifies the six-pack and the single pack stays excluded from the comparison

Scenario: A reviewer confirms an ambiguous document extraction.
  Given a filing states a two-point tax increase and the extracted figure awaits review
  When the unit's Control plane admin checks the filing and confirms the two-point figure
  Then the item is resolved and the figure retains the filing as its source

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
