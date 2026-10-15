## Purpose

This file defines the bounded, approved set of structured modeling constructs, rather than free prose, for authoring specs in this repo. Prose can describe anything, since human language has no limit, but it cannot be checked for what it leaves out: a paragraph can describe a process while never mentioning what happens under some condition, and nothing about reading it flags the gap. A construct can be checked for exactly that, the definition of each construct an author uses listing what an instance of it is checked for, and `§ When to Use Which` chooses one wherever a rule needs it, prose everywhere else.

The set is bounded and approved: a new definition, a construct, an abstract base or an interface, earns its place only by filling a real gap none of the existing ones cover, not by preference for a different notation, and extending the set is a deliberate decision, made by updating this file first, never an ad hoc addition inside a single spec.

## Fields

A field, wherever it is written, a spec's, a working file's or a construct's, is written as a line opening with its key in bold, the colon inside the bold, then a space and its value: `**{Field Label}:** {value}`, each part in braces replaced. It opens a paragraph, a line of its own within one, or a list item, its marker a hyphen; the hyphen and any indentation before the key are no part of it. A bold phrase closing on a dash is a lead-in instead (`specs/methodology/spec-style.md § Bold Lead-ins`).

**Key —** one the form defining the field declares, so a reader or a script looks a field up by a name it already knows. An unknown key is an error, not a new field, and a field appears only where the form declaring its key places it. A key means what its form defines: two forms may declare the same key, a design document's Status and a follow-up's, or a fact's Type and a steering decision's, each read by the form whose field it is. A field's key is a field label, as `Sign-off` or `Default Value` is, so it stays plain and matches exactly wherever it is written.

**Required, or its default value —** each form declaring a field says whether it is required: yes, no, or the condition under which it is. A form declaring other parts in the same table as its fields, sections, say, says the same of each of them. One required under a condition is present where the condition holds and absent where it does not. One that is not required has a default value, which a reader and a script take in its place when it is absent, as a typed language reads a value or its default. A default value of `none` leaves its absence as it is. A field that is not required is written only where its value differs from its default value, so each thing has one way to be said. A form declaring its fields in a table gives a Required and a Default Value column, the default value empty where the field is required, under a condition too; one declaring a field in prose says so in its prose. A required field or part missing is an error, as an unknown key is.

**Value —** runs from the key to the next line opening with a field's key, or to the end of the paragraph. Where the form defining the field says so, the value is instead a list: the key stands on a line of its own and the list sits directly beneath it, ending at the next line whose very first character opens a field's key, with no list marker or indentation before it, or at the end of its section.

## Defining Constructs

How every construct's definition and its instances work, stated before any definition in `§ Constructs` relies on it. A construct's section in `§ Constructs` is its definition, and each use of it an instance (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), as a class and its objects are: every instance is held to the rules of its construct's definition, of each definition that one extends and of each interface they implement. A definition is written in the constructs themselves, as a self-hosted compiler's language states its own rules, so it may use an instance of any construct, one defined after it among them, but never one resting on what it defines: as a self-hosted compiler writes its own core in a more basic syntax, a definition whose need the construct it defines would meet takes a more basic construct, and a table defining the language the constructs' cells are written in, FEEL's values, operators and functions (`specs/methodology/expressions.md § Expressions § FEEL`), is a Basic Table, never a construct whose cells that language writes. The most basic is the plain table, a table as GitHub Flavored Markdown writes one (`specs/methodology/spec-style.md § Markdown`), rows of cells under a header, which every reader and agent already knows. A Basic Table is a plain table plus what the canon adds, a Table Name (`§ Constructs § Tabular Construct`), a Reference Key, Required columns and their checks (`§ Constructs § Basic Table`): a definition before that section, and that section itself, write plain tables, declaring none of the additions, a table of fields taking the columns and the key `§ Constructs § Construct` gives it; a table declaring an addition comes after that section. The audit checks each instance against its definition, as `specs/methodology/scope.md § Rules and Skills` has a rule's checks made.

**A shape two definitions share —** a shape alone relates no definitions. Where definitions share what they are, a base they extend or an interface they implement states it once (`§ Defining Constructs § Inheritance`, `§ Defining Constructs § Interfaces and Members`); where they only represent a similar need the same way, each defines what its own need takes, citing neither the other nor the first to use the shape.

**Form or prose —** the line between a construct and prose runs through a construct's own section, the one defining it in `§ Constructs` and a spec's section holding an instance alike, between what its tables write and what the section's prose holds. A thing the prose could state is a column, a field or a form of the construct, with a check, where an outcome the spec states depends on it and the files alone could check what it says, as an exclusive choice's Guard column is, whether a move is taken deciding where the entity goes, or, in an instance, is written nowhere where its tables already give it, as the order of an Algorithm's steps is given by their numbers; where no stated outcome depends on it, it is prose, as an Algorithm's work in words is, which decides nothing; and where a stated outcome depends on it but only a judgment can check what it says, it is prose, and a reading audit asks it, as what a state's work is. Where a stated outcome depends on it and whether the files could check it is arguable, the form is favored, since a rule without a check is a suggestion (`specs/methodology/scope.md § Rules and Skills`), and a form that costs a new construct or a notation is the deliberate decision extending the set, made by updating this file first.

**A definition's fields —** each a field (`§ Fields`) opening a paragraph of its own, in this table's order and then each member of an interface it sets, directly after the prose opening its section and before any lead-in or table, so a definition's fields always come first:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Modifier | no | none | "Abstract", "Interface" | what kind of definition it is, as `§ Defining Constructs § Modifiers` has each; none for a concrete definition, which its instances declare |
| Extends | where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces | | text | the citation of the one definition it extends, its base; for an interface, a list of the interfaces it extends |
| Implements | no | none | text | a list, a citation of each interface it implements |

A Modifier, an Implements or a member Specified By Definition, the Locator among them, outside a definition's section is reported.

**Fields and lead-ins in a definition —** a definition's text uses a field wherever a form declares the key, and a lead-in everywhere else, as any text does (`§ Fields`, `specs/methodology/spec-style.md § Bold Lead-ins`). Its own fields are those this section's table declares; a member it sets is a field its interface's table of members declares; and the fields its instances declare, written in each instance and never in the definition, are its interfaces' members Specified By Instance, the members Specified By Definition Or Instance it leaves to them, and the fields of its own table of fields. Every other bold label in a definition, introducing its fields, its columns, its checks or its naming, is a lead-in, for a reader scanning it.

### Inheritance

**Extending —** a definition extends at most one base, as single inheritance has it, and every definition but `§ Constructs § Construct` itself and an interface extends it, directly or through its base. It holds everything its base holds, implements every interface its base implements, and states only what it adds: it may add fields, columns and rules, and bound what its base leaves open, never loosen or redefine what its base states, nor declare again a field or a column its base declares. A level is earned by the change test of `specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`, however deep a chain runs. A base's section comes before the section of every definition extending it, so the canon reads top down and no definition extends itself; using a construct needs no such order. An instance extending another instance of its construct is the instance's own `Extends` field (`§ Constructs § Declared Construct`).

**Checks —** an Extends citing no definition, or one whose section comes after its own; a definition but an interface citing more than one; a definition but `§ Constructs § Construct` and an interface giving none; and a field or a column a definition declares where a definition it extends declares it, are reported.

### Modifiers

A definition's Modifier field says what kind of definition it is, from a closed set; one giving none is concrete, its instances declared where they are used.

**Abstract —** a definition no instance declares: a base stating once what the definitions extending it share, as `§ Constructs § Construct` and `§ Constructs § Tabular Construct` are. How it may leave an interface's member to the definitions extending it is `§ Defining Constructs § Interfaces and Members`'.

**Interface —** a contract definitions on different branches implement, never a base they extend: a capability they share, stated once, never a mixin bringing its contents into a definition unseen, implemented as `§ Defining Constructs § Interfaces and Members` has it.

No definition is both abstract and an interface. A Construct field naming an abstract definition or an interface, and a Modifier neither `Abstract` nor `Interface`, are reported.

### Interfaces and Members

**Implementing an interface —** a definition implements as many interfaces as it needs, citing each in its Implements field, composition by reference (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), and implements every interface its base implements; an interface extends one or more interfaces, its contracts carrying no structure to collide, and a definition implementing it implements those too. An interface's section comes after `§ Constructs § Construct` and before the section of every definition implementing it or extending it.

**Members —** what an interface asks of each definition implementing it, each a field, given in the interface's table of members: a table of fields (`§ Constructs § Construct`) with a `Specified By` column after `Field`, saying who sets the field, a row's Required, Default Value and Values how it is set, by whoever its Specified By names:

| Specified By | A Member |
|---|---|
| Definition | set by every concrete definition implementing the interface, in a field of its own, every instance alike, and declared by no instance; an abstract definition may leave it to the definitions extending it |
| Instance | declared by each instance as the interface's row has it, and set by no definition |
| Definition Or Instance | set by a definition, every instance alike, or left to each instance, declared as the interface's row has it; an instance never declares one its definition sets |

A definition leaving a member to its instances may narrow it by a row of its own table of fields, as `§ Constructs § Record Form` requires its Reference Key where a type extends no other; it never removes one, a member some of an interface's implementers cannot take being an interface of its own, which only those taking it implement. A member a definition sets is never set again by its instance or by a definition extending it. A definition's own fields, those `§ Defining Constructs`' table declares, are never an interface's members. Declared Construct's Extends, which an instance declares, and a definition's own Extends share a key and are two fields, each read by the form declaring it (`§ Fields`).

**Checks —** an Implements citing what is no interface, or one whose section comes after its own; an interface whose section comes before `§ Constructs § Construct`'s, an interface extending what is no interface, and a definition extending an interface; a member Specified By Definition a concrete definition implementing its interface leaves unset, and one Specified By Instance a definition sets; a field a definition sets or narrows that is a member of no interface it implements, its bases' and the interfaces they extend among them; a member set where a definition it extends sets it; and an instance declaring a member its definition sets, are reported.

### References and Names

**A reference to a definition —** a Construct field, and a definition's Extends or Implements field, is the citation of the definition it names, an instance's Extends citing the instance it extends (`§ Constructs § Declared Construct`), (`specs/methodology/sourcing-and-citation.md § Writing a Citation`), locally qualified as any citation is, its path left out only within the definition's own file: `specs/methodology/modeling-constructs.md § Constructs § Decision Table` in any other file. Its citation, not its name, keeps a definition apart from every other, a construct an application defines among them. A Construct field that is no citation of its construct's definition, locally qualified, is reported, but a bare name in the application specs, read so until they are migrated.

**A definition's name —** says what its instances are, or, for a definition others build on, what it adds to a construct, as `Tabular Construct` and `Keyed Construct` do, and stands on its own wherever it is read, never a bare adjective or a participle, so a name is chosen for its reader; the reading audit judges it.

### Declaring a Construct

**Recognized by their shape —** some forms are so basic that a reader and an agent know them on sight and need nothing to say what they are: a field, a bold key and its value (`§ Fields`), and a Basic Table, any table outside a declared construct's block (`§ Constructs § Basic Table`). Every other construct names itself: it implements `§ Constructs § Declared Construct`, its instance opening with a `**Construct:**` field citing its definition.

**The block —** the `**Construct:**` field (`§ Fields`) opens a paragraph of its own before the construct's first table. The fields a construct sets for itself, a Decision Table's `**Hit Policy:**` or an Algorithm's `**Inputs:**` and `**Output:**`, follow it in the order the tables of the interfaces it implements give the members its instances declare, in its Implements' order, and then its own section's table, a member its own table narrows taking its place there, each opening a paragraph of its own, and its tables follow them. The declaration, its fields and its tables make one block, ending with the last table its form gives, nothing else sitting among them but a `**Table Name:**` opening one of its tables, directly before that table (`§ Constructs § Tabular Construct`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`).

**One construct to a section —** a section holds at most one declared construct of its own, not counting its subsections', so a citation of the section names the construct. Whatever prose the section needs sits between its heading and the `**Construct:**` field, or after the construct's last table, never inside its block, and another construct, a Constraint on an Algorithm's output say, takes a section of its own. A construct's multiple tables, a State Machine's States and Transitions, are one construct, and a Basic Table, such as a definition, an index or a catalogue, may sit beside it, a citation of a part naming the one table its key's columns or its path reach (`§ Constructs § Keyed Construct`).

#### Fact

A fact multiple constructs test, where it is one fact by `specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`, is declared once, as DMN's item definition is (`specs/methodology/external-references.md § External References [Name: DMN]`). It narrows the item definition to a value of one type FEEL names, a list, a context or a function among them, and adds the unit a number is counted in, the decimal places a value written to it is rounded to, the FEEL function a derived value is given by, its value as its entity is created, whether the fact may be absent and what it means. A fact's name is words separated by single spaces, each opening with a letter and holding letters, digits and apostrophes, a hyphen joining two runs of them, but a boolean fact's, which is a question, any words ending in a question mark; its first word is none FEEL keeps for itself (`specs/methodology/expressions.md § Expressions § FEEL § Names`); and its Values are values, never a fact's name. Its Initial Value is UML's default value, a Property's defaultValue evaluated when an instance is created, its section 9.5.3 (`specs/methodology/external-references.md § External References [Name: UML]`). A Decision Table names a fact it tests as `§ Constructs § Decision Table` sets. A file's facts sit in its record section of this type, a record type (`§ Constructs § Record Form`), in the file whose subject owns them:

**Construct:** `§ Constructs § Record Form`

**Plural Name:** Facts

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the fact's name |
| Type | no | yes | | text | its type, as FEEL names it (`specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions`), `list<…>` and `context<…>` among them, and a function's, `function<{parameters}> -> {type}` |
| Values | no | no | none | text | the values it may take, as FEEL's unary tests, DMN's allowed values (`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`), where its type alone does not bound them; or, for a fact whose Type is `string`, the citation of the section holding a closed set, its record section or its Basic Table, its values the identifying values of its members, keyed by one field or one column (`§ Constructs § Record Form`, `§ Constructs § Basic Table`) |
| Unit | no | no | none | text | the unit a number is counted in |
| Decimal Places | no | no | none | text | the decimal places a number is held to, a whole number or the name of a fact its file declares, as a currency's minor units (`specs/methodology/external-references.md § External References [Name: ISO 4217]`), a value written to it rounded as `specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time` has it; on a function, the value it gives |
| Derivation | no | no | none | text | where its Type is a function's, the FEEL function giving its value, `function({parameters}) {expression}`, where the specs define it; none where a system computes it outside them, its Means saying what does (`§ Constructs § Algorithm`) |
| Initial Value | no | no | none | text | its value as its entity is created, a FEEL expression of its Type, judged with its file's facts in scope |
| May Be Absent | no | no | No | "Yes", "No" | whether it may have no value |
| Means | no | yes | | text | what the fact is |

**Checks —** a Facts record whose name is no fact's name, opens with a word FEEL keeps, or, a boolean fact's, asks no question, or whose Values are empty, written plain, in no form of FEEL's unary tests, or name a fact, or cite no record section of a type identifying its records by one field, nor a Basic Table keyed by one column, or cite one on a fact whose Type is not `string`, or whose Type is no type FEEL names, or whose Decimal Places is neither a whole number nor a fact its file declares, or sits on a fact that is neither a number nor a function giving one, or whose Derivation sits on a fact that is no function, or is in no form of a FEEL function, or whose Initial Value is in no form FEEL has or of another kind than its Type, is reported.

## Constructs

The definitions, each held to `§ Defining Constructs`.

### Construct

The root every other definition but an interface extends, holding what every construct shares: an instance's fields, given by its definition, so every construct's fields are declared one way and checked alike.

**Modifier:** Abstract

