## The Order of a Design's Work

Two State Machines set the order a design's work takes, and what moves it back. The design's Status runs them ([`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files/main.md#the-states-it-moves-through)). [`§ The Order of a Design's Work § The Work of a Design`](#the-work-of-a-design) governs the in-progress state, and [`§ The Order of a Design's Work § The Apply`](#the-apply) governs the applying state. Each state's work is done as the section it cites has it, so the machines hold the order alone. A state running a check of a design names it as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has a check named where it runs. The principles stay in [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine). A design changing code takes the same order ([`specs/methodology/working-files/main.md § A Design Document § A Design Changing Code`](/specs/methodology/working-files/main.md#a-design-changing-code)).

### The Work of a Design

A design enters its work by the reason its Status entered in-progress. Its change leads back to another adversarial review wherever needs review? or needs reframing? holds and the user's approval has not ended its review ([`§ The Order of a Design's Work § Facts`](#facts)). A design its Depends On Designs names finishing is a class of occurrences. This machine's Trigger Classes table cites the section that lists its members.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| entered | the design has entered in-progress, by its Status's move | Yes | No |
| framing | the builder agrees on the design goals with the user and states the design frame, or revisits either, and brings them to the user, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has the goals, then the frame, come first, appending the `goals-agreed` entry as the user agrees the goals, taking in each set of steers that closes and each finished design its Scope relies on ([`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise)) | No | No |
| drafting | the builder takes the design's steps through the Design, Refactor, Refine process ([`specs/AGENTS.md § Design, Refactor, Refine § Design`](/specs/AGENTS.md#design), [`specs/AGENTS.md § Design, Refactor, Refine § Refactor`](/specs/AGENTS.md#refactor), [`specs/AGENTS.md § Design, Refactor, Refine § Refine`](/specs/AGENTS.md#refine)), recording each steer as it is given ([`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)) and taking in each finished design its Scope relies on ([`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise)), then makes its self-review, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles) has it, appending its Design, Refactor, Refine pass's entry and its self-review's through `--log-entry`, which checks each report by [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks), and offers the user the review's model and reasoning effort when [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has them chosen | No | No |
| reviewing | a cold agent runs the adversarial review, as [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) has it | No | No |
| settling | The builder first takes the review's report up by the design script's `--take-up-report`, which runs the checks of `--check-handed-back`, [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1) and [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`](/specs/methodology/working-files/main.md#script-checks-1), as [`specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files/main.md#who-writes-each-part) has a report taken up. The builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it: the user triages its design flaws and answers its other calls, and the builder settles the rest. The builder takes in each set of steers that closes and each finished design its Scope relies on, one finishing while the design was reviewed among them. Where the plan's approval, or a set of steers changing the goals or the frame that closed while the round ran or was settled, has ended the round, the builder settles it as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes`](/specs/AGENTS.md#the-round-at-its-causes) has a round so ended settled. A set changing less joins the round's settling. Its settling ends as it checks the settled report by the design script's `--check-settled-report` and appends the round's entry through `--log-entry`, which runs the same checks: [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks) | No | No |
| reassessing | the builder and the user step back and reassess, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a run not converging or the user's word reach a reassessment, each check then running stopped, cut short or continued as that section has it, a round continued there settled as it hands back, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has a round settled, its entry appended as its settling ends, taking in each finished design its Scope relies on | No | No |
| reassessing the send-backs | the builder and the user step back and reassess a run of the design's applies sent back, or a design approved or applying sent back to reassess on the user's word, its passes that did not converge among them, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a run not converging, taking in each finished design its Scope relies on | No | No |
| changing | the builder revises the design, as the round was settled, taking in each set of steers that closes and each finished design its Scope relies on ([`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise)), makes the change in the top-down order [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) gives a change, takes each step the change moved through the Design, Refactor, Refine process, then makes its self-review, appending its Design, Refactor, Refine pass's entry and its self-review's through `--log-entry`, which checks each report by [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks), proving the change, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove`](/specs/AGENTS.md#change-and-prove) has it | No | No |
| waiting | the design waits for each design its Depends On Designs names to be approved or applying, as [`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise) has a design go to the user's approval only then | No | No |
| validating | the builder runs `--check-workstack` and puts right what it reports, and the validation review checks the design document's structure, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles) has it, the builder fixing what it reports and running it again until it passes, the review stamping the design on its way to the user's approval ([`specs/methodology/working-files/main.md § A Design Document § The Record's Checks`](/specs/methodology/working-files/main.md#the-records-checks)) | No | No |
| awaiting approval | the user is asked to approve the plan, shown it as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval | No | No |
| approved by the user | the user approved the plan | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| entered | framing | none | entry reason = "taken up" |
| entered | framing | none | entry reason = "sent back" and consecutive send-backs < send-back run length |
| entered | reassessing the send-backs | none | entry reason = "sent back" and consecutive send-backs >= send-back run length |
| entered | reassessing the send-backs | none | entry reason = "sent back to reassess" |
| entered | changing | none | entry reason = "reopened" |
| entered | changing | none | entry reason = "a dependency finished" |
| entered | waiting | none | entry reason = "a dependency moved back" |
| reassessing the send-backs | framing | the user decides the reassessment | reassessment != "go on" or entry reason = "sent back" |
| reassessing the send-backs | approved by the user | the user decides the reassessment | reassessment = "go on" and entry reason = "sent back to reassess" |
| reassessing the send-backs | changing | the user approves the plan | none |
| framing | drafting | the user agrees on the goals and agrees to or adjusts the frame | none |
| drafting | framing | a set of steers closes | needs reframing? |
| drafting | validating | none | none |
| reviewing | settling | none | none |
| reviewing | changing | a set of steers closes | check stopped? |
| settling | reassessing | none | not(review ended by approval?) and (consecutive design flaw rounds >= design flaw run length or consecutive implementation flaw rounds >= implementation flaw run length) |
| settling | changing | none | review ended by approval? or (consecutive design flaw rounds < design flaw run length and consecutive implementation flaw rounds < implementation flaw run length) |
| framing | reassessing | the user asks for a reassessment | none |
| drafting | reassessing | the user asks for a reassessment | none |
| reviewing | reassessing | the user asks for a reassessment | none |
| settling | reassessing | the user asks for a reassessment | none |
| changing | reassessing | the user asks for a reassessment | none |
| waiting | reassessing | the user asks for a reassessment | none |
| validating | reassessing | the user asks for a reassessment | none |
| awaiting approval | reassessing | the user asks for a reassessment | none |
| reassessing | framing | the user decides the reassessment | reassessment != "go on" or not(frame agreed?) |
| reassessing | changing | the user decides the reassessment | reassessment = "go on" and frame agreed? |
| reassessing | changing | the user approves the plan | none |
| changing | framing | none | needs reframing? |
| changing | validating | none | not(needs reframing?) |
| waiting | validating | when depends on ready? | none |
| waiting | changing | a set of steers closes | none |
| waiting | changing | a design its Depends On Designs names finishes | none |
| validating | reviewing | none | needs review? and not(review ended by approval?) |
| validating | awaiting approval | none | (not(needs review?) or review ended by approval?) and depends on ready? and not(plan approved?) |
| validating | approved by the user | none | (not(needs review?) or review ended by approval?) and depends on ready? and plan approved? |
| validating | waiting | none | (not(needs review?) or review ended by approval?) and not(depends on ready?) |
| validating | changing | the validation review reports a problem | fix changes the plan? |
| validating | waiting | [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files/main.md#the-states-it-moves-through) of a design its Depends On Designs names is entered | not(needs review?) or review ended by approval? |
| validating | changing | a set of steers closes | none |
| validating | changing | a design its Depends On Designs names finishes | none |
| awaiting approval | approved by the user | the user approves the plan | depends on ready? |
| awaiting approval | changing | the user does not approve the plan | none |
| awaiting approval | drafting | the user asks for another round | none |
| awaiting approval | waiting | [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through [States.State: in-progress]`](/specs/methodology/working-files/main.md#the-states-it-moves-through) of a design its Depends On Designs names is entered | none |
| awaiting approval | changing | a design its Depends On Designs names finishes | none |

**Table Name:** Trigger Classes

| Member | Class |
|---|---|
| [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files/main.md#the-states-it-moves-through) | a design its Depends On Designs names finishes |

### The Apply

A design's apply begins only as [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files/main.md#the-states-it-moves-through) lets a design enter applying, and it ends applied or sent back. This machine orders what a check after the writing runs through: its run to its end, its settling, the fixes it calls for and the passes proving them, and the routing of the work, on or back. The order the apply takes:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| writing | the builder writes each step's text or code with each file open, within the Target, from the files as they stand, the changes a send-back kept among them ([`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back)), keeps or removes each uncommitted change as [`specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files/main.md#uncommitted-changes) has it at the writing, takes in each edit the user makes as [`specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart`](/specs/methodology/working-files/main.md#telling-a-steer-apart) has it, takes in the user's feedback on the applied result given while it writes, then makes its self-review of what it wrote, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles) has it, appending its entry through `--log-entry`, which checks each report by [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks), and starts the post-apply review, a cold agent's on the model and reasoning effort the user chose for the design | Yes | No |
| post-apply reviewing | a cold agent runs the post-apply review, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles) has it | No | No |
| settling the post-apply round | The builder first takes the review's report up by the design script's `--take-up-report`, which runs the checks of `--check-handed-back`, [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1) and [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`](/specs/methodology/working-files/main.md#script-checks-1), as [`specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files/main.md#who-writes-each-part) has a report taken up. The builder settles the round, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round) has it, its report settling each finding, and the user triages a finding lying in the plan. It sets plan finding? by what the round found, and sets next state to "user reviewing". The round's fixes follow, in proving the fixes. Its settling ends as it checks the settled report by the design script's `--check-settled-report` and appends the round's entry through `--log-entry`, which runs the same checks: [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks) | No | No |
| proving the fixes | the builder makes the fixes the check's settling calls for, each keeping what the plan decides, the nits [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit`](/specs/AGENTS.md#a-nit) has fixed among them, and each fix the user's feedback asks for, the held feedback among it. It makes each in place, as [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval § A Tactical Fix After the Apply`](/specs/methodology/working-files/main.md#a-tactical-fix-after-the-apply) has a tactical fix made, except a fix [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back) leaves to the rework once plan finding? or set closed? sends the design back. It places the feedback it takes in as a check's finding is placed, a steer among it, told apart as [`specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart`](/specs/methodology/working-files/main.md#telling-a-steer-apart) tells one, setting set closed? as the steer's set closes. It brings the user each finding of a pass whose fix [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Whose Fix It Is`](/specs/AGENTS.md#whose-fix-it-is) gives the user, and settles one whose fix would change the plan as [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval`](/specs/methodology/working-files/main.md#changes-after-approval) settles a self-review's finding. One lying in the plan sets plan finding?, its fix left to the send-back. It proves the fixes by passes of its self-review, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) has a pass made, appending each pass's entry through `--log-entry`, which checks each pass's report by [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks), and sets pass converged? and passes without converging | No | No |
| choosing after the passes | the builder brings the user the passes that did not converge, each finding they left unresolved, and its recommendation with the reason for it, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) has a call brought. The user chooses to keep revising, to reassess the design, or to accept the last pass's fixes as good enough, a reassessment being one on the user's word, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it reached. Feedback the user gives there is taken in at proving the fixes, as keeping on is. The builder appends a `passes-choice` entry for keeping on, or for feedback given there, or for accepting | No | No |
| routing | the passes have ended, and the work goes on or goes back by what the check settled and what the user gave while it ran | No | No |
| user reviewing | the builder shows the user the applied result with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and the post-apply review's entry and report, and waits on the user | No | No |
| auditing | an audit runs, made as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it | No | No |
| settling the audit | the builder reads and triages the audit's findings as [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) has an audit read, each settled in its triage as [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval`](/specs/methodology/working-files/main.md#changes-after-approval) has it, and sets plan finding?, and sets next state to "awaiting the commit". The audit's fixes follow, in proving the fixes. Its settling ends as it checks its triage by the design script's `--check-settled-report` and appends the audit's entry through `--log-entry`, which runs the same checks: [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]`](/specs/methodology/working-files/main.md#script-checks-1), [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]`](/specs/methodology/working-files/main.md#script-checks) | No | No |
| awaiting the commit | the builder shows the user the settled audit with its summary, as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has the user shown each approval, and, where the project has version control, the commit for the design's changes. It offers another audit or the commit, with its recommendation and the reason for it, and waits for the user's choice | No | No |
| committing | the builder commits the design's changes on their own, one commit for the design ([`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing)) | No | No |
| applied | the text or code its steps call for is written, its post-apply review settled, the user's review given, its audit settled, and its changes committed where the project has version control | No | Yes |
| sent back | a finding lying in the plan, a set of steers, or its builder's finding that the plan cannot be delivered, triaged by the user as lying in the plan, sends the design back to in-progress, carrying what [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back) has a send-back carry, with the changes [`specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files/main.md#uncommitted-changes) keeps at a send-back in place | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| writing | post-apply reviewing | none | none |
| writing | sent back | the user triages the builder's finding that the plan cannot be delivered as its steps and Target state it as lying in the plan | none |
| writing | sent back | a set of steers closes | none |
| post-apply reviewing | settling the post-apply round | none | none |
| post-apply reviewing | sent back | a set of steers closes | check stopped? |
| settling the post-apply round | proving the fixes | none | none |
| auditing | settling the audit | none | none |
| auditing | sent back | a set of steers closes | check stopped? |
| settling the audit | proving the fixes | none | none |
| proving the fixes | proving the fixes | none | not(pass converged?) and passes without converging < pass run length |
| proving the fixes | choosing after the passes | none | not(pass converged?) and passes without converging >= pass run length |
| proving the fixes | routing | none | pass converged? |
| choosing after the passes | proving the fixes | the user chooses to keep revising | none |
| choosing after the passes | proving the fixes | the user gives feedback on the applied result | none |
| choosing after the passes | routing | the user accepts the last pass's fixes as good enough | none |
| choosing after the passes | sent back | a set of steers closes | none |
| routing | proving the fixes | none | count(held feedback) > 0 |
| routing | sent back | none | count(held feedback) = 0 and (plan finding? or set closed?) |
| routing | user reviewing | none | count(held feedback) = 0 and not(plan finding?) and not(set closed?) and next state = "user reviewing" |
| routing | awaiting the commit | none | count(held feedback) = 0 and not(plan finding?) and not(set closed?) and next state = "awaiting the commit" |
| user reviewing | auditing | the user approves the applied result | none |
| user reviewing | post-apply reviewing | the user asks for another round | none |
| user reviewing | proving the fixes | the user gives feedback on the applied result | none |
| user reviewing | sent back | a set of steers closes | none |
| awaiting the commit | auditing | the user chooses another audit | none |
| awaiting the commit | committing | the user approves the settled audit | version control? |
| awaiting the commit | applied | the user approves the settled audit | not(version control?) |
| awaiting the commit | proving the fixes | the user gives feedback on the applied result | none |
| awaiting the commit | sent back | a set of steers closes | none |
| committing | applied | none | none |

### Facts

**Records:**
  - **Name:** entry reason \
    **Type:** string \
    **Values:** "taken up", "reopened", "a dependency moved back", "a dependency finished", "sent back", "sent back to reassess" \
    **Means:** why the design last entered in-progress, the move its Status took: taken up, reopened by the user, a design its Depends On Designs names moving back to in-progress, one finishing, its apply sending it back, or the user's word to reassess it while approved or applying, the user's choice to reassess after passes that did not converge among it; set as the design enters in-progress, by the move bringing it there, the user's word to reassess setting "sent back to reassess", and every other send-back "sent back"

  - **Name:** consecutive design flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's current major version, this one among them, whatever ended them, that the run of design flaws counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; a round stopped before it handed anything back leaves it as it stood; set back to zero by a round finding none and by a reassessment of the design's adversarial rounds, whatever it decides, and carried across a send-back

  - **Name:** consecutive implementation flaw rounds \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the adversarial rounds in a row of the design's current major version, this one among them, whatever ended them, that the run of implementation flaws counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; a round stopped before it handed anything back leaves it as it stood; set back to zero by a round finding none and by a reassessment of the design's adversarial rounds, whatever it decides, and carried across a send-back

  - **Name:** consecutive send-backs \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the applies of the design in a row, this one among them, that the run of send-backs counts, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it counted; set back to zero as an apply reaches awaiting the commit or applied; set back to zero too by a reassessment of the send-backs, whatever it decides

  - **Name:** design flaw run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of design flaws, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** implementation flaw run length \
    **Type:** number \
    **Initial Value:** 5 \
    **Means:** the length of the run of implementation flaws, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** send-back run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of send-backs, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the builder stop and reassess. No state's work, effect or occurrence sets it

  - **Name:** reassessment \
    **Type:** string \
    **Values:** "rescope", "split", "a different approach", "go on" \
    **Means:** what the user decided at a reassessment, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has one; a design abandoned leaves by [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through`](/specs/methodology/working-files/main.md#the-states-it-moves-through) instead

  - **Name:** needs review? \
    **Type:** boolean \
    **Means:** whether the design takes another adversarial round before the user's approval: the last round it settled is one [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) has another round follow, or its goals or its frame have moved since that round began (a change to the goals or the frame taking a fresh review, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has it), or it has settled none since it was last framed, or the user asked for another round

  - **Name:** needs reframing? \
    **Type:** boolean \
    **Means:** whether a set of steers the design took in changed its goals or its frame and the user has not yet approved the change, so they go back to the user for approval, the design rebuilt from the change ([`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame))

  - **Name:** frame agreed? \
    **Type:** boolean \
    **Means:** whether the user has agreed on the goals and agreed to or adjusted the frame since the design last entered framing, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has them come first, so a reassessment going on resumes at framing a design whose goals and frame are not yet agreed

  - **Name:** review ended by approval? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given before its adversarial review ended, ended it ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). The approval sets it in any state of the design's work. Only a reassessment's transitions fire on it, and each state finishes its own work first. It is set back to false only where the design is sent back, a reassessment decides other than `go on`, or the user asks for another round. So a change after the approval keeps it, a reopen or a dependency's move among them, even one changing the goals or the frame

  - **Name:** plan approved? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the user's approval of the plan, given in any state of its work, covers the plan as it stands ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval)). It is set back to false by a change after the approval to the design's goals, its frame or its steps, and by the design's entering in-progress again

  - **Name:** check stopped? \
    **Type:** boolean \
    **Means:** whether the user's call at a set of steers' close stopped the review or the audit then running, before it handed anything back, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) has work stopped; set as the call is made

  - **Name:** fix changes the plan? \
    **Type:** boolean \
    **Means:** whether fixing a problem the validation review reports changes the design's goals, its frame or a step, and not only the record around them

  - **Name:** depends on ready? \
    **Type:** boolean \
    **Means:** whether each design its Depends On Designs names is approved or applying

  - **Name:** plan finding? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether the post-apply round or the audit last settled holds a finding lying in the plan, as [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval`](/specs/methodology/working-files/main.md#changes-after-approval) has one, or a pass proving the fixes has found one lying there; set by the settling states and by proving the fixes, and set back as the work leaves routing for any state but proving the fixes

  - **Name:** version control? \
    **Type:** boolean \
    **Means:** whether the project keeps its files under version control

  - **Name:** held feedback \
    **Type:** list<string> \
    **Initial Value:** [] \
    **Means:** the user's feedback on the applied result, each piece in the user's words, given while post-apply reviewing, settling the post-apply round, auditing, settling the audit or proving the fixes, held so no check is cut short for it ([`specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means`](/specs/methodology/modeling-constructs.md#what-it-means-1) records a deferred event as a fact); a piece added as the user gives it in those states, and the list emptied as proving the fixes takes it in and as the design is sent back

  - **Name:** set closed? \
    **Type:** boolean \
    **Initial Value:** false \
    **Means:** whether a set of steers has closed while post-apply reviewing, settling the post-apply round, auditing, settling the audit or proving the fixes, the work then running continued on the user's call, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) has a set closed and its running work continued, so no check is cut short unasked; set as the set closes in those states, or as proving the fixes places held feedback that changes the plan, and set back as the design is sent back

  - **Name:** next state \
    **Type:** string \
    **Values:** "user reviewing", "awaiting the commit" \
    **Means:** the state routing moves the work to where nothing sends it back: set to user reviewing by settling the post-apply round and by user reviewing as the user's feedback leaves it, and to awaiting the commit by settling the audit and by awaiting the commit as the user's feedback leaves it

  - **Name:** pass converged? \
    **Type:** boolean \
    **Means:** whether the last pass of the builder's self-review over the fixes found no flaw and no harmful nit, a flaw the user triaged as lying in the plan aside, or no fix stood to prove; set by each pass of proving the fixes. A pass finding only harmless nits converges, its nits settled as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit`](/specs/AGENTS.md#a-nit) settles a check's nits

  - **Name:** passes without converging \
    **Type:** number \
    **Initial Value:** 0 \
    **Means:** the passes in a row over a check's fixes, this one among them, that each found a flaw or a harmful nit, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the run of passes counted, read from the `self-review` entries after the check's entry or after the last `passes-choice` entry whose Choice is keep revising or feedback; set back to zero as proving the fixes is entered from any state but itself, the choice after the passes among them

  - **Name:** pass run length \
    **Type:** number \
    **Initial Value:** 3 \
    **Means:** the length of the run of passes, at which [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the user choose how the work goes on. No state's work, effect or occurrence sets it

## A Design's Reviews

A design's Kind sizes its reviews and its audit. The effort they take grows with what a flaw in the design would cost. A design whose Target names files or directories of more than one Kind takes the highest effort among them. The kinds of the files and directories its Target names pick its audit, each one's kind as [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) defines it. Where they include `code`, the audit is `.ai/skills/verify-spec-implementation/`'s full run. Where they include any other kind, it is an `.ai/skills/audit-specs/` run given those kinds as the skill's `--kind`. A design whose Target names both runs both. A run of `.ai/skills/audit-specs/` given kinds, `canon-specs` not among them, covers the files of those kinds. A run given `canon-specs` covers every kind but `code` and `none`, since a change to the canon can leave any such file in breach of it, the application specs among them. A run the user starts with no kind is the full run, covering every kind of the skill's scope, `none` among them, and not `code`, which is `.ai/skills/verify-spec-implementation/`'s. No audit reads a design: the `none` a run covers is the working files an audit's unit names, never a design document. Of the semantic checks whose Carried Out By names `.ai/skills/audit-specs/`, a run reads each whose Reads holds a kind of file it covers, a check another skill carries out being that skill's to run. It reads each reading audit whose Kind names a kind it covers. Each Kind gives the effort this table names, which [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has a review run at:

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
3. Write the report from specs/methodology/working-files/check-report/review-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the reviewer, and check them as that section has them checked before handing the report back.
```

An audit takes no brief. Whoever starts one, the user or the builder in a design's apply, starts it as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it made.

## A Research Brief

All research a design hands off starts with this brief, each cold agent of a share given it with its own share, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research shared. Like the review's brief, it holds no part of the research's task, which that section holds, and no part of its report's form, which the research report's form template holds. The builder fills its blanks from the design and adds nothing else. Its reading step is the review's brief's. The brief sits in a fenced block, so no link is written into it:

```text
You are a cold agent doing research for a Spec of Record design. You are cold: you did not build the design, and you change nothing but your report.

Design: {design document}
Report: {report file}
Entry: {the entry the research's check is logged as}
Cause: {the research's cause, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research and specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out name it, by the entry, report or key recording it}
Places to read: {each place the builder knows to read, one to a line}
Share: {each place of your share, one to a line; or none, where the research is not shared}
Searches: {each Search, its key, what it is for, the goals it serves and its pattern, one to a line}

1. Read specs/AGENTS.md, then specs/methodology/glossary.md, then the design document whole.
2. Do the research as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: a judgment the builder hands off] has it.
3. Write the report from specs/methodology/working-files/check-report/research-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the cold agent, and check them as that section has them checked before handing the report back.
```

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
