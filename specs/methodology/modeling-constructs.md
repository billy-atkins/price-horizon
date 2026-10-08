## Purpose

This file defines the bounded, approved set of structured modeling constructs, rather than free prose, for authoring specs in this repo. Prose can describe anything, since human language has no limit, but it cannot be checked for what it leaves out: a paragraph can describe a process while never mentioning what happens under some condition, and nothing about reading it flags the gap. Each construct can be checked for exactly that:

**Construct:** Decision Table

**Conditions:** Construct

| Construct | Checked for |
|---|---|
| Lifecycle | two states sharing a name; no initial state, or more than one; a From or To naming a state its States table does not hold; a state the initial state cannot reach; a state that is not terminal with no way out, or a terminal state with one; a trigger leading from one state to two; or a transition with no trigger |
| State Machine | two states sharing a name; no initial state, or more than one; a From or To naming a state its States table does not hold; a state the initial state cannot reach; a state that is not terminal with no way out, or a terminal state with one; two transitions from one state on the same trigger, or on none, whose guards, read as a Unique Decision Table, can both hold, or a guard no case meets; a state that cannot stay where, once its work is done, some case takes no transition out of it; or a fork no join closes, or a join no fork opens |
| Decision Table | a cell in none of its forms, or a condition column testing values of more than one kind; a cell outside its column's Input Values; where it gives no Default Output, a case no row matches; a row that gives no case its outcome; an outcome cell written as a test; and, by its hit policy, a case two rows match where it is Unique, two rows a case matches giving different outcomes where it is Any, an outcome missing from its Output Values where it is Priority or Output order, an aggregating Collect's outcome other than one column, of numbers but for a count, or a case two rows match whose outcomes cannot both be carried out where it is Rule order, Output order or a Collect that does not aggregate |
| Decision Tree | a branch with no result; a jump to a step the table does not hold; a step no path from step 1 reaches; a step that leads back to itself; or a question whose answers overlap, or leave a case with no answer |
| DAG | two tasks sharing a name; a dependency naming a task the table does not hold; or a task that depends on itself, directly or through others, and so never runs |
| Algorithm | no Inputs or Output field; two steps sharing a number; a jump to a step the table does not hold; a comparison not written in its form; a comparison both of whose branches go back to an earlier step or to its own; a step that is no comparison going back; or a last step, or a branch of it, that neither ends nor jumps |
| Constraint | a rule stated but enforced nowhere, or an Enforced by citing nothing that resolves |
| Record Form | a record missing a field its type requires, holding one its type does not define, holding a value its type's Values do not allow, or giving its fields out of their order; or two records in one section sharing the values of their identifying fields |

Use one of the constructs `§ Constructs` defines when a rule, a process, an entity's behavior, or an entry written repeatedly into the specs or the working files needs that kind of checkable completeness, and use prose everywhere else. The set is bounded and approved: a new construct earns its place only by filling a real gap none of the existing ones cover, not by preference for a different notation, and extending the set is a deliberate decision, made by updating this file first, never an ad hoc addition inside a single spec. Each construct is a definition (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`): its section in `§ Constructs`, with `§ Constructs § Declaring a Construct`, defines what each use of it sets, each use an instance the audit checks against it, as `specs/methodology/scope.md § Rules and Skills` has a rule's checks made. The Record Form is defined through its record types instead (`§ Constructs § Record Form`). The Decision Table is DMN's whole decision table (`specs/methodology/external-references.md § External References [Name: DMN]`); DMN's other parts, its Decision Requirements Diagrams, its Business Knowledge Models and its boxed expressions, are outside the set, and a project needing one adds it so. The State Machine, and the Lifecycle as one, map onto UML's state machine (`specs/methodology/external-references.md § External References [Name: UML]`); the Decision Tree, the DAG, the Algorithm, the Constraint and the Record Form follow no outside standard, since none meets their need: a decision tree's standards describe trees learned from data rather than questions an author writes, a DAG's are whole workflow notations, an algorithm has no standard pseudocode, and a constraint language as wide as the Object Constraint Language is far more than a Constraint needs. The Facts record type relies on DMN's item definitions, as `§ Constructs § Declaring a Construct § A Fact` states.

This file also sets the form of markup, wherever it is written, each Markdown file in scope being written in GitHub Flavored Markdown (`specs/methodology/external-references.md § External References [Name: GFM]`):

- `§ Fields` and `§ Bold Lead-ins`, the two things a bold phrase opening a line can be, which Record Form and a diagram's fields rely on;
- `§ Emphasis`, how prose stresses a word;
- `§ Literal Text`, what backticks mark.