**Fields —** an instance declares only the fields its definition gives (`§ Fields`), those of each interface it implements among them. A definition gives them in a table of fields, as is each table of fields the definitions under `§ Constructs` are written with, a row to each field, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Field` | the field's key |
| `Required` | whether it must be given, yes, no, or the condition under which it must, by an instance, by a definition for its own fields, or, in an interface's table of members, by whoever its Specified By names |
| `Default Value` | its default value, empty where it is required, as `§ Fields` has it |
| `Values` | the values it may hold, as Values has them |
| `Holds` | what is stated in it |

A table of fields is keyed by its `Field` column, and every cell holds a value but a required field's Default Value, left blank.

**Checks —** an instance declaring a field its definition does not give, a record type's table of fields holding a row of more or fewer cells than its header, a cell holding no value but a required field's Default Value, and a Values cell in none of Values' forms, are reported.

**Values —** what a field may hold: a list of its values, each in double quotes and separated by commas, which the audit checks every value against; a citation of the section that lists them, a closed set's record section or its keyed Basic Table among them, whose members' identifying values the audit checks every value against too; or `text`, any value its Holds describes.

### Declared Construct

What a construct that names itself shares, every construct but the Basic Table, a form recognized by its shape (`§ Defining Constructs § Declaring a Construct`): each instance opens with a `**Construct:**` field, so a reader and an audit know it as one wherever it sits, and is described and named as this section has it.

**Modifier:** Interface

**Members —** the fields every instance declares:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Construct | Instance | yes | | text | the citation of its construct's definition (`§ Defining Constructs § References and Names`), a concrete definition implementing this one |
| Extends | Instance | no | none | text | the citation of the construct of the same kind it extends, which it is a sub-definition of (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`), holding everything its base holds and more: its tables hold what it adds, read as one construct with its base |

An Extends citing no construct, or one of another kind, and a construct whose section opens with no description before its Construct field, are reported; a construct declaring Extends is checked for its fields and its tables' form, and for nothing its section checks a whole construct for, since its tables hold a part of one.

**Description —** a construct's section opens with prose saying what the construct models, before its `**Construct:**` field, written for a reader meeting it for the first time, so the specs carry what documentation drawn from them tells the people using the system. A record type's description is the same prose, before its declaration.

**Name —** the heading of the section holding a construct is the construct's name, which its citations and its readers use: it names a thing, as `Payroll Run`, or asks the question the construct answers, never an activity, as `Running payroll`. A section titled for an activity gives its construct a subsection named for what the construct is, as `§ Defining Constructs § Declaring a Construct` gives its Fact; one titled for a thing or a question, as `§ When to Use Which` is, holds its construct itself. Not every construct is named, a form recognized by its shape, as a Basic Table is, naming nothing, and a definition's own guidance for naming its instances is optional, given only where the construct has guidance of its own, its instances otherwise left to this rule. This guides the names of a construct's instances, so a definition no instance declares, an abstract definition or an interface, gives none; its own name is guided by `§ Defining Constructs § References and Names`.

### Ordered Construct

What a construct whose result could depend on the order it takes its inputs or gives its results in shares: that order stated, never left to one no one chose.

**Modifier:** Interface

**Members —** the order, as an instance declares it:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Order | Instance | where the construct leaves open the order it takes its inputs or gives its results in | | text | that order, or `any` where its result is the same in every order, so a result is never left to an order no one chose, unless a Constraint enforced by `nothing:` records that the system leaves it open (`§ Constructs § Constraint`) |

### Configured Construct

What a construct whose rows, states or steps the system stores as data shares, as `§ When to Use Which § A Configured Instance` has a configured instance: the facts holding that data named, its written tables an example of it, so the data its users change is held to a shape the specs write and the audit checks.

**Modifier:** Interface

**Members —** where the data is held, as an instance declares it:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Held In | Instance | no | none | text | where it is a configured instance (`§ When to Use Which § A Configured Instance`), a list, an item for each table its form gives, in that order: the name of the fact the system holds that table's rows in, as data its users change, a colon and the citation of the Facts record declaring it, as a Decision Table's Reads item is written; the record's Type a list of a context whose entries are named as that table's columns, its Name column among them where it has one, so the data and the written table, an example of it, are held to one shape |

A Held In naming a fact nothing declares, or one whose Type is no list of a context, or a context whose entries are not the table's columns, or giving an item for other than each table its form gives, is reported.

### Keyed Construct

What a construct whose instances' parts are cited shares: a part of an instance selected by a citation naming its key's values (`specs/methodology/sourcing-and-citation.md § Writing a Citation`), so any part of a keyed instance is cited, and its citation checked, the same way.

**Modifier:** Interface

**Members —** its key, and how a key reaches a part:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Reference Key | Definition Or Instance | no | none | text | what selects one part: the names of its key's columns or fields, in order and separated by commas, one key, multiple naming one part together, as a tuple does; or, where its construct keeps its keys in more than one place, a list, an item to each place, the path to its key |
| Locator | Definition | yes | | text | where its instances keep their keys, and how a key or a path to it reaches one part, so an agent reading the definition knows how to reach a keyed target |

**Parts —** each part's values under its key are its identifying values: required, every part giving each a value, and unique, alone or together, among the parts of the table or the record section holding them, so a reader tells each part from the rest. An instance declaring its own Reference Key, a record type or a Basic Table, names its natural key, the field or fields, or the column or columns, naming each part as its readers know it, where its parts have one; it helps a reader understand the set and holds its author's parts to the intent, a citation by it an added benefit.

**A part a citation names —** its identifying values are short, kept stable for its part's life, on one line, and hold no `§`, `;` or `]`, since a citation names one part by them. A table whose cited natural key is too long is a record type's records, as `§ When to Use Which § A Table's Construct` has it. A citation carries a value verbatim, markup and all, as `specs/methodology/sourcing-and-citation.md § Writing a Citation` has it. A value no citation names is as long as it naturally is.

**Checks —** a part's key value left blank, two parts of one table or record section sharing their key's values, a value a citation names holding `§`, `;` or `]`, two or more tables in one section whose keys are declared by the same columns, unless all but one declare a distinct Table Name, a definition's Reference Key giving no path to a column of each place where its instances keep their keys in more than one, and a citation written as no key its construct has, or matching no part, are reported.

**Key or a path to it —** a construct whose instances keep their keys in one place is cited by its key alone, `[Name: Session Timeout]`; one keeping them in more than one place, multiple keyed tables or nested constructs, by a path to the key, its levels joined by dots, `one.two.three.key`, in its Reference Key, an item to each place its keys are kept, in the order they come, and in every citation of one of its parts, `[Table.Key: value]`. It is JSONPath's dot notation for a member's name (`specs/methodology/external-references.md § External References [Name: JSONPath]`), naming the path to the key and nothing more, as a column qualified by its table is written. Each level is a field label, the name its definition or its `**Table Name:**` gives the place, or the key, so the dots always part the levels. A citation names one table in its section: a declared construct keeping its keys in one place by its key alone, a Table Name it declares only labelling its table for a reader, a Basic Table declaring no Table Name by its key's columns, and a Basic Table declaring one, or a table a definition names, by the path its name and its key make, `[Terms.Term: …]`, as a State Machine's states are cited; of two or more tables in one section whose keys are declared by the same columns, by a Reference Key or by a definition naming its tables, all but one declare a distinct Table Name (`§ Constructs § Tabular Construct`), or stand in sections of their own; a table keyed by its form, a table of fields or a `Column | Holds` table (`§ Constructs § Construct`, `§ Constructs § Tabular Construct`), has no row cited and takes no part in it.

#### Part Identifier

The form a part's citation takes, Keyed Construct's contract applied to a construct's parts.

**A part of a construct —** is named as `§ Constructs § Keyed Construct` has a part named, its value under its construct's key its identifier, so a reader and an audit can find the part and check it is there. A part is named so wherever it is named from outside its construct's section; within the section, the construct's cells and the prose around it name it by its value alone, as a jump names a step, so a part's identifier is always written as a value a citation names is. A citation names one part, and multiple parts take a citation each.

A table its construct's Reference Key names `Name` for opens with a column headed `Name` exactly where a part of it is cited from outside its construct's section: the column comes with the first such citation and goes with the last, and while it is there every row gives a Name.

### Tabular Construct

The tabular structure every construct extending it takes: a table of rows and columns, any number of each, which a construct extending it may bound, its columns, its rows or both. A table is the one representation that is precise, referable row by row, readable in plain text with no rendering step, and parseable without ambiguity, which is why a construct whose instances write rows extends this one.

**Modifier:** Abstract

**Extends:** `§ Constructs § Construct`

**A field-label column —** a column headed by a field label (`specs/methodology/glossary.md`) is a field of each row, as a record's field is (`§ Constructs § Record Form`): its header names what every cell in it holds, and each cell holds the row's value of it.

**Columns —** a construct extending it gives the columns its tables take in a `Column | Holds` table, introduced by a sentence saying which of them are headed by field labels: a row to each column, its header in backticks, or, where a table takes any number of columns of a kind, a row to that kind, named in words, in the order the table gives them. Each row says what the column's cells hold, and, for a column headed by no field label, what its header represents. A `Column | Holds` table is keyed by its `Column` column, and both its columns are required.

**Table Name —** a table may open with a `**Table Name:**` field naming it, a field label unique among the tables of its section, a paragraph of its own before the table and before any other field opening it, so a reader sees what the table is and a citation reaches its part by the path its name and its key make (`§ Constructs § Keyed Construct`). A definition naming its tables, as a State Machine's does, has each instance name each table so. Its field, in a table of fields:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Table Name | where its definition names its tables | | text | the table's name, a field label |

**What its tables hold —** an instance's tables hold every column its definition gives and no other, a column its definition gives as optional written only where its definition says. A blank cell is empty, meaning nothing, and stands only where its definition lets a cell stand blank, as a Decision Table's annotation does and a Basic Table's cell outside its key and its Required columns. Where a construct reads an empty value and acts on it, its definition names the token written for it, `none`, and that cell is never blank; a Decision Table's condition writes `-`, a test meaning any value and no token, where its row does not test it; and in a column a construct's definition gives by name, `none` or `-` stands only where that definition names it, a cell of any other column holding the word as any other word.

**Checks —** an instance's table headed otherwise than its definition gives, a row of more or fewer cells than its header, a cell left blank where its definition lets none stand blank, `none` or `-` in a column a construct's definition gives by name, where that definition names neither, and a Table Name that is no field label, or one another table of its section declares, are reported.

### Decision Table

A table deciding the outcome of a case, so every case a rule decides is written down and checked for one that two rows decide or none does. Each row states, in its condition columns, the cases it matches, and in its outcome columns the outcome they are given. An outcome is decided whether anything acts on it now, later or never: a decision is apart from any action on it. A rule that is a lookup, a table there to decide by one condition (`§ When to Use Which § A Table's Construct`), is authored as a Decision Table with a single condition column, and a decision whose conditions are asked in an order is one too, as A tree of questions has it.

It is the decision table of DMN, the Object Management Group's Decision Model and Notation (`specs/methodology/external-references.md § External References [Name: DMN]`), and its cells, its computed headers and its computed outcomes are written in FEEL, DMN's expression language, adopted whole as `specs/methodology/expressions.md § Expressions § FEEL` states it, its departure for a cell a word written plain. DMN's information requirements, chaining one decision to another, are written as a table's Reads field; DMN's other parts, its Decision Requirements Diagrams, its Business Knowledge Models, its decision services and its boxed expressions, are outside the set, and a project needing one adds it so. That file and the hit policies this section gives are all an author needs, so an agent that cannot fetch DMN, or does not know it, loses nothing a Decision Table relies on.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Name

**Locator:** a row of its table, matched by its Name column, its keys kept in one place, so a citation writes its key alone, `[Name: …]`

**Fields —** after those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Hit Policy | no | Unique | `§ Constructs § Decision Table` | its hit policy, as this section's table of them names one |
| Reads | no | none | text | a list, an item for each fact or outcome it reads from elsewhere: its name, a colon, and the citation of the Facts record declaring it or of the construct deciding it |
| Conditions | yes | | text | its condition columns, named by their headers, separated by commas |
| Computed | no | none | text | its outcome columns whose cells are FEEL expressions, named by their headers, separated by commas |
| Annotations | no | none | text | its annotations, named by their headers, separated by commas |
| Input Values | no | none | text | a list, an item for each condition it gives values for: its header, a colon, and its values as FEEL's unary tests naming no fact (`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`), `null` among them where its fact may be absent; a question takes no item |
| Output Values | where its hit policy is Priority or Output order | | text | a list, an item for each outcome column it ranks by: its header, a colon, and its values as strings in double quotes separated by commas, highest priority first, the one writing of DMN's output values a ranking reads |
| Default Output | no | none | text | the outcome where no row matches: a value, or, with several outcome columns, a list, an item for each: its header, a colon and its value |

Its columns are of these kinds, `Name` and each annotation headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the row's name (`§ Constructs § Keyed Construct § Part Identifier`) |
| a condition | the tests its cells make of the value its header names, as Facts has it |
| an outcome | the outcome the row's cases are given, under its header's name |
| an annotation | what describes or illustrates the row |

**Columns —** its condition columns come first, after a Name column where it has one (`§ Constructs § Keyed Construct § Part Identifier`), and no condition or outcome column is headed `Name`. Its outcome columns follow them, one or more of each, and then its annotations, columns that only describe or illustrate a row, which neither the match nor the check reads, a cell of one left empty where it has nothing to add. Its `**Conditions:**` field names its condition columns, a lookup's one among them, so which columns are conditions is declared, never inferred. A condition's header holds no comma, and no header an Input Values or Output Values item names holds a colon, since those fields separate headers by them. An outcome cell outside a Computed column is never written as a test, `-`, `not(…)`, a comparison or a range, nor as a list, which would show a condition declared an outcome. Its `**Annotations:**` field names its annotations.

**Facts —** each condition column tests one fact. Its header names the fact, as `§ Defining Constructs § Declaring a Construct § Fact` has a fact's name written. Where the column tests a value computed from facts, its header is that computation in FEEL instead, DMN's input expression (DMN 8.2.3): a header holding `+`, `*`, `/`, `<`, `>`, `=`, a bracket, a parenthesis, a minus between spaces or a dot between two words, a path such as `installment.due date`, computes, and no other does, so a word such as `and`, `in` or `between` leaves a header a name. A computed header holds no comma, so its functions take one argument and it writes no list. A question, a header ending in a question mark, names a boolean fact, its values `true` and `false`, however its words read. A fact its file's Facts section declares by its name (`§ Defining Constructs § Declaring a Construct § Fact`) is typed by that record: its column's cells test values of its Type, and its Values, or a question's `true` and `false`, are the column's values, so the table's Input Values field gives it no item; `null` joins them, and tests it, only where it may be absent. A fact or an outcome read from elsewhere is an item of the `**Reads:**` field, its name beside the citation of the Facts record declaring it or of the construct deciding it, so a table reads another's outcome as one of its facts, DMN's information requirement (DMN 6.3.13); a fact so read is typed by its record, as a fact its file declares is, wherever the record sits. A cell, a computed header or a computed outcome names only a condition's fact, a fact its file's Facts section declares, or a Reads item, and a cell ends only at a fact of its column's kind.

**Cells —** a row matches a case only when all its conditions hold. Each condition cell holds only what tests its condition, what explains or illustrates the value going in an annotation, and tests it by FEEL's unary tests (`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`), which say what it means, or by a value written plain. The table's checks of overlap and coverage decide a table whose every cell is in one of the forms the checks read and ends at no fact, and the reading audit reads any other table for them.

The forms the checks read are these:

- a value written plain, the whole cell, commas and all, the one form FEEL does not have, standing for the string FEEL writes in quotes; it is no number, never `true`, `false`, `null` or `-`, holds no `?`, never opens with `not(`, `<`, `>`, `=`, `!`, `@`, a bracket, a brace, a parenthesis, a double quote, `date(`, `date and time(`, `time(` or `duration(`, and never opens with `null`, `true` or `false` and a comma, so it is never taken for another form, and never read as a fact's name;
- strings in double quotes separated by commas, as `"Gold", "Silver"`, each a word however it reads, so `"2"` is no number;
- a number, a date, a date and time, a time or a duration, as `specs/methodology/expressions.md § Expressions § FEEL § Its Values` writes each, alone, compared, as `< 0.5`, or bounding a range, as `[0.5..0.8)`; an end of a comparison or of a range may be a fact's name, as `< pause end` or `[1..max term]`, and `=` stands before a fact's name, as `= base currency`, a value being tested as itself and never after `=`, an expression a cell tests equality with written after `=`, and a name never standing alone as a whole cell;
- `true` or `false`, testing a question;
- `null`, matching a fact that is absent; an absent fact meets `-` only where its column's values hold `null`, and meets every other form as `specs/methodology/expressions.md § Expressions § FEEL § Null and Three-Valued Logic` has an absent value tested;
- several of these separated by commas, opening with `null` or with what opens another of these forms but a number, so a cell opening with a word or a number is never read as several;
- `not(…)` around any of these;
- `-`, for a condition the row does not test.

