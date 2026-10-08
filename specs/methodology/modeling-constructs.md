## Purpose

This file defines the bounded, approved set of structured modeling constructs, rather than free prose, for authoring specs in this repo. Prose can describe anything, since human language has no limit, but it cannot be checked for what it leaves out: a paragraph can describe a process while never mentioning what happens under some condition, and nothing about reading it flags the gap. Each construct can be checked for exactly that:

**Construct:** Decision Table

**Conditions:** Construct

| Construct | Checked for |
|---|---|
| State Machine | two states sharing a name; no initial state, or more than one; a From or To naming a state its States table does not hold; a state the initial state cannot reach; a state that is not terminal with no way out, or a terminal state with one; two transitions from one state on the same trigger, or on none, whose guards, read as a Unique Decision Table, can both hold, or a guard no case meets; a state that cannot stay where, once its work is done, some case takes no transition out of it; a fork no join closes, or a join no fork opens; a Transitions table's columns other than From, To and Trigger, then a Guard, an Effect or both in that order, or such a column every cell of which is none; a guard's cell ending at a fact no guard of its choice tests and no Facts record declares, or at a fact of another kind; an Effect cell citing no Algorithm or Decision Table; a Recorded In field that is not a fact's name, a colon and the citation of a Facts record, a record it cites whose Values are no quoted list, or a state not among them; or a protocol machine with an Effect column, a transition with no trigger or a governed state; and of a submachine state, a state governed by more than one machine, a machine governing itself, a governed state that is terminal or not left as its machine's exits have it, the words `governed by` naming no machine or a part of one, or naming none, and a description citing a machine's whole section without them |
| Decision Table | a cell in none of its forms, or a condition column testing values of more than one kind; a condition's header neither a fact's name nor a computation; a cell, a computed header or a computed outcome naming a fact nothing declares, or combining values of two kinds, or a cell ending at a fact of another kind than its column; a Reads item that is no fact's name, a colon and a citation, or a Computed field naming no outcome column; a cell testing another kind than its fact's Type, or `null` where its fact may not be absent; Input Values given for a fact a Facts record declares, or naming a fact; a cell outside its column's values; where it takes one row's outcome and gives no Default Output, a case no row matches; a First table falling through by a Default Output; a row that gives no case its outcome; an outcome cell outside a Computed column written as a test or a list; and, by its hit policy, a case two rows match where it is Unique, two rows a case matches giving different outcomes where it is Any, an outcome missing from its Output Values where it is Priority or Output order, an aggregating Collect's outcome other than one column, of numbers but for a count, or a case two rows match whose outcomes cannot both be carried out where it is Rule order, Output order or a Collect that does not aggregate |
| Decision Tree | a branch with no result; a jump to a step the table does not hold; a step no path from step 1 reaches; a step that leads back to itself; or a question whose answers overlap, or leave a case with no answer |
| DAG | two tasks sharing a name; a dependency naming a task the table does not hold; or a task that depends on itself, directly or through others, and so never runs |
| Algorithm | no Inputs or Output field; two steps sharing a number; a jump to a step the table does not hold; a comparison not written in its form; a comparison both of whose branches go back to an earlier step or to its own; a step that is no comparison going back; or a last step, or a branch of it, that neither ends nor jumps |
| Constraint | a rule stated but enforced nowhere, or an Enforced by citing nothing that resolves |
| Record Form | a record missing a field its type requires, holding one its type does not define, holding a value its type's Values do not allow, or giving its fields out of their order; or two records in one section sharing the values of their identifying fields; and a Facts record whose name is no fact's name, a boolean fact's that asks no question, or whose Values name a fact |

Use one of the constructs `§ Constructs` defines when a rule, a process, an entity's behavior, or an entry written repeatedly into the specs or the working files needs that kind of checkable completeness, and use prose everywhere else. The set is bounded and approved: a new construct earns its place only by filling a real gap none of the existing ones cover, not by preference for a different notation, and extending the set is a deliberate decision, made by updating this file first, never an ad hoc addition inside a single spec. Each construct is a definition (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`): its section in `§ Constructs`, with `§ Constructs § Declaring a Construct`, defines what each use of it sets, each use an instance the audit checks against it, as `specs/methodology/scope.md § Rules and Skills` has a rule's checks made. The Record Form is defined through its record types instead (`§ Constructs § Record Form`). The Decision Table is DMN's whole decision table (`specs/methodology/external-references.md § External References [Name: DMN]`), with the information requirements chaining one decision to another, written as a table's Reads field; DMN's other parts, its Decision Requirements Diagrams, its Business Knowledge Models, its decision services and its boxed expressions, are outside the set, and a project needing one adds it so. The State Machine adopts UML's state machine (`specs/methodology/external-references.md § External References [Name: UML]`); the Decision Tree, the DAG, the Algorithm, the Constraint and the Record Form follow no outside standard, since none meets their need: a decision tree's standards describe trees learned from data rather than questions an author writes, a DAG's are whole workflow notations, an algorithm has no standard pseudocode, and a constraint language as wide as the Object Constraint Language is far more than a Constraint needs. The Facts record type relies on DMN's item definitions, as `§ Constructs § Declaring a Construct § A Fact` states.

