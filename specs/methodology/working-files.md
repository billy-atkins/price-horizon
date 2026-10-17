## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`. What a working file settles reaches a reader only through the spec it changes.

**Reference Key:** File

**Required:** Holds

| File | Holds |
|---|---|
| `.ai/plans/` | the plans the skills write, a design document among them (`§ A Design Document`) |
| `.ai/follow-ups.md` | work on the specs or the code that should be done and is not yet, each as a follow-up (`§ A Follow-up`) |
| `.ai/tmp/` | the skills' own output, review and audit reports among it |

**A skill's scratch space is `.ai/tmp/<skill-name>/` —** created by the skill if it is not there. One directory per skill so that one skill's output is never mistaken for another's, and under `.ai/tmp/` so none of it is ever committed. A skill does not delete its own output when it finishes: the output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its own *stale* output, the file left behind from a previous run that no longer corresponds to anything, since a reader has no way to tell that from a current one.

**A skill's plans are `.ai/plans/<skill-name>/` —** a skill describing a change before making it writes each plan to a file of its own in that directory, creating the directory if it is not there. One directory per skill so that one skill's plans are never mistaken for another's, and one file per plan so each is read, reviewed and handed to a cold agent whole.

An open question about what is specified is not a working file's to hold; it is recorded in a spec, per `specs/methodology/spec-placement.md § Open Question`.

## A Design Document

Each design document is a file of its own, one per change taken through `specs/AGENTS.md § Design, Refactor, Refine`. `.ai/skills/design-specs/` writes each design changing the specs under `.ai/plans/design-specs/`, and `.ai/skills/implement-specs/` each design changing code under `.ai/plans/implement-specs/`. Both take this form; a design changing code differs only where `§ A Design Document § A Design Changing Code` sets. Each skill's steps and its script hold a design to this form, the script reaching the design document tooling the two skills share, and no audit reads a design. A design opens with a level-one heading, `Design Document`, whose section holds its fields (`specs/methodology/modeling-constructs.md § Fields`), and its sections follow as level-two headings. It holds its parts, in this order:

**Reference Key:** Part

