---
name: design-specs
description: Propose or revise a specification, the canon or the application specs, as a design document under .ai/plans/design-specs/, a plan whose steps state outcomes, and write its text at the apply. Use when adding or changing a capability, a guarantee, a mechanism, a rule, a term or a skill, reconciling two documents that disagree, closing a gap an audit or review found, or taking a change through Design, Refactor, Refine, or running a Refactor and Refine cycle over specs that have landed, the canon's or the application's, the whole or a part. Its Workflow gives each rule it applies a point-of-use citation and forks at the kind of specification changed into a reference for that kind, and it covers the failures that recur in the work, duplicating a rule that already has a home, distorting a fact while compressing it, and citing a heading that does not exist.
---

# Designing specifications

Every fact in this repo is meant to live in exactly one place. Everywhere else that needs the fact points there. Most defects introduced here are not wrong statements. They are true statements written in a second place.

That is the difficulty. A sentence you are about to write is almost always correct on its own terms. The question is never "is this true" but "is this already stated, and is this where it belongs."

This skill does not restate the repo's conventions, since restating them would be the same defect the skill exists to prevent. It says where the conventions are, and what recurs when applying them.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The defects this skill's sections record get caught at the steps that find the fact's existing home, synchronize whatever restates what you changed, and verify citations mechanically.

Each step runs in the phase its work belongs to, and the steps read in the order a design's work runs (`specs/methodology/design-workflow.md § The Order of a Design's Work`). The steps through `§ Workflow § Refactor and refine, then the reviews and the approval` run before the plan's approval: they decide what changes, state it as each step's outcome, and check the plan. The steps from `§ Workflow § Write the text in the form the rules give it` on run at the apply: they write the text and check what was written. Where a decision has text to write, the deciding step states it in a plan step's Objectives, and a writing step writes it. A step saying when it runs, as `§ Workflow § Hand a change of its own to the user to spawn or log` does, runs then. A reference's step joins a step of the phase its work belongs to.

### Start from the entry point

Read `specs/AGENTS.md`, then `specs/methodology/glossary.md`, and a directory's `index.md` before working in it, per `specs/methodology/scope.md § Progressive Disclosure` and `specs/methodology/scope.md § The Shape of the Scope`.

### Frame the change

Frame the change per `specs/AGENTS.md § Design, Refactor, Refine`. Record it in a design document in `.ai/plans/design-specs/`, copied from `.ai/skills/design-specs/references/design-document-form-template.md`, per `specs/methodology/working-files.md § A Design Document`. The design document's Kind field settles the change's kind before any file is edited. The kind also sizes the design's reviews, as `specs/methodology/design-workflow.md § A Design's Reviews` has them.

Agree on the design goals with the user first, then present the design frame, as `specs/AGENTS.md § Design, Refactor, Refine` has them come first. Record the goals as `specs/methodology/working-files.md § Design Goal` has them. Draft the steps only once the user agrees on the goals and agrees to or adjusts the frame. Record each answer as a steer.

Before the frame goes to the user, the builder gathers each rule the change states in prose, across the passages `specs/methodology/modeling-constructs.md § When to Use Which` reads as one rule, widening the frame's Scope to any passage the gathering finds. The builder tests each rule by the count that section sets, and a rule in a construct section's prose by the test `specs/methodology/modeling-constructs.md § Defining Constructs` sets too, and the frame says which way each rule went. A close call, where either answer is arguable, goes to the user as a choice with the builder's recommendation, the canon's default where the canon gives one. The answer is recorded as a steer. A design bringing specs to the canon's forms may meet prose there that fails the test. The design writes that prose into a pass of the design that owns that construct's forms. Where no such design exists, it hands the prose to the user as `§ Workflow § Hand a change of its own to the user to spawn or log` has it. Either way, it records the prose as the Out of Scope row of `specs/methodology/working-files.md § A Design Document` has it.

Where the design's Depends On names a design, state in the frame's Scope what this design relies on from each, as `specs/methodology/working-files.md § A Design Document` has the Scope hold it.

A design taken up with its goals or its frame not yet stated has them stated, and agreed to or adjusted, before its drafting goes on. Set the design's Status as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` moves it, here and at each step that moves it. Where the work wants a new branch, propose it. Create the branch only once the user approves it, per `specs/AGENTS.md § Design, Refactor, Refine`. A Refactor and Refine cycle (`specs/methodology/glossary.md`) also reads `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md` here. That reference's steps join this Workflow's from this step on.

