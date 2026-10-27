# Auditing the canon

This file holds the audits only the canon owes. It is read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each audit enforces and reads. An `other` change also owes Agent agnostic.

## The audits

### Agent agnostic

Run the script with `--list-candidates`. It lists each line naming a vendor, a model or a tool-specific path. The usual candidate to decline is the root `AGENTS.md` naming its opt-in helpers, and with them the tools they serve. That is what `specs/methodology/scope.md § Agent Agnostic`'s exception allows.

### Skill form

The script decides a registered skill's front matter, its script names and its `## Workflow` heading. It finds a step citing each section stating operating rules. It resolves each canon-spec annotation in the skills' scripts and the code they share: the annotation's form, its target, a check's record among them, and its order. It reports each Script Check record no annotation cites, as `specs/methodology/skills.md § Authoring a Skill § Script Checks [Name: script-check-carried-out]` has it. The rest is read here. Read each unregistered skill `--list-candidates` lists against `specs/methodology/skills.md § Registered Skills`' test. Let the import candidates guide the reading for the standard-library rule. Read each skill as a cold agent reading it once, for `specs/methodology/spec-style.md § Clear Prose`. The long-sentence candidates and the paths into the application specs guide that reading. Read whether the checks standing under a section hold to each of its rules between them, as `specs/methodology/scope.md § Rules and Skills` has them, and whether each check falls in one area, the area of the rule it holds to, as `specs/methodology/checks.md § The Areas of Checking` has it. Read each skill's step, each state of `specs/methodology/design-workflow.md § The Order of a Design's Work` and each row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why` that names a check standing as a record. Each cites that record, as `specs/methodology/checks.md § Check` has a check named where it runs.

What is easy to miss, as `specs/methodology/skills.md § Authoring a Skill` has it:
- a spelling or a usage American English replaces, in a skill's text or in its scripts' comments and messages, which no script lists, though one in a quotation, a title or a name from outside the specs is no finding;
- a skill restating a rule it should cite;
- a step applying a rule with no point-of-use citation;
- a section stating operating rules cited under a Workflow only by steps that do not carry its rules out, which the script takes for the section's steps;
- a row of `.ai/skills/audit-specs/SKILL.md § What the script checks` no longer describing what the script checks;
- a script's copy of values the canon states carrying no canon-spec annotation, and one pointing to an area its values do not come from;
- an annotation citing a check its unit does not carry out.

Of `specs/methodology/working-files.md § The Working Files`, this audit reads the paragraphs on a skill's scratch space and on its plans. It reads them against what the skill's text says of where the skill's output and plans go. Working-file form reads the rest.
