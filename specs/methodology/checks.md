## Check

A check a skill makes is a test of the files, of the code or of a design against a rule. It is a script check or a semantic check ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) has a script decide what the files alone settle and never a judgment. A candidate list decides nothing, so it is no check of its own: it belongs to the semantic check it guides. A reading audit of `.ai/skills/audit-specs/` makes the semantic checks of the rules it enforces, over its unit.

The record type holds the checks a skill makes, and no other. An operating rule's check is the step applying it, as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) has it. The user's check is the workflow's steps in which the user reviews the work and approves it or says what should change. Neither is a script check or a semantic check, so neither takes a record.

A check's records go in a section of their own under this one, titled with the type's Plural Name, as [`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form) has a declaring section say where its records go. The skills' tables of checks hold the checks' entries until each is moved into a record. No field of a check's record states the scope a check of the files or the code runs over a design's work. [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) decides it from the check's Checked By.

Check is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), whose records give a check's fields:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Checks \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the check's name, by which a citation names its record |
| Checked By | no | yes | | "script", "semantic" | whether a script check or a semantic check makes it |
| Reads | no | yes | | "the files", "a design", "the code" | what the check reads |
| Enforces | no | yes | | text | each section it enforces, cited, separated by semicolons |
| Carried Out By | no | yes | | text | the skill and its script's flag, or its step, carrying the check out |
| Candidates | no | no | none | text | for a semantic check, the flag of the script listing places for its reading |
| Unit | no | where Reads is "the files" or "the code" | | text | the unit the audit reads at a time |
| Kinds | no | where Reads is "the files" or "the code" | | text | the kinds of change whose audit runs it, as [`specs/methodology/working-files.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files.md#the-kinds-of-change) names them, or `none`, for a check only the full run reads, as the audits table of [`.ai/skills/audit-specs/SKILL.md`](/.ai/skills/audit-specs/SKILL.md) writes it |
| Runs In | no | where Reads is "a design" | | text | each state of [`specs/methodology/design-workflow.md § The Order of a Design's Work`](/specs/methodology/design-workflow.md#the-order-of-a-designs-work) it runs in, cited |