**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `**Name:**` field | yes | | the change, in a few words. The file is named for it in kebab-case: lower case, each run of other characters a hyphen. Other design documents name this one by that file name without its extension; one in another skill's plans folder puts this design's folder name and a slash before it, as `design-specs/{file name}` |
| Status | a `**Status:**` field | yes | | its state in `§ A Design Document § The States It Moves Through` |
| Source | a `**Source:**` field | yes | | what asked for the change: the user's own words, or the finding that raised it |
| Kind | a `**Kind:**` field | yes | | the kind of change, one of the kinds `§ A Design Document § The Kinds of Change` gives, which bounds the files the change may edit and sizes its reviews (`specs/methodology/design-workflow.md § A Design's Reviews`), settled while the design is shaped and before any file is edited |
| Target | a `**Target:**` field | yes | | every file the change edits, each a path in backticks, separated by semicolons; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | yes | | the design document this one was spawned from, or none |
| Depends On | a `**Depends On:**` field | yes | | the design documents that block this one, separated by semicolons, or none; what blocks a design, and when, is set by this section's paragraphs on what blocks what and on blocked and to revise |
| Validated | a `**Validated:**` field | yes | | the stamp the validation review left once the document passed it, per `§ A Stamp`, leaving out the Validated and Status fields, or none; current while the design is approved |
| The Problem | a `## The Problem` section | yes | | what is wrong, stated on its own, before any fix |
| Design Goals | a `## Design Goals` record section (`§ Design Goal`) | until the design is complete or abandoned | | the design's goals, or `Not yet stated.` until the user agrees them, which no design approved or further holds |
| The Design Frame | a `## The Design Frame` section | yes | | the design frame (`specs/methodology/glossary.md`) the user agreed or adjusted (`specs/AGENTS.md § Design, Refactor, Refine`), under level-three headings in this order: Scope, holding the cases the change governs and what tells them apart, then how the sweep for affected content was done and what it found, what it left out included; Approach; and Outcomes. A part not yet stated reads `Not yet stated.`, which no design approved or further holds |
| Steering Decisions | a `## Steering Decisions` record section | once the user has steered the design | | each steer the user gave, per `§ Steering Decision` |
| The Design | a `## The Design` section | yes | | what the design does, then each edit, introduced by a bold lead-in naming the file it edits (`specs/methodology/spec-style.md § Bold Lead-ins`), then `this text:` and the text it replaces, quoted exactly, then `becomes:` and its replacement; or `a new file:` and the file whole; so it can be verified and applied as written |
| Impact on the Application Specs | a `## Impact on the Application Specs` section | in a canon design | | each application file and section the canon change leaves out of step, what it leaves out of step there and what the application work must do, or that none was found; and how the application specs were reviewed |
| The Builder's Passes | a `## The Builder's Passes` section | yes | | what each pass and each review changed, each under a bold lead-in naming it and each review but the validation review named with its report, where it gave one; the nits a round left, and each judgment the builder handed off, with how its findings were settled; the builder's own trace, before a review, of each mechanism with states or routes its edits change; and the builder's own check of what its edits change in a script or code, each ephemeral differential test (`specs/methodology/glossary.md`) of a changed script or each of the local environment's tasks it ran on code, and what each showed. An adversarial review's lead-in opens `Adversarial review`, and a post-apply audit's `Post-apply audit`. Each of those two names the model and reasoning effort it ran on, as `on {model} at {effort} effort`, the effort one of the levels `specs/AGENTS.md § Design, Refactor, Refine` names, or as `on {model} as the agent allows` where the agent could not apply the effort chosen; and it records the design flaws among its findings, as `specs/methodology/glossary.md` defines them, with the user's triage of each. An adversarial review's pass also records how the builder settled its implementation flaws, the causes the round's change addressed, a mechanism it rewrote whole where its findings clustered, and the worked case proving it, or the user's approval of the design's text where it ended the review, with the round it ended; a post-apply audit's pass records how each of its findings settled, as `§ A Design Document § Changes After Approval` has them |
| Deliberately Left Alone | a `## Deliberately Left Alone` section | yes | | each change considered and declined, with the reason, and each piece of work deferred, named by the design document spawned for it or the follow-up logging it |

**Spawning keeps a design focused —** when a design turns up work that is a change of its own, a migration of files a rule change leaves out of step among them, that work is spawned as a design document of its own or logged as a follow-up (`§ A Follow-up`), as the user decides, since which suits depends on how the user means to work it. It is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change; the design's scope still sweeps what the spawned change touches, and only its edits move.

**Depends On records what blocks what —** a spawned design without which the design it came from cannot finish blocks that design, and is named in that design's Depends On; one that can be worked before or after it does not. Depends On is the one record of what blocks what, and names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks, back toward the design it began from.

**Blocked and to revise are read, not recorded —** a design finishes when it is complete or abandoned. A design is blocked while its Depends On names a design that has not finished, and is to revise once one it names has finished; both are read from the Status of the designs its Depends On names, never recorded in the design itself. A blocked design may still be worked. A design is validated and approved only once each design its Depends On names is approved or applying, a finished one taken in and removed first, so designs that build on each other can be shaped and approved before any of them is applied. A design is applied only once its Depends On names none, so they apply in dependency order. Where a design goes back to in progress, the builder moves back each approved design whose Depends On names it. Once a design its Depends On names finishes, the design goes back to in progress if it is approved, takes in what that one settled, or why it was dropped, against the files as they stand once it finishes, and removes it from Depends On.

**Unwinding —** a finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. When a design is abandoned, each open design it spawned goes on as a design of its own, or is abandoned with it, as the user decides. A Spawned By naming a design since deleted stays, as the spawned design's history.

**The record's checks —** before a design is approved, the validation review, the design script of the skill writing it, checks that the design document is a valid document: its form and its integrity, never what it says. How the builder applied the user's steers, and whether the design is right, are the adversarial review's to read (`specs/AGENTS.md § Design, Refactor, Refine`), and the steers are the review's account of how the design was shaped. The checks:

