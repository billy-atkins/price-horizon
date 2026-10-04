## Purpose

This file defines the bounded, approved set of structured modeling constructs, rather than free prose, for authoring specs in this repo. Prose can describe anything, since human language has no limit, but it cannot be checked for what it leaves out: a paragraph can describe a process while never mentioning what happens under some condition, and nothing about reading it flags the gap. Each construct can be checked for exactly that:

| Construct | Checked for |
|---|---|
| Lifecycle | a state that is not terminal with no way out, a terminal state with one, or a trigger leading from one state to two |
| State Machine | a state that is not terminal with no way out, a terminal state with one, two transitions from one state on the same trigger, or on none, that can both be taken at once, a state that cannot stay where, once its work is done, some case takes no transition out of it, a fork no join closes, or a join no fork opens |
| Decision Table | a combination of its conditions no row covers |
| Decision Tree | a branch that goes nowhere |
| DAG | a task that never runs or never completes |
| Algorithm | a loop with no stated exit condition, or a comparison with a branch whose outcome is unstated |
| Constraint | a rule stated but enforced nowhere |
| Record Form | a record missing a field, or holding one its type does not define |

Use one of the constructs `§ Constructs` defines when a rule, a process, an entity's behavior, or an entry written repeatedly into the specs or the working files needs that kind of checkable completeness, and use prose everywhere else. The set is bounded and approved: a new construct earns its place only by filling a real gap none of the existing ones cover, not by preference for a different notation, and extending the set is a deliberate decision, made by updating this file first, never an ad hoc addition inside a single spec.

This file also sets the form of markup, wherever it is written:

- `§ Fields` and `§ Bold Lead-ins`, the two things a bold phrase opening a line can be, which Record Form and a diagram's fields rely on;
- `§ Emphasis`, how prose stresses a word;
- `§ Literal Text`, what backticks mark.

`§ When to Use Which` is itself modeled with a Decision Tree, so a reader applies the same discipline this file asks of every other spec.

Each construct is authored as a table, a Record Form as a table of its fields and a list of records (`§ Constructs § Record Form`). A table is the one representation that is precise, referable row by row, readable in plain text with no rendering step, and parseable without ambiguity, and a record list keeps those properties for entries whose fields hold prose. A diagram never substitutes for either, since checkable completeness is a construct's job alone; `§ Diagrams` states the one disciplined way a rendering for a human reader is checked in beside them.

## Fields

A field is written as a line opening with its key in bold, the colon inside the bold, then a space and its value: `**Field Name:** value`. It opens a paragraph, a line of its own within one, or a list item; a list marker and any indentation before the key are no part of it.

**Its key —** one the form defining the field declares, so a reader or a script looks a field up by a name it already knows. An unknown key is an error, not a new field, and a field appears only where the form declaring its key places it. A key is one or more words separated by single spaces. Each word begins with a capital and is made of letters or digits, a hyphen joining two parts of one word as in `Sign-off`, and the key holds no other punctuation, so it stays plain and matches exactly wherever it is written.

**Its value —** runs from the key to the next line opening with a field's key, or to the end of the paragraph. Where the form defining the field says so, the value is instead a list: the key stands on a line of its own and the list sits directly beneath it, ending at the next line whose very first character opens a field's key, with no list marker or indentation before it, or at the end of its section.

## Bold Lead-ins

A bold lead-in is a bold phrase, not a field (`§ Fields`), opening a paragraph or a list item to label it for a reader scanning the page. It ends in an em dash inside the bold, with a space before the dash: `**The test —**`. When it introduces the block beneath it, a list, a table or paragraphs, it stands on a line of its own; otherwise the text it introduces follows it on its line. The character closing the bold tells the two apart: a colon makes a field, a dash a lead-in, and a bold phrase opening a line closes on nothing else. Unlike a field, its words are the author's own, defined by no form, so nothing looks one up by name, and nothing cites one (`specs/methodology/sourcing-and-citation.md § Writing a Citation`).