A condition column's cells, and its Input Values, test values of one kind, words, numbers, dates, dates and times, times, or durations of one of their two kinds, `null` aside, so no comparison rests on how one kind is read as another. In a table of two or more rows, no condition column holds one and the same cell in every row, but for a configured instance's, whose columns are its data's (`§ When to Use Which § A Configured Instance`): a column holding `-` in every row is no condition of the table; and one holding the same test in every row, where the table takes one row's outcome and gives no Default Output, is no condition of the table but of what runs it, telling no case the table decides from another, so it is held where the construct running the table, or a table reading it by Reads, decides it. Where the table gives a Default Output, or takes every row a case matches, a case that test excludes takes the default, or no row, so the column decides.

An outcome decided when any one of several conditions holds is written as a row for each; under Unique, the rows are written so no case matches two. For an outcome decided when condition A is a or condition B is b, one row tests A for `a`, with `-` for B, and another tests A by `not(a)` and B for `b`.

**Outcomes —** an outcome cell holds a value, what the case is sent to. It is never an action done, the canon's rule: evaluating a table changes nothing, FEEL having no side effects, DMN 10.3, and a table's input expressions none on one another, DMN 8.2.8, so what acts on the outcome is the construct running the table. What becomes of a request, turned away for a reason or taken, is such an outcome, as `§ Constructs § Decision Table § A Request Turned Away` has it. It is written as a condition's cell writes one, a word plain or quoted alike, a number, a date, a date and time, a time, a duration, `true`, `false` or `null`, a question's outcome `true`, `false` or `null` alone. A column its `**Computed:**` field names holds in each cell a FEEL expression over the facts a cell may name, as `principal * rate` (DMN 8.2.10, 8.3.3). A FEEL expression, in a computed outcome or a computed header, is any FEEL writes (`specs/methodology/expressions.md § Expressions § FEEL § Its Expressions`), naming only those facts and the functions FEEL builds in, a word in it written in quotes; and an outcome computed by a walk whose order changes it cites the Algorithm doing it. Its outcome columns are decided by its conditions together, and an outcome other conditions decide is a table of its own, a part needing both citing both.

**Values —** an `**Input Values:**` field gives a condition's possible values, as DMN's input values do, for each condition it names. A question takes no item, Facts giving its values. A cell naming a value they do not hold, or matching none they hold, is outside them. Where every condition gives them, the table takes one row's outcome and no cell tests against a fact, whether every case matches a row is decided rather than read. An `**Output Values:**` field gives, for each outcome column a Priority or an Output order table ranks by, its values as a list, highest priority first, and is written for no other hit policy; where it names several columns, rows rank by the first, then by the next where they tie. A case matching no row takes the table's Default Output where it gives one, and `null` where it does not, under every hit policy (DMN 10.3.2.10); a `**Default Output:**` field, optional, gives that outcome. A table taking every row a case matches, Rule order, Output order or a Collect, is not checked for a case no row matches, `null` there meaning that no row applies. Under First, the outcome where no other row matches is a last row testing nothing, `-` in every condition, which a Name can cite, never a Default Output, the one of DMN's two writings the section keeps. A Default Output written `none` is the field absent, so an outcome meaning that a case is given nothing takes a word of its own.

**What is one —** a table there to decide an outcome from the criteria its earlier columns hold is a Decision Table, as `§ When to Use Which § A Table's Construct` has a table's construct chosen, unless it is another construct's own table, a State Machine's transitions or an Algorithm's steps, say. A table there to define items, each row saying what its item is, decides nothing, and is a record type's records or a Basic Table by that section.

**Hit policy —** which of the rows a case matches give it its outcome, named in a `**Hit Policy:**` field as DMN names it, its default value DMN's default, as its table of fields gives:

| Hit Policy | A Case |
|---|---|
| Unique | matches one row at most, since no two rows can match one case |
| Any | may match several rows, each giving the same outcome |
| Priority | takes the outcome of the row it matches whose outcome comes first in its Output Values |
| First | takes the outcome of the first row it matches, so the rows' order states which takes precedence |
| Rule order | takes the outcome of every row it matches, in the rows' order |
| Output order | takes the outcome of every row it matches, in its Output Values' order |
| Collect | takes the outcome of every row it matches, combining them, or, as `Collect sum`, `Collect count`, `Collect min` or `Collect max`, aggregating them, as DMN's C+, C#, C< and C> do |

A table taking the outcome of every row it matches, Rule order, Output order or a Collect that does not aggregate, has its rows written so that, wherever one case matches two of them, both their outcomes can be carried out. An aggregating Collect has one outcome column, its cells numbers but for a count.

**A tree of questions —** a decision whose later conditions make sense only once an earlier one has been answered a certain way is a First table: the rows stand in the order the questions are asked, and a condition a row never asks is `-` in it (DMN 8.2.8). A condition that means one thing under one earlier answer and another thing under another is a column for each meaning; and a path that is a decision of its own, asked elsewhere too, is a table of its own, read by Reads. For example, a support ticket routed by its severity, then by whether a known fix matches it, then by its plan:

```markdown
## Ticket Route

Where a support ticket is sent: by its severity, then a known fix, then its plan.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** severity, known fix matches?, plan

**Input Values:**

- severity: "critical", "major", "minor"
- plan: "paid", "free"

| severity | known fix matches? | plan | Route |
|---|---|---|---|
| critical | - | - | the on-call engineer |
| - | true | - | an automated reply |
| - | - | paid | a support engineer |
| - | - | - | the community forum |
```

Whether a known fix matches is never asked of a critical ticket, and the plan only of one no fix matches, as the tree would ask them; which fix matches, a decision of its own, would be a table of its own, read by the Reads of a table testing it.

**Name —** a Decision Table is named for what it decides, `Intake Route`.

**Checks —** an instance is reported for:

- a cell in no form FEEL or its departure for a cell has, a value tested after `=`, or a condition column testing values of more than one kind;
- an expression or a cell in no form FEEL has, naming what no fact, binding or function names, combining values of two kinds, reaching by a path a part a value does not hold, calling a function FEEL does not build in, or giving one a number of arguments none of its signatures takes, a minus before what is neither a number nor a duration, a filter testing neither a yes or no nor a place, or an `@` value in no form;
- a question's outcome other than `true`, `false` or `null`;
- a condition's header neither a fact's name nor a computation;
- an annotation's header that is no field label;
- a cell, a computed header or a computed outcome naming a fact nothing declares, or combining values of two kinds, or a cell ending at a fact of another kind than its column;
- a Reads item that is no fact's name, a colon and a citation, or a Computed field naming no outcome column;
- a condition column of a table of two or more rows holding one and the same cell in every row, `-`, or one test where it takes one row's outcome and gives no Default Output, a configured instance's aside;
- a cell testing another kind than its fact's Type, or `null` where its fact may not be absent;
- an Input Values item given for a fact a Facts record declares, empty, written plain, in no form of FEEL's unary tests, or naming a fact;
- a cell outside its column's values;
- where it takes one row's outcome and gives no Default Output, a case no row matches;
- a First table falling through by a Default Output;
- a row that gives no case its outcome;
- an outcome cell outside a Computed column written as a test or a list;
- and, by its hit policy, a case two rows match where it is Unique, two rows a case matches giving different outcomes where it is Any, an outcome missing from its Output Values where it is Priority or Output order, an aggregating Collect's outcome other than one column, of numbers but for a count, or a case two rows match whose outcomes cannot both be carried out where it is Rule order, Output order or a Collect that does not aggregate.

#### A Request Turned Away

A check the system makes of a request, a command, an action asked for or a record saved, deciding whether it goes on and, where it does not, for what reason, is a Decision Table over the request where `§ When to Use Which` counts it a construct, its outcomes the reasons and what becomes of the request otherwise; a check of one fact turning a request away or taking it is prose, by that count. It is no Constraint, which states what holds (`§ Constructs § Constraint`): a request turned away is an outcome the system chooses.

- **The first reason, or every one —** under First, the rows stand in the order the system checks, a reason's row and a row sending the request on ranked by that order, and the last row tests nothing and takes the request. Under Rule order, the rows are the reasons alone, every one that applies given in the rows' order, and a request no row matches is taken, the table giving `null`; what becomes of a taken request otherwise, held or sent elsewhere, is chosen in its own right, once no reason applies.
- **Stage by stage, or item by item —** reasons given a stage at a time are an Algorithm running each stage's table in turn and ending at the first stage that gives one; reasons given for each item of a list, its loop running the table on each.
- **What runs it —** an Algorithm's step runs the table, and the Algorithm ends where the request is turned away, its Output giving the outcome; a State Machine's transitions, or a DAG's tasks, are guarded by the outcome the table gives. The table runs before any write it guards. A request turned away completes its run, which is no failure, so nothing it wrote is undone (`§ Constructs § Constraint`, its paragraph When it holds).
- **What it keeps —** a rule holding of what the system stores, which no taken request can break, is a Constraint `always`, Enforced By the rows turning away the requests that would break it, each cited by its Name. A precondition, a rule `before` the operation, is what the operation relies on, Enforced By the parts of what runs the operation that make it hold; the check this section writes is never one.
- **An action a state does not allow —** a protocol machine refuses it by its structure, the reasons it distinguishes being this table over the request (`§ Constructs § State Machine § What It Means`).

### DAG

A table of distinct tasks in an acyclic process: each the construct doing its work, the tasks it waits for, and, where it has them, its guard, its timeout and whether its failure is tolerated. Every task is considered on every run, and the tasks nothing orders run at once. Written so, what each task waits for, and what may run at once, is explicit and checked rather than implied. It is UML's activity (`specs/methodology/external-references.md § External References [Name: UML]`), adopted whole and written as a table of tasks forked and joined, with no tie to any engine, so it maps onto the DAG an orchestrator such as Airflow, Dagster or Argo Workflows defines; `§ Constructs § DAG § What It Means` states what UML means for what its table writes, and names each departure the canon makes.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Task

**Locator:** a task, a row of its table matched by its Task column, its keys kept in one place, so a citation writes its key alone, `[Task: …]`

**Fields —** after those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Runs When | yes | | text | what runs it: the citation of each construct running it, a State Machine whose state's description cites it as the state's work, or a DAG whose task's work cites it; or the occurrence it answers, written as a State Machine's trigger is written (`§ Constructs § State Machine § What It Means`), a request, a file arriving or a job's run among them, a job's run saying what a missed and a late run do (`§ Time`) |

Authored as a table, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Task` | the task's name |
| `Work` | the construct doing the task's work, or `none` |
| `Depends On` | the tasks it waits for, or `none` |
| `Guard` | what must hold on a run for the task to run, or `none` |
| `Timeout` | how long the task may run, or `none` |
| `Tolerated` | `Yes` where the run goes on past the task's failure, or `No` |

After `Depends On` come the `Guard` column, written where any of its tasks has a guard, the `Timeout` column, where any has a timeout, and the `Tolerated` column, where any task's failure is tolerated, in that order; a column every cell of which would be `none` or `No` is not written.

**Tasks —** a task's name is plain text holding no comma, not the word `and` and not ending in the word `ended`, so a dependency list reads whole. Its work is `{citation}`, the Algorithm, the Decision Table or the DAG doing it, as the worked example's check margins cites its Algorithm, run once the task runs: an Algorithm reads its Inputs from the facts the file declares, among them what an earlier task gave, and gives its Output; a Decision Table reads its conditions' facts the same and gives each outcome column's value as the fact of that column's name, its outcome columns headed by facts the file declares; and a DAG is run whole as the task, reading what its tasks read, by work or guard, less what they give, and giving what they give, no DAG holding itself through the tasks it cites. Or it is `none` where the work is done outside the specs, a person's task or an external system's, a file arriving or another system's job ending among them, written `none, leaving {fact}, {fact}` where it leaves facts the tasks after it read, as `none, leaving margins`, each a fact the file declares, the prose after the table saying whose the work is and when it counts as done. A DAG's work is never an Algorithm's work in words, a step's (`§ Constructs § Algorithm`), but this citation or `none`. The occurrence that starts a run is its Runs When, never a task; a task whose work is `none` waits only within a run, after what it depends on. Its dependencies are `none`, or a list, `{task}, {task}`, as `extract prices, extract costs`, each item a task it waits for to be done, or `{task} ended`, as `load ended`, a task it waits for to have ended however it did, as a task that reports or cleans up does, written only of a task that can end other than done. No task depends on itself, directly or through the tasks it depends on. Its guard is `{condition}`, a FEEL boolean over the facts its file declares (`specs/methodology/expressions.md § Expressions § FEEL`), as `some m in margins satisfies m.flagged?`, read as the task would run, a guard reading facts as the task's work does. Its timeout is `@"{duration}"`, a FEEL duration, as `@"PT30M"`, or a fact of that type the file declares. Its tolerated is `Yes`, written only of a task that can fail, or `No`. A dependency the logic needs is a row's Depends On, never an order written in prose; a construct a DAG would run twice with different inputs is an Algorithm whose steps run it with its bindings, the task citing that Algorithm, since a task's work reads and gives facts by name alone.

**Run —** a run of a DAG considers every task. A task runs once each task it depends on is done or skipped, or has ended where it waits for that, and its guard, where it has one, holds, the tasks free at once running at once; a task whose guard does not hold is skipped; a task is unreached where a task it waits for to be done failed or was unreached; and a task whose timeout passes before it is done fails, its work ended and what it wrote undone as a failed operation's is, a nested DAG's run failing with it. A task fails where the run of the construct its work cites fails, as an operation does (`§ Constructs § Constraint`), an Algorithm's or a DAG's run, a Decision Table's never, or where its timeout passes; work that is `none` ends done, or fails by its timeout alone, what goes wrong outside the specs being a fact it leaves. So a task can fail where its work is an Algorithm or a DAG or it has a timeout; it can be unreached where a task it waits for to be done can fail or be unreached, a guard alone only skipping, and a dependency `ended` never leaving its waiter unreached; and it can end other than done where it can fail, be skipped or be unreached. A task ends done, skipped, failed or unreached; `{task} ended` waits for any of these; and a task that is not done gives nothing, the facts its work would give or its `none` would leave holding what they held before it, or no value where nothing had set them. A failed task whose tolerated is `No` fails the run; one whose tolerated is `Yes` ends failed, its own writes undone, and the run goes on, what waited for it to be done unreached and what waited for it `ended` run. The run ends once no task is running and none can run, and fails where a task failed whose tolerated is `No`. A run that fails is all or none, as `§ Constructs § Constraint` has an operation, except for what a task wrote that reaches a failed task through a dependency `ended`, which is kept, as a report or a clean-up is; what a nested DAG's run keeps so, it keeps, its parent task's failure undoing the rest of what that run wrote. Facts pass between tasks by name, a task's work, and its guard, reading what the file declares and what the tasks it reaches through its dependencies gave, never a fact a task after it gives, unless that task reads it too and so rewrites it; the facts the occurrence gives a run, its date or the request among them, are facts the file declares, set as the run begins. A fact a task reads that some task it reaches gives is declared May Be Absent (`§ Defining Constructs § Declaring a Construct § Fact`) unless one such task gives it surely, a giver being sure where it is not guarded, not reached through a dependency `ended`, and, within a nested DAG, neither tolerated nor waiting to be done, directly or through others, for a task that is, since there the nested run completes past the failure and its parent task ends done, and an Output the work's Inputs also name given surely by any task, a nested DAG's tasks' works' among them, the fact holding its earlier value where the task is not done; a tolerated task in the reader's own DAG gives surely to what waits for it to be done, which is unreached where it fails and never reads. Two tasks free at once, neither reaching the other through its dependencies, give no fact in common and neither reads, by its work or its guard, a fact the other gives, since an order the run leaves open would decide its value; a result an order among free tasks changes states that order (`§ Constructs § Ordered Construct`).

**What the table does not write —** a task waiting for whichever of several tasks ends first is a State Machine's transition on the first occurrence (`§ Constructs § State Machine`), never a dependency; a task's retries, a pool or a priority among tasks are operations, stated in the prose after the table or held by a Constraint, never a row; and a flow over an unbounded stream, windowed or joined as it runs, is not written, as `§ Constructs § Algorithm` has a stream, a pipeline run once per event being a DAG whose Runs When is the event.

**What is no DAG —** a process that waits within a task's work on anything but that task's completion is a State Machine, whose trigger is the wait, and one that repeats a step on a condition or branches into different downstream handling, with no wait, is a State Machine or an Algorithm, as `§ When to Use Which` chooses; the same work once per item of a list is an Algorithm's loop `at once` (`§ Constructs § Algorithm`), gathering what each pass gives, a task's work being such an Algorithm where a DAG holds it; and a process whose tasks or their order are configured as data is an Algorithm over the configuration, its loop taking each configured task in turn, a configuration shipped with the system being an instance, data, never a DAG.

**A worked example —** a nightly pricing run, two extracts free at once, a check of the margins they give with a timeout, a review a person makes only where a margin is flagged, a load that waits for the check and the review, and a report that runs however the load ended and whose own failure the run tolerates, written whole as a file would hold it:

```markdown
## Nightly Pricing