### Hand a change of its own to the user to spawn or log

At any step of this Workflow, each of these goes to the user, who decides how it is worked (`specs/methodology/working-files.md § A Design Document`):

- a change of its own that the work turns up, such as a migration of files that a rule change leaves out of sync;
- code that a change to the specs leaves out of sync, as `specs/methodology/working-files.md § A Design Document` splits it.

Each is either spawned as a design or logged as a follow-up, as `specs/methodology/working-files.md § A Design Document` has it, and a change to working files alone is logged. A spawned design is not-started until it is taken up, and it is named in this design's Depends On if this design cannot finish without it, this design's Scope then stating what it relies on from it (`specs/methodology/working-files.md § A Design Document`). Work this design leaves unaddressed is recorded as the Out of Scope row of `specs/methodology/working-files.md § A Design Document` has it. A follow-up takes the form `specs/methodology/working-files.md § A Follow-up` gives, its Body naming this design. Ask rather than choose, because which suits depends on how the user means to work it. Show the user the design's or the follow-up's text, new or amended, and write it only once the user approves it.

### Revise what waited, once what it waited on finishes

When `--show-workstack` lists a design to revise (`§ Verifying a proposal`), first, if it is approved, move the design back to in progress, and move back what depends on it, as `§ Workflow § Refactor and refine, then the reviews and the approval` has a design moved back. Its work then goes on as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it. Then take in what each finished design named in its Depends On settled, or why that design was dropped, per `specs/methodology/working-files.md § A Design Document`. Rerun `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever that changes. Record the revision in the design's passes, and remove each finished design from Depends On, and from the frame's Scope what the design relied on from it (`specs/methodology/working-files.md § A Design Document`). Then run `--show-workstack` again, and delete each design it lists as may be deleted.

### Record each steer and apply it

Record each steer the user gives the design, a decision about what the design is rather than about how the work proceeds, in the design's Steering Decisions when it is given, per `specs/methodology/working-files.md § Steering Decision`. Quote the user's words rather than paraphrasing them, because a paraphrase drifts toward what the builder meant. A reviewer reading the paraphrase as background then checks fidelity to a decision the user never made. Set the steer's Type as `specs/methodology/working-files.md § Steering Decision` has it.

Confirm a steer changing the goals or the frame with the user first, stating what it would change, as `specs/AGENTS.md § Design, Refactor, Refine` has it. Record any other steer as given. Then revise the design to apply the steer before the work goes on, rerunning `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever the steer changes. The steering decisions are the history of how the design was shaped. A design lagging them leaves its reviewers reading a decision the design does not yet carry out.

A decision about other work goes where that work is held, per `specs/methodology/working-files.md § Steering Decision`, never only into your own memory. Where an approved or applying design holds the work, ask the user whether to reopen that design for the decision. Where nothing holds the work, ask whether to record a design for it or log a follow-up.

### Fork on the kind of specification

Every change is of a kind, and this skill forks on the kind (`specs/AGENTS.md § Writing specs`). A change to the canon also reads `.ai/skills/design-specs/references/canon-specs.md`. A change to the application specs also reads `.ai/skills/design-specs/references/app-specs.md`. Each reference holds the steps only that kind owes, in the order its opening gives, and each of those steps names the step it joins, or the deciding step and the writing step.

A `code` change is `.ai/skills/implement-specs/`'s, not this skill's. A `documentation` change reads neither reference, and an `other` change reads neither, except a change editing the project's root `AGENTS.md`. That change reads the canon reference, whose step adding or changing a skill holds both `AGENTS.md` files to agent-agnostic instructions.

A change needing both kinds is split, per `specs/methodology/working-files.md § A Design Document`. A canon change finds what it leaves in the application specs as `.ai/skills/design-specs/references/canon-specs.md § Workflow` has it. An application change needing the canon hands that need on as `.ai/skills/design-specs/references/app-specs.md § Workflow` has it.

### Take up the persona of what the design changes

Write as the persona `specs/methodology/spec-placement.md § Personas` gives each specification, or the documentation, that the design changes, so the persona's judgment shapes the change from its first draft rather than arriving with a review.

### Find the fact's existing home