`§ When to Use Which` is itself modeled with a Decision Tree, so a reader applies the same discipline this file asks of every other spec.

Each construct is authored as a table, a Record Form as a table of its fields and a list of records (`§ Constructs § Record Form`). A table is the one representation that is precise, referable row by row, readable in plain text with no rendering step, and parseable without ambiguity, and a record list keeps those properties for entries whose fields hold prose. A diagram never substitutes for either, since checkable completeness is a construct's job alone; `§ Diagrams` states the one disciplined way a rendering for a human reader is checked in beside them.

## Fields

A field is written as a line opening with its key in bold, the colon inside the bold, then a space and its value: `**Field Name:** value`. It opens a paragraph, a line of its own within one, or a list item, its marker a hyphen; the hyphen and any indentation before the key are no part of it.

**Its key —** one the form defining the field declares, so a reader or a script looks a field up by a name it already knows. An unknown key is an error, not a new field, and a field appears only where the form declaring its key places it. A key is one or more words separated by single spaces. Each word begins with a capital and is made of letters or digits, a hyphen joining two parts of one word as in `Sign-off`, and the key holds no other punctuation, so it stays plain and matches exactly wherever it is written.

**Required, or its default value —** each form declaring a field says whether it is required: yes, no, or the condition under which it is. A form declaring other parts in the same table as its fields, sections, say, says the same of each of them. One required under a condition is present where the condition holds and absent where it does not. One that is not required has a default value, which a reader and a script take in its place when it is absent, as a typed language reads a value or its default. A default value of `none` leaves its absence as it is. A field that is not required is written only where its value differs from its default value, so each thing has one way to be said. A form declaring its fields in a table gives a Required and a Default Value column, the default value empty where the field is required, under a condition too; one declaring a field in prose says so in its prose. A required field or part missing is an error, as an unknown key is.

**Its value —** runs from the key to the next line opening with a field's key, or to the end of the paragraph. Where the form defining the field says so, the value is instead a list: the key stands on a line of its own and the list sits directly beneath it, ending at the next line whose very first character opens a field's key, with no list marker or indentation before it, or at the end of its section.

## Bold Lead-ins

A bold lead-in is a bold phrase, not a field (`§ Fields`), opening a paragraph or a list item to label it for a reader scanning the page. It ends in an em dash inside the bold, with a space before the dash: `**The test —**`. When it introduces the block beneath it, a list, a table or paragraphs, it stands on a line of its own; otherwise the text it introduces follows it on its line. The character closing the bold tells the two apart: a colon makes a field, a dash a lead-in, and a bold phrase opening a line closes on nothing else. Unlike a field, its words are the author's own, defined by no form, so nothing looks one up by name, and nothing cites one (`specs/methodology/sourcing-and-citation.md § Writing a Citation`).

## Emphasis

Emphasis is italic, `*word*`, on a word or a short phrase inside a sentence, where stress changes what the sentence means. Italic is the one emphasis. Bold marks only a field (`§ Fields`) or a bold lead-in (`§ Bold Lead-ins`), both opening a line. A line never opens with italic, since a phrase opening a line to label it is a lead-in. A point that needs more than italic is given structure instead: its own sentence, a lead-in, or, for a rule that must hold, a Constraint (`§ Constructs § Constraint`).

## Literal Text

Backticks mark literal text: something written exactly so elsewhere, a path, a citation, an identifier, a field's key, a heading's title, a value, or a command, so a reader can copy it and a script can match it. A span opens and closes with one backtick, so literal text holds no backtick. A name is not literal text: a product, a method, a company, or a role is written plain, capitalized as a proper noun. A record type's name is literal where it stands for a section's title, `Open Questions`; the idea it names is plain prose, an open question.

## Constructs

### Declaring a Construct

Each construct is declared where it is used, so a reader and an audit know it as one. Its declaration is a `**Construct:**` field (`§ Fields`) opening a paragraph of its own before the construct's first table. Its value is the construct's name, as its section under `§ Constructs` is titled: `Lifecycle`, say. The fields a construct sets for itself, a Decision Table's `**Hit Policy:**` or an Algorithm's `**Inputs:**` and `**Output:**`, follow it in the order this section's table and then its own section's table give them, each opening a paragraph of its own, and its tables follow them. The declaration, its fields and its tables make one block, ending with the last table its form gives: a sentence introducing the construct ends before its `**Construct:**` field, and nothing else sits among them (`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`). A Record Form is declared by its titles and its record sections' fields instead (`§ Constructs § Record Form`). It is also the precedent the rest follow. A record section's title names its type, as a section's `**Construct:**` field names its construct. A record is named by its identifying fields, as a part is by its identifier.

