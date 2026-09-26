## Purpose

This file defines the bounded, approved set of structured, non-prose modeling constructs for authoring specs in this repo. Prose can describe anything, human language has no limit, but it cannot be checked for what it leaves out: a paragraph can describe a process while never mentioning what happens under some condition, and nothing about reading it flags the gap. Each construct below can be checked for exactly that. A decision table's rows can be checked against every combination of its conditions. A decision tree's branches can be checked for one that goes nowhere. A state machine's states can be checked for one with no way out. A DAG's tasks can be checked for one that never runs or never completes. An algorithm's loops can be checked for a stated exit condition, and its comparisons for a stated outcome on every branch. A constraint can be checked for whether it is actually enforced somewhere, or only stated. Use one of the constructs below when a rule, a process, or an entity's behavior needs that kind of checkable completeness, and use prose everywhere else. Extending this set is a deliberate decision, made by updating this file first, not an ad hoc addition inside a single spec.

The approved, bounded set is defined below. A new construct earns its place only by filling a real gap none of the existing ones cover, not by preference for a different notation. This section defines each construct on its own. The section that follows, `§ When to Use Which`, is itself modeled with one of the constructs defined here, a Decision Tree, so a reader applies the same discipline this file asks of every other spec.

Each construct is authored as a table. A table is the one representation that is precise, citable by row, readable in plain text with no rendering step, and parseable without ambiguity. A diagram never substitutes for one, checkable completeness is a table's job alone; `§ Diagrams` below states the one disciplined way a rendering for a human reader gets checked in alongside.

---

## Constructs

### Lifecycle

A model of the states one entity can be in over its lifetime, and the transitions between them.

Authored as a States table and a Transitions table.

A States table:

| Field | Description |
|---|---|
| state | The name of the state |
| description | What it means for an entity to be in this state |
| terminal | Whether this state ends the lifecycle, yes or no |

A Transitions table:

| From | To | Trigger or condition |
|---|---|---|
| ... | ... | What causes this transition |

Whether a lifecycle is modeled as a State Machine instead is step 2 of `§ When to Use Which`.

### Decision Table

A table mapping combinations of largely independent conditions to an outcome.

| Condition | Condition | ... | Outcome |
|---|---|---|---|
| ... | ... | ... | ... |

State explicitly whether a match requires all conditions to hold or any one of them, do not leave that implicit.

### Decision Tree

A sequence of numbered, dependent questions, where the order matters and each branch leads to a further question rather than an independent check.

Authored as a table with an explicit step column. Give each row its own identifier, a step number for the question and a second decimal segment per branch, 1.1, 1.2, 1.3 for the branches of step 1. Unlike a document's sections, which are read top-down and so need no ordinal of their own, a decision tree's steps are not read in order, a branch can jump forward or back to any other step, so each one needs a stable identifier a jump can name explicitly.

| Step | Question | Answer | Result |
|---|---|---|---|
| ... | ... | ... | The outcome, or the next step number |

### DAG

A table of tasks in an acyclic process, with their dependencies and any parallel grouping.

| task | depends_on | parallel_group |
|---|---|---|
| ... | the tasks that must complete first | tasks sharing a group run concurrently |

This maps directly onto Airflow's, Dagster's, or Argo Workflows' own DAG definitions, whichever an implementation later chooses.

### State Machine

A model of the states a system can be in, the transitions between them, and the guards, the conditions that permit or block a given transition. This is the general formalism Lifecycle is built on, technology-agnostic, with no tie to any specific serialization or execution engine.

Authored as the same States and Transitions tables as Lifecycle, extended with guards.

A States table:

| Field | Description |
|---|---|
| state | The name of the state |
| description | What it means for the system to be in this state |
| terminal | Whether this state ends the process, yes or no |

A Transitions table:

| From | To | Guard or trigger |
|---|---|---|
| ... | ... | The condition or event that causes this transition |

An exclusive choice is a state with more than one outgoing transition, each with its own guard. Steps that must run concurrently are expressed as a transition with more than one predecessor state, it does not fire until every predecessor has completed, the same effect a dedicated parallel construct would give, without needing one.

### Algorithm

A precise, step-by-step computational procedure that produces a value or a transformation. Distinct from a Workflow, a DAG or a State Machine, which orchestrates named tasks or services, an Algorithm specifies the actual computation inside one of those tasks, or any calculation that is not itself an orchestration.

Authored as a numbered table of steps.

| Step | Action |
|---|---|
| 1 | ... |
| ... | ... |

State loop and comparison steps explicitly, as their own numbered rows, with a stated exit condition for any loop and a stated outcome for every branch of any comparison. Do not fold a loop or a comparison into the description of a single row, that is exactly the kind of gap prose leaves unchecked.

### Constraint

A rule that must always hold, independent of any single decision point or process step, an invariant on the state or output of something else.

Authored as a table.

| Constraint | Applies to | Enforced by |
|---|---|---|
| ... | What the rule constrains | Which Algorithm, DAG, State Machine, or Decision Table step actually guarantees it |

A constraint with nothing in the Enforced by column is an aspiration, not a guarantee, and should be treated as an open gap, not left as though stating the rule were the same as enforcing it.

---

## When to Use Which

Choose the simplest construct that meets the need. State Machine can express anything Lifecycle, Decision Table, Decision Tree, or DAG can, it is the most general of the constructs defined here, and that generality is exactly why it should not be the default. The tree below is built around this: each path defaults to the simpler construct, and only routes to State Machine when a specific need, more states than a simple lifecycle can hold cleanly, a genuine cycle, a materially branching choice, an intentional conditional stop, actually forces it.

