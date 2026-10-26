## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in [`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed). What a working file settles reaches a reader only through the spec it changes. In construction's terms, a design document is a change order, and the specs are the as-built drawings: the plans kept true to what stands, so the next change starts from the building as it is.

The builder changes a working file as the section holding its form has it, never by a design's step: a design document by the skill writing it, and a follow-up once the user approves its text ([`§ A Follow-up`](#a-follow-up)). Where a design changes a working file's form, the builder brings the existing working files to it the same way. A working file is of no kind of change, so no design's Target names one.

**Reference Key:** File \
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

**Reference Key:** Part \
**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `**Name:**` field | yes | | the design's slug, the change in a few words in kebab-case: lowercase, each run of other characters a hyphen. The file is named `{Name}.md`. Other design documents name this one by its Name. One in another skill's plans directory puts this design's directory name and a slash before it, as `design-specs/{Name}` |
| Status | a `**Status:**` field | yes | | its state in [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) |
| Source | a `**Source:**` field | yes | | what asked for the change: the user's own words, or the finding that raised it |
| Kind | a `**Kind:**` field | yes | | the kind of change, one of the kinds [`§ A Design Document § The Kinds of Change`](#the-kinds-of-change) gives, which bounds the files the builder edits, the steps' writing and each direct edit, though not a user's edit, which lies wherever the user made it. It sizes the design's reviews ([`specs/methodology/design-workflow.md § A Design's Reviews`](/specs/methodology/design-workflow.md#a-designs-reviews)). It is settled while the design is shaped and before any file is edited |
| Target | a `**Target:**` field | yes | | every file the steps edit, each a path in backticks, separated by semicolons; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | yes | | the design document this one was spawned from, or none |
| Depends On | a `**Depends On:**` field | yes | | the design documents that block this one, separated by semicolons, or none; what blocks a design, and when, is set by this section's paragraphs on what blocks what and on blocked and to revise |
| Validated | a `**Validated:**` field | yes | | the stamp the validation review left once the document passed it, per [`§ A Stamp`](#a-stamp), leaving out the Validated and Status fields and the Design Log Entries section; none; or `by hand`, where the design is validated by hand, as this section's paragraph on a form the methodology is still adding has it; a stamp current while the design is approved |
| The Problem | a `## The Problem` section | yes | | what is wrong, stated on its own, before any fix |
| Design Goals | a `## Design Goals` record section ([`§ Design Goal`](#design-goal)) | until the design is complete or abandoned | | the design's goals, or `Not yet stated.` until the user agrees on them, which no design approved or further holds |
| The Design Frame | a `## The Design Frame` section | yes | | the design frame ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) the user agreed to or adjusted ([`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame)), under level-three headings in this order: Scope, Approach and Outcomes. Scope holds the cases the change governs and what tells them apart, then how the sweep for affected content was done and what it found. For a design whose Depends On names a design, Scope also holds what it relies on from each, a premise citing no goal: what that design leaves in the files, specs or code, that this one cites or builds on, its rules, forms, headings, units and annotations among it. What the change leaves out is its Out of Scope's. A part not yet stated reads `Not yet stated.`, which no design approved or further holds |
| Steering Decisions | a `## Steering Decisions` record section | once the user has steered the design | | each steer the user gave, per [`§ Steering Decision`](#steering-decision) |
| Design Plan Steps | a `## Design Plan Steps` record section ([`§ Design Plan Step`](#design-plan-step)) | yes | | the plan's steps, or `Not yet drafted.` until drafting states them, which no design approved or further holds |
| Retired Phrases | a `## Retired Phrases` record section ([`§ Retired Phrase`](#retired-phrase)) | no | none | the wording the design retires, each phrase with its replacement and the places it stays right, a phrase the user turned down while steering among them |
| Impact on the Application Specs | a `## Impact on the Application Specs` section | in a canon design | | each application file and section the canon change leaves out of sync, what it leaves out of sync there and what the application work must do, or that none was found; and how the application specs were reviewed |
| Design Log Entries | a `## Design Log Entries` record section ([`§ Design Log Entry`](#design-log-entry)) | once the design's first entry is appended | | the design's log: an entry for each check of its work and each event of its workflow, in the order they came |
| Out of Scope | a `## Out of Scope` section | yes | | each thing the design deliberately leaves unaddressed, so a reviewer spends no time on it: each change considered and declined, and each piece of work handed on, the code a design changing the specs leaves out of sync among it. Each item gives its reason and names no other working file, and the work it hands on is held where the skill's step handing it on sends it. Work the design waits on is named in its Depends On instead, and the application work a canon design leaves is in its Impact on the Application Specs |

**Spawning keeps a design focused.** A design may turn up work that is a change of its own, such as a migration of files a rule change leaves out of sync. That work is spawned as a design document of its own or logged as a follow-up ([`§ A Follow-up`](#a-follow-up)), as the user decides, because which suits depends on how the user means to work it. Work that changes only working files is logged as a follow-up, never spawned, since no design changes a working file ([`§ The Working Files`](#the-working-files)). The user approves each spawned design before it is written, with its text shown first, and each follow-up as [`§ A Follow-up`](#a-follow-up) has it. Nothing is spawned or logged on the builder's own call. Work is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change. The design's scope still sweeps what the spawned change touches, and only the spawned design's steps change it.

**One standing Objective.** Every step of a design carries one Objective the canon keeps rather than each step stating it: the prose around what the step changes, within the Target, stays consistent with the steps. The builder meets it at the apply, and the post-apply review checks it, never passage by passage in the steps.

**Depends On records what blocks what.** A spawned design blocks the design it came from when that design cannot finish without it, and is named in that design's Depends On. A spawned design that can be worked before or after the design it came from does not block that design. Depends On is the one record of what blocks what. It names any design that must finish first, spawned or not, as an application design names the canon design whose rule it follows. A workstack is worked from the designs nothing open blocks, back toward the design it began from.

**Blocked and to revise are read, not recorded.** A design finishes when it enters one of the states the Trigger Classes table of [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) lists. A design is blocked while its Depends On names a design that has not finished. It is to revise once a design its Depends On names has finished. Blocked and to revise are both read from the Status of the designs its Depends On names, never recorded in the design itself. A blocked design may still be worked and reviewed. A design goes to the user's approval only once each design its Depends On names is approved or applying, so designs that build on each other can be shaped and approved before any of them is applied. A finished design among those it names is taken in and removed first. It works as integrating branches early does: a conflict between the designs is found before any of them is applied, not at the merge. A design is applied only once its Depends On names none, so designs apply in dependency order. Where a design goes back to in-progress, the builder moves back each approved design whose Depends On names it. Once a design its Depends On names finishes, the design naming it goes back to in-progress if it is approved. It takes in what the finished design settled, or why it was dropped, against the files as they stand once that design finishes, and, where that design was dropped, revises itself for its absence. It then removes the finished design from Depends On, and from its Scope what it relied on from that design.

**Unwinding.** A finished design is deleted once no design names it in Depends On, so what it settled or why it was dropped stays readable until the designs that waited on it have taken it in. When a design is abandoned, each open design it spawned goes on as a design of its own, or is abandoned with it, as the user decides. A Spawned By naming a design since deleted stays, as the spawned design's history.

**The record's checks.** Before each adversarial round and before the user's approval, the validation review checks that the design document is a valid document. The validation review is the design script of the skill writing the design. It checks the document's structure alone, drawing only on the document and the canon's declarations of its form, never what the document says, and reads no file besides those. How the builder applied the user's steers, and whether the design is right, are the adversarial review's to read ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review)). The steers are that review's account of how the design was shaped. The checks:

**Reference Key:** Check \
**Required:** What The Record Holds, Why

| Check | What The Record Holds | Why |
|---|---|---|
| Form | its heading, its fields and its sections in the order and the form this section's table gives them, each block of fields and each list a field holds as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has them, each blank line placed as [`specs/methodology/spec-style.md § Blank Lines`](/specs/methodology/spec-style.md#blank-lines) has it, and, by the time it is validated, no goal, no part of its frame and no step section reading `Not yet stated.` or `Not yet drafted.` | a reader and a script find each part where the form puts it |
| Records | its design goals, its steering decisions, its design plan steps and each other record section, each record holding the fields its type declares, a Type among the values it declares, and each Name used once; each design log entry's count counting its kind from 1 in the order the entries stand, and each Timestamp no earlier than the one before it | a record out of its form is one no script can read |
| References | each goal its frame or a step's Why cites one the design holds, and each step a step cites one the design holds | a reference to nothing leads a reader, and the work, nowhere |

Whether the design's citations of other files resolve, and its Target against its Kind, are the adversarial review's to judge. The design's place in the workstack is `--check-workstack`'s, which runs before each validation. A problem it reports is put right before the design goes to a review or to the approval.

**Valid to approve.** The validation review reports each problem it finds, the builder fixes it, and the review runs again, until the document passes. On the way to the user's approval, the passing review stamps it ([`§ A Stamp`](#a-stamp)); before an adversarial round, it stamps nothing. Every problem it can report is one of form or integrity, so none is a question for the user. A stamp never waits on what the document says. The stamp is the review's record in the design. A design changed after its stamp no longer matches the stamp, so a stale validation is read from the file and never cleared by hand. The review runs again.

**A form the methodology is still adding.** A design changing the methodology may add a form, such as a part of a design document or a record type. A design whose record uses a form not yet applied is validated by hand: its Validated field reads `by hand`, and the script's reports of the form it does not yet know are the expected ones. Another design whose record uses that form names the design adding it in its Depends On. The design adding the form is stamped at its writing, once its form is applied; one depending on it, when next validated after that design finishes. Either way, the record is held to the methodology as it will be. A self-hosting compiler is built the same way, with the syntax it adds.

**A change needing both kinds is split.** The change's canon design reviews the application specs for what the change leaves out of sync there. It records that in its Impact on the Application Specs, and edits none of the application specs. That application work goes to the application design the canon design was spawned from, where there is one. Otherwise it is spawned or logged as this section's spawning paragraph has it. The canon and application designs may be worked in concert. A design changing the specs that leaves code out of sync edits none of the code either. It records the code it leaves out of sync in its Out of Scope, and that work goes to a design changing code, spawned or logged the same way. What an audit in the canon design's apply finds in the application specs is settled by [`§ A Design Document § Changes After Approval`](#changes-after-approval). What that table hands on is application work too. It is added to what the canon design's review handed on, or handed on the same way, so the canon design completes without editing the application specs. Where the application work finds the canon design wrong, the canon design takes the change while it is in-progress or approved, the user reopening an approved one. For any other canon change the application work needs, the application design spawns a canon design, which blocks it. A change to the canon design once that design is applying or complete is such a change too. Where the application design is approved, the user reopens it before the canon design is spawned. An application design already applying keeps to what was approved. The canon change is then spawned or logged without blocking it, as the user decides.

**Applying and committing.** A design's apply begins only as [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) lets the design move into applying. The user's approval of the plan authorizes the builder to write within the design's Target, no edit asking its own approval. A design's changes are:
- the writing its steps reach, within its Target;
- each direct edit a `direct-edit` entry of its log names, in a file the Target could name by its Kind;
- each edit of the user's a `user-edit` entry names, wherever it lies outside a working file, since the user confirmed it intended ([`§ Design Log Entry`](#design-log-entry), [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart)).

Every change the design makes is one of them. The design's changes are committed on their own, one commit for each design even where a branch holds several, so a revert takes exactly that design's changes, and the commit's message names each direct edit and each edit of the user's among them. [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) sets what becomes of them, and of every other change uncommitted in the design's checkout, at each event: a send-back, entering applying, the writing, the commit and an abandonment. An abandonment reverts through version control or, where the project has none, by hand.

### The Kinds of Change

What each kind bounds a change to:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
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

Once the user approves the plan, a passage outside the Target that the apply leaves false is a tactical fix ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) where a rewording that restates what the steps decide makes it true. Otherwise it is a finding lying in the plan, as [`§ A Design Document`](#a-design-document)'s paragraph on applying and committing bounds a design's changes. A finding the post-apply review makes within the Target lies in the plan or in the writing, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review) has the review settled, unless it is on text whose migration the frame hands on, which lies in neither. This section's table settles that finding, one outside the Target, and each finding the builder's self-review makes over the work and does not fix in the writing, as it settles an audit's. The builder triages and marks an audit's findings, as [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) has an audit read. Before this section's table, the builder applies [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) to each finding the table would settle, and records each finding the test drops in its triage. Each finding the test keeps is presented to the user and settled by the questions that sort it, asked in order:
- **Caused by the design?** The builder's triage answers it, and a post-apply review's finding outside the Target is triaged as an audit's is, by the one test [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) states in its opening, which also gives what holds the files as they stood, with or without version control.
- **Judged wrong by the user?** The user's judgment as the finding is presented.
- **In a file the design's Kind lets it change?** A canon design's finding in the application specs, and a code design's in the specs, answer false.
- **Handed on by the frame?** A rule the design changed may find a breach in text the apply carried over. That finding answers true where the design's Out of Scope hands the text's migration on, to a design of its own or a follow-up, as [`§ A Design Document`](#a-design-document)'s paragraph on spawning has such work handed on. It answers false where the goals take the migration in, since the migration is then the steps'. It answers false too where the frame hands nothing on, having missed text it should have held. A script check's finding and a semantic check's are answered alike.
- **A tactical fix?** As the glossary defines one. Every nit answers true. A finding asking to reword wording an Objective quotes answers false whatever its mark, as [`§ Design Plan Step`](#design-plan-step) has that wording frozen.
- **Lying in the plan?** A finding lying in the plan, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review) sorts one, answers true.

So a tactical fix never sends a design back, no design edits a file its Kind does not let it change, no migration the frame hands on is made in the design, and no row sends a tactical fix the user declines back to the writing or into the plan:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Caused by the design?, Judged wrong by the user?, In a file the design's Kind lets it change?, Handed on by the frame?, A tactical fix?, Lying in the plan?

| Caused by the design? | Judged wrong by the user? | In a file the design's Kind lets it change? | Handed on by the frame? | A tactical fix? | Lying in the plan? | Settles |
|---|---|---|---|---|---|---|
| false | - | - | - | - | - | settled as the user chooses, and recorded in the builder's triage: ignored; given a design spawned for it; or logged as a follow-up ([`§ A Follow-up`](#a-follow-up)) |
| true | true | - | - | - | - | set aside, and recorded in the builder's triage with the reason |
| true | false | false | - | - | - | handed on as work of another kind, as [`§ A Design Document`](#a-design-document)'s paragraph on a change needing both kinds has it |
| true | false | true | true | - | - | recorded in the builder's triage against the design or follow-up the Out of Scope hands the migration to |
| true | false | true | false | true | - | made as a direct edit the user approves ([`specs/AGENTS.md § Design, Refactor, Refine § Direct Edits`](/specs/AGENTS.md#direct-edits)), logged as a `direct-edit` entry, or left as the user chooses |
| true | false | true | false | false | true | sends the design back to in-progress, its changes kept, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has one |
| true | false | true | false | false | false | goes back to the writing, where the builder rewrites what the finding reaches |

### Uncommitted Changes

What becomes of each change uncommitted in a design's checkout at each event of its work, by what the change is, sorted by its answers to the questions:
- **Written by the builder?** Whether the builder wrote the change, in this apply or in one a send-back kept.
- **Reached by a step?** Whether a step of the plan as it now stands reaches it, the steps' writing within the Target.
- **Logged?** Whether a `direct-edit` or a `user-edit` entry names it ([`§ Design Log Entry`](#design-log-entry)).

So the steps' writing, a logged direct edit and a logged user's edit are the design's changes, as [`§ A Design Document`](#a-design-document)'s paragraph on applying and committing has them. The builder's writing that no step reaches and no entry logs is none of them. At the writing state, the builder removes it, so none of it is left at the commit. A change the builder did not write that no entry logs is confirmed with the user, as [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart) has an edit of the user's confirmed:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Written by the builder?, Reached by a step?, Logged?, Event \
**Input Values:**
  - Event: "a send-back", "entering applying", "the writing", "the commit", "an abandonment"

| Written by the builder? | Reached by a step? | Logged? | Event | What Becomes Of It |
|---|---|---|---|---|
| true | - | - | "a send-back" | kept in place |
| false | - | true | "a send-back" | kept in place |
| false | - | false | "a send-back", "the writing", "the commit" | confirmed with the user |
| true | - | - | "entering applying" | admitted |
| false | - | true | "entering applying" | admitted |
| false | - | false | "entering applying" | refused, the design held in approved |
| - | - | true | "the writing" | kept |
| true | true | false | "the writing" | kept |
| true | false | false | "the writing" | removed |
| - | - | true | "the commit" | committed in the design's commit |
| true | true | false | "the commit" | committed in the design's commit |
| true | false | false | "the commit" | left out of the commit |
| true | - | - | "an abandonment" | reverted |
| false | - | true | "an abandonment" | reverted or kept, as the user chooses |
| false | - | false | "an abandonment" | left as it stands |

### The States It Moves Through

The states a design document's Status moves through, and what moves it from one to the next:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
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
| approved | applying | the user gives the go-ahead to apply | its Depends On names none, [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) admits every uncommitted change, and no other design is applying in the checkout |
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

A design sent back from applying goes back to in-progress with the changes [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) keeps in place at a send-back, never set aside or reverted, since they are the plan's work with flaws to rework, not work to undo. A change the builder did not write that no entry logs is confirmed with the user first, as that section has it. These, with each edit of the user's a `user-edit` entry logs since, are the changes a send-back kept, and that section says what becomes of them at each later event. Its steps are revised against the last commit, as any design's are. The kept changes are its apply's unfinished writing, never a baseline: as the design applies again, the builder, at the writing state, keeps what the revised steps reach and removes only what is none of the design's changes, so the post-apply review finds nothing outside them. While kept changes stand in a checkout, every reading for a design in it, a review's, the builder's self-review and another design's among them, reads the files at the last commit wherever it would otherwise read the files as they stand. It reads the kept changes as the apply's unfinished writing, from their diff against that commit.

The kept changes hold their checkout as an apply's changes do. The design enters applying again as [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) admits, and no other design applies in that checkout, so each commit holds one design's changes. A design that must apply while they stand, such as a dependency the sent-back design gains, applies in the same checkout on a branch of its own, made as [`specs/AGENTS.md § Design, Refactor, Refine § A New Branch`](/specs/AGENTS.md#a-new-branch) has a new branch made. The kept changes are stashed meanwhile, so nothing is uncommitted as it enters applying. They are restored as the sent-back design applies again, its writing reconciling them with that design's commit. The working files, untracked, stay in place for both. An abandonment of the sent-back design while they are stashed restores them first, so the rows for an abandonment act on them. Where the project has no version control, nothing is stashed, so a sent-back design takes on no dependency its kept changes would block: the change it needs joins its own steps, or the design is abandoned.

### A Design Changing Code

A design changing code starts from applied specs, or from the specs as a design its Depends On names leaves them, rather than from a problem in them. It designs the code and the tests that bring the specs to life. It takes the form [`§ A Design Document`](#a-design-document) sets, the Design, Refactor, Refine process, the validation review, the adversarial review, the stamp and the post-apply review, as a design changing the specs does. It differs only where code does. Its parts differ so:

**Reference Key:** Part \
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

A design's goals ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) are agreed on before its design frame, and changed and weighed, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has them. A goal is named, never numbered, so a record speaks of a goal by its Name however the list changes. A record cites a goal as a record is cited, by its record section and its Name ([`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation)).

A design's goals sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Goals \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the goal's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which the record names and cites it |
| Description | no | yes | | text | what the goal asks of the change |

## Design Plan Step

Each step of a design's plan states what it changes and the state the applied work holds once it is changed, never the text or the code that brings the state about. That text or code is written at the apply ([`specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow.md#the-apply)). A step reaches as many files as its change does, and the design's Target is every file its steps reach.

**An Objective is an outcome.** An Objective ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) describes the outcome, never the work to reach it, and it names no phrase or passage to change. Everything a step's Objectives do not state stands as it is. A step's Objectives freeze what they state, never the words carrying it, whatever the design's kind. A step changing a mechanism states each part it adds, changes or removes, such as its rows, fields, conditions, outcomes, states, transitions, guards, facts and steps, in the form its construct's definition gives that part. It writes a value, an expression or a citation as the spec writes it. An Objective adding a Decision Table or a State Machine, or rewriting one whole, opens with a citation of the section the construct stands in, `{path} § {section}`. Indented under the Objective, it states the construct whole in its form ([`specs/methodology/modeling-constructs.md § Constructs`](/specs/methodology/modeling-constructs.md#constructs)), as a mechanism's form is its outcome. An Algorithm's, a DAG's and a Constraint's parts, and a Basic Table's and a record type's rows, are stated as any other outcome, never whole. A step states each passage of prose by the meaning it holds, never by quoting its words, each part written as free prose among them, such as a Description, a Fact's Means and an outcome written as prose. So rewording such a passage while keeping its meaning is a tactical fix ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)). An Objective quotes wording only where the wording is itself the outcome, a steer's chosen words among it, and so freezes that wording: rewording it is a finding lying in the plan, never a tactical fix. A step's Why cites a goal the step serves, as a record cites a goal ([`§ Design Goal`](#design-goal)).

A design's steps sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Plan Steps \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the step's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which the record names and cites it |
| What | no | yes | | text | what the step changes, the files and sections it reaches |
| Why | no | yes | | text | why the step is needed, citing each goal it serves |
| Objectives | no | yes | | text | a list of the states the applied work holds once the step is applied, each an Objective |

## Design Log Entry

A design's log records each check of its work and each event of its workflow, an entry each. This section declares the log's form alone: what an entry means to a check or a state is stated where that check or state is. An entry holds values alone. Each entry is appended through the design script of the skill writing the design, by its `--append-entry`. The script counts the entry among its kind and stamps it with the UTC time of appending. So the entries stand in the order their events came, and a check holds their order to their timestamps.

**When an entry is appended.** Each entry is appended when the kinds table has it appended, at the skill's step where its event ends, never in a pass after the work. A check's entry is appended by the step running the check, as its settling ends with its report in hand, and the design script's `--append-entry` refuses a check's entry whose report does not yet exist. Where the work moves past a check before its settling ends, whatever moves it, the user's approval, a steer or a send-back among them, the check's entry is appended once its report is in. Its counts are the marks its report gives, its Dropped is 0, and its Led To is the state that move took the design into. So every check that ran has its entry. An approval given in reassessing is a `plan-approval` entry in place of a `reassessment` one.

**What a check counts.** Each count counts what its check found, by the mark each holds once settled ([`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not`](/specs/AGENTS.md#converging-or-not)). A finding dropped is counted in Dropped alone, and a review observation ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) in none. The builder marks what its own Design, Refactor, Refine pass, self-review and handed-off judgment found as a review's findings are marked, and appends each entry with the model and effort it ran on.

**A check's report.** A check's entry names its report, `{design}-{entry}.md`, in the folder of `.ai/tmp/` of the skill writing the design ([`§ The Working Files`](#the-working-files)). The report is one of:
- a review's report, with the builder's settlement added;
- a report of the builder's Design, Refactor, Refine pass, of its self-review or of its handed-off judgment, holding what it found and how each was settled, its traces and tests among them;
- the builder's triage of an audit.

A design's log sits in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Log Entries \
**Reference Key:** Entry

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Entry | yes | yes | | text | its kind, one of this section's kinds table, a hyphen and its count among its kind from 1, as `adversarial-review-2` |
| Timestamp | no | yes | | text | the UTC time it was appended, as [`§ A Stamp`](#a-stamp) writes a timestamp |
| Model | no | where its kind gives it | | text | the model the check ran on |
| Effort | no | where its kind gives it | | "light", "medium", "high", "as the agent allows" | the reasoning effort the check ran at, one of the levels [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) names, or `as the agent allows` where the agent could not apply the level chosen, or where, for a builder's own check, no level it ran at is named |
| Design Flaws | no | where its kind gives it | | text | the count of design flaws the check found, a whole number |
| Implementation Flaws | no | where its kind gives it | | text | the count of implementation flaws the check found, a whole number |
| Nits | no | where its kind gives it | | text | the count of nits the check found, a whole number |
| Dropped | no | where its kind gives it | | text | the count of findings dropped as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) has a finding dropped, a whole number |
| Led To | no | where its kind gives it | | text | the state the work went into as the check ended, by its settling or by whatever moved the work past it |
| Reason | no | where its kind gives it | | text | why the design entered in-progress, one of the values of [`specs/methodology/design-workflow.md § The Order of a Design's Work § Facts [Name: entry reason]`](/specs/methodology/design-workflow.md#facts) |
| Approval | no | where its kind gives it | | "approved", "approved and apply" | the user's approval of the plan |
| Decision | no | where its kind gives it | | text | what the user decided, one of the values of [`specs/methodology/design-workflow.md § The Order of a Design's Work § Facts [Name: reassessment]`](/specs/methodology/design-workflow.md#facts) |
| Places | no | where its kind gives it | | text | where the edit lies, each a path, its section after it where the edit lies in one, separated by semicolons |

The kinds of entry, each with the fields it gives beside Entry and Timestamp, and when it is appended:

**Reference Key:** Kind \
**Required:** Fields, Appended

| Kind | Fields | Appended |
|---|---|---|
| `design-refactor-refine` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | as the builder's Design, Refactor, Refine pass ends |
| `self-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | as the builder's self-review ends |
| `handed-off-judgment` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | as the settling of a judgment the builder handed off ends |
| `adversarial-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To | as the round's settling ends |
| `post-apply-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To | as the round's settling ends |
| `audit-specs` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To | as the settling of an `.ai/skills/audit-specs/` run ends |
| `verify-spec-implementation` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To | as the settling of a `.ai/skills/verify-spec-implementation/` run ends |
| `entered` | Reason | as the design enters in-progress |
| `plan-change` | none | as the builder's revision of the steps at drafting or changing ends, before its Design, Refactor, Refine pass and its self-review |
| `plan-approval` | Approval | as the user approves the plan |
| `user-edit` | Places | in any state of the apply, or while the design is sent back with its changes kept, as the user confirms the edit intended |
| `reassessment` | Decision | as reassessing ends |
| `another-round` | none | as the user asks for another round |
| `apply` | none | as applying begins |
| `direct-edit` | Places | in any state of the apply, as the direct edit is made |

## Retired Phrase

A design retiring wording records it, so the builder's tools, not a rereading, find every place the wording stands. The design script's `--show-reach` lists each place the wording stands at drafting, and its `--check-retired-wording` reports any left in the Target's files at the builder's self-review before the post-apply review ([`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why)). A phrase the user turned down while steering is recorded as one too.

A design's retired wording sits in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Retired Phrases \
**Reference Key:** Phrase

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Phrase | yes | yes | | text | a word or phrase the design stops using in one sense, matched as whole words regardless of case |
| Replacement | no | yes | | text | what the design uses instead |
| Stays Right | no | no | none | text | the places the phrase stays right, each a path, its section after it where the place is one, separated by semicolons |

## Steering Decision

A design's Steering Decisions record only the user's steers, the decisions a steering decision records ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), such as new scope or a design flaw's fix. A steer differs from the user's direction about how the work proceeds, from the user's feedback on the applied result and from a decision about other work, as [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart) tells them apart.

**A go-ahead to take in findings.** It is a steer for the findings that change what the design is, and direction for the tactical fixes ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)). An answer carrying both is recorded for the part that decides the design.

**Each steer is recorded when it is given.** The design is then revised to apply the steer before its work goes on, so the design carries how it was formed and never lags a steer it records. A steer changing the goals or the frame is confirmed with the user, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has it. It is carried into the goals or the frame, its case reaching the Scope, the Approach and the Outcomes. Any other steer, such as one choosing wording a step quotes as its outcome or a name in code, is recorded as given. The record tells the adversarial review the user chose it. Where the steer differs from another choice only by preference, it stands. Where it breaks a rule, the review raises it as a finding pressing on the steer. The builder presents the conflict to the user with a wording or a name that follows the rule, and the user chooses either ([`§ Steering Decision § Revisiting a Steer`](#revisiting-a-steer)). Only the user revises a steer, by a later one. The record is history. A later steer revising what an earlier one decided is recorded after it, and its Decision says which steer it revises. The earlier one stays as it was given. The design follows the later one, whatever the Type of either, so the records, read in order, show how the design was shaped. A question the user leaves unanswered is asked again, never read as agreed. The adversarial review reads the steers as background, checking fidelity to them rather than reopening them ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review)). The request that opened the design is its Source. The design's log records each check and event of its work, never a steer, so each steer is recorded once.

A design's steering decisions sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Steering Decisions \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | a short name for what was decided |
| Prompted By | no | yes | | text | what the steer answered: a question, proposal or account the builder gave, with the options it offered where it offered any, a review's finding named by its ID, or the user's own initiative |
| Type | no | yes | | "selection", "perspective" | a selection or a perspective, as [`§ Steering Decision § A Steer's Type`](#a-steers-type) has it |
| Steer | no | yes | | text | the user's own words, quoted |
| Decision | no | yes | | text | the essence of what the steer decided, in a sentence or two |

### A Steer's Type

A steer is a selection where the user only selects one of the options the builder offered, a literal selection. Every other steer is a perspective, whatever its form, such as emphasis, a negative remark, a nudge or a strong direction for the design. Selecting an option is easier than sharing a perspective, and a perspective originates with the user.

### Telling a Steer Apart

#### Steer, Direction, Feedback, Other Work or the User's Edit

During an apply, or while the design is sent back with its changes kept, a steer, direction about the work, feedback on the applied result, a decision about other work and the user's own edit are each recorded by its row. An answer carrying more than one is taken a part at a time:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** What the user decides \
**Annotations:** Sounds Like

| What the user decides | Recorded | Tells a reviewer | Sounds Like |
|---|---|---|---|
| A steer | in Steering Decisions, its Steer quoting every part of the user's words that decides the design, never only the last of them | how the design was formed | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found", "call it Kind, not Type" |
| Direction about the work | not as a steer; where the record needs it, as an entry of the design's log ([`§ Design Log Entry`](#design-log-entry)), or in the Status field | nothing about what the design is | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "the applied result is approved", "create the branch", "medium effort", "G1 to G6 are design flaws", "go on" or "rescope it" deciding a reassessment, the new scope then steered at framing |
| Feedback on the applied result | not as a steer; taken into the writing, the post-apply review reading what it changes | nothing about what the design is | "that paragraph buries the rule", "say it in fewer words", "the example reads wrong" |
| A decision about other work | where that work is held | nothing about the design being worked | "the implement-specs design should weigh renaming the workstack", "keep the billing service stateless when we design it" |
| The user's own edit, made in a file during an apply or while the design is sent back with its changes kept | not as a steer; the builder confirms with the user whether it was intended, since it may be accidental, and reverts an accidental edit; an intended one it takes in as it stands and logs as a `user-edit` entry naming its places ([`§ Design Log Entry`](#design-log-entry)), one of the design's changes ([`§ A Design Document`](#a-design-document)), checking it as its self-review's row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) has it | nothing about what the design is; the reviews read a change in its places as the user's | "I reworded that sentence in the README", "I fixed the typo in the brief myself" |

### A Decision About Other Work

A decision about other work is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory. A decision about more than one design is recorded in each. What becomes of the decision, by where the work is held:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
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
- **The content hash.** SHA-256 of the file's text, encoded as UTF-8 with line-feed line endings, after dropping the lines that hold the fields and the sections the form leaves out. It is written as `sha256:` followed by the digest's first sixteen hexadecimal characters, lowercase. The hash detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding the stamp and the fields the stamp leaves out. The stamp always leaves out its own field, since writing the stamp must not change the hash. It also leaves out any field whose change the check does not concern, as a design document's Validated field leaves out its Status ([`§ A Design Document`](#a-design-document)). It may leave out a section too, its heading through the next heading of its level, as a design document's stamp leaves out its Design Log Entries, so an entry appended after the stamp leaves it current.

## A Follow-up

A follow-up records work on the specs, the code or the working files that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. A follow-up is written, or amended, only once the user approves its text, shown first. `.ai/follow-ups.md` opens with a short header naming what the file holds and citing this file. The follow-ups follow that header. Each follow-up sits under a priority heading:
- `## High`, the work to take up next;
- `## Medium`, which waits until High is settled;
- or `## Low`, worth doing once nothing more pressing is open.

Each follow-up holds these parts, in this order:

**Reference Key:** Part \
**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `###` heading, a kebab-case slug | yes | | the name the follow-up is referred to by |
| Status | a `**Status:**` field | yes | | where the follow-up is in this section's life cycle |
| Category | a `**Category:**` field | yes | | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` field | yes | | the file, section or files it concerns |
| Body | prose | yes | | the work, the context needed to take it up, and, where known, what found it, naming the design that handed the work on where one did |

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
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
