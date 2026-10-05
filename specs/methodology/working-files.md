## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`. What a working file settles reaches a reader only through the spec it changes.

| File | Holds |
|---|---|
| `.ai/plans/` | the plans the skills write, a design document among them (`§ A Design Document`) |
| `.ai/follow-ups.md` | work on the specs or the code that should be done and is not yet, each as a follow-up (`§ A Follow-up`) |
| `.ai/tmp/` | the skills' own output, review and audit reports among it |

**A skill's scratch space is `.ai/tmp/<skill-name>/` —** created by the skill if it is not there. One directory per skill so that one skill's output is never mistaken for another's, and under `.ai/tmp/` so none of it is ever committed. A skill does not delete its own output when it finishes: the output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its own *stale* output, the file left behind from a previous run that no longer corresponds to anything, since a reader has no way to tell that from a current one.

**A skill's plans are `.ai/plans/<skill-name>/` —** a skill describing a change before making it writes each plan to a file of its own in that directory, creating the directory if it is not there. One directory per skill so that one skill's plans are never mistaken for another's, and one file per plan so each is read, reviewed and handed to a cold agent whole.

An open question about what is specified is not a working file's to hold; it is recorded in a spec, per `specs/methodology/spec-placement.md § An Open Question`.

## A Design Document

Each design document is a file of its own, one per change taken through `specs/AGENTS.md § Design, Refactor, Refine`. `.ai/skills/design-specs/` writes each design changing the specs under `.ai/plans/design-specs/`, and `.ai/skills/implement-specs/` each design changing code under `.ai/plans/implement-specs/`. Both take this form; a design changing code differs only where `§ A Design Document § A Design Changing Code` sets. Each skill's steps and its script hold a design to this form, the script reaching the design document tooling the two skills share, and no audit reads a design. A design opens with a level-one heading, `Design Document`, whose section holds its fields (`specs/methodology/modeling-constructs.md § Fields`), and its sections follow as level-two headings. It holds its parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Name | a `**Name:**` field | the change, in a few words. The file is named for it in kebab-case: lower case, each run of other characters a hyphen. Other design documents name this one by that file name without its extension; one in another skill's plans folder puts this design's folder name and a slash before it, as `design-specs/{file name}` |
| Status | a `**Status:**` field | its state in this section's state machine |
| Source | a `**Source:**` field | what asked for the change: the user's own words, or the finding that raised it |
| Specs | a `**Specs:**` field | the kind of file the change is bounded to, one of the kinds this section's table of kinds gives, settled while the design is shaped and before any file is edited |
| Target | a `**Target:**` field | every file the change edits, each a path in backticks, separated by semicolons; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | the design document this one was spawned from, or none |
| Depends On | a `**Depends On:**` field | the design documents that block this one, separated by semicolons, or none; what blocks a design, and when, is set by this section's paragraphs on what blocks what and on blocked and to revise |
| Validated | a `**Validated:**` field | the stamp its validation review left, per `§ A Stamp`, leaving out the Validated and Status fields, or none; current while the design is approved |
| The Problem | a `## The Problem` section | what is wrong, stated on its own, before any fix |
| Scope | a `## Scope` section | how the sweep for affected content was done and what it found, what it left out included |
| Steering Decisions | a `## Steering Decisions` record section, once the user has steered the design | each steer the user gave, per `§ A Steering Decision` |
| The Design | a `## The Design` section | what the design does, then each edit, introduced by a bold lead-in naming the file it edits (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) and quoting exactly the text it replaces or follows, so it can be verified and applied as written |
| Impact on the Application Specs | a `## Impact on the Application Specs` section, in a canon design and no other | each application file and section the canon change leaves out of step, what it leaves out of step there and what the application work must do, or that none was found; and how the application specs were reviewed |
| The Builder's Passes | a `## The Builder's Passes` section | what each pass and each review changed, each under a bold lead-in naming it, and each review named with its report. An adversarial review's lead-in opens `Adversarial review`, and a post-apply audit's `Post-apply audit`. Each of those two names the model and reasoning effort it ran on, as `on {model} at {effort} effort`, the effort one of the levels `specs/AGENTS.md § Design, Refactor, Refine` names, or as `on {model} as the agent allows` where the agent could not apply the effort chosen, and records the flaws the user settled among its findings |
| Deliberately Left Alone | a `## Deliberately Left Alone` section | each change considered and declined, with the reason, and each piece of work deferred, named by the design document spawned for it or the follow-up logging it |

**The kinds, a Decision Table of what each bounds a change to —**