## Emphasis

Emphasis is italic, `*word*`, on a word or a short phrase inside a sentence, where stress changes what the sentence means. Italic is the one emphasis. Bold marks only a field (`§ Fields`) or a bold lead-in (`§ Bold Lead-ins`), both opening a line. A line never opens with italic, since a phrase opening a line to label it is a lead-in. A point that needs more than italic is given structure instead: its own sentence, a lead-in, or, for a rule that must hold, a Constraint (`§ Constructs § Constraint`).

## Literal Text

Backticks mark literal text: something written exactly so elsewhere, a path, a citation, an identifier, a field's key, a heading's title, a value, or a command, so a reader can copy it and a script can match it. A name is not literal text: a product, a method, a company, or a role is written plain, capitalized as a proper noun. A record type's name is literal where it stands for a section's title, `Open Questions`; the idea it names is plain prose, an open question.

## Constructs

### Lifecycle

A model of the states one entity moves through over its lifetime, and what moves it from one to the next: it answers where the entity is in its journey.

Authored as a States table and a Transitions table.

A States table:

| Field | Description |
|---|---|
| state | The name of the state |
| description | What it means for an entity to be in this state |
| terminal | Whether this state ends the lifecycle, yes or no |

A Transitions table:

| From | To | Trigger |
|---|---|---|
| ... | ... | What happens to move the entity on: an actor's action, an event, or a time elapsing |

A transition is taken whenever its trigger happens while the entity is in its From state: nothing that holds at that moment can refuse the move or send the entity elsewhere, and a move that can be refused or sent elsewhere is a State Machine's (`§ Constructs § State Machine`). A trigger names only what happens: whatever must hold when it happens for the move to be taken is a guard, never a qualifier written into the trigger. Each distinct thing that can happen is a trigger of its own: each action an actor may take, such as approving or rejecting, and each outcome of an event from outside the entity, such as a payment clearing or bouncing. Triggers moving the entity between the same two states may share a row, joined by `or`, the transition taken on any of them. A transition may lead back to an earlier state, a reopened item, say: what makes a model a lifecycle is that every move follows from its trigger alone, not that every move goes forward.

Whether a lifecycle is modeled as a State Machine instead is step 2 of `§ When to Use Which`.

### Decision Table

A table mapping combinations of largely independent conditions to an outcome.

| Condition | Condition | ... | Outcome |
|---|---|---|---|
| ... | ... | ... | ... |

State whether a match requires all its conditions to hold, or any one of them.

### Decision Tree

A sequence of numbered, dependent questions, where the order matters and each branch leads to a further question rather than an independent check.

Authored as a table with an explicit step column. Give each row its own identifier, a step number for the question and a second decimal segment per branch, 1.1, 1.2, 1.3 for the branches of step 1. A document's sections are read top-down, and so need no ordinal of their own. A decision tree's steps are not: a branch can jump forward or back to any other step, so each step needs a stable identifier a jump can name.

| Step | Question | Answer | Result |
|---|---|---|---|
| ... | ... | ... | The outcome, or the next step number |

### DAG

A table of tasks in an acyclic process, with their dependencies and any parallel grouping.

| task | depends_on | parallel_group |
|---|---|---|
| ... | the tasks that must complete first | tasks sharing a group run concurrently |

This maps directly onto Airflow's, Dagster's, or Argo Workflows' own DAG definitions, whichever an implementation chooses.

### State Machine

A model of the states a system or an entity can be in, the transitions between them, and the conditions under which each is taken. It answers what happens when something happens in a given state, and under what conditions, so a reviewer can check that every case is covered. It is the general formalism, technology-agnostic, with no tie to any specific serialization or execution engine: a Lifecycle is a State Machine whose transitions carry a trigger alone, with no guard, fork or join.

