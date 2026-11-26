# Auditing the canon

This file holds the audits only the canon owes. It is read from the fork in `.ai/skills/audit-specs/SKILL.md`, whose audits table and scoping table name what each audit enforces and reads. An `other` change also owes Agent agnostic.

## The audits

### Agent agnostic

Run the script with `--list-candidates`. It lists each line naming a vendor, a model or a tool-specific path. The reading is made as `specs/methodology/semantic-check-methods/agent-agnostic.md § Agent Agnostic` has it.

### Skill form

The script decides a registered skill's front matter, its script names and its `## Workflow` heading. It finds a step citing each section stating operating rules. It resolves each canon-spec annotation in the skills' scripts and the code they share: the annotation's form, its target, a check's record among them, and its order. Whether each unit of the audit's own checks cites the section its row of `.ai/skills/audit-specs/SKILL.md § What the script checks` names, or its check's record, is read here. It reports each Script Check record no annotation cites, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: script-check-carried-out]` has it. `--list-candidates` lists each unregistered skill that cites the methodology's rules, each import from outside the set a script may import, each long sentence and each path into the application specs.

The script decides nothing of the kept tests or of the fixture files, and reads no fixture file. What the files alone decide of them is checked with each run of the kept tests, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests § When the Kept Tests Are Run` has those checks made. A canon-spec annotation in a kept test is among what those checks read, and this script counts none as a unit carrying a check out.

The rest is read as `specs/methodology/semantic-check-methods/skill-form.md § Skill Form` has the reading made. The script takes any Workflow step citing a section stating operating rules for the step carrying its rules out, so whether the step does carry them out is read here. Among the skills' accounts of their scripts, the rows of `.ai/skills/audit-specs/SKILL.md § What the script checks` are read against what the script checks.

This audit's Kind names `fixture-files`, so it reads the fixture files too. It reads each file of the kept tests that is no fixture file, each fixture file with the tests reading its fixtures, and the index of the fixture files, against `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests`. That method says how each is read, and how the tests reading a fixture are found. A finding of a description in the index, or of a fixture's Holds, that does not say what it describes takes the report row for a summary that disagrees with what it summarizes. Every other finding of a kept test or a fixture takes the row for any other rule broken.

Of `specs/methodology/working-files/main.md § The Working Files`, this audit reads the paragraphs on a skill's scratch space and on its plans. It reads them against what the skill's text says of where the skill's output and plans go. Working-file form reads the rest.
