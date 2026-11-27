## Bulk Evidence and Accuracy Report

There is one report, not one per scope. A Control plane admin's own business unit, a Platform admin's escalated look at one business unit, and a Platform admin's installation-wide view are the same underlying join at different scopes. All of them are stated together in [`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy), which the onboarding health check [`specs/application/product/platform-and-compliance-operations/onboarding-verification.md`](/specs/application/product/platform-and-compliance-operations/onboarding-verification.md) also reuses. Access to each scope follows the query service's own existing claim-based model, and adds no new gating mechanism. A Control plane admin's claim is already scoped to one business unit, and a Platform admin's is not ([`specs/application/technical/identity-and-access.md § Platform admin access`](/specs/application/technical/identity-and-access.md#platform-admin-access)). So the existing claim model already produces the right scope for each.

### Who sees which business units

The report is open to the two roles this Decision Table names, each seeing the business units its claim allows:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Role \
**Input Values:**
  - Role: "Control plane admin", "Platform admin"

| Role | Business units in scope |
|---|---|
| Control plane admin | Their own single business unit |
| Platform admin | Every business unit the installation hosts, any one of them looked at alone when a Control plane admin escalates it |

### Report assembly

Select successfully published batch forecasts and committed live forecasts, one per immutable ID in the authorized unit selection. Resolve their rationale and retrieval trace, origin, target window and dated comparison state. Use the stored outcome for the observed price, actuals vintage, signed error and verdict. Distinct outcomes supply the accuracy denominator.

For each unit, associate each committed forecast-bearing answer with its question and forecast. Count it once by delivery identifier. Count its first authenticated client receipt separately, using the original question time for both counts. A disconnected client leaves the first count intact. Expose asker and question details only under the applicable unit audit permission. Label each count as retained only when its coverage is incomplete.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - permitted units
  - forecast rows
  - delivered activity
  - activity interval
  - retained since
  - receipts retained since
  - confirmed activity

**Output:**
  - accuracy report

**Runs When:**
  - an authorized administrator requests the evidence and accuracy report

| Step | Action |
|---|---|
| 1 | Set report rows to for f in forecast rows[list contains(permitted units, item.unit)] return {forecast: f.id, unit: f.unit, evidence: f.evidence, state: f.state, reason: f.reason, outcome: f.outcome, deliveries: delivered activity[item.unit = f.unit and item.forecast = f.id and item.at >= activity interval.start and item.at < activity interval.end].delivery, confirmations: confirmed activity[item.unit = f.unit and item.forecast = f.id and item.at >= activity interval.start and item.at < activity interval.end].delivery} |
| 2 | Set accuracy report to {rows: report rows, requested: activity interval, covered from: if retained since > activity interval.start then min([retained since, activity interval.end]) else activity interval.start, covered until: activity interval.end, complete: retained since <= activity interval.start, confirmations covered from: min([activity interval.end, max([retained since, receipts retained since, activity interval.start])]), confirmations complete: max([retained since, receipts retained since]) <= activity interval.start} |
| 3 | End |

## Facts

**Records:**
  - **Name:** receipts retained since \
    **Type:** number \
    **Means:** the start in UTC epoch milliseconds of continuous collection and retention of receipt evidence, with the same conservative treatment of unknown history as the question retention boundary

  - **Name:** confirmed activity \
    **Type:** list<context<unit: string, forecast: number, delivery: number, at: number>> \
    **Means:** distinct committed question-to-delivery links with an authenticated matching acknowledgement at the snapshot, keyed by the committed link's unit, forecast, delivery and original question time

  - **Name:** permitted units \
    **Type:** list<string> \
    **Means:** business-unit codes permitted by the role and selected report filter; an empty scope produces no rows

  - **Name:** forecast rows \
    **Type:** list<context<id: number, unit: string, evidence: number, state: string, reason: string, outcome: number>> \
    **Means:** one eligible stored forecast per immutable ID, with rationale reference, comparison state, reason for a pending or unevaluable comparison, and optional stored outcome ID

  - **Name:** delivered activity \
    **Type:** list<context<unit: string, forecast: number, delivery: number, at: number>> \
    **Means:** distinct retained audit-to-delivery links with question time in UTC epoch milliseconds permitted for the requested scope; a qualifying delivery actually references this forecast, including partial answers containing Predict

  - **Name:** report rows \
    **Type:** list<context<forecast: number, unit: string, evidence: number, state: string, reason: string, outcome: number, deliveries: list<number>, confirmations: list<number>>> \
    **Means:** one row per forecast in scope, preserving the eligible retained deliveries as a nested collection

  - **Name:** activity interval \
    **Type:** context<start: number, end: number> \
    **Means:** the requested nonempty interval of question times through the report snapshot, in UTC epoch milliseconds, including start and excluding end

  - **Name:** retained since \
    **Type:** number \
    **Means:** the start of provably complete question history at the report snapshot. Use the later of the start of audit collection and the greatest cutoff applied by a retention purge. Extending retention cannot restore purged history. If earlier cutoffs cannot be established for a legacy installation, certify coverage only from the first known continuous boundary, or the report snapshot when none is known

  - **Name:** accuracy report \
    **Type:** context<rows: list<context<forecast: number, unit: string, evidence: number, state: string, reason: string, outcome: number, deliveries: list<number>, confirmations: list<number>>>, requested: context<start: number, end: number>, covered from: number, covered until: number, complete: boolean, confirmations covered from: number, confirmations complete: boolean> \
    **Means:** the forecast rows, requested and retained bounds, and whether counts cover the entire request. Equal covered bounds denote no certified coverage