| Specs | Bounds the change to |
|---|---|
| `canon` | `specs/AGENTS.md`, the files under `specs/methodology/`, a registered skill's directory, and `.ai/skills/lib/` |
| `application` | the files under `specs/application/` |
| `code` | the application's code, within the code roots the technical stack names (`specs/methodology/spec-placement.md § The Technical Stack`), which the application specs govern (`specs/methodology/code.md`); a design changing code's only kind |
| `neither` | any other file |

Every file a design's Target names is of its declared kind or of `neither`, or is code whose annotation lines alone it edits, as `specs/methodology/code.md § Changing Code` has a design retitling a heading.

**Spawning keeps a design focused —** when a design turns up work that is a change of its own, a migration of files a rule change leaves out of step among them, that work is spawned as a design document of its own or logged as a follow-up (`§ A Follow-up`), as the user decides, since which suits depends on how the user means to work it. It is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change; the design's scope still sweeps what the spawned change touches, and only its edits move.

**Depends On records what blocks what —** a spawned design without which the design it came from cannot finish blocks that design, and is named in that design's Depends On; one that can be worked before or after it does not. Depends On is the one record of what blocks what, and names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks, back toward the design it began from.

**Blocked and to revise are read, not recorded —** a design finishes when it is complete or abandoned. A design is blocked while its Depends On names a design that has not finished, and is to revise once one it names has finished; both are read from the Status of the designs its Depends On names, never recorded in the design itself. A blocked design may still be worked. A design is validated and approved only once each design its Depends On names is approved or applying, a finished one taken in and removed first, so designs that build on each other can be shaped and approved before any of them is applied. A design is applied only once its Depends On names none, so they apply in dependency order. Where a design goes back to in progress, the builder moves back each approved design whose Depends On names it. Once a design its Depends On names finishes, the design goes back to in progress if it is approved, takes in what that one settled, or why it was dropped, against the files as they stand once it finishes, and removes it from Depends On.

**Unwinding —** a finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. When a design is abandoned, each open design it spawned goes on as a design of its own, or is abandoned with it, as the user decides. A Spawned By naming a design since deleted stays, as the spawned design's history.

**A validation review holds it to this form —** before the user is asked to approve a design, a cold agent other than the builder checks the document against this section and `§ A Steering Decision`, through the design script for what it decides and by reading for what it cannot:

- each steer is recorded as a steering decision in the user's words, not paraphrased or left in The Builder's Passes, and nothing is recorded as one that `§ A Steering Decision` calls no steer;
- each Decision is borne out by the design as it stands;
- the Source holds the request that opened the design;
- each piece of deferred work names a follow-up or a design document that exists;
- each review in the passes is named with its report;
- Scope says how its sweep was done, and a canon design's Impact on the Application Specs how its review was.

It reports what it finds, and edits nothing but the Validated field, which it stamps once the document passes. The stamp is its record in the design, and its report is named in no pass, since naming it would change what it stamped. The adversarial review reviews the design, and the validation review the record of it, so each keeps its own focus. A design changed after its stamp no longer matches it, so a stale validation is read from the file and never cleared by hand.

**A change needing both kinds is split —** its canon design reviews the application specs for what it leaves out of step there, records that in its Impact on the Application Specs, and edits none of them. That application work goes to the application design the canon design was spawned from, where there is one, or else is spawned or logged as this section's spawning paragraph has it, and the canon and application designs may be worked in concert. A design changing the specs that leaves code out of step edits none of the code either: it records the code its change leaves out of step in its Scope, and that work goes to a design changing code, spawned or logged the same way. What the canon design's post-apply audit finds in the application specs settles by this section's table of changes after approval, and what that table hands on is application work too, added to what its review handed on or handed on the same way, so the canon design completes without editing them. Where the application work finds the canon design wrong, the canon design takes the change while it is in progress or approved, the user reopening an approved one. For any other canon change the application work needs, a change to the canon design once that design is applying or complete among them, the application design spawns a canon design, which blocks it, the user reopening the application design first where it is approved. An application design already applying keeps to what was approved, the canon change spawned or logged without blocking it, as the user decides.

**Changes after approval —** once the user approves a design, every change it makes to the files is one the user approved and one the design describes. Each finding of its post-apply audit is presented to the user, and settles by what it is, in a Decision Table whose hit policy is First:

| Finding | Settles |
|---|---|
| one the user judges wrong | set aside, and recorded in the pass with the reason |
| one exposing a flaw in the design, or proposing a tactical fix to the design's own edits that the user does not approve | sends the design back to in progress: its changes to the files are reverted, and it is revised and worked afresh from the files as they stood before its apply, with what was learned |
| a canon design's, in the application specs | handed on as application work, as this section's paragraph on a change needing both kinds has it |
| one outside the design's own edits | settled as the user chooses, and recorded in the pass: folded in as a direct edit (`specs/AGENTS.md § Design, Refactor, Refine`); dropped; logged as a follow-up; or given a design, one of its own, standing apart or spawned from this one, or an existing design not yet applied taking it in, as `§ A Steering Decision` records a decision about other work |
| a tactical fix the user approves | made as a direct edit (`specs/AGENTS.md § Design, Refactor, Refine`), and recorded in the audit's pass |

**Applying and committing —** a design's apply begins only once nothing else is uncommitted and no other design is applying in the same checkout. Its changes are committed on their own, one commit for each design even where a branch holds several, so a revert takes exactly that design's changes; where the project has no version control, they are reverted by hand. A design abandoned while applying has the edits it wrote reverted.

A State Machine. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | No |
| in-progress | under the builder's passes or a review, waiting on a design its Depends On names, taking in one that finished, or, its work done, awaiting the user's approval | No |
| approved | converged, reviewed, and approved by the user, and not yet applied, awaiting the go-ahead to apply | No |
| applying | its edits being written, its post-apply audit and what that asks for under way, and, where the project has version control, its commit awaiting the user's approval | No |
| complete | applied, its audit settled; what it decided lives on in the specs it changed | Yes |
| abandoned | withdrawn by the user | Yes |

Transitions:

| From | To | Trigger | Guard |
|---|---|---|---|
| not-started | in-progress | the work is taken up | none |
| in-progress | approved | the user approves it | its adversarial review is taken in, with another after any revision that changed its structure (`specs/AGENTS.md § Design, Refactor, Refine`), its validation review has stamped it, and each design its Depends On names is approved or applying |
| approved | in-progress | the user reopens it, a design its Depends On names goes back to in progress, or one finishes | none |
| approved | applying | the user gives the go-ahead to apply | its Depends On names none |
| applying | in-progress | a finding of its post-apply audit exposes a flaw in the design, or proposes a tactical fix to the design's own edits that the user does not approve | none |
| applying | complete | the user approves its commit | its edits are written, and each finding of its post-apply audit is settled without sending it back to in progress |
| applying | complete | none | its edits are written, each finding of its post-apply audit is settled without sending it back to in progress, and the project has no version control |
| not-started | abandoned | the user abandons it | none |
| in-progress | abandoned | the user abandons it | none |
| approved | abandoned | the user abandons it | none |
| applying | abandoned | the user abandons it | none |

### A Design Changing Code

A design changing code starts from applied specs, or from the specs as a design its Depends On names leaves them, rather than from a problem in them, and designs the code and the tests that bring them to life. It takes the form `§ A Design Document` sets, and Design, Refactor, Refine, the adversarial review, the validation review and the stamp, as a design changing the specs does, and differs only where code does. Its parts differ so:

| Part | In a design changing code |
|---|---|
| The Problem | names the product module it carries out, then the specs it carries into code, cited, and what the code lacks |
| Specs | `code` |
| The Design | describes each unit of governed code it writes or changes, with the app-spec annotations it carries (`specs/methodology/code.md § Citing the Specs From Code`), the wiring that connects the units (`specs/methodology/code.md § Governed Code and Wiring Code`), and the tests that check the specs (`specs/methodology/code.md § Tests`), quoting existing code only where it changes it |

**One product module —** it carries out one product module, reading what `specs/methodology/spec-placement.md § A Product Module` sets, in the order `specs/methodology/scope.md § Progressive Disclosure` sets. Work reaching several modules is a design for each. A technical section several modules need, a shared data model's, say, is carried out by the first design changing code that takes it up; a later design names that one in its Depends On while it is unfinished, and builds on its code once it is applied.

**The builder designs, the user steers —** the builder designs the code from the specs on its own, the specs being its starting point, and the user approves the design or steers it. A steer about how the code carries out the specs is this design's. A steer changing what a spec states is spawned as a design changing the specs and named in this design's Depends On, so this design waits on it, per `§ A Design Document`'s paragraph on blocked and to revise, and takes it in once it finishes, revised against the specs as they then stand.

Its post-apply audit is `.ai/skills/verify-spec-implementation/`, reading the code it wrote as `.ai/skills/audit-specs/` reads the specs a design changed.

## A Steering Decision

