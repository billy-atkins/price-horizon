# Spec of Record: Agent Instructions

This file is the entry point to Spec of Record for these specs. Read it before any work on a file in Spec of Record's scope (`specs/methodology/scope.md § What Spec of Record Governs`). It sends each change to the procedure that governs it, and it holds the rules that reach every author. Read `specs/methodology/glossary.md` next, before anything else (`specs/methodology/scope.md § Progressive Disclosure`). `specs/architecture.md` describes the specs as a whole.

## Writing specs

`specs/methodology/` holds the rules for writing specs and for the code the specs govern. Those rules, and the rules in this file, reach the files in Spec of Record's scope, as `specs/methodology/scope.md § What Spec of Record Governs` sets. The methodology's own files are among them.

**Keeping specs in sync.** What a change reaches beyond the facts it edits is kept in sync with those facts, as `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync` has it. What it reaches is each materialized view of the facts (`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`), and the counterpart that draws their subject from the other perspective (`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`).

Every change a design makes is of one of the kinds `specs/methodology/working-files.md § A Design Document § The Kinds of Change` defines. A working file is of no kind of change, and is changed as `specs/methodology/working-files.md § The Working Files` has it. `specs/methodology/working-files.md § A Design Document` also sets when a change's design document declares its kind, and `specs/methodology/working-files.md § A Design Document § A Change Needing Both Kinds` how a change that needs two kinds is split. Each change goes to the skill for its work. The skills for the specs serve every kind of spec alike, and each skill forks on the kind where the work differs:
- **Changing a spec, or another file in scope but code.** `.ai/skills/design-specs/`. Its Workflow gives each rule it applies a point-of-use citation, and forks into the reference for the change's kind.
- **Checking a spec, or such a file.** `.ai/skills/audit-specs/`. Its Workflow forks on the kind of each file it audits, and a run reads the audits and the semantic checks of the kinds it covers, as `specs/methodology/design-workflow.md § A Design's Reviews` sets. The skill that writes a plan checks the plan (`specs/methodology/scope.md § Rules and Skills`).
- **Designing and writing code.** `.ai/skills/implement-specs/`.
- **Checking code.** `.ai/skills/verify-spec-implementation/`.

Before doing by hand a kind of work that a registered skill covers, read that skill's `SKILL.md`.

Running the procedure, rather than recalling the rules, puts each rule in mind at the step it governs (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). This section's index finds a rule mid-step, whatever the work. The index routes. It stands in for no step of a procedure.

**Reference Key:** Doing This \
**Required:** The Rules Are Here

| Doing This | The Rules Are Here |
|---|---|
| Finding which files Spec of Record governs, and how to find your way through them | `specs/methodology/scope.md § What Spec of Record Governs`, `specs/methodology/scope.md § Progressive Disclosure` |
| Meeting a term Spec of Record gives a meaning of its own | `specs/methodology/glossary.md` |
| Deciding product spec versus technical spec | `specs/methodology/spec-placement.md § Product or Technical` |
| Writing a spec or the documentation, or reviewing a design changing either, as its persona | `specs/methodology/spec-placement.md § Personas` |
| Deciding index, architecture, or detail file | `specs/methodology/spec-placement.md § Index, Architecture, Detail` |
| Placing a new file, or deciding whether a domain earns a subfolder | `specs/methodology/spec-placement.md § Where a File Goes` |
| Writing the technical stack or an environment | `specs/methodology/spec-placement.md § The Technical Stack`, `specs/methodology/spec-placement.md § Environments` |
| Naming a new product capability domain | `specs/methodology/spec-placement.md § Naming a Capability Domain` |
| Linking a product file to the technical files that build it | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Deciding whether a rule may be restated | `specs/methodology/sourcing-and-citation.md § One Home Per Fact` |
| Writing a citation, referring to other text, or deciding whether a citation may be written | `specs/methodology/sourcing-and-citation.md § Writing a Citation`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Adding or retitling a heading | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Describing a rule, a process, or an entity's behavior | `specs/methodology/modeling-constructs.md` |
| Writing an expression a construct computes or tests | `specs/methodology/expressions.md` |
| Recording a decision the specs rely on but have not made | `specs/methodology/spec-placement.md § Open Question` |
| Writing a field, a bold lead-in, emphasis, literal text, a blank line, a table of items of one kind, or an entry of a repeated kind or a closed set's members | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Markdown`, `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct`, `specs/methodology/modeling-constructs.md § Constructs § Basic Table`, `specs/methodology/spec-style.md § Bold Lead-ins`, `specs/methodology/spec-style.md § Emphasis`, `specs/methodology/spec-style.md § Literal Text`, `specs/methodology/spec-style.md § Blank Lines`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Writing or updating acceptance scenarios | `specs/methodology/acceptance-scenarios.md` |
| Removing drafting residue and hedged framing, or explaining a trade-off | `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` |
| Writing prose its primary reader understands on the first read | `specs/methodology/spec-style.md § Clear Prose` |
| Writing a sentence that states a rule | `specs/methodology/sourcing-and-citation.md § One Home Per Fact § One Rule to a Sentence` |
| Writing a number, a count, or a reference to an item | `specs/methodology/spec-style.md § Ordinals and Counts` |
| Keeping a materialized view, an `architecture.md` or a diagram, in sync with its sources, or a product spec aligned with its technical counterpart | `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`, `specs/methodology/spec-placement.md § What an Overview Describes` |
| Adding, changing, or re-checking a diagram | `specs/methodology/modeling-constructs.md § Diagrams`, then `.ai/skills/author-mermaid-diagram/` |
| Recording a proposed change, its goals, its Frame Outcomes and Assessed Areas, its steps and their Objectives, its log, a check's report and the Read Assessments of its research, the wording it retires, a steer given it, or work to take up later | `specs/methodology/working-files.md § A Design Document`, `specs/methodology/working-files.md § Design Goal`, `specs/methodology/working-files.md § A Design Document § Frame Outcome`, `specs/methodology/working-files.md § A Design Document § Assessed Area`, `specs/methodology/working-files.md § Design Plan Step`, `specs/methodology/working-files.md § Design Plan Step § Step Objective`, `specs/methodology/working-files.md § Design Log Entry`, `specs/methodology/working-files.md § A Check's Report`, `specs/methodology/working-files.md § A Check's Report § Read Assessment`, `specs/methodology/working-files.md § Retired Phrase`, `specs/methodology/working-files.md § Steering Decision`, `specs/methodology/working-files.md § A Follow-up` |
| Refactoring and refining specs that have landed, the canon's or the application's | `specs/methodology/glossary.md`, `§ Design, Refactor, Refine`, then `.ai/skills/design-specs/` |
| Taking a design through its work and its apply, in their order, sizing its reviews by its kind, picking its audit, starting a review with its brief, or applying a review's reasoning effort | `specs/methodology/design-workflow.md` |
| Setting up the agent in use to apply a review's reasoning effort | `specs/methodology/skills.md § Setting Up an Agent`, then `.ai/skills/configure-spec-of-record/` |
| Registering or authoring a skill | `specs/methodology/skills.md § Registered Skills`, `specs/methodology/skills.md § Authoring a Skill` |
| Adding or changing a rule, and the check enforcing it | `specs/methodology/scope.md § Rules and Skills` |
| Recording a check, or finding a check's area | `specs/methodology/checks.md` |
| Writing an instruction any agent can follow | `specs/methodology/scope.md § Agent Agnostic` |
| Checking that the code carries out its specs | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § The Technical Stack`, then `.ai/skills/verify-spec-implementation/` |
| Designing and writing the code the application specs govern | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § Personas`, `specs/methodology/spec-placement.md § A Product Module`, `specs/methodology/spec-placement.md § Environments`, `specs/methodology/working-files.md § A Design Document § A Design Changing Code`, then `.ai/skills/implement-specs/` |

## Design, Refactor, Refine

This section sets how anything here is built or reworked, whether a spec, a rule, a skill, or code. The working files are aside: the builder changes them as `specs/methodology/working-files.md § The Working Files` has them changed.

