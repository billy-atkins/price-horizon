# Auditing the canon

The audits only the canon owes, read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each enforces and reads.

## The audits

### Agent agnostic

Run the script with `--candidates`, which lists each line naming a vendor, a model or a tool-specific path. The root `AGENTS.md` naming its opt-in helpers, and with them the tools they serve, is what `specs/methodology/scope.md § Agent Agnostic`'s exception allows, and the usual candidate to decline.

### Skill form

The script decides a registered skill's front matter and script names; the rest is read here, with each unregistered skill `--candidates` lists read against `specs/methodology/skills.md § Registered Skills`' test and the import candidates guiding the standard-library rule. What is easy to miss: a skill restating a rule it should cite, a step applying a rule with no point-of-use citation, a row of `.ai/skills/audit-specs/SKILL.md § Operating rules carried out by a step` naming a step its skill no longer has, and a row of `.ai/skills/audit-specs/SKILL.md § What the script checks` no longer describing what the script checks. Of `specs/methodology/working-files.md § The Working Files`, this audit reads its paragraph on a skill's scratch space, against what the skill's own text says of where its output goes; Working-file form reads the rest.