Each construct's section defines the fields its instances declare (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), in a table of the shape `§ Constructs § Record Form` sets for a construct's fields. The fields every construct but a Record Form declares, its own section adding its own:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Construct | yes | | `§ Constructs` | its name, as its section under `§ Constructs` is titled, `Declaring a Construct` and `Record Form` aside |
| Order | where the construct leaves open the order it takes its inputs or gives its results in | | text | that order, or `any` where its result is the same in every order, so a result is never left to an order no one chose |

A fact several constructs test is declared as `§ Constructs § Declaring a Construct § A Fact` has it.

**One construct to a section —** a section holds at most one construct of its own, not counting its subsections', so a citation of the section names the construct. Whatever prose the section needs sits between its heading and the `**Construct:**` field, or after the construct's last table, never inside its block, and another construct, a Constraint on an Algorithm's output say, takes a section of its own. A construct's several tables, a Lifecycle's States and Transitions, are one construct, and a table that is no construct, a definition, an index or a catalogue, may sit beside it.

**Its columns —** a construct's tables hold every column its form gives and no other, a Name column and a Decision Table's annotations aside, and every cell holds a value, or `none` or `-` where its form gives one, but for a Decision Tree's Question on a branch other than the first and a Decision Table's annotation, which may be left empty.

**A part of a construct —** is named by a citation of the construct's section followed, in square brackets inside the same span, by the part's identifier written `Key: value`, as a record is named by its identifying fields (`specs/methodology/sourcing-and-citation.md § Writing a Citation`), so a reader and an audit can find the part and check it is there. A part is named so wherever it is named from outside its construct's section; within the section, the construct's cells and the prose around it name it by its identifier alone, as a jump names a step. A citation names one part, and several parts take a citation each:

**Construct:** Decision Table

**Conditions:** Part

| Part | Its identifier |
|---|---|
| a state | `State`, its name |
| "a step of an Algorithm", "a step of a Decision Tree", "a branch of a Decision Tree" | `Step`, its number, as 4 or 1.2 |
| a task of a DAG | `Task`, its name |
| "a transition", "a row of a Decision Table", "a constraint" | `Name`, its Name cell |

A Transitions table, a Decision Table or a Constraint table opens with a column headed `Name` exactly where a part of it is cited from outside its construct's section: the column comes with the first such citation and goes with the last, and while it is there every row gives a Name. No condition or outcome column is headed `Name`.

Each identifier, a state's name, a step's number, a task's name or a Name, is an identifying value (`§ Constructs § Record Form`), and no two parts of one kind in a construct share one. A state's name and a task's name also hold no comma and not the word `and`, since a From, a To and a depends_on list them by those. An Algorithm's steps are numbered from 1 in order. A Decision Tree's step is named by the number its branches share before the dot, as 2 for 2.1 and 2.2.

#### A Fact

A fact several constructs test, where it is one fact by `specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`, is declared once, as DMN's item definition is (`specs/methodology/external-references.md § External References [Name: DMN]`). It narrows the item definition to a single value of one of FEEL's types, with no components and no collection, and adds the unit a number is counted in, whether the fact may be absent and what it means. A file's facts sit in a record section titled `Facts`, in the file whose subject owns them. Each is a record in the Record Form (`§ Constructs § Record Form`) of the type named Facts:

| Field | Identifies | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the fact's name |
| Type | no | yes | | "string", "number", "boolean", "date", "time", "date and time", "days and time duration", "years and months duration" | its type, as FEEL names it |
| Values | no | no | none | text | the values it may take, a quoted list or a range, where its type alone does not bound them |
| Unit | no | no | none | text | the unit a number is counted in |
| May Be Absent | no | no | No | "Yes", "No" | whether it may have no value |
| Means | no | yes | | text | what the fact is |

### Lifecycle

A model of the states one entity moves through over its lifetime, and what moves it from one to the next: it answers where the entity is in its journey.

Authored as a States table and a Transitions table.

A States table:

| Column | Description |
|---|---|
| state | The name of the state |
| description | What it means for an entity to be in this state |
| initial | Whether the entity starts in this state, Yes or No, one state alone being initial |
| terminal | Whether this state ends the lifecycle, Yes or No |

A Transitions table:

| From | To | Trigger |
|---|---|---|
| ... | ... | What happens to move the entity on: an actor's action, an event, or a time elapsing |

