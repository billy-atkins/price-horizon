# Auditing application specs

This file holds the audits only the application specs owe. It is read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each audit enforces and reads.

## The audits

### Counterpart currency

Take each product file's `technical-specs` frontmatter as the map, and read both sides. Then sweep the other way, because a missing frontmatter entry is the likelier failure and the frontmatter map cannot see it. Check that each product section a technical file cites sits in a product file whose list names that technical file.

Sweep the same pairing once more, for the converse: an entry naming a technical file that cites nothing in that product file back. This sweep is a judgment rather than an arithmetic check, which is why it is easy to skip. Reading decides which of two things such an entry is:

- a file supplying context a capability depends on without implementing a promise of its own, which the list's scope allows (`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`);
- a missing citation on the technical side, which is the finding.

What settles it is whether that technical file makes any promise this product file states.

Overlap between the two sides is intended, as `specs/methodology/spec-placement.md § Product or Technical` explains. The overlap is not the finding; a side that has stopped doing its own job is.

### Scenario coverage

First find each capability section with no `Test Scenarios` block at all, since reading a block cannot reach a section that has none. Then read each block against its section's prose, both ways. Look for a promise or a guardrail with no scenario, and for a scenario asserting what the prose does not (`specs/methodology/acceptance-scenarios.md § Deciding What to Write`).

