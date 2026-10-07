# Spec of Record — Agent Instructions

The entry point to Spec of Record for these specifications. Read it before any work on a file in Spec of Record's scope (`specs/methodology/scope.md § What Spec of Record Governs`): it sends each change to the procedure that governs it, and holds the rules that reach every author. Read `specs/methodology/glossary.md` next, before anything else (`specs/methodology/scope.md § Progressive Disclosure`).

## Writing specs

`specs/methodology/` holds the rules for writing a specification and for the code the specs govern. Those rules, and the rules in this file, reach the files in Spec of Record's scope, the methodology's own files included, as `specs/methodology/scope.md § What Spec of Record Governs` sets.

Every change is of one of the kinds `specs/methodology/working-files.md § A Design Document § The Kinds of Change` defines: to the canon, to the application specs, to code, or to neither. `specs/methodology/working-files.md § A Design Document` also sets when a change's design document declares its kind, and how a change needing two kinds is split. A change goes to the skill for its work, and the skills for the specifications serve every kind of specification alike, each forking on the kind where the work differs:

- **Changing a specification, or another file in scope but code —** `.ai/skills/design-specs/`, whose Workflow gives each rule it applies a point-of-use citation and forks into the reference for the change's kind.
- **Checking a specification, or such a file —** `.ai/skills/audit-specs/`, whose Workflow forks the same way; a plan is checked by the skill writing it (`specs/methodology/scope.md § Rules and Skills`).
- **Designing and writing code —** `.ai/skills/implement-specs/`.
- **Checking code —** `.ai/skills/verify-spec-implementation/`.

Before doing by hand a kind of work a registered skill covers, read its `SKILL.md`.

Running the procedure, rather than recalling the rules, is what puts each rule in mind at the step it governs (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). This section's index finds a rule mid-step, whatever the work; it routes, and stands in for no step of a procedure.