The nightly pricing run: prices and costs extracted, margins checked and reviewed, then loaded and reported.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § DAG`

**Runs When:** the nightly pricing run, at 02:00 on each business date, a missed run caught up on the next and a late run taken when it comes

| Task | Work | Depends On | Guard | Timeout | Tolerated |
|---|---|---|---|---|---|
| extract prices | `§ Price Extraction` | none | none | none | No |
| extract costs | `§ Cost Extraction` | none | none | none | No |
| check margins | `§ Margin Check` | extract prices, extract costs | none | @"PT30M" | No |
| review flagged | none, leaving margins | check margins | some m in margins satisfies m.flagged? | none | No |
| load | `§ Margin Load` | check margins, review flagged | none | none | No |
| report | `§ Report Run` | load ended | none | none | Yes |

Review flagged is the pricing analyst's: each flagged margin is confirmed or corrected in the margins list, done when the analyst marks the review complete.

## Price Extraction

The night's valid prices, taken from the price feed.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- price feed

**Output:**

- prices

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set prices to price feed[valid?] |
| 2 | End |

## Cost Extraction

The night's valid costs, taken from the cost feed.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- cost feed

**Output:**

- costs

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set costs to cost feed[valid?] |
| 2 | End |

## Margin Check

Each sku's margin, flagged where it falls below the floor.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- prices
- costs
- floor

**Output:**

- margins

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set margins to for p in prices return {sku: p.sku, margin: p.price - costs[sku = p.sku][1].cost, flagged?: p.price - costs[sku = p.sku][1].cost < floor} |
| 2 | End |

## Margin Load

The load of the reviewed margins, giving how many were written.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- margins

**Output:**

- loaded

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set loaded to count(margins) |
| 2 | End |

## Report Run

The run's report of what it loaded for the business date.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- loaded
- business date

**Output:**

- report

**Runs When:** `§ Nightly Pricing`

| Step | Action |
|---|---|
| 1 | Set report to {loaded: loaded, for: business date} |
| 2 | End |

## Facts

**Records:**

- **Name:** business date
  **Type:** date
  **Means:** the date the run prices, the business date the nightly run is launched for, in the trading desk's zone

- **Name:** price feed
  **Type:** list<context<sku: string, price: number, valid?: boolean>>
  **Means:** the night's prices as the feed delivers them

- **Name:** cost feed
  **Type:** list<context<sku: string, cost: number, valid?: boolean>>
  **Means:** the night's costs as the feed delivers them

- **Name:** prices
  **Type:** list<context<sku: string, price: number>>
  **Means:** the valid prices

- **Name:** costs
  **Type:** list<context<sku: string, cost: number>>
  **Means:** the valid costs

- **Name:** floor
  **Type:** number
  **Means:** the margin below which a sku is flagged

- **Name:** margins
  **Type:** list<context<sku: string, margin: number, flagged?: boolean>>
  **Means:** each sku's margin, flagged where it is below the floor, as the review left it

- **Name:** loaded
  **Type:** number
  **May Be Absent:** Yes
  **Means:** how many margins the load wrote, absent where the load failed

- **Name:** report
  **Type:** context<loaded: number, for: date>
  **Means:** the run's report, what it loaded and the business date it priced
```

**Name —** a DAG is named for its process as a thing, `Nightly Pricing`, never for an activity, `Extract Prices`.

**Checks —** a DAG's names, dependencies, cycles, guards, timeouts and tolerated cells are checked in its file, and its works, what its tasks give and read and what runs it across files, its citations resolved, an Algorithm a task's work cites having that DAG among what runs it, which its Runs When names (`§ Constructs § Algorithm`). Whether each task's work is the whole of it, whether a task whose work is `none` is said to be whose and when done, and whether what runs the DAG is run on it are read.

An instance is reported for:

- no Runs When field;
- two tasks sharing a name;
- a task's name holding a comma or the word `and`, or ending in the word `ended`;
- a work that is neither `none`, alone or leaving facts, nor a citation resolving to an Algorithm, a Decision Table or a DAG, one citing a part of a construct, or a DAG holding itself through the tasks it cites;
- a Decision Table a task runs whose outcome column no fact declares, or a `none` leaving a fact nothing declares;
- a dependency naming a task the table does not hold, or `ended` on a task that can only end done;
- a task that depends on itself, directly or through others, and so never runs;
- a guard in no form FEEL has, giving no yes or no, naming a fact nothing declares, combining values of two kinds or reaching a part a fact does not hold;
- a timeout that is neither a FEEL duration literal nor a declared fact of a duration type;
- a tolerated that is neither `Yes` nor `No`, or `Yes` on a task that cannot fail;
- a Guard or a Timeout column every cell of which is `none`, or a Tolerated column every cell of which is `No`;
- two tasks free at once whose work gives one fact, or one of which reads, by its work or its guard, a fact the other gives;
- a task reading a fact a task after it gives without reading it, or a fact that some task before it gives and none gives surely, whose record does not say it may be absent;
- a Runs When citing a construct that does not run the DAG, or leaving out a DAG or a State Machine that does.

#### What It Means

A DAG means what UML's activity means for what its table writes, each statement citing the section of UML it rests on, so neither an author nor a reader needs to recall the standard. The canon's rules beyond UML are its departures, each named where it is stated.

**A run —** the DAG is an Activity, its section 15.2.3.1, and each run an execution, what runs it the Runs When names (`§ Constructs § DAG`, its Runs When field). Facts pass between tasks as Variables, its section 15.2.3.5, read and written by name.

**A task —** a task whose work cites an Algorithm, a Decision Table or a DAG is a CallBehaviorAction, its section 16.3.3.1, calling that construct, a Decision Table taken as the Behavior it calls, the departure `§ Constructs § Algorithm § What It Means` names for a run; a task whose work is `none` is an OpaqueAction, its section 16.2.3.2, its body the prose after the table, which says whose it is and when it counts as done, a person's task and an external system's alike, what it leaves written in its cell as its output. That a task's work is cited by name and read from the file's facts, rather than wired by pins, is the departure the Algorithm's run makes.

**A dependency, and tasks at once —** a dependency is a ControlFlow from the task waited for to the task waiting, its section 15.2.3.3; the tasks nothing orders are reached through a ForkNode, its section 15.3.3.3, and what waits for several of them through a JoinNode, its section 15.3.3.4, the table standing for the forks and joins UML draws, every task's incoming flows joined and its outgoing flows forked.

**A guard, and a timeout —** a task's guard is the guard on the ActivityEdge offering the task its token, its section 15.2.3.3, from the fork or the join before it, with a DecisionNode, its section 15.3.3.6, placed after it so that where the guard fails the token is shunted to the downstream JoinNode, as UML's own note on 15.3.3.3 has it for a guarded edge from a fork: a skipped task counting as done for what depends on it is that shunt, and no departure. Where every task is guarded and no guard holds, nothing runs and the run ends, UML's join receiving every shunted token. A task's timeout is a wait time action, its section 16.10.3.1, its trigger a TimeEvent, its section 13.3.3.4, on an interrupting edge of an InterruptibleActivityRegion holding the task, its section 15.6.3.2, which ends the task's work when the time passes; that the task then fails, its writes undone, and that a person's or an external system's work no longer counts, is the canon's departure; the region, which `§ Constructs § Algorithm § What It Means` has among what the Algorithm's table does not write, this table writes by the one column.

**An end, and a failure —** the run ends as an Activity's execution completes, its section 15.2.3.6, once no task is running and none can run. A task that fails raises an exception which, uncaught, ends the run, its sections 16.3.3.1 and 15.5.3.2; a task whose tolerated is `Yes` has an ExceptionHandler, its section 15.5.3.2, its tolerated cell standing for the handler. That UML's handler, its body complete, offers tokens to everything downstream as though the task had completed, where the canon leaves unreached what waited for the task to be done and runs only what waited `ended`, is the canon's departure; so is the run going on past an untolerated failure to what waits `ended`, keeping what such a task writes, and so is a run all or none, what it wrote undone where it fails, as `§ Constructs § Constraint § What It Means` has it for an operation.

### State Machine

