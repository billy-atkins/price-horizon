---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/guarantees-mechanics.md
---

## Logging and Traceability

PriceHorizon keeps different kinds of record about itself, each answering a different question for a different audience, never folded into one. Treating an access record as if it explained a number, or a number's own provenance as if it were an activity log, is exactly the confusion this separation exists to prevent.

### Audit Log

The record of who did something, and when: a Query user asking a question, a Control plane admin or an Identity admin changing what they govern, or Acme AI accessing an installation to support, monitor, or upgrade it. A compliance record, kept for at least a year by default, readable by both the client and Acme AI, a Control plane admin seeing their own business unit's activity and installation-wide events such as an upgrade or a change to who holds the Platform admin role, an Identity admin every change to who is granted access and every question refused for lack of any business unit access, and Acme AI its own installation's activity. The full capability, what a Control plane admin and an Identity admin can see and how, is `specs/application/product/tenant-administration/audit-log-visibility.md`.

### Application Log

The record of how the application executed a request internally: which steps ran, how long each took, what failed or retried. A debugging record, not an activity record, Acme AI's own engineering concern, with no product screen for either role. Kept only long enough to debug a recently reported issue, weeks rather than years, and never carrying the actual content of a forecast, a document, or a credential. It is forwarded to the client's own observability system, or, where the client runs none, to an observability viewer shipped alongside PriceHorizon, and PriceHorizon needs no connection outside the client's environment to forward it, never sends it to anything Acme AI hosts, and never combines it with another customer's. The self-service capability, how much detail is captured and who can raise it, is `specs/application/product/tenant-administration/application-log-control.md`.

### Answer Lineage

What a specific number is actually made of: which precomputed forecast, which qualitative evidence, which model, at which version, produced it. Neither an activity record nor a debugging record, this is how PriceHorizon backs up its own guarantee that every number traces back to a named, versioned source (`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`). A Query user sees it directly, inside the answer itself, by opening the evidence behind any driver or option without leaving the analysis (`specs/application/product/answer-engine/predict.md § Predict — what will the competitor do`), never by consulting a log of any kind.
