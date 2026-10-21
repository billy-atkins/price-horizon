## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in [`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed). What a working file settles reaches a reader only through the spec it changes. In construction's terms, a design document is a change order, and the specs are the as-built drawings: the plans kept true to what stands, so the next change starts from the building as it is.

The builder changes a working file as the section holding its form has it, never by a design's step: a design document by the skill writing it, and a follow-up once the user approves its text ([`§ A Follow-up`](#a-follow-up)). Where a design changes a working file's form, the builder brings the existing working files to it the same way. A working file is of no kind of change, so no design's Target names one.

**Reference Key:** File

**Required:** Holds

| File | Holds |
|---|---|
| `.ai/plans/` | the plans the skills write, a design document among them ([`§ A Design Document`](#a-design-document)) |
| `.ai/follow-ups.md` | work on the specs, the code or the working files that should be done and is not yet, each as a follow-up ([`§ A Follow-up`](#a-follow-up)) |
| `.ai/tmp/` | the skills' own output, review and audit reports among it |

**A skill's scratch space is `.ai/tmp/<skill-name>/`.** The skill creates the directory if it is not there. Each skill has a directory of its own, so one skill's output is never mistaken for another's. The directory sits under `.ai/tmp/`, so none of it is ever committed. A skill does not delete its output when it finishes. The output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its *stale* output: a file left behind from a previous run that no longer corresponds to anything, because a reader has no way to tell such a file from a current one.

**A skill's plans are `.ai/plans/<skill-name>/`.** A skill describing a change before making it writes each plan to a file of its own in that directory. The skill creates the directory if it is not there. Each skill has a directory of its own, so one skill's plans are never mistaken for another's. Each plan has a file of its own, so each plan is read, reviewed and handed to a cold agent whole.

An open question about what is specified is recorded in a spec, per [`specs/methodology/spec-placement.md § Open Question`](/specs/methodology/spec-placement.md#open-question). A working file never holds one.

## A Design Document

Each design document is a file of its own, one per change taken through the Design, Refactor, Refine process ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)). `.ai/skills/design-specs/` writes each design changing the specs under `.ai/plans/design-specs/`, and `.ai/skills/implement-specs/` writes each design changing code under `.ai/plans/implement-specs/`. Both take this form. A design changing code differs only where [`§ A Design Document § A Design Changing Code`](#a-design-changing-code) sets. A design document is the plan for its change, the plan [`specs/methodology/glossary.md`](/specs/methodology/glossary.md) defines: its goals, its frame and its steps are what the user's first approval covers, and the text or code its apply writes is not. Each skill's steps and script hold a design to this form. The script reaches the design document tooling the two skills share. No audit reads a design ([`specs/methodology/design-workflow.md § A Design's Reviews`](/specs/methodology/design-workflow.md#a-designs-reviews)). A design opens with a level-one heading, `Design Document`, whose section holds the design's fields ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)). The design's sections follow as level-two headings. A design holds these parts, in this order:

**Reference Key:** Part

**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `**Name:**` field | yes | | the design's slug, the change in a few words in kebab-case: lowercase, each run of other characters a hyphen. The file is named `{Name}.md`. Other design documents name this one by its Name. One in another skill's plans directory puts this design's directory name and a slash before it, as `design-specs/{Name}` |
| Status | a `**Status:**` field | yes | | its state in [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) |
| Source | a `**Source:**` field | yes | | what asked for the change: the user's own words, or the finding that raised it |
| Kind | a `**Kind:**` field | yes | | the kind of change, one of the kinds [`§ A Design Document § The Kinds of Change`](#the-kinds-of-change) gives, which bounds the files the change may edit and sizes its reviews ([`specs/methodology/design-workflow.md § A Design's Reviews`](/specs/methodology/design-workflow.md#a-designs-reviews)), settled while the design is shaped and before any file is edited |
| Target | a `**Target:**` field | yes | | every file the change edits, each a path in backticks, separated by semicolons; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | yes | | the design document this one was spawned from, or none |
| Depends On | a `**Depends On:**` field | yes | | the design documents that block this one, separated by semicolons, or none; what blocks a design, and when, is set by this section's paragraphs on what blocks what and on blocked and to revise |
| Validated | a `**Validated:**` field | yes | | the stamp the validation review left once the document passed it, per [`§ A Stamp`](#a-stamp), leaving out the Validated and Status fields, or none; current while the design is approved |
| The Problem | a `## The Problem` section | yes | | what is wrong, stated on its own, before any fix |
| Design Goals | a `## Design Goals` record section ([`§ Design Goal`](#design-goal)) | until the design is complete or abandoned | | the design's goals, or `Not yet stated.` until the user agrees on them, which no design approved or further holds |
| The Design Frame | a `## The Design Frame` section | yes | | the design frame ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) the user agreed to or adjusted ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)), under level-three headings in this order: Scope, Approach and Outcomes. Scope holds the cases the change governs and what tells them apart, then how the sweep for affected content was done and what it found. For a design whose Depends On names a design, Scope also holds what it relies on from each, a premise citing no goal: what that design leaves in the files, specs or code, that this one cites or builds on, its rules, forms, headings, units and annotations among it. What the change leaves out is its Out of Scope's. A part not yet stated reads `Not yet stated.`, which no design approved or further holds |
| Steering Decisions | a `## Steering Decisions` record section | once the user has steered the design | | each steer the user gave, per [`§ Steering Decision`](#steering-decision) |
| Design Plan Steps | a `## Design Plan Steps` record section ([`§ Design Plan Step`](#design-plan-step)) | yes | | the plan's steps, or `Not yet drafted.` until drafting states them, which no design approved or further holds |
| Impact on the Application Specs | a `## Impact on the Application Specs` section | in a canon design | | each application file and section the canon change leaves out of sync, what it leaves out of sync there and what the application work must do, or that none was found; and how the application specs were reviewed |
| The Builder's Passes | a `## The Builder's Passes` section | yes | | what each pass and each review changed, each under a bold lead-in naming it and each review but the validation review named with its report, where it gave one; the nits a round left, and each judgment the builder handed off, with how its findings were settled; the builder's own trace, before a review, of each mechanism with states or routes its steps change, and, before the post-apply review, of each mechanism its apply wrote; and the tests its self-review ran on what its apply changes in a script or code, each ephemeral differential test ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) of a changed script or each of the local environment's tasks it ran on code, and what each showed. An adversarial review's lead-in opens `Adversarial review`, a post-apply review's `Post-apply review`, and an audit's `Audit`. Each such pass names the model and reasoning effort its review ran on, as `on {model} at {effort} effort`, the effort one of the levels [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) names, or as `on {model} as the agent allows` where the agent could not apply the effort chosen. Each also records the design flaws among its findings, as [`specs/methodology/glossary.md`](/specs/methodology/glossary.md) defines them, with the user's triage of each. An adversarial review's pass also records how the builder settled its implementation flaws, the causes the round's change addressed, a mechanism it rewrote whole where its findings clustered, and the worked case proving it, or the user's approval of the plan where it ended the review, with the round it ended. A post-apply review's pass records how each of its findings was settled, whether it lay in the plan or in the writing. An audit's pass records the builder's triage of each finding, as caused by the design or not, and how each was settled, as [`§ A Design Document § Changes After Approval`](#changes-after-approval) has them |
| Out of Scope | a `## Out of Scope` section | yes | | each thing the design deliberately leaves unaddressed, so a reviewer spends no time on it: each change considered and declined, and each piece of work handed on, the code a design changing the specs leaves out of sync among it. Each item gives its reason and names no other working file, and the work it hands on is held where the skill's step handing it on sends it. Work the design waits on is named in its Depends On instead, and the application work a canon design leaves is in its Impact on the Application Specs |

**Spawning keeps a design focused.** A design may turn up work that is a change of its own, such as a migration of files a rule change leaves out of sync. That work is spawned as a design document of its own or logged as a follow-up ([`§ A Follow-up`](#a-follow-up)), as the user decides, because which suits depends on how the user means to work it. Work that changes only working files is logged as a follow-up, never spawned, since no design changes a working file ([`§ The Working Files`](#the-working-files)). The user approves each spawned design before it is written, with its text shown first, and each follow-up as [`§ A Follow-up`](#a-follow-up) has it. Nothing is spawned or logged on the builder's own call. Work is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change. The design's scope still sweeps what the spawned change touches, and only the spawned design's steps change it.

**One standing Objective.** Every step of a design carries one Objective the canon keeps rather than each step stating it: the prose around what the step changes, within the Target, stays consistent with the steps. The builder meets it at the apply, and the post-apply review checks it, never passage by passage in the steps.

**Depends On records what blocks what.** A spawned design blocks the design it came from when that design cannot finish without it, and is named in that design's Depends On. A spawned design that can be worked before or after the design it came from does not block that design. Depends On is the one record of what blocks what. It names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks, back toward the design it began from.

**Blocked and to revise are read, not recorded.** A design finishes when it enters one of the states the Trigger Classes table of [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) lists. A design is blocked while its Depends On names a design that has not finished. It is to revise once a design its Depends On names has finished. Blocked and to revise are both read from the Status of the designs its Depends On names, never recorded in the design itself. A blocked design may still be worked and reviewed. A design goes to the user's approval only once each design its Depends On names is approved or applying, so designs that build on each other can be shaped and approved before any of them is applied. A finished design among those it names is taken in and removed first. It works as integrating branches early does: a conflict between the designs is found before any of them is applied, not at the merge. A design is applied only once its Depends On names none, so designs apply in dependency order. Where a design goes back to in progress, the builder moves back each approved design whose Depends On names it. Once a design its Depends On names finishes, the design naming it goes back to in progress if it is approved. It takes in what the finished design settled, or why it was dropped, against the files as they stand once that design finishes, and, where that design was dropped, revises itself for its absence. It then removes the finished design from Depends On, and from its Scope what it relied on from that design.

**Unwinding.** A finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. When a design is abandoned, each open design it spawned goes on as a design of its own, or is abandoned with it, as the user decides. A Spawned By naming a design since deleted stays, as the spawned design's history.

**The record's checks.** Before each adversarial round and before the user's approval, the validation review checks that the design document is a valid document. The validation review is the design script of the skill writing the design. It checks the document's structure alone, drawing only on the document and the canon's declarations of its form, never what the document says, and reads no file besides those. How the builder applied the user's steers, and whether the design is right, are the adversarial review's to read ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)). The steers are that review's account of how the design was shaped. The checks:

**Reference Key:** Check

**Required:** What The Record Holds, Why

| Check | What The Record Holds | Why |
|---|---|---|
| Form | its heading, its fields and its sections in the order and the form this section's table gives them, and, by the time it is validated, no goal, no part of its frame and no step section reading `Not yet stated.` or `Not yet drafted.` | a reader and a script find each part where the form puts it |
| Records | its design goals, its steering decisions, its design plan steps and each other record section, each record holding the fields its type declares, a Type among the values it declares, and each Name used once | a record out of its form is one no script can read |
| References | each goal its frame or a step's Why cites one the design holds, and each step a step cites one the design holds | a reference to nothing leads a reader, and the work, nowhere |

Whether the design's citations of other files resolve, and its Target against its Kind, are the adversarial review's to judge. The design's place in the workstack is `--check-workstack`'s, which runs before each validation. A problem it reports is put right before the design goes to a review or to the approval.

**Valid to approve.** The validation review reports each problem it finds, the builder fixes it, and the review runs again, until the document passes. On the way to the user's approval, the passing review stamps it ([`§ A Stamp`](#a-stamp)); before an adversarial round, it stamps nothing. Every problem it can report is one of form or integrity, so none is a question for the user. A stamp never waits on what the document says. The stamp is the review's record in the design. A design changed after its stamp no longer matches the stamp, so a stale validation is read from the file and never cleared by hand. The review runs again.

**A form the methodology is still adding.** A design changing the methodology may add a form, such as a part of a design document or a record type. A design whose record uses a form not yet applied is validated by hand: its pass records each check, its Validated field reads none, and the script's reports of the form it does not yet know, and of a stamp missing once the design is approved, are the expected ones. Another design whose record uses that form names the design adding it in its Depends On. The design adding the form is stamped at its writing, once its form is applied; one depending on it, when next validated after that design finishes. Either way, the record is held to the methodology as it will be. A self-hosting compiler is built the same way, with the syntax it adds.

**A change needing both kinds is split.** The change's canon design reviews the application specs for what the change leaves out of sync there. It records that in its Impact on the Application Specs, and edits none of the application specs. That application work goes to the application design the canon design was spawned from, where there is one. Otherwise it is spawned or logged as this section's spawning paragraph has it. The canon and application designs may be worked in concert. A design changing the specs that leaves code out of sync edits none of the code either. It records the code it leaves out of sync in its Out of Scope, and that work goes to a design changing code, spawned or logged the same way. What an audit in the canon design's apply finds in the application specs is settled by [`§ A Design Document § Changes After Approval`](#changes-after-approval). What that table hands on is application work too. It is added to what the canon design's review handed on, or handed on the same way, so the canon design completes without editing the application specs. Where the application work finds the canon design wrong, the canon design takes the change while it is in progress or approved, the user reopening an approved one. For any other canon change the application work needs, the application design spawns a canon design, which blocks it. A change to the canon design once that design is applying or complete is such a change too. Where the application design is approved, the user reopens it before the canon design is spawned. An application design already applying keeps to what was approved. The canon change is then spawned or logged without blocking it, as the user decides.

**Applying and committing.** A design's apply begins only as [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) lets the design move into applying. The user's approval of the plan authorizes the builder to write within the design's Target, no edit asking its own approval. Every change the design makes lies within its Target and is reached by a step. The design's changes are committed on their own, one commit for each design even where a branch holds several, so a revert takes exactly that design's changes. A design abandoned has the changes it wrote reverted, those a send-back kept among them, through version control or, where the project has none, by hand.

### The Kinds of Change

What each kind bounds a change to:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Kind

| Kind | Bounds the change to |
|---|---|
| `canon-specs` | [`specs/AGENTS.md`](/specs/AGENTS.md), [`specs/architecture.md`](/specs/architecture.md), the files under `specs/methodology/`, a registered skill's directory, and `.ai/skills/lib/` |
| `application-specs` | the files under `specs/application/` |
| `code` | the application's code, within the code roots the technical stack names ([`specs/methodology/spec-placement.md § The Technical Stack`](/specs/methodology/spec-placement.md#the-technical-stack)), which the application specs govern ([`specs/methodology/code.md`](/specs/methodology/code.md)); a design changing code's only kind |
| `documentation` | the documentation, `README.md` and the files under `docs/` |
| `other` | any other file, the project's root `AGENTS.md` and its helper scripts among them, but no working file, which is of no kind ([`§ The Working Files`](#the-working-files)) |

Every file a design's Target names is of its declared kind, or is a file of `documentation` or `other`, or is code whose annotation lines alone it edits, as [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code) has a design retitling a heading.

### Changes After Approval

Once the user approves the plan, a passage outside the Target that the apply leaves false is a finding lying in the plan, as [`§ A Design Document`](#a-design-document)'s paragraph on applying and committing bounds the apply. A finding the post-apply review makes lies in the plan or in the writing, as [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) has the review settled. An audit run in the apply is the builder's to read: the builder triages each of its findings as caused by the design or not, and marks each it caused, as [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) has an audit read, and each is presented to the user and settled by what it is:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** Finding

| Finding | Settles |
|---|---|
| one the design did not cause | settled as the user chooses, and recorded in the pass: ignored; given a design spawned for it; or logged as a follow-up ([`§ A Follow-up`](#a-follow-up)) |
| one the user judges wrong | set aside, and recorded in the pass with the reason |
| a canon design's, in the application specs | handed on as application work, as [`§ A Design Document`](#a-design-document)'s paragraph on a change needing both kinds has it |
| one lying in the plan, a design flaw among them | sends the design back to in progress, its written changes kept, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has one |
| "an implementation flaw no direct edit fixes", "a tactical fix the user does not approve" | goes back to the writing, where the builder rewrites what the finding reaches |
| a nit | fixed as a direct edit the user approves ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)), or left as the user chooses, and recorded in the audit's pass |
| a tactical fix the user approves | made as a direct edit ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)), and recorded in the audit's pass |

### The States It Moves Through

The states a design document's Status moves through, and what moves it from one to the next:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | Yes | No |
| in-progress | its work under way, governed by [`specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design`](/specs/methodology/design-workflow.md#the-work-of-a-design) | No | No |
| approved | validated and its plan approved by the user, its adversarial review converged or ended by that approval, and not yet applied, awaiting the go-ahead to apply | No | No |
| applying | its apply under way, governed by [`specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow.md#the-apply) | No | No |
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
| approved | applying | the user gives the go-ahead to apply | its Depends On names none, nothing is uncommitted but the changes a send-back kept of its own ([`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back)), and no other design is applying in the checkout |
| applying | in-progress | none | exit = "sent back" |
| applying | complete | none | exit = "applied" |
| not-started | abandoned | the user abandons it | none |
| in-progress | abandoned | the user abandons it | none |
| approved | abandoned | the user abandons it | none |
| applying | abandoned | the user abandons it | none |

**Table Name:** Trigger Classes

| Member | Class |
|---|---|
| complete of a design its Depends On names is entered | a design its Depends On names finishes |
| abandoned of a design its Depends On names is entered | a design its Depends On names finishes |

#### A Send-back

A design sent back from applying goes back to in-progress with the changes its apply wrote kept in place in the files, never set aside or reverted, since they are the plan's work with flaws to rework, not work to undo. Its steps are revised against the last commit, as any design's are. The kept changes are its apply's writing in progress, never a baseline: as the design applies again, the writing keeps what the revised steps reach and removes what they do not, so the post-apply review finds nothing the steps do not reach. While kept changes stand in a checkout, every reading for a design in it, a review's, the builder's self-review and another design's among them, reads the files at the last commit where it would read the files as they stand, and reads the kept changes as writing in progress, from their diff against that commit.

The kept changes hold their checkout as an apply's changes do. The design enters applying again with nothing uncommitted but its own kept changes, and no other design applies in that checkout, so each commit holds one design's changes. A design that must apply while they stand, a dependency the sent-back design gains among them, applies in another checkout, made as [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) has a new branch made. The sent-back design takes that design's commit in as it applies again, its writing reconciling the two. Where the project has no version control there is no other checkout, so a sent-back design takes on no dependency its kept changes would block: the change it needs joins its own steps, or the design is abandoned, which reverts them, as [`§ A Design Document`](#a-design-document)'s paragraph on applying and committing has it.

### A Design Changing Code

A design changing code starts from applied specs, or from the specs as a design its Depends On names leaves them, rather than from a problem in them. It designs the code and the tests that bring the specs to life. It takes the form [`§ A Design Document`](#a-design-document) sets, the Design, Refactor, Refine process, the validation review, the adversarial review, the stamp and the post-apply review, as a design changing the specs does. It differs only where code does. Its parts differ so:

**Reference Key:** Part

**Required:** In A Design Changing Code

| Part | In A Design Changing Code |
|---|---|
| The Problem | names the product module it carries out, then the specs it carries into code, cited, and what the code lacks |
| Kind | `code` |
| Design Plan Steps | its steps' Objectives state the units of governed code the applied code holds, with the app-spec annotations each carries ([`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code)), the wiring that connects the units ([`specs/methodology/code.md § Governed Code and Wiring Code`](/specs/methodology/code.md#governed-code-and-wiring-code)), and the tests that check the specs ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)), as [`§ Design Plan Step`](#design-plan-step) has an Objective state an outcome |

**One product module.** A design changing code carries out one product module. It reads what [`specs/methodology/spec-placement.md § A Product Module`](/specs/methodology/spec-placement.md#a-product-module) sets, in the order [`specs/methodology/scope.md § Progressive Disclosure`](/specs/methodology/scope.md#progressive-disclosure) sets. Work reaching several modules is a design for each. A technical section several modules need, such as a shared data model's, is carried out by the first design changing code that takes it up. A later design names that design in its Depends On while that design is unfinished, and builds on that design's code once it is applied.

**The builder designs, the user steers.** The builder designs the code from the specs on its own, with the specs as its starting point. The user approves the design or steers it. A steer about how the code carries out the specs is this design's. A steer changing what a spec states is spawned as a design changing the specs and named in this design's Depends On. This design then waits on the spawned design, per [`§ A Design Document`](#a-design-document)'s paragraph on blocked and to revise. Once the spawned design finishes, this design takes it in, revised against the specs as they then stand.

The audit in its apply is the one [`specs/methodology/design-workflow.md § A Design's Reviews`](/specs/methodology/design-workflow.md#a-designs-reviews) picks from the kinds of the files its Target names, `.ai/skills/verify-spec-implementation/`'s full run for its code.

## Design Goal

A design's goals ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) are agreed on before its design frame, and changed and weighed, as [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) has them. A goal is named, never numbered, so a record speaks of a goal by its Name however the list changes. A record cites a goal as a record is cited, by its record section and its Name ([`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation)).

A design's goals sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Design Goals

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the goal's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which the record names and cites it |
| Description | no | yes | | text | what the goal asks of the change |

## Design Plan Step

Each step of a design's plan states what it changes and the state the applied work holds once it is changed, never the text or the code that brings the state about. That text or code is written at the apply ([`specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow.md#the-apply)). A step reaches as many files as its change does, and the design's Target is every file its steps reach.

**An Objective is an outcome.** An Objective ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) describes the outcome, never the work to reach it, and it names no phrase or passage to change. Everything a step's Objectives do not state stands as it is. A mechanism's states, transitions, guards and facts are its outcome, so a step changing one states each it adds, changes or removes, each in its construct's form. An Objective adding a Decision Table or a State Machine, or rewriting one whole, opens with a citation of the section the construct stands in, `{path} § {section}`. Indented under the Objective, it states the construct whole in its form ([`specs/methodology/modeling-constructs.md § Constructs`](/specs/methodology/modeling-constructs.md#constructs)), as a mechanism's form is its outcome. An Algorithm's, a DAG's and a Constraint's parts, and a Basic Table's and a record type's rows, are stated as any other outcome, never whole. An Objective quotes wording only where the wording is itself the outcome. A step's Why cites a goal the step serves, as a record cites a goal ([`§ Design Goal`](#design-goal)).

A design's steps sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Design Plan Steps

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the step's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which the record names and cites it |
| What | no | yes | | text | what the step changes, the files and sections it reaches |
| Why | no | yes | | text | why the step is needed, citing each goal it serves |
| Objectives | no | yes | | text | a list of the states the applied work holds once the step is applied, each an Objective |

## Steering Decision

A design's Steering Decisions record only the user's steers, the decisions a steering decision records ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), such as new scope or a design flaw's fix. A steer differs from the user's direction about how the work proceeds, from the user's feedback on the applied result and from a decision about other work, as [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart) tells them apart.

**A go-ahead to take in findings.** It is a steer for the findings that change what the design is, and direction for the tactical ones. An answer carrying both is recorded for the part that decides the design.

**Each steer is recorded when it is given.** The design is then revised to apply the steer before its work goes on, so the design carries how it was formed and never lags a steer it records. A steer changing the goals or the frame is confirmed with the user, as [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine) has it. It is carried into the goals or the frame, its case reaching the Scope, the Approach and the Outcomes. Any other steer, such as one choosing wording a step quotes as its outcome or a name in code, is recorded as given. The record tells the adversarial review the user chose it. Where the steer differs from another choice only by preference, it stands. Where it breaks a rule, the review raises it as a finding pressing on the steer. The builder presents the conflict to the user with a wording or a name that follows the rule, and the user chooses either ([`§ Steering Decision § Revisiting a Steer`](#revisiting-a-steer)). Only the user revises a steer, by a later one. The record is history. A later steer revising what an earlier one decided is recorded after it, and its Decision says which steer it revises. The earlier one stays as it was given. The design follows the later one, whatever the Type of either, so the records, read in order, show how the design was shaped. A question the user leaves unanswered is asked again, never read as agreed. The adversarial review reads the steers as background, checking fidelity to them rather than reopening them ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)). The request that opened the design is its Source. The Builder's Passes record what each pass changed, never a steer, so each steer is recorded once.

**A steer's Type.** A steer is a selection where the user only selects one of the options the builder offered, a literal selection. Every other steer is a perspective, whatever its form, such as emphasis, a negative remark, a nudge or a strong direction for the design. Selecting an option is easier than sharing a perspective, and a perspective originates with the user.

A design's steering decisions sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

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

#### Steer, Direction, Feedback or Other Work

How a steer, direction about the work, feedback on the applied result and a decision about other work are each recorded, an answer carrying more than one taken a part at a time:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** What the user decides

**Annotations:** Sounds Like

| What the user decides | Recorded | Tells a reviewer | Sounds Like |
|---|---|---|---|
| A steer | in Steering Decisions, its Steer quoting every part of the user's words that decides the design, never only the last of them | how the design was formed | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found", "call it Kind, not Type" |
| Direction about the work | not as a steer; where the record needs it, in the passes, as the Builder's Passes row of [`§ A Design Document`](#a-design-document) has them, or in the Status field | nothing about what the design is | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "the applied result is approved", "create the branch", "medium effort", "G1 to G6 are design flaws", "go on" or "rescope it" deciding a reassessment, the new scope then steered at framing |
| Feedback on the applied result | not as a steer; taken into the writing, the post-apply review reading what it changes | nothing about what the design is | "that paragraph buries the rule", "say it in fewer words", "the example reads wrong" |
| A decision about other work | where that work is held | nothing about the design being worked | "the implement-specs design should weigh renaming the workstack", "keep the billing service stateless when we design it" |

### A Decision About Other Work

A decision about other work is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory. A decision about more than one design is recorded in each. What becomes of the decision, by where the work is held:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Where the work is held

| Where the work is held | The decision |
|---|---|
| "a not-started design", "an in-progress design" | is its steer, applied when that design is worked |
| "an approved design", "an applying design" | is put to the user, who decides whether to reopen that design for it, an applying one only by a steer, which sends it back ([`specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow.md#the-apply)): reopened, the design takes it as its steer; not reopened, it is dropped, or, where the user wants it kept for later, logged as a follow-up |
| a follow-up, and no open design | goes in the follow-up's body ([`§ A Follow-up`](#a-follow-up)), and the design taking up the follow-up records it as its steer |
| no follow-up, and no open design, only a complete or abandoned design or nothing | the user chooses between a not-started design recorded for it, the decision its Source where it asks for the work and its steer otherwise, and a new follow-up |

### Revisiting a Steer

A design's path is not straight. Working toward an elegant solution takes loops, detours and pivots, and a steer is part of what may need to move. While settling a round ([`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round)), the builder may find that a change fixing a cause would go against one or more steers, of either Type. Those are the steers the cause presses on. The builder brings the user each such steer, the findings pressing on it and what revising it would change. The builder proposes revising the selections among them, whose options the builder framed. It proposes revising a perspective only where revising the selections cannot fix the cause, because a perspective outweighs a selection. The user decides.

## A Stamp

A stamp lets a later reader tell whether content has changed since a check passed on it, so nothing has to be cleared by hand. It is written as a UTC timestamp and a content hash separated by a space, `2026-09-29T14:05:12Z sha256:3f9a0c1b2d4e5f60`:

- **The timestamp.** A date and time as RFC 3339 writes one ([`specs/methodology/external-references.md § External References [Name: RFC 3339]`](/specs/methodology/external-references.md#external-references)), in UTC, to the second, ending in `Z`, as `YYYY-MM-DDThh:mm:ssZ`, so stamps written on different machines compare without a time zone.
- **The content hash.** SHA-256 of the file's text, encoded as UTF-8 with line-feed line endings, after dropping the lines that hold the fields the form leaves out. It is written as `sha256:` followed by the digest's first sixteen hexadecimal characters, lowercase. The hash detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding the stamp and the fields the stamp leaves out. The stamp always leaves out its own field, since writing the stamp must not change the hash. It also leaves out any field whose change the check does not concern, as a design document's Validated field leaves out its Status ([`§ A Design Document`](#a-design-document)).

## A Follow-up

A follow-up records work on the specs, the code or the working files that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. A follow-up is written, or amended, only once the user approves its text, shown first. `.ai/follow-ups.md` opens with a short header naming what the file holds and citing this file. The follow-ups follow that header. Each follow-up sits under a priority heading:

- `## High`, the work to take up next;
- `## Medium`, which waits until High is settled;
- or `## Low`, worth doing once nothing more pressing is open.

Each follow-up holds these parts, in this order:

**Reference Key:** Part

**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `###` heading, a kebab-case slug | yes | | the name the follow-up is referred to by |
| Status | a `**Status:**` field | yes | | where the follow-up is in this section's life cycle |
| Category | a `**Category:**` field | yes | | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` field | yes | | the file, section or files it concerns |
| Body | prose | yes | | the work, the context needed to take it up, and, where known, what found it, naming the design that handed the work on where one did |

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
| in-progress | not-started | [`§ A Design Document § The States It Moves Through [States.State: abandoned]`](#the-states-it-moves-through) of the design document taking it up is entered |
| in-progress | done | the change that resolves it lands |
| in-progress | done | the user decides nothing needs to change |
| not-started | done | a change made for another reason resolves it |
| not-started | done | the user decides nothing needs to change |