A Decision Tree. Start at step 1.

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | What is being described? | An entity's status over time, not the steps of a process that acts on it | Go to step 2 |
| 1.2 | | A rule that determines an outcome | Go to step 3 |
| 1.3 | | A multi-step process, executed to produce a result | Go to step 4 |
| 1.4 | | A computational procedure that produces a value or a transformation | Use Algorithm |
| 1.5 | | An invariant that must always hold, regardless of which path was taken | Use Constraint |
| 2.1 | Does the entity's status need more than a handful of states or transitions, or does it need to be directly executable? | No | Use Lifecycle |
| 2.2 | | Yes | Use State Machine |
| 3.1 | Do the conditions have a genuine order of evaluation, where a later condition only makes sense once an earlier one has been answered a certain way? | No, the conditions are independent | Use Decision Table |
| 3.2 | | Yes | Use Decision Tree |
| 4.1 | Does the process ever repeat a step under some condition, branch into materially different downstream handling, or have an intentional conditional stop that is not an error case? | No | Use DAG |
| 4.2 | | Yes | Use State Machine |

**Combining constructs.** These are not mutually exclusive inside one spec. A single task in a DAG or a state in a State Machine can itself be governed by a Decision Table, a Decision Tree, or an Algorithm: in an expense approval process, the step that routes a claim is a Decision Table over independent conditions, the claim's amount band, its category, and whether a receipt is attached, while the step that works out the reimbursable total is an Algorithm, summing line items, applying each category's own cap, and deducting any advance already paid. A Lifecycle's transition can be triggered by a process completing a step, a claim moving from under review to approved when the approval step finishes. A Constraint can bound what any of the others is allowed to produce: a reimbursable total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own final step rather than left as an expectation. Use as many of these constructs as a spec actually needs, do not force one to do a job another is built for.

---

## Diagrams

A diagram is a materialized view of a fact for a human reader, technical or not, who wants the shape of something before deciding whether to read the mechanism behind it: precomputed for whoever consumes it, never itself the source of truth, and wrong the moment it disagrees with what it was rendered from, the same way a materialized view disagreeing with the tables it was computed from is a bug rather than a second valid answer. An agent reads the construct behind a diagram with ease; many human readers do not, and nothing tells an author which reader will arrive, so a diagram is written for the human, and an agent benefits as well.

**Where it goes.** Wherever it helps its reader most: beside the main section it renders, or above all the sections it renders, as an overview's diagram sits above its detail files. Where it goes is a judgment about the reader; its form is not.

**Its form, wherever it goes.** A diagram has a heading of its own, directly followed by the diagram, then a `**Caption:**` field, then a `**Sources:**` field, and nothing else in its section, the same shape wherever it appears, as a Decision Table has. The caption says in prose what the diagram shows and carries no citation, so every citation it rests on has one place. The Sources field is `**Sources:**` on a line of its own followed by one bullet per citation, sorted in plain character order, so the order is mechanical and a script can check it; that order places same-file citations after cross-file ones.

**What it may show.** Only what its host file's own content, that file's prose or its own tables, already names. What stands behind a diagram is often far more granular, a State Machine's every state, an Algorithm's every step, and that granularity stays where it is. Check each label against the host file before adding or editing a diagram: a name, step, or distinction the host file never states is either collapsed out of the diagram, or, if it genuinely belongs at that altitude, stated in the host file first and only then rendered. Both are real outcomes, and choosing between them is a judgment about the host file's own completeness rather than about the picture. The bound falls on the diagram and not on a table beside it because a table carries a citation in every cell and stays checkable however specific it gets; a rendering that descended into detail its host never states would show a reader things the text around it never explains.

**A diagram and its sources cite each other.**

- **The diagram lists its sources.** The Sources field cites the home of everything the diagram draws, a box, an arrow, or a label on either, in the same file or another: that fact's single home, in the sense of `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, cited at the most specific section whose own text states it, a child section rather than its parent where the child states it, never a test scenario. A box naming a grouping draws the grouping, not its members, unless the diagram names them too. A summary restating a fact, an overview's included, is a materialized view of that home just as the diagram is, so it is not a source; a section stating something found nowhere else, as an overview's opening prose can, is that fact's home, and is one. Together the citations are as specific as they can be without leaving out anything the diagram uses. This is so a reader can go deeper: nothing on the picture can carry a citation of its own, so the list is the way from it to the checkable detail, and the more specific each citation, the less a reader wades through to find what a box stands for. It is also so the diagram can be checked: an agent confirming that the picture represents its sources correctly reads exactly what it draws on, and nothing it does not.
- **Each source cites the diagram back.** Every listed section cites the diagram's heading in its own text, not in a section nested inside it, in a sentence such as "`<the diagram's heading>` renders this." This is so the diagram is kept in step: whoever edits a source is the reader who must re-check the diagram, and the citation in the source is what names the diagram to them.

A section may be listed only where it may cite the diagram's file and be cited by it, per `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, so a diagram draws a fact only from a section able to name it back: a technical diagram draws a product fact from the technical section stating how it is made true, never from the product file.

A diagram's own heading is an ordinary heading, citable like any other, per `specs/methodology/sourcing-and-citation.md § Writing a Citation`, and any file may cite it to point a reader at it. What it is never cited as is the source of a fact: a citation asserting something is true names the prose or construct the diagram renders, never the rendering.

Authored as a Mermaid flowchart, checked in as source rather than as an image, so it renders in plain text and diffs like everything else here. Authoring, rendering, or changing one follows `.ai/skills/author-mermaid-diagram/`, which records the layout traps that only appear once a diagram is rendered and the check that catches a label this section's own bound would forbid. A flowchart even where a state-diagram or sequence notation would be the more formal rendering: one grammar across every diagram in this repo, boxes and arrows, is worth more to the readers these exist for than notational precision on any single one.