### What Sets the Work

The builder (`specs/methodology/glossary.md`) takes the work through this process, in the order that `specs/methodology/design-workflow.md § The Order of a Design's Work` gives. `§ Design, Refactor, Refine § Measure Twice, Cut Once` sets the builder's role against its reviewers. `§ Design, Refactor, Refine § Who Decides` and `§ Design, Refactor, Refine § Converging, or Not § The Runs` set when the builder stops for the user. `.ai/skills/design-specs/` applies the process to the canon and the application specs, and `.ai/skills/implement-specs/` applies it to code.

### Reading Fresh

Before working on a file, read it again, however small the change or recent the last read. A direct edit is no exception. Nothing tells an agent whether its memory of a file survived compaction. Content written an hour ago feels remembered when it is a reconstruction. So the builder also reads `§ Design, Refactor, Refine § What Sets the Work` again each time it resumes the work.

### The Goals and the Frame

The builder and the user agree in discussion on at least one design goal for the change (`specs/methodology/working-files.md § Design Goal`). Each goal is evaluated against the change's problem. Together the goals answer the problem, and none reaches past it. No goal need ask for elegance (`specs/methodology/glossary.md`). Every design owes elegance, as `§ Design, Refactor, Refine § Refactor`, `§ Design, Refactor, Refine § Refine` and `§ Design, Refactor, Refine § Measure Twice, Cut Once` have the builder carry it out.

Then, before drafting, the builder states the change's design frame (`specs/methodology/glossary.md`) and presents it to the user. The builder drafts only once the user agrees to the frame or adjusts it. Each answer is recorded as a steer (`specs/methodology/working-files.md § Steering Decision`). A steer that changes the goals or the frame is confirmed with the user before it is applied. The builder then presents the change, with the frame re-evaluated against any goals that changed. The user approves it before the work goes on. The design then takes a fresh adversarial review, unless the user's approval has ended its review. Any other steer is recorded as given, as `specs/methodology/working-files.md § Steering Decision § When a Steer Is Recorded` has it. A frame the user never saw lets the builder solve a problem the user does not have.

The frame's parts hold what `specs/methodology/working-files.md § A Design Document` gives them. Its Approach cites the goals it rests on, as `specs/methodology/working-files.md § A Design Document` has it, and each Frame Outcome the goals it rests on, as `specs/methodology/working-files.md § A Design Document § Frame Outcome` has it, so a change to a goal finds what to re-evaluate.

The frame's scope, the cases the change governs, is the actual scope of the change. Too small a scope reaches a local optimum, right for the file in hand and wrong for the system around it. Only the real scope admits the global optimum. The sweep for it is research, done as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Research` has research done. The sweep is widened until nothing outside it would change the answer. Its Searches run by meaning as well as by the draft's words, because a search built from the draft's terms finds only what the draft already knew about. The sweep finds every passage stating part of each rule the change states, and every use of each term the change defines or redefines. It covers the files a review reads, as `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` bounds them. The frame's scope is the cases the change governs among the areas the sweep's assessments find bearing on the design.

Each area the sweep's assessments find bearing on the design goes where `specs/methodology/working-files.md § A Design Document § Assessed Area` sends it. Where an area goes is decided as `§ Design, Refactor, Refine § Who Decides` has the call made. Where the builder would leave out an area whose Impact holds `changes`, an application area of a canon design aside, it brings the assessment and its own reading to the user. The user's answer is a steer (`specs/methodology/working-files.md § Steering Decision`). An area the user leaves out is taken up again only where the goals or the frame change. No such answer sets an Impact. An area is assessed again only as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Research` has an assessment stand. An area research turns up outside the frame takes the route `§ Design, Refactor, Refine § Settling a Round § The Test` gives a place outside the frame.

The Frame Outcomes are settled before the draft, so that the draft is judged by the Frame Outcomes, rather than the Frame Outcomes fitted to the draft. Work the builder would add as the design goes on is held to the goals, as a review's findings are. Work that no goal reaches is a change of its own, however convenient folding it in would be. The builder hands that change to the user to spawn or log, as `specs/methodology/working-files.md § A Design Document § Spawning a Change of Its Own` has it, unless the user first widens the goals.

#### Whether the Goals and the Frame Name a Mechanism

This test asks whether the goals and the frame name a mechanism the steps change. Such a mechanism has states or routes. The design alters its states, its routes or the facts deciding them, either in a step stating its rows or in keeping its text in sync. A rule written as prose that routes is such a mechanism. A mechanism whose wording alone the design keeps in sync, its decisions standing, is not. The builder asks the test at the trace, as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism` has it, and at settling, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has it. The check's report holds the table's outcome for each mechanism or decision the test is asked of: the self-review's in the trace of the mechanism, as `specs/methodology/working-files.md § A Check's Report § Trace` has a trace recorded, and the round's in the cause continuing an earlier one, as `specs/methodology/working-files.md § A Check's Report § Cause` has a cause recorded. The user triages a design flaw the table finds, as `§ Design, Refactor, Refine § Converging, or Not § A Design Flaw` has one triaged. Where the trace finds that the goals and the frame miss a mechanism, that design flaw is a call that blocks the adversarial round. It goes to the user when it arises, before that round, as `§ Design, Refactor, Refine § Who Decides` has such a call asked.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Asked at, Findings drawn again?, On a mechanism the steps change?, A goal sentence stating the mechanism's change?, The mechanism's deciding facts in the Scope?, An Outcome testing the mechanism? \
**Input Values:**
  - Asked at: "the trace", "settling"

| Asked at | Findings drawn again? | On a mechanism the steps change? | A goal sentence stating the mechanism's change? | The mechanism's deciding facts in the Scope? | An Outcome testing the mechanism? | The goals and the frame |
|---|---|---|---|---|---|---|
| settling | false | - | - | - | - | not asked |
| - | - | false | - | - | - | not asked |
| - | - | - | true | true | true | name the mechanism |
| - | - | - | - | - | - | miss the mechanism, a design flaw |

### Design

Start from the problem to solve, stated plainly. Get a draft logically working, one that solves the problem correctly, before it is good. A plan describes the draft, and for the specs and for code, the plan is a design document. Where the work turns up a change of its own, that change is spawned as a design of its own or logged as a follow-up, as `specs/methodology/working-files.md § A Design Document § Spawning a Change of Its Own` has it.

### Refactor

Make macro improvements to what is being built, to its internal workings and its external surface. These are structural changes, not wording, that make it better meet its actual needs and work toward elegance (`specs/methodology/glossary.md`). Repeat until Refactor converges, when a round leaves the structure where it was.

### Refine

Once Refactor has converged, make the elegance of what is built plain, and make it easy to use and to understand. Refine works on wording, naming, phrasing and consistency. Polishing something still moving structurally is wasted effort.

### Measure Twice, Cut Once

The builder and its reviewers pull against each other, as a software engineer and a quality assurance engineer do. The builder aims to hand a review nothing to find. The reviewer, in the adversarial review, the post-apply review and an audit alike, aims to find what the builder missed. That tension makes the work good. It holds only while the builder does its part, because quality comes from the builder's own passes, and the reviewers are a second set of eyes, never the first check. Fast and sloppy is slow, because each finding a reviewer makes sends the work back through the builder's process and can cost another review. Methodical and correct is fast.

The builder names a step's What and the Target as `specs/methodology/working-files.md § Design Plan Step § What a Step Rests On` and `specs/methodology/working-files.md § A Design Document` have them named, so its own reading sets no part of the design. An area its research turns up outside the frame takes the route `§ Design, Refactor, Refine § Settling a Round § The Test` gives a place outside the frame. The builder holds each step, and what it writes, to the rules they apply, as it works.

#### The Order of a Design's Parts

