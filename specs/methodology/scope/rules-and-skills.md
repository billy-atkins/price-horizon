## Rules and Skills

The methodology's files state Spec of Record's methodology rules. They do not sequence the work, record what goes wrong while following it, check whether a result conforms, or teach the craft a rule assumes. The skills that [`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills) registers do those things, and a cold agent needs them to follow the methodology in practice. [`specs/AGENTS.md`](/specs/AGENTS.md) states methodology rules too, and sequences the work through the Design, Refactor, Refine process. The methodology's files and [`specs/AGENTS.md`](/specs/AGENTS.md), with the specifications' main file and their overview, make up the core canon ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)). The skills, with the code they share, are the rest of the canon. Where a skill and a methodology rule disagree, the methodology rule governs, and the skill is what needs correcting.

**Where a rule lives.** What a rule governs decides where it lives, never where it stands today. The questions mean these:
- **A specification rule?** Whether the rule governs what the specifications or the code hold, rather than how the work is done, which an operating rule governs.
- **More than one skill needs it?** Whether more than one skill applies the rule. A working file's form is needed by each skill that reads or writes the file.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** A specification rule?, More than one skill needs it?

| A specification rule? | More than one skill needs it? | Lives In |
|---|---|---|
| true | - | the core canon, and never in a skill |
| false | true | the core canon, above the skills |
| false | false | that skill |

A skill keeps a rule in the form [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill) gives a rule it keeps, naming beside it the check the skill makes of it.

A rule without a check is a suggestion, so every rule of Spec of Record is enforced. A rule added or changed takes its check with it, in the same change. A check of the files or the code is run where [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over`](/specs/AGENTS.md#the-scope-a-check-runs-over) runs it, over the work as well as over the audit's units. [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose), as it reaches the working files, stands without a check. The user holds the working files to it in reading them, since an audit of files that never last would cost more than it finds. [`specs/methodology/spec-style/markdown.md § Blank Lines`](/specs/methodology/spec-style/markdown.md#blank-lines), and the layout [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) gives a block of fields, stand without a check where they reach the skills' own output that no design's log entry names, or a plan no validation reads: a design once it is complete or abandoned, and any plan other than a design document. Each such file is read by the work it was written for, so an audit of them would cost more than it finds. A check's report a design's log entry names is held to them, since the skill writing the design reads its records by that layout and checks it as it appends the check's entry ([`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]`](/specs/methodology/working-files/main.md#script-checks-1)).

**A specification rule.** It is checked against the files it governs by one of the audit skill's reading audits. A rule of [`specs/methodology/code.md`](/specs/methodology/code.md) is checked instead by a check of `.ai/skills/verify-spec-implementation/` that reads the code. Either skill's script first decides whatever the files alone settle. The script never decides a judgment, since a check that cannot decide gives a confident false clear. A script that lists places for a reading audit to look decides nothing.

**An operating rule in the core canon.** It is checked where it leaves a trace in the files the audits read: the scope's tree ([`specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope`](/specs/methodology/scope/what-spec-of-record-governs.md#the-shape-of-the-scope)), the skills registry ([`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills)), a skill's form ([`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill)), a follow-up. A plan's form leaves its trace outside those files. The skill that writes the plan checks the plan's form, through the skill's script and steps. A rule whose step records its result in a check's report leaves its trace in that report ([`specs/methodology/working-files/main.md § A Check's Report`](/specs/methodology/working-files/main.md#a-checks-report)). The skill writing the design checks it there through its script as it appends the check's entry, as it checks a plan's form through its script. Where a rule leaves no trace, as reading fresh leaves none, since no record shows when a place was read, the rule is carried out as a named step of [`specs/AGENTS.md`](/specs/AGENTS.md) or of a registered skill. A skipped step is found by what it leaves wrong in the files.

**Which check enforces each section.** Every section of [`specs/AGENTS.md`](/specs/AGENTS.md), of the main file of `specs/` and of the methodology's files is covered, except the methodology's `architecture.md` and `index.md`, its worked examples under `examples/`, each form template, told by its name ([`specs/methodology/scope/form-templates.md § Form Templates`](/specs/methodology/scope/form-templates.md#form-templates)), and each record section of `Script Checks` or `Semantic Checks`, which hold no rule of their own. A section is covered where a reading audit of `.ai/skills/audit-specs/` names it as one the audit enforces, or where a Skipped Step's Sections names it as one stating operating rules ([`§ Rules and Skills § Skipped Steps`](#skipped-steps)). A check's record standing directly under a section names that section too ([`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check)). It names no section below that one. A core-canon operating rule's check is a step under a registered skill's `## Workflow` that applies the rule. That step gives the rule a point-of-use citation. For a section of [`specs/methodology/code.md`](/specs/methodology/code.md), `.ai/skills/verify-spec-implementation/` names the check that enforces it instead, or a Skipped Step's Sections names it as one stating operating rules.

**A section read in parts.** An audit that reads only part of a section it names says which part. The audits that name one section read all of it between them, each part once. So the checks whose records stand directly under a section enforce all of it between them, each of its rules held to by at least one. Until a section's checks move into records, the entries of the skills' tables and the audits naming the section count among the checks standing under it. A Skipped Step is no check: naming the section in its Sections names it as one stating operating rules, whose check is the step carrying them out. An entry in a skill's table, or a Skipped Step, covers the section it names and the sections under it. Once the entry moves into records, each of those sections is covered by the records standing directly under it. Where a step names the section too, the step carries what leaves no trace in the files, and the audits read the rest.

### Skipped Step

A Skipped Step is one failure a step carrying out an operating rule leaves when it is skipped: the sections stating the operating rules the step carries out, the rule the failure breaks, what it leaves in the files, and what catches it. It is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), its records standing in [`§ Rules and Skills § Skipped Steps`](#skipped-steps):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Skipped Steps \
**Reference Key:** Failure

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Failure | yes | yes | | text | the failure, in a few words |
| Sections | no | yes | | text | a list, each item a citation of a section stating the operating rules the failure skips |
| Rule | no | yes | | text | a citation of the place stating the rule the failure breaks |
| Leaves | no | yes | | text | what the failure leaves in the files |
| Caught By | no | yes | | text | a list, an item to each check catching the failure: a citation of a place; a skill's directory, then its script's flag or the step of the skill, as Carried Out By names a skill's check ([`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check)); a citation of a Script Check record; or the user, where the user is its check |

### Skipped Steps

**Records:**
  - **Failure:** a fact placed, cited or formed against its rule \
    **Sections:**
      - [`specs/AGENTS.md § Writing specs`](/specs/AGENTS.md#writing-specs)

    **Rule:** [`specs/AGENTS.md § Writing specs`](/specs/AGENTS.md#writing-specs) \
    **Leaves:** the fact, placed, cited or formed against its rule \
    **Caught By:**
      - `.ai/skills/audit-specs/` reading audits

  - **Failure:** a direct edit made without the user's approval \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Direct Edits`](/specs/AGENTS.md#direct-edits) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a new branch made without the user's approval \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § A New Branch`](/specs/AGENTS.md#a-new-branch) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a review's entry naming no model and effort \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) \
    **Leaves:** a log entry naming no model and reasoning effort, refused as it is appended \
    **Caught By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a review's model and effort not offered \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a design fixed past a run's length \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) \
    **Leaves:** the design's log, whose entries show the rounds of the run and a change made after the run's last round \
    **Caught By:**
      - the user

  - **Failure:** a step stated without its reach researched \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) \
    **Leaves:** the step patched \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a passage written without zooming out \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out`](/specs/AGENTS.md#the-zoom-out) \
    **Leaves:** the passage patched \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a moved step not taken through Design, Refactor, Refine \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a finding left unmarked \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) \
    **Leaves:** a finding in the round's report holding no mark \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round)

  - **Failure:** a kept finding without its rationale or possible fix \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) \
    **Leaves:** a kept finding in the round's report holding no rationale or no possible fix, a possible fix in neither of its forms, or a dropped finding holding no reason \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a finding judged wrong raised again with no new argument \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) \
    **Leaves:** the finding in the round's report \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round)

  - **Failure:** findings weighed, or the earlier reports read, before all are collected \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) \
    **Leaves:** the report's Reading, showing what the review read \
    **Caught By:**
      - the user

  - **Failure:** an audit's finding left untriaged \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a self-review short of its reading and questions \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) \
    **Leaves:** nothing the script reads, a review then finding what the self-review would have caught \
    **Caught By:**
      - the user

  - **Failure:** a round's change proven by rereading it alone \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove`](/specs/AGENTS.md#change-and-prove) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** something the user says at the apply acted on untold apart \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § What the User Says at the Apply`](/specs/AGENTS.md#what-the-user-says-at-the-apply) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a script changed with no differential test \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check`](/specs/methodology/working-files/main.md#kinds-of-builder-check) \
    **Leaves:** a self-review's report recording no differential test of the script \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a self-review over applied work of a `canon-specs` or `application-specs` design with no construct choice recorded \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check`](/specs/methodology/working-files/main.md#kinds-of-builder-check) \
    **Leaves:** a self-review's report over applied work recording no `construct choice` Builder Check \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a draft on goals or a frame the user has not agreed to \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a settlement stating no cause or no miss \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) \
    **Leaves:** a round's Settlement holding no Cause, or a flaw's Cause holding no Miss \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a round settled finding by finding \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes`](/specs/AGENTS.md#the-round-at-its-causes) \
    **Leaves:** the round's Settlement, showing each finding settled where it sits \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a round settled by more than the least change \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) \
    **Leaves:** the round's Settlement, showing a change past the least of the revisions at its causes \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a change settling short given no reason \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) \
    **Leaves:** a Settlement holding no Departure Reason where its change settles less than the finding's possible fix reaches, which no field the script compares shows, a departure in verdict, in where a finding lies or in lineage being the script's `departures-reasoned` \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a change proposed before the misses are asked \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group`](/specs/AGENTS.md#group) \
    **Leaves:** nothing a record dates, a report holding what was read and never when \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a user's answer to a call left unrecorded \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** an applied Decision Table or State Machine left untraced \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism`](/specs/AGENTS.md#tracing-a-mechanism) \
    **Leaves:** a self-review's report over applied work holding no Trace of a table or a machine a section the diff changed holds, or a Trace leaving a path out \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** another mechanism left untraced \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism`](/specs/AGENTS.md#tracing-a-mechanism) \
    **Leaves:** a self-review's report showing the traces it records \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** an approval ending the review logged as no plan-approval entry \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval`](/specs/AGENTS.md#the-plans-approval) \
    **Leaves:** a log holding no `plan-approval` entry \
    **Caught By:**
      - the user

  - **Failure:** a set of steers closed with no steer entry \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** a Steering Decision no `steer` entry names once its set has closed \
    **Caught By:**
      - the user

  - **Failure:** a steer acted on before its set closes \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) \
    **Leaves:** a design rebuilt, or a round ended, from a steer whose set's `steer` entry stands later, or a set closed with a question of the builder's still open, which the log shows only as the order of the work \
    **Caught By:**
      - the user

  - **Failure:** work running at a set's close stopped or continued without the user's call \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) \
    **Leaves:** a set's entry whose Running Work names no call on work then running, or a check stopped after it handed back findings whose report states no ending \
    **Caught By:**
      - the user

  - **Failure:** a step back with no entry of the user's call \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) \
    **Leaves:** a log holding, after a run's last round, no entry of the call the user made at the step back \
    **Caught By:**
      - the user

  - **Failure:** a design reassessment made with no diagnosis \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Diagnosis`](/specs/methodology/working-files/main.md#a-diagnosis)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) \
    **Leaves:** a design rebuilt after the step back whose log holds no `design-reassessment` entry naming a diagnosis before the rebuilt goals' `goals-agreed` entry \
    **Caught By:**
      - the user

  - **Failure:** a nit judged harmless that harms the work \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit`](/specs/AGENTS.md#a-nit) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** goals or a frame letting findings in left unrevised \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a case, a principle or a Frame Outcome naming no goal \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Frame Part`](/specs/methodology/working-files/main.md#frame-part) \
    **Leaves:** a case of the Scope, a principle of the Approach or a Frame Outcome whose Goals names no goal \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a review reading another working file \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § What a Review Reads`](/specs/AGENTS.md#what-a-review-reads) \
    **Leaves:** nothing in the files, but where the read surfaces in a finding or a citation in the review's report \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round)

  - **Failure:** a marked finding anchored in nothing, or in what the design does not hold \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Finding`](/specs/methodology/working-files/main.md#finding) \
    **Leaves:** a marked finding naming no goal, Frame Outcome or step Objective and citing no rule it breaks, or naming one the design does not hold \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a reviewer's kept finding dropped on the builder's own call \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) \
    **Leaves:** a dropped Settlement departing from its writer's kept verdict, holding a Departure Reason and no User Decision, which no field the script compares tells from a drop the user made \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a Settlement missing its indicators \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) \
    **Leaves:** a Settlement holding no Required By, or not the Justifying Goals or Justifying Rules it names, or, where its finding is kept, no Fix Authority \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a tertiary fix made without the user's call \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) \
    **Leaves:** a tertiary Settlement, or one whose change reaches a tertiary place, holding a Fix Authority other than the user's or no User Decision \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** an order left unassigned or made shallower \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) \
    **Leaves:** a Settlement or a Changed Place holding no Order, or one shallower than its lineage gives \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a departure given no reason \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) \
    **Leaves:** a Settlement departing from a finding it settles, in verdict, in where it lies or in lineage, holding no Departure Reason \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a finding settled or dropped against the test \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) \
    **Leaves:** the round's Settlement, showing each finding it settles and drops \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a review observation counted \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § What a Review Reads`](/specs/AGENTS.md#what-a-review-reads) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a review observation not brought \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a user's edit at the apply not confirmed, logged or checked \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart § Steer, Direction, Feedback, Other Work or the User's Edit`](/specs/methodology/working-files/main.md#steer-direction-feedback-other-work-or-the-users-edit) \
    **Leaves:** a file changed outside the Target that no entry names, or a self-review's report leaving a user's edit unchecked \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-changed-files`
      - `.ai/skills/implement-specs/` `--check-changed-files`
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`](/specs/methodology/working-files/main.md#script-checks-1)
      - the user

  - **Failure:** a design's changes read from outside their home \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing) \
    **Leaves:** a rule reading a design's changes otherwise \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles)

  - **Failure:** something the user approves shown without its summary \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** the reach and wording checks left unrun \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) \
    **Leaves:** nothing the script reads, the retired wording or the file outside the Target left behind \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** the work's checks left unrun over the work \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over`](/specs/AGENTS.md#the-scope-a-check-runs-over) \
    **Leaves:** nothing the script reads, the breach the work caused left in the files \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles)

  - **Failure:** the construct checks left unrun at the self-review \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) \
    **Leaves:** a construct's gap or overlap in the applied text carried to the post-apply review \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - `.ai/skills/audit-specs/` Construct choice and form

  - **Failure:** What Sets the Work not read again on resuming \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Reading Fresh`](/specs/AGENTS.md#reading-fresh) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** findings grouped before the earlier reports are read \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group`](/specs/AGENTS.md#group) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** settling reads missing a finding's evidence \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group`](/specs/AGENTS.md#group) \
    **Leaves:** a round's Settling Reads, with the Read Assessments the log's handed-off judgments hold, leaving out a place a marked finding's Evidence names \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a self-review's reads missing a miss's place \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) \
    **Leaves:** a self-review's Reads leaving out a place a Miss of the phase names \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a settlement naming no earlier report \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Reading the Earlier Reports`](/specs/AGENTS.md#reading-the-earlier-reports) \
    **Leaves:** a round's Settlement leaving out an earlier report of its phase \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a tactical fix short of its Search's matches \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) \
    **Leaves:** a tactical fix made at fewer than every place its Search matched \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a tactical fix made with no Search \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Proposed Change`](/specs/methodology/working-files/main.md#proposed-change) \
    **Leaves:** a Cause's Proposed Change of the Kind tactical fix naming no Search \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a Trace or a continuing Cause stating no outcome \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism`](/specs/AGENTS.md#whether-the-goals-and-the-frame-name-a-mechanism) \
    **Leaves:** a Trace of a self-review before the adversarial review, asked of a mechanism the steps change with no rows, or a Cause continuing an earlier one, stating no outcome of the table \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** the goals and frame test left unasked, unrecorded or not borne out \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism`](/specs/AGENTS.md#whether-the-goals-and-the-frame-name-a-mechanism) \
    **Leaves:** the self-review's report before an adversarial round with no Trace of a mechanism the test reaches, the round's report settling a decision drawing findings again with no Cause continuing an earlier one, or either holding an outcome the goals and the frame do not bear out \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a researched place left unassessed \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) \
    **Leaves:** a report of research leaving a place a Search matched outside the design document, or a place the builder named, within no Read Assessment's Area \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a sweep unrecorded \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document) \
    **Leaves:** a Scope recording no method for its sweep \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a sweep short of the change's rules and terms \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) \
    **Leaves:** Assessed Areas missing a passage stating part of a rule the change states or a use of a term it defines or redefines \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a working file changed by a design's step \
    **Sections:**
      - [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files)

    **Rule:** [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) \
    **Leaves:** the design's Target naming the working file \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-target-kind`
      - `.ai/skills/implement-specs/` `--check-target-kind`

  - **Failure:** a design or its records out of their form \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document)
      - [`specs/methodology/working-files/main.md § Design Goal`](/specs/methodology/working-files/main.md#design-goal)
      - [`specs/methodology/working-files/main.md § Design Plan Step`](/specs/methodology/working-files/main.md#design-plan-step)
      - [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry)
      - [`specs/methodology/working-files/main.md § Retired Phrase`](/specs/methodology/working-files/main.md#retired-phrase)
      - [`specs/methodology/working-files/main.md § Steering Decision`](/specs/methodology/working-files/main.md#steering-decision)
      - [`specs/methodology/working-files/main.md § A Stamp`](/specs/methodology/working-files/main.md#a-stamp)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document) \
    **Leaves:** a design document out of its form \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a design's records out of their record types \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Goal`](/specs/methodology/working-files/main.md#design-goal)
      - [`specs/methodology/working-files/main.md § Design Plan Step`](/specs/methodology/working-files/main.md#design-plan-step)
      - [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry)
      - [`specs/methodology/working-files/main.md § Retired Phrase`](/specs/methodology/working-files/main.md#retired-phrase)
      - [`specs/methodology/working-files/main.md § Steering Decision`](/specs/methodology/working-files/main.md#steering-decision)

    **Rule:** [`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form) \
    **Leaves:** a step, a step Objective, a goal, a Frame Outcome, an Assessed Area, a steer, a log entry or a retired phrase out of its record type \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** a logged entry edited, moved or inserted after its event \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry)

    **Rule:** [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry) \
    **Leaves:** the log, an entry's record of its event changed or standing where its event did not happen \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]`](/specs/methodology/working-files/main.md#script-checks)
      - the user

  - **Failure:** a check cut short left unsettled \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Log Entry § When an Entry Is Appended`](/specs/methodology/working-files/main.md#when-an-entry-is-appended)

    **Rule:** [`specs/methodology/working-files/main.md § Design Log Entry § When an Entry Is Appended`](/specs/methodology/working-files/main.md#when-an-entry-is-appended) \
    **Leaves:** a report of a check cut short holding a finding no Settlement settles, or stating no ending \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`](/specs/methodology/working-files/main.md#script-checks-1)
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1)
      - the user

  - **Failure:** a design's own working files left out of the form its apply lands \
    **Sections:**
      - [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files)

    **Rule:** [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) \
    **Leaves:** the design's working files in a form no longer in force, which its later checks refuse \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** log entries out of their count or their order \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry)

    **Rule:** [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry) \
    **Leaves:** log entries out of their count or their order \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** a design's dependencies out of sync with the workstack \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The Record's Checks`](/specs/methodology/working-files/main.md#the-records-checks)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § What Blocks What`](/specs/methodology/working-files/main.md#what-blocks-what) \
    **Leaves:** a design whose Depends On Designs the workstack does not bear out \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-workstack`
      - `.ai/skills/implement-specs/` `--check-workstack`

  - **Failure:** a design's Status out of sync with the workstack \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The Record's Checks`](/specs/methodology/working-files/main.md#the-records-checks)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise) \
    **Leaves:** a design whose Status the workstack does not bear out \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-workstack`
      - `.ai/skills/implement-specs/` `--check-workstack`

  - **Failure:** a design's citation of another file unresolved \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The Record's Checks`](/specs/methodology/working-files/main.md#the-records-checks)

    **Rule:** [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) \
    **Leaves:** a citation of another file that does not resolve \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a Target out of its Kind \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The Record's Checks`](/specs/methodology/working-files/main.md#the-records-checks)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) \
    **Leaves:** a Target naming a file the design's Kind does not let it change \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a construct or a table in an Objective \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`](/specs/methodology/working-files/main.md#step-objective)

    **Rule:** [`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`](/specs/methodology/working-files/main.md#step-objective) \
    **Leaves:** a step Objective holding a construct or a table \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** an Objective stating no outcome \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`](/specs/methodology/working-files/main.md#step-objective)

    **Rule:** [`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`](/specs/methodology/working-files/main.md#step-objective) \
    **Leaves:** an Objective stating a means: how its step is implemented, a construct, a place in a file, a name the apply writes, wording that is not the user's, or a list of the edits its step makes, an Objective written too specifically \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-states-an-outcome]`](/specs/methodology/working-files/main.md#semantic-checks-3)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** prose around a step's change left inconsistent \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The Standing Objective`](/specs/methodology/working-files/main.md#the-standing-objective)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § The Standing Objective`](/specs/methodology/working-files/main.md#the-standing-objective) \
    **Leaves:** prose within the Target left inconsistent with the steps \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a change none of the design's changes \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing) \
    **Leaves:** a change that is none of the design's changes \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - `.ai/skills/design-specs/` `--check-changed-files`
      - `.ai/skills/implement-specs/` `--check-changed-files`

  - **Failure:** a tactical fix sent back \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval`](/specs/methodology/working-files/main.md#changes-after-approval)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Changes After Approval`](/specs/methodology/working-files/main.md#changes-after-approval) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a steer recorded out of its form \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision`](/specs/methodology/working-files/main.md#steering-decision)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision`](/specs/methodology/working-files/main.md#steering-decision) \
    **Leaves:** a Decision not giving the essence of what its steer decided \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a revising steer not naming the steer it revises \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** a revising steer's Decision not naming the steer it revises \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a steer quoting only part of the user's words \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart`](/specs/methodology/working-files/main.md#telling-a-steer-apart)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart § Steer, Direction, Feedback, Other Work or the User's Edit`](/specs/methodology/working-files/main.md#steer-direction-feedback-other-work-or-the-users-edit) \
    **Leaves:** a Steer quoting only part of the user's words that decided \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a steer of a Type other than its own \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § A Steer's Type`](/specs/methodology/working-files/main.md#a-steers-type)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § A Steer's Type`](/specs/methodology/working-files/main.md#a-steers-type) \
    **Leaves:** a steer of a Type other than its own \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a set of steers changing the goals or the frame applied unconfirmed \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** an unanswered question read as agreed \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** an earlier steering decision rewritten \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a design lagging a steer \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)
      - [`specs/methodology/working-files/main.md § Steering Decision § Revisiting a Steer`](/specs/methodology/working-files/main.md#revisiting-a-steer)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** a design not yet carrying out a directive it records, or departing from an agreement with no revision recorded citing it \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a frame out of sync with its steers or its steps \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) \
    **Leaves:** a frame out of sync with its directives, with an agreement it has not revised on the record, or with its steps, such as a Frame Outcome untrue of the steps \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a design's part holding less than its form asks \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document) \
    **Leaves:** an Out of Scope naming another working file, a dependency named with no statement of what the design relies on from it, or a canon design's Impact on the Application Specs holding no item and not saying how its research was done \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a hand-off that nothing holds \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document`](/specs/methodology/working-files/main.md#a-design-document)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Spawning a Change of Its Own`](/specs/methodology/working-files/main.md#spawning-a-change-of-its-own) \
    **Leaves:** an item of Out of Scope or of Impact on the Application Specs handing on work no design or follow-up holds \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a reliance no longer matching its dependency \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`](/specs/methodology/working-files/main.md#blocked-and-to-revise) \
    **Leaves:** a statement of what a design relies on that its finished dependency does not settle \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a decision of the user's left out of the steers \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded)

    **Rule:** [`specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`](/specs/methodology/working-files/main.md#when-a-steer-is-recorded) \
    **Leaves:** a design's steers missing a decision the user gave \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a report not recording its settlement \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report`](/specs/methodology/working-files/main.md#a-checks-report)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report`](/specs/methodology/working-files/main.md#a-checks-report) \
    **Leaves:** a check's report not recording how its findings were settled \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** an audit's triage not recording what the design caused \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Verdicts`](/specs/methodology/working-files/main.md#verdicts)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) \
    **Leaves:** the builder's triage of an audit not recording each finding as caused by the design or not \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a report handed back unchecked \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files/main.md#who-writes-each-part)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) \
    **Leaves:** a report out of its form as settling starts \
    **Caught By:**
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--take-up-report`

  - **Failure:** a reviewer's part of a report changed by the builder \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files/main.md#who-writes-each-part)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`](/specs/methodology/working-files/main.md#who-writes-each-part) \
    **Leaves:** a part its cold agent wrote no longer matching the fingerprint its Hand-back holds \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a cause or a miss the files do not bear out \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`](/specs/methodology/working-files/main.md#what-the-design-script-checks)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group`](/specs/AGENTS.md#group) \
    **Leaves:** a Cause's decision or a Miss the files do not bear out \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a verdict the files do not bear out \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`](/specs/methodology/working-files/main.md#what-the-design-script-checks)

    **Rule:** [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) \
    **Leaves:** a Finding's Verdict the files do not bear out \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a Builder Check's Result the files do not bear out \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`](/specs/methodology/working-files/main.md#what-the-design-script-checks)

    **Rule:** [`specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check`](/specs/methodology/working-files/main.md#kinds-of-builder-check) \
    **Leaves:** a Builder Check's Result the files do not bear out \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** a log entry out of its type \
    **Sections:**
      - [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry)

    **Rule:** [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry) \
    **Leaves:** a log entry out of its type, refused as it is appended \
    **Caught By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a design applied over uncommitted changes \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files/main.md#uncommitted-changes)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes`](/specs/methodology/working-files/main.md#uncommitted-changes) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a design's changes committed with another's \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a design's changes committed unbidden \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing)

    **Rule:** [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a commit message not naming each edit \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing) \
    **Leaves:** a commit message leaving out a direct edit or an edit of the user's \
    **Caught By:**
      - the user

  - **Failure:** a send-back setting aside its kept changes \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a sent-back design's kept changes read as the last commit \
    **Sections:**
      - [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`](/specs/methodology/working-files/main.md#a-send-back) \
    **Leaves:** changes that are none of the design's \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a design worked out of its machines' order \
    **Sections:**
      - [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-order-of-a-designs-work)

    **Rule:** [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-order-of-a-designs-work) \
    **Leaves:** nothing the files decide \
    **Caught By:**
      - the user

  - **Failure:** a review started with more than the standard brief, a brief of a skill's own among it, or an audit with any brief \
    **Sections:**
      - [`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)
      - [`specs/methodology/design-workflow/reviews-brief.md § A Review's Brief`](/specs/methodology/design-workflow/reviews-brief.md#a-reviews-brief)

    **Rule:** [`specs/methodology/design-workflow/reviews-brief.md § A Review's Brief`](/specs/methodology/design-workflow/reviews-brief.md#a-reviews-brief) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** research started with more than the research brief, a brief of a skill's own among it \
    **Sections:**
      - [`specs/methodology/design-workflow/reviews-brief.md § A Research Brief`](/specs/methodology/design-workflow/reviews-brief.md#a-research-brief)

    **Rule:** [`specs/methodology/design-workflow/reviews-brief.md § A Research Brief`](/specs/methodology/design-workflow/reviews-brief.md#a-research-brief) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a review not sized by its Kind \
    **Sections:**
      - [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)

    **Rule:** [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews) \
    **Leaves:** the design's log, whose entries name each review's effort \
    **Caught By:**
      - the user

  - **Failure:** a review not run at its effort \
    **Sections:**
      - [`specs/methodology/design-workflow/reviews-effort.md § A Review's Effort`](/specs/methodology/design-workflow/reviews-effort.md#a-reviews-effort)

    **Rule:** [`specs/methodology/design-workflow/reviews-effort.md § A Review's Effort`](/specs/methodology/design-workflow/reviews-effort.md#a-reviews-effort) \
    **Leaves:** the design's log, whose entries name each review's model and effort \
    **Caught By:**
      - the user

  - **Failure:** an audit in an apply run over other sub-scopes than the user settled \
    **Sections:**
      - [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)

    **Rule:** [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a canon design's research run with its sub-scopes not settled with the user \
    **Sections:**
      - [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)

    **Rule:** [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews § The Sub-scopes a Design Settles § The Sub-scopes of a Canon Design's Research`](/specs/methodology/design-workflow/designs-reviews.md#the-sub-scopes-of-a-canon-designs-research) \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a canon design's research run with its sub-scopes unrecorded \
    **Sections:**
      - [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)

    **Rule:** [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews § The Sub-scopes a Design Settles § The Sub-scopes of a Canon Design's Research`](/specs/methodology/design-workflow/designs-reviews.md#the-sub-scopes-of-a-canon-designs-research) \
    **Leaves:** a canon design's Scope holding no Search Sub-scopes, or Search Sub-scopes naming anything but a sub-scope or leaving out `core-canon` or `skills` \
    **Caught By:**
      - [`specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-sub-scopes-recorded]`](/specs/methodology/working-files/main.md#script-checks-1)

  - **Failure:** a reviewer definition left in version control \
    **Sections:**
      - [`specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent`](/specs/methodology/skills/setting-up-an-agent.md#setting-up-an-agent)

    **Rule:** [`specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent`](/specs/methodology/skills/setting-up-an-agent.md#setting-up-an-agent) \
    **Leaves:** a reviewer definition in version control \
    **Caught By:**
      - `.ai/skills/audit-specs/` `--check-scope`

  - **Failure:** a citation naming a heading that does not exist \
    **Sections:**
      - [`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure)
      - [`specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope`](/specs/methodology/scope/what-spec-of-record-governs.md#the-shape-of-the-scope)

    **Rule:** [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) \
    **Leaves:** the citation \
    **Caught By:**
      - `.ai/skills/audit-specs/` `--check-scope`

  - **Failure:** a fact given a second home \
    **Sections:**
      - [`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure)
      - [`specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope`](/specs/methodology/scope/what-spec-of-record-governs.md#the-shape-of-the-scope)
      - [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact)

    **Rule:** [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact) \
    **Leaves:** the fact stated twice \
    **Caught By:**
      - `.ai/skills/audit-specs/` Where a rule lives

  - **Failure:** a term used against its sense \
    **Sections:**
      - [`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure)
      - [`specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope`](/specs/methodology/scope/what-spec-of-record-governs.md#the-shape-of-the-scope)

    **Rule:** [`specs/methodology/glossary/glossary.md § Glossary`](/specs/methodology/glossary/glossary.md#glossary) \
    **Leaves:** the term's use \
    **Caught By:**
      - `.ai/skills/audit-specs/` Glossary terms

  - **Failure:** a sentence holding several rules \
    **Sections:**
      - [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact)

    **Rule:** [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact § One Rule to a Sentence`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-rule-to-a-sentence) \
    **Leaves:** the sentence \
    **Caught By:**
      - `.ai/skills/audit-specs/` Where a rule lives

  - **Failure:** a citation bare where it owed more \
    **Sections:**
      - [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact)

    **Rule:** [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact) \
    **Leaves:** a citation bare where it owed its application or its reason \
    **Caught By:**
      - `.ai/skills/audit-specs/` Whether the home holds the fact

  - **Failure:** a view or a counterpart left out of sync \
    **Sections:**
      - [`specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md § Keeping Specs in Sync`](/specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md#keeping-specs-in-sync)

    **Rule:** [`specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md § Keeping Specs in Sync`](/specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md#keeping-specs-in-sync) \
    **Leaves:** the view or the counterpart, out of sync with what the change reached \
    **Caught By:**
      - `.ai/skills/audit-specs/` Directory summary currency
      - `.ai/skills/audit-specs/` Diagram currency
      - `.ai/skills/audit-specs/` Counterpart currency

  - **Failure:** the technical overview's account of the code left out of sync \
    **Sections:**
      - [`specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md § Keeping Specs in Sync`](/specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md#keeping-specs-in-sync)

    **Rule:** [`specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md § Keeping Specs in Sync § Materialized Views`](/specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md#materialized-views) \
    **Leaves:** the technical overview's account, untrue of the code \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** a file or a domain placed against its test \
    **Sections:**
      - [`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)
      - [`specs/methodology/spec-placement/naming-a-capability-domain.md § Naming a Capability Domain`](/specs/methodology/spec-placement/naming-a-capability-domain.md#naming-a-capability-domain)

    **Rule:** [`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes) \
    **Leaves:** the file or the domain where its test does not place it \
    **Caught By:**
      - `.ai/skills/audit-specs/` Placement

  - **Failure:** a section stating rules that no check names \
    **Sections:**
      - [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills)

    **Rule:** [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills) \
    **Leaves:** a section stating rules that neither a reading audit of `.ai/skills/audit-specs/` names as one it enforces nor any Skipped Step's Sections names, nor, for [`specs/methodology/code.md`](/specs/methodology/code.md), the check on code's, nor a record section of checks standing directly under it \
    **Caught By:**
      - `.ai/skills/audit-specs/` `--check-scope`

  - **Failure:** a section stating operating rules no step cites \
    **Sections:**
      - [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills)

    **Rule:** [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills) \
    **Leaves:** a section stating operating rules that no Workflow step cites \
    **Caught By:**
      - `.ai/skills/audit-specs/` `--check-scope`

  - **Failure:** a work not read as its persona's \
    **Sections:**
      - [`specs/methodology/spec-placement/personas.md § Personas`](/specs/methodology/spec-placement/personas.md#personas)

    **Rule:** [`specs/methodology/spec-placement/personas.md § Personas`](/specs/methodology/spec-placement/personas.md#personas) \
    **Leaves:** a spec, the documentation, or a design changing code, that does not read as its persona's \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a review not framed as its persona \
    **Sections:**
      - [`specs/methodology/spec-placement/personas.md § Personas`](/specs/methodology/spec-placement/personas.md#personas)

    **Rule:** [`specs/methodology/spec-placement/personas.md § Personas`](/specs/methodology/spec-placement/personas.md#personas) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a technical change breaking its product file's promise \
    **Sections:**
      - [`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability)

    **Rule:** [`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability) \
    **Leaves:** the technical file, breaking a promise its product file makes \
    **Caught By:**
      - `.ai/skills/audit-specs/` Counterpart currency

  - **Failure:** a code design reaching beyond one module \
    **Sections:**
      - [`specs/methodology/spec-placement/product-module.md § A Product Module`](/specs/methodology/spec-placement/product-module.md#a-product-module)

    **Rule:** [`specs/methodology/working-files/main.md § A Design Document § A Design Changing Code § One Product Module`](/specs/methodology/working-files/main.md#one-product-module) \
    **Leaves:** a design changing code whose Target reaches beyond one module \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** a gap the module rule names \
    **Sections:**
      - [`specs/methodology/spec-placement/product-module.md § A Product Module`](/specs/methodology/spec-placement/product-module.md#a-product-module)

    **Rule:** [`specs/methodology/spec-placement/product-module.md § A Product Module`](/specs/methodology/spec-placement/product-module.md#a-product-module) \
    **Leaves:** a design written past the gap \
    **Caught By:**
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`](/specs/AGENTS.md#check-roles)
      - the user

  - **Failure:** code handed on with a local task unrun \
    **Sections:**
      - [`specs/methodology/spec-placement/environments.md § Environments`](/specs/methodology/spec-placement/environments.md#environments)

    **Rule:** [`specs/methodology/spec-placement/environments.md § Environments`](/specs/methodology/spec-placement/environments.md#environments) \
    **Leaves:** a self-review's report recording no run of the task \
    **Caught By:**
      - [`specs/methodology/spec-placement/environments.md § Environments`](/specs/methodology/spec-placement/environments.md#environments)
      - [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`](/specs/AGENTS.md#check-roles)

  - **Failure:** governed code doing what no spec states \
    **Sections:**
      - [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code)

    **Rule:** [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code) \
    **Leaves:** the code \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** code a change writes against American English \
    **Sections:**
      - [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code)

    **Rule:** [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code) \
    **Leaves:** the code's spelling \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** a change to code made outside a design \
    **Sections:**
      - [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code)

    **Rule:** [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code) \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user