Authored as a States table and a Transitions table. The States table is Lifecycle's (`§ Constructs § Lifecycle`), for a system or an entity, a terminal state ending the machine. A Transitions table:

| From | To | Trigger | Guard |
|---|---|---|---|
| ... | ... | What happens, as a Lifecycle's trigger, or none | What must hold when the trigger happens for the transition to be taken, or none |

A transition with a trigger and no guard is taken as a Lifecycle's is. One with no trigger is taken once its From state's work is done, and its guard, where it has one, holds. A state's own work being done is not a trigger: a transition taken on it carries none. A state's work is what its description says goes on in it. A state whose description states no work, one that only waits, has done its work once it is entered. A state whose description gives it nothing to wait for cannot stay once its work is done. What a State Machine expresses beyond a lifecycle:

- a guard, which lets a transition's trigger happen, or its From state's work be done, without the transition being taken;
- an exclusive choice, transitions from one state on the same trigger, or on none, each with its own guard. No two of its guards can hold at once, and where the state's work is done and it cannot stay, together they cover every case;
- a fork, a transition into several states that then run concurrently, written as one row whose To joins them with `and`;
- a join, a transition from several states running concurrently, written as one row whose From joins them with `and`. A join is taken only once every one of them has done its work: the effect a dedicated parallel construct would give, without needing one.

Every fork is closed by one join, from states its branches reach, and a join closes one fork; a terminal state reached in any branch ends the machine.

A From listing states separated by commas is a transition from any of them; a From joins its states with `and` or lists them with commas, never both.

Over a DAG, a State Machine adds what `§ When to Use Which` routes to it for at step 4.

### Algorithm

A precise, step-by-step computational procedure that produces a value or a transformation. Unlike a DAG or a State Machine, which orchestrate named tasks or services, an Algorithm specifies the computation inside one of those tasks, or any calculation that is not itself an orchestration.

Authored as a numbered table of steps.

| Step | Action |
|---|---|
| 1 | ... |
| ... | ... |

Give each loop and each comparison a numbered row of its own, with a stated exit condition for every loop and a stated outcome for every branch of every comparison: a loop or a comparison folded into another row's description is exactly the gap prose leaves unchecked.

### Constraint

A rule that must always hold, independent of any single decision point or process step, an invariant on the state or output of something else.

Authored as a table.

| Constraint | Applies to | Enforced by |
|---|---|---|
| ... | What the rule constrains | Which Algorithm, DAG, State Machine, or Decision Table step actually guarantees it |

A constraint with nothing in its Enforced by column is an aspiration, not a guarantee: it is treated as an open gap, never left as though stating the rule enforced it.

### Record Form

An entry of one kind written repeatedly into a methodology spec, an application spec, or a working file, each record stating the same named fields: what differs between records is each field's value, never which fields there are. A schema of data the product stores is not one, however many records the product holds; it is described as the rest of the specs describe data.

A record type is defined once, at the home of the rule it serves, in a section titled with the type's singular preceded by A or An, as `## An Open Question` is. The type's name, a plural, titles the sections holding its records and no other section, so a definition and a collection of records never share a title. The defining section states the type's name and where its records go, and gives any section fields it declares beyond Diagrams in a table of Field and Holds. It gives a table of its record fields, in the order a record gives them, marking the field or fields whose values identify a record:

| Field | Identifies | Holds |
|---|---|---|
| ... | yes or no | What a record states in this field |

**The record section —** a type's records sit together in a record section of their own, titled with the type's name. It holds only fields, in this order:

- `**Diagrams:**`, a section field every type has, optional: its key on a line of its own and beneath it one bullet per citation of a diagram rendering the section or any record in it, sorted in plain character order. Through it, whoever edits a record meets every diagram drawing it;
- any section fields of its own the type declares, facts about the collection as a whole, each required and given in the order its table of them sets;
- `**Records:**`, its key on a line of its own and beneath it one list item per record, ending the section.

