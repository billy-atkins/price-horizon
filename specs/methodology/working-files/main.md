## The Working Files

A working file is never committed, since no reader of the specs needs it. Which specs may name one is set in [`specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation/which-citations-are-allowed.md#which-citations-are-allowed). What a working file settles reaches a reader only through the spec it changes. In construction's terms, a design document is a change order, and the specs are the as-built drawings: the plans kept true to what stands, so the next change starts from the building as it is.

The builder changes a working file as the section holding its form has it, never by a design's step: a design document by the skill writing it, and a follow-up once the user approves its text ([`§ A Follow-up`](#a-follow-up)). A design changing a working file's form keeps its own working files in the form in force while it is designed and reviewed. They are written and checked by the rules in force, so no round judges its record by a form its steps are still writing. As its apply lands the new form, it brings its own working files to that form, every part of a design document the same way. Its log is among them: an entry's form changes, and its record of its event never does ([`§ Design Log Entry`](#design-log-entry)). Its later checks are then recorded in the new form. A design begun after the apply uses the new form from its start. Every other working file is brought to the form when the work next takes it up, as its due, by the builder working it and by no one before then. So no design's work reads another design's working files to bring them to its form, which would fill the builder's context with work that is not its own. Until then, a working file written before a form stands as it was written. A check asked of it reports what the form in force does not take, and a record it holds from before that form is read under the form it was written with. [`§ A Design Document § What Blocks What § A Design Written Under the Earlier Rules`](#a-design-written-under-the-earlier-rules) gives a design written under the earlier dependency rules its reading. A working file is of no kind of change, so no design's Target names one.

**Reference Key:** File \
**Required:** Holds

| File | Holds |
|---|---|
| `.ai/plans/` | the plans the skills write, a design document among them ([`§ A Design Document`](#a-design-document)) |
| `.ai/follow-ups.md` | work on the specs, the code or the working files that should be done and is not yet, each as a follow-up ([`§ A Follow-up`](#a-follow-up)) |
| `.ai/tmp/` | the skills' own output, a design's check reports and an audit run's reports among it, and the folder a run of the kept tests writes within |

**A design's folder is `.ai/tmp/<skill-name>/<design>/`.** Every file a design's work leaves under `.ai/tmp/` sits in the design's folder, under the folder of the skill writing the design, so a reader and a script find a design's files by where they sit. A file no design's work writes, such as an audit run's report or a diagram's render, stays where its own skill puts it. A design's folder holds these kinds of file, each where its row has it:

**Reference Key:** Kind \
**Required:** Sits In

| Kind | Sits In |
|---|---|
| report | `reports/<check kind>/`, named `{n}.md` by the kind and the number of the log entry naming it, as `reports/self-review/3.md` for `self-review-3` ([`§ A Check's Report`](#a-checks-report)) |
| diagnosis | `diagnosis/`, named `{n}.md`, n counting the diagnoses the design's `design-reassessment` entries name, as `diagnosis/3.md` for the third, whatever the count of the entry naming it ([`§ A Diagnosis`](#a-diagnosis)) |
| script | `scripts/` |
| backup | `backups/`: a copy of a file taken before the builder changes it, named for the file it copies and the moment it was taken |
| scratch | `scratch/`: every other file, a script's input or output and the builder's working text among it |

A report not in the form [`§ A Check's Report`](#a-checks-report) gives whose entry is not yet appended sits in the design's `scratch/`, and its check is run again in the form, the design taken up afresh as the user directs.

**A skill's scratch space is `.ai/tmp/<skill-name>/`.** The skill creates the directory if it is not there. Each skill has a directory of its own, so one skill's output is never mistaken for another's. The directory sits under `.ai/tmp/`, so none of it is ever committed. A skill does not delete its output when it finishes. The output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its *stale* output: a file left behind from a previous run that no longer corresponds to anything, because a reader has no way to tell such a file from a current one.

**The kept tests' run folder is `.ai/tmp/kept-tests/`.** It is no skill's scratch space. A run of the kept tests ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) writes within it, and [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests § A Run`](/specs/methodology/skills/authoring-a-skill.md#a-run) sets what a run writes there, what clears it and what a run leaves in it.

**A skill's plans are `.ai/plans/<skill-name>/`.** A skill describing a change before making it writes each plan to a file of its own in that directory. The skill creates the directory if it is not there. Each skill has a directory of its own, so one skill's plans are never mistaken for another's. Each plan has a file of its own, so each plan is read, reviewed and handed to a cold agent whole.

An open question about what is specified is recorded in a spec, per [`specs/methodology/spec-placement/open-question.md § Open Question`](/specs/methodology/spec-placement/open-question.md#open-question). A working file never holds one.

## A Design Document

Each design document is a file of its own, one per change taken through the Design, Refactor, Refine process ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)). `.ai/skills/design-specs/` writes each design changing the specs under `.ai/plans/design-specs/`, and `.ai/skills/implement-specs/` writes each design changing code under `.ai/plans/implement-specs/`. Both take this form. A design changing code differs only where [`§ A Design Document § A Design Changing Code`](#a-design-changing-code) sets. A design document is the plan for its change, the plan [`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md) defines: its goals, its frame and its steps are what the user's first approval covers, and the text or code its apply writes is not. Each skill's steps and script hold a design to this form. The script reaches the design document tooling the two skills share. The plan, its frame, its steps' Objectives and its Drafts, holds what the design changes, and cites the canon's home for each rule it relies on and leaves as it is, never stating that rule again, as [`§ A Design Document § Semantic Checks [Name: plan-cites-what-it-keeps]`](#semantic-checks) has it judged. No audit reads a design ([`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)). A design opens with a level-one heading, `Design Document`, whose section holds the design's fields ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)). The design's sections follow as level-two headings. A design holds these parts, in this order:

**Reference Key:** Part \
**Required:** Form, Required, Holds

| Part | Form | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | a `**Name:**` field | yes | | the design's slug, the change in a few words in kebab-case ([`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion)). The file is named `{Name}.md`. Other design documents name this one by its Name. One in another skill's plans directory puts this design's directory name and a slash before it, as `design-specs/{Name}` |
| Version | a `**Version:**` field | no | 0.1.0 | the design's version, as [`§ A Design Document § The Design's Version`](#the-designs-version) has it worked out |
| Status | a `**Status:**` field | yes | | its state in [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) |
| Source | a `**Source:**` field | yes | | what asked for the change: the user's own words, or the finding that raised it |
| Kind | a `**Kind:**` field | yes | | the kind of change, one of the kinds [`§ A Design Document § The Kinds of Change`](#the-kinds-of-change) gives, which bounds the files the builder edits, the steps' writing and each direct edit, though not a user's edit, which lies wherever the user made it. It sizes the design's reviews ([`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews)). It is settled while the design is shaped and before any file is edited |
| Target | a `**Target:**` field | yes | | the places standing when the plan is approved that the steps change or create under, each a path in backticks, separated by semicolons: each file holding an area the frame's Assessed Areas hold with an Impact holding `changes`, and each directory the steps create a file or folder under, its path ending in a slash, the project's root written `./`; never a file or folder the steps create, which the directory it is created under covers; none while the design is not-started and its files are not yet known |
| Spawned By | a `**Spawned By:**` field | yes | | the design document this one was spawned from, or none |
| Depends On Designs | a `**Depends On Designs:**` field | yes | | the design documents that block this one, separated by semicolons, or none; what blocks a design, and when, is set by [`§ A Design Document § What Blocks What`](#what-blocks-what) |
| Validated | a `**Validated:**` field | yes | | the stamp the validation review left once the document passed it, per [`§ A Stamp`](#a-stamp), leaving out the Validated and Status fields and the Design Log Entries section but each entry naming a report the validation review reads; or none; a stamp current while the design is approved |
| The Problem | a `## The Problem` section | yes | | what is wrong, stated on its own, before any fix: only the harm and the evidence that it happened, never what led to it, since each sentence the design does not need is an edge a reviewer can challenge. What it says of the files holds of them as they stand when goals are proposed from it, in each major version, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has the builder read it again |
| Design Goals | a `## Design Goals` record section ([`§ Design Goal`](#design-goal)) | until the design is complete or abandoned | | the design's goals, or `Not yet stated.` until the user agrees on them, which no design approved or further holds |
| The Design Frame | a `## The Design Frame` section | yes | | the design frame ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) the user agreed to ([`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame)), under level-three headings in this order: Scope, Assessed Areas, Approach and Frame Outcomes. Scope holds the cases the change governs in its Cases field, each a record of [`§ A Design Document § Scope Case`](#scope-case), then the method of the research ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) that swept for affected content, never the whole of what it matched. Until it is stated, its Scope reads `Not yet stated.` Assessed Areas is a record section of the areas in the design's scope ([`§ A Design Document § Assessed Area`](#assessed-area)). Approach holds the principles the solution applies, one or more, in its Principles field, each a record of [`§ A Design Document § Approach Principle`](#approach-principle). Frame Outcomes is a record section of the frame's outcomes ([`§ A Design Document § Frame Outcome`](#frame-outcome)). Each case, each principle and each Frame Outcome names the goals it rests on, as [`§ A Design Document § Frame Part`](#frame-part) has it, and the Assessed Areas name none. What the design assumes of a design its Depends On Designs names stands in its cases and its principles, and in no record of its own. What the change leaves out is its Out of Scope's. A part not yet stated reads `Not yet stated.`, which no design approved or further holds |
| Steering Decisions | a `## Steering Decisions` record section | once the user has steered the design | | each steer the user gave, per [`§ Steering Decision`](#steering-decision) |
| Design Plan Steps | a `## Design Plan Steps` record section ([`§ Design Plan Step`](#design-plan-step)) | yes | | the plan's steps, or `Not yet drafted.` until drafting states them, which no design approved or further holds |
| Retired Phrases | a `## Retired Phrases` record section ([`§ Retired Phrase`](#retired-phrase)) | no | none | the wording the design retires, each phrase with its replacement and the places it stays right, a phrase the user turned down while steering among them |
| Impact on the Application Specs | a `## Impact on the Application Specs` section | in a canon design | | the application work the canon change hands on, as [`§ A Design Document § A Change Needing Both Kinds`](#a-change-needing-both-kinds) has it handed on, in a list of items. An application area whose latest Read Assessment holds `changes` takes an item opening with a bold lead-in, then the area's place, citing the report holding that Read Assessment. An application finding that the post-apply review or the audit hands on at the apply takes an item opening with a bold lead-in, then citing the report holding the finding, and the finding. Each item says what the application work must do there and what it is handed on to, a design or a follow-up. Where no item stands, the section says that none was found and how the research covered the application specs |
| Design Log Entries | a `## Design Log Entries` record section ([`§ Design Log Entry`](#design-log-entry)) | once the design's first entry is appended | | the design's log: an entry for each check of its work and each event of its workflow, in the order they came |
| Out of Scope | a `## Out of Scope` section | yes | | only what the design's own words could be read to include but that it leaves out, so a reviewer spends no time on it, and nothing else, however unrelated. Each item is a part kept unchanged on purpose, a change declined, a known problem on the design's path left no worse, or a stage of a goal handed on. Work handed on is a change declined or a stage, the code a design changing the specs leaves out of sync among it. An area whose latest Read Assessment holds `changes` and that the design leaves out is a change declined, named by an item holding its place right after the item's bold lead-in. Where the change leaves such an area false, its item hands the area's update on. Each item gives its reason. It names no other working file. It names where it goes only where it is a stage or hands work on, the work held where the skill's step handing it on sends it. Each item is the user's call as it is written. The builder brings it in plain words with its recommendation, and writes it only once the user approves it. The item cites the steer approving it, whose Changes holds `Out of Scope item`. Work the design waits on is named in its Depends On Designs instead, and the application work a canon design leaves is in its Impact on the Application Specs, an application area among it |

### Semantic Checks

**Records:**
  - **Name:** plan-cites-what-it-keeps \
    **Tests:** a design's plan, its frame, its steps' Objectives and its Drafts, states what the design changes and cites the canon's home for each rule it relies on and leaves as it is; a passage restating such a rule is a second statement of a fact with a home, judged as [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact) judges one, a Draft's copy of the whole construct its step changes aside \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per design document

  - **Name:** out-of-scope-item-bounded \
    **Tests:** each item of a design's Out of Scope names what the design's own words could be read to include but that it leaves out, a part kept unchanged on purpose, a change declined, a known problem on the design's path left no worse or a stage of a goal handed on, and names where it goes only where it is a stage or hands work on, as this section's Out of Scope row has an item \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per Out of Scope item

### The Standing Objective

Every step of a design carries one Objective the canon keeps rather than each step stating it: every passage in the reach the post-apply review reads, in the Target or outside it, stays true with the step's change. The builder meets it at the apply, and the post-apply review checks it there, never passage by passage in the steps. What the change made false is told from what stood false before as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is`](/specs/AGENTS.md#whose-a-finding-is) tells a finding the work's, and a passage outside the Target is settled as [`§ A Design Document § Changes After Approval`](#changes-after-approval) has it.

### The Design's Version

A design's version says which state of the design an entry or a report stands at. So an agent or a script finds the reports of the design's current major version from the header and the entries alone. The canon adopts Semantic Versioning for it ([`specs/methodology/external-references.md § External References [Name: Semantic Versioning]`](/specs/methodology/external-references.md#external-references)). The version is written in the standard's form, and its major and minor mean what the standard says, so the rules on which reports bind read in the standard's terms.

A design's goals stand for its public interface. A design with only its problem is in initial development, at 0.1.0, as the standard starts one. The `goals-agreed` entry appended as the user agrees to the goals raises a design in initial development to 1.0.0, as [`§ A Design Document § The Design's Version [Semantic Versioning Elements.Semantic Versioning: 1.0.0]`](#the-designs-version) maps the standard's 1.0.0 onto that agreement ([`§ Design Log Entry`](#design-log-entry)). Each major version's rebuilt goals are agreed the same way, and no check's report stands before the agreement of its major version's goals. After 1.0.0, each counter is raised by its own kind of change:
- **Major.** A design reassessment is the incompatible change: its earlier reports no longer bind it.
- **Minor.** A set of steers changing the goals raises it, the reports of its major version still binding the design across it, as [`§ A Design Document § The Design's Version [Semantic Versioning Elements.Semantic Versioning: MINOR]`](#the-designs-version) departs from the standard's minor. The frame, stated after the research the goals direct, is the design's working out of its interface rather than a part of it. A set changing the frame raises the minor too, as the standard lets a substantial change within the private code raise it.
- **Revision.** A revision of the steps raises it, the goals and the frame standing, the standard's PATCH as [`§ A Design Document § The Design's Version [Semantic Versioning Elements.Semantic Versioning: PATCH]`](#the-designs-version) names it.

Comparing two versions' majors is the standard's precedence. A design a split spawns starts at 0.1.0.

The design script alone works the version out from the log, by the entries raising it in the order they stand, a raised counter clearing each counter after it. It writes the version to the header, leaving it out at 0.1.0, its default, and refuses a header version the log does not give. Each entry is stamped at the version of the design its work read, as [`§ Design Log Entry`](#design-log-entry) has it stamped. Each entry raises the counter its row gives:
- **Entry.** The entry's kind.
- **Starts a major version?** Whether the entry is a `design-reassessment` entry, or an old `reassessment` entry whose Decision is other than `go on`. Each records a design reassessment, which starts a major version as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has one start a major version.
- **In initial development?** Whether the version's major is 0.
- **Changes the goals or the frame?** Whether the highest part the Changes of the Steering Decisions a `steer` entry names hold is the goals or a part of the frame ([`§ Steering Decision`](#steering-decision)).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Entry, Starts a major version?, In initial development?, Changes the goals or the frame?

| Entry | Starts a major version? | In initial development? | Changes the goals or the frame? | Raises |
|---|---|---|---|---|
| `design-reassessment`, `reassessment` | true | false | - | major |
| `goals-agreed` | - | true | - | major |
| `steer` | - | - | true | minor |
| `plan-change` | - | - | - | revision |
| - | - | - | - | nothing |

A design reassessment in initial development raises nothing, since a design with no report has nothing to make afresh. A `goals-agreed` entry after initial development raises nothing. A set of steers raises the minor once, since its one `steer` entry names each of its Steering Decisions. A set changing the steps alone raises nothing of itself, since the `plan-change` its revision brings raises the revision counter. The step back, the user's approval given there and a set changing nothing raise nothing.

The version departs from the standard only where a row of its mapping says, each departure deliberate as [`specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard`](/specs/methodology/sourcing-and-citation/external-reference.md#a-mapping-onto-a-standard) has one:

**Table Name:** Semantic Versioning Elements \
**Reference Key:** Semantic Versioning \
**Required:** Section, Treatment

| Semantic Versioning | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| PATCH | 2, 6 | differs: the third counter, named revision, raised by a revision of the steps | the canon's form | every change is a revision, never a patch, as [`specs/AGENTS.md § Constitutional Principles § Revise, Never Patch`](/specs/AGENTS.md#revise-never-patch) has it, so the counter takes the principle's name |
| version increment | 6, 7, 8 | differs: worked out from the design's log by the design script, never set by hand | the canon's form | the log records each event that raises a counter, so a version set by hand could say what the record does not |
| normal version | 2 | differs: 0.1.0 left out of the header, an entry and a report's Reading, as a field's default value is | the canon's form | a field at its default is left out, as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has a default left |
| 1.0.0 | 5 | differs: marks the user's agreement to the design's goals, never a release | the standard's gap | a design publishes no interface; its goals stand for one, and the user's agreement is what defines them, so that agreement marks the version |
| MINOR | 7 | differs: raised once by a set of steers changing the goals or the frame, which may change or drop a goal | the standard's gap | the standard's minor only adds, while a design's reports stay binding across a change to its goals, judged against the goals as they then stand, and no counter of the standard's holds that change |
| pre-release version | 9 | not written | no need yet | a design's state is its Status, and its log records each event, so no spec needs a pre-release part |
| build metadata | 10 | not written | no need yet | no spec needs to tell apart two builds of one version of a design |

### The Record's Checks

Before each adversarial round and before the user's approval, the validation review checks that the design document is a valid document. The validation review is the design script of the skill writing the design. It checks the document's structure alone. It draws only on the document, the canon's declarations of its form, the reports of the handed-off judgments the design's log names and, for the constructs a step's Draft holds, the specs as they stand. It never judges what any of them says, and reads no file besides those. The specs give what a Draft's construct reads and does not declare. Of those reports it reads only those of the design's current major version, as [`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record) has a design's reports bind it, so no earlier major version's research binds the design. Of those it leaves out each whose entry stands after the design's last `plan-approval` entry, except where an `entered` entry, or a `steer` entry whose set changes the goals or a part of the frame ([`§ A Design Document § The Design's Version`](#the-designs-version)), follows that approval. So research logged after the plan's approval, when the frame is frozen, leaves the validation as it stood, while a design sent back, or one whose goals or frame a steer changed after the approval, reads the research rebuilt for it. How the builder applied the user's steers, and whether the design is right, are the adversarial review's to read ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review)). The steers are that review's account of how the design was shaped. The checks:

**Reference Key:** Check \
**Required:** What The Record Holds, Why

| Check | What The Record Holds | Why |
|---|---|---|
| Form | its heading, its fields and its sections in the order and the form [`§ A Design Document`](#a-design-document)'s table of parts gives them, each block of fields and each list a field holds as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has them, read by its one reader, each blank line placed as [`specs/methodology/spec-style/markdown.md § Blank Lines`](/specs/methodology/spec-style/markdown.md#blank-lines) has it, and, by the time it is validated, no goal, no part of its frame and no step section reading `Not yet stated.` or `Not yet drafted.`; and no construct and no table in a step Objective ([`§ Design Plan Step § Step Objective`](#step-objective)) | a reader and a script find each part where the form puts it |
| Records | its design goals, its steering decisions, its design plan steps and each other record section, each record holding the fields its type declares, a Type among the values it declares, and each Name used once; each design log entry's count counting its kind from 1 in the order the entries stand, and each Timestamp no earlier than the one before it; its Version the one its log gives ([`§ A Design Document § The Design's Version`](#the-designs-version)), and the Design Version each entry holds one the log held as the entry was appended; and each check's entry standing after a `goals-agreed` entry of its major version ([`§ Design Log Entry § Script Checks [Name: goals-agreed-before-checks]`](#script-checks)) | a record out of its form is one no script can read |
| References | each Name a field holds, a Frame Outcome's Goals, a step's Depends On Steps, and a step Objective's Goals and Upholds Frame Outcomes, and a case's and a principle's Goals, naming a part the design holds; no Name used twice across its goals, cases, principles, Frame Outcomes, steps and step Objectives; each goal served by a step Objective naming it, and each Frame Outcome upheld by one; no step depending on itself through the steps it depends on, and none standing before a step it depends on | a reference to nothing leads a reader, and the work, nowhere, and a part nothing serves or upholds is a gap in the plan |
| Lineage | each place a step's What names reaching an Assessed Area whose Impact holds `changes`, and each such Assessed Area reached by a step's What (a What reaching an Area where a place it names is the Area, lies within it or holds it); each Assessed Area's Impact and Assessment those of the latest Read Assessment of its Area in the reports the validation review reads; and each Area whose latest Read Assessment there holds an Impact other than `none` an Assessed Area or, its Impact holding `changes`, named by an item of the Out of Scope or, in a canon design, of the Impact on the Application Specs, holding its place right after the item's bold lead-in | nothing enters the design's scope but through an assessment, and each step changes only what is in scope |
| Drafts | each construct a step's Draft holds, as its block writes it, by the construct checks, each `markdown` block read as a file of its own beside the specs as they stand and the design's other Drafts, a citation in it resolved against both ([`§ Design Plan Step § A Draft`](#a-draft)); a block of code is checked by none | a Draft's construct is held to its form before a reviewer reads it, as the applied text's is at the apply |
| Research | of a design not yet approved alone, the research reports it reads, read together: each place a Search of them gives where its kind gives every place, and each place a Search of them of the Kind "meaning" holds, lying within the Area of a Read Assessment in one of them, whichever report holds the Search ([`§ A Check's Report § Script Checks [Name: research-covers-its-matches]`](#script-checks-1)); and each goal the design holds named by Searches by terms that together leave no operative file out, which search every file for it, and by Searches by meaning that together leave none out, which search only the files their places show ([`§ A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]`](#script-checks-1)). Of a design approved, applying or complete, it checks no research against the files | research shared among several cold agents is whole only as a union, so a gap between shares, in what they assessed or in the files their Searches reached, is found before a round reads the frame. Once the plan is approved the frame is frozen, and the files come to hold the apply's own writing, so research taken in from then on is held as the report of the round taking it in is validated, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it held |
| Out of Scope | each item of its Out of Scope citing a steer of its Steering Decisions whose Changes holds `Out of Scope item`, read only of the design the review runs on | an item no steer approves is one the user never made the call on |

Whether the design's citations of other files resolve, and its Target against its Kind, are the adversarial review's to judge. Whether a step Objective serves its goals and states an outcome, and whether the steps uphold a Frame Outcome, are the semantic checks standing under [`§ Design Plan Step § Step Objective`](#step-objective) and [`§ A Design Document § Frame Outcome`](#frame-outcome). The design's place in the workstack is `--check-workstack`'s, which runs before each validation. A problem it reports of the design is put right before the design goes to a review or to the approval. A problem it reports of another design is left to that design's builder, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has no builder write a design it is not working.

The validation review reports each problem it finds. The builder fixes in place each problem whose fix keeps what the plan decides, and the review runs again, until the document passes. A problem whose fix changes the plan, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts`](/specs/methodology/design-workflow/order-of-a-designs-work.md#facts) has such a fix, ends the validation instead. The design goes back to its revision with that change still to make, never on to the user's approval, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Work of a Design`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-work-of-a-design) has validating end. On the way to the user's approval, the passing review stamps it ([`§ A Stamp`](#a-stamp)). Before an adversarial round, it stamps nothing. Every problem it can report is one of form or integrity, so none is a question for the user. A stamp never waits on what the document says. The stamp is the review's record in the design. A design changed after its stamp no longer matches the stamp, so a stale validation is read from the file and never cleared by hand. The review runs again.

### Spawning a Change of Its Own

Spawning keeps a design focused, and fixing what stands on its path keeps work from piling up behind it. A design may turn up a problem it did not cause. The design's own breach is never such a problem. That includes an older breach of the canon's rules in text the design's steps rewrite, since the design writes that text. [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) decides the design's own breach before the plan's approval, and [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is`](/specs/AGENTS.md#whose-a-finding-is) with [`§ A Design Document § Changes After Approval`](#changes-after-approval) decide it after. A problem the design did not cause is on the design's path where it stands in a place the design's steps change and breaks no rule of the canon, such as a case the text misses or a decision gone wrong that the rewrite carries over. It is on the path too where it keeps one of the design's goals from being delivered. Work no goal reaches is a change of its own. A migration of files a rule change leaves out of sync is one, and so is a line of fixes the user hands on at a tertiary finding or place.

The builder recommends a route for each such problem, and the user decides it, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) has a call brought. The questions mean these:
- **Tertiary?** Whether it is a tertiary finding, or a change reaching a tertiary place ([`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage)).
- **Kept by the Out of Scope?** Whether an item of the design's Out of Scope keeps it, a known problem left no worse or a stage of a goal handed on, whichever check reports it.
- **Off any path by its kind?** Whether it is work of another kind, as [`§ A Design Document § A Change Needing Both Kinds`](#a-change-needing-both-kinds) splits it, or work in another product module ([`§ A Design Document § A Design Changing Code § One Product Module`](#one-product-module)).
- **Keeps a goal from being delivered?** Whether one of the design's goals cannot be delivered while it stands.
- **In a place the steps change?** Whether it stands in the text the design's steps rewrite: a unit their change is written whole in, as [`specs/AGENTS.md § Constitutional Principles § Revise, Never Patch`](/specs/AGENTS.md#revise-never-patch) has a unit, never all that a heading a step's What cites holds.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Tertiary?, Kept by the Out of Scope?, Off any path by its kind?, Keeps a goal from being delivered?, In a place the steps change?

| Tertiary? | Kept by the Out of Scope? | Off any path by its kind? | Keeps a goal from being delivered? | In a place the steps change? | The Builder Recommends |
|---|---|---|---|---|---|
| true | - | - | - | - | the call the tertiary stop brings, with the options [`§ A Check's Report § Settlement § User Decisions`](#user-decisions) marks as a Tertiary Option |
| false | true | - | - | - | nothing: it is recorded against the item keeping it, or where the item hands its stage on |
| false | false | true | - | - | spawning a design or logging a follow-up, whichever suits how the user means to work it |
| false | false | false | true | - | fixing it by the steps: the frame names it, the steps remove it, and the goal is unchanged; once the plan is approved, the design is sent back for it |
| false | false | false | false | true | widening the goals to take it in, by the route any steer changing the goals takes, the problem joining the design's Problem |
| - | - | - | - | - | spawning a design or logging a follow-up, whichever suits how the user means to work it |

The builder fixes the problems on the path in dependency order. The user may choose another route in every case. A goal's blocker the design cannot remove now may be staged: an Out of Scope item hands a stage of the goal on, to a design or a follow-up. Before the plan's approval, any other problem may be left in the Out of Scope as a known problem the design leaves no worse. After the approval, a problem the user leaves is ignored, as [`§ A Design Document § Changes After Approval`](#changes-after-approval) has it. Work that changes only working files is logged as a follow-up, never spawned, since no design changes a working file ([`§ The Working Files`](#the-working-files)). The user approves each spawned design before it is written, with its text shown first, and each follow-up as [`§ A Follow-up`](#a-follow-up) has it. Nothing is spawned, logged or taken in on the builder's own call, so a migration of specs or code to a new rule or standard is always the user's deliberate choice. Work is spawned or logged when it is deferred, not when the design completes. A spawned design's Spawned By names the design it came from, so each design, and each review of it, holds one change. The design's research still reaches what the spawned change touches, and only the spawned design's steps change it.

### What Blocks What

A design's Depends On Designs is the one record of what blocks what. It names each design that must finish before the design naming it is worked past its frame, spawned or not, as an application design names the canon design whose rule it follows. A spawned design is named in the Depends On Designs of the design it came from where that design cannot finish without it. A spawned design that can be worked before or after the design it came from is not named there. A workstack is worked from the designs nothing blocks, back toward the design it began from.

**What a name means.** A name in a design's Depends On Designs is read from the plans folders as they stand, each time it is read, and never from an event having reached the design naming it. The working files are plain files. The user may move or delete any design at any time, and nothing done as one design finishes can be counted on to reach every design naming it. A plans folder is a skill's plans directory, as [`§ The Working Files`](#the-working-files) has one, and a design stands in it where its file sits directly in that directory. A design document standing anywhere else, in an `archive/` beneath a plans folder among them, is no design of the workstack: no action of the design script reads it as one, and none writes it. What a name means is decided by its answers to the questions:
- **Stands in a plans folder?** Whether a design of that name stands in a plans folder as the name is read.
- **The named design's Status.** The Status of the design so standing, a state of [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Stands in a plans folder?, The named design's Status \
**Input Values:**
  - The named design's Status: "not-started", "in-progress", "approved", "applying", "complete", "abandoned"

| Stands in a plans folder? | The named design's Status | The Name |
|---|---|---|
| true | "not-started", "in-progress", "approved", "applying" | names an unfinished design, which blocks the design naming it |
| true | "complete", "abandoned" | names a finished design, so the foundation of the design naming it has changed |
| false | - | names a gone design, so the foundation of the design naming it has changed |

A gone design is one moved to an `archive/` or elsewhere, deleted, or never there under that name. A name means what the table gives it wherever it is read, however and whenever the named design came to stand as it does. A name that a complete or an abandoned design holds is that design's history: no check reports it, and nothing follows from it.

**A blocked design.** A design is blocked while its Depends On Designs names an unfinished design. No agent takes a blocked design past its framing, the framing state of [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Work of a Design`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-work-of-a-design). Its goals and its frame are agreed, which shows how the designs fit together, and then it waits. A blocked design may still be found past its framing, having come to name the design after its frame was agreed, or having been worked under the earlier rules. Its work then stops, and it goes to waiting. Every transition of a design's Status, of its work and of its apply follows from the rule. Work past a design's framing begins only once it names no unfinished design. It takes no step back: the user reshapes it by steers at its framing, or abandons it. A design is applied only once its Depends On Designs names none, so designs apply in dependency order.

A design that comes to name an unfinished design after its frame is agreed stops where its work stands and goes to waiting, by the route the machine governing it gives. [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Work of a Design`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-work-of-a-design) routes a design in progress, a round already handed back being settled first. [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) routes an approved design, which goes back to in-progress. [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) routes an applying design, which is sent back, its changes kept as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) keeps a send-back's.

The design script holds a blocked design to its frame, deciding each entry by what the entry does. Its `--log-entry` refuses each entry that begins or continues work past the frame: a `plan-change`, a `design-refactor-refine`, a `self-review`, an `another-round`, a `plan-approval`, a `step-back` or an `apply` entry. It appends every other entry. A check's entry ends work already begun, its report handed back before the design came to name the unfinished design, so every check that handed back a report has its entry, as [`§ Design Log Entry § When an Entry Is Appended`](#when-an-entry-is-appended) has it. Each other entry records a move of the design's Status, the user's word, or the work of its goals and its frame. The script's `--check-workstack` reports an approved or applying design naming an unfinished one.

**A changed foundation.** A design whose Depends On Designs names a finished or gone design waits to be freed. What it was framed against has changed: a finished design's apply wrote the files, or the design it waited on was dropped or is no longer there. Its builder frees it as it next works it, before any other act on it, as [`§ A Design Document § What Blocks What § Freeing a Design`](#freeing-a-design) has a design freed. Until it is freed, the design script's `--log-entry` appends no entry to its log, so no work goes on over a changed foundation, and the script's `--show-workstack` shows the design as waiting to be freed. A named design that a design reassessment makes afresh, without its finishing, changes nothing in the design naming it. That design holds only its goals and its frame, and is reassessed as the named design finishes.

**One design written.** No action of the design script writes a design document other than the one it is run on. So a design's finishing writes nothing in the designs naming it, and no builder releases, moves back or otherwise writes a design it is not working.

**A finished design.** A design finishes as its Status enters complete or abandoned ([`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through)). No design reads a finished design for anything but its Status. So no rule keeps a finished design for the designs naming it: it may be deleted or moved at any time, and `--show-workstack` says so of each. When a design is abandoned, each open design it spawned goes on as a design of its own, or is abandoned with it, as the user decides. A Spawned By naming a design since deleted stays, as the spawned design's history.

#### Freeing a Design

A design is freed by an act made on that design alone, before any other act on it, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-order-of-a-designs-work) has the freeing come first. Two actions of the design script make it. Its `--check-design-names` reports each of the design's own names that is finished or gone, and which of the two, and writes nothing, so a misspelled name is seen before anything is written. Its `--free-design` then frees the design. What the freeing writes is decided by its answers to the questions:
- **The design's Status.** The Status of the design being freed, as it is freed.
- **Goals agreed?** Whether the user's agreement to the design's goals stands in its log in its current major version, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts [Name: goals agreed?]`](/specs/methodology/design-workflow/order-of-a-designs-work.md#facts) has it.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** The design's Status, Goals agreed? \
**Input Values:**
  - The design's Status: "not-started", "in-progress", "approved", "applying", "complete", "abandoned"

| The design's Status | Goals agreed? | The Freeing |
|---|---|---|
| "complete", "abandoned" | - | writes nothing |
| - | false | removes each name of a finished or gone design from the design's Depends On Designs, and appends no entry |
| "not-started", "in-progress" | true | removes each name of a finished or gone design from the design's Depends On Designs, and appends the `design-reassessment` entry |
| "approved", "applying" | true | removes each name of a finished or gone design from the design's Depends On Designs, appends the `design-reassessment` entry, moves the design's Status to in-progress, and appends the `entered` entry of that move |

A design freed with its goals agreed is reassessed. Its `design-reassessment` entry holds its Cause, a changed foundation with each design it was freed from, as [`§ Design Log Entry`](#design-log-entry) has the Cause written, and starts a major version ([`§ A Design Document § The Design's Version`](#the-designs-version)). The design reassessment is made with no step back and no diagnosis, since no flaw of the design caused it. In every other way it is made as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a design made afresh: its work begins at framing, its goals are agreed again, its research is made afresh, and no earlier report binds it. An applying design so freed has its apply end as a send-back ends, its uncommitted changes kept as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) keeps a send-back's. Each check of the design whose settling has not ended as it is freed is cut short, as [`§ A Check's Report § Check Ending`](#check-ending) has it. A design freed before its goals are agreed takes no major version, and its work goes on from its Problem.

#### A Design Written Under the Earlier Rules

Designs written under the earlier dependency rules stand in the plans folders. Nothing writes one before its own builder next works it, as [`§ The Working Files`](#the-working-files) has a working file brought to the form in force. Until then, each state those rules left a design in has one reading:

**Reference Key:** State The Earlier Rules Left \
**Required:** Reported By, Reading

| State The Earlier Rules Left | Reported By | Reading |
|---|---|---|
| its Scope holds a Reliance | `--check-design-form`, naming each design a Reliance names that its Depends On Designs does not | its builder brings it to the form in force as it next works it: each design a Reliance names is written into its Depends On Designs where it is not there, and the Reliances are removed |
| it is approved or applying while its Depends On Designs names an unfinished design | `--check-workstack` | its builder moves it back to in-progress as it next works it, an applying one sent back, and it then waits at its agreed goals and frame |
| its steps were drafted or reviewed while its Depends On Designs names an unfinished design | no check | nothing is wrong with it as it stands: its work goes no further, and `--log-entry` refuses each further entry of that work |
| its log holds an `entered` entry whose Reason is a dependency's finishing or its move back | no check | the entry stands as it was written, read under the values it was written with, and the design script appends no such entry |

Once a design holds the form in force, its Depends On Designs alone decides it, as that field decides every design. A name of an unfinished design has it wait at its frame. A name of a finished or gone design has it freed and, its goals agreed, reassessed. So a design the earlier rules held to revise, for a finished design they had removed from its Depends On Designs, names that design again once its Reliance becomes a name, and is reassessed.

### A Form the Methodology Is Still Adding

A design changing the methodology may add a form, such as a part of a design document or a record type. While it is designed and reviewed, its own record keeps the forms in force, as [`§ The Working Files`](#the-working-files) has a design's own working files keep them. So the validation review checks it as it checks any design, and no design is validated by hand. It takes the form as its apply lands it. Another design whose record would use that form names the design adding it in its Depends On Designs, and takes the form once that design's apply lands it.

#### A Design Changing the Process

A design changing how the work is done runs under the process rules it writes. Before the apply, it is reviewed and settled by those rules wherever they differ from the rules in force. They reach its adversarial review's criteria, the marks, the runs and convergence among them, and the reviewer reads them from the design's steps. Only its record's form waits for the apply: its working files keep the form in force and meet each rule in force that the design script checks, as [`§ The Working Files`](#the-working-files) has them keep it. At the apply, each rule holds once its text is written, and the design's own working files take the forms it lands. So the post-apply review and the audit are settled by the rules the apply wrote, and the rules are tried on the design that writes them before they land. A self-hosting compiler is built the same way, with the syntax it adds.

### A Change Needing Both Kinds

A change needing both kinds is split. The change's canon design researches the application specs for what the change leaves out of sync there. It holds each application area so found in its Impact on the Application Specs, and edits none of the application specs. That application work goes to the application design the canon design was spawned from, where there is one. Otherwise it is spawned or logged as [`§ A Design Document § Spawning a Change of Its Own`](#spawning-a-change-of-its-own) has it. An application design naming the canon design in its Depends On Designs waits at its frame until the canon design finishes, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has a blocked design wait. A design changing the specs that leaves code out of sync edits none of the code either. It records the code it leaves out of sync in its Out of Scope, and that work goes to a design changing code, spawned or logged the same way. What the post-apply review or the audit in the canon design's apply finds in the application specs is settled by [`§ A Design Document § Changes After Approval`](#changes-after-approval). What that table hands on is application work too. It is held in the Impact on the Application Specs and handed on the same way, so the canon design completes without editing the application specs. Where the application work finds the canon design wrong, the canon design takes the change while it is in-progress or approved, the user reopening an approved one. For any other canon change the application work needs, the application design spawns a canon design, which blocks it. A change to the canon design once that design is applying or complete is such a change too. An approved application design so blocked goes back to in-progress and waits, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has a design that comes to name an unfinished design wait. An application design already applying keeps to what was approved. The canon change is then spawned or logged without blocking it, as the user decides.

### Applying and Committing

A design's apply begins only as [`§ A Design Document § The States It Moves Through`](#the-states-it-moves-through) lets the design move into applying. The user's approval of the plan authorizes the builder to write within the design's Target, no edit asking its own approval: to edit each file the Target names, and to create under each directory it names the files and folders the steps' Objectives need, though no part of the plan names them, never to edit a file already standing there that the Target does not name. A design's changes are:
- the writing its steps reach, within its Target;
- each direct edit a `direct-edit` entry of its log names, in a file the Target could name by its Kind;
- each edit of the user's a `user-edit` entry names, wherever it lies outside a working file, since the user confirmed it intended ([`§ Design Log Entry`](#design-log-entry), [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart)).

A design's changes are read one way, wherever a rule reads which files a design changed. With version control, they are the files changed against the last commit, the files created among them, read once the writing has kept or removed each uncommitted change, as [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) has it, so the diff holds the design's changes alone. With none, they are the files the Target names, each file the builder names as created under a Target directory, and the places the design's `direct-edit` and `user-edit` entries name. A script, which cannot know what the builder created, reads a Target directory in place of the files created under it. What a rule reads within those files, a diff, a whole file or what a file held before the apply, stays that rule's own.

Every change the design makes is one of them. The design's changes are committed on their own, one commit for each design even where a branch holds several, so a revert takes exactly that design's changes, and the commit's message names each direct edit and each edit of the user's among them. [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) sets what becomes of them, and of every other change uncommitted in the project the design is worked in, at each event: a send-back, entering applying, the writing, the commit and an abandonment. An abandonment reverts through version control or, where the project has none, by hand.

### The Kinds of Change

What each kind bounds a change to:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind

| Kind | Bounds the change to |
|---|---|
| `canon-specs` | [`specs/AGENTS.md`](/specs/AGENTS.md), the main file of `specs/`, [`specs/architecture.md`](/specs/architecture.md), the files under `specs/methodology/`, a registered skill's directory, `.ai/skills/lib/`, and `tests/spec-of-record/` |
| `application-specs` | the files under `specs/application/` |
| `code` | the application's code, within the code roots the technical stack names ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack)), which the application specs govern ([`specs/methodology/code.md`](/specs/methodology/code.md)); a design changing code's only kind |
| `documentation` | the documentation, `README.md` and the files under `docs/` |
| `other` | any other file, the project's root `AGENTS.md` and its helper scripts among them, but no working file, which is of no kind ([`§ The Working Files`](#the-working-files)) |

Every file or directory a design's Target names is of its declared kind, or is a file of `documentation` or `other`, or is code whose annotation lines alone it edits, as [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code) has a design retitling a heading.

### Frame Part

A Frame Part is a named part of a design frame: a case of its Scope, a principle of its Approach or one of its Frame Outcomes. Each names the goals it rests on in its record, rather than citing them inside its sentences, so a change to a goal finds each part to re-evaluate, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) has a change rebuild what names what it changed. A part states what the design changes, and cites the canon's home for each rule it relies on and leaves as it is, as [`§ A Design Document`](#a-design-document) has the plan cite it. Each kind of part is a record type of its own extending this one, adding the Description its kind holds, so a field naming a part of one kind, such as a step Objective's Upholds Frame Outcomes, takes no part of another. A Frame Part is always a case, a principle or a Frame Outcome, so this type holds no records of its own:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Frame Parts \
**Modifier:** Abstract \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the part's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which a field names it |
| Goals | no | yes | | text | the goals it rests on, a list, one goal's Name to an item, as [`§ Design Goal`](#design-goal) has a field name a goal |

### Scope Case

A case the change governs, one of the cases of a design frame's Scope ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)). Its records sit in the Scope's Cases field ([`§ A Design Document`](#a-design-document)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ A Design Document § Frame Part` \
**Plural Name:** Scope Cases

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Description | no | yes | | text | the case the change governs, and what tells it apart from the others |

### Assessed Area

A design holds its current scope in its frame's Assessed Areas, so an agent taking the design up finds there what the agent before it put in scope and what the design follows. Each is an area research found bearing on the design ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), and holds the Impact and the report of the latest Read Assessment of its Area ([`§ A Check's Report § Read Assessment`](#read-assessment)). Nothing enters the design's scope but through such an assessment. A step's What names only areas whose Impact holds `changes`, as [`§ Design Plan Step § What a Step Rests On`](#what-a-step-rests-on) has a What name them, and the design follows each whose Impact holds `applies`. An area whose latest Read Assessment holds `changes` that the design leaves out is named in its Out of Scope instead. An area of the application specs in a canon design whose latest Read Assessment holds `changes` is held in its Impact on the Application Specs, and nowhere else, since a canon design edits none of the application specs ([`§ A Design Document § A Change Needing Both Kinds`](#a-change-needing-both-kinds)). As a newer assessment of an Area comes in, its Assessed Area takes that assessment's Impact and report, and the earlier reports stay as the history. Only research binding the design stands, as [`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record) has a report bind, so research cut short gives no Assessed Area its assessment, and a design reassessment starting a major version has the Assessed Areas rebuilt from research made afresh ([`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research)). The validation review holds the Assessed Areas to the research and to the steps, as [`§ A Design Document § The Record's Checks`](#the-records-checks)'s Lineage check has it.

A design's Assessed Areas sit in its frame's record section of this type, after its Scope, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Assessed Areas \
**Reference Key:** Area

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Area | yes | yes | | text | the area, a file or a section, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Impact | no | yes | | text | a list, the Impact of the latest Read Assessment of its Area, each item a member of [`§ A Check's Report § Read Assessment § Read Assessment Impacts`](#read-assessment-impacts) other than `none` |
| Assessment | no | yes | | text | the report of the handed-off judgment holding that Read Assessment, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |

### Approach Principle

A principle the solution applies, one of the principles of a design frame's Approach ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)). Its records sit in the Approach's Principles field ([`§ A Design Document`](#a-design-document)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ A Design Document § Frame Part` \
**Plural Name:** Approach Principles

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Description | no | yes | | text | the principle the solution applies |

### Frame Outcome

A Frame Outcome is one of a design frame's outcomes ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)): what a successful solution achieves, stated of the applied work and never of the plan, and how that is judged. So a reviewer judges it against the steps before the apply, and against the applied work after it. It names the goals it rests on, as [`§ A Design Document § Frame Part`](#frame-part) has it. The step Objectives naming it in their Upholds Frame Outcomes uphold it ([`§ Design Plan Step § Step Objective`](#step-objective)).

A design's Frame Outcomes sit in its frame's record section of this type, after its Approach:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ A Design Document § Frame Part` \
**Plural Name:** Frame Outcomes

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Description | no | yes | | text | what the applied work achieves, and how that is judged |

#### Semantic Checks

**Records:**
  - **Name:** outcome-upheld \
    **Tests:** a Frame Outcome's Description states what the applied work achieves and how that is judged, and the step Objectives naming it in their Upholds Frame Outcomes together achieve that, judged as it says, in the steps before the apply and in the applied work after it, as this section has a Frame Outcome upheld \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/design-specs/` Check what you wrote, then the post-apply review, the audit and the commit
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews
      - `.ai/skills/implement-specs/` Check what you wrote, then the post-apply review, the audit and the commit

    **Unit:** per Frame Outcome

### Changes After Approval

Once the user approves the plan, a passage outside the Target that the apply leaves false is a tactical fix ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) where a rewording that restates what the steps decide makes it true. Otherwise it is a finding lying in the plan, as [`§ A Design Document § Applying and Committing`](#applying-and-committing) bounds a design's changes. A finding the post-apply review makes is placed as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) places one. This section's table settles each of these as it settles an audit's finding:
- a post-apply review's finding outside the Target;
- a post-apply review's finding placed as handed on;
- each finding the builder's self-review makes over the work and does not fix where it is made, in the writing or in a pass proving the fixes.

The builder triages and marks an audit's findings, as [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) has an audit read. Before this section's table, the builder applies [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) to each finding the table would settle, recording each kept finding's two indicators, and what requires each finding the test drops, as [`§ A Check's Report § Settlement`](#settlement) has them. It records each finding the test drops in its triage. It orders each finding, and each place a fix it makes changes, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) has them ordered, bringing the user a tertiary finding's call before any fix is made there. Each finding the test keeps is presented to the user and settled by the questions that sort it, asked in order:
- **Caused by the design?** The builder's triage answers it, and a post-apply review's finding outside the Target is triaged as an audit's is, by the one test [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is`](/specs/AGENTS.md#whose-a-finding-is) states, which also gives what holds the files as they stood, with or without version control.
- **On the design's path?** Whether a finding the design did not cause stands on the design's path, as [`§ A Design Document § Spawning a Change of Its Own`](#spawning-a-change-of-its-own) has a path.
- **Judged wrong by the user?** The user's judgment as the finding is presented.
- **In a file the design's Kind lets it change?** A canon design's finding in the application specs, and a code design's in the specs, answer false.
- **Handed on by the frame?** A rule the design changed may find a breach in text the apply carried over. That finding answers true where the design's Out of Scope hands the text's migration on, to a design of its own or a follow-up, as [`§ A Design Document § Spawning a Change of Its Own`](#spawning-a-change-of-its-own) has such work handed on. It answers false where the goals take the migration in, since the migration is then the steps'. It answers false too where the frame hands nothing on, having missed text it should have held. A script check's finding and a semantic check's are answered alike.
- **A tactical fix?** True for a tactical fix as the glossary defines one ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), the meaning and the logic it keeps being those the plan states. Every nit answers true but one asking to reword or rename wording or a name a step Objective quotes as the user chose it. That finding answers false whatever its mark, since that wording or name is the outcome itself ([`§ Design Plan Step § Step Objective`](#step-objective)). Rewording or renaming any other text the work holds while keeping its meaning answers true, a file or folder the apply created renamed at the user's review among it, its new name still its subject area's term for what it holds ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)). A fix answering false changes the plan, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) has a fix change it, so it lies in the plan.

So a tactical fix never sends a design back, every other fix does, no design edits a file its Kind does not let it change, and no migration the frame hands on is made in the design:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Caused by the design?, On the design's path?, Judged wrong by the user?, In a file the design's Kind lets it change?, Handed on by the frame?, A tactical fix?

| Caused by the design? | On the design's path? | Judged wrong by the user? | In a file the design's Kind lets it change? | Handed on by the frame? | A tactical fix? | Settles |
|---|---|---|---|---|---|---|
| false | true | - | - | - | - | settled by the route [`§ A Design Document § Spawning a Change of Its Own`](#spawning-a-change-of-its-own) recommends, a fix in the design sending it back to in-progress with its changes kept, or as the user chooses instead: ignored; given a design spawned for it; or logged as a follow-up; each recorded in the builder's triage |
| false | false | - | - | - | - | settled as the user chooses, and recorded in the builder's triage: ignored; given a design spawned for it; or logged as a follow-up ([`§ A Follow-up`](#a-follow-up)) |
| true | - | true | - | - | - | set aside, and recorded in the builder's triage with the reason |
| true | - | false | false | - | - | handed on as work of another kind, as [`§ A Design Document § A Change Needing Both Kinds`](#a-change-needing-both-kinds) has it |
| true | - | false | true | true | - | recorded in the builder's triage against the design or follow-up the Out of Scope hands the migration to |
| true | - | false | true | false | true | made in place, as [`§ A Design Document § Changes After Approval § A Tactical Fix After the Apply`](#a-tactical-fix-after-the-apply) has it, each nit settled as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit`](/specs/AGENTS.md#a-nit) settles it |
| true | - | false | true | false | false | sends the design back to in-progress, its changes kept, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has one |

#### A Tactical Fix After the Apply

After the apply, the builder makes a tactical fix in place, as one of the design's changes. It makes the fix whatever its size, at every place its defect stands. It makes it whichever check or feedback brings it: a post-apply round's finding, an audit's, or the user's feedback on the applied result. A fix made outside the Target is logged as [`specs/AGENTS.md § Design, Refactor, Refine § Direct Edits`](/specs/AGENTS.md#direct-edits) has an edit outside the Target logged. The builder proves the fixes by the passes [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) runs in proving the fixes. The user is shown those passes as [`specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown`](/specs/AGENTS.md#what-the-user-is-shown) has them shown. The user approves a fix with what the user next approves. Each nit is fixed or left as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit`](/specs/AGENTS.md#a-nit) settles it.

### Uncommitted Changes

What becomes of each uncommitted change in a design's project, at each event of the design's work, by what the change is, sorted by its answers to the questions:
- **Written by the builder?** Whether the builder wrote the change, in this apply or in one a send-back kept.
- **Reached by a step?** Whether a step of the plan as it now stands reaches it, the steps' writing within the Target: a file the steps' Objectives need, created under a Target directory, among it, and an edit of a file standing under that directory that the Target does not name never.
- **Logged?** Whether a `direct-edit` or a `user-edit` entry names it ([`§ Design Log Entry`](#design-log-entry)).

So the steps' writing, a logged direct edit and a logged user's edit are the design's changes, as [`§ A Design Document § Applying and Committing`](#applying-and-committing) has them. The builder's writing that no step reaches and no entry logs is none of them. At the writing state, the builder removes it, so none of it is left at the commit. A change the builder did not write that no entry logs is confirmed with the user, as [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart) has an edit of the user's confirmed:

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
**Reads:**
  - blocked?: [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts [Name: blocked?]`](/specs/methodology/design-workflow/order-of-a-designs-work.md#facts)

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| not-started | recorded, often by the design that spawned it, and not yet worked | Yes | No |
| in-progress | its work under way, governed by [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Work of a Design`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-work-of-a-design) | No | No |
| approved | validated and its plan approved by the user, its adversarial review converged or ended by that approval, and not yet applied, awaiting the go-ahead to apply | No | No |
| applying | its apply under way, governed by [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) | No | No |
| complete | applied, each audit it must run settled or bypassed on the user's word; what it decided lives on in the specs it changed | No | Yes |
| abandoned | withdrawn by the user | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| not-started | in-progress | the work is taken up | none |
| in-progress | approved | none | none |
| approved | in-progress | the user reopens it | none |
| approved | in-progress | when blocked? | none |
| approved | in-progress | the design is freed | none |
| approved | in-progress | the user asks to step back | not(blocked?) |
| approved | applying | the user gives the go-ahead to apply | its Depends On Designs names none, [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) admits every uncommitted change, and no other design is applying in the project |
| applying | in-progress | none | exit = "sent back" |
| applying | in-progress | the user asks to step back | not(blocked?) |
| applying | in-progress | the design is freed | none |
| applying | complete | none | exit = "applied" |
| not-started | abandoned | the user abandons it | none |
| in-progress | abandoned | the user abandons it | none |
| approved | abandoned | the user abandons it | none |
| applying | abandoned | the user abandons it | none |

A design's plan is written against the files as they stood before its apply, and while the design is applying the files as they stand hold the apply's writing. So a reading of the plan's citations made then reads the durable files as the last commit held them, as [`§ Design Plan Step § Step Objective`](#step-objective) has a design cite the files, and the validation review checks no research against the files, as [`§ A Design Document § The Record's Checks`](#the-records-checks) has it. The applied work is read as the files stand.

#### A Send-back

A design sent back, from applying by its apply or from approved or applying to step back, goes back to in-progress with the changes [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) keeps in place at a send-back, never set aside or reverted, since they are the plan's work with flaws to rework, not work to undo. A change the builder did not write that no entry logs is confirmed with the user first, as that section has it. These, with each edit of the user's a `user-edit` entry logs since, are the changes a send-back kept, and that section says what becomes of them at each later event. Its steps are revised against the last commit, as any design's are. The kept changes are its apply's unfinished writing, never a baseline: as the design applies again, the builder, at the writing state, keeps what the revised steps reach and removes only what is none of the design's changes, so the post-apply review finds nothing outside them. While kept changes stand in a project, every reading for a design in it, a review's, the builder's self-review and another design's among them, reads the files at the last commit wherever it would otherwise read the files as they stand, a working file, which no commit holds, alone read as it stands. It reads the kept changes as the apply's unfinished writing, from their diff against that commit.

A design is sent back only once the check sending it is settled and its passes have ended, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) has a check run. It carries only what the kept changes do not hold, each taken into its rebuilt goals, frame or steps. Where each finding the check left unresolved goes is sorted by its answers to the questions:
- **Its fix changes the plan?** Answered as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) answers it.
- **In text the rework replaces?** Whether the finding stands in text a change sending the design back reworks.
- **A flaw?** Whether it is marked a design flaw or an implementation flaw.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Its fix changes the plan?, In text the rework replaces?, A flaw?

| Its fix changes the plan? | In text the rework replaces? | A flaw? | Goes |
|---|---|---|---|
| true | - | - | carried into the rebuilt goals, frame or steps, its Settlement giving Lies In `the plan` |
| false | true | false | with the text, carried by nothing |
| false | true | true | carried as an outcome of the step reworking the text, unless that step's Objectives already state it, its Settlement naming that step in its Carried By |
| false | false | - | with the kept changes, read from the report binding while they stand ([`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record)), and fixed in the reapply's writing |

A fix in text the rework replaces is not made, since the rework replaces the text. A finding no pass resolved in text the rework keeps holds to what the plan decides, so it stays with the kept changes. Each fix the builder made stays one of the design's changes through the reapply, so its writing keeps it and the design's commit holds it.

The kept changes occupy the project as an apply's changes do. The design enters applying again as [`§ A Design Document § Uncommitted Changes`](#uncommitted-changes) admits, and no other design applies in that project, so each commit holds one design's changes. A design that must apply while they stand, such as a dependency the sent-back design gains, applies in the same project on a branch of its own, made as [`specs/AGENTS.md § Design, Refactor, Refine § A New Branch`](/specs/AGENTS.md#a-new-branch) has a new branch made. The kept changes are stashed meanwhile, so nothing is uncommitted as it enters applying. They are restored as the sent-back design applies again, its writing reconciling them with that design's commit. The working files, untracked, stay in place for both. An abandonment of the sent-back design while they are stashed restores them first, so the rows for an abandonment act on them. Where the project has no version control, nothing is stashed, so a sent-back design takes on no dependency its kept changes would block: the change it needs joins its own steps, or the design is abandoned.

### A Design Changing Code

A design changing code starts from applied specs, rather than from a problem in them. Where a design has yet to apply the specs it carries out, it names that design in its Depends On Designs, has its goals and its frame agreed, and waits until that design finishes, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has a blocked design wait. It designs the code and the tests that bring the specs to life. It takes the form [`§ A Design Document`](#a-design-document) sets, the Design, Refactor, Refine process, the validation review, the adversarial review, the stamp and the post-apply review, as a design changing the specs does. It differs only where code does. Its parts differ so:

**Reference Key:** Part \
**Required:** In A Design Changing Code

| Part | In A Design Changing Code |
|---|---|
| The Problem | what the code of the product module it carries out lacks, the harm, citing the specs it carries into code as the evidence, and nothing more, as [`§ A Design Document`](#a-design-document) has the Problem hold |
| Kind | `code` |
| Design Plan Steps | its steps' Objectives state, by their meaning, what the applied code does for the specs it carries out and what its tests check, as [`§ Design Plan Step § Step Objective`](#step-objective) has an Objective state an outcome. The builder writes at the apply the units of governed code, the app-spec annotations each carries ([`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code)), the wiring that connects the units ([`specs/methodology/code.md § Governed Code and Wiring Code`](/specs/methodology/code.md#governed-code-and-wiring-code)) and the tests that check the specs ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)), as a design changing the specs writes its constructs there |

The audit in its apply is the one [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews) has a design run, `.ai/skills/verify-spec-implementation/`'s full run for its code, beside a run over the sub-scopes the user settles, where the user settles any.

#### One Product Module

A design changing code carries out one product module. It reads what [`specs/methodology/spec-placement/product-module.md § A Product Module`](/specs/methodology/spec-placement/product-module.md#a-product-module) sets, in the order [`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure) sets. Work reaching several modules is a design for each. A technical section several modules need, such as a shared data model's, is carried out by the first design changing code that takes it up. A later design names that design in its Depends On Designs while that design is unfinished, and builds on that design's code once it is applied.

#### The Builder Designs, the User Steers

The builder designs the code from the specs on its own, with the specs as its starting point. The user approves the design or steers it. A steer about how the code carries out the specs is this design's. A steer changing what a spec states is spawned as a design changing the specs and named in this design's Depends On Designs. This design then waits on the spawned design, from whatever state its work stands in, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has a design that comes to name an unfinished design wait. Once the spawned design finishes, this design's builder frees this design as it next works it, and the design is reassessed against the specs as they then stand, as [`§ A Design Document § What Blocks What § Freeing a Design`](#freeing-a-design) has a design freed.

## Design Goal

A design's goals ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) are agreed on before its design frame, and changed and weighed, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has them. A goal is named, never numbered, so a record speaks of a goal by its Name however the list changes. A design's goals, the cases of its Scope and the principles of its Approach, its Frame Outcomes, steps and step Objectives each take a Name no other part of the design takes. A field naming any of them holds each by its Name alone, a list, one Name to an item, and the design script resolves each against the design. Prose cites a goal as a record is cited, by its record section and its Name ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation)).

A goal states the change the user needs. Another means of achieving that change would satisfy the same goal. A goal may name the mechanism whose result matters to the user. Its steps and operation belong to the design of the means. An outcome already achieved in full wherever Spec of Record governs states no change. An outcome achieved only in part, including one that the canon requires but the work does not deliver, still states a change.

A design's goals sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Goals \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the goal's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which a field names it and prose cites it |
| Description | no | yes | | text | what the goal asks of the change: an outcome removing a root cause of the harm the Problem states, written as this section has a goal written |

### Semantic Checks

**Records:**
  - **Name:** goal-states-an-outcome \
    **Tests:** each goal's Description states the change the user needs in terms that hold across different ways of achieving it, as this section has a goal written \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per goal

  - **Name:** goal-states-a-change \
    **Tests:** each goal's outcome is a change, something new, updated or removed, and fails where its outcome already holds in full wherever Spec of Record governs, as this section has a goal state a change \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per goal

## Design Plan Step

Each step of a design's plan states what it changes and, in its Objectives, the state the applied work holds once it is changed. The text or the code that brings the state about is written at the apply, from the Objectives ([`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply)). A step carries a Draft of that means where [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has one owed, worked out before the apply for its reviewers to read, which binds nothing ([`§ Design Plan Step § A Draft`](#a-draft)). A step reaches as many files as its change does. The design's Target names each standing file its steps reach, and each directory they create a file or folder under, so no step, Objective or Target names a file or folder the design creates ([`§ A Design Document`](#a-design-document)).

A design's steps sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Plan Steps \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the step's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which a field names it and the record cites it |
| What | no | yes | | text | what the step changes, each area it changes named as a place, as [`§ Design Plan Step § What a Step Rests On`](#what-a-step-rests-on) has a What name it |
| Why | no | yes | | text | why the step is needed |
| Depends On Steps | no | yes | | text | the steps it builds on, a list, one step's Name to an item, as [`§ Design Goal`](#design-goal) has a field name a step, or `none` |
| Draft | no | where [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has the step owe one | | text | the means its builder works out for the change its Objectives reach, fenced blocks, as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has a field's fenced blocks, and as [`§ Design Plan Step § A Draft`](#a-draft) has a Draft |
| Objectives | no | yes | | a list of [`§ Design Plan Step § Step Objective`](#step-objective) | the states the applied work holds once the step is applied |

### What a Step Rests On

A step's What names each area the step changes, as a place, and only areas the frame's Assessed Areas ([`§ A Design Document § Assessed Area`](#assessed-area)) hold with an Impact holding `changes`, never a place read only to confirm the builder's understanding. Within those areas, the step's change is written whole, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § A Rule Written Whole`](/specs/AGENTS.md#a-rule-written-whole) has a rule written whole. Its Why holds why the step is needed alone, and the step serves the goals its Objectives name. A step names the steps it builds on in its Depends On Steps, and stands after each of them, so the steps are read and built in the order they build on each other. Its Objectives state the outcomes it achieves, each written as [`§ Design Plan Step § Step Objective`](#step-objective) has an Objective written.

### Step Objective

A step Objective is an Objective ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)): it states the outcome its step achieves toward the goals it names, by its meaning, held to the rule that a goal states only an outcome and never the means ([`§ Design Goal`](#design-goal)), and for the same reason, but not to the rule that a goal's outcome is a change. It never states the work to reach the outcome, nor the means carrying it out. It holds no construct, no table, no row and no quoted wording, but wording or a name the user chose as the outcome itself, quoted as the steer gives it ([`§ Steering Decision § When a Steer Is Recorded`](#when-a-steer-is-recorded)), and never the name of a file or folder the design creates, which guides the apply without freezing it even where the builder and the user talked it over as the design was shaped. It names no place in a file: it says by its meaning what its outcome concerns. It cites the canon's home for each rule it relies on and leaves as it is, as [`§ A Design Document`](#a-design-document) has the plan cite it, and such a citation names no place its outcome is placed at. It fixes no name the apply writes, so text carrying the same outcome under another name meets it. Each citation in a design names a heading its reader finds in the files as the citation reads them. A Draft's construct cites the files as they will stand once the design's steps apply ([`§ Design Plan Step § A Draft`](#a-draft)). Every other part of a design cites the files as they stood before its apply. So it cites no heading its own apply or a dependency's has yet to write, and it goes on citing a heading its own apply removes or retitles. Until the design is applying, those are the files as they stand, or the last commit's while kept changes stand ([`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back)). While the design is applying, they are the durable files as the last commit held them, a working file, which no commit holds, read as it stands. Every reading of a design's citations reads them so, the design script's check of the headings a design cites among them, and none reports a heading the design's own apply removed or retitled.

An Objective states its outcome at the grain of what its step decides, never at the grain of the text carrying it. An Objective that one wording alone meets, wording or a name the user chose aside, or that lists the edits its step makes, the passages it rewrites, the sentences it keeps or the clauses it adds, is written too specifically: it is a second draft of the text, and it fails as an Objective stating a means fails. Within the areas its step's What names, each decision the step's Objectives leave unstated stands as it is, and only the text carrying it is the apply's to rewrite. So an Objective lists neither what stays in those areas nor how their text changes. The Objective the canon keeps for every step ([`§ A Design Document § The Standing Objective`](#the-standing-objective)) is never listed in the step.

The step's What names the places the step changes ([`§ Design Plan Step § What a Step Rests On`](#what-a-step-rests-on)). The builder writes the means at the apply, from the step, its Objectives and the Target as it stands: the text, the names it writes and each construct, whose form is chosen there by [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which). So a step's Objectives freeze the outcomes they state, never the text carrying them, whatever the design's kind, and a tactical fix ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), keeping each outcome, lies in the writing ([`§ A Design Document § Changes After Approval`](#changes-after-approval)).

A step's Objectives sit in its Objectives field, records of this type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Step Objectives \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the Objective's slug, in kebab-case as a design document's Name is ([`§ A Design Document`](#a-design-document)), by which a field names it |
| Goals | no | yes | | text | the goals the Objective serves, a list, one goal's Name to an item, as [`§ Design Goal`](#design-goal) has a field name a goal |
| Upholds Frame Outcomes | no | yes | | text | the Frame Outcomes the Objective upholds, a list, one Frame Outcome's Name to an item, as [`§ Design Goal`](#design-goal) has a field name one |
| State | no | yes | | text | the state the applied work holds once the step is applied, written as this section has an Objective's text written |

#### Semantic Checks

**Records:**
  - **Name:** objective-serves-its-goals \
    **Tests:** each step Objective's State achieves something each goal its Goals names asks of the change, as this section has an Objective state the outcome its step achieves toward the goals it names \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per step Objective

  - **Name:** objective-states-an-outcome \
    **Tests:** each step Objective states the outcome its step achieves, by its meaning, at the grain of what its step decides, and never how the step is implemented: it fails where other text carrying the same outcome, in other wording, under another name or in another form, would leave it unmet, wording or a name the user chose aside, and where it lists the edits its step makes, as this section has an Objective written too specifically \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per step Objective

### A Draft

A step's Draft is its builder's working of the means for the change its Objectives reach, worked out before the apply. It is barely above the scratch pad the builder already keeps, its design folder's `scratch/` ([`§ The Working Files`](#the-working-files)), placed in the design document only so the builder's own self-review and the adversarial reviewer can read it verbatim ([`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review)). Its fenced blocks are its value, standing beneath its key as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has a field's fenced blocks stand: a construct or text in a `markdown` block, and code in a block of its language. A step owes one in a design changing the specs and in one changing code alike, as [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has it. A Draft cites the canon's home for each rule it relies on and leaves as it is, as [`§ A Design Document`](#a-design-document) has the plan cite it, the construct its step changes, or the parts of it the Draft holds, aside. Its construct cites sections as the files will stand once the design's steps apply, a heading another of its Drafts creates among them, so a check stands under the section stating the rule it enforces, a new section among them, and the records citing it are drafted. The validation review resolves those citations against the specs as they stand and the design's Drafts ([`§ A Design Document § The Record's Checks`](#the-records-checks)).

To draft a change to a construct a file holds, the builder copies into the Draft what [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has the Draft hold of it: a logic construct whole, and of any other construct each part the step adds or changes. It copies them as the file holds them, read at the last commit while a send-back's or a design reassessment's changes are kept, or as an earlier step's Draft of the design leaves them. The builder makes the step's change in the copy, checks the change against the step's Objectives, and runs the design script's `--check-design`, whose checks read each Draft's constructs as [`§ A Design Document § The Record's Checks`](#the-records-checks) has them read, settling each problem it reports before any review reads the plan. A construct the step creates is drafted whole from nothing, and checked the same way.

A step's Draft binds the apply to nothing. The step's Objectives remain the outcomes the plan freezes ([`§ Design Plan Step § Step Objective`](#step-objective)), and the builder writes the means at the apply from them, whatever the Draft held. While the plan is not approved, a Draft is amended with its step as any part of the plan is, and validated and stamped with the plan ([`§ A Design Document § The Record's Checks`](#the-records-checks)). Once the apply begins, the Draft is history, and nothing is owed to it.

#### When a Draft Earns Its Place

A step creating or updating a construct a file holds, an instance of one of the canon's constructs, owes a Draft holding it as the step would leave it. A logic construct, as [`specs/methodology/modeling-constructs.md § When to Use Which § Logic Constructs`](/specs/methodology/modeling-constructs.md#logic-constructs) lists them, stands in the Draft whole, with the description opening its section and the facts it names, each copied with it or cited where it stands. Of any other construct, the Draft holds each part its step adds or changes, whole, with what the construct's checks read with it: a record section's records under its Records field, a Basic Table's rows under its header fields, and a record type's fields under its declaration's fields, with the field its Reference Key names. A step owes one too where a reviewer reading its Objectives alone cannot tell whether the means is right, as with a mechanism, a shape other checks or designs read, or an algorithm or a contract in code. A step whose Objectives leave its means in no doubt and that creates or updates no construct, as with prose the apply writes, carries none. Whether a step creates or updates a construct is told by the count [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which) sets, made as the step is drafted.

#### Semantic Checks

**Records:**
  - **Name:** draft-owed \
    **Tests:** each step that creates or updates a modeling construct carries a Draft of it, and each other step whose means its Objectives alone leave in doubt carries a Draft of that means, as [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has a Draft earn its place. What a Draft of a construct holds is [`§ Design Plan Step § A Draft § Semantic Checks [Name: construct-drafted-whole]`](#semantic-checks-4)'s to test \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per design plan step

  - **Name:** construct-drafted-whole \
    **Tests:** each logic construct a step creates or updates stands in the step's Draft whole, as the step would leave it, with the description opening its section and the facts it names, and each part a step adds to or changes in any other construct stands in the Draft whole, with what the construct's checks read with it, as [`§ Design Plan Step § A Draft § When a Draft Earns Its Place`](#when-a-draft-earns-its-place) has a Draft hold them; a finding names the construct and what of it the Draft leaves out \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` Refactor and refine, then the reviews and the approval
      - `.ai/skills/implement-specs/` Design, Refactor, Refine, then the reviews

    **Unit:** per design plan step

## Design Log Entry

A design's log records what happened in the design's work, an entry for each check of its work and each event of its workflow, so it shows the journey. The process drives the log's entries, and the log never drives the process. Each entry is appended as its event happens, and no rule places an entry before or after another so that a check can find it. The process reads earlier entries to decide which options are valid from where the work stands, as the design script's refusals, the version worked out from the log and the routing of the work read them. Entries are only appended: no entry's record of its event is edited, moved or inserted after it, and a change to the log's form reaches the log as it reaches every working file ([`§ The Working Files`](#the-working-files)). Since each entry stands where its event happened, the log's order is what happened, and a rule reads it as it reads any record.

This section declares the log's form alone: what an entry means to a check or a state is stated where that check or state is. An entry holds values alone. Each entry is appended through the design script of the skill writing the design, by its `--log-entry`. The script counts the entry among its kind and stamps it with the UTC time of appending, so the timestamps stand in the order the entries were appended, and a check holds the entries' order to them. It stamps each entry with the version of the design its work read ([`§ A Design Document § The Design's Version`](#the-designs-version)). A check's entry takes the version its report's Reading records, and the script refuses a version the log never held. An entry with no report takes the version as it is appended. So research handed off before a set of steers and handed back after it stands after the set's entry, at the version before the set. A round settled after a set stands at the version its reviewers read. A report whose Reading records no version, written before the Reading held one, is read at the version of the entry naming it.

A design's log sits in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Design Log Entries \
**Reference Key:** Entry

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Entry | yes | yes | | text | its kind, one of this section's kinds table, a hyphen and its count among its kind from 1, as `adversarial-review-2` |
| Timestamp | no | yes | | text | the UTC time it was appended, as [`§ A Stamp`](#a-stamp) writes a timestamp |
| Design Version | no | no | 0.1.0 | text | the version of the design its work read, written as [`§ A Design Document § The Design's Version`](#the-designs-version) has a version written |
| Model | no | where its kind gives it | | text | the model the check ran on |
| Effort | no | where its kind gives it | | "light", "medium", "high", "as the agent allows" | the reasoning effort the check ran at, one of the levels [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) names, or `as the agent allows` where the agent could not apply the level chosen, or where, for a builder's own check, no level it ran at is named |
| Design Flaws | no | where its kind gives it | | text | the count of design flaws the check found, a whole number |
| Implementation Flaws | no | where its kind gives it | | text | the count of implementation flaws the check found, a whole number |
| Nits | no | where its kind gives it | | text | the count of nits the check found, a whole number |
| Dropped | no | where its kind gives it | | text | the count of findings its report holds dropped, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) has a finding dropped and [`§ Design Log Entry § What a Check Counts`](#what-a-check-counts) has them counted, a whole number |
| Led To | no | where its kind gives it | | text | the state the work went into as the check's settling ended, whatever took it there |
| Settled Judgments | no | where its kind gives it | | text | the entry keys of the handed-off judgments settled with this review round ([`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round)), in numeric order, separated by semicolons, or `none` |
| Reason | no | where its kind gives it | | text | why the design entered in-progress, one of the values of [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts [Name: entry reason]`](/specs/methodology/design-workflow/order-of-a-designs-work.md#facts) |
| Approval | no | where its kind gives it | | "approved", "approved and apply" | the user's approval of the plan |
| Cause | no | where its kind gives it | | text | what caused the design reassessment, written in one of two forms. For a changed foundation it is `changed foundation:`, then each design the design was freed from, by the name its Depends On Designs held, followed by `finished` or `gone`, as [`§ A Design Document § What Blocks What`](#what-blocks-what) has a name of each read, separated by semicolons, as `changed foundation: {design} finished; {design} gone`. For one chosen at the step back it is `step back:`, then what brought the design to the step back, one of `a run of flaws`, `a run of send-backs`, `passes that did not converge` and `the user's word`, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has the step back reached. An entry appended before the entry held a Cause holds none, stands as it was written, and is read as one chosen at the step back |
| Decision | no | where its kind gives it, in a `design-reassessment` entry only where its Cause is a step back | | text | what the user decided at the step back, one of the values of [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts [Name: design reassessment]`](/specs/methodology/design-workflow/order-of-a-designs-work.md#facts) |
| Diagnosis | no | where its kind gives it, in a `design-reassessment` entry only where its Cause is a step back | | text | the diagnosis the design reassessment recorded, the path of its file in the design's folder, sitting as [`§ The Working Files`](#the-working-files) has a diagnosis sit |
| Places | no | where its kind gives it | | text | where the edit lies, each a path, its section after it where the edit lies in one, separated by semicolons |
| Steering Decision | no | where its kind gives it | | text | the Name of each Steering Decision ([`§ Steering Decision`](#steering-decision)) of the set of steers it logs, separated by semicolons |
| Cuts Short | no | no | none | text | an old log's field, which no entry appended holds: in a log written before a check's report stated how it ended, the Entry of each check a `steer` or `reassessment` entry cut short, read only for a report holding no such statement ([`§ A Check's Report § The Reading and the Settlement`](#the-reading-and-the-settlement)) |
| Running Work | no | no | none | text | each researcher and reviewer still working as the set closed or the step back was reached, and the user's call on it, `stopped` or `continued`, or `cut short` where a run reaching its length cut it short, separated by semicolons: a check named by the Entry it takes, and work stopped before it handed anything back by its kind and its brief |
| Choice | no | where its kind gives it | | "keep revising", "feedback", "good enough" | the user's choice after passes that did not converge, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) has it made |
| Settled Sub-scopes | no | where its kind gives it | | text | each sub-scope the user settled for the audit, a Sub-scope of the Sub-scopes table of [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews), separated by semicolons |
| Audit | no | where its kind gives it | | "specs", "code" | the audit the user bypassed: `specs` for `.ai/skills/audit-specs/`, `code` for `.ai/skills/verify-spec-implementation/` |

The kinds of entry, each with the fields it gives beside Entry, Timestamp and Design Version, the report it names, and when it is appended:

**Reference Key:** Kind \
**Required:** Fields, Report, Appended

| Kind | Fields | Report | Appended |
|---|---|---|---|
| `design-refactor-refine` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | the builder's own report | as the builder's Design, Refactor, Refine pass ends |
| `self-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | the builder's own report | as the builder's self-review ends |
| `handed-off-judgment` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped | the builder's own report | as the settling of a judgment the builder handed off ends: for research, as the builder takes its Read Assessments in; for one settled with a round, as the round's settling ends ([`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round)) |
| `adversarial-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To, Settled Judgments | a review's report | as the round's settling ends |
| `post-apply-review` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To, Settled Judgments | a review's report | as the round's settling ends |
| `audit-specs` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To, Settled Sub-scopes | the builder's triage of an audit | as the settling of an `.ai/skills/audit-specs/` run ends |
| `verify-spec-implementation` | Model, Effort, Design Flaws, Implementation Flaws, Nits, Dropped, Led To | the builder's triage of an audit | as the settling of a `.ai/skills/verify-spec-implementation/` run ends |
| `entered` | Reason | none | as the design enters in-progress |
| `goals-agreed` | none | none | as the user agrees to the goals of a major version |
| `plan-change` | none | none | as the builder's revision of the steps at drafting or changing ends, before its Design, Refactor, Refine pass and its self-review |
| `plan-approval` | Approval | none | as the user approves the plan |
| `steer` | Steering Decision, Running Work | none | as the set of steers closes ([`§ Steering Decision § When a Steer Is Recorded`](#when-a-steer-is-recorded)) |
| `user-edit` | Places | none | in any state of the apply, or while the design is sent back with its changes kept, as the user confirms the edit intended |
| `step-back` | Running Work | none | as the step back is reached, the user's calls on the work then running made, whatever the user then decides there |
| `design-reassessment` | Cause, Decision, Diagnosis | none | as the design reassessment is made, so it starts the major version the design is then worked in. One chosen at the step back is appended as the diagnosis is recorded in diagnosing, before the rebuild's goals are agreed. One made for a changed foundation is appended by the design script's action freeing the design, as that action removes each name of a finished or gone design from its Depends On Designs |
| `reassessment` | Decision, Cuts Short, Running Work | none | none is appended: an old log's entry, read under the fields it was written with, starting a major version where its Decision is other than `go on`, as [`§ A Design Document § The Design's Version`](#the-designs-version) has it |
| `another-round` | none | none | as the user asks for another round |
| `passes-choice` | Choice | none | as the user chooses to keep revising, gives feedback at the choice, or chooses to accept the last pass's fixes as good enough |
| `apply` | none | none | as applying begins |
| `direct-edit` | Places | none | in any state of the apply, as the direct edit is made |
| `audit-bypass` | Audit | none | as the user gives the word bypassing that audit, never brought by the builder, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) has it given, one entry for each audit bypassed |

### When an Entry Is Appended

Each entry is appended when [`§ Design Log Entry`](#design-log-entry)'s kinds table has it appended, at the skill's step where its event ends, never in a pass after the work. A check's entry is appended by the step running the check, as its settling ends with its report in hand. A report a cold agent wrote is taken up and settled as [`§ A Check's Report § Who Writes Each Part § The Report's Workflow`](#the-reports-workflow) has it, and every report is validated by the design script's `--stamp-settled-report` before its entry is appended ([`§ A Check's Report § A Report's Stamp`](#a-reports-stamp)). The design script's `--log-entry` refuses a check's entry whose report does not stand where [`§ Design Log Entry § The Report an Entry Names`](#the-report-an-entry-names) has it, or holds no stamp current with what the stamp was taken over.

**What the appending reads.** Appending an entry reads the design's header, log and steering decisions. From the report it takes the validated stamp, the counts and the version in the Reading. For a review round it also selects the eligible judgments under [`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round). It reads the candidate reports to identify the judgments and research. It uses the same selected contents to verify the stamp and records the corresponding keys, or `none` for an empty selection. For each other file the stamp covers, the appending reads its contents to verify the hash. The other refusals kept with the appending read only what bears on that entry, so a design whose other parts do not parse still takes one. Appending runs no test.

No check's entry is appended before the `goals-agreed` entry of its major version, since no check's report stands before the agreement of the goals it is judged against ([`§ A Design Document § The Design's Version`](#the-designs-version)). Whatever moves the work on while a check runs or is settled, the user's approval, a set of steers, a send-back, the step back or a design reassessment among them, the builder settles each of the check's findings in its report before the check's entry is appended. Each Settlement says what became of its findings ([`§ A Check's Report § Settlement`](#settlement)). Where the report owes the statement, its Settlement states how the check ended ([`§ A Check's Report § Check Ending`](#check-ending)). The entry's Led To is the state the work went into. So every check that handed back a report has its entry, and no entry is appended while its report holds a finding it does not settle. Work stopped before it handed anything back takes no entry of its own: the Running Work of the set's `steer` entry or of the `step-back` entry records the call, or the cut a run's length made, so the log shows the work ran and was stopped. The `step-back` entry is appended as the step back is reached, whatever the user then decides there, so an approval given at the step back is a `plan-approval` entry after it.

### The Report an Entry Names

A check's entry names its report, in the design's folder as [`§ The Working Files`](#the-working-files) has it. The report takes the form [`§ A Check's Report`](#a-checks-report) gives it.

### What a Check Counts

Each count of a check's entry is taken from its report, never given by the builder. Each finding the report holds is counted once, by the verdict of the Settlement settling it ([`§ A Check's Report § Settlement`](#settlement)), in the count [`§ A Check's Report § Verdicts`](#verdicts) gives that verdict, a reviewer's own drop the builder upholds counted in Dropped. The builder marks what its own Design, Refactor, Refine pass, self-review and handed-off judgment found as a review's findings are marked, and appends each entry with the model and effort it ran on.

### Script Checks

**Records:**
  - **Name:** counts-taken-from-the-report \
    **Tests:** each count of a check's entry is the count its report gives, each finding counted once by the verdict of the Settlement settling it, as [`§ Design Log Entry § What a Check Counts`](#what-a-check-counts) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Name:** goals-agreed-before-checks \
    **Tests:** no check's entry stands before a `goals-agreed` entry of its major version, as [`§ Design Log Entry § When an Entry Is Appended`](#when-an-entry-is-appended) has it: `--log-entry` refuses such an entry as it is appended, and the validation review reads the order over the whole log \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - `.ai/skills/design-specs/` `--check-design`
      - `.ai/skills/implement-specs/` `--check-design`

  - **Name:** entry-at-the-version-read \
    **Tests:** a check's entry is stamped at the version its report's Reading records, a version the log held by the time the entry is appended, and an entry with no report at the version as it is appended, as [`§ Design Log Entry`](#design-log-entry) has an entry stamped \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - `.ai/skills/design-specs/` `--check-design`
      - `.ai/skills/implement-specs/` `--check-design`

  - **Name:** sub-scopes-named \
    **Tests:** each sub-scope an entry's Settled Sub-scopes holds, taken one at a time, is a Sub-scope of the Sub-scopes table of [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews): `--log-entry` refuses an entry naming anything else as it is appended, and the design's check reads the whole log \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - `.ai/skills/design-specs/` `--check-design`
      - `.ai/skills/implement-specs/` `--check-design`

  - **Name:** settled-sub-scopes-keep-what-changed \
    **Tests:** an entry's Settled Sub-scopes hold each sub-scope holding a file the design changed, its changes read as [`§ A Design Document § Applying and Committing`](#applying-and-committing) has them read, as [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews § The Sub-scopes a Design Settles § The Sub-scopes of a Design's Audit`](/specs/methodology/design-workflow/designs-reviews.md#the-sub-scopes-of-a-designs-audit) has the user settle them: `--log-entry` refuses an entry dropping one as it is appended, and the design's check never reads it, since the changes then stand no longer once the design commits \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Name:** audits-run-or-bypassed \
    **Tests:** before the builder brings the user the commit, or, where the project has no version control, before the design becomes applied, the design's log, after its last `apply` entry, holds for each audit the design must run its entry or an `audit-bypass` entry naming it: the specs audit where the design changed a file of any sub-scope of the Sub-scopes table of [`specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews`](/specs/methodology/design-workflow/designs-reviews.md#a-designs-reviews), and the code audit where it changed code, its changes read as [`§ A Design Document § Applying and Committing`](#applying-and-committing) has them read: `--check-audits` refuses a design lacking one, naming each audit neither run nor bypassed, and nothing reads the log once the design has committed \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-audits`
      - `.ai/skills/implement-specs/` `--check-audits`

  - **Name:** entry-names-a-stamped-report \
    **Tests:** a check's entry is appended only where the report it names holds a stamp current with it, as [`§ A Check's Report § A Report's Stamp`](#a-reports-stamp) has a report stamped, and the appending makes no other check of the report than the refusals the canon keeps with it, the entry's version read from the report's Reading among them, and runs no test \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

## A Check's Report

A check's report records what a check of a design found and how its findings were settled, what the builder's own work in the check read, searched, traced and asked, and, for research, how each area the cold agent doing it read bears on the design. So nothing a later step, a later round, a review or a session taking the design up fresh needs lies in one agent's context alone, and the design script checks each record against what it works out from the files. This section is the one home of a report's form. The form reaches every report a design's log entry names. It reaches no audit run's own report, which keeps its own skill's form and folder, and no file a log entry does not name. A report is one of these, the Report its entry's row of [`§ Design Log Entry`](#design-log-entry)'s kinds table gives:
- a review's report, recording a cold reviewer's check of the design;
- the builder's own report, recording its Design, Refactor, Refine pass, its self-review, or a judgment it handed off to a cold agent;
- the builder's triage of an audit, holding each audit finding it settles as a finding of its own.

These tell whose check a report records and which checks read it, never who writes a part, which [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) gives for every kind of report. Each takes its parts from one table and its records from the same record types. A report holds these parts, in this order, each part's Holds citing the rule whose result it holds. A part not required where it holds nothing is left out with its heading, so a round that found nothing passes. A report holds no summary of its counts, since its log entry takes them from it:

**Reference Key:** Part \
**Required:** Heading, Required, Holds

| Part | Heading | Required | Holds |
|---|---|---|---|
| Title | `# Check's Report`, with the fields Design, Entry, Stopped At and Goal Comparison as owed | yes | Design and Entry identify the report. [`§ A Check's Report § Evidence Owed for Goals`](#evidence-owed-for-goals) gives its other title fields |
| Reading | `## Reading` | yes | what the check read, each file read fresh as [`specs/AGENTS.md § Design, Refactor, Refine § Reading Fresh`](/specs/AGENTS.md#reading-fresh) has it, in a review's passes as [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) orders them |
| Goal Judgments | `## Goal Judgments`, a record section of Goal Judgments | where [`§ A Check's Report § Evidence Owed for Goals`](#evidence-owed-for-goals) requires goal judgments | the wording and both answers for every goal, as [`§ A Check's Report § Goal Judgment`](#goal-judgment) has a judgment made |
| Findings | `## Findings`, a record section of Findings | where the check found anything | each finding, as [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review), [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) and the audit's settling in [`specs/AGENTS.md § Design, Refactor, Refine § An Audit`](/specs/AGENTS.md#an-audit) have one reported |
| Searches | `## Searches`, a record section of Searches | where a search was run | each search the builder or a reviewer ran for its own check, as [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact) has a fact's home sought and [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) has a tactical fix made at every place its defect stands, and each search a cold agent ran doing research, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research done |
| Read Assessments | `## Read Assessments`, a record section of Read Assessments | where the report is a judgment's doing research | each area the cold agent doing the research assessed, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research assessed |
| Traces | `## Traces`, a record section of Traces | where the builder traced a mechanism | each trace, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism`](/specs/AGENTS.md#tracing-a-mechanism) has a mechanism traced and [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether a Changed Mechanism Serves a Goal`](/specs/AGENTS.md#whether-a-changed-mechanism-serves-a-goal) has its test asked |
| Builder Checks | `## Builder Checks`, a record section of Builder Checks | where the builder made a check of its own | each check only the builder makes, as [`§ A Check's Report § Kinds of Builder Check`](#kinds-of-builder-check) has it recorded |
| Hand-back | `## Hand-back`, text | once the builder takes up a report a cold agent wrote | a fingerprint of each part the cold agent wrote, as [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) has the builder take a report up |
| Script Output | `## Script Output`, text | where the report is a self-review's | the output of the design script's checks the self-review runs for its phase, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) gives them, written by `--stamp-settled-report` as the report is validated |
| Causes | `## Causes`, a record section of Causes | where the report's Ending is `its own settling` and the round is one [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes`](/specs/AGENTS.md#the-round-at-its-causes) settles at its causes and a finding it settles, its own or a handed-off judgment's settled with it, takes a mark | the round's causes, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose) has them stated |
| Settlement | `## Settlement` | once the report is validated | how the check ended, where the report owes the statement, the earlier reports read and the builder's reading at settling, as [`specs/AGENTS.md § Design, Refactor, Refine § Reading the Earlier Reports`](/specs/AGENTS.md#reading-the-earlier-reports) and [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group`](/specs/AGENTS.md#group) have them read before grouping, and how each finding was settled, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose`](/specs/AGENTS.md#propose), [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test), [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) and [`§ A Design Document § Changes After Approval`](#changes-after-approval) have it recorded |

**A report not in the form.** A report not in the form keeps the form it was written in, and a check reading the design's earlier reports reads one not in the form as holding no records.

### Who Writes Each Part

A report is written by more than one hand, each writing only its own parts, and no hand changes a record another wrote. Which hand writes each part of each kind of report:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Kind of report, Part \
**Input Values:**
  - Kind of report: "a review's", "research", "another handed-off judgment's", "a Design, Refactor, Refine pass's", "a self-review's", "an audit's triage"

| Kind of report | Part | Written by |
|---|---|---|
| - | "Script Output" | the design script, as the report is validated |
| - | "Causes" | the builder |
| - | "Settlement" | the builder, but for its Validated field, which the design script writes as the report is validated |
| - | "Hand-back" | the design script, as the builder takes the report up |
| "a review's" | "Searches" | the cold reviewer, the builder adding its own after the reviewer's |
| "a review's", "research", "another handed-off judgment's" | - | the cold agent |
| - | - | the builder |

The Reading's Design Version is written by the agent that read the design's header, with the rest of the Reading, never by the builder at settling nor by `--log-entry` as the entry is appended, since either can come after a set of steers has raised the version.

The design script checks each part while the hand that wrote it holds the report, as [`§ A Check's Report § Who Writes Each Part § Which Action Checks a Part`](#which-action-checks-a-part) has each part checked.

Once the builder takes a report up, no check reads a part its cold agent wrote against the design or the files again. The part stands as it was taken up, held only to the fingerprint the take-up wrote of it ([`§ A Check's Report § Script Checks [Name: cold-parts-kept]`](#script-checks-1)), which `--check-settled-report` and `--stamp-settled-report` confirm. A check of the builder's parts reads a cold agent's records for what they hold, as a Settlement names the Findings it settles, and holds those records to nothing. The builder changes files after the take-up, the design document while settling among them. A fix can write a searched phrase somewhere new, and a change to the design can remove a goal, a Frame Outcome or a step Objective a Finding names. So no later change refuses a part that was right as it was taken up, no taken-up report is left with the builder unable to be settled, and a report goes back to its cold agent only as [`§ A Check's Report § Who Writes Each Part § The Report's Workflow`](#the-reports-workflow) returns one.

The research binding the design is still read together as a report is validated, the report of each entry [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) names. That reading is no check of a research report: it refuses no research report and returns none.

#### Which Action Checks a Part

Which action of the design script checks a part of a report turns on whose part it is. What it checks of a report is [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks)'s to say:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Written by \
**Input Values:**
  - Written by: "a cold agent", "the builder", "no one hand"

| Written by | Checked by |
|---|---|
| "a cold agent" | `--check-handed-back`, as the cold agent hands the report back, and `--take-up-report`, which runs that check again as the builder takes the report up |
| "the builder" | `--check-settled-report`, each time it is run, and `--stamp-settled-report`, which runs that check before it stamps |
| "no one hand" | each of those actions |

The part no one hand wrote is the order of a report's parts. In a report the builder writes alone, every other part is the builder's. In a report a cold agent wrote, the builder's parts are the Causes, the Settlement and, in a review's report, each Search the builder adds after the reviewer's. The two actions checking a cold agent's part each read it against the design and the files as they then stand: its form and its layout, the form of each value holding places, each key it cites, each part of the design a Finding names, each place its Reads hold and each cause it names for assessing an area again where the report holds Read Assessments, and each Search it recorded, read as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has a cold agent's Search read at each.

#### The Report's Workflow

Writing a report moves from hand to hand, each move taken once the check before it passes:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine` \
**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| being written | its first hand writes its parts: the cold agent of a review or of a judgment handed off, or the builder of a report it writes alone | Yes | No |
| handed back | the cold agent's check passed, and the builder has yet to take the report up | No | No |
| with the builder | the builder took the report up, and writes its parts | No | No |
| settled | the report's validation passed, and its stamp is current | No | No |
| entered | the report's entry is appended | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| being written | handed back | `--check-handed-back` reports no problem | a cold agent writes the report |
| being written | settled | `--stamp-settled-report` stamps the report | the builder writes the report alone |
| handed back | with the builder | `--take-up-report` reports no problem | none |
| handed back | being written | `--take-up-report` reports a problem | none |
| with the builder | settled | `--stamp-settled-report` stamps the report | none |
| settled | with the builder | the report, or a file its stamp takes in, changes | none |
| settled | entered | `--log-entry` appends the report's entry | the report's stamp is current |
| with the builder | being written | the design script returns the report to its cold agent, clearing every part the builder and the take-up wrote | a part the cold agent wrote no longer matches the fingerprint the take-up wrote of it |

Each action checks the parts [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) gives it. `--check-handed-back` holds the cold agent's parts to everything the design script checks of them, and refuses any other part the report holds. `--take-up-report` runs that check again and, where it passes, writes the report's Hand-back part, a fingerprint of each part the cold agent wrote. `--check-settled-report` holds the builder's parts to everything the design script checks of them, a report the builder writes alone in every part. It confirms that each part the cold agent wrote still matches its fingerprint, the builder's own Searches after a review's Searches aside, and checks nothing else of such a part. `--stamp-settled-report` makes each check `--check-settled-report` makes and stamps the report where they pass, as [`§ A Check's Report § A Report's Stamp`](#a-reports-stamp) has a report stamped.

A report `--take-up-report` refuses goes back to its cold agent as it was handed back, with what the check reports. Once a report is taken up, it goes back only for a part the cold agent wrote that no longer matches its fingerprint, a part changed or removed since the take-up. Where `--check-settled-report` or `--stamp-settled-report` finds such a part, the design script clears every part the builder and the take-up wrote, and the report goes back with what the check reports. So the builder never edits or strips a cold part. A report refused for a fault in the builder's own parts stays with the builder, who leaves the cold parts and the settlement as they stand and puts the builder's own parts right. Where the agent in use cannot continue a report that goes back, its check is run again with the same brief. The cold agent puts the refused part right and hands the report back, and `--take-up-report` reads it as a report newly handed back, so a research share so returned binds once it is taken up again.

### The Reading and the Settlement

The Reading opens with the field Design Version: the version of the design the check read, from the design's header as the check began. It is left out at 0.1.0, its default. Where the report is a review's, the Reading then holds the field Reviewer Readings, a list of [`§ A Check's Report § Reviewer Reading`](#reviewer-reading) records, one for each reviewer. Where the report is any other check's, it holds the field Reads: the places the check read, or `none` where it read nothing. A report of research's Reads holds the places the builder named. The Settlement holds these fields, in this order:
- Validated, the report's stamp, as [`§ A Check's Report § A Report's Stamp`](#a-reports-stamp) has it written, held once the report is validated and written by the design script alone;
- Ending, held where the report owes the statement ([`§ A Check's Report § Ending Statement Owed`](#ending-statement-owed)), whether or not it holds a Finding: `its own settling`, or `decided` or `cut short`, a comma, and what ended it in words, as [`§ A Check's Report § Check Ending`](#check-ending) gives the ending; left out of a report written before the statement was owed;
- Earlier Reports, places, `none` where the round's phase holds no report before it; in a report of research handed off while a round is settled, that round's report among them, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research name it;
- Settling Reads, places, the builder's reading at settling, held where the report is a review's, `none` where no Finding holds a mark;
- Settlements, a list of [`§ A Check's Report § Settlement`](#settlement) records, held where the report holds a Finding.

### A Report's Stamp

A report is validated by the design script's `--stamp-settled-report`, once the builder has settled it. The action makes every check `--check-settled-report` makes of the report. Where the report's entry is one at which the research binding the design is read together, it reads that research ([`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks)). For a self-review over applied work it runs the kept tests and the checks made with their run, as [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Kept Tests § When the Kept Tests Are Run`](/specs/methodology/skills/authoring-a-skill.md#when-the-kept-tests-are-run) has them run, and writes what they gave into the report's Script Output. Where nothing is reported, it writes the report's stamp into the Validated field of its Settlement, in the form [`§ A Stamp`](#a-stamp) gives, a part no cold agent writes, so taking a report up and stamping it leave each part a cold agent wrote as it was handed back. Where anything is reported, it writes no stamp, and it clears a stamp the report held.

The stamp covers the report's text with its own field left out. It includes the paths and contents of any further files under [`§ A Stamp`](#a-stamp). A change to the report, the selection of files or their contents requires validation again before append. The design script alone writes the stamp.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Review round?, Self-review?, Over applied work?

| Review round? | Self-review? | Over applied work? | Further files covered |
|---|---|---|---|
| true | - | - | the judgment reports selected under [`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round) |
| false | true | true | the durable files in the design's changes under [`§ A Design Document § Applying and Committing`](#applying-and-committing) |
| false | - | - | none |

`--check-settled-report` makes the same checks of the report, writes nothing and runs no test, so the builder may check its settling as often as it likes before it validates.

### Ending Statement Owed

Which kinds of report state, in their Settlement, how their check ended. A report stating none is read for whether it binds as [`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record) reads it.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Check \
**Input Values:**
  - Check: "a review's round", "a research share", "another handed-off judgment", "the audit's triage", "a self-review", "a Design, Refactor, Refine pass"

| Check | Owes the statement? |
|---|---|
| "a review's round", "a research share", "another handed-off judgment", "the audit's triage" | true |
| "a self-review", "a Design, Refactor, Refine pass" | false |

### Check Ending

What a check's ending decides, for each kind of check owing the statement: how it ended, the change it makes, its Causes, whether it binds and where its findings, nits among them, go, each known as the check is settled. A judgment settled with a round takes its round's ending, as [`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round) has it settled. So another handed-off judgment in this table is one settled on its own. The user stops or continues each check at a set's close, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) has the call made, and at the step back, where a check is also cut short, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has it. A design reassessment for a changed foundation cuts short every check of the design whose settling has not ended as the design is freed, one still running, one handed back and not yet taken up and one being settled alike, on no call of the user's: the builder stops each researcher and reviewer still working as it frees the design, and each such check binds nothing, its findings going nowhere.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Check, Ended by \
**Input Values:**
  - Check: "a review's round", "a research share", "another handed-off judgment", "the audit's triage"
  - Ended by: "its own settling", "a set ending the round, its settling continued", "the plan's approval", "a set's close, the check stopped", "the step back, the check stopped", "a run's length", "a design reassessment chosen at the step back", "a design reassessment for a changed foundation"

| Check | Ended by | Ending | Change made | Causes | Binds? | Findings go to |
|---|---|---|---|---|---|---|
| "a review's round" | "its own settling" | its own settling | its own | as the Causes part of [`§ A Check's Report`](#a-checks-report) has them | true | its own change |
| "a review's round" | "a set ending the round, its settling continued" | decided | none | none | true | the set's change |
| "a review's round" | "the plan's approval" | decided | none | none | true | the approved plan |
| - | "its own settling" | its own settling | none | none | true | its own settlement |
| - | "a set's close, the check stopped" | cut short | none | none | false | the set's change |
| - | "the step back, the check stopped" | cut short | none | none | false | what the user decides at the step back, or the set's change where a set of steers closes there instead |
| - | "a run's length" | cut short | none | none | false | what the user decides at the step back, or the set's change where a set of steers closes there instead |
| - | "a design reassessment chosen at the step back" | cut short | none | none | false | the diagnosis |
| - | "a design reassessment for a changed foundation" | cut short | none | none | false | nowhere |
| - | - | no such ending | none | none | false | nowhere |

### A Value Holding Places

A field of a report holding places holds them as a list, one place to an item, each a citation, as [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) writes one, of a file, of a section within one or of a part a keyed instance holds, or, where the field holds one place, that citation alone. One place covers another where it is that place or holds it:
- a file covers each of its sections;
- a section covers each section beneath it;
- a part a keyed instance holds covers itself alone.

Each place is matched as it is cited.

### Over Applied Work, and a Phase's Record

A report lies over an apply where its entry stands after that `apply` entry and before the next `entered` entry, and over applied work where its entry stands after the design's last `apply` entry, with no `entered` entry after that. A report is of the design's current major version where the entry naming it holds that major version ([`§ A Design Document § The Design's Version`](#the-designs-version)). The reports a design is held to, for its findings, the lineage of its fixes, its phase's record and its runs, are its own reports of its current major version. Another design's reports never bind it, and neither a commit nor a steer unbinds one of its own. A line of fixes is read through every report of the current major version, so it runs on across a send-back and a later apply.

A report's findings bind the design while what it read stands, sorted by its answers to the questions:
- **Of the current major version?** Whether the report is of the design's current major version.
- **Cut short?** Whether the report's Settlement states its check was cut short, as [`§ A Check's Report § The Reading and the Settlement`](#the-reading-and-the-settlement) has the statement made; for a report owing no statement, or written before the statement, whether a `reassessment` or `steer` entry's Cuts Short names its entry ([`§ Design Log Entry`](#design-log-entry)).
- **Over an apply?** Whether the report lies over an apply.
- **Replaced by a later apply?** Whether a `post-apply-review` entry stands after an `apply` entry later than the one it lies over, the next apply's writing having replaced what it read.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Of the current major version?, Cut short?, Over an apply?, Replaced by a later apply?

| Of the current major version? | Cut short? | Over an apply? | Replaced by a later apply? | Binds the Design |
|---|---|---|---|---|
| false | - | - | - | false |
| - | true | - | - | false |
| - | - | true | true | false |
| - | - | - | - | true |

So a design reassessment unbinds every report before it, since it starts a major version and the design it read is made afresh. A check cut short binds nothing, kept as history, and a set's rebuild hands its brief again where it needs the check. A report no longer binding the design stays in the design's folder as the record of how the design came to be, read as [`specs/AGENTS.md § Design, Refactor, Refine § Reading the Earlier Reports`](/specs/AGENTS.md#reading-the-earlier-reports) has it read.

A phase's record is the reports binding the design whose entries stand in the phase, those of its review entries and of each `handed-off-judgment` entry among them, so the Misses of the phase are those its record holds. An adversarial review's phase starts after the design's last `design-reassessment` entry, or its last `entered` entry whose Reason is a send-back's, `sent back`, `sent back for a dependency` or `sent back to the step back`, whichever stands later, or at the log's start, and a post-apply review's after the design's last `apply` entry. So a report over an apply the design was sent back from joins the record of no phase after the send-back. The builder's self-review before the plan's next approval reads it for the findings it carries, as [`§ A Check's Report § Kinds of Builder Check`](#kinds-of-builder-check) has a carried finding checked. The runs are not bounded by a phase: an adversarial round counts in them across a send-back, as [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a run set back only by a round finding no flaw of its kind or by the step back. A self-review follows a round's change where the last review entry of its phase before it, after the design's last `self-review` entry, names a report holding a Proposed Change.

### A Judgment Settled with a Round

At first settlement a round takes the nonresearch judgments whose reports identify this design and judgment and whose keys no earlier judgment entry or review's Settled Judgments has recorded. A research judgment settles on its own when the builder takes in its Read Assessments. A judgment handed off after the last round also settles on its own ([`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § After the Last Round`](/specs/AGENTS.md#after-the-last-round)). The log records each judgment's entry when [`§ Design Log Entry`](#design-log-entry) requires it.

Rechecking an entered round reads the keys on its entry, each naming a distinct report eligible at the time of that round. An entry of the earlier form supplies no recorded keys. A primary Changed Place must name findings its change settles. Where ownership was unrecorded, a key outside the round's own Findings cannot by itself establish that the change failed this check.

Where the round holds Causes, each marked Settlement of a judgment it owns cites its Cause by the round's report and the Cause's key. A judgment settled with a round that holds no Causes omits the Cause citation.

### What the Design Script Checks

The design script checks of a report what it works out from the files, and nothing of what a record must cover beyond it. An item this section lists that names its own moment is asked then. Every other item is asked of a part only while the hand that wrote the part holds the report, at the moments [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) gives: of a cold agent's part as its report is handed back and as it is taken up, and of the builder's parts at each check of the settled report. Of every report:
- it holds the form [`§ A Check's Report`](#a-checks-report) gives and the layout [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) and [`specs/methodology/spec-style/markdown.md § Blank Lines`](/specs/methodology/spec-style/markdown.md#blank-lines) give;
- each key it cites names a record a report of the design's current major version holds, or one the report's own Earlier Reports names, as [`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record) has a design's reports bind it, each Lands On, a Finding's as it is handed back and a Settlement's as it is settled, naming a Cause or a Settlement;
- each Finding is settled by exactly one Settlement;
- each Settlement's Carried By, but `none`, names a step the design holds;
- each Finding whose Verdict is a mark names in its Affected Goals, Affected Frame Outcomes or Affected Step Objectives what it bears on, each Name resolved as [`§ A Check's Report § Finding`](#finding) requires, or cites in its Broken Rules the rules it breaks;
- each Search read as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has one read.

Of the goal evidence [`§ A Check's Report § Evidence Owed for Goals`](#evidence-owed-for-goals) requires, as [`§ A Check's Report § Goal Judgment`](#goal-judgment) defines it:
- for a full review, check one judgment per goal. When its goal set is independently available, compare every Name and complete Description. The current design supplies that set when no change of goals intervened. When the original set is unavailable, the comparison basis discloses that limitation;
- each answer other than `met` names a Finding of this report whose reviewer marked it a design flaw and whose Affected Goals include the judged goal. Whether its evidence establishes failure on this question takes a reader;
- for a structural stop, check for a marked finding identifying a structural rule, an affected step Objective or a Frame Outcome. The reader judges its substance.

At hand-back and take-up the checker reads the cold reviewer's evidence. Once taken up, it preserves that evidence under [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part). A builder's self-review is checked before entry. On a later reading its judgments stand against the wording recorded at the time. An entered report written under an earlier form keeps that form.

Of a report holding Read Assessments:
- each place its Reads holds lying within the Area of one of its Read Assessments, as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has one place cover another, so each report is held to the places it was given to read;
- each Read Assessment whose Area a research report binding the design already assesses holding its Assessed Again For, naming a cause that counts against each such earlier report. A cause counts against an earlier report only where that report could not have weighed it. A set counts where its `steer` entry stands after the earlier report's entry, or its version is past the version the earlier report read. A finding counts where it is a finding of a report the earlier report's Earlier Reports does not name. The finding is read from the report it names: one a check's entry of the design's current major version names, or one standing in the design's folder that no entry names yet, the round being settled, whose report stands handed back while its entry waits.

Of the research binding the design, the union of the research reports binding it, as [`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record) has a report bind: each place that a Search of one of them giving every place gives, and each place that a Search of one of them of the Kind "meaning" holds, read as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has a Search read where the research is read together, lying within the Area of a Read Assessment in one of them, whichever report holds the Search. A place no binding report assesses takes a first assessment, and one another share assesses takes none. The union is read where the binding research is read together:
- as the report of the builder's first check after research is taken in is validated, other than a handed-off judgment's, so a gap is found before a round reads the frame;
- in the validation review of a design not yet approved, over the research reports it reads;
- for research taken in after the plan's last approval, as the report of the round whose settling took that research in is validated.

The validation review reads the union only of a design not yet approved. The frame is frozen at the plan's approval, and once the design applies the files hold its apply's own writing, which a Search run then would give as places no research assessed. So research taken in at the apply is held as the report of the round taking it in is validated, and by no validation review.

Of that union too, each goal the design holds is searched over every operative file by terms, and asked over every operative file by meaning, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has each goal searched ([`§ A Check's Report § Script Checks [Name: goals-searched-over-every-operative-file]`](#script-checks-1)). A Search counts toward a goal where its Goals name the goal, its Kind is "meaning" or "terms", and its Target is "current-operative-files", or "committed-operative-files" with no Commit. A Target logged under an earlier name is read as [`§ A Check's Report § Search`](#search) gives that name, and its Search counts as a Search of the target it is read as. The Searches of each of those Kinds counting toward a goal are narrowed to paths that together leave no operative file out, a Search narrowed to none asked over every file. A Search by terms gives every place, so the files it was asked over are the files it searched. A Search by meaning gives a part of a ranking, so it counts as searching only the files its Places hold, however few: it is asked over every operative file so that each is ranked, and the goal's Searches by terms search every file. A Search of the fixture files, a Search of the working files, a Search holding a Commit, a Search of any other Kind and a Search logged before a Search held a Kind count toward no goal. The check runs no Search. It reads the paths each was narrowed to against the operative files the last commit holds, or against those standing where the project is under no version control. So a file an apply has written and not committed is asked of none of them. It reads those files as the scope names them at the check, whenever a Search was logged. So a design in flight whose Searches were narrowed by path is asked for Searches of each operative file the scope has gained since. The check is made as the report of each of those entries is validated, and in the validation review of a design not yet approved. A design approved before it takes research in is asked only as a report after that research is validated, and then for every goal.

Of a self-review:
- before the apply, a Trace of each Decision Table and State Machine standing in a section a step's What names, holding its Outcome where the Trace's form requires one;
- over applied work, a Trace of each Decision Table and State Machine a section the diff changed holds, naming each of its paths, a Decision Table's rows and a State Machine's transitions each named by its cells. A pass proving the fixes, a self-review whose entry stands after a `post-apply-review` entry of the apply, needs a Trace only of those its Reads cover, since its Reads hold the reach of those fixes;
- each Builder Check required of it, as [`§ A Check's Report § Kinds of Builder Check`](#kinds-of-builder-check) gives it, its Places Checked covering each item it is required for;
- among them, a `problem re-evaluation` in a major version's first self-review alone: the one whose entry no `self-review` entry stands before since the `design-reassessment` entry starting that major version ([`§ A Design Document § The Design's Version`](#the-designs-version)), or since the log's start in a design's first. Its Places Checked cover each citation holding a path that the design's Problem holds as the report is validated. A self-review appended to a major version whose first self-review the log already holds owes none;
- for one following a round's change, its Reads covering each place a Miss of the phase names;
- its Script Output, written by `--stamp-settled-report`;
- over applied work, as its report is validated and never as `--check-settled-report` checks it, the kept tests passing of each script one of whose files the design's changes hold, each check made with a run of them reporting nothing, and the design script's comparison run where those changes hold a file of the design script, each run by the design script and its result written into the Script Output ([`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]`](/specs/methodology/skills/authoring-a-skill.md#script-checks));
- where that comparison is run, its `differential test` Builder Checks covering in their Places Checked each design the comparison lists.

Of a round's settlement:
- its Earlier Reports listing each report of the phase's record before the round;
- its Settling Reads, or the Area of a Read Assessment in the report of a handed-off judgment the design's log names, covering each place the Evidence of a Finding whose Verdict is a mark names;
- each Cause settling a flaw holding its Misses;
- each Cause settling a flaw holding its Proposed Change, but where a Settlement naming it gives Lies In the plan or handed on in a post-apply round;
- a Cause continuing an earlier one holding its Outcome;
- a Proposed Change that is a tactical fix citing a Search, its own Places covering each place the Searches [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) requires of a tactical fix found.

Of each Settlement, its two indicators:
- what requires its findings: its Justifying Goals and its Justifying Rules held as its Required By names them, each goal one the design holds;
- whose authority their fix is, held only where its Verdict is other than dropped, since a finding The Test drops has no fix: its User Decision held where its Fix Authority is the user's, and its Fix Authority the user's where the report or its entry shows [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Whose Fix It Is`](/specs/AGENTS.md#whose-fix-it-is) giving the user the call, which it shows where:
  - the report is the builder's triage of an audit, its entry's kind `audit-specs` or `verify-spec-implementation`;
  - its Verdict, or the Verdict of a finding it settles, is a design flaw, a review observation, set aside or not caused;
  - its Lies In, or the Lies In of a finding it settles, is the plan or handed on;
  - its Order is tertiary, or a change settling its findings reaches a tertiary place;
  - such a change is made, its Places or its Cause's Proposed Change recording it, and its Required By is nothing.

Of each Settlement and each Changed Place, the order its lineage gives:
- a Settlement's Order as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage § A Finding's Order`](/specs/AGENTS.md#a-findings-order) gives it, worked out from its own Lands On and from the Lands On of each finding it settles, taking the deeper. The fix a Lands On names is a Cause's Proposed Change or a Settlement's Places, and that fix's order is the shallowest Order among the Settlements naming its Cause, or the Order of the Settlement holding its Places. A fix whose Settlements hold the User Decision `widen the goals` starts its line again;
- a Changed Place's Order primary where it holds Settles, each Finding one its change settles, secondary where it Follows a primary place of its own change, and tertiary where it Follows a secondary one.

Of each Settlement, each departure from a finding it settles, in Verdict, in Lies In or in Lands On, holding its Departure Reason.

A report whose entry the log holds is read under the field names it was written with, its Weighs Again as its Lands On, and a Search holding a Pattern as it was read before the record held a Kind: the design script runs that expression by its own reading, `^` and `$` matching where a file's text starts and ends, over the ground such a Search had then: the operative files of each kind its design's Target names, the kinds being those [`§ A Design Document § The Kinds of Change`](#the-kinds-of-change) gives, a canon design's own kind among them whatever its Target holds, the code where `application-specs` is among the kinds, and, where `canon-specs` is among them, the files of each sub-scope the `Search Sub-scopes` field of its design document's Scope names, a field a canon design's Scope held before research searched every operative file and read for this ground alone, the design document with them but for a Search in a report of research. A fixture file is of the fixture files wherever the design script answers a file's kind, and of no kind of change ([`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs)), so that ground holds none. A Scope reading `Not yet stated.` with that field alone after it is read as not yet stated. Where a Search it holds has no Snapshot, none is asked of it, and one holding no Goals outside a report of research is asked for none. Where none of its Settlements holds a field, nothing that field is checked for is refused in it. So where none holds an Order, each earlier change it records is read as primary. Where none holds a Required By, neither indicator is refused, and where none holds a Departure Reason, no departure is.

**What no check decides.** When a place was read; which facts' homes a pass or a self-review sought, or whether a search was the one a fact needed; whether a finding lands on the change its lineage names; what a Builder Check found; which findings in text the rework replaces a send-back carries; whether a Settlement's account of what became of its findings is true; whether the goals and rules a Settlement names justify its findings as its Assessment says, or a fix it records was made; whether a fix needs a call of the user's that no field of the report shows; whether a change settles less than a finding's Possible Fix reaches; whether a place states or reads the decision it aligns with; whether a finding bears on the parts it names, or a Read Assessment's Impact is right; and whether a cause or a verdict is right. Each is a judgment, checked for its presence and the keys it cites alone, and the next review's and the user's to read.

#### Reading a Search

A Search written in the form [`§ A Check's Report § Search`](#search) gives is read as its own report is checked, by the actions [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) names for its recorder: the builder's own with its report, and a cold agent's as its report is handed back and as it is taken up. A research's Search of the operative files or of the fixture files is read too where the research binding the design is read together, at the moments [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) gives. A Search is read at no other moment. How the design script reads a recorded Search is decided by when it is read and by what its kind gives:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Read, Its Kind Gives \
**Input Values:**
  - Read: "as the builder's own Search is checked with its report", "as a cold agent's report is handed back or taken up", "as a check after its report's take-up meets a cold agent's Search", "where the research binding the design is read together"
  - Its Kind Gives: "every place", "a part of a ranking"

| Read | Its Kind Gives | The Search is run | Held to |
|---|---|---|---|
| "as the builder's own Search is checked with its report" | "every place" | as it was asked, over the files its Target asks of, within the paths it was narrowed to | each place it gives stands among its Places |
| "as the builder's own Search is checked with its report" | "a part of a ranking" | not at all | nothing by a run: its record stands as written, held to its form |
| "as a cold agent's report is handed back or taken up" | "every place" | as it was asked, over the files its Target asks of, within the paths it was narrowed to | each place it gives stands among its Places |
| "as a cold agent's report is handed back or taken up" | "a part of a ranking" | not at all | nothing by a run: its record stands as written, held to its form |
| "as a check after its report's take-up meets a cold agent's Search" | - | not at all | nothing by a run: the part holding it stands as it was taken up, held only to its fingerprint, as [`§ A Check's Report § Script Checks [Name: cold-parts-kept]`](#script-checks-1) holds it |
| "where the research binding the design is read together" | "every place" | as it was asked, over the files its Target asks of, within the paths it was narrowed to | each place it gives lies in an area the research binding the design assessed |
| "where the research binding the design is read together" | "a part of a ranking" | not at all | each of its Places lies in an area the research binding the design assessed |

A Search of the Kind "meaning" gives a part of a ranking, and a Search of any other Kind gives every place, as the Completeness of a search's result has each, whose form `.ai/skills/search-spec-of-record-scope/` states. A Search of the Kind "terms" is run asking for exact where its Exact is "yes", and by default where it is "no", so every reading runs it as it was asked. A Search is run no wider than it was asked, whichever reading runs it. The design script keeps nothing of a run between readings, and no reading of a Search writes into a report: it asks the search at each reading, and the search gives the answer it kept where what was asked, the files and its own reading stand as they did, as `.ai/skills/search-spec-of-record-scope/` has it in its section on where the search's output goes.

A run reads the files the Search's Target asks of, the Target [`§ A Check's Report § Search`](#search) has a search made in a design's work ask. A Target logged under an earlier name is read as the table of earlier names in [`§ A Check's Report § Search`](#search) gives it. Its Search is then run and held as every Search of that target is, over the files the target reads as they stand at the run, so it reaches each file the scope has gained since it was logged. A Search naming "current-operative-files" or "current-fixture-files" is run over the files the design works from as every reading of the files as they stand is made: as they stand, the design's work in flight among them once it applies, and at the last commit wherever [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has such a reading take it. A Search naming "committed-operative-files" or "committed-fixture-files" and holding no Commit is run over the last commit as it stands at the run, whatever state the design is in. While a design applies, that commit holds the files before the design's work. One holding a Commit is run over that commit, always. No run of a Search of a commit's files gives a design's own uncommitted writing, whenever it is run: that writing is found by the searches each later check makes afresh. No check refuses a Search for the Target it names, the design script reading nothing that shows a design's own changes are kept, so a Search of the files as they stand made while a design's uncommitted changes are kept is read as any Search of that Target is. The working files a Search names are read as they stand.

A report of research is held as any other cold agent's is: as it is handed back and as it is taken up, each Search of it giving every place is run, and the report is refused, going back to its cold agent, where its Places leave out a place the run gives. A research's Places hold every place its Search gave, whichever share assesses each, and what its Searches give is held too where the research is read together. Where a file has changed between the hand-back and the take-up, the take-up's run is held to the files as they then stand, and a place the files have gained is one the research must assess. The report is refused too for what a Search asks: the search refuses what the Search asks, a regular expression Python's `re` does not read and a code structure the search does not know among them, its term or passage reduces to no word, its citation names no place among the files, or a path it is narrowed to holds no file of its Target.

Where the research binding the design is read together, each place a Search giving every place gives, and each place a Search of the Kind "meaning" holds, lies in an area the research binding the design assessed. One outside every such area takes a first assessment, at the apply as before it, a place in a file the apply created among them. That reading tells a design each place outside every assessed area. It does not tell which assessed area's text a change rewrote, that the files changed under a Search of the Kind "meaning", or that a Search has come to ask nothing since its report was handed back. A research's Search is not held there to its own Places, so a place it gives that its record lacks is read as any place it gives. A Search the search refuses there, or one that asks nothing, gives no place and is passed over, its report no longer able to go back. A Search logged holding a Pattern is read there as it was before the record held a Kind, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has a logged report read, each place it matches lying in an assessed area. A research's Search of the working files is read at no moment but the check of its own report. The design document, a working file, is searched by a Search of its own whose Target is the working files and whose Narrowed To names it.

The Snapshot a Search holds is the code its recorder's result carried, held to the form of a snapshot code. It shows which Searches were made against the same files. No reading turns on it, and no check compares it with a code the search gives, the files being free to change between a search and the check of its report. So which files it names rests on its recorder's word.

A part of a ranking is not run again. A ranking moves with more than the files of its Target, the search ranking by words over an index that holds every target's passages, so a run could refuse a record made honestly. No check holds its Places to a run. Its record is held to its form: no more Places than its Ranking Part spans, and `none` only where its Ranking Part is `none`. Nothing kept shows that the search was made, so a check reading such a record rests on its recorder's word. No reading takes its Places for every place, and a tactical fix naming a Search of the Kind "meaning" is refused.

A tactical fix's Search reads the files of Spec of Record's scope its defect can stand in. In a report over applied work its Target is "current-operative-files" and it is narrowed to no path, so its run reads every operative file. Where the design's Target holds a fixture file, a Search asking the same of "current-fixture-files", narrowed to no path, stands beside it in the report's Searches. The fix's Places cover each place those Searches found, so a defect standing in a fixture file is fixed at every place it stands. A file of the design's Target outside the scope is read by no Search, and the builder reads it for the defect itself. In any other report, where a round's fix changes the design document alone, its Target is "working-files" and its Narrowed To names the design document. A tactical fix naming a Search of any other Target is refused.

A Search giving every place, in a report other than research's, is held at each run to the files as the run then reads them, whatever Snapshot it holds: a place it gives outside its Places refuses the report, until the search is made again and recorded. One the search refuses refuses the report too, and one that asks nothing gives no place and is held as any. The run holds the record, and nothing of whether a fix reached the places the record lists.

Once its report is taken up, a Search a cold agent recorded is run by no check of that report. The files go on changing after the take-up, by the builder's fixes among others, and a run made then would read words the cold agent's search never met. So no check refuses the report, or returns it to its cold agent, for what such a run would give. A research's Search is still run where the research binding the design is read together, and that reading is no check of the report holding it: it refuses that report for nothing, and returns none.

A Search in a report other than research's is read with its own report and never after: a cold agent's up to the take-up, and the builder's own until its report's entry is appended. So no later cycle runs it. A search narrowed to some paths cannot show it found every place outside them.

### Reviewer Reading

What one reviewer of a review read, its records in a review's report's Reading, each written by its reviewer:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Reviewer Readings \
**Reference Key:** Reviewer

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Reviewer | yes | yes | | text | its key, the name of the reviewer's file |
| Collecting Reads | no | yes | | text | the places it read collecting its findings, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written, `none` where it read none |
| Earlier Reports | no | yes | | text | the earlier reports it read between its passes, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written, `none` where it read none |
| Weighing Reads | no | yes | | text | the places it read weighing its findings, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written, `none` where it read none |

### Evidence Owed for Goals

The report author follows the first matching row. A pre-approval review here is an adversarial review or the builder's self-review for that round. Its reading names a version the log held in a major version whose goals were agreed. The reviewer judges the structural checks in [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review). A marked finding identifies the structural check it failed, the affected step Objective or the affected Frame Outcome. A reader judges whether that finding establishes the failure.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Pre-approval review?, Stopped at a structural failure?

| Pre-approval review? | Stopped at a structural failure? | Evidence owed |
|---|---|---|
| false | - | neither goal judgments nor a title field about them or the structural stop |
| true | true | Stopped At holding `the structure` and the findings explaining the stop |
| true | false | Goal Comparison and the Goal Judgments for every goal read |

### Goal Judgment

A full review states once how its goal coverage can be verified. Goal Comparison holds `compared with reviewed goals` when the set of Names and Descriptions from the version reviewed is available for independent comparison. When the reviewed set is unavailable, `reviewer's account only` identifies the reviewer as the source of the wording and answers. The reader can inspect that account but cannot independently confirm its completeness or wording. Each answer is either `met` or the key of a design flaw the reviewer upheld about that goal and that question in this report. One such finding can support both answers when it establishes both failures.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Goal Judgments \
**Reference Key:** Goal

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Goal | yes | yes | | text | the Name of the goal judged |
| Wording | no | yes | | text | the full Description the reviewer judged |
| Outcome Only | no | yes | | text | the answer to [`§ Design Goal § Semantic Checks [Name: goal-states-an-outcome]`](#semantic-checks-2) |
| Genuine Change | no | yes | | text | the answer to [`§ Design Goal § Semantic Checks [Name: goal-states-a-change]`](#semantic-checks-2) |

### Finding

A finding a check reports, of any verdict, its records in a report's Findings. A Finding whose Verdict is a mark and that is anchored in the plan names what it bears on in its Affected Goals, its Affected Frame Outcomes and its Affected Step Objectives, each Name resolved against the design its report identifies. For a goal judgment, the Finding refers to the goal as it stood in the version reviewed. Where the original goal set is unavailable, the Goal Judgment that cites the Finding supplies the goal’s Name and wording, as [`§ A Check's Report § Goal Judgment`](#goal-judgment) has the comparison disclosed. One showing the work's breach cites each rule it breaks in its Broken Rules, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) sorts a finding. A Finding names no steer: a review judges the design, so a finding pressing on a steer names the part of the design carrying the steer's choice, and the builder finds the steers behind the parts it names at settling ([`§ Steering Decision § Revisiting a Steer`](#revisiting-a-steer)). A triage's Finding may stand for the audit rows one decision settles, and is counted once:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Findings \
**Reference Key:** Finding

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Finding | yes | yes | | text | its key, its reviewer's file's name before it |
| Verdict | no | yes | | [`§ A Check's Report § Verdicts`](#verdicts) | its writer's word on it |
| Decision | no | where its Verdict is a mark | | text | the decision of the design it touches, in its writer's words |
| Affected Goals | no | no | none | text | the goals of the design it bears on, a list, one goal's Name to an item, as [`§ Design Goal`](#design-goal) has a field name a goal |
| Affected Frame Outcomes | no | no | none | text | the Frame Outcomes of the design it bears on, a list, one Frame Outcome's Name to an item, as [`§ Design Goal`](#design-goal) has a field name one |
| Affected Step Objectives | no | no | none | text | the step Objectives of the design it bears on, a list, one step Objective's Name to an item, as [`§ Design Goal`](#design-goal) has a field name one |
| Broken Rules | no | no | none | text | the rules of the canon the work's breach it shows breaks, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Description | no | yes | | text | the finding, or the observation |
| Evidence | no | where its Verdict is not a review observation | | a list of [`§ A Check's Report § Report Evidence`](#report-evidence) | its evidence |
| Rationale | no | yes | | text | what goes wrong in the work if it is left, or why it was dropped, set aside, set apart or found not caused |
| Possible Fix | no | where its Verdict is a mark | | [`§ A Check's Report § Possible Fix`](#possible-fix) | its possible fix, in the form [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) gives it |
| Lies In | no | where its Verdict is a mark and the report lies over applied work | | [`§ A Check's Report § Where a Finding Lies`](#where-a-finding-lies) | where it lies, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) places a finding |
| Lands On | no | no | none | text | the earlier change of the design's current major version it lands on, as its writer traces it, cited as [`§ A Check's Report § Settlement`](#settlement) has a Lands On cite one |

### Report Evidence

A piece of a finding's evidence, its records in a Finding's Evidence:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Report Evidence Items \
**Reference Key:** Description

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Description | yes | yes | | text | the evidence, the words quoted among it |
| Places | no | yes | | text | the places it is drawn from, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |

### Possible Fix

A finding's possible fix, in one of the two forms [`specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings`](/specs/AGENTS.md#weighing-a-reviews-findings) gives, its record in a Finding's Possible Fix:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Possible Fixes \
**Reference Key:** Kind

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Kind | yes | yes | | [`§ A Check's Report § Kinds of Fix`](#kinds-of-fix) | its form |
| Fix | no | where its Kind is tactical fix | | text | the tactical fix |
| Delivers | no | where its Kind is revision | | text | what the revision of its Finding's Decision must deliver |

### Search

A search the builder or a reviewer ran for its own check, or a cold agent ran doing research, its records in a report's Searches:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Searches \
**Reference Key:** Search

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Search | yes | yes | | text | its key, its reviewer's file's name before it where a reviewer ran it |
| For | no | yes | | text | the fact whose home it sought, the defect whose every place it found, or what the research it serves sought: a rule's reach, the frame's sweep or what restates a change |
| Goals | no | yes | | text | a list, each item the Name of a design goal ([`§ Design Goal`](#design-goal)) the search serves, so a change at the goals finds the searches it reaches; or `none` alone, where the Search was made for a check, a finding or a defect naming no goal of the design |
| Kind | no | yes | | "citers", "cited sections", "lines", "terms", "code structure", "meaning", "pattern" | the kind of search made, a Kind of a search's result, whose form `.ai/skills/search-spec-of-record-scope/` states |
| Query | no | yes | | text | what was asked, as it was given the search: a citation, a term, a structure with its name, a passage, or, where the Kind is "pattern", a regular expression |
| Exact | no | no | "no" | "yes", "no" | of a Search of the Kind "terms", whether the search was asked for exact, as its result states it, so a run of the Search asks the same, each kind of search asking as [`§ A Check's Report § Search § Who Asks for Exact`](#who-asks-for-exact) has it |
| Target | no | no | "current-operative-files" | "current-operative-files", "committed-operative-files", "current-fixture-files", "committed-fixture-files", "working-files" | the target the search was run with, one target to a Search, which a run of the Search reads; a Search logged under an earlier name of a target holds that name, read as the table of earlier names beside this type gives it and measured against the files that target reads as they then stand |
| Commit | no | no | none | text | the Commit the search's result holds, which a result holds only where its asker named a commit to the search, by its full name; a run of the Search reads that commit, and the last commit as it stands at the run where a Search of "committed-operative-files" or of "committed-fixture-files" holds none |
| Narrowed To | no | where the Target is "working-files" | | text | a list, the paths the search was narrowed to, which a search of the working files always names; a Search a tactical fix names holds no path of the operative files or of the fixture files |
| Ranking Part | no | where the Kind is "meaning" | | text | the part of the ranking read, by the numbers its places hold in the ranking, as `1 to 40`; `none` where the ranking held no place there, the Places then `none` |
| Snapshot | no | yes | | text | the snapshot code the search's result carried, in the form a search's result writes one, which `.ai/skills/search-spec-of-record-scope/` states, standing for the files of its Target as the search was made, so Searches holding one code were made against the same files |
| Places | no | yes | | text | the places the search gave, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written, `none` where it gave none; where the Kind is "meaning", no more places than its Ranking Part spans |

The Required column is asked of a Search written in this form. A Search of a report logged before the form stood is read under the field names it was written with, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has a logged report read, so nothing the column requires is asked of it.

A Search logged before a target took its present name holds the name it was logged with, read as the target this table gives:

**Reference Key:** Earlier Name \
**Required:** Read As

| Earlier Name | Read As |
|---|---|
| "current-durable-files" | "current-operative-files" |
| "committed-durable-files" | "committed-operative-files" |

The design script reads the earlier names from this table, so no code holds one.

A search made in a design's work asks a target of the files as they stand, "current-operative-files" or "current-fixture-files", for the files the design works from. It asks a target of a commit's files, "committed-operative-files" or "committed-fixture-files", for the files before a design's work, naming a commit only to ask of that one commit. A search naming no target reads the operative files, and the fixture files are read only by a search asking for them, as [`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs) has a fixture file read. While a design's uncommitted changes are kept, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has a send-back keep them, each search of the operative files or of the fixture files made for that design asks the target of a commit's files and names no commit, since the files as they stand then hold an apply's unfinished writing. A Search's Target is the target its search was run with, and its Commit the one its asker named. Which target is asked rests with whoever makes the search: no check holds a recorder to it, as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has it.

Each Search names in its Goals the goals of the design it serves, each the Name of a goal the design holds: the goals the research it serves was made for, or the goals of the part of the design its check or its tactical fix bears on. A Search serving no goal of the design holds `none` alone, and only these may: a reviewer's Search, its key opening with its Reviewer Reading's key and a hyphen, made for a check or a finding that rests on a rule alone; a Search in the report of an audit's triage, made for a defect the design did not cause; and a Search a tactical fix's Proposed Change names, where each Finding its Cause settles names no goal in its Affected Goals. Whether a reviewer's or a triage's Search serves no goal rests on its recorder's word. A Search holding `none` counts toward no goal's Searches, and no Search in a report of research holds it.

#### Who Asks for Exact

Whether a search by terms asks for exact is decided by its purpose, as this table has each kind of search ask:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Search \
**Annotations:** Why \
**Input Values:**
  - Search: "research's", "the builder's, a reviewer's or another cold agent's own, for its check", "a reader's search by wording for replaced wording", "a round's tactical fix's", "a tactical fix's made outside a round's Causes", "`--check-retired-wording`", "`--show-reach`"

| Search | Asks for exact | Why |
|---|---|---|
| "research's" | no | research asks where the files say something, a sentence with words between can say it, and a place research leaves out is an area no one assessed |
| "the builder's, a reviewer's or another cold agent's own, for its check" | no | it looks for where a fact already stands, to find its home or a second statement of it, so it needs every way the fact is worded |
| "a reader's search by wording for replaced wording" | no | it looks for each passage still stating the old fact, and a passage holding the phrase's words apart can still state it |
| "a round's tactical fix's" | yes | the fix starts from a known defect in wording, and its Searches prove it reached every place the defect's exact wording stands. A sentence holding the words apart is other wording that may still use the term, as "the operative and fixture files" uses "operative files". The builder reads such a use for the defect itself, and the Searches hold only the exact wording |
| "a tactical fix's made outside a round's Causes" | no | the fix names no Search and no check holds it to one, so a search the builder makes for it is its own, finding every place the wording stands, together and apart; the builder fixes each place the exact wording stands and reads each place marked words apart for the defect itself |
| "`--check-retired-wording`" | yes | asked in the design script's code, it proves a retired phrase's exact wording no longer stands; words standing apart are other wording, which a reader's search by wording reads for the old fact |
| "`--show-reach`" | yes | asked in the design script's code, it lists the lines a change must rewrite because they hold the exact wording of the phrase it retires; a line holding the words apart is other wording, which a reader's search by wording reads for the old fact |

### Read Assessment

How an area of the files bears on a design, as the cold agent doing research ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) judged it, its records in a report's Read Assessments. The cold agent assesses each place it reads, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research assessed. The most specific Area holding a place decides that place's Impact, so a file assessed `none` may hold a section assessed `changes`. An area holding both `applies` and `changes` is followed as changed, as [`§ A Design Document § A Form the Methodology Is Still Adding § A Design Changing the Process`](#a-design-changing-the-process) has a design run under the process rules it writes. A Read Assessment says how its area bears on the design and never where the area goes, into the frame, the Out of Scope, a canon design's Impact on the Application Specs or the user's hands, which is the builder's or the user's to decide, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) has the call made:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Read Assessments \
**Reference Key:** Area

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Area | yes | yes | | text | the area it judges, a file or a section, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Impact | no | yes | | text | a list, each item a member of [`§ A Check's Report § Read Assessment § Read Assessment Impacts`](#read-assessment-impacts): `none` alone, or one or both of `applies` and `changes` |
| Reason | no | yes | | text | why the area bears on the design as its Impact says, the words it draws on quoted among it |
| Goals | no | yes | | text | a list, each item the Name of a design goal ([`§ Design Goal`](#design-goal)) the assessment was made for, so a change at the goals finds the assessments it reaches |
| Assessed Again For | no | where a research report binding the design already assesses its Area | | text | the cause the area is assessed again for, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has an area assessed again: the Entry of the `steer` entry marking a set of steers, or a finding, cited as a part of the report holding it |

Two research reports assess one area only where their Areas are the same. A section within a file another report assesses is the more specific Area, and decides for itself.

#### Read Assessment Impacts

How an area bears on the design, held by a Read Assessment and an Assessed Area:

**Reference Key:** Impact \
**Required:** Means

| Impact | Means |
|---|---|
| none | the area bears on the design in no way |
| applies | the design follows the area, as a rule or a form it is shaped by |
| changes | the design changes the area |

### Trace

A Trace records the builder's judgment of coverage before the apply and the paths it traces through the applied mechanism afterward. Its records sit in a report's Traces:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Traces \
**Reference Key:** Trace

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Trace | yes | yes | | text | its key |
| Mechanism | no | yes | | text | the mechanism traced or asked of, cited by the section holding it, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Outcome | no | where the report is a self-review's before the apply, unless a `plan-approval` entry of the phase stands before it with no `another-round` entry after it | | [`§ A Check's Report § Mechanism Outcomes`](#mechanism-outcomes) | the outcome [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether a Changed Mechanism Serves a Goal`](/specs/AGENTS.md#whether-a-changed-mechanism-serves-a-goal) gives it, asked of a mechanism the steps change, from the steps' What and Objectives, with no rows |
| Paths | no | where the report lies over applied work | | a list of [`§ A Check's Report § Trace Path`](#trace-path) | each path traced through the text the apply wrote |

### Trace Path

A path of a traced mechanism, its records in a Trace's Paths:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Trace Paths \
**Reference Key:** Path

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Path | yes | yes | | text | the path, named by its row's or its transition's cells where the mechanism is a Decision Table or a State Machine, and otherwise by the route it takes |
| Result | no | yes | | text | what the path does, and whether it upholds what its check judges the mechanism against, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism`](/specs/AGENTS.md#tracing-a-mechanism) has a path judged after the apply |

### Builder Check

A check only the builder makes, its records in a report's Builder Checks:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Builder Checks \
**Reference Key:** Check

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Check | yes | yes | | text | its key |
| Kind | no | yes | | [`§ A Check's Report § Kinds of Builder Check`](#kinds-of-builder-check) | which check it is |
| Places Checked | no | yes | | text | what it was made of, citing the item it is required for where [`§ A Check's Report § Kinds of Builder Check`](#kinds-of-builder-check) requires one for each, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Result | no | yes | | text | what it found, a miss's question with the answer the work gave it |

### Cause

A cause of a round settled at its causes, its records in a report's Causes, each holding its Misses and its Proposed Change. A Cause's Proposed Change is the change the round proposes at it, made once the round is settled. Where the Cause settles a tertiary finding, or its Proposed Change reaches a tertiary place, the change waits for the user's call there, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) has the builder stop. The change is then made as the user's decision has it, and each Settlement naming the Cause records that decision in its User Decision. Where the user's call hands the line on or cuts it off, the Proposed Change holds nothing the call leaves out.

A Cause holding no Proposed Change, its nits left or a Settlement naming it placing its findings in `the plan` or `handed on`, says why in the How Settled of each Settlement naming it. A Cause continuing an earlier round's cites it by that round's report and its key, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Causes \
**Reference Key:** Cause

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Cause | yes | yes | | text | its key |
| Decision | no | yes | | text | the name the builder gives the concept the findings it settles touch, kept across the phase's rounds |
| Continues | no | no | none | text | the earlier round's cause it continues |
| Outcome | no | where Continues is held | | [`§ A Check's Report § Mechanism Outcomes`](#mechanism-outcomes) | the outcome [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether a Changed Mechanism Serves a Goal`](/specs/AGENTS.md#whether-a-changed-mechanism-serves-a-goal) gives it |
| Conflicting Steers | no | no | none | text | each steer it presses on, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Weigh the Steers`](/specs/AGENTS.md#weigh-the-steers) has it weighed, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Misses | no | where it settles a design flaw or an implementation flaw | | a list of [`§ A Check's Report § Miss`](#miss) | why the builder's pass and self-review let each flaw through, checked under [`§ A Check's Report § Cause § When a Cause Holds Misses`](#when-a-cause-holds-misses) |
| Proposed Change | no | where it settles a flaw, no Settlement naming it giving Lies In the plan or handed on in a post-apply round | | [`§ A Check's Report § Proposed Change`](#proposed-change) | the change the round proposes at it, a Cause settling only nits holding one where the round fixes them |

#### When a Cause Holds Misses

The Settlements available to check a Cause are the round's own and those of its selected judgments under [`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round). Ownership is known at first settlement and on recheck of an entry with Settled Judgments. A flaw in this decision is a design flaw or an implementation flaw.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** A flaw cites this Cause?, Ownership known?

| A flaw cites this Cause? | Ownership known? | Misses on this Cause |
|---|---|---|
| true | - | required |
| false | true | absent |
| false | false | optional |

### Miss

Why the builder's own pass and self-review let a flaw through, as [`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md) defines a miss, its records in a Cause's Misses:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Misses \
**Reference Key:** Miss

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Miss | yes | yes | | text | its key |
| Kind | no | yes | | "place not read", "place read stale", "place read in part", "question not asked" | the miss's kind |
| Place | no | where its Kind is not `question not asked` | | text | the place missed, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Reads | no | where its Kind is not `question not asked` | | text | the places the builder then read for it, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Question | no | where its Kind is question not asked | | text | the question not asked |
| Answer | no | where its Kind is question not asked | | text | the answer the work gave the question, asked before the round's change was proposed |

### Proposed Change

The change a round proposes at a cause, its record in a Cause's Proposed Change. Each place it changes is ordered and traced as [`§ A Check's Report § Proposed Change § Changed Place`](#changed-place) has it:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Proposed Changes \
**Reference Key:** Kind

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Kind | yes | yes | | [`§ A Check's Report § Kinds of Fix`](#kinds-of-fix) | the change's kind |
| Search | no | where its Kind is tactical fix | | text | the search that found every place its defect stands |
| Reason | no | where its Kind is tactical fix | | text | why its fix is a tactical one |
| Decision Rewritten | no | where its Kind is revision | | text | the decision it rewrites whole |
| Places | no | yes | | a list of [`§ A Check's Report § Proposed Change § Changed Place`](#changed-place) | the places it changes |

#### Changed Place

A place a change the builder makes changes, its records in a Proposed Change's Places and a Settlement's Places, ordered as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) orders a change's places:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Changed Places \
**Reference Key:** Place

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Place | yes | yes | | text | the place changed, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Order | no | yes | | [`§ A Check's Report § Settlement § Orders`](#orders) | its order |
| Settles | no | where its Order is primary | | text | the findings whose fix it is, a list, one Finding's key to an item |
| Follows | no | where its Order is secondary or tertiary | | text | the place of the same change it follows, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written: a secondary place's the primary place it aligns with, and a tertiary place's the secondary place whose change made it needed |

### Settlement

How the builder settled one or more findings sharing a verdict, its records in a report's Settlement's Settlements. Whatever became of a kept finding, its Settlement holds the finding's two indicators ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), in fields of their own and in the builder's own words. A finding The Test drops has no fix, so its Settlement holds what requires it, as The Test justified it, and the reason it is dropped, and no authority over a fix. Either Settlement holds its findings' order and lineage too, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) gives them. Where they land on an earlier change of the design's current major version, its Lands On cites that change by its report and its key, one place as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written: the Cause whose Proposed Change made it, or the Settlement whose Places record it. Its Lands On is the builder's own word on the lineage. It answers each earlier change a finding it settles names, whether the finding lands on that change, on another or on none. Where it departs from a finding it settles, in its Verdict, its Lies In or its Lands On, or in a change settling less than the finding's Possible Fix reaches, its Departure Reason holds why, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) has a departure weighed. Where its findings' fix is made with no Cause of the report carrying it, as in an audit's triage, a nit fixed after the apply or a self-review's fix, each place the fix changes is a record of its Places:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Settlements \
**Reference Key:** Settlement

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Settlement | yes | yes | | text | its key |
| Settled Findings | yes | yes | | text | the findings it settles, one or more sharing its other fields, a list, one Finding's key to an item |
| Verdict | no | yes | | [`§ A Check's Report § Verdicts`](#verdicts) | the builder's last word on them |
| Required By | no | yes | | [`§ A Check's Report § Settlement § Requirements`](#requirements) | what requires them, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) has a finding justified |
| Justifying Goals | no | where its Required By names the goals | | text | the goals of the design their fix helps deliver, a list, one goal's Name to an item, as [`§ Design Goal`](#design-goal) has a field name a goal |
| Justifying Rules | no | where its Required By names the rules | | text | the rules of the canon the design's own text breaks without their fix, a list as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written |
| Assessment | no | yes | | text | the builder's assessment of them: how their fix helps deliver each goal it names and how the design's own text breaks each rule it names, or, where nothing requires them, why |
| Order | no | yes | | [`§ A Check's Report § Settlement § Orders`](#orders) | their order |
| Fix Authority | no | where its Verdict is other than dropped | | [`§ A Check's Report § Settlement § Fix Authorities`](#fix-authorities) | whose authority they are fixed or left on: where their fix is made or proposed, whose [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Whose Fix It Is`](/specs/AGENTS.md#whose-fix-it-is) gives it; where they are left, whose call left them |
| User Decision | no | where its Fix Authority is the user's | | [`§ A Check's Report § Settlement § User Decisions`](#user-decisions) | the decision the user made on them |
| Lies In | no | where its Verdict is a mark and the report lies over applied work | | [`§ A Check's Report § Where a Finding Lies`](#where-a-finding-lies) | the builder's last word on where they lie, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review) has the builder settle a finding by where it lies |
| Cause | no | where the report holds Causes and its Verdict is a mark | | text | the cause they lie in |
| Lands On | no | where they land on an earlier change of the design's current major version, or a finding it settles names one | | text | the earlier change they land on, whatever their order, or `none` where a finding names one they do not land on |
| Departure Reason | no | where it departs from a finding it settles | | text | why the builder departs from the finding's writer |
| Carried By | no | no | none | text | the Name of the step whose rework carries them into the rebuilt plan, where a send-back leaves their fix to the rework of their text, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has it |
| Places | no | where its findings' fix is made and no Cause of the report carries it | | a list of [`§ A Check's Report § Proposed Change § Changed Place`](#changed-place) | the places their fix changes |
| How Settled | no | yes | | text | what became of them, whatever moved the work on: the fix made, or proposed and left unmade; the plan's outcome carrying them; the text the rework replaced; the user's choice, the user's answer to each call the builder brought among it; or that the design did not cause them |

#### Orders

A finding's or a changed place's order, held by a Settlement and a Changed Place:

**Reference Key:** Order \
**Required:** Means

| Order | Means |
|---|---|
| primary | a primary finding or place, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) tells one |
| secondary | a secondary finding or place, as that section tells one |
| tertiary | a tertiary finding or place, as that section tells one |

#### Requirements

What requires the findings a Settlement settles, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) has a finding justified, held by a Settlement:

**Reference Key:** Required By \
**Required:** Means

| Required By | Means |
|---|---|
| the goals | goals of the design their fix helps deliver, which its Justifying Goals name |
| the rules | rules of the canon the design's own text breaks without their fix, which its Justifying Rules name |
| the goals and the rules | both, each named in its field |
| nothing | no such goal and no such rule, its Assessment saying why |

#### Fix Authorities

Whose authority a Settlement's findings are fixed or left on, held by a Settlement:

**Reference Key:** Fix Authority \
**Required:** Means

| Fix Authority | Means |
|---|---|
| the builder's | the builder's own, within the calls [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) gives it |
| the user's | the user's decision, on a call that section gives the user |

#### User Decisions

The decisions the user makes on findings whose Fix Authority is the user's, held by a Settlement. Those whose Tertiary Option is yes are the options the builder brings at a tertiary finding or place, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage`](/specs/AGENTS.md#order-and-lineage) has the builder stop:

**Reference Key:** User Decision \
**Required:** Tertiary Option, Means

| User Decision | Tertiary Option | Means |
|---|---|---|
| fix approved | no | the user approves a fix, the builder's recommendation or one the user gives, and it is made |
| left as it stands | no | the user leaves them as they stand, and no fix is made |
| sent back | no | the user sends the design back, and its rework carries them, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has it |
| carried by the approval | no | the user's approval of the plan or of the applied result ends the round, and they stand as the approved text has them |
| taken by the step back | no | the check holding them was stopped at the step back, cut short by a run reaching its length, or cut short by the design reassessment the user chose after it was continued past the step back, and what the user decides at the step back takes them: a design reassessment's diagnosis, the plan's approval or abandoning, or, where a set of steers closes there instead, the set's change |
| taken by a changed foundation | no | the check holding them had not ended its settling as the design was freed from a name of a finished or gone design, whether it was still running, handed back and not yet taken up, or being settled, and was cut short by that design reassessment: they bind nothing and go to no diagnosis and no round, the design being made afresh |
| carried by a steer | no | a steer the user gives decides them, recorded as [`§ Steering Decision § When a Steer Is Recorded`](#when-a-steer-is-recorded) has it |
| widen the goals | yes | the user widens the goals to take the line in, by a steer, and the tertiary fix is made under the widened goals |
| cut at the secondary | yes | the line is cut off at its secondary: no tertiary fix is made, and the secondary stands |
| remove at the root | yes | the change at the line's primary is removed, and each change down the line with it |
| hand on | yes | the line is handed on as a migration, spawned as a design or logged as a follow-up, as [`§ A Design Document § Spawning a Change of Its Own`](#spawning-a-change-of-its-own) has a change of its own handed on |

### Verdicts

A finding's verdict, held by a Finding and a Settlement:

**Reference Key:** Verdict \
**Required:** Counted In, Means

| Verdict | Counted In | Means |
|---|---|---|
| design flaw | Design Flaws | a design flaw, as [`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md) defines one |
| implementation flaw | Implementation Flaws | an implementation flaw, as the glossary defines one |
| nit | Nits | a nit, as the glossary defines one |
| dropped | Dropped | a finding [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test`](/specs/AGENTS.md#the-test) drops |
| set aside | none | a finding the user judged wrong, before the plan's approval or after it, as [`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Whose Fix It Is`](/specs/AGENTS.md#whose-fix-it-is) sets one aside |
| review observation | none | a review observation, as the glossary defines one |
| not caused | none | an audit's finding the design did not cause |

### Where a Finding Lies

Where a finding over applied work lies, held by a Finding and a Settlement:

**Reference Key:** Lies In \
**Required:** Means

| Lies In | Means |
|---|---|
| the plan | it lies in the plan, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) places a finding |
| the writing | it lies in the writing, as that section places a finding |
| handed on | it is on text whose migration the frame hands on, or in a file the design's Kind does not let it change, each handed on as [`§ A Design Document § Changes After Approval`](#changes-after-approval) has it |

### Kinds of Fix

A fix's kind, held by a Possible Fix and a Proposed Change:

**Reference Key:** Kind \
**Required:** Means

| Kind | Means |
|---|---|
| tactical fix | the fix made at every place its defect stands |
| revision | the decision the finding touches revised whole |

### Mechanism Outcomes

The outcome [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether a Changed Mechanism Serves a Goal`](/specs/AGENTS.md#whether-a-changed-mechanism-serves-a-goal) gives, held by a Trace and a Cause:

**Reference Key:** Outcome \
**Required:** Means

| Outcome | Means |
|---|---|
| cover the mechanism | the Trace or Cause records that the mechanism is covered |
| miss the mechanism, a design flaw | the Trace or Cause records a gap that requires design-flaw triage |
| not asked | the coverage test does not apply to this case |

### Kinds of Builder Check

The checks only the builder makes, held by a Builder Check, each with the self-reviews it is required in:

**Reference Key:** Check Kind \
**Required:** Means, Required

| Check Kind | Means | Required |
|---|---|---|
| steers against the user's messages | each steer's quoted words and its decision checked against every message of the user's the builder still holds | in every self-review |
| linked work | the work the design hands on, each item of its Out of Scope handing work on and each item of its Impact on the Application Specs, checked as held where the step handing it on sends it. Work handed to a spawned design is read only from the design script's `--show-design`, which shows that design's header and its goals, and never from the design itself, since a builder opens no design but the one it is working. Where the showing names a field as missing or not valid, the builder treats that design as old and suspect and goes on with the design it is working. Nothing brings the other design to the form in force before its own builder takes it up ([`§ The Working Files`](#the-working-files)). Work logged as a follow-up is read from `.ai/follow-ups.md`. The lineage of both is checked by the workstack check of the skill writing the design, as its validating state runs it | in every self-review |
| user edit | an edit a `user-edit` entry names checked against the design and the rest of the applied work, each concern brought to the user with the builder's recommendation, an Objective the edit leaves unmet among them, the user keeping the edit or having it adjusted | in every self-review, for each `user-edit` entry since the design's last `self-review` entry, citing its places |
| worked case | a case worked through a Cause's change or an implementation flaw's settlement, read for what it means and not only for whether it passes its checks | in a self-review following a round's change, for each Cause holding a Proposed Change and each implementation flaw the round settles, citing it |
| miss's question | a question a Miss names asked of the work, with the answer the work gave, showing what the builder's reading lacked | in every self-review of a phase holding a Miss naming a question, for each Question a Miss of the phase names, citing its Cause |
| construct choice | the record of the count [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) has the builder make: each passage the count reached, with the form the count gives it. Where none of the work falls in the files [`specs/methodology/modeling-constructs.md § Purpose`](/specs/methodology/modeling-constructs.md#purpose) sets the constructs for, it holds the work's places and states that none falls in them | in every self-review over applied work of a design whose Kind is `canon-specs` or `application-specs` |
| differential test | a test of a script the diff changes against its version at the last commit, the kind turning on the script. Of every script but the design script, it is an ephemeral differential test ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), which the builder runs in the files on inputs it picks. Of the design script, it is the kept comparison, which is no ephemeral test: the design script runs it over the designs of the plans folders as the self-review's report is validated, the builder picks no inputs for it, and the builder records its judgment of each design the comparison lists, as a difference the change meant or a fault | in a self-review over applied work, for each script the diff changes, citing it, and, where the comparison is run, for each design it lists; in a pass proving the fixes, for each such script its Reads cover |
| problem re-evaluation | the builder's reading of each place the design's Problem cites against the files as they stand, made before goals are proposed in a major version, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has the Problem read again, with what the files no longer bore out and how the Problem was brought to them | in the first self-review of each major version, its Places Checked covering each place the Problem cites |
| diagnosis answered | what in the rebuilt design answers a root cause or a flaw of the diagnosis it is rebuilt from, a flaw a later change fixed among them | in the self-review before a rebuilt design's first adversarial round, for each Root Cause and each Flaw of that diagnosis |
| carried finding | a finding carried from a report over an apply the design was sent back from, checked as taken into the rebuilt goals, frame or steps, as [`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back) has a send-back carry it | in every self-review after a send-back and before the plan's next approval, for each Finding of such a report, while it binds the design ([`§ A Check's Report § Over Applied Work, and a Phase's Record`](#over-applied-work-and-a-phases-record)), whose Settlement gives Lies In `the plan` or a Carried By, citing it |
| cycle's changes | the trace of each line a Refactor and Refine cycle's changes show, as `.ai/skills/design-specs/` has a cycle trace them | where a cycle's changes are traced, citing each place `--show-refactor-and-refine-of-existing-specs` lists |

### Script Checks

**Records:**
  - **Name:** report-stamped-only-where-its-checks-pass \
    **Tests:** a settled report is stamped only where every check of it the design script makes passes, the kept tests of a self-review over applied work run and passing among them, and a report holding a stamp is cleared of it where they no longer pass, as [`§ A Check's Report § A Report's Stamp`](#a-reports-stamp) has a report stamped \
    **Reads:**
      - `canon-specs`
      - `fixture-files`
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--stamp-settled-report`
      - `.ai/skills/implement-specs/` `--stamp-settled-report`

  - **Name:** cold-parts-kept \
    **Tests:** a report a cold agent wrote holds, as it is handed back, no part the builder or the design script writes; and, once the builder takes it up, a Hand-back holding a fingerprint of each part the cold agent wrote, each such part still matching it, the builder's own Searches after a review's Searches aside, as [`§ A Check's Report § Who Writes Each Part`](#who-writes-each-part) has each hand write only its own parts \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

  - **Name:** report-in-its-form \
    **Tests:** each report a check's entry names holds the parts required by its kind, phase and stopping point in their order, with the fields and records their form gives them. Its goal judgments hold the wording, two answers and comparison basis [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has checked \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

  - **Name:** findings-anchored-in-the-design \
    **Tests:** each Finding whose Verdict is a mark, in a report a check's entry names, names in its Affected Goals, Affected Frame Outcomes or Affected Step Objectives what it bears on, each Name resolved as [`§ A Check's Report § Finding`](#finding) requires, or cites in its Broken Rules the rules it breaks, as [`§ A Check's Report § Finding`](#finding) has a finding name what it bears on \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

  - **Name:** report-laid-out \
    **Tests:** each report a check's entry names is laid out as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) and [`specs/methodology/spec-style/markdown.md § Blank Lines`](/specs/methodology/spec-style/markdown.md#blank-lines) have a block of fields laid out \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

  - **Name:** findings-settled-once \
    **Tests:** each Finding of a report a check's entry names is settled by exactly one Settlement \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** settlements-justified \
    **Tests:** each Settlement of a report a check's entry names holds its two indicators as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) reads them: its Justifying Goals and Justifying Rules as its Required By names them, each goal one the design holds; and, where its Verdict is other than dropped, its Fix Authority, the user's wherever the report shows the call the user's, with the User Decision it holds, and none where its Verdict is dropped \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** orders-follow-their-lineage \
    **Tests:** each Settlement and each Changed Place of a report a check's entry names states the order its lineage gives, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) works it out, each Settles naming findings its change settles, and each Follows naming a place of its own change \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** recorded-judgments-name-eligible-reports \
    **Tests:** on recheck of an entered review, its recorded judgment keys have the order given by [`§ Design Log Entry`](#design-log-entry) and each identifies a distinct eligible report under [`§ A Check's Report § A Judgment Settled with a Round`](#a-judgment-settled-with-a-round) \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** report-keys-name-records \
    **Tests:** each key a report cites names a record a report of the design's current major version holds, each Lands On a Cause or a Settlement, and each Settlement's Carried By names a step the design holds, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

  - **Name:** departures-reasoned \
    **Tests:** each Settlement of a report a check's entry names holds its Departure Reason wherever it departs from a finding it settles in Verdict, in Lies In or in Lands On, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) finds a departure \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** searches-cover-their-matches \
    **Tests:** each Search a report holds whose Kind gives every place covers in its Places each place the search it records gives, each place counting as its citation alone, run asking for exact where its Exact is "yes" and as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has it run: the builder's own as its report is checked, and one a cold agent recorded, research's among them, as its report is handed back and as it is taken up, and by no check after the take-up; each Search in a report of research whose Kind gives every place is one the search can run whose term or passage reduces to some word, and one whose citation names a place and whose paths each hold a file; each Search of the Kind "terms" holds, written or read as its default, the Exact the table of [`§ A Check's Report § Search`](#search) gives its kind of search, a Search being a round's tactical fix's where a Proposed Change that is a tactical fix names it or it is the Search of "current-fixture-files" standing beside one so named, research's where it stands in a report of research, and otherwise the builder's, a reviewer's or another cold agent's own; each Search of the Kind "meaning" holds no more Places than its Ranking Part spans, and `none` only where its Ranking Part is `none`; each Search's Snapshot is in the form of a snapshot code; and each Search's Goals name goals the design holds, or hold `none` alone where the Search is a reviewer's, stands in the report of an audit's triage, or is named by a tactical fix each of whose settled Findings names no goal \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--take-up-report`

  - **Name:** reads-assessed \
    **Tests:** in a report holding Read Assessments, each place the builder named, held in its Reads, lies within the Area of one of its Read Assessments, as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has one place cover another \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--take-up-report`

  - **Name:** area-reassessments-name-their-cause \
    **Tests:** as a report of research is handed back and as it is taken up, and at no check after, each of its Read Assessments whose Area a research report binding the design already assesses holds its Assessed Again For, naming a cause that counts against each such earlier report, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has a cause count \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--take-up-report`

  - **Name:** research-covers-its-matches \
    **Tests:** each place a Search of the research binding the design gives where its kind gives every place, and each place a Search of that research of the Kind "meaning" holds, lies within the Area of a Read Assessment in that research, whichever report holds the Search, each Search read as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has one read where the binding research is read together: `--check-settled-report` reads it of the report of each entry [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) names, and the validation review reads it of a design not yet approved alone, never of one approved, applying or complete \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-design`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-design`

  - **Name:** goals-searched-over-every-operative-file \
    **Tests:** among the research binding a design, read together where [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it read, each goal the design holds is named in the Goals of Searches of the Kind "terms" whose Target is "current-operative-files", or "committed-operative-files" with no Commit, and whose Narrowed To together leave no operative file out, so that every operative file is searched for the goal, and in the Goals of Searches of the Kind "meaning" of those Targets whose Narrowed To together leave no operative file out, so that each is ranked over every operative file, a Search of the Kind "meaning" counting as searching only the files its Places hold, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has each goal searched, the operative files being those the last commit holds, or those standing where the project is under no version control, a Target logged under an earlier name read as the table of earlier names gives it, no Search run, and a Search logged before a Search held a Kind counting for nothing \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-design`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-design`

  - **Name:** traces-name-their-paths \
    **Tests:** a self-review's report holds a Trace of each construct its phase traces, naming each of its paths where the report lies over applied work, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** builder-checks-required \
    **Tests:** a self-review's report holds each Builder Check required of it, covering each item it is required for, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** reads-cover-the-misses \
    **Tests:** a self-review's report following a round's change covers in its Reads each place a Miss of the phase names, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** earlier-reports-listed \
    **Tests:** a round's settlement lists in its Earlier Reports each report of the phase's record before the round, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** settling-reads-cover-the-evidence \
    **Tests:** a round's settlement covers each place the Evidence of a Finding whose Verdict is a mark names, by its Settling Reads or by the Area of a Read Assessment in the report of a handed-off judgment the design's log names, as [`§ A Check's Report § What the Design Script Checks`](#what-the-design-script-checks) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** tactical-fixes-cover-their-searches \
    **Tests:** a Proposed Change that is a tactical fix names a Search whose Kind gives every place, whose Target is "current-operative-files" with no Narrowed To in a report over applied work, a Search of "current-fixture-files" standing beside it where the design's Target holds a fixture file, and "working-files" with the design document among its Narrowed To in any other, and covers in its Places each place those Searches found, as [`§ A Check's Report § What the Design Script Checks § Reading a Search`](#reading-a-search) has it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-settled-report`

  - **Name:** places-in-their-form \
    **Tests:** each value holding places in a report a check's entry names is in the form [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) gives it \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-settled-report`
      - `.ai/skills/design-specs/` `--check-handed-back`
      - `.ai/skills/implement-specs/` `--check-settled-report`
      - `.ai/skills/implement-specs/` `--check-handed-back`

## A Diagnosis

The record a design reassessment chosen at the step back keeps of what it found, a working file of its own in the design's folder, sitting as [`§ The Working Files`](#the-working-files) has a diagnosis sit. The `design-reassessment` entry whose Cause is a step back names it, and a design reassessment made for a changed foundation keeps none ([`§ Design Log Entry`](#design-log-entry)). It takes its parts from this table, each required, and its template is [`specs/methodology/working-files/diagnosis-form-template.md`](/specs/methodology/working-files/diagnosis-form-template.md).

**Reference Key:** Part \
**Required:** Heading, Holds

| Part | Heading | Holds |
|---|---|---|
| Title | `# Diagnosis`, with the fields Design, Design Reassessment, Flaw Set and Earlier Diagnoses | the design, by its Name; the `design-reassessment` entry naming the diagnosis, by its kind and its count; the reports of every major version its flaws are read from; and the diagnoses it read, each a path as [`§ A Check's Report § A Value Holding Places`](#a-value-holding-places) has a value holding places written, or none |
| Flaws | `## Flaws`, a record section of Flaws | each flaw of the flaw set, as [`§ A Diagnosis § Flaw`](#flaw) has it |
| Root Causes | `## Root Causes`, a record section of Root Causes | each root cause the flaws fall under, as [`§ A Diagnosis § Root Cause`](#root-cause) has it |
| Scope | `## Scope`, with the fields Question and Answer | its answer to whether the scope is too narrow or too wide |

### Flaw

A flaw of a diagnosis's flaw set, the findings [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a diagnosis collect, its records in a diagnosis's Flaws.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Flaws \
**Reference Key:** Flaw

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Flaw | yes | yes | | text | its key, the citation of a finding of the flaw set |
| Still Applies | no | yes | | "yes", "no" | whether the flaw still applies, as the diagnosis judges it, so the rebuild knows whether it must still remove it |
| Why Not | no | where its Still Applies is no | | text | why the flaw no longer applies, the change that fixed it |
| Root Cause | no | yes | | text | the Root Cause it falls under, whether or not the flaw still applies |

### Root Cause

A root cause a design reassessment found reading its flaws together, its records in a diagnosis's Root Causes.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Root Causes \
**Reference Key:** Root Cause

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Root Cause | yes | yes | | text | its key |
| Question | no | yes | | text | the question that found it, one of those [`specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs`](/specs/AGENTS.md#the-runs) has a diagnosis ask or another the builder asks of the flaws |
| Description | no | yes | | text | what it is |
| Account | no | yes | | text | how the rebuild is to answer it, which the rebuilt design's self-review holds it to |

### Script Checks

**Records:**
  - **Name:** diagnosis-whole-and-in-form \
    **Tests:** each `design-reassessment` entry whose Cause is a step back, an entry holding no Cause read as one, names a diagnosis standing in the design's folder, numbered by its count among the design's diagnoses as [`§ The Working Files`](#the-working-files) has a diagnosis named, and holding the header fields and the parts its form gives it, its Scope part among them; a [`§ A Diagnosis § Flaw`](#flaw) record for each finding of its flaw set, read from the reports of every major version, each holding its Still Applies, its Root Cause, that Root Cause one the diagnosis holds, and its Why Not where its Still Applies is no; and each [`§ A Diagnosis § Root Cause`](#root-cause) record holding its Question, its Description and its Account; an entry whose Cause is a changed foundation asked for no diagnosis, and an entry written before the diagnosis asked for none \
    **Reads:**
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

## Retired Phrase

A design retiring wording records it, so the builder's tools, not a rereading, find every place the wording stands. The design script's `--show-reach` lists each place the wording stands at drafting, in whatever form it takes, a plural and an identifier among them, found as `.ai/skills/search-spec-of-record-scope/` finds a term asked for exact, as [`§ A Check's Report § Search § Who Asks for Exact`](#who-asks-for-exact) has `--show-reach` ask. Its `--check-retired-wording` reports any left in the Target's files and in each file created under a Target directory, found the same way. Both read the operative files, and each fixture file the design's Target holds. A fixture file no Target holds is read for no design's wording. A fixture keeping the wording on purpose is named in the phrase's Stays Right. The showing reads those files as they stand and, while a design's uncommitted changes are kept, as the last commit held them ([`§ A Design Document § The States It Moves Through § A Send-back`](#a-send-back)). The check reads them as they stand. Neither reads a file of the Target outside Spec of Record's scope, which the builder reads itself. Both are run as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review`](/specs/AGENTS.md#the-self-review) has it. A phrase the user turned down while steering is recorded as one too.

A design's retired wording sits in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Retired Phrases \
**Reference Key:** Phrase

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Phrase | yes | yes | | text | a word or phrase the design stops using in one sense, found as the search finds a term asked for exact, in whatever form it takes |
| Replacement | no | yes | | text | what the design uses instead |
| Stays Right | no | no | none | text | the places the phrase stays right, each a path, its section after it where the place is one, separated by semicolons |

## Steering Decision

A design's Steering Decisions record only the user's steers, the decisions a steering decision records ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), such as new scope or a design flaw's fix. A steer differs from the user's direction about how the work proceeds, from the user's feedback on the applied result and from a decision about other work, as [`§ Steering Decision § Telling a Steer Apart`](#telling-a-steer-apart) tells them apart.

**A go-ahead to take in findings.** It is a steer for the findings that change what the design is, and direction for the tactical fixes ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)). An answer carrying both is recorded for the part that decides the design.

A design's steering decisions sit in its record section of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Steering Decisions \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | a short name for what was decided |
| Prompted By | no | yes | | text | what the steer answered: a question, proposal or account the builder gave, with the options it offered where it offered any, a review's finding named by its ID, or the user's own initiative |
| Type | no | yes | | "agreement", "directive" | an agreement or a directive, as [`§ Steering Decision § A Steer's Type`](#a-steers-type) has it |
| Steer | no | yes | | text | the user's own words, quoted |
| Decision | no | yes | | text | the essence of what the steer decided, in a sentence or two |
| Changes | no | where a `steer` entry ([`§ Design Log Entry`](#design-log-entry)) names it | | "the goals", "the Scope", "the Assessed Areas", "the Approach", "the Frame Outcomes", "the steps", "Out of Scope item", "none" | a list, an item to each part of the design whose decision the steer changes, the parts ranked in the order of these values from the highest; `Out of Scope item` where the steer approves an item of the design's Out of Scope as it is written, or `none` where it changes no decision. A single value is a list of one. The highest part the steers its set's entry names change shows where the design is rebuilt from |

### When a Steer Is Recorded

Each steer is recorded once, in the Steering Decisions, when it is given. The steers the user gives are gathered into a set of steers ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), a single steer a set of one, weighed and closed as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers`](/specs/AGENTS.md#a-set-of-steers) has a set closed. The set's one `steer` entry logs it as it closes, naming each of its Steering Decisions, appended as [`§ Design Log Entry`](#design-log-entry)'s kinds table has it. A steer recorded whose set has not yet closed has no entry, so it ends no round and raises nothing. The design is then rebuilt once, from the highest part the set's steers change, before its work goes on, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`](/specs/AGENTS.md#the-order-of-a-designs-parts) has a change rebuild, so the design carries how it was formed and never lags a steer it records. A set of steers changing the goals or the frame is confirmed with the user, as [`specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame`](/specs/AGENTS.md#the-goals-and-the-frame) has it. The steers of any other set are recorded as given, a steer choosing wording a step quotes as its outcome or a name in code among them. The record tells the adversarial review the user chose each. Where the steer differs from another choice only by preference, it stands. Where it breaks a rule, the review raises a finding on the part of the design carrying the steer's choice, naming that part and no steer ([`§ A Check's Report § Finding`](#finding)). At settling, the builder finds the steers behind the parts a finding names, in the order [`§ Steering Decision § Revisiting a Steer`](#revisiting-a-steer) gives them. It presents the conflict to the user with a wording or a name that follows the rule, and the user chooses either. The record is history. A later steer revising what an earlier one decided is recorded after it, and its Decision says which steer it revises. The earlier one stays as it was given, and the design follows the later one, so the records, read in order, show how the design was shaped. The builder revises what an agreement decided as [`§ Steering Decision § Revisiting a Steer`](#revisiting-a-steer) has it revised. A question the user leaves unanswered is asked again, never read as agreed. The reviews read the steers as [`§ Steering Decision § A Steer's Type`](#a-steers-type) has them read. The request that opened the design is its Source.

### A Steer's Type

A steer is an agreement where the user only agrees to one of the options the builder framed, a literal selection. Every other steer is a directive, whatever its form, such as emphasis, a negative remark, a nudge or a strong direction for the design. An agreement takes up the builder's own framing, while a directive originates with the user. So the builder's triage, its recommendations, its revisions and its design reassessments answer to the directives, never to an earlier agreement. The reviews hold the design to its directives, reading its agreements as how the design came to be. A steer's type takes no call from the user: every call [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) gives the user stays the user's, whatever steer stands behind the part it changes. A design whose steers hold the types selection and perspective, written before these, is read as holding agreements and directives. Its steers are brought to these names as [`§ The Working Files`](#the-working-files) has a working file brought to the form in force.

### Telling a Steer Apart

#### Steer, Direction, Feedback, Other Work or the User's Edit

During an apply, or while the design is sent back with its changes kept, a steer, direction about the work, feedback on the applied result, a decision about other work and the user's own edit are each recorded by its row. What the user asks of the applied result is feedback where a tactical fix ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) carries it out. Where it changes the plan, as [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review § Placing a Finding`](/specs/AGENTS.md#placing-a-finding) has a fix change it, it is a steer, and the design goes back to in-progress. An answer carrying more than one is taken a part at a time:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** What the user decides \
**Annotations:** Sounds Like

| What the user decides | Recorded | Tells a reviewer | Sounds Like |
|---|---|---|---|
| A steer | in Steering Decisions, its Steer quoting every part of the user's words that decides the design, never only the last of them | how the design was formed | "split the canon and application work", "count each review phase apart", "yes, take in the new scope we found", "call it Kind, not Type" |
| Direction about the work | not as a steer; where the record needs it, as an entry of the design's log ([`§ Design Log Entry`](#design-log-entry)), or in the Status field | nothing about what the design is | "yes, fold in the tactical fixes", "rerun the validation review", "approved and apply", "the applied result is approved", "create the branch", "medium effort", "G1 to G6 are design flaws", "approve it" or "rescope it" at the step back, the new scope then steered at framing |
| Feedback on the applied result | not as a steer; made by the builder in place, as [`§ A Design Document § Changes After Approval § A Tactical Fix After the Apply`](#a-tactical-fix-after-the-apply) has a tactical fix made, and taken in at proving the fixes, as [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) has it | nothing about what the design is | "that paragraph buries the rule", "say it in fewer words", "the example reads wrong" |
| A decision about other work | where that work is held | nothing about the design being worked | "the implement-specs design should weigh renaming the workstack", "keep the billing service stateless when we design it" |
| The user's own edit | not as a steer; the builder confirms with the user whether it was intended, since it may be accidental, and reverts an accidental edit; an intended one it takes in as it stands and logs as a `user-edit` entry naming its places ([`§ Design Log Entry`](#design-log-entry)), one of the design's changes ([`§ A Design Document § Applying and Committing`](#applying-and-committing)), checking it as [`§ A Check's Report § Kinds of Builder Check [Check Kind: user edit]`](#kinds-of-builder-check) has it | nothing about what the design is; the reviews read a change in its places as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Whose a Finding Is`](/specs/AGENTS.md#whose-a-finding-is) has it read | "I reworded that sentence in the README", "I fixed the typo in the brief myself" |

### A Decision About Other Work

A decision about other work is recorded where that work is held, so whoever takes the work up finds it in the files rather than in one agent's memory. A decision about more than one design is recorded in each. What becomes of the decision, by where the work is held:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Where the work is held

| Where the work is held | The decision |
|---|---|
| "a not-started design", "an in-progress design" | is its steer, applied when that design is worked |
| "an approved design", "an applying design" | is put to the user, who decides whether to reopen that design for it, an applying one only by a steer, which sends it back ([`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply)): reopened, the design takes it as its steer; not reopened, it is dropped, or, where the user wants it kept for later, logged as a follow-up |
| a follow-up, and no open design | goes in the follow-up's body ([`§ A Follow-up`](#a-follow-up)), and the design taking up the follow-up records it as its steer |
| no follow-up, and no open design, only a complete or abandoned design or nothing | the user chooses between a not-started design recorded for it, the decision its Source where it asks for the work and its steer otherwise, and a new follow-up |

### Revisiting a Steer

A design's path is not straight. Working toward an elegant solution takes loops, detours and pivots, and a steer is part of what may need to move. While settling a round ([`specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`](/specs/AGENTS.md#settling-a-round)), the builder may find that a change fixing a cause would go against one or more steers, of either Type. Those are the steers the cause presses on. Where that serves the goals better, the builder revises what an agreement among them decided, on its own call and with no stop for the user. It records the revision in the Settlement or the change making it, citing the agreement. The steer's record stands as it was given. Only the user revises a directive. The builder brings the user a directive the cause presses on, the findings pressing on it and what revising it would change, only where revising the agreements cannot fix the cause. The user decides.

## A Stamp

A stamp lets a later reader tell whether content has changed since a check passed on it, so nothing has to be cleared by hand. It is written as a UTC timestamp and a content hash separated by a space, `2026-09-29T14:05:12Z sha256:3f9a0c1b2d4e5f60`:
- **The timestamp.** A date and time as RFC 3339 writes one ([`specs/methodology/external-references.md § External References [Name: RFC 3339]`](/specs/methodology/external-references.md#external-references)), in UTC, to the second, ending in `Z`, as `YYYY-MM-DDThh:mm:ssZ`, so stamps written on different machines compare without a time zone.
- **The content hash.** SHA-256 of the file's text, encoded as UTF-8 with line-feed line endings, after dropping the lines that hold the fields and the sections the form leaves out. Where the form takes in other files beside the one holding the stamp, the hash runs on over each of them in turn after that text, in the sorted order of their paths, each path written from the project's root with forward slashes on a line of its own and followed by the file's text, encoded the same way, a file gone taken as its path alone. It is written as `sha256:` followed by the digest's first sixteen hexadecimal characters, lowercase. The hash detects a change, and is not meant to resist tampering.

The form a stamp is used in names the field holding the stamp, the fields the stamp leaves out and the other files it takes in. The stamp always leaves out its own field, since writing the stamp must not change the hash. It also leaves out any field whose change the check does not concern, as a design document's Validated field leaves out its Status ([`§ A Design Document`](#a-design-document)). It may leave out a section too, its heading through the next heading of its level, but for lines its form keeps, as a design document's stamp leaves out its Design Log Entries but each entry naming a report the validation review reads ([`§ A Design Document`](#a-design-document)). So an entry appended after the stamp leaves it current, unless the validation review reads the report it names. It takes in another file where what the check passed on lies in that file too, as a self-review's stamp over applied work takes in the files the design's changes hold ([`§ A Check's Report § A Report's Stamp`](#a-reports-stamp)).

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
| Name | a `###` heading, a kebab-case slug ([`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion)) | yes | | the name the follow-up is referred to by |
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