**Reference Key:** Check

**Required:** What The Record Holds, Why

| Check | What The Record Holds | Why |
|---|---|---|
| Form | its heading, its fields and its sections in the order and the form this section's table gives them, and, by the time it is validated, no goal and no part of its frame reading `Not yet stated.` | a reader and a script find each part where the form puts it |
| Records | its design goals, its steering decisions and each other record section, each record holding the fields its type declares, a Type among the values it declares, and each Name used once | a record out of its form is one no script can read |
| The edits | each quoted edit of The Design applying to its file exactly once, or already applied | what the user approved is what is applied |
| References | each citation resolving in the files as they stand or as the design's own edits leave them, the steers and the passes, which tell history, aside; each goal its frame cites one the design holds; and each design document its Depends On names existing | a reference to nothing leads a reader, and the work, nowhere |

**Valid to approve —** the validation review reports each problem it finds, the builder fixes it, and the review runs again, until the document passes and the review stamps it (`§ A Stamp`). Every problem it can report is one of form or integrity, so none is a question for the user, and a stamp never waits on what the document says. The stamp is the review's record in the design. A design changed after its stamp no longer matches it, so a stale validation is read from the file and never cleared by hand, and the review runs again.

**A form the method is still adding —** a design whose record uses a form that a design changing the method adds, a part of a design document or a record type, names that design in its Depends On, and its checks, its validation review and its stamp run with that design's edits applied, through the design script's `--with-edits-of`; a design adding such a form uses it in its own record and runs with its own edits applied, naming itself in no Depends On; so the record is held to the method as it will be, as a self-hosting compiler is built with the syntax it adds.

**A change needing both kinds is split —** its canon design reviews the application specs for what it leaves out of step there, records that in its Impact on the Application Specs, and edits none of them. That application work goes to the application design the canon design was spawned from, where there is one, or else is spawned or logged as this section's spawning paragraph has it, and the canon and application designs may be worked in concert. A design changing the specs that leaves code out of step edits none of the code either: it records the code its change leaves out of step in its design frame's Scope, and that work goes to a design changing code, spawned or logged the same way. What the canon design's post-apply audit finds in the application specs settles by `§ A Design Document § Changes After Approval`, and what that table hands on is application work too, added to what its review handed on or handed on the same way, so the canon design completes without editing them. Where the application work finds the canon design wrong, the canon design takes the change while it is in progress or approved, the user reopening an approved one. For any other canon change the application work needs, a change to the canon design once that design is applying or complete among them, the application design spawns a canon design, which blocks it, the user reopening the application design first where it is approved. An application design already applying keeps to what was approved, the canon change spawned or logged without blocking it, as the user decides.

**Applying and committing —** a design's apply begins only as `§ A Design Document § The States It Moves Through` lets it move into applying. Its changes are committed on their own, one commit for each design even where a branch holds several, so a revert takes exactly that design's changes; where the project has no version control, they are reverted by hand. A design abandoned while applying has the edits it wrote reverted.

### The Kinds of Change

What each kind bounds a change to:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Kind

| Kind | Bounds the change to |
|---|---|
| `canon-specs` | `specs/AGENTS.md`, `specs/architecture.md`, the files under `specs/methodology/`, a registered skill's directory, and `.ai/skills/lib/` |
| `application-specs` | the files under `specs/application/` |
| `code` | the application's code, within the code roots the technical stack names (`specs/methodology/spec-placement.md § The Technical Stack`), which the application specs govern (`specs/methodology/code.md`); a design changing code's only kind |
| `documentation` | the documentation, `README.md` and the files under `docs/` |
| `other` | any other file, the project's root `AGENTS.md`, its helper scripts and the working files a design changes among them |

Every file a design's Target names is of its declared kind, or is a file of `documentation` or `other`, or is code whose annotation lines alone it edits, as `specs/methodology/code.md § Changing Code` has a design retitling a heading.

### Changes After Approval

Once the user approves a design, every change it makes to the files is one the user approved and one the design describes. Each finding of its post-apply audit is presented to the user, and settles by what it is:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** Finding

