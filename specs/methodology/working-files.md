## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`. What a working file settles reaches a reader only through the spec it changes.

| File | Holds |
|---|---|
| `.ai/plans/` | the plans the skills write, a design document among them (`§ A Design Document`) |
| `.ai/follow-ups.md` | work on the specs that should be done and is not yet, each as a follow-up (`§ A Follow-up`) |
| `.ai/tmp/` | the skills' own output, review and audit reports among it |

**A skill's scratch space is `.ai/tmp/<skill-name>/` —** created by the skill if it is not there. One directory per skill so that one skill's output is never mistaken for another's, and under `.ai/tmp/` so none of it is ever committed. A skill does not delete its own output when it finishes: the output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its own *stale* output, the file left behind from a previous run that no longer corresponds to anything, since a reader has no way to tell that from a current one.

**A skill's plans are `.ai/plans/<skill-name>/` —** a skill describing a change before making it writes each plan to a file of its own there, created by the skill if it is not there. One directory per skill so that one skill's plans are never mistaken for another's, and one file per plan so each is read, reviewed and handed to a cold agent whole.

`.ai/follow-ups.md` opens with a short header naming what the file holds and citing this file, and its follow-ups follow that header.

An open question about what is specified is not a working file's to hold; it is recorded in a spec, per `specs/methodology/spec-placement.md § An Open Question`.

## A Design Document

`.ai/skills/design-specs/` writes each design document to a file of its own under `.ai/plans/design-specs/`, one per change taken through `specs/AGENTS.md § Design, Refactor, Refine (DRR)`. That skill's steps and script hold it to this form, and no audit reads it. It opens with a level-one heading, `Design Document`, whose section holds its fields (`specs/methodology/modeling-constructs.md § Fields`), and its sections follow as level-two headings. It holds its parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Name | a `**Name:**` field | the change, in a few words; the file is named for it in kebab-case, lower case with each run of other characters a hyphen, and other design documents name this one by that file name, without its extension |
| Status | a `**Status:**` field | its state in this section's lifecycle |
| Source | a `**Source:**` field | what asked for the change: the user's own words, or the finding that raised it |
| Specs | a `**Specs:**` field | the kind of file the change is bounded to, settled while the design is shaped and before any file is edited: `canon`, `specs/AGENTS.md` and the files under `specs/methodology/` and a registered skill's directory; `application`, the files under `specs/application/`; or `neither`, any other file. Every file its Target names is of the declared kind or of `neither` |
| Target | a `**Target:**` field | every file the change edits, each a path in backticks, separated by semicolons; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | the design document this one was spawned from, or none |
| Depends On | a `**Depends On:**` field | the design documents that must be approved or applying before this one is validated and approved, and must finish before it is applied, separated by semicolons, or none |
| Validated | a `**Validated:**` field | the stamp its validation review left, per `§ A Stamp`, leaving out the Validated and Status fields, or none; current while the design is approved |
| The Problem | a `## The Problem` section | what is wrong, stated on its own, before any fix |
| Scope | a `## Scope` section | how the sweep for affected content was done and what it found, what it left out included |
| Steering Decisions | a `## Steering Decisions` record section, once the user has steered the design | each steer the user gave, per `§ A Steering Decision` |
| The Design | a `## The Design` section | what the design does, then each edit, introduced by a bold lead-in naming the file it edits (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) and quoting exactly the text it replaces or follows, so it can be verified and applied as written |
| Impact on the Application Specs | a `## Impact on the Application Specs` section, in a canon design and no other | each application file and section the canon change leaves out of step, what it leaves out of step there and what the application work must do, or that none was found; and how the application specs were reviewed |
| The Builder's Passes | a `## The Builder's Passes` section | what each pass and each review changed, each under a bold lead-in naming it, an adversarial DRR's opening `Adversarial DRR` and a post-apply audit's `Post-apply audit`, each review named with its report, and each of those two with the model and reasoning effort it ran on, in the form `on {model} at {effort} effort`, the effort one of the levels `specs/AGENTS.md § Design, Refactor, Refine (DRR)` names, or `on {model} as the agent allows` where the agent could not apply the reasoning effort chosen; and, in each of those two, the flaws the user settled among its findings |
| Deliberately Left Alone | a `## Deliberately Left Alone` section | each change considered and declined, with the reason, and each piece of work deferred, named by the design document spawned for it or the follow-up logging it |

**Spawning keeps a design focused —** work a design turns up that is a change of its own, a migration of files a rule change leaves out of step among them, is spawned as a design document of its own or logged as a follow-up (`§ A Follow-up`), as the user decides, since which suits depends on how the user means to work it. It is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change; the design's scope still sweeps what the spawned change touches, and only its edits move. A spawned design without which the design it came from cannot finish blocks that design, and is named in that design's Depends On; one that can be worked before or after it does not. Depends On is the one record of what blocks what, and names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks back to the design it began from.