A design is read and built in the order its parts name each other: its goals, then its frame, its Scope and its Assessed Areas before its Frame Outcomes, then its steps, each after the steps its Depends On Steps names (`specs/methodology/working-files.md § Design Plan Step § What a Step Rests On`). The builder drafts a design in that order, top-down. It makes each change at the highest part the change touches, whether the change is a steer's, a round's settlement, a pass's or the revision of what waited on another design. It then revises each part naming that part, down the same order, from the list the design script's `--show-dependents` gives of the parts naming or citing a part, a Scope paragraph named by its bold lead-in among them. A rule is stated once, at the highest part holding it, and each part below cites it, as `specs/methodology/sourcing-and-citation.md § One Home Per Fact` gives a fact one home. A part left unrevised below a changed one restates what the change has moved, and the next round finds it. A build tool works the same way, rebuilding each target after the targets it depends on.

The builder takes the steps through Design, Refactor, Refine before validation. It takes them through again whenever a change reaches a step, a steer's change among them, before the validation that precedes the next adversarial round. At the apply, it takes what it writes through them.

#### Research

Reading and searching to find what a change reaches, or what the design must follow, are research (`specs/methodology/glossary.md`). The user's steers and the Read Assessments of the design's research are the design's inputs, standing above it. They feed its goals, its frame and its steps, and no part of the design sets them. A steer changes only by the user's word (`specs/methodology/working-files.md § Steering Decision § When a Steer Is Recorded`). An assessment changes only by its Area being assessed again, as this section has an assessment stand. Research sets no part of the design but through its assessments.

The builder chooses what to research: its Searches, for a rule's reach, for the frame's sweep and for what restates a change, and the places it knows to read, by the reach of its zoom-out (`§ Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out`). It hands them to a cold agent, as `§ Design, Refactor, Refine § A Handed-off Judgment` has a judgment handed off, with the design document and a brief naming the research's cause. The cold agent records the places the builder named in its report's Reading. It runs the Searches and reads each matched and named place. It records a Read Assessment of each area within them (`specs/methodology/working-files.md § A Check's Report § Read Assessment`). The builder designs from the assessments, stating a step's Objectives from them. So the builder's context holds what bears on the design, and none of the text that does not. Whatever else the builder reads, the canon it applies, a review's report or a finding's evidence, is its own reading, and sets nothing.

A place is assessed once, and its assessment stands. A place is first assessed when the builder researches it. A place a review's finding names that no assessment covers is first assessed as that finding is settled, that place alone, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has it. An area already assessed is assessed again only where the user changes the goals or the frame in a way bearing on what was read, or where a review's finding shows the area's assessment wants a new perspective. The builder's brief then names the change or the finding. The cold agent assesses again only the places it reaches. So a finding feeds an assessment, and an assessment the design, never the design an assessment. A step's revision and a round's settlement assess nothing again but on such a finding. The frame freezes at the plan's approval, as `§ Design, Refactor, Refine § The Adversarial Review § The Plan's Approval` has a change to the frame undo the approval. An assessment made after it reaches the design only as a finding the user settles, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has it.

#### The Zoom-Out

The builder zooms out to find how far the rule the change touches reaches, every other place stating the fact a fix changes among it. Before the plan's approval, the builder zooms out before it states a step's outcome and before it makes a fix to a step in settling a round. That zoom-out is research, done as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Research` has research done.

At the apply, the builder zooms out before it writes and before it makes a fix to text it wrote. It reads fresh, as `§ Design, Refactor, Refine § Reading Fresh` has a file read, each area assessed other than `none` that bears on what it writes: the areas the step's What names, which it changes, and the Assessed Areas holding `applies`, which it follows. That zoom-out is no research. A Read Assessment, filtering for relevance, replaces none of its reading. Reading more costs only time and tokens, while reading too little costs the specs and what is built from them.

The zoom-out reaches:
- around: the parent of the section holding the change, whole, the section's siblings among it. Where the section is a top-level section, or the change sits in a file's text before its first section, it reaches that section or that text, with the sections on either side of it;
- up: each ancestor's text before its first child heading, among them a file's text under its title, before its first section heading;
- across: every passage elsewhere that cites what it reached around or any section within it, any ancestor of the section holding the change, or the file whole, a citation of one part by its key among them. It reaches each such passage around and up in turn, and no further;
- in code or a script: the unit holding the change, the units it calls and the units that call it.

#### A Rule Written Whole

At the apply or in a fix, the builder writes the rule within the areas a step names whole, as one coherent statement, however much text that takes. It never writes it as a clause wedged into what stood. Patches laid one on another leave a rule in pieces no reader can follow.

#### Tracing a Mechanism

The builder traces each mechanism with states or routes, such as a State Machine, a DAG or an Algorithm, through every path it allows, every way into each state of a State Machine among them. Before the adversarial review, it traces each mechanism its steps change, from the rows the steps state. Before the post-apply review, it traces each mechanism the apply wrote. Before the adversarial review, it also takes each mechanism that `§ Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism` reaches, those it traces among them, and asks whether the goals and the frame name it, as that section has it. It records the trace in its self-review's report, as `specs/methodology/working-files.md § A Check's Report § Trace` has a trace recorded. A path left untraced is the next review's finding, and finding it first costs less than the round that would find it.

#### The Self-Review

The builder makes its self-review (`specs/methodology/glossary.md`) before each review that follows a change of its own, the first adversarial round and the first post-apply round among them. Where no round follows, it makes it before the validation or before the user's review.

Before its other checks, it asks each question `specs/methodology/working-files.md § A Check's Report § Kinds of Builder Check [Check Kind: miss's question]` requires of it. It reads what the review that follows reads, as that review's record in `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles` cites its Work, fresh as `§ Design, Refactor, Refine § Reading Fresh` has a file read. It runs the construct checks of the skill writing the design on the constructs the steps state. It makes the judgments of the review that follows, as that review's section sets them, and before an adversarial round it judges the plan's structure first, as `§ Design, Refactor, Refine § The Adversarial Review` has the structure judged. At the apply, it runs the checks the post-apply review runs over the work, as `§ Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over` scopes them. It reports each thing it finds as a Finding quoting its evidence, as the review that follows reports one (`specs/methodology/working-files.md § A Check's Report § Finding`).

Beside those, it makes the checks only the builder makes, each as `specs/methodology/working-files.md § A Check's Report § Kinds of Builder Check` has it, where that table requires it. Once a round's change is made, it reads each place a Miss (`specs/methodology/working-files.md § A Check's Report § Miss`) of the phase so far names, this round's among them, since that miss shows what its reading lacked. It traces each mechanism as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism` has it. For code, it runs the local environment's tasks, as `specs/methodology/spec-placement.md § Environments` sets. At drafting, it reads the reach of the wording the design retires, by its design script's `--show-reach`. Before the post-apply review, it runs its design script's `--check-retired-wording` (`specs/methodology/working-files.md § Retired Phrase`). It runs `--check-changed-files` then too, for any file changed that is none of the design's changes (`specs/methodology/working-files.md § A Design Document § Applying and Committing`).

It records each reading, search, trace and test in its report, as `specs/methodology/working-files.md § A Check's Report` has it. The design script's `--append-entry` checks the report as it appends the self-review's entry, by the script checks among those `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]` runs.

#### What the User Says at the Apply

At the apply, the builder tells apart each thing the user says, a steer, feedback on the applied result, direction or a decision about other work, by `specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`, before acting on it. It then acts by that thing's route. Where the user's words ask for a route the canon does not have, it says so and names the canon's route before acting.

### A Handed-off Judgment