| Finding | Settles |
|---|---|
| one the user judges wrong | set aside, and recorded in the pass with the reason |
| a canon design's, in the application specs | handed on as application work, as `§ A Design Document`'s paragraph on a change needing both kinds has it |
| a nit | fixed as a direct edit the user approves (`specs/AGENTS.md § Design, Refactor, Refine`), or left as the user chooses, and recorded in the audit's pass |
| "one exposing a design flaw", "an implementation flaw no direct edit fixes", "one proposing a tactical fix to the design's own edits that the user does not approve" | sends the design back to in progress: its changes to the files are reverted, and it is revised and worked afresh from the files as they stood before its apply, with what was learned |
| one outside the design's own edits | settled as the user chooses, and recorded in the pass: folded in as a direct edit (`specs/AGENTS.md § Design, Refactor, Refine`); dropped; logged as a follow-up; or given a design, one of its own, standing apart or spawned from this one, or an existing design not yet applied taking it in, as `§ Steering Decision § A Decision About Other Work` has it |
| a tactical fix the user approves | made as a direct edit (`specs/AGENTS.md § Design, Refactor, Refine`), and recorded in the audit's pass |

### The States It Moves Through

The states a design document's Status moves through, and what moves it from one to the next:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | Yes | No |
| in-progress | its work under way, governed by `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` | No | No |
| approved | validated and approved by the user, its adversarial review converged or ended by the user's approval of its text, and not yet applied, awaiting the go-ahead to apply | No | No |
| applying | its apply under way, governed by `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply` | No | No |
| complete | applied, its audit settled; what it decided lives on in the specs it changed | No | Yes |
| abandoned | withdrawn by the user | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| not-started | in-progress | the work is taken up | none |
| in-progress | approved | none | none |
| approved | in-progress | the user reopens it | none |
| approved | in-progress | in-progress of a design its Depends On names is entered | none |
| approved | in-progress | a design its Depends On names finishes | none |
| approved | applying | the user gives the go-ahead to apply | its Depends On names none, nothing else is uncommitted, and no other design is applying in the checkout |
| applying | in-progress | none | exit = "sent back" |
| applying | complete | none | exit = "applied" |
| not-started | abandoned | the user abandons it | none |
| in-progress | abandoned | the user abandons it | none |
| approved | abandoned | the user abandons it | none |
| applying | abandoned | the user abandons it | none |

A design its Depends On names finishing is its entering complete or abandoned, a class of occurrences.

### A Design Changing Code

A design changing code starts from applied specs, or from the specs as a design its Depends On names leaves them, rather than from a problem in them, and designs the code and the tests that bring them to life. It takes the form `§ A Design Document` sets, and Design, Refactor, Refine, the adversarial review, the validation review and the stamp, as a design changing the specs does, and differs only where code does. Its parts differ so:

**Reference Key:** Part

**Required:** In A Design Changing Code

| Part | In A Design Changing Code |
|---|---|
| The Problem | names the product module it carries out, then the specs it carries into code, cited, and what the code lacks |
| Kind | `code` |
| The Design | describes each unit of governed code it writes or changes, with the app-spec annotations it carries (`specs/methodology/code.md § Citing the Specs From Code`), the wiring that connects the units (`specs/methodology/code.md § Governed Code and Wiring Code`), and the tests that check the specs (`specs/methodology/code.md § Tests`), quoting existing code only where it changes it, in the forms `§ A Design Document`'s The Design row gives |

**One product module —** it carries out one product module, reading what `specs/methodology/spec-placement.md § A Product Module` sets, in the order `specs/methodology/scope.md § Progressive Disclosure` sets. Work reaching several modules is a design for each. A technical section several modules need, a shared data model's, say, is carried out by the first design changing code that takes it up; a later design names that one in its Depends On while it is unfinished, and builds on its code once it is applied.

**The builder designs, the user steers —** the builder designs the code from the specs on its own, the specs being its starting point, and the user approves the design or steers it. A steer about how the code carries out the specs is this design's. A steer changing what a spec states is spawned as a design changing the specs and named in this design's Depends On, so this design waits on it, per `§ A Design Document`'s paragraph on blocked and to revise, and takes it in once it finishes, revised against the specs as they then stand.