A model of the states a system or an entity can be in, the transitions between them, and the conditions under which each is taken: it answers where the entity is in its journey, and what happens when something happens in a given state, so a reviewer can check that every case is covered. It is UML's state machine (`specs/methodology/external-references.md § External References [Name: UML]`), adopted whole and written as tables, with no tie to any serialization or execution engine; `§ Constructs § State Machine § What It Means` states what UML means for what its tables write, and names each departure the canon makes from UML. A machine whose every transition is taken on its trigger alone, an entity's plain lifecycle, is a State Machine leaving its optional parts unused, no construct of its own (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`).

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:**
- States.State
- Transitions.Name

**Locator:** a state, a row of its States table matched by its State column, or a transition, a row of its Transitions table matched by its Name column, its keys kept in more than one place, so a citation writes the path to its key, `[States.State: …]` or `[Transitions.Name: …]`

**Fields —** after those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Protocol | no | No | "Yes", "No" | whether it says which actions an actor may take in each state, UML's protocol state machine, rather than what the entity does, its behavioral state machine |
| Recorded In | no | none | text | the fact the entity records its state in, its name, a colon and the citation of the Facts record declaring it, as a Decision Table's Reads item is written, each state's name one of that record's Values |

Authored as a States table and a Transitions table, each opening with its `**Table Name:**`, `States` and `Transitions` (`§ Constructs § Tabular Construct`), so a reader sees each table's name and a citation reaches a part of either by the path its name and its key make.

A States table, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `State` | the name of the state, holding no comma and not the word `and`, since a From and a To list states by those |
| `Description` | what it means for an entity to be in this state |
| `Initial` | whether the entity starts in this state, Yes or No |
| `Terminal` | whether this state ends the machine's run, Yes or No |

A state drawn from a closed set, its machine recording its state in a fact whose Values cite the set's section (`§ Constructs § Record Form`), opens its description with the citation of its own member, its record or its row, and of no other, for what holding it means, and then states any work it does in this machine, so a set several workflows draw on keeps its meaning in one home and each workflow its own work.

A Transitions table, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the transition's name (`§ Constructs § Keyed Construct § Part Identifier`) |
| `From` | the state or states the entity leaves |
| `To` | the state or states the entity enters |
| `Trigger` | what happens to move the entity on, of a kind `§ Constructs § State Machine § What It Means` names, or `none` |
| `Guard` | what must hold when the trigger happens for the transition to be taken, or `none` |
| `Effect` | the citation of the Algorithm or the Decision Table the transition runs, or `none` |

After `Trigger` come the `Guard` column, written where any of its transitions has a guard, and the `Effect` column, where any runs an effect, in that order; a column every cell of which would be `none` is not written.

A guard testing a fact for a word, by `=`, `!=` or `in` a list or tests, wherever it stands in the guard, tests one of the fact's Values, as a Decision Table's cell does: the fact its machine's own file declares, or else the one other files declare alike; a name other files declare with differing Values is read, not checked.

A trigger names only what happens: whatever must hold when it happens for the move to be taken is a guard, never a qualifier written into the trigger. A trigger is written in the same words wherever it recurs, since two triggers are the same only where their words are. Each distinct thing that can happen is a trigger of its own, each action an actor may take and each outcome of an event from outside the entity, so each takes a row of its own, and no row lists triggers; a class of occurrences, named once in the section's prose with each of its members, is one trigger, UML's trigger accepting any event of a class (UML 14.2.3.9.2). A From names one state, or, for a join, joins several with `and`, so transitions from several states to one on the same trigger take a row for each From. A transition may lead back to an earlier state, a reopened item, say. A state's own work being done is not a trigger: a transition taken on it carries none. A state whose description gives it nothing to wait for cannot stay once its work is done.

What a State Machine expresses beyond a move its trigger alone decides:

- a guard, which lets a transition's trigger happen, or its From state's work be done, without the transition being taken;
- an exclusive choice: two or more transitions from one state on the same trigger, on none, or on conditions one occurrence makes true together, whose guards never both hold, a departure where UML would take either. Each of their guards is a FEEL boolean expression, UML's guard written in FEEL (`specs/methodology/expressions.md § Expressions § FEEL`), as `receipt = "attached"` or `paid on < due date and amount >= minimum`, a word in it quoted, and a guard of none tests no fact. A boolean fact it tests is a question, `fully paid?` or `not(fully paid?)`; a fact another is compared with is one a guard of the choice tests or a Facts section declares, of the kind of the fact it is compared with; and a fact a guard tests holds no word FEEL keeps in its name (`specs/methodology/expressions.md § Expressions § FEEL § Names`), so FEEL never reads a word of its name as one of its own. Where each guard is a conjunction, joined by `and`, of tests of a fact each, a comparison with a value or another fact, `in`, `between`, or a question alone or within `not(…)`, each fact tested once, read together the guards are a Unique Decision Table over those facts, each test its fact's cell and a fact a guard does not test `-`; where the state's work is done and it cannot stay, together they also cover every case; and a choice with any other guard is read for both. A guard on a transition alone on its trigger, or alone with none, is prose, and once another transition joins it, both guards take this form;
- an effect, an Algorithm or a Decision Table a transition runs as it is taken;
- a fork, a transition into several states that then run concurrently, written as one row whose To joins them with `and`;
- a join, a transition from several states running concurrently, written as one row whose From joins them with `and`, taken once every one of them has done its work.

Every fork is closed by one join, from states its branches reach, and a join closes one fork.

**Name —** a State Machine is named for the entity it follows, `Work Order`.

**Checks —** an instance is reported for:

- two states sharing a name;
- no initial state, or more than one;
- a From or To naming a state its States table does not hold;
- a state the initial state cannot reach;
- a state that is not terminal with no way out, or a terminal state with one;
- two transitions from one state on the same trigger, or on none, whose guards, read as a Unique Decision Table, can both hold, or a guard no case meets;
- such a guard in no form FEEL has, or giving no yes or no, or testing as a boolean a fact whose name asks no question, or a fact whose name holds a word FEEL keeps;
- a state that cannot stay where, once its work is done, some case takes no transition out of it;
- a fork no join closes, or a join no fork opens;
- a Transitions table's columns other than From, To and Trigger, then a Guard, an Effect or both in that order, or such a column every cell of which is `none`;
- a guard comparing a fact with another no guard of its choice tests and no Facts record declares, or of another kind;
- an Effect cell citing no Algorithm or Decision Table;
- a States or a Transitions table not opening with its Table Name, `States` or `Transitions`;
- a Recorded In field that is not a fact's name, a colon and the citation of a Facts record, a record it cites whose Values are neither a quoted list nor the citation of a closed set, or a state not among them, or a state drawn from a closed set whose description opens with no citation of its member, its record or its row, or a guard testing a fact for a word outside the fact's Values;
- a protocol machine with an Effect column, a transition with no trigger or a governed state;
- of a submachine state, a state governed by more than one machine, a machine governing itself, a governed state that is terminal or not left as its machine's exits have it, the words `governed by` naming no machine or a part of one, or naming none, and a description citing a machine's whole section without them.

#### What It Means

A State Machine means what UML's state machine means for what its tables write, each statement citing the section of UML it rests on, so neither an author nor a reader needs to recall the standard. The canon's rules beyond UML are its departures, each named where it is stated: an action a protocol machine does not take refused; a protocol machine's transitions taken on an actor's action alone; conditions one occurrence makes true together taken in one step; an exclusive choice's guards never both holding; relative time counted from entering the state; a terminal state in a fork's branch ending the run; a join carrying a trigger; `exit` naming which terminal state the machine governing a state reached; and, in `§ Time`, an instant already past taken at once and an instant following its fact.

**One occurrence at a time —** the machine handles each thing that happens fully before it takes the next, taking the transitions it enables until it reaches states where it waits, UML's run-to-completion, its section 14.2.3.9.1. An occurrence no transition is enabled by is discarded, but in a protocol machine. A state's work being done is handled ahead of anything else waiting. Conditions one occurrence makes true together are taken in its one step, a departure, UML dispatching each event on its own, the transitions they enable from one state an exclusive choice.

**A state and its initial state —** a state is UML's state; the initial state is the one the machine enters as its run begins, the target of UML's initial Pseudostate's transition, its section 14.2.3.7. Before its run begins and once it has ended, a machine is in no state, its sections 14.2.3.4.2 and 14.2.3.8.3. What must outlast a run is a fact the entity records: its status, named by the entity, as `loan status`, declared in a Facts section (`§ Defining Constructs § Declaring a Construct § Fact`), its Values the values it may take, listed, or the citation of the section holding a closed set, its record section or its keyed Basic Table, their one home; the machine names that fact in its Recorded In field, and its states are those of the values it uses, a terminal state's among them, a value it does not use left out.

**A state's work —** what its description says goes on in it, begun when the state is entered, UML's entry and doActivity Behaviors, its section 14.2.3.4.3; done, it lets a transition with no trigger be taken, UML's completion transition, its section 14.2.3.8.3, at once for a state whose description states no work, and once the run of the machine governing it ends for a submachine state. A transition taken while the work runs cuts it short. A transition from a state to itself leaves the state and enters it again, UML's external transition, its section 14.2.3.8.1, its work, the run of the machine governing it and its relative times starting afresh.

**A terminal state —** the machine's run is complete, UML's final state, its section 14.2.3.6. It has no work: what its description says is the run's outcome, and work that ends a run is the effect of the transition entering it.

**A fact —** held by the entity, or by another, and set by a state's work, a transition's effect or an occurrence's data, or from outside the machine, as a payment received lowers a balance, declared in a Facts section where a guard compares a fact with it.

**A trigger —** names what happens, UML's event, its sections 13.3.3.2 to 13.3.3.4, its kind decided by what moves the entity:

**Construct:** `§ Constructs § Decision Table`

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

**A guard —** tested when its trigger happens, or when its state's work is done, against the facts as they then stand, a transition whose guard does not hold being no transition at all for that occurrence, its section 14.2.3.9.2, a transition with no guard having one always true. It may test any fact about the entity or another, another entity's recorded status among them, `loan status = "closed"`, a terminal state's name included; the state a machine governs is left by which terminal state that machine reached, tested by `exit` alone, its value that state's name, as `exit = "approved"`, a departure, UML telling its ends apart by exit points, its section 14.2.3.4.6.

**Two transitions one occurrence enables —** at most one is taken from a state, its section 14.2.3.9.3; the exclusive choice decides which. Where a governed state and a state of the machine governing it both leave on one occurrence, the inner machine's transition is taken, the more deeply nested, its sections 14.2.3.9.4 and 14.2.3.9.5.

**An effect —** the Algorithm or the Decision Table a transition's Effect cell cites, run as the transition is taken, after its From state is left and before its To state is entered, UML's effect Behavior, its sections 14.2.3.8 and 14.2.3.9.6. An action whose outcome decides where the entity goes is no effect but a state's work, the transitions from that state routing on what it found. One occurrence moving several entities in order is written in the machine it reaches first, its effect an Algorithm whose steps move the others, each moved machine's trigger citing that step and each step's move complete before the next.

**A fork and a join —** UML's fork and join Pseudostates, its section 14.2.3.7, the branches between them its orthogonal regions, its section 14.2.3.2, each running at once, one occurrence able to take one transition in each, its section 14.2.3.9.1. A terminal state reached in one branch ends the machine's run, its other branches cut short, a departure, UML's final state completing that branch's region alone, its section 14.2.3.6; and a join may carry a trigger, a departure, UML's join taking none, its section 14.2.3.7.

**A protocol machine —** a machine whose Protocol field is `Yes` is UML's protocol state machine, its section 14.4: its states hold no work, its section 14.4.3.1, so it takes no Effect column, no transition with no trigger and no governed state; each transition is taken on an actor's action, saying the state allows it, a departure where UML allows other events, its section 14.4.3.2.4; and an action no transition from the state takes is refused, a departure, UML leaving it undefined, its section 14.4.3.2.1, and leaving an operation no transition refers to callable in any state, its section 14.4.3.2.3, which the canon does not write. Where the system tells an actor why, the reasons it distinguishes are a Decision Table over the request, as `§ Constructs § Decision Table § A Request Turned Away` has it, and no other reasons are written. Whether the machine allows an action in the entity's state is a fact, named `{entity} permits {action}?`, a question, as `loan permits disbursal?`, which any construct may test, citing the machine.

**Resuming where it left off —** UML returns to where a machine was through a history Pseudostate, its section 14.2.3.4.4; the canon writes it with a fact the entity records, guarding the transitions from the machine's initial state.

**What the tables do not write —** each part of UML's state machine named in this list, and the writing the canon uses instead:

- **A composite state —** which its section 14.2.3.4.7 calls semantically equivalent to a submachine state: a nested machine is a section of its own, governing a state as `§ Constructs § State Machine § A Submachine State` has it.
- **Entry and exit points —** its sections 14.2.3.4.6 and 14.2.3.7: a machine is entered at its initial state and left by its terminal states, told apart by `exit`, as `exit = "approved"`.
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

- **Machine —** one at most; a machine never governs itself, directly or through those it governs; a governed state is never terminal, a terminal state having no work.
- **Entering it —** at the governing machine's initial state, by however many transitions reach it, the transitions from that initial state guarded by why it was entered, where that matters.
- **Leaving it by its machine's end —** by transitions with no trigger, as its table of exits has them, `exit` the one fact their guards test: a holder that routes on a fact as well leads each transition guarded by `exit` to a state with no work, whose own transitions route on that fact.
- **Leaving it on a trigger —** a transition with a trigger, taken from whatever state the governing machine is in, UML's group Transition, its sections 14.2.3.4.7 and 14.2.3.8.2. A trigger every state of the work leaves the same way, to one state outside it, is written once, on the outermost governed state whose every state it so leaves, and on no state inside it; one only some states of the work take, or take differently, is written inside the work, on each state taking it, leading to a terminal state where it ends the work.

Its table of exits:

**Construct:** `§ Constructs § Decision Table`

**Conditions:** Its machine's terminal states, Where it stands

| Its machine's terminal states | Where it stands | Left by |
|---|---|---|
| "none" | - | its triggers alone, its machine never ending |
| "one" | "outside a join's From" | one transition with no trigger and no guard |
| "more than one" | "outside a join's From" | one transition with no trigger for each, guarded `exit = "{terminal state}"`, naming the terminal state reached, so together they are an exclusive choice covering every end |
| "one", "more than one" | "in a join's From" | the join alone, taken once every branch's work is done |

### Algorithm

A precise, step-by-step computational procedure that produces a value or a transformation. Unlike a DAG or a State Machine, which orchestrate named tasks or services, an Algorithm specifies the computation inside one of those tasks, or any calculation that is not itself an orchestration. Each step written in one of its forms is checked, so a computation is stated exactly rather than described. It is UML's activity (`specs/methodology/external-references.md § External References [Name: UML]`), adopted whole and written as a numbered table of steps taken one at a time, with no tie to any language or engine; `§ Constructs § Algorithm § What It Means` states what UML means for what its table writes, and names each departure the canon makes from UML.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Step

**Locator:** a step, a row of its table matched by its Step column, its keys kept in one place, so a citation writes its key alone, `[Step: …]`

**Fields —** after those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Inputs | yes | | text | the facts it reads, each item a fact's name, or a fact's name, a colon and the citation of the Facts record declaring it in another file, as a Decision Table's Reads item is written; or none, written on the key's line |
| Output | yes | | text | the facts it gives, each item a fact's name; or none, written on the key's line, where the work its steps do is all it does |
| Runs When | yes | | text | what runs it: the citation of each construct running it, another Algorithm whose run cites it, a State Machine whose Effect cell or state's description cites it as the work done, a DAG whose task's work cites it, or a Decision Table whose computed outcome cites it as the Algorithm doing it, a citation of one of its steps or rows, a trigger, a plain outcome, an annotation and a Constraint's enforcement running nothing; or the occurrence it answers, written as a trigger of the kind something done is (`§ Constructs § State Machine § What It Means`), a request or a job's run among them, a job's run saying what a missed and a late run do (`§ Time`) |
| Precision | no | 34 | text | the significant digits each operation's result is rounded to, a whole number above zero and below 34, where its system's arithmetic holds fewer than FEEL's (`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`) |
| Rounding Mode | no | half even | text | the mode each operation's result is rounded by, and a value written to a fact holding decimal places: one of the modes `specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time` names, or the name of a fact the Algorithm knows whose Values hold only those modes, where the system's configuration chooses it |

**Facts —** a step names only a fact its Inputs or its Output name, a fact its file's Facts section declares, a fact a step sets, a loop's item and what it gathers, and a part of any of them, reached by FEEL's path, as `transaction.amount` (`specs/methodology/expressions.md § Expressions § FEEL § Its Expressions`). A fact its file's Facts section declares is typed by its record, a list's or a context's by the type its record names, so a path into it is typed too; a fact read from another file, and any other, is known by name alone, its kind read.

**A stored value and a derived one —** a fact's value never changes once set, as a FEEL context never does (`specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions`): setting a part gives the fact a new value, that part replaced and every other as it was. So:

- **A stored value —** read by path, `{fact}.{part}`, as `period.emi`: a part a step sets or the system stores.
- **A value the system derives from others —** read by a call, `{function}({value})`, given the current value, as `fully paid(period)`; never by a path, as `period.fully paid`, which keeps what it held before a step changed what it derives from. In a filter the call is given `item`, as `periods[not(fully paid(item))]`.
- **An item copied from a list —** a value too: once a step changes the list, the item is read from the list again, `{list}[{key} = {item}.{key}][1]`, as `periods[number = target.number][1]`, before it is changed, run or merged back, so no step works on, or merges back, a version older than the list's.

The function a step calls is a fact its file's Facts section declares (`§ Defining Constructs § Declaring a Construct § Fact`), its Type `function<{parameters}> -> {type}`, or one a step sets, and it is of one of these kinds:

- **A derived value —** of what it is given, as whether a period is fully paid; where the specs define it, its record's Derivation holds the FEEL function giving it.
- **A computation a system makes outside the specs —** as a library's or a service's; its record holds no Derivation, and its Means says what computes it.
- **A function a computation sets —** FEEL's own function value, `Set {name} to function({parameters}) {expression}`, as `Set lowest to function(xs) xs[number = min(xs.number)][1]`, named within the Algorithm alone.
- **An operation giving a changed value —** of what it is given, as `mapping added(transaction, installment.number, component, portion)`, a step writing what it gives back to a fact.

A computation another construct specifies is never a function: it is run. For example, a Facts record and an Algorithm reading it:

```markdown
- **Name:** fully paid
  **Type:** function<context> -> boolean
  **Derivation:** function(period) period.emi + period.credited amounts = period.paid principal + period.paid interest
  **Means:** whether a repayment period is fully paid

| Step | Action |
|---|---|
| 1 | Set period.emi to period.paid principal + period.paid interest - period.credited amounts |
| 2 | Set settled? to fully paid(period) |
| 3 | End |
```

Step 2 reads the EMI step 1 set, where `period.fully paid` would give what was true before it.

**Expressions —** a computation's expression, a comparison's condition, a loop's list and its order, a run's argument and a Terminates cell are FEEL (`specs/methodology/expressions.md § Expressions § FEEL`), each judged with the facts the step may name in scope. The checks decide each one's form, the names it holds and the kinds it combines and gives, a condition's a yes or no, a loop's list a list and a Terminates cell's a number, and that a value written to a fact, a part or an Input is of the kind its record types it; whether work computes or decides, and whether what it reads is what it means, is read.

Authored as a numbered table of steps, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Step` | the step's number, the steps numbered from 1 in order |
| `Action` | what the step does, one of the kinds Steps names |
| `Terminates` | why a step's loop ends, as A loop that must end has it, or `none` |

**Steps —** each step is one of these, and nothing else, a loop or a comparison a step of its own, never folded into another's work:

- **A computation —** `Set {fact} to {expression}`, giving the fact the expression's value; or `Set {fact}.{path} to {expression}`, giving the fact its value with that part's replaced, as FEEL's `context put` gives it, its path names joined by `.`, each reaching into a context and none through a list. A value a later step reads is set so, never in words. A value a condition chooses is one computation, FEEL's `if … then … else`, never a comparison whose only work is setting one fact, on one branch or both.
- **A run —** `Run` and the citation of the Algorithm or the Decision Table it runs, and of nothing else; then, for each fact the construct takes that the fact of the same name here does not give, ` with {input} as {expression}`, these separated by commas; then, where the run gives facts a later step reads, `, giving` and what it gives separated by commas, each a fact the construct run gives, written by its name, or `{output} as {fact}` where the fact here that holds it has another name. An Algorithm takes its Inputs and gives its Output; a Decision Table takes its conditions' facts, the facts of value its computed headers and computed outcomes name, a function they call being the table's own, and its Reads, and gives its outcomes. Each fact it takes that no `with` gives is the fact of its name here. A run of the Algorithm it belongs to, or of a construct running it back, an Algorithm's run or a Decision Table's computed outcome, recurs.
- **A loop over a list —** `For each {item} of {list}, {order}: steps {n} to {m}`, its body the steps from the one after it to step m, each pass taking the next item through them, the loop ending once every item has passed and the step after step m following. Its order is `by` a FEEL expression over the item and `ascending` or `descending`, a tie broken by `, then by` another; `in any order`, where no order changes what the loop gives; `in an order the system leaves open`, where an order changes it and none is fixed, the exception the Order field allows (`§ Constructs § Ordered Construct`); or `at once`, every pass running at the same time, a pass setting only its item and what it gathers, by a computation, a run or a loop it holds. A loop gathering a fact each pass sets writes `, gathering {fact} into {list}` before its colon. The list is set once the loop ends, and holds one value for each pass that set the fact. Its order is the order of the list walked as it stood when the loop began, sorted by the loop's keys where it has them, whatever order the passes ran in. A body reading the list reads what it held before the loop. A loop gathering its own item gathers it from every pass, changed or not, so updating some items keeps the rest. A body holds whole loops of its own, never the table's last step, and is entered only from its loop and left only at `End`: a jump from it names a step of it, and a jump from outside it names none. The order a loop walks its list is the loop's own; an Algorithm's Order field names the order it takes its Inputs and gives its Output.
- **A comparison —** `If {condition}, {branch}; otherwise, {branch}`, the condition a FEEL boolean expression, as `unprocessed amount > 0 and processing type = "horizontal"`; each branch a computation, a run or work, or nothing, written `continue`.
- **Work —** anything else the system does, written in words: posting, deleting, recording, sending. It computes no value a later step reads, decides nothing and runs no construct, a value being a computation's, a choice a comparison's and a construct's run a run's: it cites no Algorithm or Decision Table whole, a citation of one of its steps or rows referring to it and running nothing.

**Ends —** each branch, and each step that is no comparison, ends `Go to step` and the number of a step the table holds, or `End`, or else continues to the next step. A loop's last step continuing takes the next pass. `End` ends the run, inside a loop's body as anywhere, its Output's facts holding the values set, a list the loop was gathering left as it stood before the loop; it is written alone, a result named by a computation before it. Each fact the Output names is set by a computation, given by a run or gathered by a loop on every path to `End`, but one its Inputs also name, which, where no step on the path sets it, holds the value it was given. The last step, and each branch of it where it is a comparison, ends `End` or goes to another step, so the Algorithm ends only at an `End`.

**A loop that must end —** a loop is a loop over a list, a comparison one of whose branches goes back to an earlier step or to its own, or a run recurring; a step that is no comparison never goes back, so a loop whose test falls in its middle is written with its test at the step going back. A loop over a list ends with its list, fixed as the loop begins. Every other loop states why it ends in a `Terminates` column after Action: in the cell of each step going back or recurring, a FEEL expression giving the number that shrinks with each pass toward an end the step reaches, as `high - low`, or the citation of the Constraint its end rests on, one something keeps; `none` in every other cell; the column written only where a step goes back or recurs.

**Arithmetic —** a number is FEEL's (`specs/methodology/expressions.md § Expressions § FEEL § Its Values`), unless the Algorithm's Precision and Rounding Mode state its system's, each operation then rounded as `specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time` has it. A value written to a fact holding decimal places is rounded to them under either, by the Algorithm's Rounding Mode, as that section has it. Any other value is rounded only by a computation calling `decimal` or one of FEEL's rounding functions (`specs/methodology/expressions.md § Expressions § FEEL § Its Functions`), its decimal places a number or a fact choosing them, never by the word `rounded`. An Algorithm holds one precision and one rounding mode for every step: steps its system computes with another are an Algorithm of their own, run, stating theirs, and one operation rounded otherwise is rounded by its computation's own call.

**Order —** a result that could depend on an order states it, as the Order field has it (`§ Constructs § Ordered Construct`), a loop's order with its ties broken, and a remainder's share given by the order that takes it.

**A worked example —** a schedule's instalments, each period given its share of the rate by a Decision Table, in a system holding 19 significant digits and rounding money half up, written whole as a file would hold it:

```markdown
### Instalments

A schedule's instalments, each period's share of the rate applied to its balance, and the total still due.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- periods
- rate

**Output:**

- periods
- total due

**Runs When:** `§ Schedule Build`

**Precision:** 19

**Rounding Mode:** half up

| Step | Action |
|---|---|
| 1 | For each period of periods, by period.number ascending, gathering period into periods: steps 2 to 4 |
| 2 | Run `§ Period Share` with Days as (period.due date - period.from date).days, with Annual rate as rate, giving Share as share |
| 3 | Set instalment to balance(period) * share |
| 4 | Set period.instalment to instalment |
| 5 | Set total due to sum(for p in periods[not(settled(item))] return p.instalment) |
| 6 | End |

#### Facts

**Records:**

- **Name:** periods
  **Type:** list<context<number: number, from date: date, due date: date, instalment: number>>
  **Means:** the schedule's periods, in order

- **Name:** instalment
  **Type:** number
  **Decimal Places:** 2
  **Means:** a period's instalment, held to cents

- **Name:** balance
  **Type:** function<context> -> number
  **Decimal Places:** 2
  **Means:** a period's opening balance, as the ledger computes it

- **Name:** settled
  **Type:** function<context> -> boolean
  **Derivation:** function(period) period.instalment = 0
  **Means:** whether a period has nothing left to pay
```

Step 1 walks the list in its keys' order and gathers each updated item back into it, the list set once the loop ends; step 2 runs a Decision Table, giving each fact it takes by `with` and writing its outcome `Share` to a fact of another name by `as`; step 3 multiplies money, so it writes to a fact holding decimal places, rounded to cents half up, each operation first held to 19 digits, and reads a value the ledger computes by a call; step 4 sets a part from that fact, a part holding no decimal places of its own; and step 5 reads a value the specs derive, by a call given each current period, its `settled` defined once by its Derivation.

**Name —** an Algorithm is named for its process as a thing, `Report Assembly`, never for an activity, `Running payroll`.

**Checks —** an instance is reported for:

- no Inputs, Output or Runs When field, an Inputs item that is neither a fact's name nor a name, a colon and a citation, an Output item that is no fact's name, or an Output fact its Inputs do not name that nothing sets;
- two steps sharing a number;
- a jump to a step the table does not hold;
- a Precision that is no whole number above zero and below 34, or a Rounding Mode that is neither a mode `specs/methodology/expressions.md` names nor a fact the Algorithm knows whose Values hold only modes;
- a step in none of its forms, a comparison not written in its form, whose condition gives no yes or no or whose branch is a loop, a computation not written `Set` a fact or its part `to` an expression, a run not written `Run`, a citation, its arguments and what it gives, a run citing no Algorithm or Decision Table, a loop over a list not written in its form, or work citing an Algorithm or a Decision Table whole;
- an expression in no form FEEL has, naming a fact the step does not know, combining values of two kinds, or reaching a part a fact does not hold;
- a value written to a fact, a part or an Input of another kind, or a part set by a path that is not names joined by `.` or that reaches through a list;
- a run giving a fact the construct run does not give, naming as an argument no fact it takes, or leaving a fact it takes neither given nor known;
- a comparison whose only work is setting one fact;
- a comparison both of whose branches go back to an earlier step or to its own;
- a step that is no comparison going back;
- a loop's body that is not the steps after it, reaches past the body holding it or holds the table's last step, a jump into or out of a body, a loop over what is no list, or a pass `at once` setting a fact other than its item and what it gathers;
- a step going back or a run recurring with no Terminates cell, a Terminates cell giving no number or citing no Constraint, or citing one nothing enforces, one on a step that neither goes back nor recurs, or a Terminates column every cell of which is none;
- a jump or an `End` that does not end its branch, or an `End` with words after it;
- a last step, or a branch of it, that neither ends nor jumps;
- a Runs When citing a construct that does not run it, or leaving out one that does.

#### What It Means

An Algorithm means what UML's activity means for what its table writes, each statement citing the section of UML it rests on, so neither an author nor a reader needs to recall the standard. The canon's rules beyond UML are its departures, each named where it is stated: a loop going back or a run recurring stating why it ends; a value a later step reads set only by a computation; a run's arguments and what it gives matched to the construct's facts by name; a gathered list in the order of the list walked, whatever order the passes ran in, holding the item of every pass where a loop gathers its own item, and left as it stood where an `End` in the body ends the run; a Decision Table run as a Behavior; an Output its Inputs also name holding what it was given where nothing sets it; and `End` inside a loop's body ending the whole run.

**A run —** the Algorithm is an Activity, its section 15.2.3.1, and each run of it an execution, taking its Inputs as its input parameters and giving its Output as its output parameters, its sections 15.2.3.6 and 15.4.3.2. Its Inputs and Output are its parameters, a fact both name an inout parameter, its section 15.2.3.6. That it holds what it was given where nothing sets it is a departure, UML passing out only what flows to its output node. A run of another construct is a CallBehaviorAction, its section 16.3.3.1, a Decision Table taken as the Behavior it calls, a departure, a DMN decision being no UML Behavior, synchronous, the step waiting until that construct's run ends; each `with` an argument, the value its input pin passes to a parameter, and each fact it takes given none the value a ReadVariableAction, its section 16.9.3.2, reads from the fact of that name; and each fact it gives the value on an output pin, written to the fact of that name, or to the fact `as` names, by an AddVariableValueAction, its section 16.9.3.3. UML matches pins to parameters by their order; the canon matches them by name, a departure. A run recurring states why it ends, a departure, UML requiring none.

**A step —** an Action, its section 16.2.3.1, its steps following one another by control flows, its section 15.2.3.3. A computation is a ValueSpecificationAction, its section 16.4.3.5, whose value an AddVariableValueAction writes to the fact, held as a Variable is, its sections 15.2.3.5 and 16.9.3.3, replacing what it held, FEEL its language; a computation setting a part reads the fact by a ReadVariableAction, its section 16.9.3.2, replaces the part's value by an AddStructuralFeatureValueAction for each name of its path, `isReplaceAll` true, its section 16.8.3.3, which, the fact's value being a data value, gives a modified copy on its result pin, its section 16.8.3.1, and writes that copy back to the fact by an AddVariableValueAction; and work is an OpaqueAction whose body is written in words, its section 16.2.3.2. That a value a later step reads is set only by a computation is a departure, UML letting an OpaqueAction write values.

**A comparison and a jump —** a comparison is a DecisionNode whose two outgoing flows are guarded by its condition and by `else`, its section 15.3.3.6; a step two flows reach, by a jump or by following another, is entered through a MergeNode, its section 15.3.3.5, a jump back so forming a loop. That such a loop states why it ends is a departure, UML requiring none.

**A loop over a list —** an ExpansionRegion over the list, its section 16.12.3: iterative where it is ordered `by` keys, its passes run one after another in that order, the list sorted by them; iterative over an unordered collection where it is `in any order` or `in an order the system leaves open`; parallel where it is `at once`, its passes free to overlap; and what it gathers an output ExpansionNode, offered once every pass has completed, holding the values of the passes that set it in the order the input collection induces. Its list is fixed as it begins, the input collection of UML's expansion region. That a gathered list keeps the order of the list walked where the region is unordered or parallel, holds the item of a pass that set nothing where the loop gathers its own item, and is left as it stood where an `End` inside the body ends the run, are departures, UML leaving the first undefined, filtering out the second's pass and offering the third partly filled.

**An end —** `End` is an ActivityFinalNode, its section 15.3.3.2: the first reached ends the run and every flow in it, the Output's facts holding the values set. Inside a loop's body it ends the whole run, a departure, UML's final node inside a structured node or an expansion region ending that node or region alone, its sections 16.11.3.1 and 16.12.3.

**What the table does not write —** each of these, by UML's sections cited, is written elsewhere or not at all:

- **A fork and a join of steps, and steps run at once other than a loop's passes —** its sections 15.3.3.3 and 15.3.3.4: a DAG (`§ Constructs § DAG`).
- **A wait for an occurrence —** its section 16.10.3.1, AcceptEventAction: a State Machine's trigger, the Algorithm running once it happens.
- **An exception raised and handled —** its sections 16.13.3.2 and 15.5.3.2: a failure is an outcome its Output gives, the run ending at `End` with it.
- **An interruptible region and a partition —** its section 15.6.3: not written by an Algorithm's table; a task's timeout writes the region in a DAG's (`§ Constructs § DAG § What It Means`).
- **A stream, and an object flow other than a named fact —** its sections 13.2, 16.12.3 and 15.2.3.4: not written, a fact passing between steps by its name.

### Constraint

A rule that must hold of a system's facts, independent of any single decision point or process step: an invariant on the state or output of something else, or a condition an operation requires as it begins or guarantees once it ends. Written so, what must hold and what keeps it are stated, and a rule nothing keeps is recorded rather than hidden. It is UML's Constraint (`specs/methodology/external-references.md § External References [Name: UML]`), adopted whole and written as a table of rules, each a FEEL boolean, with no tie to any language or engine; `§ Constructs § Constraint § What It Means` states what UML means for what its table writes, and names what the canon adds to UML.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Name

**Locator:** a rule, a row of its table matched by its Name column, its keys kept in one place, so a citation writes its key alone, `[Name: …]`

Authored as a table, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the rule's name (`§ Constructs § Keyed Construct § Part Identifier`) |
| `Constraint` | the rule |
| `Applies To` | when the rule holds |
| `Enforced By` | what keeps the rule |

**Rule —** a FEEL boolean (`specs/methodology/expressions.md § Expressions § FEEL`) over the facts its file declares, each named as its Facts record declares it (`§ Defining Constructs § Declaring a Construct § Fact`), as `sum(portions) + overpayment = amount`; a Constraint sits in the file whose Facts section declares the facts its rules name, so a rule names no fact another file declares, and reaches another construct's facts only as When it holds has it. A rule of every entity of a kind names the fact holding them all, a list, and quantifies over it, `every {item} in {list} satisfies {rule}`, as `every t in transactions satisfies t.debits = t.credits`; a value as it stood before an operation is a fact declared for it, `balance before`; and a rule reaching along a chain of entities calls a function fact that gives the chain, as `ancestors(record)`. A rule governing some values only tests them in itself, `if {condition} then {rule} else true`, as `if currency.decimal places = 0 then modulo(amount, currency.multiple) = 0 else true`, since Applies To says when a rule holds, never of which values; a State Machine's state invariant is such a rule, narrowed by the fact the machine's Recorded In names, `if status = "active" then balance >= 0 else true`. Its explanation, where it needs one, is prose after the table.

**When it holds —** an operation is a run of an Algorithm or of a DAG, a transition taken with its effect, an occurrence a State Machine answers, or what a section's own text states is done, and each is all or none: an operation either completes, reaching its end, or fails, stopped by an error, a timeout or a precondition it cannot meet, and what a failed one wrote is undone, so a rule holding as it began holds as it ends (`§ Constructs § Constraint § What It Means`). A request turned away completes, and keeps what it wrote, as `§ Constructs § Decision Table § A Request Turned Away` has it. A construct whose operation keeps less than all of its writes states so where it says what a failure does. Applies To is `always`, `after {citation}` or `before {citation}`, the citation an operation's. A rule `always` holds at every rest, whenever no operation is running. A rule `after` an operation holds once a run of it completes, the operation's postcondition; a rule that holds only once some part has run, as a summary a job recomputes, is `after` that operation. A rule `before` an operation holds as its run begins, its precondition, what the operation relies on, Enforced By the parts of what runs the operation that make it hold; a check the system makes of a request is none, as `§ Constructs § Decision Table § A Request Turned Away` has it. Beside the file's facts, a rule `after` an Algorithm reads its Inputs and Output, one `before` it reads its Inputs, one `after` or `before` a transition reads those of the Algorithm its effect runs, one `before` a DAG reads what the work of its first tasks takes and one `after` it what the work of its tasks takes and gives, as `§ Constructs § DAG` has them, and one `after` or `before` an operation a section's own text states reads the file's facts alone. The citation names the operation whole, an Algorithm's or a DAG's section, a transition by its Name, or a section whose own text states what is done, never a step or a task.

**Enforcement —** Enforced By is the canon's addition to UML's Constraint, naming what keeps the rule: the citation of each part of another construct, a step, a row, a transition or a task, or of a section whose own text states the mechanism, that keeps it where a write could break it, several joined by `and`, `{citation} and {citation}`, since an invariant is kept only where every operation changing its facts keeps it. A rule a Decision Table turning requests away keeps is Enforced By that table's rows, as `§ Constructs § Decision Table § A Request Turned Away` has it. A part that breaks the rule, tolerates its breach or runs on no path keeps nothing, and is no enforcement. A rule nothing keeps is written so the specs say what holds and what does not: its Enforced By is `nothing: {what breaks it or leaves it unkept}`, citing after those words any part that keeps some of it. A rule some paths keep and others do not is written by its paths, each by when its rule holds: a path whose rule holds at every rest is an `always` row narrowed by the fact that tells the path apart, its source or its writer; a path whose rule holds only as its own operation completes is a row `after` that operation; and the path nothing keeps is the row opening `nothing:`. A Constraint enforced by `nothing:` is listed on every audit run as a warning, never a finding: the gap is the system's, recorded, and the specs are complete in recording it.

**A derived value —** a stored fact the system derives from others is a Constraint whose rule is `{fact} = {expression}`, UML's derivation specified by a constraint, `always` where the system keeps it so, or `after` the operation that recomputes it where it lags between runs, Enforced By what writes it; a value the system derives on demand, stored nowhere, is a Facts record's Derivation (`§ Constructs § Algorithm`). No Constraint states a fact's value as its entity is created: that is the Facts record's Initial Value (`§ Defining Constructs § Declaring a Construct § Fact`).

**A case a Constraint rules out —** a Decision Table covers every case the Values of the facts it tests allow (`§ Constructs § Decision Table`), a Constraint narrowing no table's cases, since a Constraint may fail. A value no fact ever holds is excluded by the fact's Values, where its type alone does not bound them, and a table then need not cover it.

**An approximation —** a rule bounding an approximation states the bound as the rule, `abs({computed} - {intended}) <= {tolerance}`, Enforced By the step that approximates.

**A worked example —** a schedule's instalments, a payment settling one, written whole as a file would hold it: an invariant over every instalment, a postcondition of the settlement reading its Output and a before-value, and a stored total the system derives and keeps only by a nightly job, a warning:

```markdown
## Instalment Settlement

A payment received, settled against its instalment up to what is due.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:**

- instalment
- payment

**Output:**

- instalment

**Runs When:** a payment is received

| Step | Action |
|---|---|
| 1 | Set instalment.paid to min(instalment.paid + payment, instalment.due) |
| 2 | End |

## Settlement Rules

What holds of a schedule's instalments as payments settle them.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Constraint`

| Constraint | Applies To | Enforced By |
|---|---|---|
| every i in instalments satisfies i.paid <= i.due | always | `§ Instalment Settlement [Step: 1]` |
| instalment.paid >= paid before | after `§ Instalment Settlement` | `§ Instalment Settlement [Step: 1]` |
| schedule.total paid = sum(for i in instalments return i.paid) | always | nothing: the total is written by a nightly job and lags the instalments between its runs |

## Facts

**Records:**

- **Name:** instalments
  **Type:** list<context<due: number, paid: number>>
  **Means:** the schedule's instalments, each with what it is due and what has been paid of it

- **Name:** instalment
  **Type:** context<due: number, paid: number>
  **Means:** the instalment a payment settles

- **Name:** payment
  **Type:** number
  **Means:** the amount received

- **Name:** paid before
  **Type:** number
  **Means:** what the instalment had paid as the settlement began

- **Name:** schedule
  **Type:** context<total paid: number>
  **Means:** the schedule, with the total its nightly job writes
```

**Checks —** a Constraint is checked with its citations resolved, once, across files, a citation that resolves to nothing being the citation checks'. Which part keeps a rule, whether a section an Applies To cites states in its own text an operation, whether every write able to break a rule is covered and whether a bounded step keeps its bound are read, never decided by the script.

An instance is reported for:

- a rule in no form FEEL has, judged with the facts in scope, giving no yes or no, naming a fact nothing declares, combining values of two kinds or reaching a part a fact does not hold;
- an Applies To that is neither `always` nor `after` or `before` a citation, or citing a step or a task, a construct that is no operation, a record section, or a State Machine and no transition of it;
- an Enforced By that is neither citations joined by `and` nor `nothing:` and words;
- a rule nothing keeps listed as a warning, never a finding.

#### What It Means

A Constraint means what UML's Constraint means for what its table writes, each statement citing the section of UML it rests on, so neither an author nor a reader needs to recall the standard. The canon's rules beyond UML are its additions, each named where it is stated.

**A rule —** a Constraint, its section 7.6.3, its rule the Constraint's specification, a ValueSpecification of type Boolean, satisfied where it evaluates to true; its language FEEL, which its section 7.6.4 leaves to the Constraint, so FEEL is no departure. The facts the rule names are its constrainedElements, and its Applies To its context, which its section 7.6.3 has decide when the Constraint is evaluated; that `always` is every rest between operations is the canon's, an addition, UML naming no such time.

**A precondition and a postcondition —** a rule `before` an operation is a precondition and one `after` it a postcondition of the Behavior the Algorithm, the DAG or the transition's effect is, its section 13.2.3.1, an Activity holding them as a Behavior does, its section 15.2.3.6: a precondition holding as the Behavior is invoked, which an implementation may assume, and a postcondition holding once its invocation completes successfully. That an operation a section's own text states takes them is the canon's, an addition, UML holding a precondition and a postcondition of a Behavior alone. A protocol transition's precondition is its guard and its postcondition a Constraint, as `§ Constructs § State Machine § What It Means` has it.

**A derived value —** a derived Property, its section 9.5.3, whose derivation may be specified by a constraint, which the Constraint whose rule is `{fact} = {expression}` is.

**An operation all or none —** an occurrence a State Machine answers is dispatched only once the one before it is fully processed, its section 14.2.3.9.1; that an occurrence, a run of an Algorithm or of a DAG, or a transition taken is all or none, what it wrote undone where it fails, failing where it does not complete, is the canon's, an addition.

**Enforced By —** the canon's addition: UML holds that an unsatisfied Constraint makes the model's realization invalid, its section 7.6.3, and says nothing of what keeps one satisfied.

### Basic Table

A table of items of one kind, each row an item and each column one of its fields: the Record Form's pattern laid out in rows (`§ Constructs § Record Form`), so items of one kind read at a glance and, where keyed, each row can be cited. It is recognized by its shape (`§ Defining Constructs § Declaring a Construct`), the one concrete construct implementing no `§ Constructs § Declared Construct`: a table outside a construct's block is a Basic Table, whatever it holds, and follows this section, never another construct's. Whether a table of entries should be one is `§ When to Use Which § A Table's Construct`'s question: one there to define items needing no more than a row declares. It is checked for its form, its key, its required columns and its citations rather than for what it leaves out. It follows no outside standard, since none meets its need.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Keyed Construct`

**Locator:** a row of the table its fields open, matched by the columns its Reference Key names, its keys kept in one place, so a citation writes its key alone, or, where the table declares a Table Name, the path its name and its key make

**Columns —** every column headed by a field label, but a header in backticks, literal text written as it is elsewhere (`specs/methodology/spec-style.md § Literal Text`), and a proper noun keeping its own casing, as `macOS`:

| Column | Holds |
|---|---|
| a field | the row's value of the field its header names, however Columns has the header written |

**Reference Key —** wherever its rows have a natural key, the column or columns naming each row as its readers know it, whether or not a row is cited, a `**Reference Key:**` field (`§ Constructs § Keyed Construct`) naming them, opening a paragraph of its own before the table, after its Table Name where it has one; a table whose rows have none declares none. Its columns are required, and their values unique together, as `§ Constructs § Keyed Construct` has every key. It names only columns its table holds. A citation names a row by its key, or by the path its Table Name and its key make, and a Basic Table declaring no key has no row cited.

**Required —** the columns besides its key every row must fill, named in a `**Required:**` field, separated by commas, opening a paragraph of its own before the table and after its Table Name and its Reference Key where it has them; any other cell may stand blank, meaning nothing (`§ Constructs § Tabular Construct`). Its own field, in a table of fields:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Required | no | none | text | the columns besides its key every row must fill, separated by commas |

**Checks —** an instance is reported for:

- a header that is no field label, but a header in backticks and a word in a proper noun's own casing;
- a Reference Key naming a column its table does not hold;
- a Required naming a column its table does not hold, or one its Reference Key names;
- a blank cell in a column its Reference Key or its Required names;
- its fields out of their order, Table Name, Reference Key, Required.

### Record Form

An entry of one kind written repeatedly into a methodology spec, an application spec, or a working file, each record stating the same named fields: what differs between records is each field's value, never which fields there are. Written so, every entry carries the fields its kind needs, each checked, and none goes missing. It follows no outside standard, since none meets its need. A closed set a spec defines may be one too (`specs/methodology/glossary.md`), its members each with fields saying what it is, as a work order's statuses, settled as a vocabulary before, and apart from, the workflows that use it; an application's sits in its product spec (`specs/methodology/spec-placement.md § Product or Technical`). Whether entries are a record type's records or a Basic Table's rows is `§ When to Use Which § A Table's Construct`'s question. A set that changes while the product runs is data, a configured instance's (`§ When to Use Which § A Configured Instance`). A schema of data the product stores is not one, however many records the product holds: the technical specs describe it as they describe data, and a closed set's technical counterpart cites the set rather than restating its records, as `specs/methodology/spec-placement.md § Product or Technical` places it.

**Extends:** `§ Constructs § Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Keyed Construct`

**Locator:** a record of the record section a citation names, matched by its identifying fields, each record section keeping its keys in one place, so a citation writes its key alone

A record type is an instance of this form, as a Decision Table is of its section, and its records are its instances (`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`). A type is defined at the home of the rule it serves, in a section titled with the type's name, as a construct's section is titled with its own, `## Open Question` say, whose prose says where its records go. It is declared there as a construct is (`§ Defining Constructs § Declaring a Construct`): a `**Construct:**` field naming this form, then its fields, then its tables, a type extending another by Extends holding every field its base holds, in its base's order, and its own after them. Its fields, after those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Plural Name | yes | | text | the plural of the type's name, which titles each section holding its records and no other section where they may sit, so a definition and a collection of records never share a title: a canon type's records may sit in any file, and an application spec's type's in the application specs, no two types reaching one file sharing a Plural Name |
| Reference Key | where it extends no type | | text | its key (`§ Constructs § Keyed Construct`), its identifying fields, a key of one field marking that field Unique; a type extending another declares none, taking its base's |

Its tables come in this order, each a table of fields as `§ Constructs § Construct` gives one. Where it declares section fields beyond a record section's own, Diagrams and Records, a table of them comes first. Then comes the table of its record fields, in the order a record gives them, with a column after `Field`, headed by a field label:

| Column | Holds |
|---|---|
| `Unique` | yes or no: whether the field's values are unique on their own across a record section's records |

**The record section —** a type's records sit together in a record section of their own, titled as its type's Plural Name has it. It holds only fields: `**Diagrams:**`, then any section fields of its own the type declares, facts about the collection as a whole, each given in the order its table of them sets and each required one present, then `**Records:**`, ending the section. A record section's own fields, in a table of fields (`§ Constructs § Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Diagrams | no | none | text | a list, a citation of each diagram rendering the section or any record in it, sorted in plain character order, so whoever edits a record meets every diagram drawing it |
| Records | yes | | text | a list, an item to each record, at least one |

A blank line separates one section field from the next, and one record from the next, and each list value ends as `§ Fields` states, so the Diagrams bullets and the records never run together.

**A record —** its fields (`§ Fields`), at most one per row of its type's table and in that order: the first on the list item's own line, each of the rest on a line indented two spaces directly beneath the one before, every line of the item belonging to one field's value. No blank line falls between a record's fields, since they are one record's facts serving one purpose, and whitespace separates only content that differs. Every record carries every field its type requires, and no field its type does not define, and no two records in one section share the values of their identifying fields. An identifying field is required.

**An identifying value —** a record's is written as `§ Constructs § Keyed Construct` has any part's; a type whose records are cited and whose natural identifier is long, a question or a description, adds a short one, its key, the natural identifier then a field marked Unique.

**Why a list —** records are not table rows, because an entry needs what a row cannot declare, as `§ When to Use Which § A Table's Construct`'s More than a row declares? has it. They are not headings, because a heading's section admits any content and further headings, where a list item holding only its fields is bounded, so a reader and a script can tell where one record ends and whether it holds exactly its type's fields.

**A closed set —** a fact whose values are a closed set's members takes them by its Values, the citation of the section holding them, its record section or, where its members need no more than a row, its keyed Basic Table (`§ Defining Constructs § Declaring a Construct § Fact`, `§ Constructs § Basic Table`), so every construct testing the fact draws on the one set: a State Machine recording its state in it, each of its states one of the set and described as `§ Constructs § State Machine` has a state drawn from a closed set described, and a Decision Table's condition testing it, each cell within it. The set's members sit in the one section cited, its home, and another section of its type holding records where they may sit is reported. Several workflows may each draw on one set, using the members each needs.

**A worked example —** a work order's statuses, a closed set a product spec defines, a fact taking its values from them, and a workflow drawing on the set, written whole as a file would hold it:

```markdown
## Work Order Status

A status a work order can hold, the set the product owner settles before, and apart from, the workflows that move a work order between them, each with the code integrations exchange for it. Its records sit in this spec.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Work Order Statuses

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the status as users read it |
| Description | no | yes | | text | what it means for a work order to hold it |
| Is Active | no | no | Yes | "Yes", "No" | whether a work order may still be given it |
| Code | yes | yes | | text | the identifier integrations exchange for it, never changed once published |

## Work Order Statuses

**Records:**

- **Name:** Open
  **Description:** raised, not yet given to a technician
  **Code:** WO-OPEN

- **Name:** Assigned
  **Description:** given to a technician to carry out
  **Code:** WO-ASGN

- **Name:** On Hold
  **Description:** paused awaiting parts, retired, no workflow giving it any longer
  **Is Active:** No
  **Code:** WO-HOLD

- **Name:** Completed
  **Description:** carried out and signed off
  **Code:** WO-DONE

- **Name:** Cancelled
  **Description:** withdrawn before it was carried out
  **Code:** WO-CANC

## Facts

**Records:**

- **Name:** work order status
  **Type:** string
  **Values:** `§ Work Order Statuses`
  **Means:** the status a work order holds

## Work Order

The workflow of a work order raised through the portal.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Recorded In:** work order status: `§ Facts [Name: work order status]`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| Open | `§ Work Order Statuses [Name: Open]`, waiting in the portal's queue for a dispatcher | Yes | No |
| Assigned | `§ Work Order Statuses [Name: Assigned]`, its technician notified by the portal | No | No |
| Completed | `§ Work Order Statuses [Name: Completed]` | No | Yes |
| Cancelled | `§ Work Order Statuses [Name: Cancelled]` | No | Yes |

**Table Name:** Transitions

| From | To | Trigger |
|---|---|---|
| Open | Assigned | a dispatcher assigns it |
| Open | Cancelled | the requester cancels it |
| Assigned | Completed | the technician signs it off |
| Assigned | Cancelled | the requester cancels it |
```

The statuses are records, not a Basic Table's rows, since Is Active takes a default and is held to its Values, and Code is unique on its own (`§ When to Use Which § A Table's Construct`). The defining section, titled with the type's name, declares it, its Plural Name titling the record section and its Reference Key, Name, what a citation of a status names; Code is unique on its own, never cited. On Hold writes Is Active, where it differs from its default. The fact's Values cite the record section, so its values are the statuses' Names, and the State Machine recorded in it uses all but the retired On Hold, each state's description opening with its status's record and then saying what goes on in it in this workflow.

**Name —** a record type is named for the entity its records are, `Work Order Status`.

**Checks —** an instance is reported for:

- a record type declared with no Plural Name, or with tables other than any table of its section fields and then its table of record fields, a field it or its base names twice, a Unique cell neither yes nor no, no Reference Key, its own or its base's, or one naming a field the type does not give or does not require, or a Default Value given where its field is required or left empty where it is not;
- its section titled with an article or with its Plural Name;
- a Plural Name another type declares;
- a record section titled with no declared type's Plural Name, or with a type's but holding no records;
- a section field its type requires missing, given out of order, at its default or outside its Values, or one its type does not declare;
- a value outside a closed set its field cites;
- a second record section of a closed set;
- a record missing a field its type requires, holding one its type does not define, holding a value its type's Values do not allow, or giving its fields out of their order;
- two records in one section sharing a value of a field its type marks Unique;
- a Reference Key on a type extending another, or of one field not marked Unique.

## Time

How a construct reads time, wherever a cell, a guard, a trigger or a step reads a date, a time or a duration.

**The clock —** a date or a time is read on a clock: the wall clock, unless a construct names another. A clock other than the wall clock, as a business date a job advances, is a fact of the Type date or date and time, declared once, in the Facts section of the file whose subject owns it (`§ Defining Constructs § Declaring a Construct § Fact`), and named by that fact's name wherever a cell, a guard, a trigger or a step reads it, in any file, its time zone, where it matters, stated in the fact's Means.

**The value in force —** a value that changes from a date on, as a rate or a limit does, is a fact read at an instant: a construct reads it at the start of the period it computes unless its prose names another instant, and a period a change falls within says how it is split. A rule changed from a date is one construct testing the period's date, not two.

**Backdated and withdrawn —** an instant computed from a fact follows the fact while the machine waits on it, so it moves when the fact changes and is withdrawn when the fact is removed, a departure where UML leaves a time event fixed once activated. A status that may change on past dates is derived from its facts each time it is read, never a machine's state.

**Calendars —** date and time arithmetic is FEEL's, in the Gregorian calendar (`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`). An end-of-month rule other than FEEL's is named where it is used; another calendar, a business-day calendar among them, is a named input; and a length counting both its first and its last day is written with `+ 1`.

**An instant already past —** an absolute instant already past when its state is entered is taken at once, a departure, UML leaving it unsaid (`specs/methodology/external-references.md § External References [Name: UML]`, its section 13.3.3.4).

**A relative amount —** the amount of relative time passing may be a fact, read each time its state is entered; and time counted from a condition becoming true is an absolute instant computed from the recorded fact of when it did.

**A job's run —** a time or a condition a periodic job detects, as a close of business does, is written as the job's run, something done: the trigger names the run, as `the close of business for a date` does, and the section of the construct it runs says what a missed run and a late run do, catching up each date missed, only the latest, or losing it.

## When to Use Which

A construct is used where a rule, a process, an entity's behavior, an entry written repeatedly into the specs or the working files, or a closed set a spec defines needs checkable completeness, and prose everywhere else: prose states a rule one fact decides, sending its cases to at most two outcomes, the fact's and its otherwise, unless the rule is written as a table, which `§ When to Use Which § A Table's Construct` decides; and a rule reading two or more facts, or one fact sending its cases to more than two outcomes, takes the construct this section's table chooses, however it reads, since routing written in an author's own words never looks like a rule to the one writing it; a claim that something holds of the system's facts sends no case anywhere and is a Constraint's (`§ Constructs § Constraint`), and a request turned away for a reason is one of the outcomes counted.

Choose the simplest construct that meets the need, by the questions its table asks, in order: the first answered yes chooses, so prose is reached first, the State Machine after every other construct a rule or a process can take, since it is the most general of them, and the Record Form, which holds entries and no logic, last. Each question is answered from the shape of the case, what it is made of and what it waits for, never from what it is called, and the construct chosen is written as its section in `§ Constructs` has it, meaning what its standard says. A table is never prose: `§ When to Use Which § A Table's Construct` decides which of a Decision Table, a record type's records and a Basic Table a table is, where these questions send its case to no DAG, Algorithm, State Machine or Constraint; and a definition whose need the construct it defines would meet takes a more basic one, as `§ Defining Constructs` has it. A table's construct is chosen as the table is written: an existing table keeps the construct its declaration gives, a table declaring none a Basic Table, until the user decides to migrate it.

**Construct:** `§ Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** Decided by one fact?, Claimed of every reachable state?, An outcome from conditions alone?, Tasks some of which run at once?, Steps run in turn?, Waits for occurrences?, Entries of one kind?

| Decided by one fact? | Claimed of every reachable state? | An outcome from conditions alone? | Tasks some of which run at once? | Steps run in turn? | Waits for occurrences? | Entries of one kind? | Construct |
|---|---|---|---|---|---|---|---|
| true | - | - | - | - | - | - | prose |
| - | true | - | - | - | - | - | Constraint |
| - | - | true | - | - | - | - | Decision Table |
| - | - | - | true | - | - | - | DAG |
| - | - | - | - | true | - | - | Algorithm |
| - | - | - | - | - | true | - | State Machine |
| - | - | - | - | - | - | true | Record Form |
| - | - | - | - | - | - | - | prose |

What each question asks, each decided from the case's shape, and what tells it from the question after it:

- **Decided by one fact? —** the rule sends its cases to outcomes by one fact, to at most two of them, the fact's and its otherwise, as a claim paid on approval where its receipt is attached and held otherwise: prose, by the count this section sets, a list naming a set's values, each with what it means, being no rule and answering no.
- **Claimed of every reachable state? —** the rule is claimed true in every state the system can reach, whatever was done to reach it, whether or not the system keeps it, or of one operation as it begins or ends: a Constraint, `always`, `before` or `after` (`§ Constructs § Constraint`). A precondition is one, and a check the system makes of a request answers no, as `§ Constructs § Decision Table § A Request Turned Away` has them; a stored value claimed equal to what others give is one, a derivation; and a value derived on demand, stored nowhere, is no construct's but a Facts record's Derivation where its expression chooses no case, and a construct the questions after this one choose where it picks among cases.
- **An outcome from conditions alone? —** the case's conditions alone pick its outcome among several, by no steps of its own, nothing keeping a status between one case and the next, whether or not anything acts on the outcome: a Decision Table (`§ Constructs § Decision Table`), what becomes of a request among them, as `§ Constructs § Decision Table § A Request Turned Away` has it. A condition that takes steps to find is an Algorithm's, whose result the table tests, and an outcome that must act, consume a counter or correct a value, is the step of the Algorithm running the table, the table deciding and the step doing.
- **Tasks some of which run at once? —** distinct units of work, each named, with what each waits for, some free to run at once, every task considered on every run: a DAG, which `§ Constructs § DAG` tells from an Algorithm's loop `at once`, from tables chained by Reads, from a process configured as data and from a process that waits within a task.
- **Steps run in turn? —** steps taken one after another, which may loop or take one path or another by a condition, nothing in them waiting for an occurrence from outside, a retry until something holds a loop stating why it ends: an Algorithm (`§ Constructs § Algorithm`). A run that parks until something outside it happens is split, each leg an Algorithm and the whole a State Machine whose states are the legs, resuming where it left off by a fact.
- **Waits for occurrences? —** something keeps a status between occurrences from outside it, an action of an actor, a message, a time or a condition becoming true, and moves when one happens, however few of a machine's parts it needs: a State Machine (`§ Constructs § State Machine`). A field actions set in some states and the system derives in another is such a machine over the states the actions move between, with one open state whose description cites the function fact whose Derivation gives the field there. The states it moves between may be the members of a closed set a spec defines, a record type's records or a Basic Table's rows settled apart from the machine, which the fact it records its state in cites (`§ Constructs § Record Form`).
- **Entries of one kind? —** an entry of one kind written again and again into the specs or the working files, each stating the same named fields, or the members of a closed set a spec defines, each saying what it is, and not the schema of data the product stores: a Record Form (`§ Constructs § Record Form`), `§ When to Use Which § A Table's Construct` choosing between a record type's records and a Basic Table for a table of them.

### A Table's Construct

Which construct a table is, among a Decision Table, a record type's records and a Basic Table, decided by what it is there for. A table is never prose, even one deciding two outcomes: these questions are asked of every table whose case `§ When to Use Which`'s questions, by its shape, send to no DAG, Algorithm, State Machine or Constraint, a process or a behavior written as a table taking the construct they choose. The author writing a table answers them, in order, the first answered yes choosing.

None is asked of a plain table a definition writes before `§ Constructs § Basic Table`, the base the constructs start from, a Basic Table declaring none of the additions, as `§ Defining Constructs` has it, of a table defining FEEL, a Basic Table as `§ Defining Constructs` has it, or of a record type the canon declares, reached by the skills and their point-of-use citations.

**Construct:** `§ Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** There to decide an outcome?, More than a row declares?

| There to decide an outcome? | More than a row declares? | Construct |
|---|---|---|
| true | - | Decision Table |
| - | true | Record Form |
| - | - | Basic Table |

What each question asks its author:

- **There to decide an outcome? —** the table is built so a case can be looked up by the criteria its earlier columns hold and given an outcome, whether or not anything acts on it, as a shipment given its rate by its zone; a table built so a reader can look up what each item is answers no, as a currency's symbol and its decimal places, and so does a table whose rows sample an open set of cases, since it cannot be checked for a case it leaves out.
- **More than a row declares? —** an entry needs a field holding a list or more than one paragraph, values held to a list of allowed values or a test, as a record type's Values declares them, a default where it is absent, uniqueness on its own beside its key, or a natural key too long for a citation naming its entries, a short identifier its key and the natural key a field marked Unique: a record type's records (`§ Constructs § Record Form`). A field an entry may leave blank is no reason, nor a value its type alone bounds.
- **Otherwise —** a Basic Table, declaring its natural key where its rows have one and the columns every row must fill (`§ Constructs § Basic Table`).

### A Configured Instance

An instance of a construct implementing `§ Constructs § Configured Construct` may be a configured instance: its rows, its states and transitions or its steps are data the system stores and its users change, held in the facts its `Held In` field names, the tables written being an example instance, which shows the data's shape and is checked as the data is, never one the system falls back to; a process whose tasks or their order are data is an Algorithm over that data, as `§ Constructs § DAG` has it. It is chosen by its shape as any other is, these questions asked of what the data does, never of the data's being stored: a value a rule reads, a setting, a threshold or a record's field, is an input and never structure; and records the system generates from its configuration are an Algorithm's Output, each then a run of the construct its shape chooses. Logic a deployment supplies as code, or chooses among by a setting, is written as its default, an Algorithm run where it is used, running a Decision Table where one decides, its contract a Constraint `before` and `after` the Algorithm (`§ Constructs § Constraint`) and its section's prose saying another may be supplied; a choice among built-in ones by a setting is a Decision Table over the setting, the setting an input. An instance is checked, as it is saved, as the written construct is, and one the checks would report is turned away; the section holding the construct says so, since a check made only of the written example is no check of the instances. An instance someone outside the system's authors owns, a clinic's own form or a tenant's own catalogue, is a specification its owner keeps, and the system's spec states what every instance obeys.

### Combining Constructs

Constructs are not mutually exclusive inside one spec: a part of one hands its work, or the deciding of its case's outcome, to another.

#### Construct Handoff

Where a part's handoff to another construct is written, decided by the part and the work:

**Construct:** `§ Constructs § Decision Table`

**Conditions:** The part, Its work

| The part | Its work | Written |
|---|---|---|
| a State Machine's state | the run of a State Machine | in its description, the words `governed by` and that machine's section cited, as `§ Constructs § State Machine § A Submachine State` has it |
| a State Machine's state | "the run of an Algorithm", "the run of a Decision Table", "the run of a DAG" | in its description, that construct's section cited as the state's work |
| a State Machine's transition | "the run of an Algorithm", "the run of a Decision Table" | in its Effect cell, as `§ Constructs § State Machine § What It Means` has an effect |
| a DAG's task | "the run of an Algorithm", "the run of a Decision Table", "the run of a DAG" | in its work cell, as `§ Constructs § DAG` has it |
| an Algorithm's step | "the run of an Algorithm", "the run of a Decision Table" | as a run, `Run` and the citation with its bindings, as `§ Constructs § Algorithm` has it |
| an Algorithm's step going back or recurring | the Constraint its end rests on | in its Terminates cell, as `§ Constructs § Algorithm` has it |
| a Decision Table | another table's outcome, read as a condition | as a Reads item, as `§ Constructs § Decision Table` has it |
| a Decision Table's computed outcome | a walk whose order changes it | the section of the Algorithm doing the walk cited in the cell, as `§ Constructs § Decision Table` has an outcome computed by a walk |

The citation says what the part does, and the part stays what its own construct makes it. A part of another construct being reached is a trigger, as a claim moves from under review to approved when a process's approval step is reached, where that process runs apart from the claim (`§ Constructs § State Machine § What It Means`, `§ Constructs § State Machine § A Submachine State`). A Decision Table's choice among the moves a request may make reaches the machine as the fact the table gives, which the transition's guard tests. An Algorithm cutting, ranking or reducing a table's hits runs the table under a policy taking every row a case matches and works on its hits in the steps after, and one applying a table again to the input it altered is a loop stating why it ends. Where an Algorithm runs on successive parts of one quantity, a Constraint states what the parts' results owe the whole's, enforced by the step carrying one part's end into the next. A Constraint may bound what any construct produces (`§ Constructs § Constraint`). In an expense approval process, the step that routes a claim is a Decision Table over independent conditions: the claim's amount band, its category, and whether a receipt is attached. The step that works out the reimbursable total is an Algorithm: it sums the line items, applies each category's own cap, and deducts any advance already paid. A Constraint holds that the total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own step flooring the total at zero rather than left as an expectation. Use as many constructs as a spec needs, and never force one to do a job another is built for.

## Diagrams

A diagram is a materialized view of a fact, for a human reader, technical or not, who wants the shape of something before deciding whether to read the mechanism behind it. Like a materialized view, it is precomputed for whoever consumes it and is never itself the source of truth: a diagram disagreeing with what it was rendered from is wrong, as a materialized view disagreeing with its tables is a bug rather than a second valid answer. An agent reads the construct behind a diagram with ease; many human readers do not, and nothing tells an author which reader will arrive, so a diagram is written for the human, and an agent benefits as well.

**Where it goes —** wherever it helps its reader most: beside the main section it renders, or above all the sections it renders, as an overview's diagram sits above its detail files. Where it goes is a judgment about the reader; its form is not.

**Form, wherever it goes —** a diagram has a heading of its own, directly followed by the diagram, then its fields (`§ Fields`), in this table's order, a table of fields (`§ Constructs § Construct`):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Caption | yes | | text | what the diagram shows, in prose |
| Sources | yes | | text | a list, a citation of the home of each fact the diagram draws |

Nothing else is in its section, and its shape is the same wherever it appears, as a Decision Table's is. The caption carries no citation, so every citation the diagram rests on has one place. The Sources field's key stands on a line of its own, its bullets sorted in plain character order, so the order is mechanical and a script can check it; that order places same-file citations after cross-file ones. A diagram is authored as a Mermaid flowchart (`specs/methodology/external-references.md § External References [Name: Mermaid]`), checked in as source rather than as an image, so it renders in plain text and diffs like everything else here. It is a flowchart even where a state diagram or sequence notation would be the more formal rendering, since one grammar across every diagram in this repo, boxes and arrows, is worth more to the readers diagrams exist for than notational precision on any single one. Authoring, rendering or changing one follows `.ai/skills/author-mermaid-diagram/`.

**What it may show —** only what its host file's own content, that file's prose or its own tables, already names. What stands behind a diagram is often far more granular, a State Machine's every state, an Algorithm's every step, and that granularity stays where it is. Check each label against the host file before adding or editing a diagram. A name, step, or distinction the host file never states is either collapsed out of the diagram or, if it genuinely belongs at that altitude, stated in the host file first and only then rendered. Choosing between them is a judgment about the host file's completeness, not about the picture. The bound falls on the diagram and not on a table beside it, because a table can carry a citation in every cell and stays checkable however specific it gets; a rendering that descended into detail its host never states would show a reader things the text around it never explains.

**A diagram and its sources cite each other —**

- **The diagram lists its sources —** the Sources field cites the home of everything the diagram draws, a box, an arrow, or a label on either, in the same file or another. Each is cited at that fact's single home (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`), at the most specific section or record whose own text states it: a child section rather than its parent where the child states it, and never a test scenario. A box naming a grouping draws the grouping, not its members, unless the diagram names them too. A summary restating a fact, an overview's included, is a materialized view of that home just as the diagram is, so it is not a source. A section stating something found nowhere else, as an overview's connecting prose can, is that fact's home, and is one. Together the citations are as specific as they can be without leaving out anything the diagram uses. This is so a reader can go deeper: nothing on the picture can carry a citation of its own, so the list is the way from it to the checkable detail, and the more specific each citation, the less a reader wades through to find what a box stands for. It is also so the diagram can be checked: an agent confirming that the picture represents its sources correctly reads exactly what it draws on, and nothing it does not.
- **Each source cites the diagram back —** every listed section cites the diagram's heading in its own text, not in a section nested inside it, in a sentence such as "`<the diagram's heading>` renders this." A record section, or a record, listed among a diagram's Sources cites it in the record section's `**Diagrams:**` field instead (`§ Constructs § Record Form`). This is so the diagram is kept in step: whoever edits a source is the reader who must re-check the diagram, and the citation in the source is what names the diagram to them.

A section may be listed only where it may cite the diagram's file and be cited by it, per `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, so a diagram draws a fact only from a section able to name it back: a technical diagram draws a product fact from the technical section stating how it is made true, never from the product file.

A diagram's own heading is an ordinary heading, citable like any other, per `specs/methodology/sourcing-and-citation.md § Writing a Citation`, and any file may cite it to point a reader at it. What it is never cited as is the source of a fact: a citation asserting something is true names the prose or construct the diagram renders, never the rendering.