The builder hands a judgment off to a cold agent it briefs, as `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: a judgment the builder hands off]` has the judgment made. The cold agent reads within the bound `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` sets, and only the items the builder names. It judges each item against what the builder names it with, its text at the baseline or the home it cites, and gives a verdict for each. Its brief holds what the text's own reader would have. A question of what the text's author meant goes to its author, the user for what a specification decides, never to the cold agent. Research is among these judgments, as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Research` has it done.

### The Adversarial Review

When the builder judges the work optimal, a cold agent reviews it, as `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]` has the review made. The reviewer is never the builder, since re-reading your own work re-reads what you meant. It reviews as the persona of what the design changes (`specs/methodology/spec-placement.md § Personas`). It reads within the bound `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` sets. The reviewer derives no solution of its own to the design's problem.

It reads the design document whole, its problem, its design goals, its design frame and its steps each stated on its own. It reads the design's steering decisions as the settled record of how the user shaped it (`specs/methodology/working-files.md § Steering Decision`). It reads the files the steps reach, and the specs or code they rely on, the canon's or the application's, as they stand. While kept changes stand, it reads the files as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has them read.

It judges the plan's structure first, by `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-serves-its-goals]`, `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-states-an-outcome]` and `specs/methodology/working-files.md § A Design Document § Frame Outcome § Semantic Checks [Name: outcome-upheld]`, asked of every step Objective and Frame Outcome. A round any of them fails reports those findings alone and judges the design no further. Its reviewer writes in its report's Title the field Stopped At, holding `the structure`, as `specs/methodology/working-files.md § A Check's Report` has a round stopped at the structure marked. A plan whose parts do not hold together fails whatever the rest of its design says, so a round reading the design's whole reach would spend itself on a design that must change first.

Past the structure, it confirms or denies that the design's steps bring its goals, in the context of its frame, to fruition. It confirms or denies too that their Objectives let the implemented design be validated as accomplished, each Objective a state of the applied work that a reviewer can confirm or find unmet. The goals are its yardstick, the frame their context, and the steering decisions settled, not reopened. Its criteria are the plan's steps against the design goals and the design frame, and the canon's rules over the design's own composition, as `§ Design, Refactor, Refine § Settling a Round § The Test` holds every review to them. It looks hardest where the design decides, since that is where defects concentrate. It takes the design through the Design, Refactor, Refine process again, looking for Rube Goldberg machines and Potemkin villages (`specs/methodology/glossary.md`), and for a step patched where it should have been rewritten whole. It challenges whether the goals reach what the problem needs. A finding arguing that a goal misses it or reaches past it, or that the frame misses a place, is sorted as `§ Design, Refactor, Refine § Settling a Round § The Test` sorts it.

It judges whether the design's frame is in sync with its steers and its steps, and cites the goals it rests on. It judges whether each Frame Outcome is true of them. It judges these parts against what `specs/methodology/working-files.md § A Design Document` gives each to hold:
- the Scope, for what the design relies on from each design its Depends On Designs names;
- the Out of Scope, for naming no other working file;
- in a canon design, the Impact on the Application Specs, for each item handing its work on, or, holding no item, for saying how the research covered the application specs.

It judges whether each citation in the design resolves: to a heading in the files as they stand, to a heading a step adds, or to what the design states it relies on from a design its Depends On Designs names. It judges the design's Target against its Kind. It judges the frame's Assessed Areas, and the design against each whose Impact holds `applies`.

It researches nothing: it redoes no sweep and assesses no area again. Where it holds that the frame misses a case, it raises a finding from its own reading, within the bound `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` gives it. A passage within the Target that the change leaves false is its finding only where that passage holds a decision the steps do not make. A passage outside the Target that the change leaves false is always its finding, the work's breach. That breach lies in the plan, as `specs/methodology/working-files.md § A Design Document § Applying and Committing` bounds the apply, or, outside the frame, takes the route `§ Design, Refactor, Refine § Settling a Round § The Test` gives a place outside the frame. It judges an implementation flaw by the frame and the canon.

It edits nothing. It groups its findings by the decision of the design each touches. It marks each finding a design flaw, an implementation flaw or a nit (`specs/methodology/glossary.md`), to be settled as `§ Design, Refactor, Refine § Converging, or Not` has it. It weighs each finding before reporting it, as `§ Design, Refactor, Refine § Weighing a Review's Findings` has it. Each finding quotes its evidence from the files as they stand, and names what it bears on as `specs/methodology/working-files.md § A Check's Report § Finding` has a finding name it. It reports anything else it would want different as a review observation, as `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` has it. It writes its report in the form `specs/methodology/working-files.md § A Check's Report` gives a review's report. It checks its part by the design script's `--check-report` before handing it back, by the script checks among those `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]` runs.

The builder confirms each finding's quoted evidence before acting on it, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has it. It settles an adversarial review's findings as `§ Design, Refactor, Refine § Settling a Round` has it. A round that finds a design flaw, as the user triages it, or an implementation flaw is followed by another round, which checks the fixes. A round stopped at the structure is followed by another round too, and never converges the review, whatever its findings settle to. The adversarial review converges at the first round not stopped at the structure that finds only nits the builder judges harmless, or nothing.

#### The Plan's Approval

The user's approval of the plan ends the review too. The user may give it in any state of the work, before any round or during one. The state in hand finishes its own work. An approval given in a reassessment is that reassessment's decision. A round still running or being settled is left with its findings as they are. The approval is logged as a `plan-approval` entry (`specs/methodology/working-files.md § Design Log Entry`). The design goes on to its validation and, once stamped, is approved. The approval authorizes the apply's writing, as `specs/methodology/working-files.md § A Design Document § Applying and Committing` has it. It is applied where the user approved it with apply, once the apply may begin (`specs/methodology/working-files.md § A Design Document § The States It Moves Through`).

A change to the goals, the frame or a step after the approval undoes the approval. The design then comes back to the user to approve again, never to another round on its own, unless the user asks for one. After a review that converged instead, a change to the goals, the frame or a step takes another round (`specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design`). With the user's go-ahead, the plan is then applied, in the order `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply` gives.

### The Post-Apply Review

Once the builder has written the plan's text or code, a cold agent reviews it as the persona of what the design changes, as `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]` has the review made. It reads within the bound `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` sets. It reads the apply's changes: the diff of the altered files against the last commit, or the Target's files whole where the project has no version control. It reads the files as they stand and the frozen design. For a Refactor and Refine cycle, it reads the files at the cycle's baseline too.

It reads the applied work against the frozen design and asks, in order:
- whether the applied work meets each step's Objectives, the standing Objective (`specs/methodology/working-files.md § A Design Document § The Standing Objective`) among them, and changes nothing but the design's changes;
- whether the applied work achieves each Frame Outcome, by `specs/methodology/working-files.md § A Design Document § Frame Outcome § Semantic Checks [Name: outcome-upheld]`;
- whether the applied whole delivers the design goals;
- whether its structure and wording hold, as `§ Design, Refactor, Refine § Refactor` and `§ Design, Refactor, Refine § Refine` judge a draft.

Its criteria are the applied changes against each step's Objectives, the Frame Outcomes, the design goals, the design frame and the specs, and the canon's rules over the design's own composition, as `§ Design, Refactor, Refine § Settling a Round § The Test` holds every review to them. It runs every check `§ Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over` scopes to the work, over the scope it gives each. It runs the script checks by the `--check-work` of the skill writing the design, the construct checks among them. It reads a change that a `direct-edit` entry logs as the builder's writing. It reads a change in a `user-edit` entry's places as `§ Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is` has it read. It reopens nothing the design decided.

It marks each finding as the adversarial review marks its own, quoting its evidence and naming what it bears on as `specs/methodology/working-files.md § A Check's Report § Finding` has a finding name it. It places each finding as `§ Design, Refactor, Refine § The Post-Apply Review § Placing a Finding` has it. It weighs each finding as the adversarial review weighs its own. It reports anything else it would want different as a review observation, as the adversarial review does. It writes its report, and checks its part, as the adversarial review does, by the script checks among those `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]` runs.

The builder settles each round as `§ Design, Refactor, Refine § Settling a Round` has it. Within the Target, it makes a tactical fix in the files. A finding outside the Target, and one on text whose migration the frame hands on, is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it. A finding lying in the plan goes to the user, whose triage sends the design back with its changes kept. The review converges at the first round that finds only nits, or nothing. The builder then shows the user the applied result, as `§ Design, Refactor, Refine § What the User Is Shown` has it. The user approves it, asks for another round, or gives feedback. The builder takes the user's feedback into its writing, which the post-apply review then reads again.

#### Placing a Finding

