## The Order of a Design's Work

Two State Machines set the order a design's work takes, and what moves it back. The design's Status runs them ([`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through)). [`§ The Order of a Design's Work § The Work of a Design`](#the-work-of-a-design) governs the in-progress state, and [`§ The Order of a Design's Work § The Apply`](#the-apply) governs the applying state. Each state's work is done as the section it cites has it, so the machines hold the order alone. A state running a check of a design names it as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has a check named where it runs. The principles stay in [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine). A design changing code takes the same order ([`specs/methodology/working-files.md § A Design Document § A Design Changing Code`](/specs/methodology/working-files.md#a-design-changing-code)).

### The Work of a Design

A design enters its work by the reason its Status entered in-progress. Its change leads back to another adversarial review wherever needs review? or needs reframing? holds and the user's approval has not ended its review ([`§ The Order of a Design's Work § Facts`](#facts)). A design its Depends On Designs names finishing is a class of occurrences. This machine's Trigger Classes table cites the section that lists its members.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| entered | the design has entered in-progress, by its Status's move | Yes | No |
| framing | the builder agrees on the design goals with the user and states the design frame, or revisits either, and brings them to the user, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has the goals, then the frame, come first, taking in each steer the user gives and each design its Depends On Designs names that has finished ([`specs/methodology/working-files.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files.md#blocked-and-to-revise)) | No | No |
| drafting | the builder takes the design's steps through the Design, Refactor, Refine process ([`specs/AGENTS.md § Design, Refactor, Refine § Design`](/specs/AGENTS.md#design), [`specs/AGENTS.md § Design, Refactor, Refine § Refactor`](/specs/AGENTS.md#refactor), [`specs/AGENTS.md § Design, Refactor, Refine § Refine`](/specs/AGENTS.md#refine)), recording each steer as it is given ([`specs/methodology/working-files.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files.md#when-a-steer-is-recorded)) and taking in each design its Depends On Designs names that has finished ([`specs/methodology/working-files.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files.md#blocked-and-to-revise)), then makes its self-review, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles) has it, appending its pass's entry and its self-review's through `--append-entry`, which checks each report by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks), and offers the user the review's model and reasoning effort when [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has them chosen | No | No |
| reviewing | a cold agent runs the adversarial review, as [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) has it | No | No |
| settling | The builder first checks the review's report by the design script's `--check-report`, by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), handing a report out of its form back as [`specs/methodology/working-files.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files.md#who-writes-each-part) has it. The builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it: the user triages its design flaws and answers its other calls, and the builder settles the rest. The builder takes in each steer the user gives and each design its Depends On Designs names that has finished, one finishing while the design was reviewed among them. Where the user's approval has ended the review, the builder settles nothing, and the round's findings are left as they are. Its settling ends as it appends the round's entry through `--append-entry`, which checks the report by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks) | No | No |
| reassessing | the builder and the user step back and reassess, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging, taking in each design its Depends On Designs names that has finished | No | No |
| reassessing the send-backs | the builder and the user step back and reassess a run of the design's applies sent back, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging, taking in each design its Depends On Designs names that has finished | No | No |
| changing | the builder revises the design, as the round was settled, taking in each steer the user gives and each design its Depends On Designs names that has finished ([`specs/methodology/working-files.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files.md#blocked-and-to-revise)), makes the change in the top-down order [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) gives a change, takes each step the change moved through the Design, Refactor, Refine process, then makes its self-review, appending its pass's entry and its self-review's through `--append-entry`, which checks each report by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks), proving the change, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove`](/specs/AGENTS.md#change-and-prove) has it | No | No |
| waiting | the design waits for each design its Depends On Designs names to be approved or applying, as [`specs/methodology/working-files.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files.md#blocked-and-to-revise) has a design go to the user's approval only then | No | No |
| validating | the builder runs `--check-workstack` and puts right what it reports, and the validation review checks the design document's structure, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles) has it, the builder fixing what it reports and running it again until it passes, the review stamping the design on its way to the user's approval ([`specs/methodology/working-files.md § A Design Document § The Record's Checks`](/specs/methodology/working-files.md#the-records-checks)) | No | No |
| awaiting approval | the user is asked to approve the plan, shown it as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval | No | No |
| approved by the user | the user approved the plan | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| entered | framing | none | entry reason = "taken up" |
| entered | framing | none | entry reason = "sent back" and consecutive send-backs < send-back run length |
| entered | reassessing the send-backs | none | entry reason = "sent back" and consecutive send-backs >= send-back run length |
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
| settling | reassessing | none | not(review ended by approval?) and (consecutive design flaw rounds >= design flaw run length or consecutive implementation flaw rounds >= implementation flaw run length) |
| settling | changing | none | review ended by approval? or (consecutive design flaw rounds < design flaw run length and consecutive implementation flaw rounds < implementation flaw run length) |
| reassessing | framing | the user decides the reassessment | reassessment != "go on" |
| reassessing | changing | the user decides the reassessment | reassessment = "go on" |
| reassessing | changing | the user approves the plan | none |
| changing | framing | none | needs reframing? |
| changing | validating | none | not(needs reframing?) |
| waiting | validating | when depends on ready? | none |
| waiting | changing | the user gives a steer | none |
| waiting | changing | a design its Depends On Designs names finishes | none |
| validating | reviewing | none | needs review? and not(review ended by approval?) |
| validating | awaiting approval | none | (not(needs review?) or review ended by approval?) and depends on ready? and not(plan approved?) |
| validating | approved by the user | none | (not(needs review?) or review ended by approval?) and depends on ready? and plan approved? |
| validating | waiting | none | (not(needs review?) or review ended by approval?) and not(depends on ready?) |
| validating | changing | the validation review reports a problem | fix changes the plan? |
| validating | waiting | [`specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files.md#the-states-it-moves-through) of a design its Depends On Designs names is entered | not(needs review?) or review ended by approval? |
| validating | changing | the user gives a steer | none |
| validating | changing | a design its Depends On Designs names finishes | none |
| awaiting approval | approved by the user | the user approves the plan | depends on ready? |
| awaiting approval | changing | the user does not approve the plan | none |
| awaiting approval | drafting | the user asks for another round | none |
| awaiting approval | waiting | [`specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files.md#the-states-it-moves-through) of a design its Depends On Designs names is entered | none |
| awaiting approval | changing | a design its Depends On Designs names finishes | none |

**Table Name:** Trigger Classes

| Member | Class |
|---|---|
| [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) | a design its Depends On Designs names finishes |

### The Apply

A design's apply begins only as [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) lets a design enter applying, and it ends applied or sent back. The order the apply takes:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| writing | the builder writes each step's text or code with each file open, within the Target, from the files as they stand, the changes a send-back kept among them ([`specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files.md#a-send-back)), keeps or removes each uncommitted change as [`specs/methodology/working-files.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files.md#uncommitted-changes) has it at the writing, takes in each edit the user makes as [`specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`](/specs/methodology/working-files.md#telling-a-steer-apart) has it, takes in the user's feedback on the applied result, then makes its self-review of what it wrote, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles) has it, appending its entry through `--append-entry`, which checks each report by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks), and starts the post-apply review, a cold agent's on the model and reasoning effort the user chose for the design | Yes | No |
| post-apply reviewing | a cold agent runs the post-apply review, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles) has it | No | No |
| settling the post-apply round | The builder first checks the review's report by the design script's `--check-report`, by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), handing a report out of its form back as [`specs/methodology/working-files.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files.md#who-writes-each-part) has it. The builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it, and the user triages a finding lying in the plan. The builder makes the round's tactical fixes and sets plan finding? and writing flaw? by what the round found. Its settling ends as it appends the round's entry through `--append-entry`, which checks the report by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks) | No | No |
| user reviewing | the builder shows the user the applied result with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and the post-apply review's entry and report, and waits on the user | No | No |
| auditing | an audit runs, made as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it | No | No |
| settling the audit | the builder reads and triages the audit's findings as [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) has an audit read, each settled as [`specs/methodology/working-files.md § A Design Document § Changes After Approval`](/specs/methodology/working-files.md#changes-after-approval) has it, and the builder sets plan finding? and audit rework?; its settling ends as it appends the audit's entry through `--append-entry`, which checks its triage by [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files.md#script-checks-1), [`specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files.md#script-checks) | No | No |
| reassessing the apply | the builder and the user step back and reassess, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a phase not converging | No | No |
| awaiting the commit | the builder shows the user the settled audit with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and the commit for the design's changes, and waits for the go-ahead | No | No |
| committing | the builder commits the design's changes on their own, one commit for the design ([`specs/methodology/working-files.md § A Design Document § Applying and Committing`](/specs/methodology/working-files.md#applying-and-committing)) | No | No |
| applied | the text or code its steps call for is written, its post-apply review converged, the user's review given, its audit settled, and its changes committed where the project has version control | No | Yes |
| sent back | a finding lying in the plan, a steer, a reassessment of the apply, or its builder's finding that the plan cannot be delivered, triaged by the user as lying in the plan, sends the design back to in-progress, with the changes [`specs/methodology/working-files.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files.md#uncommitted-changes) keeps at a send-back in place, as [`specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files.md#a-send-back) has it | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| writing | post-apply reviewing | none | none |
| writing | sent back | the user triages the builder's finding that the plan cannot be delivered as its steps and Target state it as lying in the plan | none |
| post-apply reviewing | settling the post-apply round | none | none |
| settling the post-apply round | sent back | none | plan finding? |
| settling the post-apply round | reassessing the apply | none | not(plan finding?) and writing flaw? and consecutive post-apply flaw rounds >= post-apply flaw run length |
| settling the post-apply round | writing | none | not(plan finding?) and writing flaw? and consecutive post-apply flaw rounds < post-apply flaw run length |
| settling the post-apply round | user reviewing | none | not(plan finding?) and not(writing flaw?) |
| user reviewing | auditing | the user approves the applied result | none |
| user reviewing | post-apply reviewing | the user asks for another round | none |
| auditing | settling the audit | none | none |
| settling the audit | sent back | none | plan finding? |
| settling the audit | reassessing the apply | none | not(plan finding?) and audit rework? and consecutive rework audits >= rework audit run length |
| settling the audit | writing | none | not(plan finding?) and audit rework? and consecutive rework audits < rework audit run length |
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
    **Means:** why the design last entered in-progress, the move its Status took: taken up, reopened by the user, a design its Depends On Designs names moving back to in-progress, one finishing, or its apply sending it back

  - **Name:** consecutive design flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's phase, this one among them, that the run of design flaws counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero by a round finding none, by a reassessment of the design's adversarial rounds, whatever it decides, and as a send-back or a reassessment of the send-backs takes the design to framing

  - **Name:** consecutive implementation flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's phase, this one among them, that the run of implementation flaws counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero by a round finding none, by a reassessment of the design's adversarial rounds, whatever it decides, and as a send-back or a reassessment of the send-backs takes the design to framing

  - **Name:** consecutive send-backs \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the applies of the design in a row, this one among them, that the run of send-backs counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero as an apply reaches awaiting the commit or applied; set back to zero too by a reassessment of the send-backs, whatever it decides, and by a reassessment of the apply that decides other than `go on`. The apply such a reassessment sends back is not counted

  - **Name:** consecutive post-apply flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the post-apply rounds in a row of the apply, this one among them, that the run of post-apply flaws counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero by a round finding none, by a reassessment of the apply, whatever it decides, and as an apply begins

  - **Name:** consecutive rework audits \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the audits in a row of the apply, this one among them, that the run of rework audits counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero by an audit sending none, by a reassessment of the apply, whatever it decides, and as an apply begins

  - **Name:** design flaw run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of design flaws, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** implementation flaw run length \
    **Type:** number \
    **Initial Value:** 5 \
    **Means:** the length of the run of implementation flaws, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** post-apply flaw run length \
    **Type:** number \
    **Initial Value:** 5 \
    **Means:** the length of the run of post-apply flaws, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** rework audit run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of rework audits, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** send-back run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of send-backs, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** reassessment \
    **Type:** string \
    **Values:** "rescope", "split", "a different approach", "go on" \
    **Means:** what the user decided at a reassessment, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has one; a design abandoned leaves by [`specs/methodology/working-files.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files.md#the-states-it-moves-through) instead

  - **Name:** needs review? \
    **Type:** boolean \
    **Means:** whether the design takes another adversarial round before the user's approval: the last round it settled is one [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) has another round follow, or its goals or its frame have moved since that round began (a change to the goals or the frame taking a fresh review, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has it), or it has settled none since it was last framed, or the user asked for another round

  - **Name:** needs reframing? \
    **Type:** boolean \
    **Means:** whether a steer the design took in changed its goals or its frame and the user has not yet approved the change, so they go back to the user for approval, the design rebuilt from the change ([`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame))

  - **Name:** review ended by approval? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given before its adversarial review ended, ended it ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). The approval sets it in any state of the design's work. Only a reassessment's transitions fire on it, and each state finishes its own work first. It is set back to false only where the design is sent back, a reassessment decides other than `go on`, or the user asks for another round. So a change after the approval keeps it, a reopen or a dependency's move among them, even one changing the goals or the frame

  - **Name:** plan approved? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given in any state of its work, covers the plan as it stands ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). It is set back to false by a change after the approval to the design's goals, its frame or its steps, and by the design's entering in-progress again

  - **Name:** fix changes the plan? \
    **Type:** boolean \
    **Means:** whether fixing a problem the validation review reports changes the design's goals, its frame or a step, and not only the record around them

  - **Name:** depends on ready? \
    **Type:** boolean \
    **Means:** whether each design its Depends On Designs names is approved or applying

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

A design's Kind sizes its reviews and its audit. The effort they take grows with what a flaw in the design would cost. A design whose Target names files of more than one Kind takes the highest effort among them. The kinds of the files its Target names pick its audit, each file's kind as [`specs/methodology/working-files.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files.md#the-kinds-of-change) defines it. Where they include `code`, the audit is `.ai/skills/verify-spec-implementation/`'s full run. Where they include any other kind, it is an `.ai/skills/audit-specs/` run given those kinds as the skill's `--kind`. A design whose Target names both runs both. A run of `.ai/skills/audit-specs/` given kinds, `canon-specs` not among them, covers the files of those kinds. A run given `canon-specs` covers every kind but `code` and `none`, since a change to the canon can leave any such file in breach of it, the application specs among them. A run the user starts with no kind is the full run, covering every kind of the skill's scope, `none` among them, and not `code`, which is `.ai/skills/verify-spec-implementation/`'s. No audit reads a design: the `none` a run covers is the working files an audit's unit names, never a design document. Of the semantic checks whose Carried Out By names `.ai/skills/audit-specs/`, a run reads each whose Reads holds a kind of file it covers, a check another skill carries out being that skill's to run. It reads each reading audit whose Kind names a kind it covers. Each Kind gives the effort this table names, which [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has a review run at:

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

Every adversarial review and every post-apply review the standard process runs is started with this brief alone, the same in every round, so the design is the one thing that changes between rounds. The brief holds no part of a review's task. The review's section, [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) or [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review), holds the whole of it, the section its record in [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles`](/specs/AGENTS.md#check-roles) cites as its Work. The builder fills the brief's blanks as it starts a round, and adds nothing about the design or the rounds before it. What a finding means and where it goes stay the builder's to settle. The brief sits in a fenced block, so no link is written into it and it stays this text:

```text
You are the {adversarial | post-apply} reviewer of a Spec of Record design. You are cold: you did not build or apply it, and you change nothing but your report.

Design: {design document}
Report: {report file}

1. Read specs/AGENTS.md, then specs/methodology/glossary.md, then the design document whole.
2. Do the {adversarial | post-apply} review as specs/AGENTS.md § Design, Refactor, Refine § {The Adversarial Review | The Post-Apply Review} sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the {adversarial | post-apply} review] has it.
3. Write the report in the form specs/methodology/working-files.md § A Check's Report gives a review's report.
```

An audit takes no brief. Whoever starts one, the user or the builder in a design's apply, starts it as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it made.

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