| Doing this | The rule is here |
|---|---|
| Finding which files Spec of Record governs, and how to find your way through them | `specs/methodology/scope.md § What Spec of Record Governs`, `specs/methodology/scope.md § Progressive Disclosure` |
| Meeting a term Spec of Record gives a meaning of its own | `specs/methodology/glossary.md` |
| Deciding product spec versus technical spec | `specs/methodology/spec-placement.md § Product or Technical` |
| Writing a spec, or reviewing a design changing one, as its persona | `specs/methodology/spec-placement.md § Personas` |
| Deciding index, architecture, or detail file | `specs/methodology/spec-placement.md § Index, Architecture, Detail` |
| Placing a new file, or deciding whether a domain earns a subfolder | `specs/methodology/spec-placement.md § Where a File Goes` |
| Writing the technical stack or an environment | `specs/methodology/spec-placement.md § The Technical Stack`, `specs/methodology/spec-placement.md § Environments` |
| Naming a new product capability domain | `specs/methodology/spec-placement.md § Naming a Capability Domain` |
| Linking a product file to the technical files that build it | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Deciding whether a rule may be restated | `specs/methodology/sourcing-and-citation.md § One Home Per Fact` |
| Writing a citation, referring to other text, or deciding whether a citation may be written | `specs/methodology/sourcing-and-citation.md § Writing a Citation`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Adding or retitling a heading | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Describing a rule, a process, or an entity's behavior | `specs/methodology/modeling-constructs.md` |
| Recording a decision the specs rely on but have not made | `specs/methodology/spec-placement.md § An Open Question` |
| Writing a field, a bold lead-in, emphasis, literal text, or an entry of a repeated kind | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis`, `specs/methodology/modeling-constructs.md § Literal Text`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Writing or updating acceptance scenarios | `specs/methodology/acceptance-scenarios.md` |
| Removing drafting residue and hedged framing, or explaining a trade-off | `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` |
| Writing prose its primary reader understands on the first read | `specs/methodology/spec-style.md § Clear Prose` |
| Writing a number, a count, or a reference to an item | `specs/methodology/spec-style.md § Ordinals and Counts` |
| Keeping a counterpart spec, an `architecture.md` or a diagram in step | `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step` |
| Adding, changing, or re-checking a diagram | `specs/methodology/modeling-constructs.md § Diagrams`, then `.ai/skills/author-mermaid-diagram/` |
| Recording a proposed change, a steer given it, or work to take up later | `specs/methodology/working-files.md § A Design Document`, `specs/methodology/working-files.md § A Steering Decision`, `specs/methodology/working-files.md § A Follow-up` |
| Refactoring and refining specs that have landed, the canon's or the application's | `specs/methodology/glossary.md`, `§ Design, Refactor, Refine`, then `.ai/skills/design-specs/` |
| Setting up the agent in use to apply a review's reasoning effort | `specs/methodology/skills.md § Setting Up an Agent`, then `.ai/skills/configure-spec-of-record/` |
| Registering or authoring a skill | `specs/methodology/skills.md § Registered Skills`, `specs/methodology/skills.md § Authoring a Skill` |
| Adding or changing a rule, and the check enforcing it | `specs/methodology/scope.md § Rules and Skills` |
| Writing an instruction any agent can follow | `specs/methodology/scope.md § Agent Agnostic` |
| Checking that the code carries out its specs | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § The Technical Stack`, then `.ai/skills/verify-spec-implementation/` |
| Designing and writing the code the application specs govern | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § Personas`, `specs/methodology/spec-placement.md § A Product Module`, `specs/methodology/spec-placement.md § Environments`, `specs/methodology/working-files.md § A Design Document § A Design Changing Code`, then `.ai/skills/implement-specs/` |

## Design, Refactor, Refine

How anything here gets built or reworked, whether a spec, a rule, a skill, or code. The builder takes it through the process this section sets, and a cold agent then runs its own adversarial review over the result. `.ai/skills/design-specs/` applies it to the canon and the application specs, and `.ai/skills/implement-specs/` to code.

**Read fresh before any work —** before working on a file, however small the change or recent the last read, read it again, direct edits included. Nothing tells an agent whether its memory of a file survived compaction, and content written an hour ago feels remembered when it is a reconstruction.

**The design frame comes first —** before drafting, the builder states the change's design frame (`specs/methodology/glossary.md`) and presents it to the user, drafting only once the user agrees or adjusts it, the answer recorded as a steer (`specs/methodology/working-files.md § A Steering Decision`). A frame the user never saw lets the builder solve a problem the user does not have. Its scope, the cases the change governs, is the actual scope of the change. Too small a scope reaches a local optimum, right for the file in hand and wrong for the system around it; only the real scope admits the global one. Widen it until nothing outside it would change the answer, and sweep for it by meaning as well as by the draft's own words: a search built from the draft's terms finds only what the draft already knew about. Its outcomes are settled before the draft, so the draft is judged by them rather than the outcomes being fitted to the draft.

- **Design —** start from the problem to solve, stated plainly, and get it logically working: a draft that solves it correctly, before it is good. The draft is described in a plan: for the specifications and for code, a design document. A change of its own that the work turns up is spawned as a design of its own or logged as a follow-up, as the user decides (`specs/methodology/working-files.md § A Design Document`).
- **Refactor —** macro improvements to its internal workings and its external surface: structural changes, not wording, that make it better meet its actual needs and work toward elegance (`specs/methodology/glossary.md`). Repeat until it converges, when a round leaves the structure where it was.
- **Refine —** once Refactor has converged, make its elegance plain and make it easy to use and to understand: wording, naming, phrasing, consistency. Polishing something still moving structurally is wasted effort.

**Measure twice, cut once —** the builder and its reviewers pull against each other, as a software engineer and a quality assurance engineer do. The builder aims to hand a review nothing to find. The reviewer, in the adversarial review, the validation review and the audit alike, aims to find what the builder missed. That tension is what makes the work good, and it holds only while the builder does its part: quality comes from the builder's own passes, and the reviewers are a second set of eyes, never the first check. Fast and sloppy is slow, since each finding a reviewer makes sends the work back through the builder's process and can cost another review; methodical and correct is fast. So the builder:

- reads the text an edit changes, and what surrounds it, before putting the edit in its plan;
- holds each edit to the rules it applies, as it works;
- checks the whole of the work, not only what it last changed, after its own last edit and before any review.

**The adversarial review —** when the builder judges the work optimal, the cold agent is given the builder's complete plan: the problem, the design frame and the design, each stated on its own, and the steers that settled it (`specs/methodology/working-files.md § A Steering Decision`). It is never the builder, since re-reading your own work re-reads what you meant. It does not derive its own solution: it takes the builder's design through Design, Refactor, Refine again, looking for Rube Goldberg machines and Potemkin villages (`specs/methodology/glossary.md`). It reports findings; it does not edit.

Brief it with more than the task:

- name the failure patterns earlier rounds found;
- point it at the steers the plan records, the user's decisions about what the design is, so it checks fidelity to them rather than reopening them (`specs/methodology/working-files.md § A Steering Decision`);
- ask for any sweep of the repo to be redone by its own method;
- point it at whatever the design decides, since that is where defects concentrate.

The builder checks every finding against the files before acting on it, since a review can be confidently wrong. The user decides which findings are addressed and how. Accepted findings go back through the builder's process, and if they changed the structure, the revised design gets another adversarial review. Then, with the user's go-ahead, the builder applies the work and a cold agent audits it, the post-apply audit: for specs `.ai/skills/audit-specs/`, and for code `.ai/skills/verify-spec-implementation/` (`specs/methodology/working-files.md § A Design Document § A Design Changing Code`).

**Converging, or not —** a hard problem can take many review rounds, and each phase counts its own: the adversarial reviews of a design before it is approved, and the audits of its applied work after. A flaw is a finding the user settles as the design, or the approach to it, being wrong; a tactical fix is no flaw, and a round may find several flaws. Before revising the design for a flaw an adversarial review finds, the builder asks whether its design frame let the flaw in, its scope missing a case, its approach not reaching it or its outcomes not judging it; where it did, the builder revises the frame first, and has the user agree or adjust it again before the design is revised. Three rounds in a row within one phase that each found a flaw mean the work is not converging, and that the design or its approach is itself flawed. The builder then stops revising and takes it to the user, and the two step back and reassess: they rescope, split or abandon the design, and start afresh with what was learned.

**Each review's model and effort —** the adversarial review and the post-apply audit each run on a model and at a reasoning effort (`specs/methodology/glossary.md`) that the user chooses before the review starts, as separate choices. The effort is light, medium or high. By default, a review runs on the model the agent runs on, at medium effort. A model other than the agent's own can see past a blind spot a reviewer on the same model would share, and a higher effort costs more; neither changes the review's scope or its brief. A level is applied as the nearest the agent offers, through the reviewer definition the agent was set up with for it where it needs one (`specs/methodology/skills.md § Setting Up an Agent`), and a choice the agent cannot apply runs as the agent allows. The review's pass in the plan names the model and effort it ran on, per `specs/methodology/working-files.md § A Design Document`.

**Direct edits —** a small tactical edit, narrow in scope and low in risk, may skip this process and be applied directly, but only once the user has approved it. Anything larger or riskier goes through the process.

**A new branch —** is created only once the user approves it, the builder proposing its name and what it starts from. How work is split across branches decides how it is reviewed and merged, which is the user's to settle, as a direct edit is.