Grep before drafting, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`. If the fact has a home, the work is a citation, plus what that section asks of a citing place. In that case, `§ Workflow § Decide its altitude, and its file` through `§ Workflow § Record what the specs rely on but have not decided` do not apply.

### Decide its altitude, and its file

`specs/methodology/spec-placement.md § Index, Architecture, Detail` decides index versus architecture versus detail. `specs/methodology/spec-placement.md § Where a File Goes` decides which file, and where the file's row sits in its directory's `index.md`, which is the order it is read in. That section also decides the file's folder or, for a root file, the domain the product `architecture.md` names it under, which decides the product module the file belongs to (`specs/methodology/spec-placement.md § A Product Module`).

### Check whether a construct applies before writing prose

`specs/methodology/modeling-constructs.md § When to Use Which` decides whether a passage is a construct or prose, by the count it sets, and which construct it is. The decision covers routing too, however the routing reads. Gather a rule's passages before counting its facts, as that section reads a rule whole. `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct` decides which of a Decision Table, records and a Basic Table a table is. `specs/methodology/modeling-constructs.md § When to Use Which § A Configured Instance` decides the same where a construct's rows, states or steps are the system's data. `specs/methodology/modeling-constructs.md § When to Use Which § Combining Constructs` decides how one construct hands its work to another. `specs/methodology/modeling-constructs.md § Constructs` gives the form the construct is written in.

### Record what the specs rely on but have not decided

Record it as an open question, per `specs/methodology/spec-placement.md § Open Question`, in the Objectives of the step whose text relies on it, rather than hedging it inside settled prose.

### Draft with the source file open

Compare anything compressed from another file against that file clause by clause, rather than re-reading it in isolation. Before stating a step's outcome, zoom out and find the rule's reach, as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and name it in the step's What and in the Target. At the apply, write that reach whole, with each file open.

### State each step as its outcome

Write each step as a record of the type `specs/methodology/working-files.md § Design Plan Step` declares, in the design's Design Plan Steps. Its What names what it changes, its Why cites each goal it serves, and its Objectives state the state the applied work holds, as that section has an Objective, never the work to reach it. The prose around what a step changes is the standing Objective's, never listed in a step (`specs/methodology/working-files.md § A Design Document`).

### Verify mechanically

Run `.ai/skills/design-specs/scripts/design-specs.py`, per `§ Verifying a proposal`: `--check-cited-headings` for every heading the design cites, `--check-target-kind` for its Target against its Kind, and `--check-constructs` for each Decision Table or State Machine a step's Objectives state whole. Run them as part of your self-review, at drafting and before each validation. Settle each finding `--check-constructs` reports as any finding of your self-review, and read each candidate it lists. The design document's structure is the validation review's, run at validating. These are the expected reports:

- a heading a step adds, reported until the apply writes it;
- a construct's finding whose cause the same step's Objectives add;
- a heading added by a design that this design's Depends On names, where the frame's Scope states the design relies on it.

A design whose record uses a form not yet applied is validated by hand, as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding.

A design citing a heading that does not exist misleads its reviewer and its writer, however sound its reasoning. Anything the script cannot decide goes to a cold agent, as a judgment the builder hands off, per `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` and `§ Recall picks the direction; the file supplies the words`.

### Refactor and refine, then the reviews and the approval

Work the design in the order `specs/methodology/design-workflow.md § The Order of a Design's Work` gives, per `specs/AGENTS.md § Design, Refactor, Refine`. Rerun `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever each pass changes. What this skill adds at the states of `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design`, each named where it acts, in the order a design's work runs:

- **Design, Refactor, Refine of the steps.** At drafting, take the steps through the Design, Refactor, Refine process, and at changing, each step the change moved, a steer's change among them, as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it. Read the design against its problem, too, and against the rules this Workflow's steps apply.
- **Your self-review.** Then, at the end of drafting and of changing, before the design goes to validating, make your self-review for the adversarial review that follows, as your row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets. So the work runs Design, Refactor, Refine, your self-review, the validation, then the adversarial review.
- **Offering a review's model and effort.** At drafting, offer the user a review's model and effort once for a design, before its first adversarial review. Where the user's approval ends the review before any round, offer them before its post-apply review instead. The post-apply review and the audit start on the same choice, as `specs/AGENTS.md § Design, Refactor, Refine` has the choice kept. Offer two choices, each lettered with its default first. For effort: (a) the level the design's Kind gives (`specs/methodology/design-workflow.md § A Design's Reviews`) or (b) another, named in the answer. For model: (a) the one you run on or (b) another you can start a reviewer on, named in the answer. Offer only a level you can apply, as `specs/methodology/design-workflow.md § A Review's Effort` has it, and say which levels you cannot apply. Name the model and the effort in the review's pass.
- **The validation review.** At validating, run `--check-workstack` first, and put right what it reports, per `§ Verifying a proposal`. Then run the validation review: `--check-design` before an adversarial round, and `--stamp-validation` on the way to the user's approval, which stamps the design once it passes, in the form `specs/methodology/working-files.md § A Stamp` gives. Fix each problem the script reports and run it again. None of those problems is a question for the user. A design still validated, read with `--show-validation`, goes on as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it.
- **Starting the adversarial review.** At reviewing, start a cold agent with the brief `specs/methodology/design-workflow.md § A Review's Brief` holds, naming the adversarial review, its blanks filled and nothing added, the report a file under `.ai/tmp/design-specs/`, as `specs/methodology/working-files.md § The Working Files` gives a skill's output. The review's task is its paragraph and its row in `specs/AGENTS.md § Design, Refactor, Refine`.
- **Settling a round.** At settling, settle the round per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`. Before each fix, zoom out as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and write the fix whole across every place stating the fact it changes. At changing, prove the change by your self-review, never by rereading the fix alone. Record each review's pass as `specs/methodology/working-files.md § A Design Document` has it.
- **An approval that ends the review.** Where the user approves the plan anywhere in its work, record the approval in a pass, saying whether it was given with apply. Let the state in hand finish its own work, leaving a round still running or being settled with its findings as they are. Where the approval was given in reassessing, apply the round's settled change first, so the user approves the plan again. Then go on to validating, as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it. Once stamped, the design is approved. It is applied where the approval said so, once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it move into applying.
- **Asking for approval.** At awaiting approval, ask for approval of the plan as a choice of approved, approved and apply, or not approved, so the answer is a word and the user can approve a design and pause. Where the user's approval had ended the review, another round is a choice too. Approved moves the design's Status to approved. Approved and apply moves it to approved and begins the apply. Offer approved and apply only once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` would let the design move into applying. Not approved keeps the design in progress. Whatever the user says with that answer is a steer where it decides what the design is, per `specs/methodology/working-files.md § Steering Decision`.
- **Moving a design back.** Whenever a design moves back to in progress, run `--check-workstack`, per `§ Verifying a proposal`. Move back each approved design it reports depending on one not approved, per `specs/methodology/working-files.md § A Design Document`. Run it again until it reports none.

### Write the text in the form the rules give it

