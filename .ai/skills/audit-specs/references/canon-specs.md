# Auditing the canon

The audits only the canon owes, read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each enforces and reads.

## The audits

### Agent agnostic

Run the script with `--list-candidates`, which lists each line naming a vendor, a model or a tool-specific path. The root `AGENTS.md` naming its opt-in helpers, and with them the tools they serve, is what `specs/methodology/scope.md § Agent Agnostic`'s exception allows, and the usual candidate to decline.

### Skill form

The script decides a registered skill's front matter, its script names and its `## Workflow` heading, finds a step citing each operating rule, and resolves each canon-spec annotation in the skills' scripts and the code they share, its form, its target and its order; the rest is read here, with each unregistered skill `--list-candidates` lists read against `specs/methodology/skills.md § Registered Skills`' test and the import candidates guiding the standard-library rule, and the long-sentence candidates and the paths into the application specs guiding its reading of each skill for `specs/methodology/spec-style.md § Clear Prose`, as a cold agent reading it once. What is easy to miss: a skill restating a rule it should cite, a step applying a rule with no point-of-use citation, an operating rule cited under a Workflow only by steps that do not carry it out, which the script takes for the rule's steps, a row of `.ai/skills/audit-specs/SKILL.md § What the script checks` no longer describing what the script checks, a script's copy of values the canon states carrying no canon-spec annotation, and one pointing to an area its values do not come from, per `specs/methodology/skills.md § Authoring a Skill`. Of `specs/methodology/working-files.md § The Working Files`, this audit reads its paragraphs on a skill's scratch space and on its plans, against what the skill's own text says of where its output and its plans go; Working-file form reads the rest.