A finding over applied work lies in the plan or in the writing, or is handed on, as `specs/methodology/working-files.md § A Check's Report § Where a Finding Lies` names where it lies. Its questions mean these:
- **In a file the design's Kind lets it change?** Answered as `specs/methodology/working-files.md § A Design Document § Changes After Approval` answers it.
- **Handed on by the frame?** Answered as `specs/methodology/working-files.md § A Design Document § Changes After Approval` answers it.
- **Its fix changes the plan?** True for a design fix (`specs/methodology/glossary.md`), and for any fix that would change the goals, the frame, the Target, or a step's What or its Objectives. False for a tactical fix (`specs/methodology/glossary.md`), and for an implementation flaw the writing settles by meeting a step's Objectives.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** In a file the design's Kind lets it change?, Handed on by the frame?, Its fix changes the plan?

| In a file the design's Kind lets it change? | Handed on by the frame? | Its fix changes the plan? | Lies In |
|---|---|---|---|
| false | - | - | handed on |
| true | true | - | handed on |
| true | false | true | the plan |
| true | false | false | the writing |

### An Audit

An audit is a run of its skill, `.ai/skills/audit-specs/`'s, or for code `.ai/skills/verify-spec-implementation/`'s, made as `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]` has it. `specs/methodology/design-workflow.md § A Design's Reviews` picks the run from the kinds it is given, sets what it runs over, and sizes its effort by the design's Kind. An audit is never narrowed to a design's changes. It names no design, so it cannot tell which change wrote what it reads. Where a rule reaches only what a change writes, the audit reports each breach of it wherever it finds one. Its criteria are the complete specs, by the rules the audit is instructed to check. It reports each finding as its skill reports one, and anything else it would want different as a review observation.

Run by the user, an audit's report is the user's to read. Run by the builder in a design's apply, once the user approves the applied result, its report is the builder's, since the builder knows what it changed and why. The builder confirms each finding's quoted evidence before acting on it, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has a round's confirmed. It reads each finding against the diff of the files the apply altered, as `§ Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is` has a finding read. The builder's triage tells what the design wrote from what it left as it stood. It triages each finding as caused by the design or not. It marks each finding the design caused as the post-apply review marks its own, a design flaw, an implementation flaw or a nit, and places it as `§ Design, Refactor, Refine § The Post-Apply Review § Placing a Finding` has it. Each finding is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it.

### Converging, or Not

A hard problem can take many review rounds, and each phase counts its own, as `§ Design, Refactor, Refine § Converging, or Not § The Runs` has each run counted: the adversarial reviews of a design before it is approved, the post-apply reviews of its applied work, its audits, and its applies. A finding `§ Design, Refactor, Refine § Settling a Round § The Test` keeps, whether an adversarial review's, a post-apply review's or an audit's, is a design flaw, an implementation flaw or a nit. A flaw is always named a design flaw or an implementation flaw. When each review converges is set by `§ Design, Refactor, Refine § The Adversarial Review` and `§ Design, Refactor, Refine § The Post-Apply Review`. Whose call each verdict is, `§ Design, Refactor, Refine § Who Decides` says. A flaw is settled by the round's change, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Weigh by the Goals` has it. A round's settling ends as `§ Design, Refactor, Refine § Settling a Round` has it end, and the round's change and its proof follow, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove` has them.

#### A Design Flaw

Examples of a design flaw (`specs/methodology/glossary.md`) include a goal that misses what the problem needs or reaches past it, as `§ Design, Refactor, Refine § Settling a Round § The Test` has it sorted, and a place outside the frame that that section makes a flaw in the frame. Others are an approach that cannot reach a goal, and a Frame Outcome that does not judge one. The builder brings each design flaw to the user after the round, with the builder's recommended change to the design goals, the design frame or both. The user triages it, whoever uncovers it, the one writing the text or one reviewing it, as `§ Design, Refactor, Refine § Who Decides` has it.

#### An Implementation Flaw

An implementation flaw (`specs/methodology/glossary.md`) can be of any seriousness. Examples include a case the scope names and the steps miss, a rule broken, and a file left out of sync. Before approval, the builder settles each as `§ Design, Refactor, Refine § Settling a Round` has a round settled, and the reviewer's next round checks it. After the apply, a post-apply review's implementation flaw is settled as `§ Design, Refactor, Refine § The Post-Apply Review` has it. An audit's implementation flaw is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it.

#### A Nit

In an adversarial review, a nit (`specs/methodology/glossary.md`) is the builder's call, as `§ Design, Refactor, Refine § Who Decides` has it. A round that finds a design flaw or an implementation flaw has all its nits fixed in the change the round makes. In a round that finds only nits, the builder judges each nit. Where the builder judges one harmful, because leaving it would harm the applied files or what is built from them, the builder marks it an implementation flaw. The round then has a flaw, and all its nits are fixed. Where the builder judges none harmful, it leaves them. It records each nit it leaves as a Settlement whose Verdict is nit in the round's report, as `specs/methodology/working-files.md § A Check's Report § Settlement` declares it. A harmless nit is like lint on a moving blanket protecting an item in transit: the lint will not harm the item. Lint on the sterile cloth that holds a surgeon's scalpels is different, because it is not healthy for the patient. After the apply, a nit is a tactical fix, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` marks one. A post-apply review's nit is settled as `§ Design, Refactor, Refine § The Post-Apply Review` settles a tactical fix. An audit's nit is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it.

#### The Runs

Every round of the adversarial review that the user's approval did not end, and every round of the post-apply review, is settled at its causes, whatever it finds, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes` has it. The builder counts each run apart. It counts a round's design flaws by the user's triage. Each run's length is a Fact of `specs/methodology/design-workflow.md § The Order of a Design's Work § Facts`, its Initial Value:
- the run of design flaws, adversarial rounds in a row, none ended by the user's approval, that each found a design flaw, at its length `design flaw run length`, means the design is not converging, its goals or frame wrong past what its rounds can mend;
- the run of implementation flaws, adversarial rounds in a row, none ended by the user's approval, that each found an implementation flaw, at its length `implementation flaw run length`, means its steps are not converging;
- the run of post-apply flaws, post-apply rounds in a row that each found an implementation flaw lying in the writing, at its length `post-apply flaw run length`, means its writing is not converging;
- the run of rework audits, audits in a row that each sent a finding back to the writing, at its length `rework audit run length`, means its apply is not converging;
- the run of send-backs, applies in a row that each ended with the design sent back, at its length `send-back run length`, means the plan is not converging on what can be applied.

A run reaching its length has the builder stop revising and take the design to the user, and the two step back and reassess. The builder brings its recommendation, with revised goals and frame where the run is of design flaws, and its case for why the work should now converge. They then rescope, split or abandon the design, or take a different approach, and start afresh with what was learned. Or the user has the work go on, and the run is not set back. Each further round that extends the run brings the builder and the user back to reassess, until a round ends the run.

### Each Review's Model and Effort

The adversarial review, the post-apply review and an audit in the apply each run on a model and at a reasoning effort (`specs/methodology/glossary.md`). The user chooses the model and the effort as two separate choices. The user makes both once for a design, before the design's first adversarial review. Where the user's approval ends the review before any round, the user makes them before the design's post-apply review instead. The choices are kept for each later review and audit until the user changes them. The effort is light, medium or high. By default, a review runs on the model the agent runs on, at the effort the design's Kind gives it (`specs/methodology/design-workflow.md § A Design's Reviews`). A model other than the agent's own can see past a blind spot that a reviewer on the same model would share. A higher effort costs more. Neither changes what a review or an audit reads, nor a review's brief. A level is applied as `specs/methodology/design-workflow.md § A Review's Effort` has it. A review on a model the agent cannot start a reviewer on runs as the agent allows. The review's entry in the design's log names the model and the effort the review ran on, as `specs/methodology/working-files.md § Design Log Entry` has it.

### Direct Edits

A small tactical fix (`specs/methodology/glossary.md`), narrow in scope and low in risk, may skip this process and be applied directly, once the user approves it, as `§ Design, Refactor, Refine § Who Decides` has the call made. Made in a design's apply, it is one of the design's changes (`specs/methodology/working-files.md § A Design Document § Applying and Committing`). It is logged as a `direct-edit` entry naming its places, as `specs/methodology/working-files.md § Design Log Entry` has it. Anything larger or riskier goes through the process.

