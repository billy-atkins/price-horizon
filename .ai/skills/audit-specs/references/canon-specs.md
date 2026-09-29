# Auditing the canon

The audits only the canon owes, read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each enforces and reads.

## The audits

### Agent agnostic

Run the script with `--list-candidates`, which lists each line naming a vendor, a model or a tool-specific path. The root `AGENTS.md` naming its opt-in helpers, and with them the tools they serve, is what `specs/methodology/scope.md § Agent Agnostic`'s exception allows, and the usual candidate to decline.

### Skill form

The script decides a registered skill's front matter, its script names and its `## Workflow` heading, and finds a step citing each operating rule; the rest is read here, with each unregistered skill `--list-candidates` lists read against `specs/methodology/skills.md § Registered Skills`' test and the import candidates guiding the standard-library rule. What is easy to miss: a skill restating a rule it should cite, a step applying a rule with no point-of-use citation, an operating rule cited under a Workflow only by steps that do not carry it out, which the script takes for the rule's steps, and a row of `.ai/skills/audit-specs/SKILL.md § What the script checks` no longer describing what the script checks. Of `specs/methodology/working-files.md § The Working Files`, this audit reads its paragraphs on a skill's scratch space and on its plans, against what the skill's own text says of where its output and its plans go; Working-file form reads the rest.

