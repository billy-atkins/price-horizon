## The Order of a Design's Work

Two State Machines set the order a design's work takes, and what moves it back. The design's Status runs them ([`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through)). [`§ The Order of a Design's Work § The Work of a Design`](#the-work-of-a-design) governs the in-progress state, and [`§ The Order of a Design's Work § The Apply`](#the-apply) governs the applying state. Each state's work is done as the section it cites has it, so the machines hold the order alone. The principles stay in [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine). A design changing code takes the same order ([`specs/methodology/working-files.md § A Design Document § A Design Changing Code`](/specs/methodology/working-files.md#a-design-changing-code)).

### The Work of a Design

A design enters its work by the reason its Status entered in-progress. Its change leads back to another adversarial review wherever needs review? or needs reframing? holds and the user's approval has not ended its review ([`§ The Order of a Design's Work § Facts`](#facts)). A design its Depends On names finishing is a class of occurrences. This machine's Trigger Classes table cites the section that lists its members.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| entered | the design has entered in-progress, by its Status's move | Yes | No |
| framing | the builder agrees on the design goals with the user and states the design frame, or revisits either, and brings them to the user, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has the goals, then the frame, come first, taking in each steer the user gives and each design its Depends On names that has finished ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)) | No | No |
| drafting | the builder takes the design's steps through the Design, Refactor, Refine process ([`specs/AGENTS.md § Design, Refactor, Refine § Design`](/specs/AGENTS.md#design), [`specs/AGENTS.md § Design, Refactor, Refine § Refactor`](/specs/AGENTS.md#refactor), [`specs/AGENTS.md § Design, Refactor, Refine § Refine`](/specs/AGENTS.md#refine)), recording each steer as it is given ([`specs/methodology/working-files.md § Steering Decision`](/specs/methodology/working-files.md#steering-decision)) and taking in each design its Depends On names that has finished ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)), then makes its self-review, as its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) sets, and, before the design's first adversarial review, or before its post-apply review where the user's approval of the plan ends the review before any round, offers the user the review's model and reasoning effort | No | No |
| reviewing | a cold agent runs the adversarial review, as [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) has it | No | No |
| settling | the builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it: the user triages its design flaws and answers its other calls, and the builder settles the rest. The builder takes in each steer the user gives and each design its Depends On names that has finished, one finishing while the design was reviewed among them. Where the user's approval has ended the review, the builder settles nothing, and the round's findings are left as they are | No | No |
| reassessing | the builder and the user step back and reassess, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging, taking in each design its Depends On names that has finished | No | No |
| reassessing the send-backs | the builder and the user step back and reassess a run of the design's applies sent back, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging, taking in each design its Depends On names that has finished | No | No |
| changing | the builder revises the design, as the round was settled, taking in each steer the user gives and each design its Depends On names that has finished ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)), takes each step the change moved through the Design, Refactor, Refine process, then makes its self-review, proving the change, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove`](/specs/AGENTS.md#change-and-prove) has it | No | No |
| waiting | the design waits for each design its Depends On names to be approved or applying, as [`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document) has a design go to the user's approval only then | No | No |
| validating | the builder runs `--check-workstack` and puts right what it reports, and the validation review checks the design document's structure, as its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) sets, the builder fixing what it reports and running it again until it passes, the review stamping the design on its way to the user's approval ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)) | No | No |
| awaiting approval | the user is asked to approve the plan, shown it as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval | No | No |
| approved by the user | the user approved the plan | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| entered | framing | none | entry reason = "taken up" |
| entered | framing | none | entry reason = "sent back" and consecutive send-backs < 3 |
| entered | reassessing the send-backs | none | entry reason = "sent back" and consecutive send-backs >= 3 |
| entered | changing | none | entry reason = "reopened" |
| entered | changing | none | entry reason = "a dependency finished" |
| entered | waiting | none | entry reason = "a dependency moved back" |
| reassessing the send-backs | framing | the user decides the reassessment | none |
| reassessing the send-backs | changing | the user approves the plan | none |
| framing | drafting | the user agrees on the goals and agrees to or adjusts the frame | none |
| drafting | framing | the user gives a steer | needs reframing? |
| drafting | validating | none | none |
| reviewing | settling | none | none |
| reviewing | changing | the user gives a steer | none |
| settling | reassessing | none | not(review ended by approval?) and (consecutive design flaw rounds >= 3 or consecutive implementation flaw rounds >= 5) |
| settling | changing | none | review ended by approval? or (consecutive design flaw rounds < 3 and consecutive implementation flaw rounds < 5) |
| reassessing | framing | the user decides the reassessment | reassessment != "go on" |
| reassessing | changing | the user decides the reassessment | reassessment = "go on" |
| reassessing | changing | the user approves the plan | none |
| changing | framing | none | needs reframing? |
| changing | validating | none | not(needs reframing?) |
| waiting | validating | when depends on ready? | none |
| waiting | changing | the user gives a steer | none |
| waiting | changing | a design its Depends On names finishes | none |
| validating | reviewing | none | needs review? and not(review ended by approval?) |
| validating | awaiting approval | none | (not(needs review?) or review ended by approval?) and depends on ready? and not(plan approved?) |
| validating | approved by the user | none | (not(needs review?) or review ended by approval?) and depends on ready? and plan approved? |
| validating | waiting | none | (not(needs review?) or review ended by approval?) and not(depends on ready?) |
| validating | changing | the validation review reports a problem | fix changes the plan? |
| validating | waiting | [`specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files.md#the-states-it-moves-through) of a design its Depends On names is entered | not(needs review?) or review ended by approval? |
| validating | changing | the user gives a steer | none |
| validating | changing | a design its Depends On names finishes | none |
| awaiting approval | approved by the user | the user approves the plan | depends on ready? |
| awaiting approval | changing | the user does not approve the plan | none |
| awaiting approval | drafting | the user asks for another round | none |
| awaiting approval | waiting | [`specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files.md#the-states-it-moves-through) of a design its Depends On names is entered | none |
| awaiting approval | changing | a design its Depends On names finishes | none |

**Table Name:** Trigger Classes

| Member | Class |
|---|---|
| [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) | a design its Depends On names finishes |

### The Apply

A design's apply begins only as [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) lets a design enter applying, and it ends applied or sent back. The order the apply takes:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| writing | the builder writes each step's text or code with each file open, within the Target, from the files as they stand, the changes a send-back kept among them ([`specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files.md#a-send-back)), keeps or removes each uncommitted change as [`specs/methodology/working-files.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files.md#uncommitted-changes) has it at the writing, takes in each edit the user makes as [`specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`](/specs/methodology/working-files.md#telling-a-steer-apart) has it, takes in the user's feedback on the applied result, then makes its self-review of what it wrote, as its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) sets, and starts the post-apply review, a cold agent's on the model and reasoning effort the user chose for the design | Yes | No |
| post-apply reviewing | a cold agent runs the post-apply review, as its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) sets | No | No |
| settling the post-apply round | the builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it, and the user triages a finding lying in the plan. The builder makes the round's tactical fixes and sets plan finding? and writing flaw? by what the round found | No | No |
| user reviewing | the builder shows the user the applied result with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and the post-apply review's entry and report, and waits on the user | No | No |
| auditing | a cold agent runs an audit, given the skill's name and the kinds [`§ A Design's Reviews`](#a-designs-reviews) sets, as its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) sets | No | No |
| settling the audit | the builder reads and triages the audit's findings as [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) has an audit read, each settled as [`specs/methodology/working-files.md § A Design Document § Changes After Approval`](/specs/methodology/working-files.md#changes-after-approval) has it, and the builder sets plan finding? and audit rework? | No | No |
| reassessing the apply | the builder and the user step back and reassess, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging | No | No |
| awaiting the commit | the builder shows the user the settled audit with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and the commit for the design's changes, and waits for the go-ahead | No | No |
| committing | the builder commits the design's changes on their own, one commit for the design ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)) | No | No |
| applied | the text or code its steps call for is written, its post-apply review converged, the user's review given, its audit settled, and its changes committed where the project has version control | No | Yes |
| sent back | a finding lying in the plan, a steer, a reassessment of the apply, or its builder's finding that the plan cannot be delivered, triaged by the user as lying in the plan, sends the design back to in-progress, with the changes [`specs/methodology/working-files.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files.md#uncommitted-changes) keeps at a send-back in place, as [`specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files.md#a-send-back) has it | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| writing | post-apply reviewing | none | none |
| writing | sent back | the user triages the builder's finding that the plan cannot be delivered as its steps and Target state it as lying in the plan | none |
| post-apply reviewing | settling the post-apply round | none | none |
| settling the post-apply round | sent back | none | plan finding? |
| settling the post-apply round | reassessing the apply | none | not(plan finding?) and writing flaw? and consecutive post-apply flaw rounds >= 5 |
| settling the post-apply round | writing | none | not(plan finding?) and writing flaw? and consecutive post-apply flaw rounds < 5 |
| settling the post-apply round | user reviewing | none | not(plan finding?) and not(writing flaw?) |
| user reviewing | auditing | the user approves the applied result | none |
| user reviewing | post-apply reviewing | the user asks for another round | none |
| auditing | settling the audit | none | none |
| settling the audit | sent back | none | plan finding? |
| settling the audit | reassessing the apply | none | not(plan finding?) and audit rework? and consecutive rework audits >= 3 |
| settling the audit | writing | none | not(plan finding?) and audit rework? and consecutive rework audits < 3 |
| settling the audit | awaiting the commit | none | not(plan finding?) and not(audit rework?) and version control? |
| settling the audit | applied | none | not(plan finding?) and not(audit rework?) and not(version control?) |
| reassessing the apply | sent back | the user decides the reassessment | reassessment != "go on" |
| reassessing the apply | writing | the user decides the reassessment | reassessment = "go on" |
| awaiting the commit | committing | the user approves its commit | none |
| committing | applied | none | none |
| writing | sent back | the user gives a steer | none |
| post-apply reviewing | sent back | the user gives a steer | none |
| settling the post-apply round | sent back | the user gives a steer | none |
| user reviewing | sent back | the user gives a steer | none |
| auditing | sent back | the user gives a steer | none |
| settling the audit | sent back | the user gives a steer | none |
| reassessing the apply | sent back | the user gives a steer | none |
| awaiting the commit | sent back | the user gives a steer | none |
| post-apply reviewing | writing | the user gives feedback on the applied result | none |
| settling the post-apply round | writing | the user gives feedback on the applied result | none |
| user reviewing | writing | the user gives feedback on the applied result | none |
| auditing | writing | the user gives feedback on the applied result | none |
| settling the audit | writing | the user gives feedback on the applied result | none |
| awaiting the commit | writing | the user gives feedback on the applied result | none |

### Facts

**Records:**
  - **Name:** entry reason \
    **Type:** string \
    **Values:** "taken up", "reopened", "a dependency moved back", "a dependency finished", "sent back" \
    **Means:** why the design last entered in-progress, the move its Status took: taken up, reopened by the user, a design its Depends On names moving back to in-progress, one finishing, or its apply sending it back

  - **Name:** consecutive design flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's phase, this one among them, each not ended by the user's approval and finding a design flaw the user triaged as one, counted as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase converge; set back to zero by a round finding none and by the design's starting afresh at its frame, a reassessment's or a send-back's

  - **Name:** consecutive implementation flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's phase, this one among them, each not ended by the user's approval and finding an implementation flaw, a nit the builder judged harmful among them, counted as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase converge; set back to zero by a round finding none and by the design's starting afresh at its frame, a reassessment's or a send-back's

  - **Name:** consecutive send-backs \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the applies of the design in a row, this one among them, each ending sent back; set back to zero as an apply reaches awaiting the commit or applied; set back to zero too by a reassessment, of the send-backs or of the apply, that decides other than "go on", the apply it sends back not counted

  - **Name:** consecutive post-apply flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the post-apply rounds in a row of the apply, this one among them, each finding an implementation flaw lying in the writing; set back to zero by a round finding none and as an apply begins

  - **Name:** consecutive rework audits \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the audits in a row of the apply, this one among them, each sending a finding back to writing; set back to zero by an audit sending none and as an apply begins

  - **Name:** reassessment \
    **Type:** string \
    **Values:** "rescope", "split", "a different approach", "go on" \
    **Means:** what the user decided at a reassessment, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has one; a design abandoned leaves by [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) instead

  - **Name:** needs review? \
    **Type:** boolean \
    **Means:** whether the design takes another adversarial round before the user's approval: the last round it settled found a design flaw the user triaged as one or an implementation flaw, or its goals, its frame or its steps have moved since that round began, or it has settled none since it was last framed, or the user asked for another round ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review), [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame))

  - **Name:** needs reframing? \
    **Type:** boolean \
    **Means:** whether a steer the design took in changed its goals or its frame and the user has not yet approved the change, so they go back to the user for approval, the frame re-evaluated against goals that changed ([`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame))

  - **Name:** review ended by approval? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given before its adversarial review ended, ended it ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). The approval sets it in any state of the design's work. No transition fires on it but the reassessments', and each state finishes its own work first. It is set back to false only where the design is sent back, a reassessment starts it afresh or the user asks for another round. So a change after the approval keeps it, a reopen or a dependency's move among them, even one changing the goals or the frame, and the design comes back to the user

  - **Name:** plan approved? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given in any state of its work, covers the plan as it stands ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). It is set back to false by a change after the approval to the design's goals, its frame or its steps, and by the design's entering in-progress again. After such a change, the design comes back to the user to approve again

  - **Name:** fix changes the plan? \
    **Type:** boolean \
    **Means:** whether fixing a problem the validation review reports changes the design's goals, its frame or a step, and not only the record around them

  - **Name:** depends on ready? \
    **Type:** boolean \
    **Means:** whether each design its Depends On names is approved or applying

  - **Name:** plan finding? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the post-apply round or the audit just settled holds a finding lying in the plan, as [`specs/methodology/working-files.md § A Design Document § Changes After Approval`](/specs/methodology/working-files.md#changes-after-approval) has one; set by the settling state, and set back as that state is left

  - **Name:** writing flaw? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the post-apply round just settled found an implementation flaw lying in the writing; set by settling the post-apply round, and set back as it is left

  - **Name:** audit rework? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether a finding of the audit just settled, one the design caused, goes back to writing, as [`specs/methodology/working-files.md § A Design Document § Changes After Approval`](/specs/methodology/working-files.md#changes-after-approval) has it; set by settling the audit, and set back as it is left

  - **Name:** version control? \
    **Type:** boolean \
    **Means:** whether the project keeps its files under version control

## A Design's Reviews

A design's Kind sizes its reviews and its audit. The effort they take grows with what a flaw in the design would cost. A design whose Target names files of more than one Kind takes the highest effort among them. The kinds of the files its Target names pick its audit, each file's kind as [`specs/methodology/working-files.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files.md#the-kinds-of-change) defines it. Where they include `code`, the audit is `.ai/skills/verify-spec-implementation/`'s full run. Where they include any other kind, it is an `.ai/skills/audit-specs/` run given those kinds as the skill's `--kind`, which reads only the audits, and the files, of those kinds. A design whose Target names both runs both. A run given `canon-specs` reads every audit but the audit of the working files' form, over the files of every kind but `code`, since a change to the canon can leave any such file in breach of it, the application specs among them. A run the user starts with no kind is the full run, every audit over the skill's complete scope, the audit of the working files' form among them. No audit a design's apply runs reads a working file. The effort each Kind gives is a review's default ([`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind

| Kind | Effort |
|---|---|
| `canon-specs` | high |
| `application-specs` | medium |
| `code` | medium |
| `documentation` | light |
| `other` | medium |

A flaw in the canon is reproduced in every spec written under it. A mint's engraving plate works the same way: a flaw in it is reproduced on every banknote it prints. A flaw in the documentation reaches no file beyond it. A flaw in the application specifications reaches the code built from them, and a flaw in code reaches what it runs, so each takes the middle effort. What another file reaches is not known in advance, so it takes the middle effort too.

## A Review's Brief

Every adversarial review and every post-apply review the standard process runs is started with this brief alone, the same in every round, so the design is the one thing that changes between rounds. The brief holds no part of a review's task. The review's section, [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) or [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review), and its row of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) hold the whole of it. The builder fills the brief's blanks as it starts a round, and adds nothing about the design or the rounds before it. What a finding means and where it goes stay the builder's to settle. The brief sits in a fenced block, so no link is written into it and it stays this text:

```text
You are the {adversarial | post-apply} reviewer of a Spec of Record design. You are cold: you did not build or apply it, and you change nothing but your report.

Design: {design document}
Report: {report file}

1. Read specs/AGENTS.md, then specs/methodology/glossary.md, then the design document whole.
2. Do the {adversarial | post-apply} review as specs/AGENTS.md § Design, Refactor, Refine § {The Adversarial Review | The Post-Apply Review} and its row of specs/AGENTS.md § Design, Refactor, Refine § Who Checks What set it.
3. Write the report with its kept findings, its dropped findings and its review observations each apart, and end with its path, a count of its kept findings by mark, and its dropped findings and review observations listed without a count.
```

An audit takes no brief. Whoever starts one, the user or the builder in a design's apply, starts a cold agent given the skill's name and, in a design's apply, the kinds [`§ A Design's Reviews`](#a-designs-reviews) sets, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What`](/specs/AGENTS.md#who-checks-what) has an audit run.

## A Review's Effort

A review's reasoning effort is the level the user chose ([`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort)). The level is applied in the way the agent in use can apply it. The builder offers only a level the agent in use can apply. Where the agent in use can apply none, the review runs as the agent allows. How a level is applied:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** How the agent applies a level, definition set up?

| How the agent applies a level | definition set up? | Applied |
|---|---|---|
| "as it starts a reviewer" | - | at the nearest level the agent offers, set as the reviewer starts |
| "through a reviewer definition" | true | through the definition the agent was set up with for that level ([`specs/methodology/skills.md § Setting Up an Agent`](/specs/methodology/skills.md#setting-up-an-agent)) |
| "through a reviewer definition" | false | as the agent allows, the agent's setting itself up offered to the user for the reviews after it, since a definition written now may load only once the agent restarts (`.ai/skills/configure-spec-of-record/`) |
| "not at all" | - | as the agent allows |
