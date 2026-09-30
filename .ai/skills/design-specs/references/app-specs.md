# Designing application specs

The steps a change to the application specs owes beyond the Workflow of `.ai/skills/design-specs/SKILL.md`, read from its fork, in the order that Workflow reaches them. Each names the step it joins.

## Workflow

**Hand a change needing the canon to the canon —** at `.ai/skills/design-specs/SKILL.md § Workflow § Fork on the kind of specification`, or wherever the work finds a rule of Spec of Record wrong or missing: hand it to the canon as `specs/methodology/working-files.md § A Design Document` has a change needing both kinds split, to the canon design this one depends on where what is wrong is that design's change, and otherwise to a canon design document spawned for it, rather than working around the rule.

**Decide which spec it belongs to —** before `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`: `specs/methodology/spec-placement.md § Product or Technical`. Before editing a technical file, read the product files whose `technical-specs` name it, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Name its capability domain —** within `.ai/skills/design-specs/SKILL.md § Workflow § Decide its altitude, and its file`, for a product capability: `specs/methodology/spec-placement.md § Naming a Capability Domain` first, then `specs/methodology/spec-placement.md § Where a File Goes`'s test for subfolder versus root file.

**Update the scenarios in the same pass —** after `.ai/skills/design-specs/SKILL.md § Workflow § Write the text in the form the rules give it`: `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Step`, each in the form `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` gives, covering what `specs/methodology/acceptance-scenarios.md § Deciding What to Write` asks, and never standing in for a construct, per `specs/methodology/acceptance-scenarios.md § Why a Scenario Is Not a Modeling Construct`.

**Link a product file to the technical files building it —** within `.ai/skills/design-specs/SKILL.md § Workflow § Write the references`, when a technical file now fulfills a product file's capability, per `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`.

**Keep the counterpart in step —** within `.ai/skills/design-specs/SKILL.md § Workflow § Synchronize whatever restates what you changed`: a product fact and its technical mechanism name each other and change together, per `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`.

## Adding a statement changes which rules apply to it

Conventions here are often conditional. `specs/methodology/acceptance-scenarios.md § Deciding What to Write` exempts a guarantee stated *only* in a cross-cutting file from needing a scenario under each capability relying on it. Add that guarantee to a capability's own section and the condition stops holding: it is now a guardrail stated in that section, and a scenario is owed.

Before adding a sentence, check which conventions currently apply because of where the fact is *not* stated. Citing the existing statement rather than restating it usually keeps the condition intact and owes nothing further, which is also what `specs/methodology/sourcing-and-citation.md § One Home Per Fact` asks for anyway.

## Hand product decisions back

Some forks are craft and yours to settle: where content goes, how a rule is worded, whether to cite or restate.

Some are not. What the product does, who may do it, what it promises a user, are decisions about the thing being specified rather than about specifying it. Present the options and consequences, recommend one, and let the person decide. Settling these quietly inside a proposal is how a specification acquires facts nobody chose.