A design's Steering Decisions record only the user's steers, the decisions a steering decision records (`specs/methodology/glossary.md`), new scope or a flaw's fix among them. A steer differs from the user's direction about how the work proceeds, and from a decision about other work, which is no steer of the design being worked. How each is recorded, an answer carrying more than one taken a part at a time, is a Decision Table:

| What the user decides | Recorded | Tells a reviewer | Sounds like |
|---|---|---|---|
| A steer | in Steering Decisions, its Steer quoting the words that decide the design | how the design was formed | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found" |
| Direction about the work | not as a steer; where the record needs it, in the passes, as the Builder's Passes row of `§ A Design Document` has them, or in the Status field | nothing about what the design is | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "create the branch", "medium effort", "G1 to G6 are flaws" |
| A decision about other work | where that work is held | nothing about the design being worked | "the implement-specs design should weigh renaming the workstack", "keep the billing service stateless when we design it" |

**A go-ahead to take in findings —** is a steer for the findings that change what the design is and direction for the tactical ones; an answer carrying both is recorded for the part that decides the design.

**A decision about other work —** is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory, and a decision about more than one design is recorded in each. What becomes of the decision, by where the work is held, is a Decision Table:

| Where the work is held | The decision |
|---|---|
| a not-started or in-progress design | is its steer, applied when that design is worked |
| an approved or applying design | is put to the user, who decides whether to reopen that design for it, an applying one only as a flaw in what it applies (`§ A Design Document`): reopened, the design takes it as its steer; not reopened, it is dropped, or, where the user wants it kept for later, logged as a follow-up |
| a follow-up (`§ A Follow-up`), and no open design | goes in the follow-up's body, and the design taking up the follow-up records it as its steer |
| no follow-up, and no open design, only a complete or abandoned design or nothing | the user chooses between a not-started design recorded for it, the decision its Source where it asks for the work and its steer otherwise, and a new follow-up |

**Each steer is recorded when it is given —** and the design is revised to apply it before its work goes on, so the design carries how it was formed and never lags a steer it records. The adversarial review reads the steers as background, checking fidelity to them rather than reopening them, and a later revision does not reopen what the user decided. The request that opened the design is its Source, and The Builder's Passes record what each pass changed, never a steer, so each steer is recorded once.

A design's steering decisions sit in its record section titled `Steering Decisions`, each a record in the Record Form (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) of the type named Steering Decisions:

| Field | Identifies | Holds |
|---|---|---|
| Name | yes | a short name for what was decided |
| Prompted By | no | what the steer answered: a question, proposal or account the builder gave, a review's finding named by its ID, or the user's own initiative |
| Steer | no | the user's own words, quoted |
| Decision | no | what the steer settles for the design, as the design applies it |

## A Stamp

A stamp lets a later reader tell whether content has changed since a check passed on it, so nothing has to be cleared by hand. It is written as a UTC timestamp and a content hash separated by a space, `2026-09-29T14:05:12Z sha256:3f9a0c1b2d4e5f60`:

- **The timestamp —** ISO 8601 in UTC, to the second, ending in `Z`, as `YYYY-MM-DDThh:mm:ssZ`, so stamps written on different machines compare without a time zone.
- **The content hash —** SHA-256 of the file's text, encoded as UTF-8 with line-feed line endings, after dropping the lines that hold the fields the form leaves out; written as `sha256:` followed by the digest's first sixteen hexadecimal characters, lower case. It detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding it and the fields it leaves out: its own field always, since writing the stamp must not change the hash, and any field whose change the check does not concern, as a design document's Validated field leaves out its Status (`§ A Design Document`).

## A Follow-up

A follow-up records work on the specs or the code that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. `.ai/follow-ups.md` opens with a short header naming what the file holds and citing this file, and its follow-ups follow that header. Each sits under a priority heading: `## High`, the work to take up next; `## Medium`, which waits until High is settled; or `## Low`, worth doing once nothing more pressing is open. Each holds its parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Name | a `###` heading, a kebab-case slug | the name the follow-up is referred to by |
| Status | a `**Status:**` field | where the follow-up is in this section's lifecycle |
| Category | a `**Category:**` field | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` field | the file, section or files it concerns |
| Body | prose | the work, the context needed to take it up, and, where known, what found it |

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, and not yet taken up | No |
| in-progress | taken up, usually as a design document | No |
| done | resolved, and removed from the file | Yes |

Transitions:

| From | To | Trigger |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | not-started | the design document taking it up is abandoned |
| in-progress | done | the change that resolves it lands, or the user decides nothing needs to change |
| not-started | done | a change made for another reason resolves it, or the user decides nothing needs to change |