**Blocked and to revise are read, not recorded —** a design finishes when it is complete or abandoned. A design is blocked while its Depends On names a design that has not finished; it may be worked while blocked, and is validated and approved only once each design its Depends On names is approved or applying, a finished one taken in and removed first, so designs that build on each other can be shaped and approved before any of them is applied; it is applied only once its Depends On names none, so they apply in dependency order. Where a design goes back to in progress, the builder moves back each approved design whose Depends On names it. Once a design its Depends On names finishes, the design goes back to in progress if it is approved, takes in what that one settled, or why it was dropped, against the files as they stand once it finishes, and removes it from Depends On. Blocked and to revise are read from the Status of the designs its Depends On names, never recorded in the design itself.

**Unwinding —** a finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. An open design spawned by one abandoned goes on as a design of its own or is abandoned with it, as the user decides, and a Spawned By naming a design since deleted stays as its history.

**A validation review holds it to this form —** before the user is asked to approve a design, a cold agent other than the builder checks the document against this section and `§ A Steering Decision`: for what the design script decides, and by reading for what it cannot, each steer recorded as a steering decision in the user's words rather than paraphrased or left in The Builder's Passes, nothing recorded as one that `§ A Steering Decision` calls no steer, and each Decision borne out by the design as it stands, the Source holding the request that opened the design, each piece of deferred work naming a follow-up or a design document that exists, each review in the passes named with its report, Scope saying how its sweep was done, and a canon design's Impact on the Application Specs how its review was. It reports what it finds, and edits nothing but the Validated field, which it stamps once the document passes; the stamp is its record in the design, its report named in no pass, since naming it would change what it stamped. The adversarial DRR reviews the design, and the validation review the record of it, so each keeps its own focus. A design changed after its stamp no longer matches it, so a stale validation is read from the file and never cleared by hand.

**A change needing both kinds is split —** its canon design reviews the application specs for what it leaves out of step there, records that in its Impact on the Application Specs, and edits none of them. That application work goes to the application design the canon design was spawned from, where there is one, or else is spawned or logged as this section's spawning paragraph has it. The two may be worked in concert. What the canon design's post-apply audit finds in the application specs is application work too, added to what its review handed on or handed on the same way, so the canon design completes without editing them. Where the application work finds the canon design wrong, the canon design takes the change while it is in progress or approved, the user reopening an approved one. For any other canon change the application work needs, the canon design's change among them once it is applying or complete, the application design spawns a canon design, which blocks it, the user reopening the application design first where it is approved. An application design already applying keeps to what was approved, the canon change spawned or logged without blocking it, as the user decides.

**Changes after approval —** once the user approves a design, every change it makes to the files is one the user approved and one the design describes. Each finding of its post-apply audit is presented to the user and settles one way. A tactical fix is made as a direct edit once the user approves it (`specs/AGENTS.md § Design, Refactor, Refine (DRR)`), and recorded in the audit's pass. A canon design's finding in the application specs is application work, handed on as this section's paragraph on a change needing both kinds has it. A finding the user judges wrong is set aside, and recorded in the pass with the reason. And a finding that exposes a flaw in the design, or a fix the user does not approve, sends the design back to in progress: its changes to the files are reverted, and it is revised and worked afresh from the files as they stood before its apply, with what was learned. A design's apply begins only once nothing else is uncommitted and no other design is applying in the same checkout, and its changes are committed on their own, one commit for each design, even where a branch holds several, so that a revert takes exactly that design's changes; where the project has no version control, its changes are reverted by hand. A design stays applying until the user approves its commit.

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | No |
| in-progress | under the builder's passes or a review, waiting on a design its Depends On names, or taking in one that finished | No |
| approved | converged, reviewed, and approved by the user, and not yet applied | No |
| applying | its edits being written, and its post-apply audit and what that asks for under way | No |
| complete | applied, its audit settled; what it decided lives on in the specs it changed | Yes |
| abandoned | withdrawn by the user | Yes |

Transitions:

| From | To | Trigger or condition |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | approved | its adversarial DRR, and another after a revision that changed its structure, as `specs/AGENTS.md § Design, Refactor, Refine (DRR)` has one, is taken in, its validation review has stamped it, each design its Depends On names is approved or applying, and the user approves it |
| approved | in-progress | the user reopens it, a design its Depends On names goes back to in progress, or one finishes, to take it in |
| approved | applying | the user gives the go-ahead to apply, and its Depends On names none |
| applying | in-progress | a finding of its post-apply audit exposes a flaw in the design, or the user does not approve its fix; its changes to the files are reverted |
| applying | complete | its edits are written, each finding of its post-apply audit is settled without sending it back to in progress, and its changes are committed on their own where the project has version control |
| not-started | abandoned | the user abandons it |
| in-progress | abandoned | the user abandons it |
| approved | abandoned | the user abandons it |
| applying | abandoned | the user abandons it, and the edits it wrote are reverted |

