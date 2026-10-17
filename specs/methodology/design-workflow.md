## The Order of a Design's Work

The order a design's work takes, and what moves it back, as two State Machines its Status runs (`specs/methodology/working-files.md § A Design Document § The States It Moves Through`): the in-progress state is governed by `§ The Order of a Design's Work § The Work of a Design`, and the applying state by `§ The Order of a Design's Work § The Apply`. Each state's work is done as the section it cites has it, so the machines hold the order alone, the principles staying in `specs/AGENTS.md § Design, Refactor, Refine`. A design changing code takes the same order (`specs/methodology/working-files.md § A Design Document § A Design Changing Code`).

### The Work of a Design

A design enters its work by the reason its Status entered in-progress, and its change leads back to another adversarial review wherever needs review? or needs reframing? holds and the user's approval has not ended its review (`§ The Order of a Design's Work § Facts`). A design its Depends On names finishes, a class of occurrences, when its Status enters complete or enters abandoned (`specs/methodology/working-files.md § A Design Document`).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| entered | the design has entered in-progress, by its Status's move | Yes | No |
| framing | the builder agrees on the design goals with the user and states the design frame, or revisits either, and brings them to the user, as `specs/AGENTS.md § Design, Refactor, Refine` has the goals, then the frame, come first, taking in each steer the user gives and each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`) | No | No |
| drafting | the builder takes the design through Design, Refactor, Refine (`specs/AGENTS.md § Design, Refactor, Refine`), recording each steer as it is given (`specs/methodology/working-files.md § Steering Decision`) and taking in each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`), checks its whole work, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and, before the design's first adversarial review, or before its post-apply audit where the user's approval ends the review before any round, offers the user the review's model and reasoning effort | No | No |
| reviewing | a cold agent runs the adversarial review, as `specs/AGENTS.md § Design, Refactor, Refine` has it | No | No |
| settling | the builder groups the round's findings, weighs them against the design's goals and weighs the steers they press on and states the causes and the change it proposes, the user triaging its design flaws and answering its other calls, the builder settling the rest, as `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round` has it, taking in each steer the user gives and each design its Depends On names that has finished, one finishing while the design was reviewed among them; where the user's approval has ended the review, it settles nothing, the round's findings left as they are | No | No |
| reassessing | the builder and the user step back and reassess, as `specs/AGENTS.md § Design, Refactor, Refine` has a phase not converging, taking in each design its Depends On names that has finished | No | No |
| changing | the builder revises the design, as the round was settled, taking in each steer the user gives and each design its Depends On names that has finished (`specs/methodology/working-files.md § A Design Document`), and proves the change, as `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round` has it | No | No |
| waiting | the design waits for each design its Depends On names to be approved or applying, as `specs/methodology/working-files.md § A Design Document` has a design validated and approved only then | No | No |
| validating | the builder checks its whole work, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and the validation review checks that the design document is valid, the builder fixing what it reports and running it again until it stamps the design (`specs/methodology/working-files.md § A Design Document`) | No | No |
| awaiting approval | the user is asked to approve the design | No | No |
| approved by the user | the user approved the design | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| entered | framing | none | entry reason = "taken up" |
| entered | framing | none | entry reason = "sent back" |
| entered | changing | none | entry reason = "reopened" |
| entered | changing | none | entry reason = "a dependency finished" |
| entered | waiting | none | entry reason = "a dependency moved back" |
| framing | drafting | the user agrees on the goals and agrees to or adjusts the frame | none |
| drafting | framing | the user gives a steer | needs reframing? |
| drafting | reviewing | none | not(review ended by approval?) |
| drafting | validating | none | review ended by approval? and depends on ready? |
| drafting | waiting | none | review ended by approval? and not(depends on ready?) |
| reviewing | settling | none | none |
| reviewing | changing | the user gives a steer | none |
| settling | reassessing | none | not(review ended by approval?) and (consecutive design flaw rounds >= 3 or consecutive implementation flaw rounds >= 5) |
| settling | changing | none | review ended by approval? or (consecutive design flaw rounds < 3 and consecutive implementation flaw rounds < 5) |
| reassessing | framing | the user decides the reassessment | reassessment != "go on" |
| reassessing | changing | the user decides the reassessment | reassessment = "go on" |
| reassessing | changing | the user approves the design's text | none |
| changing | framing | none | needs reframing? |
| changing | drafting | none | not(needs reframing?) and needs review? and not(review ended by approval?) |
| changing | validating | none | not(needs reframing?) and (not(needs review?) or review ended by approval?) and depends on ready? |
| changing | waiting | none | not(needs reframing?) and (not(needs review?) or review ended by approval?) and not(depends on ready?) |
| waiting | validating | depends on ready? becomes true | none |
| waiting | changing | the user gives a steer | none |
| waiting | changing | a design its Depends On names finishes | none |
| validating | approved by the user | none | text approved? |
| validating | awaiting approval | none | not(text approved?) |
| validating | changing | the validation review reports a problem | fix changes the design? |
| validating | waiting | `specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]` of a design its Depends On names is entered | none |
| validating | changing | the user gives a steer | none |
| validating | changing | a design its Depends On names finishes | none |
| awaiting approval | approved by the user | the user approves the design's text | depends on ready? |
| awaiting approval | changing | the user does not approve the design's text | none |
| awaiting approval | drafting | the user asks for another round | none |
| awaiting approval | waiting | `specs/methodology/working-files.md § A Design Document § The States It Moves Through [States.State: in-progress]` of a design its Depends On names is entered | none |
| awaiting approval | changing | a design its Depends On names finishes | none |

### The Apply

The order a design's apply takes, begun only as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets a design enter applying, and ended applied or sent back:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| writing | the builder writes the design's edits, checks the files against them, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets, and starts the post-apply audit as `§ A Design's Reviews` sizes it, a cold agent's on the model and reasoning effort the user chose for the design | Yes | No |
| auditing | the post-apply audit runs, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets | No | No |
| settling the audit | each finding of the audit is settled with the user, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it | No | No |
| reassessing the apply | the builder and the user step back and reassess, as `specs/AGENTS.md § Design, Refactor, Refine` has a phase not converging | No | No |
| awaiting the commit | the builder shows the user the commit for the design's changes and waits for the go-ahead | No | No |
| committing | the builder commits the design's changes on their own, one commit for the design (`specs/methodology/working-files.md § A Design Document`) | No | No |
| reverting | the builder reverts the changes the design wrote, through version control where the project has it, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has a design sent back | No | No |
| applied | the design's edits are written, its audit settled, and its changes committed where the project has version control | No | Yes |
| sent back | the design goes back to in-progress, its changes reverted, a finding of its audit sending it back or its builder finding, as it writes, a change the design does not hold | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard |
|---|---|---|---|
| writing | auditing | none | none |
| writing | reverting | the builder finds a change the design does not hold | none |
| auditing | settling the audit | none | none |
| settling the audit | reassessing the apply | none | audit sends back? and consecutive send-back audits >= 3 |
| settling the audit | reverting | none | audit sends back? and consecutive send-back audits < 3 |
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

