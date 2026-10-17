---
technical-specs:
  - specs/application/technical/control-plane-service/control-plane.md
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
---

## Audit Log Visibility

[`specs/application/product/logging-and-traceability.md § Logging and Traceability § Audit Log`](/specs/application/product/logging-and-traceability.md#audit-log) defines the audit log: what it is, and why it is kept separate from an application log or an answer's own lineage. This capability is how the Control plane admin and the Identity admin ([`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)) see it.

A Control plane admin can see, at any time, who has done what within the admin's own business unit:

- Acme AI's access
- every configuration change made to the business unit's settings, and who made it
- the business unit's Query users' questions and what was returned to them, the positioning options, simulated outcomes, and exact narrative wording alike

The admin sees the positioning options, simulated outcomes and exact narrative wording in full, not only a reference that leaves the admin to take Acme AI's word for what it said.

Every Control plane admin also sees each change the client's own infrastructure team makes to which kinds of model call reach a frontier model provider ([`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology § Frontier Models`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#frontier-models)), with the kinds named before and after it. This holds whichever business unit the admin administers, since the choice reaches every business unit.

An Identity admin sees, across the installation, every change to who is granted which business unit and role, and who made it. The Identity admin also sees every question refused because its asker has access to no business unit at all. A change to access to a business unit is also among the changes that business unit's Control plane admin sees. A change to who holds the Platform admin role is seen by every Control plane admin.

This record never shows the underlying protected content beneath any of that. A competitor's pricing data, a document's content, or a credential never appears in the record itself.

The record covers every access Acme AI takes through PriceHorizon's own systems. That includes Acme AI's engineers reading the application log in the observability viewer shipped alongside PriceHorizon, where a client runs no observability system of its own. A business unit may instead grant Acme AI a scoped credential into the business unit's own external observability platform, to triage a specific issue using application log detail forwarded there. That access happens entirely outside PriceHorizon and does not appear here. The same residency choice that keeps that data off Acme AI's infrastructure in the first place also puts the record of that access outside what this audit log can promise to cover. Scoping that grant to what the issue needs, rather than to a standing account, is the business unit's responsibility to hold. It is the same discipline the business unit would apply to its own workforce's access to its own tools.

Reviewing this record at scale means finding one entry, not reading every one. A Control plane admin narrows the record by who took the action, what kind of action it was, and a specific window of time. For the business unit's own Query users' questions, the admin can also narrow it by which competitor or geography the question concerned. A filter matching nothing states so plainly, rather than looking broken or stuck loading. A day-by-day count of matching entries across the selected window surfaces a pattern, such as an unusual cluster of activity, before anyone has had to read a single row to notice it. Opening any entry shows its full detail without losing the current filter.

The filtered set, exactly the entries matching, can be exported to hand to a security or compliance reviewer of the client's own. That reviewer needs no PriceHorizon access to receive it. The export never carries the exact narrative wording or the positioning-and-simulation figures a Query user saw. Only the fact of what happened and a reference to the forecast behind it travel with the export. The wording and figures stay viewable in the product, never inside a file that leaves it.

A Control plane admin can also see, read-only, how long this record is currently kept for the installation. Raising that period further is a contractual matter Acme AI governs, not a self-service setting. This is the same distinction already drawn for the archetype rules and weighting rubrics behind every forecast.

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