### A New Branch

The builder proposes a new branch's name and what the branch starts from. The branch is created only once the user approves it. How work is split across branches decides how the work is reviewed and merged, so the split is the user's to settle, as `§ Design, Refactor, Refine § Who Decides` has it.

### Who Decides

A call the canon gives the user stays the user's, and is settled as its home sets. The user's calls include:
- a design flaw, as `§ Design, Refactor, Refine § Converging, or Not § A Design Flaw` has one triaged;
- a review observation;
- a breach in text the design only reads, as `§ Design, Refactor, Refine § Settling a Round § The Test` sorts one;
- a finding the builder cannot settle within the goals and the frame, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes` has it brought;
- a steer a round's change presses on, as `specs/methodology/working-files.md § Steering Decision § Revisiting a Steer` has it decided;
- a post-apply review's finding lying in the plan, as `§ Design, Refactor, Refine § The Post-Apply Review § Placing a Finding` places one;
- how each audit finding `§ Design, Refactor, Refine § Settling a Round § The Test` keeps is settled, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it;
- the design goals and the design frame, agreed to or adjusted as `§ Design, Refactor, Refine § The Goals and the Frame` has them, each answer a steer;
- leaving out an area whose Impact holds `changes`, as `§ Design, Refactor, Refine § The Goals and the Frame` has the call brought;
- a direct edit, as `§ Design, Refactor, Refine § Direct Edits` has one made;
- a new branch, as `§ Design, Refactor, Refine § A New Branch` has one made;
- the model and the effort each review runs on, as `§ Design, Refactor, Refine § Each Review's Model and Effort` has them chosen.

Every other call is the builder's, made on its own recommendation. Among them are an implementation flaw before approval, a nit in an adversarial review, and where an area goes that the user's calls leave to it. No cold agent makes a call. A review reports what it finds, and a Read Assessment places no area, as `specs/methodology/working-files.md § A Check's Report § Read Assessment` has it.

The builder asks a call of the user's that blocks the next step when the call arises. The calls that block nothing wait, and go to the user all together with that blocking call. Each goes with the builder's recommendation, so the user answers in a word. The builder brings each review observation to the user with its round, as the round's settlement ends, or with its triage of an audit. An observation blocks none of the settlement. The round's settlement, or the audit's triage, records the user's answer to each call the builder brought.

### What the User Is Shown

The builder shows the user each thing the user approves with its summary, so what the user sees rests on no builder's choice:
- the plan, at its approval: what changed since the user last saw it and why, each change from the builder's self-review or from a review, how the builder settled the findings, and the findings each reviewer dropped with the reviewer's reasons;
- the applied result, at the user's review: what the applied work does, each round's counts by mark, the findings each reviewer dropped with the reviewer's reasons, how each finding was settled, and the checks the builder ran;
- the settled audit, before the commit: what the audit found and how each finding was settled, in the files or handed on.

### Who Checks What and Why

A design and its work go through the checks `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles` records, in the form `§ Design, Refactor, Refine § Who Checks What and Why § Check Role` declares. Why each check is feedback is `§ Design, Refactor, Refine § Who Checks What and Why § A Check Is Feedback`'s to say. The scope each runs over is `§ Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over`'s, and whose a finding is, `§ Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is`'s. What any review reads is bounded by `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads`.

#### A Check Is Feedback

A check is feedback to whoever writes. The builder and the post-apply review run each check of the files or the code over the work. The audit runs its checks over its units, as `§ Design, Refactor, Refine § An Audit` has it. So the builder learns of an implementation flaw of its own before any review does. A compiler reports to an author the same way, on the code they wrote.

The reason serves the agent itself: a flaw is cheapest to fix where it is caused. An agent that sees no gain in a check takes the shortcut past it. The builder's self-review and the post-apply review read the reach of the work. The audit reads what `§ Design, Refactor, Refine § An Audit` has it read. The findings already standing in those files are among its findings, each triaged against the design's changes as `§ Design, Refactor, Refine § An Audit` has an audit read. One whose fix goes back to the writing runs that audit whole again, as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply` routes it. So a flaw the work caused costs a reading of its reach where the work is checked, and far more once it reaches the audit. An agent skipping a check over its work to save time spends more than the check would have cost. Every review's cost and the audit's grow with the scope of the change, so the larger the change, the more early feedback saves. The design workflow orders the checks so the most immediate feedback on a rule is acted on before the flaw grows costlier.

#### The Scope a Check Runs Over

The scope a check runs over a design's work is decided by its type alone, as `specs/methodology/checks.md § Check` declares the types. A script check reads the whole scope, as it stands and as it stood at the last commit. A semantic check reads the reach `§ Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out` has the builder zoom out to: around, up and across from each section the apply wrote in, or, in code or a script, from each unit it wrote. The candidates standing in that reach guide its reading and never bound it. What lies past that reach, the audit reads. Where a check runs, over a design or over its work, is stated as `specs/methodology/checks.md § Check` has it.

Until the checks' entries are records, the semantic checks over the work are those of the audit `specs/methodology/design-workflow.md § A Design's Reviews` sets for the kinds of the files the Target names. They are the rules of each reading audit that audit runs, in the audits table of `.ai/skills/audit-specs/SKILL.md`, and, where the kinds include `code`, the readings the table of checks of `.ai/skills/verify-spec-implementation/SKILL.md` lists.

The builder's self-review, the post-apply review and the audit each run in a state of the apply. The builder's self-review runs at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: writing]`, before the post-apply review. The post-apply review runs at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: post-apply reviewing]`. The audit runs at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: auditing]`.

#### Whose a Finding Is

One test settles whose a finding of either kind is. A finding is the work's where the last commit, read by the rules as they stood in it, did not hold it: the diff wrote the breach, made text false that was true, or changed a rule that carried-over text now breaks. A semantic check tells which by reading its finding against the diff. A breach the last commit held by its own rules, carried over unchanged, is the audit's. A breach the apply rewrote and kept is the work's, since the diff wrote it. The last commit holds the files as they stood before the apply. Where the project has no version control, the test reads against the builder's own account of the files it changed. A rule the apply changed may find a breach in text the apply carried over. The frame settles that breach, for a script check and a semantic check alike, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` settles it. A change in a `user-edit` entry's places is the user's, and no finding of either kind. Nor is an Objective a finding where an edit of the user's, kept by the user, leaves it unmet.

#### What a Review Reads

No review, whether the adversarial review, the post-apply review or a handed-off judgment, reads a working file but the design it is given, its own report and each report the design's log entries name (`specs/methodology/working-files.md § Design Log Entry § The Report an Entry Names`). So another design document and `.ai/follow-ups.md` lie outside its reading. Keeping a design in sync with them is the builder's, checked by its self-review as `specs/methodology/working-files.md § A Check's Report § Kinds of Builder Check [Check Kind: linked work]` has it. A review reads the files in Spec of Record's scope or in the design's Target, the working files aside, as its task needs. What an audit reads is `§ Design, Refactor, Refine § An Audit`'s to say.

A check asks only what the Work of its record in `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles` gives it. No reviewer builds a script, a harness or a copy of the files to read anything. A review reports what it would want different beyond its criteria as a review observation (`specs/methodology/glossary.md`), apart from its review findings. No count reads an observation, since the design bounds what is core to it.

#### Check Role

A Check Role is one check a design or its work goes through: who makes it, where what it reads and asks is stated, which check records it runs, and what it leaves to another. No Check record says this (`specs/methodology/checks.md § Check`). It is a record type (`specs/methodology/modeling-constructs.md § Constructs § Record Form`), its records standing in `§ Design, Refactor, Refine § Who Checks What and Why § Check Roles`:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Check Roles \
**Reference Key:** Check

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Check | yes | yes | | text | the check's name |
| Made By | no | yes | | text | who makes the check |
| Work | no | yes | | text | a list, each item a citation of a section holding what the check reads and asks |
| Runs | no | yes | | text | a list, each item a citation of a Script Check or a Semantic Check record the check runs (`specs/methodology/checks.md § Check`), or `none` |
| Leaves | no | yes | | text | a list, each item one sentence naming one thing the check leaves to another and whose it is, or `none` |

