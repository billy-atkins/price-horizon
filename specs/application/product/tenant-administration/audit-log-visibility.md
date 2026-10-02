---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
---

## Audit Log Visibility

The audit log itself, what it is and why it is kept separate from an application log or an answer's own lineage, is `specs/application/product/logging-and-traceability.md § Logging and Traceability § Audit Log`; this is the Control plane admin's and the Identity admin's (`specs/application/product/roles.md § Roles`) own capability to see it.

A Control plane admin can see who has done what within their own business unit at any time: Acme AI's own access, every configuration change made to their own business unit's settings and who made it, and their own Query users' questions and what was actually returned to them, the positioning options, simulated outcomes, and exact narrative wording alike, not just a reference requiring them to take Acme AI's word for what it said. Every Control plane admin also sees each change the client's own infrastructure team makes to which kinds of model call reach a frontier model provider (`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology § Frontier Models`), with the kinds named before and after it, whichever business unit they administer, since the choice reaches every one. An Identity admin sees every change to who is granted which business unit and role, across the installation, and who made it, and every question refused because its asker has access to no business unit at all; a change to access to a business unit is also among that business unit's own changes its Control plane admin sees, and a change to who holds the Platform admin role is seen by every Control plane admin. What's never shown is the underlying protected content beneath any of that, a competitor's own pricing data, a document's own content, or a credential, never appears in this record itself.

This covers every access Acme AI takes through PriceHorizon's own systems, including its engineers reading the application log in the observability viewer shipped alongside PriceHorizon, where a client runs no observability system of its own. If a business unit instead grants Acme AI a scoped credential into their own external observability platform to triage a specific issue using application log detail forwarded there, that access happens entirely outside PriceHorizon and does not appear here, the same residency choice that keeps that data off Acme AI's own infrastructure in the first place also puts its own access record outside what this audit log can promise to cover; scoping that grant to what the issue actually needs, rather than a standing account, is the business unit's own responsibility to hold, the same discipline they would apply to their own workforce's access to their own tools.

Reviewing this record at scale means finding one entry, not reading every one. A Control plane admin narrows it by who took the action, what kind of action it was, and a specific window of time, and, for their own Query users' questions, which competitor or geography the question concerned; a filter matching nothing states so plainly, rather than looking broken or stuck loading. A day-by-day count of matching entries across the selected window surfaces a pattern, an unusual cluster of activity, before anyone has had to read a single row to notice it. Opening any entry shows its own full detail without losing the current filter. The filtered set itself, exactly the entries actually matching, can be exported to hand to a security or compliance reviewer of the client's own, without that reviewer needing PriceHorizon access of their own to receive it, though the export never carries the exact narrative wording or the positioning-and-simulation figures a Query user actually saw, only the fact of what happened and a reference to the forecast behind it travel with the export; the wording and figures themselves stay viewable in the product, never inside a file that leaves it. A Control plane admin can also see how long this record is currently being kept for their own installation, read-only, since raising it further is a contractual matter Acme AI governs, not a self-service setting, the same distinction already drawn for the archetype rules and weighting rubrics behind every forecast.

### Test Scenarios