A transition is taken whenever its trigger happens while the entity is in its From state: nothing that holds at that moment can refuse the move or send the entity elsewhere, and a move that can be refused or sent elsewhere is a State Machine's (`§ Constructs § State Machine`). A trigger names only what happens: whatever must hold when it happens for the move to be taken is a guard, never a qualifier written into the trigger. A trigger is written in the same words wherever it recurs, since two triggers are the same only where their words are. Each distinct thing that can happen is a trigger of its own: each action an actor may take, such as approving or rejecting, and each outcome of an event from outside the entity, such as a payment clearing or bouncing. Each trigger takes a row of its own, as each of several conditions deciding one outcome takes a Decision Table row of its own (`§ Constructs § Decision Table`), so no row lists triggers. A From names one state, so transitions from several states to one on the same trigger take a row for each From. A transition may lead back to an earlier state, a reopened item, say: what makes a model a lifecycle is that every move follows from its trigger alone, not that every move goes forward.

Whether a lifecycle is modeled as a State Machine instead is `§ When to Use Which [Step: 2]`.

### Decision Table

A table deciding what follows for a case. Each row states, in its condition columns, the cases it matches, and in its outcome columns what follows for them; its conditions are largely independent of one another. A rule that is a lookup, one condition deciding the outcome, is authored as a Decision Table with a single condition column.

| Condition | ... | Outcome | ... |
|---|---|---|---|
| ... | ... | ... | ... |

It is the decision table of DMN, the Object Management Group's Decision Model and Notation (`specs/methodology/external-references.md § External References [Name: DMN]`), and its cells are the forms of FEEL's simple unary tests, the cell syntax of DMN's expression language, that this section lists. Those forms and the hit policies this section gives are all an author needs, so an agent that cannot fetch DMN, or does not know it, loses nothing a Decision Table relies on. Adding a form of FEEL this section does not list is a change to this section and to the audit's checks of its cells, made together.

