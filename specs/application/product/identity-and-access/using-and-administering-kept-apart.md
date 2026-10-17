---
technical-specs:
  - specs/application/technical/engineering-and-production-considerations.md
---

## Using and Administering Kept Apart

PriceHorizon keeps using it and administering it on architecturally separate paths, rather than relying on a permissions setting alone. The path that answers questions never holds the credentials to change configuration. So a problem in the far more widely used query path has no way to reach the far more sensitive administrative one.

A security-conscious buyer can know who can ask a pricing question, and who can change what a competitor's code means or edit a threshold. The buyer can also know that those two are never the same path by accident, even for a person holding both the Query user and Control plane admin roles. Every role holds to this separation, and so does every technical service boundary built to enforce it.

[`specs/application/product/architecture.md § Diagrams § Using and Administering`](/specs/application/product/architecture.md#using-and-administering) renders this.

### Test Scenarios

```gherkin
Scenario: The path that answers a question cannot change configuration.
  Given a Query user in North America Snacks
  When they ask where Competitor Brand's effective price will be in Texas in 6 months
  Then the path that answers them holds no credential to change North America Snacks' thresholds or reference data

Scenario: Holding both roles does not join the two paths.
  Given a person holds both the Query user and Control plane admin roles in North America Snacks
  When they ask where Competitor Brand's effective price will be in Texas in 6 months
  Then the path that answers them holds no credential to change North America Snacks' thresholds or reference data

Scenario: A person holding both roles changes configuration only on the administrative path.
  Given a person holds both the Query user and Control plane admin roles in North America Snacks
  When they raise North America Snacks' stable-price threshold from 1% to 2% of today's price
  Then the change is made on the administrative path
  And not on the path that answers their questions
```