A blank line separates one section field from the next, and one record from the next, and each list value ends as `§ Fields` states, so the Diagrams bullets and the records never run together.

**A record —** its fields (`§ Fields`), one per row of its type's table and in that order: the first on the list item's own line, each of the rest on a line indented two spaces directly beneath the one before, every line of the item belonging to one field's value. No blank line falls between a record's fields, since they are one record's facts serving one purpose, and whitespace separates only content that differs. Every record carries every field and no other, and no two records in one section share the values of their identifying fields.

**An identifying value —** short, kept stable for the record's life, and plain text on one line, with no Markdown, backtick, `§`, `;` or `]`, since a citation names one record by its identifying values (`specs/methodology/sourcing-and-citation.md § Writing a Citation`). A type whose natural identifier is long, a question or a description, adds a short one.

**Why a list —** records are not table rows, because a field holds prose a table cell cannot carry readably. They are not headings, because a heading's section admits any content and further headings, where a list item holding only its fields is bounded, so a reader and a script can tell where one record ends and whether it holds exactly its type's fields.

## When to Use Which

Choose the simplest construct that meets the need. State Machine is the most general of the constructs, able to express anything Lifecycle, Decision Table, Decision Tree or DAG can, and that generality is why it is not the default. This section's Decision Tree defaults each path to the simpler construct. It routes to State Machine only when a specific need forces it. Over a lifecycle, that need is a move its trigger alone does not decide, a guard or an exclusive choice, or an entity in several states at once, a fork and its join. Over a DAG, it is a genuine cycle, a materially branching choice, or an intentional conditional stop.

A Decision Tree. Start at step 1.

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | What is being described? | An entity's status over time, not the steps of a process that acts on it | Go to step 2 |
| 1.2 | | A rule that determines an outcome | Go to step 3 |
| 1.3 | | A multi-step process, executed to produce a result | Go to step 4 |
| 1.4 | | A computational procedure that produces a value or a transformation | Use Algorithm |
| 1.5 | | An invariant that must always hold, regardless of which path was taken | Use Constraint |
| 1.6 | | An entry of one kind written repeatedly into the specs or the working files, each stating the same named fields, not data the product stores | Use Record Form |
| 2.1 | Can what holds when the entity would move refuse the move or decide where it goes, or can the entity be in several states at once? | No, every move follows from its trigger alone, and the entity is in one state at a time | Use Lifecycle |
| 2.2 | | Yes | Use State Machine |
| 3.1 | Do the conditions have a genuine order of evaluation, where a later condition only makes sense once an earlier one has been answered a certain way? | No, the conditions are independent | Use Decision Table |
| 3.2 | | Yes | Use Decision Tree |
| 4.1 | Does the process ever repeat a step under some condition, branch into materially different downstream handling, or have an intentional conditional stop that is not an error case? | No | Use DAG |
| 4.2 | | Yes | Use State Machine |

**Combining constructs —** these are not mutually exclusive inside one spec. A single task in a DAG or a state in a State Machine can itself be governed by a Decision Table, a Decision Tree, or an Algorithm. In an expense approval process, the step that routes a claim is a Decision Table over independent conditions: the claim's amount band, its category, and whether a receipt is attached. The step that works out the reimbursable total is an Algorithm: it sums the line items, applies each category's own cap, and deducts any advance already paid. A Lifecycle's transition can be triggered by a process completing a step, a claim moving from under review to approved when the approval step approves it. A Constraint can bound what any of the others is allowed to produce: a reimbursable total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own step flooring the total at zero rather than left as an expectation. Use as many constructs as a spec needs, and never force one to do a job another is built for.

## Diagrams