Its post-apply audit is `.ai/skills/verify-spec-implementation/`, reading the code it wrote as `.ai/skills/audit-specs/` reads the specs a design changed.

## Design Goal

A design's goals (`specs/methodology/glossary.md`) are agreed before its design frame, and changed and weighed, as `specs/AGENTS.md § Design, Refactor, Refine` has them. A goal is named, never numbered, so a record speaks of one by its Name however the list changes, and cites it as a record is cited, by its record section and its Name (`specs/methodology/sourcing-and-citation.md § Writing a Citation`).

A design's goals sit in its record section of this type, a record type (`specs/methodology/modeling-constructs.md § Constructs § Record Form`):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Design Goals

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the goal's slug, in kebab-case as a design document's file name is (`§ A Design Document`), by which the record names and cites it |
| Description | no | yes | | text | what the goal asks of the change |

## Steering Decision

A design's Steering Decisions record only the user's steers, the decisions a steering decision records (`specs/methodology/glossary.md`), new scope or a design flaw's fix among them. A steer differs from the user's direction about how the work proceeds, and from a decision about other work, which is no steer of the design being worked (`§ Steering Decision § Telling a Steer Apart`).

**A go-ahead to take in findings —** is a steer for the findings that change what the design is and direction for the tactical ones; an answer carrying both is recorded for the part that decides the design.

**Each steer is recorded when it is given —** and the design is revised to apply it before its work goes on, so the design carries how it was formed and never lags a steer it records. A steer changing the goals or the frame is confirmed with the user, as `specs/AGENTS.md § Design, Refactor, Refine` has it, and is carried into them, its case reaching the Scope, the Approach and the Outcomes. Any other steer, one choosing the wording of the edits or a name in code among them, is recorded as given, and tells the adversarial review the user chose it. Where the steer differs from another choice only by preference, it stands; where it breaks a rule, the review raises it as a finding pressing on the steer, and the builder presents the conflict to the user with a wording or a name that follows the rule, the user choosing either (`§ Steering Decision § Revisiting a Steer`). Only the user revises a steer, by a later one, and the record is history: a later steer revising what an earlier one decided is recorded after it, its Decision saying which it revises, and the earlier one stays as it was given, the design following the later one whatever the Type of either, so the records, read in order, show how the design was shaped. A question the user leaves unanswered is asked again, never read as agreed. The adversarial review reads the steers as background, checking fidelity to them rather than reopening them. The request that opened the design is its Source, and The Builder's Passes record what each pass changed, never a steer, so each steer is recorded once.

**A steer's Type —** a steer is a selection where the user merely selects one of the options the builder offered, a literal selection; every other steer is a perspective, whatever its form, such as emphasis, a negative remark, a nudge or a strong direction for the design. Selecting an option is easier than sharing a perspective, and a perspective originates with the user.

A design's steering decisions sit in its record section of this type, a record type (`specs/methodology/modeling-constructs.md § Constructs § Record Form`):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Steering Decisions

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | a short name for what was decided |
| Prompted By | no | yes | | text | what the steer answered: a question, proposal or account the builder gave, with the options it offered where it offered any, a review's finding named by its ID, or the user's own initiative |
| Type | no | yes | | "selection", "perspective" | a selection or a perspective, as this section's paragraph A steer's Type has it |
| Steer | no | yes | | text | the user's own words, quoted |
| Decision | no | yes | | text | the essence of what the steer decided, in a sentence or two |

### Telling a Steer Apart

#### Steer, Direction or Other Work

How a steer, direction about the work and a decision about other work are each recorded, an answer carrying more than one taken a part at a time:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** What the user decides

**Annotations:** Sounds Like