At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`, move the design's Status to applying only once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it. At writing, write each step's text with each file open, within the Target, with no change asking its own approval, since the user's approval of the plan authorizes it (`specs/methodology/working-files.md § A Design Document`). Write from the files as they stand, the changes a send-back kept among them, keeping what the steps reach and removing what they do not, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has them. Write a field, a bold lead-in, emphasis and literal text as `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Bold Lead-ins`, `specs/methodology/spec-style.md § Emphasis` and `specs/methodology/spec-style.md § Literal Text` give them. Write an entry of a repeated kind, or a closed set's members, as `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct` chooses: a record type's records or a Basic Table's rows. Write a number only where `specs/methodology/spec-style.md § Ordinals and Counts` keeps one.

### Write the references

Cite a section as `specs/methodology/sourcing-and-citation.md § Writing a Citation` gives. Refer to any other text as `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text` gives. `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` decides whether a citation may point where it does. `specs/methodology/sourcing-and-citation.md § Titling a Heading` governs any heading added or retitled.

### Synchronize whatever restates what you changed

Follow `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync`. Within `§ Workflow § State each step as its outcome`, find each passage and diagram restating what a step changes, and name it in the step's What and in the Target. At the apply, keep each in sync. A section you changed that a diagram renders cites that diagram, wherever the diagram sits, so the diagram to re-check is named in the text you just wrote.

A diagram is the easiest view to leave stale and the hardest to notice, because a wrong one is invisible in source and obvious only once rendered. Author or re-check a diagram as `specs/methodology/modeling-constructs.md § Diagrams` has it, through `.ai/skills/author-mermaid-diagram/`. That skill covers the altitude check that keeps a label inside what its host file states. It also covers the render step that catches what reading the source will not.

### Strip drafting residue, and write clearly

Follow `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` for a comparison kept, and `specs/methodology/spec-style.md § Clear Prose` for prose its primary reader understands on the first read.

### Check what you wrote, then the post-apply review, the audit and the commit

Work the apply in the order `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply` gives. What this skill adds at its states, each named where it acts, in the order they run:

- **What the user says.** At every state of the apply, before acting on anything the user says, tell it apart by `specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`, as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and act by its route. Where the user's words ask for a route the canon does not have, say so and name the canon's route before acting.
- **Your self-review of what you wrote.** Once the text is in, run `--refresh-links`, per `specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link`. Run `--check-constructs` on each file of the Target holding a construct the writing changed. Read each finding against the diff of the altered files, and fix in the writing each one the writing caused. Then, before the post-apply review, make your self-review for the post-apply review that follows, as your row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets.
- **Starting the post-apply review.** At the end of writing, start a cold agent with the brief `specs/methodology/design-workflow.md § A Review's Brief` holds, naming the post-apply review, its blanks filled and nothing added, the report a file under `.ai/tmp/design-specs/`, as `specs/methodology/working-files.md § The Working Files` gives a skill's output. At settling the post-apply round, settle the round per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`, fixing its nits in the files. Before each fix, zoom out as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and write the fix whole across every place stating the fact it changes. Before the next round, or before the user's review where none follows, prove the change by your self-review, never by rereading the fix alone. A finding lying in the plan goes to the user, whose triage sends the design back.
- **The user's review.** At user reviewing, show the user the applied result and the post-apply review's pass, and ask for a choice of approving the applied result, another round, or feedback, which goes back to writing. Take that feedback in at writing, never as a steer (`specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`).
- **The audit.** At auditing, start a cold agent on each audit `specs/methodology/design-workflow.md § A Design's Reviews` picks from the kinds of the files the Target names: given `.ai/skills/audit-specs/`'s name and, as its `--kind`, those kinds other than `code`, or, for code, `.ai/skills/verify-spec-implementation/`'s name. Its script catches a citation left pointing at a heading that moved. Its audits catch a summary that no longer describes what it summarizes. At settling the audit, read each finding against the diff of the files the apply altered, still uncommitted, against the last commit, and triage it as caused by the design or not, as `specs/AGENTS.md § Design, Refactor, Refine` has an audit read. Settle each finding with the user by the Decision Table in `specs/methodology/working-files.md § A Design Document § Changes After Approval`, taking its rows in their order.
- **A send-back, an abandonment and the commit.** A design sent back to in progress keeps its written changes in place, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has them, and nothing is reverted. A design abandoned has the changes it wrote reverted, those a send-back kept among them, per `specs/methodology/working-files.md § A Design Document`. At awaiting the commit, commit the design's changes on their own, one commit for the design, on the user's go-ahead, and move its Status to complete.

## Search for the fact before drafting the sentence

Not after. Not during review. Search before, because once a well-formed paragraph exists, the instinct is to place it rather than delete it. A second home for a fact is nearly invisible afterward. Both copies read correctly, and they diverge later when one is edited.

The search is cheap and mechanical. Take the fact's distinctive nouns and grep for each. Take the rule's governing verb and grep for that. If a search returns a document already covering the subject, read it before writing anything, even when you are confident it says something different.

`specs/methodology/sourcing-and-citation.md § One Home Per Fact` says what to do when you find one: cite the home, and add what it asks of a citing place. Deciding a home for the first time follows the same section. The decision turns on whose subject the rule is, not on which file happened to need it first.

**Your own recent work is not exempt.** A document you edited earlier in the session is searched and read like any other, per `§ Recall picks the direction; the file supplies the words`.

## Compression distortion

`specs/methodology/spec-placement.md § Index, Architecture, Detail` requires `architecture.md` to describe its directory, every directory beneath it, and what `specs/methodology/spec-placement.md § What an Overview Describes` names beyond it, in its own words and without accumulating full detail. Meeting that requirement means compressing its detail files. Every clause compressing a paragraph into a phrase is an opportunity to assert something the source does not.

The ways it goes wrong, in rough order of frequency:

- **A dropped qualifier that was load-bearing.** The source says a capability works "though never carrying X". The summary says it works. The exception was the protection, and the overview now promises something broader than the system does.
- **A default promoted to a universal.** The source says a path is "the default" among several. The summary says it is how the thing works.
- **A count asserted where the source enumerates.** The source names two behaviors and points at a third elsewhere. The summary says "two ways," which reads as closed and is not.
- **A referent stranded by the cut.** The summary keeps "than that window allows" after deleting the clause naming the window.

Re-reading your own summary will not catch these, because it will read fine. Open the source beside the clause and compare the two directly. Ask what the source said that the clause does not, and whether the omission changes what a reader concludes.