- **Name:** consecutive design flaw rounds
  **Type:** number
  **Initial Value:** 0
  **Means:** the adversarial rounds in a row of the design's phase, this one among them, each not ended by the user's approval and finding a design flaw the user triaged as one, counted as `specs/AGENTS.md § Design, Refactor, Refine` has a phase converge; set back to zero by a round finding none and by the design's starting afresh at its frame, a reassessment's or a send-back's

- **Name:** consecutive implementation flaw rounds
  **Type:** number
  **Initial Value:** 0
  **Means:** the adversarial rounds in a row of the design's phase, this one among them, each not ended by the user's approval and finding an implementation flaw, a nit the builder judged harmful among them, counted as `specs/AGENTS.md § Design, Refactor, Refine` has a phase converge; set back to zero by a round finding none and by the design's starting afresh at its frame, a reassessment's or a send-back's

- **Name:** consecutive send-back audits
  **Type:** number
  **Initial Value:** 0
  **Means:** the post-apply audits in a row of the design, this one among them, each sending the design back, for a design flaw or an implementation flaw, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has it, counted as `specs/AGENTS.md § Design, Refactor, Refine` has a phase converge; set back to zero only by an audit sending none back, a send-back leaving it as it stands

- **Name:** reassessment
  **Type:** string
  **Values:** "rescope", "split", "a different approach", "go on"
  **Means:** what the user decided at a reassessment, as `specs/AGENTS.md § Design, Refactor, Refine` has one; a design abandoned leaves by `specs/methodology/working-files.md § A Design Document § The States It Moves Through` instead