A diagram is a materialized view of a fact, for a human reader, technical or not, who wants the shape of something before deciding whether to read the mechanism behind it. Like a materialized view, it is precomputed for whoever consumes it and is never itself the source of truth: a diagram disagreeing with what it was rendered from is wrong, as a materialized view disagreeing with its tables is a bug rather than a second valid answer. An agent reads the construct behind a diagram with ease; many human readers do not, and nothing tells an author which reader will arrive, so a diagram is written for the human, and an agent benefits as well.

**Where it goes —** wherever it helps its reader most: beside the main section it renders, or above all the sections it renders, as an overview's diagram sits above its detail files. Where it goes is a judgment about the reader; its form is not.

**Its form, wherever it goes —** a diagram has a heading of its own, directly followed by the diagram, then a `**Caption:**` field, then a `**Sources:**` field (`§ Fields`). Nothing else is in its section, and its shape is the same wherever it appears, as a Decision Table's is. The caption says in prose what the diagram shows and carries no citation, so every citation it rests on has one place. The Sources field is `**Sources:**` on a line of its own followed by one bullet per citation, sorted in plain character order, so the order is mechanical and a script can check it; that order places same-file citations after cross-file ones. A diagram is authored as a Mermaid flowchart, checked in as source rather than as an image, so it renders in plain text and diffs like everything else here. It is a flowchart even where a state diagram or sequence notation would be the more formal rendering, since one grammar across every diagram in this repo, boxes and arrows, is worth more to the readers diagrams exist for than notational precision on any single one. Authoring, rendering or changing one follows `.ai/skills/author-mermaid-diagram/`.

**What it may show —** only what its host file's own content, that file's prose or its own tables, already names. What stands behind a diagram is often far more granular, a State Machine's every state, an Algorithm's every step, and that granularity stays where it is. Check each label against the host file before adding or editing a diagram. A name, step, or distinction the host file never states is either collapsed out of the diagram or, if it genuinely belongs at that altitude, stated in the host file first and only then rendered. Choosing between them is a judgment about the host file's completeness, not about the picture. The bound falls on the diagram and not on a table beside it, because a table can carry a citation in every cell and stays checkable however specific it gets; a rendering that descended into detail its host never states would show a reader things the text around it never explains.

**A diagram and its sources cite each other —**

- **The diagram lists its sources —** the Sources field cites the home of everything the diagram draws, a box, an arrow, or a label on either, in the same file or another. Each is cited at that fact's single home (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`), at the most specific section or record whose own text states it: a child section rather than its parent where the child states it, and never a test scenario. A box naming a grouping draws the grouping, not its members, unless the diagram names them too. A summary restating a fact, an overview's included, is a materialized view of that home just as the diagram is, so it is not a source. A section stating something found nowhere else, as an overview's connecting prose can, is that fact's home, and is one. Together the citations are as specific as they can be without leaving out anything the diagram uses. This is so a reader can go deeper: nothing on the picture can carry a citation of its own, so the list is the way from it to the checkable detail, and the more specific each citation, the less a reader wades through to find what a box stands for. It is also so the diagram can be checked: an agent confirming that the picture represents its sources correctly reads exactly what it draws on, and nothing it does not.
- **Each source cites the diagram back —** every listed section cites the diagram's heading in its own text, not in a section nested inside it, in a sentence such as "`<the diagram's heading>` renders this." A record section, or a record, listed among a diagram's Sources cites it in the record section's `**Diagrams:**` field instead (`§ Constructs § Record Form`). This is so the diagram is kept in step: whoever edits a source is the reader who must re-check the diagram, and the citation in the source is what names the diagram to them.

A section may be listed only where it may cite the diagram's file and be cited by it, per `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, so a diagram draws a fact only from a section able to name it back: a technical diagram draws a product fact from the technical section stating how it is made true, never from the product file.

A diagram's own heading is an ordinary heading, citable like any other, per `specs/methodology/sourcing-and-citation.md § Writing a Citation`, and any file may cite it to point a reader at it. What it is never cited as is the source of a fact: a citation asserting something is true names the prose or construct the diagram renders, never the rendering.