This file also sets the form of markup, wherever it is written, each Markdown file in scope being written in GitHub Flavored Markdown (`specs/methodology/external-references.md § External References [Name: GFM]`):

- `§ Fields` and `§ Bold Lead-ins`, the two things a bold phrase opening a line can be, which Record Form and a diagram's fields rely on;
- `§ Emphasis`, how prose stresses a word;
- `§ Literal Text`, what backticks mark.

`§ When to Use Which` is itself modeled with a Decision Tree, so a reader applies the same discipline this file asks of every other spec. `§ Time` says how a construct reads time.

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

Each construct is declared where it is used, so a reader and an audit know it as one. Its declaration is a `**Construct:**` field (`§ Fields`) opening a paragraph of its own before the construct's first table. Its value is the construct's name, as its section under `§ Constructs` is titled: `State Machine`, say. The fields a construct sets for itself, a Decision Table's `**Hit Policy:**` or an Algorithm's `**Inputs:**` and `**Output:**`, follow it in the order this section's table and then its own section's table give them, each opening a paragraph of its own, and its tables follow them. The declaration, its fields and its tables make one block, ending with the last table its form gives: a sentence introducing the construct ends before its `**Construct:**` field, and nothing else sits among them (`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`). A Record Form is declared by its titles and its record sections' fields instead (`§ Constructs § Record Form`). It is also the precedent the rest follow. A record section's title names its type, as a section's `**Construct:**` field names its construct. A record is named by its identifying fields, as a part is by its identifier.

Each construct's section defines the fields its instances declare (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), in a table of the shape `§ Constructs § Record Form` sets for a construct's fields. The fields every construct but a Record Form declares, its own section adding its own:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Construct | yes | | `§ Constructs` | its name, as its section under `§ Constructs` is titled, `Declaring a Construct` and `Record Form` aside |
| Order | where the construct leaves open the order it takes its inputs or gives its results in | | text | that order, or `any` where its result is the same in every order, so a result is never left to an order no one chose |

A fact several constructs test is declared as `§ Constructs § Declaring a Construct § A Fact` has it.

**One construct to a section —** a section holds at most one construct of its own, not counting its subsections', so a citation of the section names the construct. Whatever prose the section needs sits between its heading and the `**Construct:**` field, or after the construct's last table, never inside its block, and another construct, a Constraint on an Algorithm's output say, takes a section of its own. A construct's several tables, a State Machine's States and Transitions, are one construct, and a table that is no construct, a definition, an index or a catalogue, may sit beside it.

**Its columns —** a construct's tables hold every column its form gives and no other, a Name column, a Decision Table's annotations and a State Machine's Guard and Effect, where its section gives them, aside, and every cell holds a value, or `none` or `-` where its form gives one, but for a Decision Tree's Question on a branch other than the first and a Decision Table's annotation, which may be left empty.

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

A fact several constructs test, where it is one fact by `specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`, is declared once, as DMN's item definition is (`specs/methodology/external-references.md § External References [Name: DMN]`). It narrows the item definition to a single value of one of FEEL's types, with no components and no collection, and adds the unit a number is counted in, whether the fact may be absent and what it means. A fact's name is words separated by single spaces, each opening with a letter and holding letters, digits and apostrophes, a hyphen joining two runs of them, but a boolean fact's, which is a question, any words ending in a question mark; and its Values are values, never a fact's name. A Decision Table names a fact it tests as `§ Constructs § Decision Table` sets. A file's facts sit in a record section titled `Facts`, in the file whose subject owns them. Each is a record in the Record Form (`§ Constructs § Record Form`) of the type named Facts:

| Field | Identifies | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the fact's name |
| Type | no | yes | | "string", "number", "boolean", "date", "time", "date and time", "days and time duration", "years and months duration" | its type, as FEEL names it |
| Values | no | no | none | text | the values it may take, a quoted list or a range, where its type alone does not bound them |
| Unit | no | no | none | text | the unit a number is counted in |
| May Be Absent | no | no | No | "Yes", "No" | whether it may have no value |
| Means | no | yes | | text | what the fact is |

### Decision Table

A table deciding what follows for a case. Each row states, in its condition columns, the cases it matches, and in its outcome columns what follows for them; its conditions are largely independent of one another. A rule that is a lookup, one condition deciding the outcome, is authored as a Decision Table with a single condition column.

| Condition | ... | Outcome | ... |
|---|---|---|---|
| ... | ... | ... | ... |

