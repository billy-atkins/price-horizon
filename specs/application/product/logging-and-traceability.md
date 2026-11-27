---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/guarantees-mechanics.md
---

## Logging and Traceability

PriceHorizon keeps different kinds of record about itself. Each kind answers a different question for a different audience, and the kinds are never folded into one. The separation exists to prevent one confusion: treating an access record as if it explained a number, or a number's own provenance as if it were an activity log.

### Audit Log

The audit log is the record of who did something, and when: a Query user asking a question, a Control plane admin or an Identity admin changing what they govern, or Acme AI accessing an installation to support, monitor, or upgrade it. It is a compliance record, kept for at least a year by default. Both the client and Acme AI can read it:
- A Control plane admin sees their own business unit's activity, and installation-wide events such as an upgrade or a change to who holds the Platform admin role.
- An Identity admin sees every change to who is granted access, and every question refused for lack of any business unit access.
- Acme AI sees its own installation's activity.

The full capability, what a Control plane admin and an Identity admin can see and how, is [`specs/application/product/tenant-administration/audit-log-visibility.md`](/specs/application/product/tenant-administration/audit-log-visibility.md).

### Application Log

The application log is the record of how the application executed a request internally: which steps ran, how long each took, what failed or retried. It is a debugging record, not an activity record. It is Acme AI's own engineering concern, with no end-user log screen for a Query user, Control plane admin or Identity admin. The application log is kept only long enough to debug a recently reported issue, weeks rather than years. It never carries the actual content of a forecast, a document, or a credential.

PriceHorizon forwards the application log to the client's own observability system. Where the client runs none, PriceHorizon forwards the log to an observability viewer shipped alongside PriceHorizon. PriceHorizon needs no connection outside the client's environment to forward the log. It never sends the log to anything Acme AI hosts, and never combines it with another customer's.

The self-service capability, how much detail is captured and who can raise it, is [`specs/application/product/tenant-administration/application-log-control.md`](/specs/application/product/tenant-administration/application-log-control.md).

### Answer Lineage

Answer lineage is what a specific number is made of: which precomputed forecast, which qualitative evidence, and which model, at which version, produced it. It is neither an activity record nor a debugging record. Answer lineage is how PriceHorizon backs up its guarantee that every number traces back to a named, versioned source ([`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)). A Query user sees it directly, inside the answer, by opening the evidence behind any driver or option without leaving the analysis ([`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)). The Query user never consults a log of any kind to see it.

### Test Scenarios

```gherkin
Scenario: An analyst can trace a price without access to operational logs.
  Given a Query user has a forecast with a documented driver in their own business unit
  When they open that driver in the answer
  Then they see its source and the recorded contribution
  And that action grants no access to the audit log or application log

Scenario: A background job can be diagnosed without attributing it to a Query user.
  Given a scheduled forecast refresh fails before any user asks a question
  When an authorized operator inspects its trace
  Then the trace identifies the service, run and application version
  And it contains no forecast values, document content or credentials

Scenario: A failure during Predict retains a question with no delivery.
  Given an authorized question reaches Predict but no forecast completes
  When its retries are exhausted
  Then its retained audit entry identifies the failed question with no Delivered Answer
  And the authorized reader sees no substituted forecast or downstream figure
```
