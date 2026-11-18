# Auditing the canon

This file holds the audits only the canon owes. It is read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each audit enforces and reads. An `other` change also owes Agent agnostic.

## The audits

### Agent agnostic

Run the script with `--list-candidates`. It lists each line naming a vendor, a model or a tool-specific path. The reading is made as `specs/methodology/making-a-semantic-check/agent-agnostic.md § Agent Agnostic` has it.

### Skill form

The script decides a registered skill's front matter, its script names and its `## Workflow` heading. It finds a step citing each section stating operating rules. It resolves each canon-spec annotation in the skills' scripts and the code they share: the annotation's form, its target, a check's record among them, and its order. It reports each Script Check record no annotation cites, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: script-check-carried-out]` has it. `--list-candidates` lists each unregistered skill that cites the methodology's rules, each import from outside the set a script may import, each long sentence and each path into the application specs.

The rest is read as `specs/methodology/making-a-semantic-check/skill-form.md § Skill Form` has the reading made. The script takes any Workflow step citing a section stating operating rules for the step carrying its rules out, so whether the step does carry them out is read here. Among the skills' accounts of their scripts, the rows of `.ai/skills/audit-specs/SKILL.md § What the script checks` are read against what the script checks.

Of `specs/methodology/working-files/main.md § The Working Files`, this audit reads the paragraphs on a skill's scratch space and on its plans. It reads them against what the skill's text says of where the skill's output and plans go. Working-file form reads the rest.
