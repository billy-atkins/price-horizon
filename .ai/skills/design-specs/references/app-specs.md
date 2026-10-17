# Designing application specs

These are the steps a change to the application specs owes beyond the Workflow of `.ai/skills/design-specs/SKILL.md`. They are read from that Workflow's fork, in the order the Workflow reaches them. Each names the step it joins.

## Workflow

**Hand a change needing the canon to the canon.** At `.ai/skills/design-specs/SKILL.md § Workflow § Fork on the kind of specification`, or wherever the work finds a rule of Spec of Record wrong or missing, hand what the canon needs to the canon rather than working around the rule. Hand it on as `specs/methodology/working-files.md § A Design Document` has a change needing both kinds split. Where what is wrong is a change that a canon design this one depends on makes, hand it to that design. Otherwise hand it to a canon design document spawned for it.

**Decide which spec it belongs to.** Before `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`, decide it by `specs/methodology/spec-placement.md § Product or Technical`. Before editing a technical file, read the product files whose `technical-specs` name it, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Name its capability domain.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`, for a product capability, apply `specs/methodology/spec-placement.md § Naming a Capability Domain` first. Then apply the test in `specs/methodology/spec-placement.md § Where a File Goes` for subfolder versus root file.

**Record an abbreviation the application coins.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Write the text in the form the rules give it`, record it once, beside its term's definition, and nowhere else, per `specs/methodology/glossary.md § Using an Abbreviation`.

**Update the scenarios in the same pass.** After `.ai/skills/design-specs/SKILL.md § Workflow § Write the text in the form the rules give it`, update them as `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Sync` has it. Write each in the form `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` gives, covering what `specs/methodology/acceptance-scenarios.md § Deciding What to Write` asks. A scenario never stands in for a construct, per `specs/methodology/acceptance-scenarios.md § Why a Scenario Is Not a Modeling Construct`.

**Link a product file to the technical files building it.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Write the references`, link them when a technical file now fulfills a product file's capability, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Keep the counterpart in sync.** Within `.ai/skills/design-specs/SKILL.md § Workflow § Synchronize whatever restates what you changed`, a product spec and its technical counterpart name each other and stay aligned, per `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`.

## Adding a statement changes which rules apply to it

Conventions here are often conditional. `specs/methodology/acceptance-scenarios.md § Deciding What to Write` exempts a guarantee stated *only* in a cross-cutting file from needing a scenario under each capability relying on it. Add that guarantee to a capability's own section and the condition stops holding. The guarantee is now a promise or a guardrail stated in that section, and a scenario is owed.

Before adding a sentence, check which conventions currently apply because of where the fact is *not* stated. Citing the existing statement rather than restating it usually keeps the condition intact and owes nothing further. Citing it is also what `specs/methodology/sourcing-and-citation.md § One Home Per Fact` asks for.

## Hand product decisions back

Some forks are craft and yours to settle: where content goes, how a rule is worded, whether to cite or restate.

Some are not. The decisions about the thing being specified are the user's, per `specs/methodology/spec-placement.md § Personas`. Present the options and their consequences, recommend one, and let the user decide. Settling these quietly inside a proposal is how a specification acquires facts nobody chose.