- **Name:** needs review?
  **Type:** boolean
  **Means:** whether the design takes another adversarial round before it is validated: the last round it settled found a design flaw the user triaged as one or an implementation flaw, or its goals, its frame or its structure have moved since that round began, or it has settled none since it was last framed (`specs/AGENTS.md § Design, Refactor, Refine`)

- **Name:** needs reframing?
  **Type:** boolean
  **Means:** whether a steer the design took in changed its goals or its frame and the user has not yet approved the change, so they go back to the user for approval, the frame re-evaluated against goals that changed (`specs/AGENTS.md § Design, Refactor, Refine`)

- **Name:** review ended by approval?
  **Type:** boolean
  **Initial Value:** false
  **Means:** whether the user's approval of the design's text, given before its adversarial review ended, ended it (`specs/AGENTS.md § Design, Refactor, Refine`). The approval sets it in any state of the design's work. No transition fires on it but the reassessment's, and each state finishes its own work first. It is set back to false only where the design is sent back, a reassessment starts it afresh or the user asks for another round. So a change after the approval keeps it, a reopen or a dependency's move among them, even one changing the goals or the frame, and the design comes back to the user

- **Name:** text approved?
  **Type:** boolean
  **Initial Value:** false
  **Means:** whether the user's approval of the design's text, given in any state of its work, covers the text as it stands (`specs/AGENTS.md § Design, Refactor, Refine`); set back to false by a change after the approval to its goals, its frame or The Design, the design then coming back to the user to approve again, and by its entering in-progress again

- **Name:** fix changes the design?
  **Type:** boolean
  **Means:** whether fixing a problem the validation review reports changes The Design, as an edit that no longer applies does, and not only the record around it

- **Name:** depends on ready?
  **Type:** boolean
  **Means:** whether each design its Depends On names is approved or applying

- **Name:** audit sends back?
  **Type:** boolean
  **Means:** whether a finding of the post-apply audit sends the design back to in-progress, as `specs/methodology/working-files.md § A Design Document § Changes After Approval` has one

- **Name:** version control?
  **Type:** boolean
  **Means:** whether the project keeps its files under version control

## A Design's Reviews

A design's Kind sizes its reviews, so the effort a design's reviews take, and what its post-apply audit reads, grow with what a flaw in it would cost, and a design whose Target names files of more than one Kind takes the highest effort among them. The effort this table gives is a review's default (`specs/AGENTS.md § Design, Refactor, Refine`); what the post-apply audit reads is its Kind's, as `.ai/skills/audit-specs/SKILL.md` sets it, and `.ai/skills/verify-spec-implementation/` for code:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Kind

| Kind | Effort |
|---|---|
| `canon-specs` | high |
| `application-specs` | medium |
| `code` | medium |
| `documentation` | light |
| `other` | medium |

A flaw in the canon is reproduced in every specification written under it, as a flaw in a mint's engraving plate is reproduced on every banknote it prints. A flaw in the documentation reaches no file beyond it. A flaw in the application specifications reaches the code built from them, and a flaw in code reaches what it runs, so each takes the middle effort. What another file reaches is not known in advance, so it takes the middle effort too.

## A Review's Effort

A review's reasoning effort, the level the user chose (`specs/AGENTS.md § Design, Refactor, Refine`), is applied by how the agent in use can apply it; the builder offers only a level it can apply, and where it can apply none, the review runs as the agent allows:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** How the agent applies a level, definition set up?

| How the agent applies a level | definition set up? | Applied |
|---|---|---|
| "as it starts a reviewer" | - | at the nearest level the agent offers, set as the reviewer starts |
| "through a reviewer definition" | true | through the definition the agent was set up with for that level (`specs/methodology/skills.md § Setting Up an Agent`) |
| "through a reviewer definition" | false | as the agent allows, the agent's setting itself up offered to the user for the reviews after it, since a definition written now may load only once the agent restarts (`.ai/skills/configure-spec-of-record/`) |
| "not at all" | - | as the agent allows |
