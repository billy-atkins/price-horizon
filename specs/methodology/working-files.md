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
| Depends On | a `**Depends On:**` field | the design documents that must finish before this one is applied, separated by semicolons, or none |
| Validated | a `**Validated:**` field | the stamp its validation review left, per `§ A Stamp`, leaving out the Validated and Status fields, or none; current while the design is approved |
| The Problem | a `## The Problem` section | what is wrong, stated on its own, before any fix |
| Scope | a `## Scope` section | how the sweep for affected content was done and what it found, what it left out included |
| Steering Decisions | a `## Steering Decisions` record section, once the user has steered the design | each steer the user gave, per `§ A Steering Decision` |
| The Design | a `## The Design` section | what the design does, then each edit, introduced by a bold lead-in naming the file it edits (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) and quoting exactly the text it replaces or follows, so it can be verified and applied as written |
| The Builder's Passes | a `## The Builder's Passes` section | what each pass and each review changed, each under a bold lead-in naming it, an adversarial DRR's opening `Adversarial DRR`, and each review named with its report |
| Deliberately Left Alone | a `## Deliberately Left Alone` section | each change considered and declined, with the reason, and each piece of work deferred, named by the design document spawned for it or the follow-up logging it |

**Spawning keeps a design focused —** work a design turns up that is a change of its own, a migration of files a rule change leaves out of step among them, is spawned as a design document of its own or logged as a follow-up (`§ A Follow-up`), as the user decides, since which suits depends on how the user means to work it. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change; the design's scope still sweeps what the spawned change touches, and only its edits move. A spawned design without which the design it came from cannot finish blocks that design, and is named in that design's Depends On; one that can be worked before or after it does not. Depends On is the one record of what blocks what, and names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks back to the design it began from.

**Blocked and to revise are read, not recorded —** a design finishes when it is complete or abandoned. A design is blocked while its Depends On names a design that has not finished; it may be worked and approved while blocked, but not applied. Once a design its Depends On names finishes, the design takes in what that one settled, or why it was dropped, and removes it from Depends On, an approved design going back to in-progress to do so. Blocked and to revise are read from the Status of the designs its Depends On names, so a design finishing changes no other design's file.

**Unwinding —** a finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. An open design spawned by one abandoned goes on as a design of its own or is abandoned with it, as the user decides, and a Spawned By naming a design since deleted stays as its history.

**A validation review holds it to this form —** before the user is asked to approve a design, a cold agent other than the builder checks the document against this section and `§ A Steering Decision`: for what the design script decides, and by reading for what it cannot, each steer recorded as a steering decision in the user's words rather than paraphrased or left in The Builder's Passes, and each Decision borne out by the design as it stands, the Source holding the request that opened the design, each piece of deferred work naming a follow-up or a design document that exists, each review in the passes named with its report, and Scope saying how its sweep was done. It reports what it finds, and edits nothing but the Validated field, which it stamps once the document passes; the stamp is its record in the design, its report named in no pass, since naming it would change what it stamped. The adversarial DRR reviews the design, and the validation review the record of it, so each keeps its own focus. A design changed after its stamp no longer matches it, so a stale validation is read from the file and never cleared by hand.

A change needing both kinds is two design documents, the application one depending on the canon one. Work the change defers is spawned or logged when it is deferred, not when the design completes.

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | No |
| in-progress | under the builder's passes, a review, or taking in a design it waited on | No |
| approved | converged, reviewed, and approved by the user, and not yet applied | No |
| applying | its edits being written, and its post-apply audit and what that asks for under way | No |
| complete | applied, its audit settled; what it decided lives on in the specs it changed | Yes |
| abandoned | withdrawn by the user | Yes |

Transitions:

| From | To | Trigger or condition |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | approved | its adversarial DRR, and another after a revision that changed its structure, as `specs/AGENTS.md § Design, Refactor, Refine (DRR)` has one, is taken in, its validation review has stamped it, and the user approves it |
| approved | in-progress | a design its Depends On names finishes, or the user reopens it |
| approved | applying | the user gives the go-ahead to apply, and its Depends On names none |
| applying | complete | its edits are written, and its post-apply audit and the fixes that asks for are settled |
| not-started | abandoned | the user abandons it |
| in-progress | abandoned | the user abandons it |
| approved | abandoned | the user abandons it |
| applying | abandoned | the user abandons it, and the edits it wrote are reverted |

## A Steering Decision

Each steer the user gives a design while it is shaped or reviewed is recorded when it is given, and the design is revised to apply it before the work goes on, so the design carries the journey that settled it and never lags a steer it records: the adversarial DRR reads it as background, checking fidelity to it rather than reopening it, and a later revision does not reopen what the user decided. The request that opened the design is its Source, and The Builder's Passes record what each pass changed, not what the user decided, so each steer is recorded once. Its records sit in a design document's record section titled Steering Decisions. It is a Record Form (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) whose type is named Steering Decisions:

| Field | Identifies | Holds |
|---|---|---|
| Name | yes | a short name for what was decided |
| Prompted By | no | what the steer answered: a question, proposal or account the builder gave, a review's finding named by its ID, or the user's own initiative |
| Steer | no | the user's own words, quoted |
| Decision | no | what the steer settles for the design, as the design now applies it |

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