## Never propose structure before proving the existing structure fails

New sections, new files, new domains, new notation. Each is expensive, hard to remove later, and the most satisfying thing to write. That is how a Rube Goldberg machine gets built where the aim is elegance (`specs/methodology/glossary.md`).

Before proposing any, name the existing home that would have to receive the content, and say why it cannot. If you cannot name one, you have not looked hard enough. A proposal that starts from new structure and reasons toward it will always find the reasoning. The tests are already written: `specs/methodology/spec-placement.md § Where a File Goes` for whether a domain earns a subfolder or stays a root file, `specs/methodology/spec-placement.md § Naming a Capability Domain` for whether a domain exists at all, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` for whether a bold lead-in should become a heading.

The strongest disconfirming question is whether the thing is ordinary. A capability every comparable system has, one a reader assumes without being told, rarely deserves its own home. What deserves stating is the part that is *not* ordinary. A generic affordance plus one unusual property is usually one sentence about the unusual property, not a file about the affordance.

A column, a field or a form added to a construct's own tables is decided by the test `specs/methodology/modeling-constructs.md § Defining Constructs` sets, not by this rule alone. The section's prose is the existing structure, and that prose fails where the test says it does.

## Recall picks the direction; the file supplies the words

Recall is the right instrument for deciding where to go: which file probably holds this, what shape the change takes, which rule governs, whether the fact likely already has a home. Being wrong there costs one lookup, and the lookup corrects it.

Recall is never the source for anything written down. A quotation, a heading path, a count, a claim that a file does or does not say something: each of those is read from the file at the moment of writing it, not recalled from having read it.

The reason is the one `specs/AGENTS.md § Design, Refactor, Refine` gives for reading fresh before any work.

When this has gone wrong, the tell is that the *direction* was right and the *text* was not: the correct file, named with a heading it does not have. That pattern is the signature. It means a design can be wholly sound in substance and cite what is not there.

**One instrument for each half.**

**What is mechanically decidable goes to the script.** `.ai/skills/design-specs/scripts/design-specs.py` verifies cited heading paths with `--check-cited-headings`, a design document's structure with `--check-design`, and the constructs a design or a file states with `--check-constructs`, per `§ Verifying a proposal`. They are separate checks because a design makes each kind of claim. A design can hold its form while every heading it cites is wrong, or its constructs leave a case unmatched. That is how several wrong headings once reached a reviewer in a single revision, in a proposal whose every other check passed.

**What needs judgment goes to a cold agent.** Whether a section states the rule attributed to it, whether a count holds, whether "nothing in the repo says X" is true: no script decides these. Re-reading your own work does not decide them either, for the reason `specs/AGENTS.md § Design, Refactor, Refine` gives. While drafting, that cold agent's check is a judgment the builder hands off. Over the whole design, the check is the adversarial review, then the post-apply review and an audit, each as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets.

## Names carry claims

A term smuggles in whatever its ordinary meaning implies. A word suggesting rhythm implies recurrence. A word suggesting configuration implies something holds a setting. A word suggesting choice implies an actor who chooses.

When naming anything, state the claims the word makes beyond your definition and confirm each is true. When reviewing an existing name, ask what a reader would assume from the word alone, then check whether the document supports it. Renaming is cheap before citations exist and expensive after. `specs/methodology/sourcing-and-citation.md § Titling a Heading` requires every citation to move in the same edit.

Sometimes the answer is no name at all. If a distinction has two values that work as adjectives on something already named, the axis may not need a noun. Inventing one creates a thing readers expect to be able to set.

A term Spec of Record itself would give a meaning of its own is a change to the canon, made as `.ai/skills/design-specs/references/canon-specs.md` says.

## Numbers stated in passing

A figure quoted to support an argument gets believed and reused, including by you. A count from a quick search usually counts something adjacent to the claim: occurrences of a character rather than of the construct containing it, lines rather than matches, files rather than instances.

Verify a number before stating it, or state none. An argument needing a specific count to work is an argument needing the count to be right.

## Decline explicitly

A proposal silently omitting something looks identical to one that never considered it, and the next reader raises it again.

When you consider a change and reject it, say so and why, in the design's Out of Scope. When work is real but out of scope, record it and hand it on as `§ Workflow § Hand a change of its own to the user to spawn or log` has it. A statement that something was deliberately left alone is worth as much to the next reader as the changes.

## Verifying a proposal

`.ai/skills/design-specs/scripts/design-specs.py` checks that a heading a design cites is there. It checks that a design document, and the workstack the design documents draw, hold together. It also shows what a Refactor and Refine cycle changed. These checks and this skill's steps hold a design document to its form, per `specs/methodology/working-files.md § A Design Document`. The script's checks are flags, per `specs/methodology/skills.md § Authoring a Skill`. The exit status is 0 when every check passes, 1 when one finds a problem, and 2 for a usage error, so a run can gate a proposal.

    python .ai/skills/design-specs/scripts/design-specs.py --check-cited-headings <proposal>
    python .ai/skills/design-specs/scripts/design-specs.py --check-design-form <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-target-kind <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-constructs <design-document-or-spec-file>
    python .ai/skills/design-specs/scripts/design-specs.py --check-design <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-workstack [plans-dir]
    python .ai/skills/design-specs/scripts/design-specs.py --show-workstack [plans-dir]
    python .ai/skills/design-specs/scripts/design-specs.py --show-validation <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --stamp-validation <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --refresh-links [root]
    python .ai/skills/design-specs/scripts/design-specs.py --show-refactor-and-refine-of-existing-specs <baseline-commit>

`--check-design-form` checks a design document against `specs/methodology/working-files.md § A Design Document`, `specs/methodology/working-files.md § Design Goal`, `specs/methodology/working-files.md § Design Plan Step` and `specs/methodology/working-files.md § Steering Decision`. It checks:

- its heading, its fields in order, a Name that is a slug and its file's name, a Status that is a state, and a Target of paths;
- its sections in order, a canon design's Impact on the Application Specs among them and no other design's;
- its Design Goals' records against the Design Goal type its declaration gives, each Name a slug used once, and each citation of a goal in its design frame naming one;
- its design frame's headings in order and, once it is approved, neither its goals nor a part of its frame reading `Not yet stated.`, nor its steps `Not yet drafted.`;
- its Design Plan Steps' records against the Design Plan Step type its declaration gives, each Name a slug used once, Objectives a list and the record's last field, each Why citing a goal the design holds, and each step a step cites one the design holds;
- each steering decision's fields, and its Type one of the values the field allows;
- a design approved or further carrying a stamp, current while it is approved;
- each adversarial review's, post-apply review's and audit's pass naming the model and reasoning effort it ran on, its lead-in written exactly as that section sets it.

`--check-target-kind` reads the design's Kind field, for the builder's check of what the adversarial review judges. It checks that every file the design's Target names is of that kind, or is a file of `documentation` or `other`, by the kinds `specs/methodology/working-files.md § A Design Document § The Kinds of Change` defines. It reports a working file the Target names, whatever the Kind, since a working file is of no kind of change (`specs/methodology/working-files.md § The Working Files`). `--check-target-kind` decides the canon and application paths and the working files alone. Whether a file is the application's code is set by the code roots the technical stack names, which `.ai/skills/verify-spec-implementation/` reads.

`--check-constructs` runs the construct checks in `.ai/skills/lib/constructs.py`, the ones `.ai/skills/audit-specs/` runs, through their one function. Given a path in the skill's plans folder, it reads a design. It checks each Decision Table or State Machine an Objective states whole, in the form `specs/methodology/working-files.md § Design Plan Step` gives it, read as part of the file and section its opening citation names. The specs are read as they stand, or at the last commit while kept changes stand, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has a reading made. A section or file a step adds is read as empty. It reports each finding with the step's Name, its line in the design and the rule it breaks. It also reports an Objective that states a construct whole with no opening citation. Given any other Markdown file in scope, it reads that file and reports each finding in it, with its line and the rule. Either way, it lists the candidates apart, a construct whose completeness it cannot decide among them. A finding exits 1, a candidate alone 0, and a path neither in the plans folder nor in scope is a usage error, 2. Its output names what it leaves to the apply's self-review and the audit: a part a step changes, an Algorithm, a DAG or a Constraint, and what a change brings in another file.

`--check-design` is the validation review. It runs `--check-design-form`, drawing only on the design document and the canon's declarations of its form, and reads no file besides those. It reports where `specs/methodology/working-files.md § Steering Decision` does not declare the Steering Decision type, `specs/methodology/working-files.md § Design Goal` the Design Goal type, or `specs/methodology/working-files.md § Design Plan Step` the Design Plan Step type, since this tooling reads the records' fields from those declarations. Any problem it reports counts, whatever it is filed under.

`--show-workstack` reads every design document under `.ai/plans/design-specs/`, unless given another directory. It also reads every design document in the other skills' plans folders beside it, because a workstack spans designs, a design changing code among them, which `.ai/skills/implement-specs/` writes and revises. A design in another folder prints as that folder's name, a slash and its Name.

`--show-workstack` draws the tree from each design's Spawned By and Depends On. It marks each design blocked, with a finished design to take in, or, while it is in progress or approved, validated or validation stale. It lists the designs ready to work, the one the most open designs wait on first, the blocked ones apart, and the finished ones no design names in its Depends On, which may be deleted. `--check-workstack` reads the same designs. It reports a Status out of sync with what the design depends on, a Depends On naming no design, and a loop in Depends On or Spawned By.

`--show-refactor-and-refine-of-existing-specs` shows, through git, what a Refactor and Refine cycle changed in the specs and the skills since its baseline commit, per `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md`. It reads a heading without its level, and sets bare markup aside. It shows every line of six words or more now repeated more often than at the baseline, every line now held fewer times than at the baseline, and every line held more times, each with the files holding it. It decides nothing and exits 0, because whether a repeat is a second home or one made by design, and what each loss or gain traces to, is a reader's to judge. It runs from the repository's root, on a working tree with the cycle's changes applied.

`--refresh-links` writes and refreshes the link each citation carries in every file a person reads on GitHub, under the repository's root unless given another, per `specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link`.

`--show-validation` prints a design's stamped hash, its hash as it stands, and whether it is validated, stale or never stamped. The script compares the hashes, and they are never compared by hand.

`--stamp-validation` draws only on the design and the canon's declarations of its form, as the validation review does. The design's Depends On is `--check-workstack`'s, run before each validation: it reports an approved design whose Depends On names one not approved, per `specs/methodology/working-files.md § A Design Document`. `--stamp-validation` runs `--check-design`. When that finds nothing but the stamp's own absence, and neither the design's goals nor a part of its design frame reads `Not yet stated.`, nor its steps `Not yet drafted.`, it writes the stamp `specs/methodology/working-files.md § A Stamp` sets into the Validated field. It leaves a current stamp as it is, so the stamp's date stays that of the review that earned it. The builder runs it at validating on the way to the user's approval, as `specs/methodology/working-files.md § A Design Document` has the validation review stamp. Every check it stamps on is the script's own, so a stamp vouches for nothing a reader had to judge.

How each of the record's checks (`specs/methodology/working-files.md § A Design Document`) is decided, `--stamp-validation` running `--check-design` before it stamps:

**Reference Key:** Check

**Required:** Decided By

| Check | Decided By |
|---|---|
| Form | `--check-design` for the heading, the fields in order and their values, the Kind among them, the sections, the frame's headings and, by the time it is validated, no goal, no part of its frame and no step section not yet stated or drafted |
| Records | `--check-design` for each record's fields, its Type's values, each goal's and each step's Name a slug and each Name used once |
| References | `--check-design` for each goal the frame or a step's Why cites one the design holds, and each step a step cites one the design holds |

`--check-cited-headings` reads the design itself and resolves every cross-file citation span in it against the live file:

```
path/from/root.md § Parent § Child
```

It reports a missing file, a heading that does not exist, and a lineage that is wrong while the title is right. For a wrong lineage, it prints the real lineage beside it. That report is the most useful of these, because it names the fix.

It resolves a filename given in shorthand by path suffix, because a proposal is prose for a reviewer and refers back to a file whose full path it gave once. A suffix matching several files is reported rather than guessed. In a tree holding several `architecture.md` files, a bare one names nothing in particular. A proposal relying on surrounding prose to disambiguate is relying on the reader to do it too.

A same-file citation, one with no path, is skipped. A proposal is not the file it cites into, so a bare section token in it has no file to resolve against. So a proposal is clearer giving the full path in every citation, even where a spec would legitimately shorten it.

The script's actions are the code the skills share in `.ai/skills/lib/design_documents.py`, and its `--help` gives them. `.ai/skills/implement-specs/` runs that code through its own entry script too.

Run `--check-cited-headings`, `--check-target-kind` and `--check-constructs` at your self-review, before each validation. Run `--show-refactor-and-refine-of-existing-specs` once the design's changes are written. The script cannot tell you a design is right. It tells you the design holds together and cites what is there, which is a cheaper thing to be wrong about.