## A Steering Decision

Steering Decisions record only the user's steers, the decisions a steering decision records (`specs/methodology/glossary.md`), new scope or a flaw's fix among them. The user's direction about how the work proceeds, and tactical adjustments that leave the design as it is, are no steer; and a decision about other work is no steer of the design being worked. They differ so:

| | A steer | Direction about the work | A decision about other work |
|---|---|---|---|
| Sounds like | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found" | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "create the branch", "medium effort", "G1 to G6 are flaws" | "the implement-specs design should weigh renaming the workstack", "keep the query service read-only when we design it" |
| Recorded | in Steering Decisions, its Steer quoting the words that decide the design | not as a steer; where the record needs it, in the passes, as the Builder's Passes row of `§ A Design Document` has them, or in the Status field | where that work is held |
| Tells a reviewer | how the design was formed | nothing about what the design is | nothing about the design being worked |

A go-ahead to take in findings is a steer for those that change what the design is and direction for the tactical ones, and an answer carrying both is recorded for the part that decides the design. A decision about other work is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory. Where a design not yet approved holds the work, the decision is its steer, applied when that design is worked. Where an approved or applying design holds it, the user is asked whether to reopen that design for it, an applying one only as a flaw in what it applies (`§ A Design Document`): reopened, the design takes it as its steer; not reopened, the decision is dropped, or, where the user wants it kept for later, logged as a follow-up. Where only a follow-up holds the work (`§ A Follow-up`), the decision goes in its body, and the design taking up the follow-up records it as its steer. Where nothing holds the work, the user chooses between a not-started design recorded for it, the decision its Source where it asks for the work and its steer otherwise, and a new follow-up. A decision about more than one design is recorded in each. Each steer is recorded when it is given, and the design is revised to apply it before its work goes on, so the design carries how it was formed and never lags a steer it records: the adversarial DRR reads the steers as background, checking fidelity to them rather than reopening them, and a later revision does not reopen what the user decided. The request that opened the design is its Source, and The Builder's Passes record what each pass changed and the direction the record needs, never a steer, so each steer is recorded once. Its records sit in a design document's record section titled Steering Decisions. It is a Record Form (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) whose type is named Steering Decisions:

| Field | Identifies | Holds |
|---|---|---|
| Name | yes | a short name for what was decided |
| Prompted By | no | what the steer answered: a question, proposal or account the builder gave, a review's finding named by its ID, or the user's own initiative |
| Steer | no | the user's own words, quoted |
| Decision | no | what the steer settles for the design, as the design applies it |

## A Stamp

A stamp records that a check passed, when, and on what content, so a later reader can tell whether the content changed since, and nothing has to be cleared by hand. It is a field's value, a UTC timestamp and a content hash separated by a space, `2026-09-29T14:05:12Z sha256:3f9a0c1b2d4e5f60`:

- **The timestamp —** ISO 8601 in UTC, to the second, ending in `Z`, as `YYYY-MM-DDThh:mm:ssZ`, so stamps written on different machines compare without a time zone.
- **The content hash —** SHA-256 of the file's text encoded as UTF-8, its line endings a line feed, with the lines holding the fields the form leaves out dropped; written as `sha256:` and the digest's first sixteen hexadecimal characters, lower case. It detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding it and the fields it leaves out: its own field always, since writing the stamp must not change the hash, and any field whose change the check does not concern, as a design document's Validated field leaves out its Status (`§ A Design Document`).

## A Follow-up

A follow-up records work on the specs that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. Each sits under a priority heading: `## High`, the work to take up next; `## Medium`, which waits until High is settled; or `## Low`, worth doing once nothing more pressing is open. Each holds its parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Name | a `###` heading, a kebab-case slug | the name the follow-up is referred to by |
| Status | a `**Status:**` line | where the follow-up is in this section's lifecycle |
| Category | a `**Category:**` line | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` line | the file, section or files it concerns |
| Body | prose | the work, the context needed to take it up, and, where known, what found it |

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, and not yet taken up | No |
| in-progress | taken up, usually as a design document | No |
| done | resolved, and removed from the file | Yes |

Transitions:

| From | To | Trigger or condition |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | not-started | the design document taking it up is abandoned |
| in-progress | done | the change that resolves it lands, or the user decides nothing needs to change |
| not-started | done | a change made for another reason resolves it, or the user decides nothing needs to change |