#### Check Roles

**Records:**
  - **Check:** the builder's self-review \
    **Made By:** the builder \
    **Work:**
      - `§ Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`

    **Runs:**
      - `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-serves-its-goals]`
      - `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-states-an-outcome]`
      - `specs/methodology/working-files.md § A Design Document § Frame Outcome § Semantic Checks [Name: outcome-upheld]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: builder-checks-required]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`
      - `specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`

    **Leaves:**
      - The design document's form is the validation review's.

  - **Check:** a judgment the builder hands off \
    **Made By:** a cold agent the builder briefs \
    **Work:**
      - `§ Design, Refactor, Refine § A Handed-off Judgment`

    **Runs:**
      - `none`

    **Leaves:**
      - The design as a whole is the adversarial review's.
      - Settling its findings is the builder's, as `§ Design, Refactor, Refine § Settling a Round` has it.
      - Where an assessed area goes is the builder's and the user's, as `§ Design, Refactor, Refine § Who Decides` has it.

  - **Check:** the adversarial review \
    **Made By:** a cold agent, started with the standard brief alone (`specs/methodology/design-workflow.md § A Review's Brief`) \
    **Work:**
      - `§ Design, Refactor, Refine § The Adversarial Review`

    **Runs:**
      - `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-serves-its-goals]`
      - `specs/methodology/working-files.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-states-an-outcome]`
      - `specs/methodology/working-files.md § A Design Document § Frame Outcome § Semantic Checks [Name: outcome-upheld]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`

    **Leaves:**
      - Writing the text or code is the apply's.
      - The applied work is the post-apply review's.
      - The design's linked work is the builder's self-review's.

  - **Check:** the validation review \
    **Made By:** the design script of the skill writing the design, as `specs/methodology/working-files.md § A Design Document § The Record's Checks` has it \
    **Work:**
      - `specs/methodology/working-files.md § A Design Document § The Record's Checks`

    **Runs:**
      - `none`

    **Leaves:**
      - What `specs/methodology/working-files.md § A Design Document § The Record's Checks` leaves to the adversarial review is that review's.
      - The design's place in the workstack is `--check-workstack`'s, as `specs/methodology/working-files.md § A Design Document § The Record's Checks` has it.

  - **Check:** the post-apply review \
    **Made By:** a cold agent, started with the standard brief alone (`specs/methodology/design-workflow.md § A Review's Brief`) \
    **Work:**
      - `§ Design, Refactor, Refine § The Post-Apply Review`

    **Runs:**
      - `specs/methodology/working-files.md § A Design Document § Frame Outcome § Semantic Checks [Name: outcome-upheld]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`
      - `specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`

    **Leaves:**
      - What lies past the scope a check runs over the work is an audit's.
      - Testing behavior is the builder's self-review's.

  - **Check:** an audit \
    **Made By:** a cold agent, given the skill's name and, in a design's apply, the kinds `specs/methodology/design-workflow.md § A Design's Reviews` sets \
    **Work:**
      - `§ Design, Refactor, Refine § An Audit`

    **Runs:**
      - `none`

    **Leaves:**
      - Triaging its findings against a design's changes is the builder's, as `§ Design, Refactor, Refine § An Audit` has an audit read.
      - Testing behavior is the builder's self-review's.

  - **Check:** the user's \
    **Made By:** the user \
    **Work:**
      - `§ Design, Refactor, Refine § Who Decides`
      - `§ Design, Refactor, Refine § What the User Is Shown`

    **Runs:**
      - `none`

    **Leaves:**
      - `none`

### Reading the Earlier Reports

The reports a design's log entries name (`specs/methodology/working-files.md § Design Log Entry § The Report an Entry Names`) are read for what each check found and how its findings were settled. Where a report's settlement and the design differ, the design governs.

### Weighing a Review's Findings

The adversarial review and the post-apply review each weigh their findings before writing the report, in a collecting pass and a weighing pass.

In the collecting pass, the reviewer collects every issue it finds. It marks each finding, and sets each review observation apart as `§ Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` has it.

In the weighing pass, the reviewer weighs each finding by `§ Design, Refactor, Refine § Settling a Round § The Test`. A finding it keeps is reported with its rationale and a possible fix. The rationale shows what goes wrong in the work if the finding is left. A finding landing on text an earlier round's change added names that round in its rationale. Where the finding's fix is a tactical fix (`specs/methodology/glossary.md`), the possible fix is that tactical fix. Otherwise the possible fix names the decision the finding touches and what that decision's revision must deliver. The reviewer leaves the revision to the builder, which makes it at the round's causes, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose` has it. A finding it drops is reported as dropped, with the reason the reviewer changed its mind. A review observation is reported with the reviewer's reason for judging the work wrong, and with no fix.

Between its passes, the reviewer reads the reports the design's log entries name, as `§ Design, Refactor, Refine § Reading the Earlier Reports` has them read. A finding the builder dropped in an earlier round is raised again only with an argument that round's settlement did not weigh.

A reviewer's dropped findings, with its reasons, show where its first reading was preference.

### Settling a Round

A round's settling ends with its report holding its Causes and its Settlement, and with the round's entry appended, as `specs/methodology/working-files.md § Design Log Entry § When an Entry Is Appended` has an entry appended. The round's change and its proof follow the settling, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove` has them.

#### The Test

The builder addresses a review finding only where this test needs it addressed, or where the user asked for it. Each review's criteria, as its section states them, hold the design to its goals, its frame and its steps. They hold it to the canon's rules over the design's own composition alone, as the design's goals and frame may change those rules. So a breach in text the design only reads bears on no review's criteria.

The test sorts each item a review reports, and each finding of an audit or of the builder's self-review it is applied to, by what the item bears on, never by the label its writer gave it. Its questions ask:
- **An audit's finding not caused?** Whether the item is an audit's finding that the builder's triage holds the design did not cause, as `§ Design, Refactor, Refine § An Audit` has a finding triaged.
- **Anchored in.** Where the item is anchored:
  - `the plan`, where it bears on a stated goal, Frame Outcome or step Objective inside the frame;
  - `the work's breach`, where it shows the design's own composition breaking the canon. Before the apply, that is text the design writes or its steps would leave wrong. After it, that is a breach `§ Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is` makes the work's, wherever its text lies, a place outside the frame taking the route this section gives one;
  - `neither`, where it bears on neither.
- **Goals or frame shown wrong?** Whether it shows the goals or the frame wrong, a goal missing what the problem needs or reaching past it among them, as `§ Design, Refactor, Refine § Converging, or Not § A Design Flaw` has a design flaw.
- **Bloat?** Whether it asks for mechanism, such as a state, a field, a flag, a rule or a check, to cover a case that no goal's or Objective's words name, or a risk that a guard already in the canon or the design covers.
- **May merit a change of its own?** Whether the builder judges that what it asks for may merit a change of its own.
- **Shows a harm?** Whether it shows one of these going wrong in the work if it is left:
  - the work contradicting itself, its goals or the canon;
  - an Objective that cannot be confirmed;
  - a case that a goal's or an Objective's own words name, missed by the work;
  - a reference or a value that is wrong.
- **A call the user's?** Whether `§ Design, Refactor, Refine § Who Decides` gives the user the call it raises, a breach in text the design only reads among them.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** An audit's finding not caused?, Anchored in, Goals or frame shown wrong?, Bloat?, May merit a change of its own?, Shows a harm?, A call the user's? \
**Input Values:**
  - Anchored in: "the plan", "the work's breach", "neither"

| An audit's finding not caused? | Anchored in | Goals or frame shown wrong? | Bloat? | May merit a change of its own? | Shows a harm? | A call the user's? | The Item |
|---|---|---|---|---|---|---|---|
| true | - | - | - | - | - | - | not caused |
| - | the work's breach | - | - | - | - | - | a review finding |
| - | the plan | true | - | - | - | - | a design flaw |
| - | the plan | - | true | true | - | - | a review observation |
| - | the plan | - | true | - | - | - | dropped |
| - | the plan | - | - | - | true | - | a review finding |
| - | neither | - | - | - | - | true | a call the user's |
| - | neither | - | - | - | - | - | a review observation |
| - | - | - | - | - | - | - | dropped |

