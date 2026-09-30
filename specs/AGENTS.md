# Spec of Record — Agent Instructions

The entry point to Spec of Record for these specifications. Read it before any work under `specs/`, with a skill the method registers, or on a working file: it sends each change to the procedure that governs it, and holds the rules that reach every author. Read `specs/methodology/glossary.md` next, before anything else (`specs/methodology/scope.md § Progressive Disclosure`).

## Writing specs

`specs/methodology/` holds the rules for writing a specification, which apply to every file in Spec of Record's scope (`specs/methodology/scope.md § What Spec of Record Governs`), its own files included, and so do the rules in this file.

Every change is to the canon, to the application specs, or to neither, the kinds `specs/methodology/working-files.md § A Design Document` defines, and its design document says which before any file is edited, a change needing both kinds being split into a canon design and the application work it leaves; a direct edit, which needs no design document, is of a kind all the same (`§ Design, Refactor, Refine (DRR)`). The same two skills serve every kind, each forking on it where the work differs:

- **Changing a specification —** `.ai/skills/design-specs/`, whose Workflow gives each rule it applies a point-of-use citation and forks into the reference for the change's kind.
- **Checking one —** `.ai/skills/audit-specs/`, whose Workflow forks the same way.

Before doing by hand a kind of work a registered skill covers, read its `SKILL.md`.

Running the procedure, rather than recalling the rules, is what puts each rule in mind at the step it governs (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). This section's index finds a rule an author of application specs applies, mid-step; it routes, and stands in for no step of a procedure.

