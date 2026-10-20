# Designing application specs

These are the steps a change to the application specs owes beyond the Workflow of `.ai/skills/design-specs/SKILL.md`. They are read from that Workflow's fork, in the order the Workflow reaches the last step each joins. Each names the step it joins, or, where it decides and writes, the deciding step and the writing step.

## Workflow

**Hand a change needing the canon to the canon.** At `.ai/skills/design-specs/SKILL.md § Workflow § Fork on the kind of specification`, or wherever the work finds a rule of Spec of Record wrong or missing, hand what the canon needs to the canon rather than working around the rule. Hand it on as `specs/methodology/working-files.md § A Design Document` has a change needing both kinds split. Where what is wrong is a change that a canon design this one depends on makes, hand it to that design. Otherwise hand it to a canon design document spawned for it. Either way, this design names that canon design in its Depends On and states in its frame's Scope what it relies on from it (`specs/methodology/working-files.md § A Design Document`).

**Decide which spec it belongs to.** Before `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`, decide it by `specs/methodology/spec-placement.md § Product or Technical`. Before stating a change to a technical file, read the product files whose `technical-specs` name it, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Name its capability domain.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`, for a product capability, apply `specs/methodology/spec-placement.md § Naming a Capability Domain` first. Then apply the test in `specs/methodology/spec-placement.md § Where a File Goes` for subfolder versus root file.

**Update the scenarios in the same pass.** Within `.ai/skills/design-specs/SKILL.md § Workflow § State each step as its outcome`, state in a step's Objectives each scenario the change adds or changes, covering what `specs/methodology/acceptance-scenarios.md § Deciding What to Write` asks, so a scenario keeps in step with its prose as `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Sync` has it. Within `.ai/skills/design-specs/SKILL.md § Workflow § Write the text in the form the rules give it`, write each in the form `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` gives. A scenario never stands in for a construct, per `specs/methodology/acceptance-scenarios.md § Why a Scenario Is Not a Modeling Construct`.

**Record an abbreviation the application coins.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Write the text in the form the rules give it`, record it once, beside its term's definition, and nowhere else, per `specs/methodology/glossary.md § Using an Abbreviation`.

**Link a product file to the technical files building it.** Within `.ai/skills/design-specs/SKILL.md § Workflow § State each step as its outcome`, name in the step's What and in the Target each product file whose capability a technical file the step changes now fulfills. Within `.ai/skills/design-specs/SKILL.md § Workflow § Write the references`, link them, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Keep the counterpart in sync.** Within `.ai/skills/design-specs/SKILL.md § Workflow § State each step as its outcome`, name in the step's What and in the Target the counterpart of each spec the step changes. Within `.ai/skills/design-specs/SKILL.md § Workflow § Synchronize whatever restates what you changed`, keep a product spec and its technical counterpart naming each other and aligned, per `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`.

## Adding a statement changes which rules apply to it

Conventions here are often conditional. `specs/methodology/acceptance-scenarios.md § Deciding What to Write` exempts a guarantee stated *only* in a cross-cutting file from needing a scenario under each capability relying on it. Add that guarantee to a capability's own section and the condition stops holding. The guarantee is now a promise or a guardrail stated in that section, and a scenario is owed.

Before adding a sentence, check which conventions currently apply because of where the fact is *not* stated. Citing the existing statement rather than restating it usually keeps the condition intact and owes nothing further. Citing it is also what `specs/methodology/sourcing-and-citation.md § One Home Per Fact` asks for.

## Hand product decisions back

Some forks are craft and yours to settle: where content goes, how a rule is worded, whether to cite or restate.

Some are not. The decisions about the thing being specified are the user's, per `specs/methodology/spec-placement.md § Personas`. Present the options and their consequences, recommend one, and let the user decide. Settling these quietly inside a proposal is how a specification acquires facts nobody chose.