It is the decision table of DMN, the Object Management Group's Decision Model and Notation (`specs/methodology/external-references.md § External References [Name: DMN]`), and its cells, its computed headers and its computed outcomes are written in FEEL, DMN's expression language, in the subset this section lists. Its departures from FEEL are a word written plain and a question's `Yes` and `No`, standing for FEEL's `true` and `false`; where DMN allows two writings of one thing, the section keeps one. Those forms and the hit policies this section gives are all an author needs, so an agent that cannot fetch DMN, or does not know it, loses nothing a Decision Table relies on; what they mean where the section is silent is DMN's, its section cited beside each form. Adding a form of FEEL this section does not list is a change to this section and to the audit's checks of its cells, made together.

**Its fields —** after those every construct declares (`§ Constructs § Declaring a Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Hit Policy | no | Unique | `§ Constructs § Decision Table` | its hit policy, as this section's table of them names one |
| Reads | no | none | text | a list, an item for each fact or outcome it reads from elsewhere: its name, a colon, and the citation of the Facts record declaring it or of the construct deciding it |
| Conditions | yes | | text | its condition columns, named by their headers, separated by commas |
| Computed | no | none | text | its outcome columns whose cells are FEEL expressions, named by their headers, separated by commas |
| Annotations | no | none | text | its annotations, named by their headers, separated by commas |
| Input Values | no | none | text | a list, an item for each condition it gives values for: its header, a colon, and its values as a quoted list or a range of values, and `null` where its fact may be absent; a question takes no item |
| Output Values | where its hit policy is Priority or Output order | | text | a list, an item for each outcome column it ranks by: its header, a colon, and its values as a list, highest priority first |
| Default Output | no | none | text | the outcome where no row matches: a value, or, with several outcome columns, a list, an item for each: its header, a colon and its value |

**Its columns —** its condition columns come first, after a Name column where it has one (`§ Constructs § Declaring a Construct`). Its outcome columns follow them, one or more of each, and then its annotations, columns that only describe or illustrate a row, which neither the match nor the check reads. Its `**Conditions:**` field names its condition columns, a lookup's one among them, so which columns are conditions is declared, never inferred. A condition's or an annotation's header holds no comma, and no header an Input Values or Output Values item names holds a colon, since those fields separate headers by them. An outcome cell outside a Computed column is never written as a test, `-`, `not(…)`, a comparison or a range, nor as a list, which would show a condition declared an outcome. Its `**Annotations:**` field names its annotations.

**Its facts —** each condition column tests one fact. Its header names the fact, as `§ Constructs § Declaring a Construct § A Fact` has a fact's name written. Where the column tests a value computed from facts, its header is that computation in FEEL instead, DMN's input expression (DMN 8.2.3): a header holding `+`, `*`, `/`, `<`, `>`, `=`, a bracket, a parenthesis or a minus between spaces computes, and no other does, so a word such as `and` leaves a header a name. A computed header holds no comma, so its functions take one argument and it writes no list. A question, a header ending in a question mark, names a boolean fact, its values `Yes` and `No`, however its words read. A fact its file's Facts section declares by its name (`§ Constructs § Declaring a Construct § A Fact`) is typed by that record: its column's cells test values of its Type, and its Values, or a question's `Yes` and `No`, are the column's values, so the table's Input Values field gives it no item; `null` joins them, and tests it, only where it may be absent. A fact or an outcome read from elsewhere is an item of the `**Reads:**` field, its name beside the citation of the Facts record declaring it or of the construct deciding it, so a table reads another's outcome as one of its facts, DMN's information requirement (DMN 6.3.13). A cell, a computed header or a computed outcome names only a condition's fact, a fact its file's Facts section declares, or a Reads item, and a cell ends only at a fact of its column's kind.

**Its cells —** a row matches a case only when all its conditions hold. Each condition cell holds only what tests its condition, what explains or illustrates the value going in an annotation, and tests it in one of these forms, and no other:

- by a value written plain, the whole cell, commas and all, the one form FEEL does not have, standing for the string FEEL writes in quotes; it is no number, never opens with `not(`, `<`, `>`, `=`, `!`, a bracket, a parenthesis, a double quote, `date(`, `date and time(`, `time(` or `duration(`, is never `-` or `null` alone, and never opens with `null` and a comma, so it is never taken for another form, and never read as a fact's name;
- by a list of values, any one of which matches, each in double quotes and separated by commas, as `"Gold", "Silver"`, each value a word however it reads, so `"2"` is no number;
- by a number, as FEEL writes one, digits with a decimal point among them where it has a fraction and a minus sign before them where it is negative, as `-5` or `0.5`; by a comparison, as `< 0.5` or `>= 100`; or by a range, as `[0.5..0.8)`, a bracket including its end and a parenthesis excluding it, its two ends of one kind; an end of a comparison or of a range may be a fact's name in place of a value, as `< pause end` or `[1..max term]`, and `=` before a fact's name tests equality with that fact, as `= base currency`, a value being tested as itself and never after `=`, and a name never standing alone as a whole cell (DMN 10.3.1.2, grammar rules 7, 8 and 16);
- by a date, or a date and time to the second with its offset, as FEEL writes one, `date("2024-07-01")` or `date and time("2024-07-01T09:00:00Z")`, a fraction of a second after a decimal point where it has one; by a time of day, `time("09:00:00")`, its offset where it has one; or by a duration, of days and time, `duration("P3D")` or `duration("PT12H")`, or of years and months, `duration("P1Y6M")`, the two kinds never compared with each other (DMN 10.3.2.3); each alone, compared or bounding a range as a number does;
- by `null`, matching a fact that is absent. An absent fact meets `-` only where its column's values hold `null`; it meets no value, comparison or range; and it meets `not(…)` around values only, as `not("Gold")` does, FEEL comparing an absent value with a value to false and with a comparison or a range to no answer (DMN 10.3.2.2, 10.3.2.10 grammar rule 15; Tables 49, 52, 54 and 55);
- by a list of these tests, any one of which matches, separated by commas, as `< 18, >= 60` or `null, "Gold"`, opening with `null` or with what opens a form above but a number, so a cell opening with a word or a number is never read as a list (DMN 10.3.1.2, grammar rule 14);
- by `not(…)` around any of these, matching what it does not, as `not("Silver")`;
- by `-`, any value, for a condition the row does not test.

A condition column's cells, and its Input Values, test values of one kind, words, numbers, dates, dates and times, times, or durations of one of their two kinds, `null` aside, so no comparison rests on how one kind is read as another.

An outcome decided when any one of several conditions holds is written as a row for each; under Unique, the rows are written so no case matches two. For an outcome decided when condition A is a or condition B is b, one row tests A for `a`, with `-` for B, and another tests A by `not(a)` and B for `b`.

**Its outcomes —** an outcome cell holds a value, written as a condition's cell writes one, a word plain or quoted alike, a number, a date, a date and time, a time, a duration or `null`. A column its `**Computed:**` field names holds in each cell a FEEL expression over the facts a cell may name, as `principal * rate` (DMN 8.2.10, 8.3.3). A FEEL expression, in a computed outcome or a computed header, is built of those facts, values written as FEEL writes them, a word in quotes, `+`, `-`, `*` and `/`, a minus between spaces, comparisons, `and`, `or`, `not(…)`, `if … then … else …`, a list in brackets, a filter `[…]` whose test reads `item`, `some` and `every … in … satisfies …`, `for … in … return …`, and the functions `count`, `sum`, `min`, `max` and `list contains` (DMN 10.3.2, 10.3.4.4); a yes or no in an expression is FEEL's `true` or `false`, a question's `Yes` and `No` being its cells' alone; and an outcome computed by a walk whose order changes it cites the Algorithm doing it. Its outcome columns are decided by its conditions together, and an outcome other conditions decide is a table of its own, a part needing both citing both.

**Its values —** an `**Input Values:**` field gives a condition's possible values, as DMN's input values do, for each condition it names. A question takes no item, Its facts giving its values. A cell naming a value they do not hold, or matching none they hold, is outside them. Where every condition gives them, the table takes one row's outcome and no cell tests against a fact, whether every case matches a row is decided rather than read. An `**Output Values:**` field gives, for each outcome column a Priority or an Output order table ranks by, its values as a list, highest priority first, and is written for no other hit policy; where it names several columns, rows rank by the first, then by the next where they tie. A case matching no row takes the table's Default Output where it gives one, and `null` where it does not, under every hit policy (DMN 10.3.2.10); a `**Default Output:**` field, optional, gives that outcome. A table taking every row a case matches, Rule order, Output order or a Collect, is not checked for a case no row matches, `null` there meaning that no row applies. Under First, the outcome where no other row matches is a last row testing nothing, `-` in every condition, which a Name can cite, never a Default Output, the one of DMN's two writings the section keeps. A Default Output written `none` is the field absent, so an outcome meaning that nothing follows takes a word of its own.

**What is one —** a table that defines each case of a closed set and states what follows for it is a Decision Table, since it decides, unless it is another construct's own table, a State Machine's transitions or a Decision Tree's steps, say. A table saying only what a term, a value, a form or an example is, or where something is stated, decides nothing: it is a definition, an index or a catalogue, and no construct. So is a table whose rows sample an open set of cases, since it cannot be checked for a case it leaves out.

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

A model of the states a system or an entity can be in, the transitions between them, and the conditions under which each is taken: it answers where the entity is in its journey, and what happens when something happens in a given state, so a reviewer can check that every case is covered. It is UML's state machine (`specs/methodology/external-references.md § External References [Name: UML]`), adopted whole and written as tables, with no tie to any serialization or execution engine; `§ Constructs § State Machine § What It Means` states what UML means for what its tables write, and names each departure the canon makes from UML. A machine whose every transition is taken on its trigger alone, an entity's plain lifecycle, is a State Machine leaving its optional parts unused, no construct of its own (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`).

**Its fields —** after those every construct declares (`§ Constructs § Declaring a Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Protocol | no | No | "Yes", "No" | whether it says which actions an actor may take in each state, UML's protocol state machine, rather than what the entity does, its behavioral state machine |
| Recorded In | no | none | text | the fact the entity records its state in, its name, a colon and the citation of the Facts record declaring it, as a Decision Table's Reads item is written, each state's name one of that record's Values |

Authored as a States table and a Transitions table.

A States table:

| Column | Description |
|---|---|
| state | The name of the state |
| description | What it means for an entity to be in this state |
| initial | Whether the entity starts in this state, Yes or No, one state alone being initial |
| terminal | Whether this state ends the machine's run, Yes or No |

A Transitions table:

| From | To | Trigger |
|---|---|---|
| ... | ... | What happens to move the entity on, of a kind `§ Constructs § State Machine § What It Means` names, or none |

After its Trigger, a Transitions table adds a Guard column, each cell what must hold when the trigger happens for the transition to be taken, or none, where any of its transitions has a guard, and then an Effect column, each cell the citation of the Algorithm or the Decision Table the transition runs, or none, where any runs an effect; a column every cell of which would be none is not written.

A trigger names only what happens: whatever must hold when it happens for the move to be taken is a guard, never a qualifier written into the trigger. A trigger is written in the same words wherever it recurs, since two triggers are the same only where their words are. Each distinct thing that can happen is a trigger of its own, each action an actor may take and each outcome of an event from outside the entity, so each takes a row of its own, and no row lists triggers; a class of occurrences, named once in the section's prose with each of its members, is one trigger, UML's trigger accepting any event of a class (UML 14.2.3.9.2). A From names one state, or, for a join, joins several with `and`, so transitions from several states to one on the same trigger take a row for each From. A transition may lead back to an earlier state, a reopened item, say. A state's own work being done is not a trigger: a transition taken on it carries none. A state whose description gives it nothing to wait for cannot stay once its work is done.

What a State Machine expresses beyond a move its trigger alone decides:

- a guard, which lets a transition's trigger happen, or its From state's work be done, without the transition being taken;
- an exclusive choice: two or more transitions from one state on the same trigger, on none, or on conditions one occurrence makes true together, whose guards never both hold, a departure where UML would take either. Each of their guards is written as a Decision Table's row is. It tests named facts, each fact and the cell testing it joined by a colon, as `receipt: attached`, and the facts joined by the word `and`; it names only the facts it tests, and a guard of none tests no fact. Each cell tests its fact as a Decision Table's cell does (`§ Constructs § Decision Table`), a comparison's or a range's end naming another fact only where a guard of the choice tests it or a Facts section declares it, of the kind of the fact the cell tests; and a fact's name, and a value written without quotes, hold no colon, no comma and not the word `and`, but for the `date and time(…)` FEEL writes a date and time in. Read together, the guards are a Unique Decision Table over those facts, a fact a guard does not test being `-`. Where the state's work is done and it cannot stay, together they also cover every case. A guard on a transition alone on its trigger, or alone with none, is prose, and once another transition joins it, both guards take this form;
- an effect, an Algorithm or a Decision Table a transition runs as it is taken;
- a fork, a transition into several states that then run concurrently, written as one row whose To joins them with `and`;
- a join, a transition from several states running concurrently, written as one row whose From joins them with `and`, taken once every one of them has done its work.

Every fork is closed by one join, from states its branches reach, and a join closes one fork.

Over a DAG, a State Machine adds what `§ When to Use Which [Step: 4]` routes to it for.

#### What It Means

A State Machine means what UML's state machine means for what its tables write, each statement citing the section of UML it rests on, so neither an author nor a reader needs to recall the standard. The canon's rules beyond UML are its departures, each named where it is stated: an action a protocol machine does not take refused; a protocol machine's transitions taken on an actor's action alone; conditions one occurrence makes true together taken in one step; an exclusive choice's guards never both holding; relative time counted from entering the state; a terminal state in a fork's branch ending the run; a join carrying a trigger; `exit:` testing which terminal state the machine governing a state reached; and, in `§ Time`, an instant already past taken at once and an instant following its fact.

**One occurrence at a time —** the machine handles each thing that happens fully before it takes the next, taking the transitions it enables until it reaches states where it waits, UML's run-to-completion, its section 14.2.3.9.1. An occurrence no transition is enabled by is discarded, but in a protocol machine. A state's work being done is handled ahead of anything else waiting. Conditions one occurrence makes true together are taken in its one step, a departure, UML dispatching each event on its own, the transitions they enable from one state an exclusive choice.

**A state and its initial state —** a state is UML's state; the initial state is the one the machine enters as its run begins, the target of UML's initial Pseudostate's transition, its section 14.2.3.7. Before its run begins and once it has ended, a machine is in no state, its sections 14.2.3.4.2 and 14.2.3.8.3. What must outlast a run is a fact the entity records: its status, named by the entity, as `loan status`, declared in a Facts section (`§ Constructs § Declaring a Construct § A Fact`), its Values the complete list of the values it may take, their one home; the machine names that fact in its Recorded In field, and its states are those of the values it uses, a terminal state's among them, a value it does not use left out.

**A state's work —** what its description says goes on in it, begun when the state is entered, UML's entry and doActivity Behaviors, its section 14.2.3.4.3; done, it lets a transition with no trigger be taken, UML's completion transition, its section 14.2.3.8.3, at once for a state whose description states no work, and once the run of the machine governing it ends for a submachine state. A transition taken while the work runs cuts it short. A transition from a state to itself leaves the state and enters it again, UML's external transition, its section 14.2.3.8.1, its work, the run of the machine governing it and its relative times starting afresh.

**A terminal state —** the machine's run is complete, UML's final state, its section 14.2.3.6. It has no work: what its description says is the run's outcome, and work that ends a run is the effect of the transition entering it.

**A fact —** held by the entity, or by another, and set by a state's work, a transition's effect or an occurrence's data, or from outside the machine, as a payment received lowers a balance, declared in a Facts section where a guard's cell ends at it.

**A trigger —** names what happens, UML's event, its sections 13.3.3.2 to 13.3.3.4, its kind decided by what moves the entity:

**Construct:** Decision Table

**Hit Policy:** First

**Conditions:** What moves the entity

| What moves the entity | Its trigger |
|---|---|
| "the state's own work being done, whatever it found" | none: a transition with no trigger, guarded by what the work found where that decides where it goes |
| "a periodic job's run, detecting a time or a condition" | something done: the job's run, as `§ Time` has it |
| "time, counted from entering the state the transition leaves" | time passing, relative |
| "time, counted from anything else" | time passing, an absolute instant computed from a fact |
| "a fact reaching a value, whatever changed it" | a condition becoming true |
| "a part of another construct being reached, or another machine's state being entered" | that part reached, or that state entered |
| "an action of an actor, or a message from another system, by its happening" | something done |

- **Something done —** an action of an actor, a message from another system, or a periodic job's run: a user approving, a payment arriving, UML's message event, its section 13.3.3.2. What it carries, a payment's amount, say, is a fact its occurrence sets, the data its message carries, its section 13.3.3.2, declared in a Facts section, which its transition's guard may test. A delayed message whose time is fixed when it is sent is something done, written as the message.
- **A part reached, or a state entered —** another construct's part completing, or another machine's state being entered, written as the part's citation and `is reached` or `is entered`, in the same words wherever it recurs, UML's signal event, its section 13.3.3.2; two machines may each be triggered by the other's. Another machine's state is cited, and a state of another instance of the same machine named by its identifier, as a part within its own section is, either followed by its instance after `of` where it matters, as `active of another sale of its loan is entered`.
- **A condition becoming true —** taken the moment it goes from false to true, never while it stays true: a balance reaching zero, UML's change event, its section 13.3.3.3.
- **Time passing —** relative, as 30 days passing, counted from entering the state the transition leaves, a departure where the machine waited elsewhere first, UML counting from the time event's activation; or an absolute instant, as month end, or a payment's due date and 30 days, UML's time event, its section 13.3.3.4. What clock it reads is `§ Time`'s.

**A guard —** tested when its trigger happens, or when its state's work is done, against the facts as they then stand, a transition whose guard does not hold being no transition at all for that occurrence, its section 14.2.3.9.2, a transition with no guard having one always true. It may test any fact about the entity or another, another entity's recorded status among them, `loan status: closed`, a terminal state's name included; the state a machine governs is left by which terminal state that machine reached, tested by `exit:` alone, a departure, UML telling its ends apart by exit points, its section 14.2.3.4.6.

**Two transitions one occurrence enables —** at most one is taken from a state, its section 14.2.3.9.3; the exclusive choice decides which. Where a governed state and a state of the machine governing it both leave on one occurrence, the inner machine's transition is taken, the more deeply nested, its sections 14.2.3.9.4 and 14.2.3.9.5.

**An effect —** the Algorithm or the Decision Table a transition's Effect cell cites, run as the transition is taken, after its From state is left and before its To state is entered, UML's effect Behavior, its sections 14.2.3.8 and 14.2.3.9.6. An action whose outcome decides where the entity goes is no effect but a state's work, the transitions from that state routing on what it found. One occurrence moving several entities in order is written in the machine it reaches first, its effect an Algorithm whose steps move the others, each moved machine's trigger citing that step and each step's move complete before the next.

**A fork and a join —** UML's fork and join Pseudostates, its section 14.2.3.7, the branches between them its orthogonal regions, its section 14.2.3.2, each running at once, one occurrence able to take one transition in each, its section 14.2.3.9.1. A terminal state reached in one branch ends the machine's run, its other branches cut short, a departure, UML's final state completing that branch's region alone, its section 14.2.3.6; and a join may carry a trigger, a departure, UML's join taking none, its section 14.2.3.7.

**A protocol machine —** a machine whose Protocol field is `Yes` is UML's protocol state machine, its section 14.4: its states hold no work, its section 14.4.3.1, so it takes no Effect column, no transition with no trigger and no governed state; each transition is taken on an actor's action, saying the state allows it, a departure where UML allows other events, its section 14.4.3.2.4; and an action no transition from the state takes is refused, a departure, UML leaving it undefined, its section 14.4.3.2.1, and leaving an operation no transition refers to callable in any state, its section 14.4.3.2.3, which the canon does not write. Where the system tells an actor why, the reasons it distinguishes are a Decision Table over the request, and no other reasons are written. Whether the machine allows an action in the entity's state is a fact, named `{entity} permits {action}?`, a question, as `loan permits disbursal?`, which any construct may test, citing the machine.

**Resuming where it left off —** UML returns to where a machine was through a history Pseudostate, its section 14.2.3.4.4; the canon writes it with a fact the entity records, guarding the transitions from the machine's initial state.

**What the tables do not write —** each part of UML's state machine named in this list, and the writing the canon uses instead:

- **A composite state —** which its section 14.2.3.4.7 calls semantically equivalent to a submachine state: a nested machine is a section of its own, governing a state as `§ Constructs § State Machine § A Submachine State` has it.
- **Entry and exit points —** its sections 14.2.3.4.6 and 14.2.3.7: a machine is entered at its initial state and left by its terminal states, told apart by `exit:`.
- **History Pseudostates, and deferred events —** its section 14.2.3.4.4: written with a fact the entity records.
- **Internal and local transitions —** its section 14.2.3.8.1: an occurrence that moves the entity nowhere is no transition; what it changes is a fact.
- **Exit Behaviors —** its section 14.2.3.4.3: the effect of the transitions leaving the state.
- **Choice and junction Pseudostates, and compound transitions —** its sections 14.2.3.7 and 14.2.3.8.4: a state whose work decides, its transitions an exclusive choice.
- **A terminate Pseudostate —** its section 14.2.3.7: a terminal state.
- **An AnyReceiveEvent —** its section 13.3.3.2: a class of occurrences, named once.
- **A state invariant, and a protocol transition's postcondition —** its sections 14.2.3.4 and 14.4.3.2.3: a Constraint (`§ Constructs § Constraint`), a protocol transition's precondition being its guard.
- **A guard testing another object's state —** its section 14.2.3.8.3: a test of that entity's recorded status.
- **Protocol conformance —** its section 14.4.3.3: not written.

A design adds a form for one where a spec needs what these writings cannot say.

#### A Submachine State

A State Machine's state whose work is the run of another State Machine, started by entering the state, is UML's submachine state, its section 14.2.3.4.7, governed by that machine. A machine run apart from the state, another entity's or one started elsewhere, is no state's work: a state waiting on it is left on a trigger, a part of it being reached. Its description says it is governed: the words `governed by`, which name only a machine, then that machine's section cited. A description citing another machine's whole section always says them, so a state referring to a machine it is not governed by cites one of its parts.

- **Its machine —** one at most; a machine never governs itself, directly or through those it governs; a governed state is never terminal, a terminal state having no work.
- **Entering it —** at the governing machine's initial state, by however many transitions reach it, the transitions from that initial state guarded by why it was entered, where that matters.
- **Leaving it by its machine's end —** by transitions with no trigger, as its table of exits has them, `exit:` testing nothing else: a holder that routes on a fact as well leads each `exit:` transition to a state with no work, whose own transitions route on that fact.
- **Leaving it on a trigger —** a transition with a trigger, taken from whatever state the governing machine is in, UML's group Transition, its sections 14.2.3.4.7 and 14.2.3.8.2. A trigger every state of the work leaves the same way, to one state outside it, is written once, on the outermost governed state whose every state it so leaves, and on no state inside it; one only some states of the work take, or take differently, is written inside the work, on each state taking it, leading to a terminal state where it ends the work.

Its table of exits:

**Construct:** Decision Table

**Conditions:** Its machine's terminal states, Where it stands

| Its machine's terminal states | Where it stands | Left by |
|---|---|---|
| "none" | - | its triggers alone, its machine never ending |
| "one" | "outside a join's From" | one transition with no trigger and no guard |
| "more than one" | "outside a join's From" | one transition with no trigger for each, guarded `exit: {terminal state}`, naming the terminal state reached, so together they are an exclusive choice covering every end |
| "one", "more than one" | "in a join's From" | the join alone, taken once every branch's work is done |

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

## Time

How a construct reads time, wherever a cell, a guard, a trigger or a step reads a date, a time or a duration.

**The clock —** a date or a time is read on a clock: the wall clock, unless a construct names another. A clock other than the wall clock, as a business date a job advances, is a fact of the Type date or date and time, declared once, in the Facts section of the file whose subject owns it (`§ Constructs § Declaring a Construct § A Fact`), and named by that fact's name wherever a cell, a guard, a trigger or a step reads it, in any file, its time zone, where it matters, stated in the fact's Means.

**The value in force —** a value that changes from a date on, as a rate or a limit does, is a fact read at an instant: a construct reads it at the start of the period it computes unless its prose names another instant, and a period a change falls within says how it is split. A rule changed from a date is one construct testing the period's date, not two.

**Backdated and withdrawn —** an instant computed from a fact follows the fact while the machine waits on it, so it moves when the fact changes and is withdrawn when the fact is removed, a departure where UML leaves a time event fixed once activated. A status that may change on past dates is derived from its facts each time it is read, never a machine's state.

**Calendars —** date and time arithmetic is FEEL's, in the Gregorian calendar (`specs/methodology/external-references.md § External References [Name: DMN]`, its section 10.3.2.15, Table 57). An end-of-month rule other than FEEL's is named where it is used; another calendar, a business-day calendar among them, is a named input; and a length counting both its first and its last day is written with `+ 1`.

**An instant already past —** an absolute instant already past when its state is entered is taken at once, a departure, UML leaving it unsaid (`specs/methodology/external-references.md § External References [Name: UML]`, its section 13.3.3.4).

**A relative amount —** the amount of relative time passing may be a fact, read each time its state is entered; and time counted from a condition becoming true is an absolute instant computed from the recorded fact of when it did.

**A job's run —** a time or a condition a periodic job detects, as a close of business does, is written as the job's run, something done: the trigger names the run, as `the close of business for a date` does, and the section of the construct it runs says what a missed run and a late run do, catching up each date missed, only the latest, or losing it.

## When to Use Which

Choose the simplest construct that meets the need. State Machine is the most general of the constructs, able to express anything Decision Table, Decision Tree or DAG can, and that generality is why it is not the default. This section's Decision Tree defaults each path to the simpler construct. It routes to State Machine only when a specific need forces it, or when what is described is an entity's status over time, which a State Machine writes using only the parts its case needs. Over a DAG, the need is a genuine cycle, a materially branching choice, or an intentional conditional stop.

**Construct:** Decision Tree

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | What is being described? | An entity's status over time, not the steps of a process that acts on it | Use State Machine |
| 1.2 | | A rule that determines an outcome | Go to step 3 |
| 1.3 | | A multi-step process orchestrating tasks or services to produce a result | Go to step 4 |
| 1.4 | | A computational procedure that produces a value or a transformation | Use Algorithm |
| 1.5 | | An invariant that must always hold, regardless of which path was taken | Use Constraint |
| 1.6 | | An entry of one kind written repeatedly into the specs or the working files, each stating the same named fields, not data the product stores | Use Record Form |
| 3.1 | Do the conditions have a genuine order of evaluation, where a later condition only makes sense once an earlier one has been answered a certain way? | No, each condition makes sense on its own, whichever row takes precedence | Use Decision Table |
| 3.2 | | Yes | Use Decision Tree |
| 4.1 | Does the process ever repeat a step under some condition, branch into materially different downstream handling, or have an intentional conditional stop that is not an error case? | No | Use DAG |
| 4.2 | | Yes | Use State Machine |

**Combining constructs —** these are not mutually exclusive inside one spec. A single task in a DAG or a state in a State Machine can itself have its work done by a Decision Table, a Decision Tree, or an Algorithm. In an expense approval process, the step that routes a claim is a Decision Table over independent conditions: the claim's amount band, its category, and whether a receipt is attached. The step that works out the reimbursable total is an Algorithm: it sums the line items, applies each category's own cap, and deducts any advance already paid. A State Machine's transition can be triggered by a process completing a step, a claim moving from under review to approved when the approval step approves it. A Constraint can bound what any of the others is allowed to produce: a reimbursable total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own step flooring the total at zero rather than left as an expectation. Use as many constructs as a spec needs, and never force one to do a job another is built for.

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