| What the user decides | Recorded | Tells a reviewer | Sounds Like |
|---|---|---|---|
| A steer | in Steering Decisions, its Steer quoting every part of the user's words that decides the design, never only the last of them | how the design was formed | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found", "call it Kind, not Type" |
| Direction about the work | not as a steer; where the record needs it, in the passes, as the Builder's Passes row of `§ A Design Document` has them, or in the Status field | nothing about what the design is | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "create the branch", "medium effort", "G1 to G6 are design flaws" |
| A decision about other work | where that work is held | nothing about the design being worked | "the implement-specs design should weigh renaming the workstack", "keep the billing service stateless when we design it" |

### A Decision About Other Work

A decision about other work is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory, and a decision about more than one design is recorded in each. What becomes of it, by where the work is held:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Where the work is held

| Where the work is held | The decision |
|---|---|
| "a not-started design", "an in-progress design" | is its steer, applied when that design is worked |
| "an approved design", "an applying design" | is put to the user, who decides whether to reopen that design for it, an applying one only as a design flaw in what it applies (`§ A Design Document § Changes After Approval`): reopened, the design takes it as its steer; not reopened, it is dropped, or, where the user wants it kept for later, logged as a follow-up |
| a follow-up, and no open design | goes in the follow-up's body (`§ A Follow-up`), and the design taking up the follow-up records it as its steer |
| no follow-up, and no open design, only a complete or abandoned design or nothing | the user chooses between a not-started design recorded for it, the decision its Source where it asks for the work and its steer otherwise, and a new follow-up |

### Revisiting a Steer

A design's path is not straight: working toward an elegant solution takes loops, detours and pivots, and a steer is part of what may need to move. Where the builder, settling a round (`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`), finds that a change fixing a cause would go against one or more steers, of either Type, those are the steers the cause presses on. The builder brings the user each such steer, the findings pressing on it and what revising it would change, and proposes revising the selections among them, whose options the builder framed, and a perspective only where revising the selections cannot fix the cause: a perspective outweighs a selection. The user decides.

## A Stamp

A stamp lets a later reader tell whether content has changed since a check passed on it, so nothing has to be cleared by hand. It is written as a UTC timestamp and a content hash separated by a space, `2026-09-29T14:05:12Z sha256:3f9a0c1b2d4e5f60`:

- **The timestamp —** a date and time as RFC 3339 writes one (`specs/methodology/external-references.md § External References [Name: RFC 3339]`), in UTC, to the second, ending in `Z`, as `YYYY-MM-DDThh:mm:ssZ`, so stamps written on different machines compare without a time zone.
- **The content hash —** SHA-256 of the file's text, encoded as UTF-8 with line-feed line endings, after dropping the lines that hold the fields the form leaves out; written as `sha256:` followed by the digest's first sixteen hexadecimal characters, lower case. It detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding it and the fields it leaves out: its own field always, since writing the stamp must not change the hash, and any field whose change the check does not concern, as a design document's Validated field leaves out its Status (`§ A Design Document`).

## A Follow-up

A follow-up records work on the specs or the code that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. `.ai/follow-ups.md` opens with a short header naming what the file holds and citing this file, and its follow-ups follow that header. Each sits under a priority heading: `## High`, the work to take up next; `## Medium`, which waits until High is settled; or `## Low`, worth doing once nothing more pressing is open. Each holds its parts, in this order:

**Reference Key:** Part

**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `###` heading, a kebab-case slug | yes | | the name the follow-up is referred to by |
| Status | a `**Status:**` field | yes | | where the follow-up is in this section's lifecycle |
| Category | a `**Category:**` field | yes | | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` field | yes | | the file, section or files it concerns |
| Body | prose | yes | | the work, the context needed to take it up, and, where known, what found it |

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| not-started | recorded, and not yet taken up | Yes | No |
| in-progress | taken up, usually as a design document | No | No |
| done | resolved, and removed from the file | No | Yes |

**Table Name:** Transitions

| From | To | Trigger |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | not-started | `§ A Design Document § The States It Moves Through [States.State: abandoned]` of the design document taking it up is entered |
| in-progress | done | the change that resolves it lands |
| in-progress | done | the user decides nothing needs to change |
| not-started | done | a change made for another reason resolves it |
| not-started | done | the user decides nothing needs to change |