| Doing this | The rule is here |
|---|---|
| Finding which files Spec of Record governs, and how to find your way through them | `specs/methodology/scope.md § What Spec of Record Governs`, `specs/methodology/scope.md § Progressive Disclosure` |
| Meeting a term Spec of Record gives a meaning of its own | `specs/methodology/glossary.md` |
| Deciding product spec versus technical spec | `specs/methodology/spec-placement.md § Product or Technical` |
| Deciding index, architecture, or detail file | `specs/methodology/spec-placement.md § Index, Architecture, Detail` |
| Placing a new file, or deciding whether a domain earns a subfolder | `specs/methodology/spec-placement.md § Where a File Goes` |
| Naming a new product capability domain | `specs/methodology/spec-placement.md § Naming a Capability Domain` |
| Linking a product file to the technical files that build it | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Deciding whether a rule may be restated | `specs/methodology/sourcing-and-citation.md § One Home Per Fact` |
| Writing a citation, referring to other text, or deciding whether a citation may be written | `specs/methodology/sourcing-and-citation.md § Writing a Citation`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Adding or retitling a heading | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Describing a rule, a process, or an entity's behavior | `specs/methodology/modeling-constructs.md` |
| Recording a decision the specs rely on but have not made | `specs/methodology/spec-placement.md § An Open Question` |
| Writing a field, a bold lead-in, emphasis, literal text, or an entry of a repeated kind | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis`, `specs/methodology/modeling-constructs.md § Literal Text`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Writing or updating acceptance scenarios | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Removing drafting residue and hedged framing | `specs/methodology/spec-style.md § What a Finished Spec Reads Like` |
| Keeping a counterpart spec, an `architecture.md` or a diagram in step | `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step` |
| Adding, changing, or re-checking a diagram | `specs/methodology/modeling-constructs.md § Diagrams`, then `.ai/skills/author-mermaid-diagram/` |
| Recording a proposed change, a steer given it, or work to take up later | `specs/methodology/working-files.md § A Design Document`, `specs/methodology/working-files.md § A Steering Decision`, `specs/methodology/working-files.md § A Follow-up` |
| Setting up the agent in use to apply a review's reasoning effort | `specs/methodology/skills.md § Setting Up an Agent`, then `.ai/skills/configure-spec-of-record/` |

## Ordinals and Counts

Avoid numbers that add nothing a reader cannot already see but create friction when the set changes. A number restating a list's order or its size goes stale silently the moment an item is added or moved, and so does everything that refers to it. Say what things are, what they mean, or cite where they are; whoever needs a count can count them when they do the work.

- Nothing is numbered: not a heading, a bold lead-in, or a list item.
- Nothing refers to an item by its position, by number or by word ("step 5", "the second", "the latter"). Refer to it by its name.
- Nothing says how many things a list or the repo holds. Name them, describe them, or cite them.

Numbers that carry value stay. Algorithm and Decision Tree tables keep their numbered steps, and references to those steps, because that numbering is an industry standard a cold agent reads without further instruction, as a software engineer would (`specs/methodology/modeling-constructs.md`). A Gherkin scenario states its own test case in full, and its numbers are that case's data. A value is not a count: a two-week window, a floor of two options, exactly one home. Neither is naming a pair, "both", "either" or "the two". Where something sits on the page is no count, and no way to refer to it either: other text is cited (`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`).

## Design, Refactor, Refine (DRR)

How anything here gets built or reworked, whether a spec, a rule, a skill, or code. The builder takes it through the process this section sets, and a cold agent then runs its own adversarial DRR over the result. `.ai/skills/design-specs/` applies it to the canon and the application specs.

**Read fresh before any work —** before working on a file, however small the change or recent the last read, read it again, direct edits included. Nothing tells an agent whether its memory of a file survived compaction, and content written an hour ago feels remembered when it is a reconstruction.

**Scope comes first —** determine the actual scope of the change before drafting it. Too small a scope reaches a local optimum, right for the file in hand and wrong for the system around it; only the real scope admits the global one. Widen it until nothing outside it would change the answer, and sweep for it by meaning as well as by the draft's own words: a search built from the draft's terms finds only what the draft already knew about.

- **Design —** start from the problem to solve, stated plainly, and get it logically working: a draft that solves it correctly, before it is good. The draft is described in a plan, for the specifications a design document, and a change of its own that the work turns up is spawned as a design of its own or logged as a follow-up, as the user decides (`specs/methodology/working-files.md § A Design Document`).
- **Refactor —** macro improvements to its internal workings and its external surface: structural changes, not wording, that make it better meet its actual needs and work toward elegance (`specs/methodology/glossary.md`). Repeat until it converges, when a round leaves the structure where it was.
- **Refine —** once Refactor has converged, make its elegance plain and make it easy to use and to understand: wording, naming, phrasing, consistency. Polishing something still moving structurally is wasted effort.

**The adversarial DRR —** when the builder judges the work optimal, the cold agent is given the builder's complete plan: the problem and the design, each stated on its own, and the steers that settled it (`specs/methodology/working-files.md § A Steering Decision`). It is never the builder, since re-reading your own work re-reads what you meant. It does not derive its own solution: it takes the builder's design through Design, Refactor and Refine again, looking for Rube Goldberg machines and Potemkin villages (`specs/methodology/glossary.md`). It reports findings; it does not edit.

Brief it with more than the task: name the failure patterns earlier rounds found, point it at the steers the plan records, the decisions the user has settled, so it checks fidelity to them rather than reopening them, ask for any sweep of the repo to be redone by its own method, and point it at whatever the design decides, since that is where defects concentrate.

The builder checks every finding against the files before acting on it, since a review can be confidently wrong. The user steers which findings are addressed and how. Accepted findings go back through the builder's process, and if they changed the structure, the revised design gets another adversarial DRR. Then, with the user's go-ahead, the builder applies the work and a cold agent audits it, which for specs means `.ai/skills/audit-specs/`.

**Each review's model and effort —** the adversarial DRR and the post-apply audit each run on a model and at a reasoning effort (`specs/methodology/glossary.md`), light, medium or high, that the user chooses before the review starts, as separate choices, the model the agent runs on and medium effort being the defaults. A model other than the agent's own can see past a blind spot a reviewer on the same model would share, and a higher effort costs more; neither changes the review's scope or its brief. A level is applied as the nearest the agent offers, through the reviewer definition the agent was set up with for it where it needs one (`specs/methodology/skills.md § Setting Up an Agent`), and a choice the agent cannot apply runs as the agent allows. Its pass in the plan names the model and effort it ran on, per `specs/methodology/working-files.md § A Design Document`.

**Direct edits —** a small tactical edit, narrow in scope and low in risk, may skip this process and be applied directly, but only once the user has approved it. Anything larger or riskier goes through the process.

**A new branch —** is created only once the user approves it, the builder proposing its name and what it starts from: how work is split across branches decides how it is reviewed and merged, which is the user's to settle, as a direct edit is.