A review finding and a design flaw are needed. The builder never drops a design flaw: it goes to the user, as `§ Design, Refactor, Refine § Who Decides` has the call brought, as do each call the user's and each review observation. An audit's finding the design did not cause is no review's, and is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` settles one. A dropped finding holds no mark, so no count by mark, no Fact and no run reads it. It is listed as dropped in the round's settlement, or in the builder's triage of an audit, and counted in Dropped (`specs/methodology/working-files.md § Design Log Entry § What a Check Counts`).

One rule routes a place outside the frame, whether the builder's research or a review's finding brings it. A place outside the frame that the change leaves wrong is handed on where the design already hands its work on, as `specs/methodology/working-files.md § A Check's Report § Where a Finding Lies` has a finding handed on. Any other place the change leaves wrong is a flaw in the frame. So is a case the change leaves right that a stated goal's own words reach. The builder brings such a flaw to the user, as a design flaw. Any other place outside the frame is nothing to the design. An argument that the frame take it in is a review observation, brought to the user as `§ Design, Refactor, Refine § Who Decides` has one brought.

The builder weighs each finding the reviewer kept and each it dropped, taking in the reviewer's rationale and its possible fix. Where the builder's verdict on a finding differs from the reviewer's, the round's settlement says why. So it does where the round's change settles less than the reviewer's possible fix reaches.

#### The Round at Its Causes

The builder settles every finding the test keeps within the design goals and the design frame. It brings the user, with its recommendation, only each call that `§ Design, Refactor, Refine § Who Decides` gives the user, a finding it cannot settle within the goals and frame among them. A reviewer's findings are what the reviewer saw of the design. They are often right, and often symptoms of a cause that the reviewer, not being the builder, does not name. A finding fixed where it sits can leave its cause to produce the next round's findings. So the builder settles each round of an adversarial review that the user's approval did not end, and each round of a post-apply review, as design work, never one finding at a time. It first confirms each finding's quoted evidence, as `§ Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` has it. An audit's findings are settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has them. To settle a round, the builder steps back.

##### Group

The builder confirms that each finding's quoted evidence stands in the files by searching for it, before acting on the finding, since a review can be confidently wrong. Before grouping, it reads the earlier reports, as `§ Design, Refactor, Refine § Reading the Earlier Reports` has them read. It hands to a cold agent each place a finding of the round names that no Read Assessment covers, for a first assessment. It hands on too each area a finding shows wants a new perspective, for an assessment again, the brief naming the finding. Each is assessed as `§ Design, Refactor, Refine § Measure Twice, Cut Once § Research` has a place assessed. Before the plan's approval, it takes those assessments into the frame, as `§ Design, Refactor, Refine § The Goals and the Frame` has an assessed area taken in. Only then does it find the round's causes, from the findings, the assessments and the earlier reports. So it judges a flaw's scope from what the places a finding names hold rather than from the line it quotes. In an adversarial round, it reads no place a finding names.

In a post-apply round, the frame stands frozen. A finding naming a new place whose Impact holds `changes` is settled as `specs/methodology/working-files.md § A Design Document § Changes After Approval` settles a finding outside the Target, and goes to the user. A finding naming a new place whose Impact holds `applies` alone is fixed following that place. The builder reads fresh, as `§ Design, Refactor, Refine § Reading Fresh` has a file read, what the round's change rewrites and what that writing follows, a new place among it wherever its assessment is other than `none`. It records that reading in the round's Settling Reads, as `specs/methodology/working-files.md § A Check's Report § The Reading and the Settlement` has it.

It groups the round's findings by the decision of the design each touches, such as a rule the design states, a form it chooses, a unit it writes or its frame's reach. The groups take in the findings of the phase's earlier rounds too, and those a judgment the builder handed off has made since the last round. No finding is fixed as it arrives. Of each decision drawing findings, the builder asks what lets them in. It asks first of each decision drawing findings again, one an earlier round of the phase drew findings on too. Of such a decision, before any other cause, it asks whether the goals and the frame are the cause, as `§ Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism` has it. That test asks only whether the goals and the frame name the mechanism. Where it is not asked, or finds that they name it, the cause may still be another design flaw in the goals or in the frame, as `§ Design, Refactor, Refine § Converging, or Not § A Design Flaw` names them. It may be an implementation flaw instead, such as a case the scope names and the steps miss, a rule stated in pieces with no one home, or a form chosen wrong.

Of each finding the test keeps that is marked a design flaw or an implementation flaw, the builder then asks why its own Design, Refactor, Refine pass and self-review let the flaw through. The answer is the flaw's miss (`specs/methodology/glossary.md`). Before it proposes the round's change, the builder asks each question a miss names of the work, recording the answer the work gives it beside the miss. In an adversarial round, it answers from the assessments. In a post-apply round, it first reads each place a miss names, fresh as `§ Design, Refactor, Refine § Reading Fresh` has a file read.

##### Weigh by the Goals

The builder weighs against the design's goals each finding that asks the design to do more, less or other, and each change it would propose, the test dropping what the work does not need. Each flaw the round holds is settled by the one change the round proposes at its causes, a design flaw once the user has triaged it.

##### Weigh the Steers

The builder weighs the steers that the causes press on, as `specs/methodology/working-files.md § Steering Decision § Revisiting a Steer` has it.

##### Propose

The builder states the round's causes, each flaw's miss beside its cause, and the one change it proposes at them, with each finding's settlement under it. As it states them, it shows the user each Miss of the round with the question or the place it names, and the number of Misses the phase holds. A cause holding only nits is settled as `§ Design, Refactor, Refine § Converging, or Not § A Nit` has nits settled. In a post-apply round, a cause lying in the plan goes to the user, as `§ Design, Refactor, Refine § The Post-Apply Review § Placing a Finding` places a finding. Of the other causes, one whose fix is a tactical fix (`specs/methodology/glossary.md`) has that fix made at every place its defect stands. The settlement gives the reason its fix is a tactical one. Every other cause has the decision it lies in revised by Design, Refactor, Refine from that decision's problem, as `§ Design, Refactor, Refine § Design` starts a draft. The revision is written whole, as `§ Design, Refactor, Refine § Measure Twice, Cut Once § A Rule Written Whole` has a rule written. Each clause wedged in opens a path the next round finds, so a revision made now costs less than the rounds a patch would bring. Where the goals or the frame let findings in, their revision comes first.

A round goes to the user when it holds a call that `§ Design, Refactor, Refine § Who Decides` gives the user, a design flaw or a steer the round's change presses on among them.

The round's change is the least of the revisions at its causes, weighed by what the revised work holds. It is the revision delivering the goals with the fewest rules, as `specs/methodology/glossary.md` has elegance, and with the least text. It is never weighed by how little of the decision as it stands it changes, nor by the text each finding needs. A change removing text, or citing the home that holds the fact, comes before one adding text. Where a finding lands on text that an earlier round's change added, the builder first weighs again, by `§ Design, Refactor, Refine § Settling a Round § The Test`, the finding that change settled. Where that finding is not needed, the least change removes what the earlier change added, which settles both findings. A steer the earlier change carried out is weighed as `specs/methodology/working-files.md § Steering Decision § Revisiting a Steer` has it.

##### Change and Prove

The builder revises the design as the round was settled, top-down, as `§ Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts` has a change made, or, in a post-apply round, the files. It then proves the round's change by its self-review, as `§ Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review` has it, never by rereading the round's change alone. It proves it before the next round, or, where no round follows, before the design is validated or, after a post-apply round, before the user's review.

#### After the Last Round

When the builder hands off a judgment after the phase's last round, the judgment's findings are settled together, in one pass, before the design is validated or, after the post-apply review, before the user's review. Where a round completes any run that `§ Design, Refactor, Refine § Converging, or Not § The Runs` sets, the design is not revised until the builder and the user have reassessed it, as that section has it.
