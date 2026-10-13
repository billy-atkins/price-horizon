## The Order of a Design's Work

The order a design's work takes, and what moves it back, as two State Machines its Status runs (`specs/methodology/working-files.md § A Design Document § The States It Moves Through`): the in-progress state is governed by `§ The Order of a Design's Work § The Work of a Design`, and the applying state by `§ The Order of a Design's Work § The Apply`. Each state's work is done as the section it cites has it, so the machines hold the order alone, the principles staying in `specs/AGENTS.md § Design, Refactor, Refine`. A design changing code takes the same order (`specs/methodology/working-files.md § A Design Document § A Design Changing Code`).

### The Work of a Design

A design enters its work by the reason its Status entered in-progress, and its change leads back to another adversarial review wherever needs review? holds (`§ The Order of a Design's Work § Facts`). A design its Depends On names finishes, a class of occurrences, when its Status enters complete or enters abandoned (`specs/methodology/working-files.md § A Design Document`).

**Construct:** State Machine

| state | description | initial | terminal |
|---|---|---|---|
| entered | the design has entered in-progress, by its Status's move | Yes | No |
| framing | the builder states the design frame, or revisits it, and brings it to the user, as `specs/AGENTS.md § Design, Refactor, Refine` has the frame come first, taking in each steer the user gives and each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`) | No | No |
| drafting | the builder takes the design through Design, Refactor, Refine (`specs/AGENTS.md § Design, Refactor, Refine`), recording each steer as it is given (`specs/methodology/working-files.md § Steering Decision`) and taking in each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`), checks its whole work, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and offers the user the review's model and reasoning effort | No | No |
| reviewing | a cold agent runs the adversarial review, as `specs/AGENTS.md § Design, Refactor, Refine` has it | No | No |
| settling | the builder groups the round's findings, weighs the steers they press on and brings the user the causes and the change it proposes, as `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round` has it, taking in each steer the user gives and each design its Depends On names that has finished, one finishing while the design was reviewed among them | No | No |
| reassessing | the builder and the user step back and reassess, as `specs/AGENTS.md § Design, Refactor, Refine` has a phase not converging, taking in each design its Depends On names that has finished | No | No |
| changing | the builder revises the design, as the user decided, taking in each steer the user gives and each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`), and proves the change, as `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round` has it | No | No |
| waiting | the design waits for each design its Depends On names to be approved or applying, as `specs/methodology/working-files.md § A Design Document` has a design validated and approved only then | No | No |
| validating | the builder checks its whole work, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and a cold agent runs the validation review, run again once the builder has corrected the record, until it stamps the design (`specs/methodology/working-files.md § A Design Document`) | No | No |
| awaiting approval | the user is asked to approve the design | No | No |
| approved by the user | the user approved the design | No | Yes |

| From | To | Trigger | Guard |
|---|---|---|---|
| entered | framing | none | entry reason = "taken up" |
| entered | framing | none | entry reason = "sent back" |
| entered | changing | none | entry reason = "reopened" |
| entered | changing | none | entry reason = "a dependency finished" |
| entered | waiting | none | entry reason = "a dependency moved back" |
| framing | drafting | the user agrees or adjusts the frame | none |
| drafting | reviewing | the user chooses the review's model and effort | none |
| reviewing | settling | none | none |
| reviewing | changing | the user gives a steer | none |
| settling | reassessing | the user decides the round's settlement | consecutive flawed rounds >= 3 |
| settling | changing | the user decides the round's settlement | consecutive flawed rounds < 3 |
| reassessing | framing | the user decides the reassessment | reassessment != "go on" |
| reassessing | changing | the user decides the reassessment | reassessment = "go on" |
| changing | drafting | none | needs review? |
| changing | validating | none | not(needs review?) and depends on ready? |
| changing | waiting | none | not(needs review?) and not(depends on ready?) |
| waiting | validating | depends on ready? becomes true | none |
| waiting | changing | the user gives a steer | none |
| waiting | changing | a design its Depends On names finishes | none |
| validating | awaiting approval | none | none |
| validating | waiting | `specs/methodology/working-files.md § A Design Document § The States It Moves Through [State: in-progress]` of a design its Depends On names is entered | none |
| validating | changing | the user gives a steer | none |
| validating | changing | a design its Depends On names finishes | none |
| awaiting approval | approved by the user | the user approves it | depends on ready? |
| awaiting approval | changing | the user does not approve it | none |
| awaiting approval | waiting | `specs/methodology/working-files.md § A Design Document § The States It Moves Through [State: in-progress]` of a design its Depends On names is entered | none |
| awaiting approval | changing | a design its Depends On names finishes | none |

### The Apply

The order a design's apply takes, begun only as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets a design enter applying, and ended applied or sent back:

**Construct:** State Machine

| state | description | initial | terminal |
|---|---|---|---|
| writing | the builder writes the design's edits, checks the files against them, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and offers the user the audit's model and reasoning effort | Yes | No |
| auditing | a cold agent runs the post-apply audit, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets | No | No |
| settling the audit | each finding of the audit is settled with the user, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it | No | No |
| reassessing the apply | the builder and the user step back and reassess, as `specs/AGENTS.md § Design, Refactor, Refine` has a phase not converging | No | No |
| awaiting the commit | the builder shows the user the commit for the design's changes and waits for the go-ahead | No | No |
| committing | the builder commits the design's changes on their own, one commit for the design (`specs/methodology/working-files.md § A Design Document`) | No | No |
| reverting | the builder reverts the changes the design wrote, through version control where the project has it, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has a design sent back | No | No |
| applied | the design's edits are written, its audit settled, and its changes committed where the project has version control | No | Yes |
| sent back | the design goes back to in-progress, its changes reverted, a finding of its audit sending it back or its builder finding, as it writes, a change the design does not hold | No | Yes |

| From | To | Trigger | Guard |
|---|---|---|---|
| writing | auditing | the user chooses the review's model and effort | none |
| writing | reverting | the builder finds a change the design does not hold | none |
| auditing | settling the audit | none | none |
| settling the audit | reassessing the apply | none | audit sends back? and consecutive flawed audits >= 3 |
| settling the audit | reverting | none | audit sends back? and consecutive flawed audits < 3 |
| settling the audit | awaiting the commit | none | not(audit sends back?) and version control? |
| settling the audit | applied | none | not(audit sends back?) and not(version control?) |
| reassessing the apply | reverting | the user decides the reassessment | none |
| awaiting the commit | committing | the user approves its commit | none |
| committing | applied | none | none |
| reverting | sent back | none | none |

### Facts

**Records:**

- **Name:** entry reason
  **Type:** string
  **Values:** "taken up", "reopened", "a dependency moved back", "a dependency finished", "sent back"
  **Means:** why the design last entered in-progress, the move its Status took: taken up, reopened by the user, a design its Depends On names moving back to in-progress, one finishing, or its apply sending it back

- **Name:** consecutive flawed rounds
  **Type:** number
  **Initial Value:** 0
  **Means:** the adversarial rounds in a row of the design's phase, this one among them, each finding a flaw the user settled as one, counted as `specs/AGENTS.md § Design, Refactor, Refine` has a phase converge; set back to zero by a round finding none and by the design's starting afresh at its frame, a reassessment's or a send-back's

- **Name:** consecutive flawed audits
  **Type:** number
  **Initial Value:** 0
  **Means:** the post-apply audits in a row of the design, this one among them, each finding a flaw the user settled as one, counted as `specs/AGENTS.md § Design, Refactor, Refine` has a phase converge; set back to zero only by an audit finding none, a send-back leaving it as it stands

- **Name:** reassessment
  **Type:** string
  **Values:** "rescope", "split", "a different approach", "go on"
  **Means:** what the user decided at a reassessment, as `specs/AGENTS.md § Design, Refactor, Refine` has one; a design abandoned leaves by `specs/methodology/working-files.md § A Design Document § The States It Moves Through` instead

- **Name:** needs review?
  **Type:** boolean
  **Means:** whether the design's structure has moved since the last adversarial review it settled began, or it has settled none since it was last framed, so that it takes another before it is validated (`specs/AGENTS.md § Design, Refactor, Refine`)

- **Name:** depends on ready?
  **Type:** boolean
  **Means:** whether each design its Depends On names is approved or applying

- **Name:** audit sends back?
  **Type:** boolean
  **Means:** whether a finding of the post-apply audit sends the design back to in-progress, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has one

- **Name:** version control?
  **Type:** boolean
  **Means:** whether the project keeps its files under version control

## A Review's Effort

A review's reasoning effort, the level the user chose (`specs/AGENTS.md § Design, Refactor, Refine`), is applied by how the agent in use can apply it; the builder offers only a level it can apply, and where it can apply none, the review runs as the agent allows:

**Construct:** Decision Table

**Conditions:** How the agent applies a level, definition set up?

| How the agent applies a level | definition set up? | Applied |
|---|---|---|
| "as it starts a reviewer" | - | at the nearest level the agent offers, set as the reviewer starts |
| "through a reviewer definition" | true | through the definition the agent was set up with for that level (`specs/methodology/skills.md § Setting Up an Agent`) |
| "through a reviewer definition" | false | as the agent allows, the agent's setting itself up offered to the user for the reviews after it, since a definition written now may load only once the agent restarts (`.ai/skills/configure-spec-of-record/`) |
| "not at all" | - | as the agent allows |
