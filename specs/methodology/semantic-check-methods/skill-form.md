## Skill Form

This check reads each skill for its form, and reads the checks the canon records.

The reader reads:
- **Each skill no registry row names.** Against the test of [`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills).
- **Each script's imports.** Against the standard-library rule of [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill), with any list of imports as a guide.
- **Each rule a skill states.** The reader says what kind of rule it is, by [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills). It may be a rule the skill keeps: an operating rule no other skill needs. It may be a canon rule the skill restates, which the skill should cite. Or it may be a rule in the wrong place: one that decides what the specs or the code hold, or one more than one skill needs. Each rule in the wrong place is a finding.
- **Each rule a skill keeps.** The reader confirms the rule names its check beside it, as [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill) has a kept rule name it. A kept rule that names none is a finding.
- **Each skill, once, as a cold agent.** Against [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose), with any list of long sentences and of paths into the application specs as a guide.
- **The checks standing under each section.** Whether, between them, they cover each of the section's rules, as [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills) has them. Whether each check falls in one area, the area of the rule it enforces, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has it.
- **Each place that names a check standing as a record.** [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has such a place cite the record. The places are a skill's step, a state of [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-order-of-a-designs-work), and the Runs of a Check Role record of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles`](/specs/AGENTS.md#check-roles).
- **Where a skill says its output and its plans go.** Against the paragraphs of [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) on a skill's scratch space and on its plans.

What is easy to miss, each against [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill):
- a spelling or a usage that is not American English, in a skill's text or in its scripts' comments and messages. [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose) has both written in it. One in a quotation, a title or a name from outside the specs is no finding;
- a skill restating a rule it should cite;
- a step that applies a rule and gives it no point-of-use citation;
- a section stating operating rules that a Workflow cites only from steps that do not carry those rules out;
- a skill's description of what its script does that is no longer true of the script;
- a script's copy of values the canon states that carries no canon-spec annotation, or one whose annotation points to an area the values do not come from;
- an annotation that cites a check its unit does not carry out.