**Its fields —** after those every construct declares (`§ Constructs § Declaring a Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Hit Policy | no | Unique | `§ Constructs § Decision Table` | its hit policy, as this section's table of them names one |
| Conditions | yes | | text | its condition columns, named by their headers, separated by commas |
| Annotations | no | none | text | its annotations, named by their headers, separated by commas |
| Input Values | no | none | text | a list, an item for each condition it gives values for: its header, a colon, and its values as a quoted list or a range; a question takes no item, its values being `Yes` and `No` |
| Output Values | where its hit policy is Priority or Output order | | text | a list, an item for each outcome column it ranks by: its header, a colon, and its values as a list, highest priority first |
| Default Output | no | none | text | the outcome where no row matches: a value, or, with several outcome columns, a list, an item for each: its header, a colon and its value |

**Its columns —** its condition columns come first, after a Name column where it has one (`§ Constructs § Declaring a Construct`). Its outcome columns follow them, one or more of each, and then its annotations, columns that only describe or illustrate a row, which neither the match nor the check reads. Its `**Conditions:**` field names its condition columns, a lookup's one among them, so which columns are conditions is declared, never inferred. A condition's or an annotation's header holds no comma, and no header an Input Values or Output Values item names holds a colon, since those fields separate headers by them. An outcome cell is never written as a test, `-`, `not(…)`, a comparison or a range, which would show a condition declared an outcome. Its `**Annotations:**` field names its annotations.

**Its cells —** a row matches a case only when all its conditions hold. Each condition cell holds only what tests its condition, what explains or illustrates the value going in an annotation, and tests it in one of these forms, and no other:

- by a value written plain, the whole cell, commas and all, the one form FEEL does not have, standing for the string FEEL writes in quotes; it is no number, never opens with `not(`, `<`, `>`, `=`, `!`, a bracket, a parenthesis, a double quote, `date(`, `date and time(`, `time(` or `duration(`, and is never `-` alone, so it is never taken for another form;
- by a list of values, any one of which matches, each in double quotes and separated by commas, as `"Gold", "Silver"`, each value a word however it reads, so `"2"` is no number;
- by a number, as FEEL writes one, digits with a decimal point among them where it has a fraction and a minus sign before them where it is negative, as `-5` or `0.5`; by a comparison, as `< 0.5` or `>= 100`; or by a range, as `[0.5..0.8)`, a bracket including its end and a parenthesis excluding it, its two ends of one kind;
- by a date, or a date and time to the second with its offset, as FEEL writes one, `date("2024-07-01")` or `date and time("2024-07-01T09:00:00Z")`, a fraction of a second after a decimal point where it has one, alone, compared or bounding a range as a number does;
- by `not(…)` around any of these, matching what it does not, as `not("Silver")`;
- by `-`, any value, for a condition the row does not test.

A condition column's cells, and its Input Values, test values of one kind, words, numbers, dates, or dates and times, so no comparison rests on how one kind is read as another.

An outcome decided when any one of several conditions holds is written as a row for each; under Unique, the rows are written so no case matches two. For an outcome decided when condition A is a or condition B is b, one row tests A for `a`, with `-` for B, and another tests A by `not(a)` and B for `b`.

**Its values —** an `**Input Values:**` field gives a condition's possible values, as DMN's input values do, for each condition it names. A condition whose header ends in a question mark asks a question, answered `Yes` or `No`: those are its Input Values, and the field gives it no item. A cell naming a value they do not hold, or matching none they hold, is outside them. Where every condition gives them, whether every case matches a row is decided rather than read. An `**Output Values:**` field gives, for each outcome column a Priority or an Output order table ranks by, its values as a list, highest priority first, and is written for no other hit policy; where it names several columns, rows rank by the first, then by the next where they tie. A `**Default Output:**` field gives the outcome where no row matches, so every case has one.

**What is one —** a table that defines each case of a closed set and states what follows for it is a Decision Table, since it decides, unless it is another construct's own table, a Lifecycle's transitions or a Decision Tree's steps, say. A table saying only what a term, a value, a form or an example is, or where something is stated, decides nothing: it is a definition, an index or a catalogue, and no construct. So is a table whose rows sample an open set of cases, since it cannot be checked for a case it leaves out.

**Its hit policy —** which of the rows a case matches give it its outcome, named in a `**Hit Policy:**` field as DMN names it, its default value DMN's default, as its table of fields gives:

| Hit policy | A case |
|---|---|
| Unique | matches one row at most, since no two rows can match one case |
| Any | may match several rows, each giving the same outcome |
| Priority | takes the outcome of the row it matches whose outcome comes first in its Output Values |
| First | takes the outcome of the first row it matches, so the rows' order states which takes precedence |
| Rule order | takes the outcome of every row it matches, in the rows' order |
| Output order | takes the outcome of every row it matches, in its Output Values' order |
| Collect | takes the outcome of every row it matches, combining them, or, as `Collect sum`, `Collect count`, `Collect min` or `Collect max`, aggregating them, as DMN's C+, C#, C< and C> do |

A table taking the outcome of every row it matches, Rule order, Output order or a Collect that does not aggregate, has its rows written so that, wherever one case matches two of them, both their outcomes can be carried out. An aggregating Collect has one outcome column, its cells numbers but for a count.

### Decision Tree

A sequence of numbered, dependent questions, where the order matters and each branch leads to a further question rather than an independent check. It starts at step 1.

Authored as a table with an explicit step column. Give each row its own identifier, a step number for the question and a second decimal segment per branch, 1.1, 1.2, 1.3 for the branches of step 1. A document's sections are read top-down, and so need no ordinal of their own. A decision tree's steps are not: a branch can jump to any other step, so each step needs a stable identifier a jump can name. A step's question is written on its first branch's row, the Question cell of its other branches left empty.

| Step | Question | Answer | Result |
|---|---|---|---|
| ... | ... | ... | An outcome, or a jump: `Go to step` and the number of a step the table holds |

A step's answers never overlap, and together they answer its question for every case. No step leads back to itself through the jumps from it: a tree asks a case each question once, since a question asked again of the same case gives the same answer, and a question asked again of a case that has changed is a State Machine's.

### DAG

A table of tasks in an acyclic process and their dependencies. A task may run concurrently with any task that neither depends on it nor is depended on by it, directly or through others.

| task | depends_on |
|---|---|
| ... | the tasks that must complete first, separated by commas, or none |

No task depends on itself, directly or through the tasks it depends on.

This maps directly onto Airflow's, Dagster's, or Argo Workflows' own DAG definitions, whichever an implementation chooses.

### State Machine

A model of the states a system or an entity can be in, the transitions between them, and the conditions under which each is taken. It answers what happens when something happens in a given state, and under what conditions, so a reviewer can check that every case is covered. It is the general formalism, a UML state machine written as tables (`specs/methodology/external-references.md § External References [Name: UML]`), with no tie to any serialization or execution engine. Each of its parts maps onto one of UML's: a state onto a state, a trigger onto a trigger, a guard onto a guard, a transition with no trigger onto a completion transition, its initial state onto the target of the initial pseudostate's transition, a terminal state onto a final state, and a fork and a join onto UML's fork and join pseudostates, each branch between them an orthogonal region. Where its rules differ from UML's, its rules hold: an exclusive choice's guards never both hold, where UML would take either; a terminal state reached in one of a fork's branches ends the machine, as UML's terminate pseudostate does; and a join may carry a trigger, where UML's join takes none. A Lifecycle is a State Machine whose transitions carry a trigger alone, with no guard, fork or join.

Authored as a States table and a Transitions table. The States table is Lifecycle's (`§ Constructs § Lifecycle`), for a system or an entity, a terminal state ending the machine. A Transitions table:

| From | To | Trigger | Guard |
|---|---|---|---|
| ... | ... | What happens, as a Lifecycle's trigger, or none | What must hold when the trigger happens for the transition to be taken, or none |

A transition with a trigger and no guard is taken as a Lifecycle's is. One with no trigger is taken once its From state's work is done, and its guard, where it has one, holds. A state's own work being done is not a trigger: a transition taken on it carries none. A state's work is what its description says goes on in it. A state whose description states no work, one that only waits, has done its work once it is entered. A state whose description gives it nothing to wait for cannot stay once its work is done. What a State Machine expresses beyond a lifecycle:

- a guard, which lets a transition's trigger happen, or its From state's work be done, without the transition being taken;
- an exclusive choice: two or more transitions from one state on the same trigger, or on none. Each of their guards is written as a Decision Table's row is. It tests named facts, each fact and the cell testing it joined by a colon, as `receipt: attached`, and the facts joined by the word `and`; it names only the facts it tests, and a guard of none tests no fact. Each cell tests its fact as a Decision Table's cell does (`§ Constructs § Decision Table`), and a fact's name, and a value written without quotes, hold no colon, no comma and not the word `and`, but for the `date and time(…)` FEEL writes a date and time in. Read together, the guards are a Unique Decision Table over those facts, a fact a guard does not test being `-`, so no two of them can hold at once. Where the state's work is done and it cannot stay, together they also cover every case. A guard on a transition alone on its trigger, or alone with none, is prose, and once another transition joins it, both guards take this form;
- a fork, a transition into several states that then run concurrently, written as one row whose To joins them with `and`;
- a join, a transition from several states running concurrently, written as one row whose From joins them with `and`. A join is taken only once every one of them has done its work: the effect a dedicated parallel construct would give, without needing one.

Every fork is closed by one join, from states its branches reach, and a join closes one fork; a terminal state reached in any branch ends the machine.

A From names one state, as a Lifecycle's does (`§ Constructs § Lifecycle`), or, for a join, joins several with `and`.

Over a DAG, a State Machine adds what `§ When to Use Which [Step: 4]` routes to it for.

### Algorithm

A precise, step-by-step computational procedure that produces a value or a transformation. Unlike a DAG or a State Machine, which orchestrate named tasks or services, an Algorithm specifies the computation inside one of those tasks, or any calculation that is not itself an orchestration.

Its fields, after those every construct declares (`§ Constructs § Declaring a Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Inputs | yes | | text | what it reads, or none |
| Output | yes | | text | what it produces |

Authored as a numbered table of steps.

| Step | Action |
|---|---|
| 1 | ... |
| ... | ... |

Give each loop and each comparison a numbered row of its own: a loop or a comparison folded into another row's description is exactly the gap prose leaves unchecked. A comparison is written `If {condition}, {what follows}; otherwise, {what follows}`, a branch with nothing to do written `continue`. Each branch, and each step that is no comparison, ends `Go to step` and the number of a step the table holds, or `End`, or else continues to the next step. A loop is a comparison one of whose branches goes back to an earlier step or to its own, its other branch its exit; a step that is no comparison never goes back. The last step, and each branch of it where it is a comparison, ends `End` or goes to another step, so the Algorithm ends only at an `End`.

### Constraint

A rule that must always hold, independent of any single decision point or process step, an invariant on the state or output of something else.

Authored as a table.

| Constraint | Applies to | Enforced by |
|---|---|---|
| ... | What the rule constrains | What actually guarantees it: a part of another construct, such as a step, a task, a transition or a row, or a section whose own text states the mechanism, either named by its citation (`specs/methodology/sourcing-and-citation.md § Writing a Citation`) |

A constraint with nothing in its Enforced by column is an aspiration, not a guarantee: it is treated as an open gap, never left as though stating the rule enforced it.

### Record Form

An entry of one kind written repeatedly into a methodology spec, an application spec, or a working file, each record stating the same named fields: what differs between records is each field's value, never which fields there are. A schema of data the product stores is not one, however many records the product holds; it is described as the rest of the specs describe data.

A record type is a definition and its records are its instances (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), each type a sub-definition of this form keeping its own fields. A type is defined at the home of the rule it serves, in a section titled with the type's singular preceded by A or An, as `## An Open Question` is. The type's name, a plural, titles the sections holding its records and no other section, so a definition and a collection of records never share a title. The defining section states the type's name and where its records go, and gives any section fields it declares beyond Diagrams in a table of Field, Required, Default Value, Values and Holds, the shape every construct's table of fields (`§ Constructs § Declaring a Construct`) and every record type's takes. It gives a table of its record fields in the same shape, in the order a record gives them, a column after Field marking the field or fields whose values identify a record:

| Field | Identifies | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| ... | yes or no | as `§ Fields` sets | as `§ Fields` sets | the values it may hold | What a record states in this field |

**Its values —** what a field may hold: a list of its values, each in double quotes and separated by commas, which the audit checks every value against; a citation of the section that lists them; or `text`, any value its Holds describes.

**The record section —** a type's records sit together in a record section of their own, titled with the type's name. It holds only fields, in this order:

- `**Diagrams:**`, a section field every type has, not required, its default value `none`: its key on a line of its own and beneath it one bullet per citation of a diagram rendering the section or any record in it, sorted in plain character order. Through it, whoever edits a record meets every diagram drawing it;
- any section fields of its own the type declares, facts about the collection as a whole, each given in the order its table of them sets, and each required one present;
- `**Records:**`, required, its key on a line of its own and beneath it one list item per record, at least one, ending the section.

A blank line separates one section field from the next, and one record from the next, and each list value ends as `§ Fields` states, so the Diagrams bullets and the records never run together.

**A record —** its fields (`§ Fields`), at most one per row of its type's table and in that order: the first on the list item's own line, each of the rest on a line indented two spaces directly beneath the one before, every line of the item belonging to one field's value. No blank line falls between a record's fields, since they are one record's facts serving one purpose, and whitespace separates only content that differs. Every record carries every field its type requires, and no field its type does not define, and no two records in one section share the values of their identifying fields. An identifying field is required.

**An identifying value —** short, kept stable for the record's life, and plain text on one line, with no Markdown, backtick, `§`, `;` or `]`, since a citation names one record by its identifying values (`specs/methodology/sourcing-and-citation.md § Writing a Citation`). A type whose natural identifier is long, a question or a description, adds a short one.

**Why a list —** records are not table rows, because a field holds prose a table cell cannot carry readably. They are not headings, because a heading's section admits any content and further headings, where a list item holding only its fields is bounded, so a reader and a script can tell where one record ends and whether it holds exactly its type's fields.

## When to Use Which

Choose the simplest construct that meets the need. State Machine is the most general of the constructs, able to express anything Lifecycle, Decision Table, Decision Tree or DAG can, and that generality is why it is not the default. This section's Decision Tree defaults each path to the simpler construct. It routes to State Machine only when a specific need forces it. Over a lifecycle, that need is a move its trigger alone does not decide, a guard or an exclusive choice, or an entity in several states at once, a fork and its join. Over a DAG, it is a genuine cycle, a materially branching choice, or an intentional conditional stop.

**Construct:** Decision Tree

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | What is being described? | An entity's status over time, not the steps of a process that acts on it | Go to step 2 |
| 1.2 | | A rule that determines an outcome | Go to step 3 |
| 1.3 | | A multi-step process orchestrating tasks or services to produce a result | Go to step 4 |
| 1.4 | | A computational procedure that produces a value or a transformation | Use Algorithm |
| 1.5 | | An invariant that must always hold, regardless of which path was taken | Use Constraint |
| 1.6 | | An entry of one kind written repeatedly into the specs or the working files, each stating the same named fields, not data the product stores | Use Record Form |
| 2.1 | Can what holds when the entity would move refuse the move or decide where it goes, or can the entity be in several states at once? | No, every move follows from its trigger alone, and the entity is in one state at a time | Use Lifecycle |
| 2.2 | | Yes | Use State Machine |
| 3.1 | Do the conditions have a genuine order of evaluation, where a later condition only makes sense once an earlier one has been answered a certain way? | No, each condition makes sense on its own, whichever row takes precedence | Use Decision Table |
| 3.2 | | Yes | Use Decision Tree |
| 4.1 | Does the process ever repeat a step under some condition, branch into materially different downstream handling, or have an intentional conditional stop that is not an error case? | No | Use DAG |
| 4.2 | | Yes | Use State Machine |

**Combining constructs —** these are not mutually exclusive inside one spec. A single task in a DAG or a state in a State Machine can itself be governed by a Decision Table, a Decision Tree, or an Algorithm. In an expense approval process, the step that routes a claim is a Decision Table over independent conditions: the claim's amount band, its category, and whether a receipt is attached. The step that works out the reimbursable total is an Algorithm: it sums the line items, applies each category's own cap, and deducts any advance already paid. A Lifecycle's transition can be triggered by a process completing a step, a claim moving from under review to approved when the approval step approves it. A Constraint can bound what any of the others is allowed to produce: a reimbursable total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own step flooring the total at zero rather than left as an expectation. Use as many constructs as a spec needs, and never force one to do a job another is built for.

## Diagrams

A diagram is a materialized view of a fact, for a human reader, technical or not, who wants the shape of something before deciding whether to read the mechanism behind it. Like a materialized view, it is precomputed for whoever consumes it and is never itself the source of truth: a diagram disagreeing with what it was rendered from is wrong, as a materialized view disagreeing with its tables is a bug rather than a second valid answer. An agent reads the construct behind a diagram with ease; many human readers do not, and nothing tells an author which reader will arrive, so a diagram is written for the human, and an agent benefits as well.

**Where it goes —** wherever it helps its reader most: beside the main section it renders, or above all the sections it renders, as an overview's diagram sits above its detail files. Where it goes is a judgment about the reader; its form is not.

**Its form, wherever it goes —** a diagram has a heading of its own, directly followed by the diagram, then a `**Caption:**` field, then a `**Sources:**` field (`§ Fields`), each required. Nothing else is in its section, and its shape is the same wherever it appears, as a Decision Table's is. The caption says in prose what the diagram shows and carries no citation, so every citation it rests on has one place. The Sources field is `**Sources:**` on a line of its own followed by one bullet per citation, sorted in plain character order, so the order is mechanical and a script can check it; that order places same-file citations after cross-file ones. A diagram is authored as a Mermaid flowchart (`specs/methodology/external-references.md § External References [Name: Mermaid]`), checked in as source rather than as an image, so it renders in plain text and diffs like everything else here. It is a flowchart even where a state diagram or sequence notation would be the more formal rendering, since one grammar across every diagram in this repo, boxes and arrows, is worth more to the readers diagrams exist for than notational precision on any single one. Authoring, rendering or changing one follows `.ai/skills/author-mermaid-diagram/`.

**What it may show —** only what its host file's own content, that file's prose or its own tables, already names. What stands behind a diagram is often far more granular, a State Machine's every state, an Algorithm's every step, and that granularity stays where it is. Check each label against the host file before adding or editing a diagram. A name, step, or distinction the host file never states is either collapsed out of the diagram or, if it genuinely belongs at that altitude, stated in the host file first and only then rendered. Choosing between them is a judgment about the host file's completeness, not about the picture. The bound falls on the diagram and not on a table beside it, because a table can carry a citation in every cell and stays checkable however specific it gets; a rendering that descended into detail its host never states would show a reader things the text around it never explains.

**A diagram and its sources cite each other —**

- **The diagram lists its sources —** the Sources field cites the home of everything the diagram draws, a box, an arrow, or a label on either, in the same file or another. Each is cited at that fact's single home (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`), at the most specific section or record whose own text states it: a child section rather than its parent where the child states it, and never a test scenario. A box naming a grouping draws the grouping, not its members, unless the diagram names them too. A summary restating a fact, an overview's included, is a materialized view of that home just as the diagram is, so it is not a source. A section stating something found nowhere else, as an overview's connecting prose can, is that fact's home, and is one. Together the citations are as specific as they can be without leaving out anything the diagram uses. This is so a reader can go deeper: nothing on the picture can carry a citation of its own, so the list is the way from it to the checkable detail, and the more specific each citation, the less a reader wades through to find what a box stands for. It is also so the diagram can be checked: an agent confirming that the picture represents its sources correctly reads exactly what it draws on, and nothing it does not.
- **Each source cites the diagram back —** every listed section cites the diagram's heading in its own text, not in a section nested inside it, in a sentence such as "`<the diagram's heading>` renders this." A record section, or a record, listed among a diagram's Sources cites it in the record section's `**Diagrams:**` field instead (`§ Constructs § Record Form`). This is so the diagram is kept in step: whoever edits a source is the reader who must re-check the diagram, and the citation in the source is what names the diagram to them.

A section may be listed only where it may cite the diagram's file and be cited by it, per `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, so a diagram draws a fact only from a section able to name it back: a technical diagram draws a product fact from the technical section stating how it is made true, never from the product file.

A diagram's own heading is an ordinary heading, citable like any other, per `specs/methodology/sourcing-and-citation.md § Writing a Citation`, and any file may cite it to point a reader at it. What it is never cited as is the source of a fact: a citation asserting something is true names the prose or construct the diagram renders, never the rendering.