```gherkin
Scenario: A Control plane admin can see Acme AI's own access to their business unit at any time.
  Given Acme AI's Platform admin staff has accessed North America Snacks for a support session
  When a Control plane admin for North America Snacks reviews the audit log
  Then the admin sees who accessed it, what kind of action it was, and when
  And the admin does not see the content of what was viewed, since none is recorded

Scenario: A Control plane admin can see which of their own Query users asked what, and what they were told.
  Given a Query user for North America Snacks has asked where Competitor Brand's effective price will be in Texas in 6 months, and received an answer including positioning options and simulated outcomes
  When a Control plane admin for North America Snacks reviews the audit log
  Then the admin sees who asked, when, which forecast was actually returned, the positioning options and simulated outcomes actually shown, and the exact narrative text the Query user was shown
  And the underlying forecast's own substance is shown by a reference to that forecast, not a duplicate of its values

Scenario: A Control plane admin can see who changed a configuration setting, and what it changed from and to.
  Given a Control plane admin for North America Snacks lowered the materiality threshold for North America Snacks last week
  When a Control plane admin for North America Snacks reviews the audit log
  Then the admin sees who made the change, which setting it was, its previous value, its new value, and when it happened

Scenario: An Identity admin can see every change to who is granted access.
  Given an Identity admin mapped the IdP group EU-Pricing-Analysts to the Query user role for Europe Beverages yesterday
  When an Identity admin reviews the audit log
  Then the Identity admin sees who made the change, the business unit and role it granted, and when

Scenario: An Identity admin sees a question refused because its asker has no business unit access.
  Given a person signed in through the customer's identity provider, with no IdP group mapped to any business unit, asked a question yesterday and was refused
  When an Identity admin reviews the audit log
  Then the Identity admin sees who asked, that the question was refused, and when

Scenario: A change to access for one business unit is not shown to another business unit's admin.
  Given an Identity admin mapped the IdP group EU-Pricing-Analysts to the Query user role for Europe Beverages yesterday
  When a Control plane admin for Europe Beverages and a Control plane admin for North America Snacks each review their audit log
  Then the Europe Beverages admin sees the change
  And the North America Snacks admin does not

Scenario: Every Control plane admin sees a change to who holds the Platform admin role.
  Given an Identity admin mapped the IdP group Acme-Support to the Platform admin role yesterday
  When a Control plane admin for North America Snacks reviews the audit log
  Then the admin sees who made the change, the role it granted, and when

Scenario: Filtering narrows the audit log to a specific actor and time window.
  Given North America Snacks' audit log has entries spanning more than a year, including several from a specific Platform admin support engagement last month
  When a Control plane admin for North America Snacks filters by that Platform admin's own access and last month's date range
  Then only entries matching both the actor and the time range are shown

Scenario: A cluster of activity is visible before reading individual entries.
  Given a Control plane admin for North America Snacks lowered several configuration settings within the same hour last week
  When a Control plane admin for North America Snacks reviews the audit log for that week
  Then the day-by-day view shows that hour's cluster of configuration_changed entries as a visible spike
  And the admin does not need to open each entry individually to notice the cluster

Scenario: A filter matching nothing says so plainly.
  Given no configuration_changed entry exists for North America Snacks in the past 24 hours
  When a Control plane admin for North America Snacks filters the audit log to configuration_changed entries in the past 24 hours
  Then the view states plainly that no entries match
  And the view is not shown as broken or left loading indefinitely

Scenario: Exporting the audit log produces exactly the filtered rows, not a sample.
  Given a Control plane admin for North America Snacks has filtered the audit log to a specific date range
  When the admin exports the filtered audit log
  Then the export contains every entry matching that filter
  And no entry outside the filtered range is included

Scenario: Exporting the audit log never carries the protected content it references.
  Given a Query user for North America Snacks asked a question and received an answer with narrative text and positioning and simulation figures
  When a Control plane admin for North America Snacks exports that entry as part of a filtered audit log
  Then the export includes who asked, when, and a reference to the forecast returned
  And the export does not include the narrative text or the positioning and simulation figures themselves

Scenario: A Control plane admin can see how long their own audit log is retained, without being able to shorten it.
  Given North America Snacks' installation retains its audit log for the default one-year period
  When a Control plane admin for North America Snacks views the audit log's retention setting
  Then the admin sees the currently configured retention period
  And the admin has no self-service way to lower it

Scenario: Acme AI reading the application log in the viewer shipped alongside PriceHorizon is recorded.
  Given North America Snacks' installation runs no observability system of its own, so its application log goes to the viewer shipped alongside PriceHorizon
  When a Platform admin reads that application log in the viewer
  Then a Control plane admin for North America Snacks sees that access in the audit log, who made it, and when

Scenario: Acme AI's scoped access to a client's own external observability platform is outside this record.
  Given North America Snacks has granted Acme AI's Platform admin staff a scoped credential into North America Snacks' own external observability platform to triage a specific issue using forwarded application log detail, entirely outside PriceHorizon
  When a Control plane admin for North America Snacks reviews the audit log
  Then that access does not appear in the audit log, since it never touched PriceHorizon at all

Scenario: Every Control plane admin can see a change to which kinds of model call reach a frontier model provider.
  Given the client's own infrastructure team has named rendering an explanation for a frontier model provider in the installation's configuration
  When a Control plane admin for Europe Beverages, in the same installation, reviews the audit log
  Then the admin sees the change, with the kinds named before and after it, and that the client's own infrastructure team made it
```
