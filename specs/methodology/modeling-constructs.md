## Purpose

This file defines the bounded, approved set of structured modeling constructs, rather than free prose, for authoring specs in this repo. Prose can describe anything, since human language has no limit. But prose cannot be checked for what it leaves out. A paragraph can describe a process without ever mentioning what happens under some condition, and nothing in reading it flags the gap. A construct can be checked for exactly that: the definition of each construct an author uses lists what an instance of it is checked for. [`§ When to Use Which`](#when-to-use-which) chooses a construct wherever a rule needs one, and prose everywhere else.

**Between a language and prose.** Each construct gives structure to what prose would leave to grammar and spelling alone. It stands between a modern programming language, which a machine checks but a reader must learn, and prose, which anyone reads but nothing checks: a reader takes a construct in as a table or a record, and a script checks it as it would a program. A construct is chosen over prose as [`§ Defining Constructs`](#defining-constructs) draws the line between them. And a construct leans on the industry's standards. It adopts a notation an agent or an engineer already knows before the canon invents one, and says where it departs from that notation and why. Each departure is deliberate, and is judged again as the standards move, as [`specs/methodology/sourcing-and-citation.md § External Reference § A Mapping onto a Standard`](/specs/methodology/sourcing-and-citation.md#a-mapping-onto-a-standard) has a departure judged.

The set is bounded and approved. A new definition, whether a construct, an abstract base or an interface, earns its place only by filling a real gap that none of the existing definitions cover. A preference for a different notation does not earn it a place. Extending the set is a deliberate decision, made by updating this file first, never an ad hoc addition inside a single spec.

## Fields

A field is written the same way wherever it appears, in a spec, a working file or a construct. It is a line opening with its key in bold, the colon inside the bold, then a space and its value: `**{Field Label}:** {value}`, with each part in braces replaced. The line opens a paragraph, stands as a line of its own within one, or opens a list item whose marker is a hyphen. The hyphen and any indentation before the key are no part of the field. A lead-in closes on a period instead ([`specs/methodology/spec-style.md § Bold Lead-ins`](/specs/methodology/spec-style.md#bold-lead-ins)).

**Key.** A field's key is one that the form defining the field declares, so a reader or a script looks a field up by a name it already knows. An unknown key is an error, not a new field. A field appears only where the form declaring its key places it. A key means what its form defines. Two forms may declare the same key, as a design document and a follow-up each declare a Status, or a fact and a steering decision each declare a Type. Each such field is read by the form whose field it is. A field's key is a field label, as `Sign-off` or `Default Value` is, so it stays plain and matches exactly wherever it is written.

**Required, or its default value.** Each form declaring a field says whether the field is required: yes, no, or the condition under which it is. A form that declares other parts in the same table as its fields, such as sections, says the same of each of those parts. A field or part required under a condition is present where the condition holds and absent where it does not. One that is not required has a default value, which a reader and a script take in its place when it is absent, as a typed language reads a value or its default. A default value of `none` leaves the absence as it is. A field that is not required is written only where its value differs from its default value, so each thing has one way to be said. A form declaring its fields in a table gives a Required column and a Default Value column. The default value is empty where the field is required, under a condition too. A form declaring a field in prose says so in its prose. A missing required field or part is an error, as an unknown key is.

**Value.** A field's value runs from the key to the next line opening with a field's key, or to the end of the paragraph. Where the form defining the field says so, the value is a list instead. The key then stands on a line of its own, and the list sits directly beneath it. The list ends at the next line whose very first character opens a field's key, with no list marker or indentation before it, or at the end of its section. In a record ([`§ Constructs § Record Form`](#record-form)), a field whose value is a list is the record's last, and its list ends with the record: at the next record's first field, or at the end of the section.

## Defining Constructs

This section states how every construct's definition and its instances work, before any definition in [`§ Constructs`](#constructs) relies on it. A construct's section in [`§ Constructs`](#constructs) is its definition, and each use of the construct is an instance ([`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances)), as a class and its objects are. Every instance is held to the rules of its construct's definition, of each definition that one extends, and of each interface they implement.

A definition is written in the constructs themselves, as a self-hosted compiler's language states its own rules. So a definition may use an instance of any construct, including one defined after it, but never one resting on what it defines. A definition whose need the construct it defines would meet takes a more basic construct, as a self-hosted compiler writes its own core in a more basic syntax. A table defining the language the constructs' cells are written in, FEEL's values, operators and functions ([`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel)), is a Basic Table, never a construct whose cells that language writes.

The most basic form is the plain table: a table as GitHub Flavored Markdown writes one ([`specs/methodology/spec-style.md § Markdown`](/specs/methodology/spec-style.md#markdown)), rows of cells under a header, which every reader and agent already knows. A Basic Table is a plain table plus what the canon adds: a Table Name ([`§ Constructs § Tabular Construct`](#tabular-construct)), a Reference Key, Required columns and their checks ([`§ Constructs § Basic Table`](#basic-table)). A definition before that section, and that section itself, write plain tables that declare none of the additions. A table of fields among them takes the columns and the key that [`§ Constructs § Construct`](#construct) gives it. A table declaring an addition comes after that section. The audit checks each instance against its definition, as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) has a rule's checks made.

**A shape two definitions share.** A shape alone relates no definitions. Where definitions share what they are, a base they extend or an interface they implement states it once ([`§ Defining Constructs § Inheritance`](#inheritance), [`§ Defining Constructs § Interfaces and Members`](#interfaces-and-members)). Where they only represent a similar need the same way, each defines what its own need takes. It cites neither the other definition nor the first to use the shape.

**Form or prose.** The line between a construct and prose runs through a construct's own section, both the section defining it in [`§ Constructs`](#constructs) and a spec's section holding an instance. It falls between what the section's tables write and what the section's prose holds. A thing the prose could state is a column, a field or a form of the construct, with a check, where an outcome the spec states depends on it and the files alone could check what it says. An exclusive choice's Guard column is one: whether a move is taken decides where the entity goes. In an instance, such a thing is written nowhere where the instance's tables already give it, as the order of an Algorithm's steps is given by their numbers. Where no stated outcome depends on the thing, it is prose, as an Algorithm's work in words is, which decides nothing. Where a stated outcome depends on it but only a judgment can check what it says, it is prose too, and a reading audit asks it, as it asks what a state's work is. Where a stated outcome depends on it and whether the files could check it is arguable, the form is favored, since a rule without a check is a suggestion ([`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills)). How often a thing appears is no part of this test. A case written once in prose is one nothing checks, so the form is favored for it as for a case written many times. A form that costs a new construct or a notation is the deliberate decision extending the set, made by updating this file first.

**A definition's fields.** Each is a field ([`§ Fields`](#fields)) opening a paragraph of its own. They come in this table's order, followed by each member of an interface the definition sets. They stand directly after the prose opening the definition's section and before any lead-in or table, so a definition's fields always come first:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Modifier | no | none | "Abstract", "Interface" | what kind of definition it is, as [`§ Defining Constructs § Modifiers`](#modifiers) has each; none for a concrete definition, which its instances declare |
| Extends | where it is neither [`§ Constructs § Construct`](#construct) nor an interface, or is an interface extending interfaces | | text | the citation of the one definition it extends, its base; for an interface, a list of the interfaces it extends |
| Implements | no | none | text | a list, a citation of each interface it implements |

A Modifier, an Implements or a member Specified By Definition, the Locator among them, is reported where it stands outside a definition's section.

**Fields and lead-ins in a definition.** A definition's text uses a field wherever a form declares the key, and a lead-in everywhere else, as any text does ([`§ Fields`](#fields), [`specs/methodology/spec-style.md § Bold Lead-ins`](/specs/methodology/spec-style.md#bold-lead-ins)). The definition's own fields are those this section's table declares. A member it sets is a field that its interface's table of members declares. The fields its instances declare are written in each instance and never in the definition. They are its interfaces' members Specified By Instance, the members Specified By Definition Or Instance it leaves to its instances, and the fields of the definition's own table of fields. Every other bold label in a definition, introducing its fields, its columns, its checks or its naming, is a lead-in for a reader scanning it.

### Inheritance

**Extending.** A definition extends at most one base, as single inheritance has it. Every definition but [`§ Constructs § Construct`](#construct) itself and an interface extends [`§ Constructs § Construct`](#construct), directly or through its base. A definition holds everything its base holds and implements every interface its base implements. It states only what it adds. It may add fields, columns and rules, and bound what its base leaves open. It never loosens or redefines what its base states, and never declares again a field or a column its base declares. The ban on loosening is the same as Java's and C#'s overriding rules, which forbid weakening a contract. A level is earned by the change test of [`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances), however deep a chain runs. A base's section comes before the section of every definition extending it, so the canon reads top down and no definition extends itself. Using a construct needs no such order. An instance extending another instance of its construct does so by the instance's own `Extends` field ([`§ Constructs § Declared Construct`](#declared-construct)).

**Checks.** Each of these is reported:

- an Extends citing no definition, or one whose section comes after its own;
- a definition other than an interface citing more than one;
- a definition other than [`§ Constructs § Construct`](#construct) and an interface giving none;
- a field or a column a definition declares where a definition it extends declares it.

### Modifiers

A definition's Modifier field says what kind of definition it is, from a closed set. A definition giving none is concrete, and its instances are declared where they are used.

**Abstract.** A definition no instance declares. It is a base stating once what the definitions extending it share, as [`§ Constructs § Construct`](#construct) and [`§ Constructs § Tabular Construct`](#tabular-construct) are. How it may leave an interface's member to the definitions extending it is [`§ Defining Constructs § Interfaces and Members`](#interfaces-and-members)'.

**Interface.** A contract that definitions on different branches implement, never a base they extend. It states once a capability they share, and is never a mixin bringing its contents into a definition unseen. It is implemented as [`§ Defining Constructs § Interfaces and Members`](#interfaces-and-members) has it.

No definition is both abstract and an interface. A Construct field naming an abstract definition or an interface, and a Modifier neither `Abstract` nor `Interface`, are reported.

### Interfaces and Members

**Implementing an interface.** A definition implements as many interfaces as it needs, citing each in its Implements field. This is composition by reference ([`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances)). A definition also implements every interface its base implements. An interface extends one or more interfaces, its contracts carrying no structure to collide, and a definition implementing it implements those interfaces too. An interface's section comes after [`§ Constructs § Construct`](#construct) and before the section of every definition implementing it or extending it.

**Members.** What an interface asks of each definition implementing it. Each member is a field, given in the interface's table of members. That table is a table of fields ([`§ Constructs § Construct`](#construct)) with a `Specified By` column after `Field`, saying who sets the field. A row's Required, Default Value and Values say how the field is set, by whoever its Specified By names:

| Specified By | A Member |
|---|---|
| Definition | set by every concrete definition implementing the interface, in a field of its own, every instance alike, and declared by no instance; an abstract definition may leave it to the definitions extending it |
| Instance | declared by each instance as the interface's row has it, and set by no definition |
| Definition Or Instance | set by a definition, every instance alike, or left to each instance, declared as the interface's row has it; an instance never declares one its definition sets |

A definition leaving a member to its instances may narrow the member by a row of its own table of fields, as [`§ Constructs § Record Form`](#record-form) requires its Reference Key where a type extends no other. A definition never removes a member. A member that some of an interface's implementers cannot take is an interface of its own, which only the implementers taking it implement. A member a definition sets is never set again by its instance or by a definition extending it. A definition's own fields, those [`§ Defining Constructs`](#defining-constructs)' table declares, are never an interface's members. Declared Construct's Extends, which an instance declares, and a definition's own Extends share a key but are two fields, each read by the form declaring it ([`§ Fields`](#fields)).

**Checks.** Each of these is reported:

- an Implements citing what is no interface, or one whose section comes after its own;
- an interface whose section comes before [`§ Constructs § Construct`](#construct)'s, an interface extending what is no interface, and a definition extending an interface;
- a member Specified By Definition that a concrete definition implementing its interface leaves unset, and one Specified By Instance that a definition sets;
- a field a definition sets or narrows that is a member of no interface it implements, its bases' and the interfaces they extend among them;
- a member set where a definition it extends sets it;
- an instance declaring a member its definition sets.

### References and Names

**A reference to a definition.** A Construct field, and a definition's Extends or Implements field, is the citation of the definition it names ([`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation)). An instance's Extends cites the instance it extends ([`§ Constructs § Declared Construct`](#declared-construct)). The citation is locally qualified, as any citation is, its path left out only within the definition's own file: [`specs/methodology/modeling-constructs.md § Constructs § Decision Table`](/specs/methodology/modeling-constructs.md#decision-table) in any other file. Java and C# work the same way: a class or type reference is assumed local to its package or namespace when no qualifier says otherwise. A definition's citation, not its name, keeps it apart from every other definition, a construct an application defines among them. A Construct field that is no locally qualified citation of its construct's definition is reported. The exception is a bare name in the application specs, read as that citation until they are migrated.

**A definition's name.** A definition's name says what its instances are. For a definition others build on, it says what the definition adds to a construct, as `Tabular Construct` and `Keyed Construct` do. The name stands on its own wherever it is read, never a bare adjective or a participle, so a name is chosen for its reader. The reading audit judges it.

### Declaring a Construct

**Recognized by their shape.** Some forms are so basic that a reader and an agent know them on sight and need nothing to say what they are: a field, which is a bold key and its value ([`§ Fields`](#fields)), and a Basic Table, which is any table outside a declared construct's block ([`§ Constructs § Basic Table`](#basic-table)). Every other construct names itself. It implements [`§ Constructs § Declared Construct`](#declared-construct), and its instance opens with a `**Construct:**` field citing its definition.

**The block.** The `**Construct:**` field ([`§ Fields`](#fields)) opens a paragraph of its own before the construct's first table. The fields a construct sets for itself, such as a Decision Table's `**Hit Policy:**` or an Algorithm's `**Inputs:**` and `**Output:**`, follow it, each opening a paragraph of its own. The members its instances declare come first, in the order the tables of the interfaces it implements give them, taking the interfaces in its Implements' order. The fields of its own section's table come next, and a member its own table narrows takes its place there. The construct's tables follow its fields. The declaration, its fields and its tables make one block, which ends with the last table its form gives. Nothing else sits among them but a `**Table Name:**` opening one of its tables, directly before that table ([`§ Constructs § Tabular Construct`](#tabular-construct), [`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`](/specs/methodology/sourcing-and-citation.md#referring-to-other-text)).

**One construct to a section.** A section holds at most one declared construct of its own, not counting its subsections' constructs, so a citation of the section names the construct. Whatever prose the section needs sits between its heading and the `**Construct:**` field, or after the construct's last table, never inside its block. Another construct, such as a Constraint on an Algorithm's output, takes a section of its own. A construct's multiple tables, such as a State Machine's States and Transitions, are one construct. A Basic Table, such as a definition, an index or a catalog, may sit beside it, and a citation of a part names the one table its key's columns or its path reach ([`§ Constructs § Keyed Construct`](#keyed-construct)).

#### Fact

A fact that multiple constructs test, where it is one fact by [`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances), is declared once, as DMN's ItemDefinition is ([`specs/methodology/external-references.md § External References [Name: DMN]`](/specs/methodology/external-references.md#external-references)). A fact narrows the item definition to a value of one type FEEL names, a list, a context or a function among them. It adds the unit a number is counted in, the decimal places a value written to it is rounded to, and the FEEL function a derived value is given by. It adds the fact's value as its entity is created, whether the fact may be absent, and what the fact means.

A fact's name is words separated by single spaces. Each word opens with a letter and holds letters, digits and apostrophes, with a hyphen joining two runs of them. A boolean fact's name is a question instead: any words ending in a question mark. No fact's name opens with a word that FEEL keeps for itself ([`specs/methodology/expressions.md § Expressions § FEEL § Names`](/specs/methodology/expressions.md#names)). A fact's Values are values, never a fact's name. Its Initial Value is UML's default value, a Property's defaultValue evaluated when an instance is created, its section 9.5.3 ([`specs/methodology/external-references.md § External References [Name: UML]`](/specs/methodology/external-references.md#external-references)). A Decision Table names a fact it tests as [`§ Constructs § Decision Table`](#decision-table) sets. A file's facts sit in its record section of this type, a record type ([`§ Constructs § Record Form`](#record-form)), in the file whose subject owns them:

**Construct:** `§ Constructs § Record Form`

**Plural Name:** Facts

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the fact's name |
| Type | no | yes | | text | its type, as FEEL names it ([`specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions`](/specs/methodology/expressions.md#lists-contexts-and-functions)), `list<…>` and `context<…>` among them, and a function's, `function<{parameters}> -> {type}` |
| Values | no | no | none | text | the values it may take, as FEEL's unary tests, DMN's allowed values ([`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`](/specs/methodology/expressions.md#unary-tests)), where its type alone does not bound them; or, for a fact whose Type is `string`, the citation of the section holding a closed set, its record section or its Basic Table, its values the identifying values of its members, keyed by one field or one column ([`§ Constructs § Record Form`](#record-form), [`§ Constructs § Basic Table`](#basic-table)) |
| Unit | no | no | none | text | the unit a number is counted in |
| Decimal Places | no | no | none | text | the decimal places a number is held to, a whole number or the name of a fact its file declares, as a currency's minor units ([`specs/methodology/external-references.md § External References [Name: ISO 4217]`](/specs/methodology/external-references.md#external-references)), a value written to it rounded as [`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time) has it; on a function, the value it gives |
| Derivation | no | no | none | text | where its Type is a function's, the FEEL function giving its value, `function({parameters}) {expression}`, where the specs define it; none where a system computes it outside them, its Means saying what does ([`§ Constructs § Algorithm`](#algorithm)) |
| Initial Value | no | no | none | text | its value as its entity is created, a FEEL expression of its Type, judged with its file's facts in scope |
| May Be Absent | no | no | No | "Yes", "No" | whether it may have no value |
| Means | no | yes | | text | what the fact is |

**Worked examples.** Facts sections written whole, as a file would hold them, are in `specs/methodology/examples/construct/fact/`.

**Checks.** A Facts record is reported where:

- its name is no fact's name, opens with a word FEEL keeps, or, a boolean fact's, asks no question;
- its Values are empty, written plain, in no form of FEEL's unary tests, or name a fact, or cite no record section of a type identifying its records by one field, nor a Basic Table keyed by one column, or cite one on a fact whose Type is not `string`;
- its Type is no type FEEL names;
- its Decimal Places is neither a whole number nor a fact its file declares, or sits on a fact that is neither a number nor a function giving one;
- its Derivation sits on a fact that is no function, or is in no form of a FEEL function;
- its Initial Value is in no form FEEL has, or of another kind than its Type.

## Constructs

This section holds the definitions, each held to [`§ Defining Constructs`](#defining-constructs).

### Construct

The root that every other definition but an interface extends. It holds what every construct shares: an instance's fields, given by its definition, so every construct's fields are declared one way and checked alike.

**Modifier:** Abstract

**Fields.** An instance declares only the fields its definition gives ([`§ Fields`](#fields)), those of each interface it implements among them. A definition gives them in a table of fields, with a row to each field and each column headed by a field label. Each table of fields the definitions under [`§ Constructs`](#constructs) are written with takes this form too:

| Column | Holds |
|---|---|
| `Field` | the field's key |
| `Required` | whether it must be given, yes, no, or the condition under which it must, by an instance, by a definition for its own fields, or, in an interface's table of members, by whoever its Specified By names |
| `Default Value` | its default value, empty where it is required, as [`§ Fields`](#fields) has it |
| `Values` | the values it may hold, as Values has them |
| `Holds` | what is stated in it |

A table of fields is keyed by its `Field` column. Every cell holds a value but a required field's Default Value, which is left blank.

**Checks.** Each of these is reported:

- an instance declaring a field its definition does not give;
- a record type's table of fields holding a row of more or fewer cells than its header;
- a cell holding no value but a required field's Default Value;
- a Values cell in none of Values' forms.

**Values.** What a field may hold, in one of these forms:

- a list of its values, each in double quotes and separated by commas, which the audit checks every value against;
- a citation of the section that lists them, a closed set's record section or its keyed Basic Table among them, whose members' identifying values the audit checks every value against too;
- `text`, any value its Holds describes.

### Declared Construct

What a construct that names itself shares. Every construct names itself but the Basic Table, a form recognized by its shape ([`§ Defining Constructs § Declaring a Construct`](#declaring-a-construct)). Each instance opens with a `**Construct:**` field, so a reader and an audit know it as one wherever it sits. Each instance is described and named as this section has it.

**Modifier:** Interface

**Members.** The fields every instance declares:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Construct | Instance | yes | | text | the citation of its construct's definition ([`§ Defining Constructs § References and Names`](#references-and-names)), a concrete definition implementing this one |
| Extends | Instance | no | none | text | the citation of the construct of the same kind it extends, which it is a sub-definition of ([`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances)), holding everything its base holds and more: its tables hold what it adds, read as one construct with its base |

An Extends citing no construct, or one of another kind, is reported. So is a construct whose section opens with no description before its Construct field. A construct declaring Extends is checked for its fields and its tables' form. It is checked for nothing its section checks a whole construct for, since its tables hold a part of one.

**Description.** A construct's section opens with prose saying what the construct models, before its `**Construct:**` field. The prose is written for a reader meeting the construct for the first time, so the specs carry what documentation drawn from them tells the people using the system. A record type's description is the same prose, before its declaration.

**Name.** The heading of the section holding a construct is the construct's name, which its citations and its readers use. It names a thing, as `Payroll Run`, or asks the question the construct answers, never an activity, as `Running payroll`. A section titled for an activity gives its construct a subsection named for what the construct is, as [`§ Defining Constructs § Declaring a Construct`](#declaring-a-construct) gives its Fact. A section titled for a thing or a question, as [`§ When to Use Which`](#when-to-use-which) is, holds its construct itself. Not every construct is named: a form recognized by its shape, as a Basic Table is, names nothing. A definition's own guidance for naming its instances is optional. It is given only where the construct has guidance of its own, and otherwise the definition's instances are left to this rule. This rule guides the names of a construct's instances, so a definition no instance declares, an abstract definition or an interface, gives no such guidance. Its own name is guided by [`§ Defining Constructs § References and Names`](#references-and-names).

### Ordered Construct

What a construct shares whose result could depend on the order it takes its inputs or gives its results in: that order is stated, never left to one no one chose.

**Modifier:** Interface

**Members.** The order, as an instance declares it:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Order | Instance | where the construct leaves open the order it takes its inputs or gives its results in | | text | that order, or `any` where its result is the same in every order, so a result is never left to an order no one chose, unless a Constraint enforced by `nothing:` records that the system leaves it open ([`§ Constructs § Constraint`](#constraint)) |

### Configured Construct

What a construct shares whose rows, states or steps the system stores as data, as [`§ When to Use Which § A Configured Instance`](#a-configured-instance) has a configured instance. The facts holding that data are named, and the construct's written tables are an example of the data, so the data its users change is held to a shape the specs write and the audit checks.

**Modifier:** Interface

**Members.** Where the data is held, as an instance declares it:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Held In | Instance | no | none | text | where it is a configured instance ([`§ When to Use Which § A Configured Instance`](#a-configured-instance)), a list, an item for each table its form gives, in that order: the name of the fact the system holds that table's rows in, as data its users change, a colon and the citation of the Facts record declaring it, as a Decision Table's Reads item is written; the record's Type a list of a context whose entries are named as that table's columns, its Name column among them where it has one, so the data and the written table, an example of it, are held to one shape |

A Held In is reported where it names a fact nothing declares, or one whose Type is no list of a context, or a context whose entries are not the table's columns. A Held In giving an item for other than each table its form gives is reported too.

### Keyed Construct

What a construct shares whose instances' parts are cited: a part of an instance is selected by a citation naming its key's values ([`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation)), so any part of a keyed instance is cited, and its citation checked, the same way.

**Modifier:** Interface

**Members.** Its key, and how a key reaches a part:

| Field | Specified By | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Reference Key | Definition Or Instance | no | none | text | what selects one part: the names of its key's columns or fields, in order and separated by commas, one key, multiple naming one part together, as a tuple does; or, where its construct keeps its keys in more than one place, a list, an item to each place, the path to its key |
| Locator | Definition | yes | | text | where its instances keep their keys, and how a key or a path to it reaches one part, so an agent reading the definition knows how to reach a keyed target |

**Parts.** Each part's values under its key are its identifying values. They are required, every part giving each a value. They are unique, alone or together, among the parts of the table or the record section holding them, so a reader tells each part from the rest. An instance declaring its own Reference Key, a record type or a Basic Table, names its natural key where its parts have one: the field or fields, or the column or columns, naming each part as its readers know it. The natural key helps a reader understand the set and holds its author's parts to the intent. A citation by it is an added benefit.

**A part a citation names.** Its identifying values are short, kept stable for the part's life, and written on one line. They hold no `§`, `;` or `]`, since a citation names one part by them. A table whose cited natural key is too long is a record type's records, as [`§ When to Use Which § A Table's Construct`](#a-tables-construct) has it. A citation carries a value verbatim, markup and all, as [`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation) has it. A value no citation names is as long as it naturally is.

**Checks.** Each of these is reported:

- a part's key value left blank;
- two parts of one table or record section sharing their key's values;
- a value a citation names holding `§`, `;` or `]`;
- two or more tables in one section whose keys are declared by the same columns, unless all but one declare a distinct Table Name;
- a definition's Reference Key giving no path to a column of each place where its instances keep their keys in more than one;
- a citation written as no key its construct has, or matching no part.

**Key or a path to it.** A construct whose instances keep their keys in one place is cited by its key alone, `[Name: Session Timeout]`. One keeping them in more than one place, in multiple keyed tables or nested constructs, is cited by a path to the key, its levels joined by dots, `one.two.three.key`. The path is written in its Reference Key, an item to each place its keys are kept, in the order they come, and in every citation of one of its parts, `[Table.Key: value]`. The path is JSONPath's dot notation for a member's name ([`specs/methodology/external-references.md § External References [Name: JSONPath]`](/specs/methodology/external-references.md#external-references)), which it departs from as its mapping's rows have it ([`§ Constructs § Keyed Construct [JSONPath Elements.JSONPath: member-name-shorthand]`](#keyed-construct)). It names the path to the key and nothing more, as a column qualified by its table is written. Each level is a field label, the name its definition or its `**Table Name:**` gives the place, or the key, so the dots always part the levels.

The mapping from JSONPath's dot notation to a path:

**Table Name:** JSONPath Elements

**Reference Key:** JSONPath

**Required:** Section, Treatment

| JSONPath | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| member-name-shorthand | 2.5.1.1 | differs: each level a field label, its words parted by spaces, as `UML Elements.UML`, where JSONPath's shorthand takes a name holding no space, a name with spaces written in its bracket notation | the canon's form | a level is the name a reader knows a table or a key by, written as its section writes it, where brackets and quotes around each would bury the path |
| root identifier | 2.2.1 | not written: a path starts at the construct its citation's section holds, never at `$` | the canon's form | a citation's section already names the construct a path starts from, so a root would say it twice |

A citation names one table in its section. A declared construct keeping its keys in one place is cited by its key alone, and a Table Name it declares only labels its table for a reader. A Basic Table declaring no Table Name is cited by its key's columns. A Basic Table declaring one, or a table a definition names, is cited by the path its name and its key make, `[Terms.Term: …]`, as a State Machine's states are cited. Where two or more tables in one section have keys declared by the same columns, by a Reference Key or by a definition naming its tables, all but one declare a distinct Table Name ([`§ Constructs § Tabular Construct`](#tabular-construct)), or the tables stand in sections of their own. A table keyed by its form, a table of fields or a `Column | Holds` table ([`§ Constructs § Construct`](#construct), [`§ Constructs § Tabular Construct`](#tabular-construct)), has no row cited and takes no part in it.

#### Part Identifier

The form a part's citation takes: Keyed Construct's contract applied to a construct's parts.

**A part of a construct.** A part is named as [`§ Constructs § Keyed Construct`](#keyed-construct) has a part named. Its value under its construct's key is its identifier, so a reader and an audit can find the part and check it is there. A part is named so wherever it is named from outside its construct's section. Within the section, the construct's cells and the prose around it name the part by its value alone, as a jump names a step, so a part's identifier is always written as a value a citation names is. A citation names one part, and multiple parts take a citation each.

Where a construct's Reference Key names `Name` for a table, the table opens with a column headed `Name` exactly where a part of it is cited from outside its construct's section. The column comes with the first such citation and goes with the last. While the column is there, every row gives a Name.

### Tabular Construct

The tabular structure every construct extending it takes: a table of rows and columns, any number of each. A construct extending it may bound the columns, the rows or both. A table is the one representation that is precise, referable row by row, readable in plain text with no rendering step, and parseable without ambiguity. That is why a construct whose instances write rows extends this one.

**Modifier:** Abstract

**Extends:** `§ Constructs § Construct`

**A field-label column.** A column headed by a field label ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) is a field of each row, as a record's field is ([`§ Constructs § Record Form`](#record-form)). Its header names what every cell in it holds, and each cell holds the row's value of it.

**Columns.** A construct extending it gives the columns its tables take in a `Column | Holds` table. A sentence introduces that table, saying which of the columns are headed by field labels. The `Column | Holds` table gives a row to each column, its header in backticks. Where a table takes any number of columns of a kind, the `Column | Holds` table gives a row to that kind, named in words. The rows come in the order the table gives the columns. Each row says what the column's cells hold, and, for a column headed by no field label, what its header represents. A `Column | Holds` table is keyed by its `Column` column, and both its columns are required.

**Table Name.** A table may open with a `**Table Name:**` field naming it, so a reader sees what the table is and a citation reaches its part by the path its name and its key make ([`§ Constructs § Keyed Construct`](#keyed-construct)). The name is a field label unique among the tables of its section. The field is a paragraph of its own, before the table and before any other field opening it. A definition naming its tables, as a State Machine's does, has each instance name each table so. The field, in a table of fields:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Table Name | where its definition names its tables | | text | the table's name, a field label |

**What its tables hold.** An instance's tables hold every column its definition gives and no other. A column its definition gives as optional is written only where the definition says. A blank cell is empty, meaning nothing. It stands only where the definition lets a cell stand blank, as a Decision Table's annotation does, and a Basic Table's cell outside its key and its Required columns. Where a construct reads an empty value and acts on it, its definition names the token written for it, `none`, and that cell is never blank. A Decision Table's condition writes `-` where its row does not test it, a test meaning any value, and no token. In a column a construct's definition gives by name, `none` or `-` stands only where that definition names it. A cell of any other column holds the word as any other word.

**Checks.** Each of these is reported:

- an instance's table headed otherwise than its definition gives;
- a row of more or fewer cells than its header;
- a cell left blank where its definition lets none stand blank;
- `none` or `-` in a column a construct's definition gives by name, where that definition names neither;
- a Table Name that is no field label, or one another table of its section declares.

### Decision Table

A table deciding the outcome of a case, so every case a rule decides is written down and checked for a case that two rows decide or none does. Each row states the cases it matches in its condition columns, and the outcome they are given in its outcome columns. An outcome is decided whether anything acts on it now, later or never: a decision is apart from any action on it. A rule that is a lookup, a table there to decide by one condition ([`§ When to Use Which § A Table's Construct`](#a-tables-construct)), is authored as a Decision Table with a single condition column. A decision whose conditions are asked in an order is a Decision Table too, as A tree of questions has it.

It is DMN's DecisionTable, of the Object Management Group's Decision Model and Notation ([`specs/methodology/external-references.md § External References [Name: DMN]`](/specs/methodology/external-references.md#external-references)). Its cells, its computed headers and its computed outcomes are written in FEEL, DMN's expression language. FEEL is adopted whole as [`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel) states it, with its departure for a cell, a word written plain ([`specs/methodology/expressions.md § Expressions § FEEL [DMN Elements.DMN: string literal]`](/specs/methodology/expressions.md#feel)). DMN's InformationRequirement, chaining one Decision to another, is written as a table's Reads field. DMN's other parts, its Decision Requirements Diagrams, its decision services and its boxed expressions, are outside the set, and a project needing one adds it so. Its Business Knowledge Model is the form of the canon's own functions alone ([`specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions`](/specs/methodology/expressions.md#the-canons-functions)). That file and the hit policies this section gives are all an author needs, so an agent that cannot fetch DMN, or does not know it, loses nothing a Decision Table relies on.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Name

**Locator:** a row of its table, matched by its Name column, its keys kept in one place, so a citation writes its key alone, `[Name: …]`

**Fields.** After those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Hit Policy | no | Unique | [`§ Constructs § Decision Table`](#decision-table) | its hit policy, as this section's table of them names one |
| Reads | no | none | text | a list, an item for each fact or outcome it reads from elsewhere: its name, a colon, and the citation of the Facts record declaring it or of the construct deciding it |
| Conditions | yes | | text | its condition columns, named by their headers, separated by commas |
| Computed | no | none | text | its outcome columns whose cells are FEEL expressions, named by their headers, separated by commas |
| Annotations | no | none | text | its annotations, named by their headers, separated by commas |
| Input Values | no | none | text | a list, an item for each condition it gives values for: its header, a colon, and its values as FEEL's unary tests naming no fact ([`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`](/specs/methodology/expressions.md#unary-tests)), `null` among them where its fact may be absent; a question takes no item |
| Output Values | where its hit policy is Priority or Output order | | text | a list, an item for each outcome column it ranks by: its header, a colon, and its values as strings in double quotes separated by commas, highest priority first, the one writing of DMN's output values a ranking reads |
| Default Output | no | none | text | the outcome where no row matches: a value, or, with several outcome columns, a list, an item for each: its header, a colon and its value |

Its columns are of these kinds, with `Name` and each annotation headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the row's name ([`§ Constructs § Keyed Construct § Part Identifier`](#part-identifier)) |
| a condition | the tests its cells make of the value its header names, as Facts has it |
| an outcome | the outcome the row's cases are given, under its header's name |
| an annotation | what describes or illustrates the row |

**Columns.** Its condition columns come first, after a Name column where it has one ([`§ Constructs § Keyed Construct § Part Identifier`](#part-identifier)). No condition or outcome column is headed `Name`. Its outcome columns follow the conditions, one or more of each. Its annotations come after them. An annotation is a column that only describes or illustrates a row, which neither the match nor the check reads, and a cell of one is left empty where it has nothing to add. Its `**Conditions:**` field names its condition columns, a lookup's one among them, so which columns are conditions is declared, never inferred. A condition's header holds no comma, and no header that an Input Values or Output Values item names holds a colon, since those fields separate headers by them. An outcome cell outside a Computed column is never written as a test, `-`, `not(…)`, a comparison or a range, nor as a list, which would show a condition declared an outcome. Its `**Annotations:**` field names its annotations.

**Facts.** Each condition column tests one fact. Its header names the fact, as [`§ Defining Constructs § Declaring a Construct § Fact`](#fact) has a fact's name written. Where the column tests a value computed from facts, its header is that computation in FEEL instead, DMN's input expression (DMN 8.2.3). A header computes where it holds `+`, `*`, `/`, `<`, `>`, `=`, a bracket, a parenthesis, a minus between spaces, or a dot between two words, a path such as `installment.due date`. No other header computes, so a word such as `and`, `in` or `between` leaves a header a name. A computed header holds no comma, so its functions take one argument and it writes no list. A question, a header ending in a question mark, names a boolean fact whose values are `true` and `false`, however its words read. A fact its file's Facts section declares by its name ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)) is typed by that record. Its column's cells test values of its Type. Its Values, or a question's `true` and `false`, are the column's values, so the table's Input Values field gives it no item. `null` joins those values, and tests the fact, only where the fact may be absent. A fact or an outcome read from elsewhere is an item of the `**Reads:**` field, its name beside the citation of the Facts record declaring it or of the construct deciding it. A table so reads another's outcome as one of its facts, DMN's InformationRequirement (DMN 6.3.13). A fact so read is typed by its record, as a fact its file declares is, wherever the record sits. A cell, a computed header or a computed outcome names only a condition's fact, a fact its file's Facts section declares, or a Reads item. A cell ends only at a fact of its column's kind.

**Cells.** A row matches a case only when all its conditions hold. Each condition cell holds only what tests its condition, and what explains or illustrates the value goes in an annotation. A cell tests its condition by FEEL's unary tests ([`specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`](/specs/methodology/expressions.md#unary-tests)), which say what it means, or by a value written plain. The table's checks of overlap and coverage decide a table whose every cell is in one of the forms the checks read and ends at no fact. The reading audit reads any other table for overlap and coverage.

The forms the checks read are these:

- a value written plain, the whole cell, commas and all, the one form FEEL does not have, standing for the string FEEL writes in quotes; it is no number, never `true`, `false`, `null` or `-`, holds no `?`, never opens with `not(`, `<`, `>`, `=`, `!`, `@`, a bracket, a brace, a parenthesis, a double quote, `date(`, `date and time(`, `time(` or `duration(`, and never opens with `null`, `true` or `false` and a comma, so it is never taken for another form, and never read as a fact's name;
- strings in double quotes separated by commas, as `"Gold", "Silver"`, each a word however it reads, so `"2"` is no number;
- a number, a date, a date and time, a time or a duration, as [`specs/methodology/expressions.md § Expressions § FEEL § Its Values`](/specs/methodology/expressions.md#its-values) writes each, alone, compared, as `< 0.5`, or bounding a range, as `[0.5..0.8)`; an end of a comparison or of a range may be a fact's name, as `< pause end` or `[1..max term]`, and `=` stands before a fact's name, as `= base currency`, a value being tested as itself and never after `=`, an expression a cell tests equality with written after `=`, and a name never standing alone as a whole cell;
- `true` or `false`, testing a question;
- `null`, matching a fact that is absent; an absent fact meets `-` only where its column's values hold `null`, and meets every other form as [`specs/methodology/expressions.md § Expressions § FEEL § Null and Three-Valued Logic`](/specs/methodology/expressions.md#null-and-three-valued-logic) has an absent value tested;
- several of these separated by commas, opening with `null` or with what opens another of these forms but a number, so a cell opening with a word or a number is never read as several;
- `not(…)` around any of these;
- `-`, for a condition the row does not test.

A condition column's cells, and its Input Values, test values of one kind, `null` aside, so no comparison rests on how one kind is read as another. The kinds are words, numbers, dates, dates and times, times, and durations of one of their two kinds. In a table of two or more rows, no condition column holds one and the same cell in every row, except in a configured instance, whose columns are its data's ([`§ When to Use Which § A Configured Instance`](#a-configured-instance)). A column holding `-` in every row is no condition of the table. A column holding the same test in every row, where the table takes one row's outcome and gives no Default Output, is no condition of the table but of what runs it. It tells no case the table decides from another, so it is held where the construct running the table, or a table reading it by Reads, decides it. Where the table gives a Default Output, or takes every row a case matches, a case that test excludes takes the default, or no row, so the column decides.

An outcome decided when any one of several conditions holds is written as a row for each. Under Unique, the rows are written so no case matches two. For an outcome decided when condition A is a or condition B is b, one row tests A for `a`, with `-` for B, and another tests A by `not(a)` and B for `b`.

**Outcomes.** An outcome cell holds a value, what the case is sent to. It is never an action done, which is the canon's rule. Evaluating a table changes nothing: FEEL has no side effects, DMN 10.3, and a table's input expressions have none on one another, DMN 8.2.8. So what acts on the outcome is the construct running the table. It is like command-query separation: a query returns a value and changes nothing. What becomes of a request, turned away for a reason or taken, is such an outcome, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it. An outcome is written as a condition's cell writes one: a word, plain or quoted alike, a number, a date, a date and time, a time, a duration, `true`, `false` or `null`. A question's outcome is `true`, `false` or `null` alone. A column its `**Computed:**` field names holds in each cell a FEEL expression over the facts a cell may name, as `principal * rate` (DMN 8.2.10, 8.3.3). A FEEL expression, in a computed outcome or a computed header, is any expression FEEL writes ([`specs/methodology/expressions.md § Expressions § FEEL § Its Expressions`](/specs/methodology/expressions.md#its-expressions)). It names only those facts and the functions FEEL builds in, and a word in it is written in quotes. An outcome computed by a walk whose order changes it cites the Algorithm doing it. A table's outcome columns are decided by its conditions together. An outcome other conditions decide is a table of its own, and a part needing both tables cites both.

**Values.** An `**Input Values:**` field gives a condition's possible values for each condition it names, as DMN's input values do. A question takes no item, since Facts gives its values. A cell naming a value they do not hold, or matching none they hold, is outside them. Whether every case matches a row is decided, rather than read, where every condition gives its values, the table takes one row's outcome, and no cell tests against a fact. An `**Output Values:**` field gives, for each outcome column a Priority or an Output order table ranks by, its values as a list, highest priority first. It is written for no other hit policy. Where it names several columns, rows rank by the first, then by the next where they tie. A case matching no row takes the table's Default Output where it gives one, and `null` where it does not, under every hit policy (DMN 10.3.2.10). An optional `**Default Output:**` field gives that outcome. A table taking every row a case matches, under Rule order, Output order or a Collect, is not checked for a case no row matches, since `null` there means that no row applies. Under First, the outcome where no other row matches is a last row testing nothing, `-` in every condition, which a Name can cite. It is never a Default Output: the last row is the one of DMN's two writings the section keeps. A Default Output written `none` is the field absent, so an outcome meaning that a case is given nothing takes a word of its own.

**What is one.** A table there to decide an outcome from the criteria its earlier columns hold is a Decision Table, as [`§ When to Use Which § A Table's Construct`](#a-tables-construct) has a table's construct chosen. The exception is another construct's own table, such as a State Machine's transitions or an Algorithm's steps. A table there to define items, each row saying what its item is, decides nothing. By that section, it is a record type's records or a Basic Table.

**Hit policy.** Which of the rows a case matches give it its outcome. The hit policy is named in a `**Hit Policy:**` field as DMN names it, and its default value is DMN's default, as the table of fields gives it:

| Hit Policy | A Case |
|---|---|
| Unique | matches one row at most, since no two rows can match one case |
| Any | may match several rows, each giving the same outcome |
| Priority | takes the outcome of the row it matches whose outcome comes first in its Output Values |
| First | takes the outcome of the first row it matches, so the rows' order states which takes precedence |
| Rule order | takes the outcome of every row it matches, in the rows' order |
| Output order | takes the outcome of every row it matches, in its Output Values' order |
| Collect | takes the outcome of every row it matches, combining them, or, as `Collect sum`, `Collect count`, `Collect min` or `Collect max`, aggregating them, as DMN's C+, C#, C< and C> do |

A Unique table is like a switch whose cases never overlap, and a First table is like an if, else if chain, written in order of precedence so it is evaluated correctly.

Under Rule order, Output order or a Collect that does not aggregate, a table takes the outcome of every row a case matches. Such a table has its rows written so that, wherever one case matches two of them, both their outcomes can be carried out. An aggregating Collect has one outcome column, whose cells are numbers but for a count.

**A tree of questions.** A decision whose later conditions make sense only once an earlier one has been answered a certain way is a First table. The rows stand in the order the questions are asked, and a condition a row never asks is `-` in it (DMN 8.2.8). A condition that means one thing under one earlier answer and another thing under another is a column for each meaning. A path that is a decision of its own, asked elsewhere too, is a table of its own, read by Reads. It is the relational way: normalization splits a wide table into related tables, so what would repeat is stored once. For example, a support ticket is routed by its severity, then by whether a known fix matches it, then by its plan:

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

Whether a known fix matches is never asked of a critical ticket, and the plan is asked only of a ticket no fix matches, as the tree would ask them. Which fix matches is a decision of its own, and would be a table of its own, read by the Reads of a table testing it.

**Name.** A Decision Table is named for what it decides, `Intake Route`.

**Checks.** An instance is reported for:

- a cell in no form FEEL or its departure for a cell ([`specs/methodology/expressions.md § Expressions § FEEL [DMN Elements.DMN: string literal]`](/specs/methodology/expressions.md#feel)) has, a value tested after `=`, or a condition column testing values of more than one kind;
- an expression or a cell in no form FEEL has, naming what no fact, binding or function names, combining values of two kinds, reaching by a path a part a value does not hold, calling a function neither FEEL builds in nor the canon's functions hold, or giving one a number of arguments none of its signatures takes, a minus before what is neither a number nor a duration, a filter testing neither a yes or no nor a place, or an `@` value in no form;
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

The system checks a request, whether a command, an action asked for or a record saved, to decide whether it goes on and, where it does not, for what reason. Where [`§ When to Use Which`](#when-to-use-which) counts such a check a construct, it is a Decision Table over the request. Its outcomes are the reasons, and what becomes of the request otherwise. By that count, a check of one fact turning a request away or taking it is prose. The check is no Constraint, which states what holds ([`§ Constructs § Constraint`](#constraint)). A request turned away is an outcome the system chooses.

- **The first reason, or every one.** Under First, the rows stand in the order the system checks, and a reason's row and a row sending the request on are ranked by that order. The last row tests nothing and takes the request. Under Rule order, the rows are the reasons alone, and every reason that applies is given, in the rows' order. A request no row matches is taken, the table giving `null`. What becomes of a taken request otherwise, held or sent elsewhere, is chosen in its own right, once no reason applies.
- **Stage by stage, or item by item.** Reasons given a stage at a time are an Algorithm that runs each stage's table in turn and ends at the first stage that gives one. Reasons given for each item of a list are an Algorithm whose loop runs the table on each item.
- **What runs it.** An Algorithm's step runs the table, and the Algorithm ends where the request is turned away, its Output giving the outcome. A State Machine's transitions, or a DAG's tasks, are guarded by the outcome the table gives. The table runs before any write it guards. A request turned away completes its run, which is no failure, so nothing the run wrote is undone ([`§ Constructs § Constraint`](#constraint), its paragraph When it holds).
- **What it keeps.** A rule holding of what the system stores, which no taken request can break, is a Constraint `always`. It is Enforced By the rows turning away the requests that would break it, each row cited by its Name. A precondition, a rule `before` the operation, is what the operation relies on. It is Enforced By the parts of what runs the operation that make it hold. The check this section writes is never a precondition.
- **An action a state does not allow.** A protocol machine refuses such an action by its structure. The reasons it distinguishes are this table over the request ([`§ Constructs § State Machine § What It Means`](#what-it-means-1)).

### DAG

A table of distinct tasks in an acyclic process. Each task gives the construct doing its work, the tasks it waits for, and, where it has them, its guard, its timeout and whether its failure is tolerated. Every task is considered on every run, and the tasks nothing orders run at once. Written so, what each task waits for, and what may run at once, is explicit and checked rather than implied. A DAG is UML's Activity ([`specs/methodology/external-references.md § External References [Name: UML]`](/specs/methodology/external-references.md#external-references)), adopted whole and written as a table of tasks forked and joined. It has no tie to any engine, so it maps onto the DAG an orchestrator such as Airflow, Dagster or Argo Workflows defines. [`§ Constructs § DAG § What It Means`](#what-it-means) states what UML means for what its table writes, and names each departure the canon makes.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Task

**Locator:** a task, a row of its table matched by its Task column, its keys kept in one place, so a citation writes its key alone, `[Task: …]`

**Fields.** After those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Runs When | yes | | text | what runs it: the citation of each construct running it, a State Machine whose state's description cites it as the state's work, or a DAG whose task's work cites it; or the occurrence it answers, written as a State Machine's trigger is written ([`§ Constructs § State Machine § What It Means`](#what-it-means-1)), a request, a file arriving or a job's run among them, a job's run saying what a missed and a late run do ([`§ Time`](#time)) |

It is authored as a table whose columns are each headed by a field label:

| Column | Holds |
|---|---|
| `Task` | the task's name |
| `Work` | the construct doing the task's work, or `none` |
| `Depends On` | the tasks it waits for, or `none` |
| `Guard` | what must hold on a run for the task to run, or `none` |
| `Timeout` | how long the task may run, or `none` |
| `Tolerated` | `Yes` where the run goes on past the task's failure, or `No` |

After `Depends On` come, in this order, the `Guard` column, written where any of its tasks has a guard, the `Timeout` column, where any has a timeout, and the `Tolerated` column, where any task's failure is tolerated. A column whose every cell would be `none` or `No` is not written.

**Tasks.** A task's name is plain text that holds no comma, is not the word `and`, and does not end in the word `ended`, so a dependency list reads whole. A task's work is `{citation}`, citing the Algorithm, the Decision Table or the DAG doing it, as the worked example's check margins cites its Algorithm. The cited construct runs once the task runs. An Algorithm reads its Inputs from the facts the file declares, among them what an earlier task gave, and gives its Output. A Decision Table reads its conditions' facts the same way and gives each outcome column's value as the fact of that column's name, its outcome columns headed by facts the file declares. A DAG is run whole as the task. It reads what its tasks read, by work or guard, less what they give, and gives what they give. No DAG holds itself through the tasks it cites.

Otherwise a task's work is `none`, where the work is done outside the specs: a person's task or an external system's, a file arriving or another system's job ending among them. Where such work leaves facts the tasks after it read, it is written `none, leaving {fact}, {fact}`, as `none, leaving margins`, each a fact the file declares. The prose after the table says whose the work is and when it counts as done. A DAG's work is this citation or `none`, never an Algorithm's work in words, a step's ([`§ Constructs § Algorithm`](#algorithm)). The occurrence that starts a run is the DAG's Runs When, never a task. A task whose work is `none` waits only within a run, after what it depends on.

A task's dependencies are `none`, or a list, `{task}, {task}`, as `extract prices, extract costs`. Each item is a task it waits for to be done, or `{task} ended`, as `load ended`, a task it waits for to have ended however it did, as a task that reports or cleans up does. A `{task} ended` item is written only of a task that can end other than done. No task depends on itself, directly or through the tasks it depends on. A task's guard is `{condition}`, a FEEL boolean over the facts its file declares ([`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel)), as `some m in margins satisfies m.flagged?`. The guard is read as the task would run, and reads facts as the task's work does. A task's timeout is `@"{duration}"`, a FEEL duration, as `@"PT30M"`, or a fact of that type the file declares. A task's tolerated is `Yes`, written only of a task that can fail, or `No`. A dependency the logic needs is a row's Depends On, never an order written in prose. A construct a DAG would run twice with different inputs is an Algorithm whose steps run it with its bindings, and the task cites that Algorithm, since a task's work reads and gives facts by name alone.

**Run.** A run of a DAG considers every task. A task runs once each task it depends on is done or skipped, or has ended where it waits for that, and once its guard, where it has one, holds. The tasks free at once run at once. A task whose guard does not hold is skipped. A task is unreached where a task it waits for to be done failed or was unreached. A task whose timeout passes before it is done fails. Its work is ended, and what it wrote is undone as a failed operation's writes are. A nested DAG's run fails with it.

A task fails where the run of the construct its work cites fails, as an operation does ([`§ Constructs § Constraint`](#constraint)), or where its timeout passes. An Algorithm's or a DAG's run can fail, and a Decision Table's never does. Work that is `none` ends done, or fails by its timeout alone, and what goes wrong outside the specs is a fact it leaves. So a task can fail where its work is an Algorithm or a DAG, or where it has a timeout. A task can be unreached where a task it waits for to be done can fail or be unreached. A guard alone only skips, and a dependency `ended` never leaves its waiter unreached. A task can end other than done where it can fail, be skipped or be unreached.

A task ends done, skipped, failed or unreached, and `{task} ended` waits for any of these. A task that is not done gives nothing. The facts its work would give, or its `none` would leave, hold what they held before it, or no value where nothing had set them. A failed task whose tolerated is `No` fails the run. A failed task whose tolerated is `Yes` ends failed, with its own writes undone, and the run goes on. What waited for it to be done is unreached, and what waited for it `ended` runs. The run ends once no task is running and none can run, and fails where a task failed whose tolerated is `No`. A run that fails is all or none, as [`§ Constructs § Constraint`](#constraint) has an operation. The exception is what a task wrote that reaches a failed task through a dependency `ended`, which is kept, as a report or a clean-up is. What a nested DAG's run keeps so, it keeps, and its parent task's failure undoes the rest of what that run wrote.

Facts pass between tasks by name. A task's work, and its guard, read what the file declares and what the tasks it reaches through its dependencies gave. They never read a fact a task after it gives, unless that task reads the fact too and so rewrites it. The facts the occurrence gives a run, its date or the request among them, are facts the file declares, set as the run begins. A fact a task reads that some task it reaches gives is declared May Be Absent ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)), unless one such task gives it surely. A giver is sure where it is not guarded, is not reached through a dependency `ended`, and, within a nested DAG, is neither tolerated nor waiting to be done, directly or through others, for a task that is, since there the nested run completes past the failure and its parent task ends done. An Output the work's Inputs also name is given surely by any task, a nested DAG's tasks' works' among them, the fact holding its earlier value where the task is not done. A tolerated task in the reader's own DAG gives surely to what waits for it to be done, which is unreached where the task fails and never reads. Two tasks free at once, neither reaching the other through its dependencies, give no fact in common. Neither reads, by its work or its guard, a fact the other gives, since an order the run leaves open would decide the fact's value. A result an order among free tasks changes states that order ([`§ Constructs § Ordered Construct`](#ordered-construct)).

**What the table does not write.** A task waiting for whichever of several tasks ends first is a State Machine's transition on the first occurrence ([`§ Constructs § State Machine`](#state-machine)), never a dependency. A task's retries, a pool or a priority among tasks are operations, stated in the prose after the table or held by a Constraint, never a row. A flow over an unbounded stream, windowed or joined as it runs, is not written, as [`§ Constructs § Algorithm`](#algorithm) has a stream. A pipeline run once per event is a DAG whose Runs When is the event.

**What is no DAG.** A process that waits within a task's work on anything but that task's completion is a State Machine, whose trigger is the wait. A process that repeats a step on a condition or branches into different downstream handling, with no wait, is a State Machine or an Algorithm, as [`§ When to Use Which`](#when-to-use-which) chooses. The same work once per item of a list is an Algorithm's loop `at once` ([`§ Constructs § Algorithm`](#algorithm)), gathering what each pass gives. Where a DAG holds such work, a task's work is that Algorithm. A process whose tasks or their order are configured as data is an Algorithm over the configuration, its loop taking each configured task in turn. A configuration shipped with the system is an instance, data, never a DAG.

**Worked examples.** DAGs written whole, as a file would hold them, are in `specs/methodology/examples/construct/dag/`.

**Name.** A DAG is named for its process as a thing, `Nightly Pricing`, never for an activity, `Extract Prices`.

**Checks.** A DAG's names, dependencies, cycles, guards, timeouts and tolerated cells are checked in its file. Its works, what its tasks give and read, and what runs it are checked across files, with its citations resolved. The check across files also confirms that an Algorithm a task's work cites has that DAG among what runs it, which the Algorithm's Runs When names ([`§ Constructs § Algorithm`](#algorithm)). Whether each task's work is the whole of it, whether the prose says whose a task whose work is `none` is and when it is done, and whether what runs the DAG is run on it are read.

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

A DAG means what UML's Activity means for what the DAG's table writes, element by element as this section's UML Elements table gives it, so neither an author nor a reader needs to recall the standard.

**A run.** Each run of the DAG is an execution, and the Runs When names what runs it ([`§ Constructs § DAG`](#dag), its Runs When field). Facts pass between tasks, read and written by name.

**A task.** A task whose work cites an Algorithm, a Decision Table or a DAG calls that construct. A task whose work is `none` is described in the prose after the table, which says whose the task is and when it counts as done, for a person's task and an external system's alike. What the task leaves is written in its cell as its output. A task's work is cited by name and read from the file's facts.

**A dependency, and tasks at once.** A dependency runs from the task waited for to the task waiting. The tasks nothing orders are reached at once, and a task may wait for several of them. A task waits for every task it depends on, and every task depending on it may start once it ends.

**A guard, and a timeout.** A task's guard is tested as the task becomes ready to start, once every task it waits for has ended as it waits. Where the guard fails, the task is skipped. A skipped task counts as done for what depends on it. Where every task is guarded and no guard holds, nothing runs and the run ends. A task's timeout ends the task's work when the time passes. The task then fails, its writes undone, and a person's or an external system's work no longer counts.

**An end, and a failure.** The run ends once no task is running and none can run. A task that fails, untolerated, fails the run, and the run goes on to what waits `ended`, keeping what such a task writes. Where a task whose tolerated is `Yes` fails, what waited for it to be done is left unreached, and only what waited `ended` runs. A run is all or none, what it wrote undone where it fails, as [`§ Constructs § Constraint § What It Means`](#what-it-means-3) has it for an operation.

The mapping from UML's Activity to the DAG:

**Table Name:** UML Elements

**Reference Key:** UML

**Required:** Section, Treatment

| UML | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| Activity | 15.2.3.1 | differs: the DAG, each run an execution, all or none, what it wrote undone where it fails, as [`§ Constructs § Constraint § What It Means`](#what-it-means-3) has it for an operation | the standard's gap | a Constraint over what a run writes relies on the run being all or none, and UML leaves what a failed execution wrote in place |
| Variable | 15.2.3.5 | the same: a fact passed between tasks, read and written by name | | |
| CallBehaviorAction | 16.3.3.1 | differs: a task whose work cites an Algorithm, a Decision Table or a DAG, calling that construct; a Decision Table is taken as the Behavior it calls, and a task's work is cited by name and read from the file's facts rather than wired by pins, the departures [`§ Constructs § Algorithm § What It Means`](#what-it-means-2) names for a run | the canon's form | a table has no pins to wire, and a fact named once in a Facts section is what a check follows across files |
| OpaqueAction | 16.2.3.2 | the same: a task whose work is `none`, its body the prose after the table | | |
| ControlFlow | 15.2.3.3 | the same: a dependency, from the task waited for to the task waiting | | |
| ForkNode | 15.3.3.3 | the same: the table stands for the forks and joins UML draws; the tasks nothing orders are reached through one, every task's outgoing flows forked; UML's own note on it has a token shunted to the downstream JoinNode where a guard on an edge from it fails | | |
| JoinNode | 15.3.3.4 | the same: a task waiting for several tasks, every task's incoming flows joined; where every task is guarded and no guard holds, it receives every shunted token | | |
| guard | 15.2.3.3 | the same: a task's guard, on the ActivityEdge offering the task its token from the fork or the join before it | | |
| DecisionNode | 15.3.3.6 | the same: placed after the fork or the join before a guarded task, so that where the guard fails the token is shunted to the downstream join node, a skipped task counting as done for what depends on it | | |
| wait time action | 16.10.3.1 | the same: a task's timeout | | |
| TimeEvent | 13.3.3.4 | the same: the timeout's trigger | | |
| InterruptibleActivityRegion | 15.6.3.2 | differs: holding the task, with the TimeEvent on an interrupting edge, it ends the task's work when the time passes, and the task then fails, its writes undone, and a person's or an external system's work no longer counts; [`§ Constructs § Algorithm § What It Means`](#what-it-means-2) has it among what the Algorithm's table does not write, and the DAG's table writes it by its Timeout column | the standard's gap, the canon's form | a timeout bounds one task, so the task's row writes it, where a region is drawn around the task; and undoing the task's writes keeps the run all or none |
| activity execution completing | 15.2.3.6 | the same: the run ends once no task is running and none can run | | |
| exception | 16.3.3.1, 15.5.3.2 | differs: the run goes on past an untolerated failure to what waits `ended`, keeping what such a task writes, where in UML an exception a failing task raises, uncaught, ends the run | the canon's form | a run that fails must still be able to report or clean up, and `ended` writes that wait as a dependency a check reads, where UML would need a handler around every task |
| ExceptionHandler | 15.5.3.2 | differs: a task whose tolerated is `Yes`, its tolerated cell standing for the handler, leaves unreached what waited for it to be done and runs only what waited `ended`, where UML, once the handler's body completes, offers tokens to everything downstream as though the task had completed | the standard's gap | a tolerated failure is no success, and running what waited for the task to be done would let a task act on work that never happened |

### State Machine

A model of the states a system or an entity can be in, the transitions between them, and the conditions under which each transition is taken. It answers where the entity is in its journey, and what happens when something happens in a given state, so a reviewer can check that every case is covered. It is UML's StateMachine ([`specs/methodology/external-references.md § External References [Name: UML]`](/specs/methodology/external-references.md#external-references)), adopted whole and written as tables, with no tie to any serialization or execution engine. [`§ Constructs § State Machine § What It Means`](#what-it-means-1) states what UML means for what the tables write, and names each departure the canon makes from UML. A machine whose every transition is taken on its trigger alone, an entity's plain life cycle, is a State Machine that leaves its optional parts unused. It is no construct of its own ([`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances)).

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:**
- States.State
- Transitions.Name

**Locator:** a state, a row of its States table matched by its State column, or a transition, a row of its Transitions table matched by its Name column, its keys kept in more than one place, so a citation writes the path to its key, `[States.State: …]` or `[Transitions.Name: …]`

**Fields.** After those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Protocol | no | No | "Yes", "No" | whether it says which actions an actor may take in each state, UML's ProtocolStateMachine, rather than what the entity does, a behavior StateMachine |
| Recorded In | no | none | text | the fact the entity records its state in, its name, a colon and the citation of the Facts record declaring it, as a Decision Table's Reads item is written, each state's name one of that record's Values |

A State Machine is authored as a States table and a Transitions table, and, where a trigger names a class of occurrences, a Trigger Classes table after them, in the machine's section before any subsection of it. Each table opens with its `**Table Name:**`, `States`, `Transitions` and `Trigger Classes` ([`§ Constructs § Tabular Construct`](#tabular-construct)). A reader then sees each table's name, and a citation reaches a part of its States or its Transitions table by the path the table's name and its key make.

A States table's columns are each headed by a field label:

| Column | Holds |
|---|---|
| `State` | the name of the state, holding no comma and not the word `and`, since a From and a To list states by those |
| `Description` | what it means for an entity to be in this state |
| `Initial` | whether the entity starts in this state, Yes or No |
| `Terminal` | whether this state ends the machine's run, Yes or No |

A state may be drawn from a closed set, its machine recording its state in a fact whose Values cite the set's section ([`§ Constructs § Record Form`](#record-form)). Such a state's description opens with the citation of the state's own member, its record or its row, and of no other, for what holding the state means. The description then states any work the state does in this machine. A set that several workflows draw on so keeps its meaning in one home, and each workflow keeps its own work.

A Transitions table's columns are each headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the transition's name ([`§ Constructs § Keyed Construct § Part Identifier`](#part-identifier)) |
| `From` | the state or states the entity leaves |
| `To` | the state or states the entity enters |
| `Trigger` | what happens to move the entity on, of a kind [`§ Constructs § State Machine § What It Means`](#what-it-means-1) names, written in that kind's form, or `none` |
| `Guard` | what must hold when the trigger happens for the transition to be taken, or `none` |
| `Effect` | the citation of the Algorithm or the Decision Table the transition runs, or `none` |

A Trigger Classes table's columns are each headed by a field label:

| Column | Holds |
|---|---|
| `Member` | an occurrence of the class, written as a trigger is, or the citation of another machine's section whose Trigger Classes table holds the class |
| `Class` | the class's name, as the Transitions table writes it as a trigger |

After `Trigger` come the `Guard` column and the `Effect` column, in that order. The `Guard` column is written where any of the table's transitions has a guard, and the `Effect` column where any runs an effect. A column every cell of which would be `none` is not written.

A guard testing a fact for a word, by `=`, `!=` or `in` a list or tests, wherever the test stands in the guard, tests one of the fact's Values, as a Decision Table's cell does. The fact, as any fact a guard or a trigger names, is the one its machine's own file declares, or else the one other files declare alike. A name that other files declare with differing Values or Types is read, not checked.

A trigger names only what happens. Whatever must hold when it happens for the move to be taken is a guard, never a qualifier written into the trigger. A trigger is written in its kind's form, as [`§ Constructs § State Machine § What It Means`](#what-it-means-1) gives each kind. A trigger in words is written in the same words wherever it recurs, since two such triggers are the same only where their words are, and it never opens with `after`, `at` or `when` and a space, the openings of a trigger written in FEEL. Two triggers written in FEEL are the same where their expressions' tokens are, the spaces between them aside. Each name a trigger written in FEEL holds is a fact a Facts section declares, found as a guard's fact is. Each distinct thing that can happen is a trigger of its own: each action an actor may take, and each outcome of an event from outside the entity. So each takes a row of its own, and no row lists triggers. A class of occurrences is one trigger, written where UML lists a Transition's several triggers ([`§ Constructs § State Machine § What It Means [UML Elements.UML: Transition's triggers]`](#what-it-means-1)). Its name is the trigger, and each of its members is a row of the machine's Trigger Classes table. A member may instead be the citation of another machine's section whose Trigger Classes table holds the class, standing for every member that table gives it, so a class two machines take keeps its members in one home. A state taking a class's trigger takes none of its members as a trigger of its own. A From names one state, or, for a join, joins several with `and`, so transitions from several states to one on the same trigger take a row for each From. A transition may lead back to an earlier state, as a reopened item does. A state's own work being done is not a trigger, and a transition taken on it carries none. A state whose description gives it nothing to wait for cannot stay once its work is done.

What a State Machine expresses beyond a move its trigger alone decides:

- a guard, which lets a transition's trigger happen, or its From state's work be done, without the transition being taken;
- an exclusive choice: two or more transitions from one state on the same trigger, on none, or on conditions one occurrence makes true together, whose guards never both hold. This departs from UML, which would take either ([`§ Constructs § State Machine § What It Means [UML Elements.UML: conflicting transitions]`](#what-it-means-1)). Each of their guards is a FEEL boolean expression, UML's guard written in FEEL ([`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel)), as `receipt = "attached"` or `paid on < due date and amount >= minimum`, with a word in it quoted. A guard of none tests no fact. A boolean fact a guard tests is a question, as `fully paid?` or `not(fully paid?)`. A fact that another is compared with is one a guard of the choice tests or a Facts section declares, of the same kind as the fact compared with it. A fact a guard tests holds no word FEEL keeps in its name ([`specs/methodology/expressions.md § Expressions § FEEL § Names`](/specs/methodology/expressions.md#names)), so FEEL never reads a word of the name as one of its own. Where each guard is a conjunction, joined by `and`, of tests of one fact each, with each fact tested once, the guards read together are a Unique Decision Table over those facts. A test here is a comparison with a value or another fact, `in`, `between`, or a question alone or within `not(…)`. Each test is its fact's cell, and a fact a guard does not test is `-`. Where the state's work is done and the state cannot stay, together the guards also cover every case. A choice with any other guard is read for both. A guard on a transition alone on its trigger, or alone with none, is prose. Once another transition joins it, both guards take this form;
- an effect, an Algorithm or a Decision Table a transition runs as it is taken;
- a fork, a transition into several states that then run concurrently, written as one row whose To joins them with `and`;
- a join, a transition from several states running concurrently, written as one row whose From joins them with `and`, taken once every one of them has done its work.

Every fork is closed by one join, from states its branches reach, and a join closes one fork.

**Worked examples.** State Machines written whole, as a file would hold them, are in `specs/methodology/examples/construct/state-machine/`.

**Name.** A State Machine is named for the entity it follows, `Work Order`.

**Checks.** An instance is reported for:

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
- a protocol machine with an Effect column, a transition with no trigger, one taken on time or a condition, or a governed state;
- a trigger opening with `after`, `at` or `when` and a space, its expression in no form FEEL has, naming a name no fact in scope declares, reading the wall clock by `today()` or `now()`, or giving `after` no duration, `at` no date or date and time, or `when` no yes or no;
- a Trigger Classes table, or a table headed Member and Class with no Table Name, outside a machine's section before its first subsection, a second in one, or not opening with its Table Name, not headed Member and Class, or holding a row that is not a member and its class each written; a member written twice; a member citing no machine whose Trigger Classes table holds its class; a class no transition's trigger names; or a state taking a class's trigger and a member's too;
- of a submachine state, a state governed by more than one machine, a machine governing itself, a governed state that is terminal or not left as its machine's exits have it, the words `governed by` naming no machine or a part of one, or naming none, and a description citing a machine's whole section without them.

#### What It Means

A State Machine means what UML's StateMachine means for what the machine's tables write, element by element as this section's UML Elements table gives it, so neither an author nor a reader needs to recall the standard.

**One occurrence at a time.** The machine handles each thing that happens fully before it takes the next, taking the transitions the occurrence enables until it reaches states where it waits. An occurrence that enables no transition is discarded, except in a protocol machine. A state's work being done is handled ahead of anything else waiting. Conditions one occurrence makes true together are taken in the occurrence's one step, and the transitions they enable from one state are an exclusive choice. Within one occurrence's step, a transition the step has taken is not taken again on a condition already true, an instant already past or an amount of zero or less; it waits for a change.

**A state and its initial state.** The initial state is the one the machine enters as its run begins. Before its run begins and once the run has ended, a machine is in no state. What must outlast a run is a fact the entity records: its status, named by the entity, as `loan status`, and declared in a Facts section ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)). The fact's Values are the values it may take, either listed or given as the citation of the section holding a closed set, its record section or its keyed Basic Table, their one home. The machine names that fact in its Recorded In field. The machine's states are those of the values it uses, a terminal state's among them, and a value it does not use is left out.

**A state's work.** A state's work is what its description says goes on in it, begun when the state is entered. Once done, the work lets a transition with no trigger be taken. For a state whose description states no work, that transition may be taken at once, and for a submachine state, once the run of the machine governing it ends. A transition taken while the work runs cuts it short. A transition from a state to itself leaves the state and enters it again, and the state's work, the run of the machine governing it and its relative times then start afresh.

**A terminal state.** Entering a terminal state completes the machine's run. It has no work: what its description says is the run's outcome, and work that ends a run is the effect of the transition entering it.

**A fact.** A fact is held by the entity, or by another. It is set by a state's work, a transition's effect or an occurrence's data, or from outside the machine, as a payment received lowers a balance. It is declared in a Facts section where a guard compares a fact with it.

**A trigger.** A trigger names what happens. What moves the entity decides the trigger's kind:

**Construct:** `§ Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** What moves the entity, Counted on

| What moves the entity | Counted on | Its trigger |
|---|---|---|
| "the state's own work being done, whatever it found" | - | none: a transition with no trigger, guarded by what the work found where that decides where it goes |
| "a periodic job's run, detecting a time or a condition" | - | something done: the job's run, as [`§ Time`](#time) has it |
| "time, counted from entering the state the transition leaves" | "the wall clock, every day alike" | time passing, relative, `after` its amount |
| "time, counted from entering the state the transition leaves" | "the wall clock, in business days" | time passing, an absolute instant computed from a fact recording when the state was entered, `at` it, as [`§ Time`](#time) has it |
| "time, counted from anything else" | "the wall clock, every day alike", "the wall clock, in business days" | time passing, an absolute instant computed from a fact, `at` it |
| "time, counted from entering the state the transition leaves", "time, counted from anything else" | "another clock" | a condition becoming true on that clock's fact, `when {clock} >= {instant}`, its instant computed from a fact recording when the time began, as [`§ Time`](#time) has it |
| "a fact reaching a value, whatever changed it" | - | a condition becoming true, `when` it |
| "a part of another construct being reached, or another machine's state being entered" | - | that part reached, or that state entered |
| "an action of an actor, or a message from another system, by its happening" | - | something done |

- **Something done.** An action of an actor, a message from another system, or a periodic job's run, as a user approving or a payment arriving. What it carries, as a payment's amount, is a fact its occurrence sets. That fact is declared in a Facts section, and the transition's guard may test it. A delayed message whose time is fixed when it is sent is something done, written as the message.
- **A part reached, or a state entered.** Another construct's part completing, or another machine's state being entered. It is written as the part's citation and `is reached` or `is entered`, in the same words wherever it recurs. Two machines may each be triggered by the other's. Another machine's state is cited. A state of another instance of the same machine is named by its identifier, as a part within its own section is. Either is followed by its instance after `of` where the instance matters, as `active of another sale of its loan is entered`.
- **A condition becoming true.** Written `when {condition}`, a FEEL boolean expression over the facts, as `when balance <= 0`, UML's notation for a ChangeEvent with its expression in FEEL (UML 13.3.4). Taken the moment the condition goes from false to true, never while it stays true, as a balance reaching zero. A condition that is `null` is not true, so one going from `null` to `true` becomes true. A condition already true as its state is entered is taken at once, which departs from UML ([`§ Constructs § State Machine § What It Means [UML Elements.UML: ChangeEvent]`](#what-it-means-1)), as One occurrence at a time bounds it. A condition ceasing, going from true to false or to `null`, is written `when not(({condition}) = true)`. [`§ Time`](#time) says what clock a condition reads.
- **Time passing.** Either relative, written `after {duration}`, a FEEL duration, as `after @"P30D"` or `after hold limit`, or an absolute instant, written `at {instant}`, a FEEL date or date and time, as `at due date + @"P30D"`, UML's notation for a TimeEvent with its expression in FEEL (UML 13.3.4). Relative time is counted from entering the state the transition leaves, even where the machine waited elsewhere first; an amount of zero or less is taken at once, as One occurrence at a time bounds it, and one that is `null` never. [`§ Time`](#time) says what clock each reads, and `specs/methodology/examples/time/trigger/` shows each kind of time trigger at work.

**A guard.** A guard is tested when its trigger happens, or when its state's work is done, against the facts as they then stand. A transition whose guard does not hold is no transition at all for that occurrence. A transition with no guard has one that is always true. A guard may test any fact about the entity or another, another entity's recorded status among them, as `loan status = "closed"`, a terminal state's name included. The state a machine governs is left by which terminal state that machine reached. A guard tests that by `exit` alone, whose value is that terminal state's name, as `exit = "approved"`.

**Two transitions one occurrence enables.** At most one is taken from a state, and the exclusive choice decides which, its guards never both holding. A governed state and a state of the machine governing it may both leave on one occurrence. Then the inner machine's transition, the more deeply nested, is taken.

**An effect.** An effect is the Algorithm or the Decision Table a transition's Effect cell cites, run as the transition is taken, after the From state is left and before the To state is entered. An action whose outcome decides where the entity goes is no effect. It is a state's work, and the transitions from that state route on what the work found. One occurrence that moves several entities in order is written in the machine it reaches first. That machine's effect is an Algorithm whose steps move the others. Each moved machine's trigger cites the step that moves it, and each step's move is complete before the next.

**A fork and a join.** The branches between a fork and a join each run at once, and one occurrence can take one transition in each. A terminal state reached in one branch ends the machine's run and cuts its other branches short. A join may carry a trigger.

**A protocol machine.** A machine whose Protocol field is `Yes` is a protocol machine. Its states hold no work, so it takes no Effect column, no transition with no trigger and no governed state. Each transition is taken on an actor's action alone, and says the state allows that action. An action no transition from the state takes is refused. Where the system tells an actor why, the reasons it distinguishes are a Decision Table over the request, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it, and no other reasons are written. Whether the machine allows an action in the entity's state is a fact, a question named `{entity} permits {action}?`, as `loan permits disbursal?`. Any construct may test that fact, citing the machine.

**Resuming where it left off.** A machine resumes where it left off by a fact the entity records, guarding the transitions from the machine's initial state.

A design adds a form for an element the canon does not write where a spec needs what the canon's writing cannot say. The mapping from UML's StateMachine to the State Machine:

**Table Name:** UML Elements

**Reference Key:** UML

**Required:** Section, Treatment

| UML | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| State | 14.2.3.4 | the same | | |
| initial Pseudostate | 14.2.3.7 | the same: the target of its transition is the initial state | | |
| no active state | 14.2.3.4.2, 14.2.3.8.3 | the same: before its run begins and once the run has ended, a machine is in no state | | |
| run-to-completion | 14.2.3.9.1 | differs: conditions one occurrence makes true together are taken in the occurrence's one step, where UML dispatches each event on its own | the standard's gap | an occurrence making two conditions true is one thing that happened, and a spec states one outcome for it, where dispatching each apart makes the outcome hang on an order no spec states |
| entry and doActivity Behaviors | 14.2.3.4.3 | the same: a state's work, begun when the state is entered | | |
| completion transition | 14.2.3.8.3 | the same: a transition with no trigger, taken once the state's work is done | | |
| external transition | 14.2.3.8.1 | the same: a transition from a state to itself | | |
| FinalState | 14.2.3.6 | differs: a terminal state, entering it completing the run; reached in one branch of a fork, it ends the machine's run and cuts its other branches short, where UML's FinalState completes that branch's Region alone | the standard's gap | a terminal state means the entity's journey is over, where completing one Region alone would leave it both finished and still moving |
| Event | 13.3.3.2 to 13.3.3.4 | the same: a trigger, its kind decided by what moves the entity | | |
| MessageEvent | 13.3.3.2 | the same: something done, what it carries the data its message carries, a fact its occurrence sets | | |
| SignalEvent | 13.3.3.2 | the same: a part reached, or a state entered | | |
| ChangeEvent | 13.3.3.3 | differs: a condition becoming true; one already true as its state is entered is taken at once, and one going from `null` to `true` becomes true, where UML's ChangeEvent occurs only as its expression changes from false to true | the standard's gap | an entity entering a state whose condition already holds would wait for a change that has already happened, which no spec means, and FEEL's `null` is a value UML's boolean expression does not have |
| TimeEvent | 13.3.3.4 | differs: relative time is counted from entering the state the transition leaves, even where the machine waited elsewhere first, where UML counts from the TimeEvent's activation; and, as [`§ Time`](#time) has it, an instant already past is taken at once, and an instant follows its fact; a relative amount of zero or less is taken at once, and a `null` one never | the standard's gap | a time rule is read from the state the entity is in, as 30 days in this state is, and an instant moved or already past, or an amount of zero, less or none, is a case UML leaves to the tool, which a spec must decide |
| guard | 14.2.3.9.2 | the same: a transition whose guard does not hold is no transition for that occurrence | | |
| conflicting transitions | 14.2.3.9.3 | differs: at most one is taken, as UML has it, and an exclusive choice's guards never both hold | the standard's gap | UML takes either of two enabled transitions, leaving the outcome to chance, where a spec decides one outcome for every case and a check proves the guards never both hold |
| transition priority | 14.2.3.9.4, 14.2.3.9.5 | the same: of a governed state and a state of the machine governing it, both leaving on one occurrence, the inner machine's transition is taken | | |
| effect Behavior | 14.2.3.8, 14.2.3.9.6 | the same: the Algorithm or the Decision Table a transition's Effect cell cites | | |
| fork Pseudostate | 14.2.3.7 | the same | | |
| join Pseudostate | 14.2.3.7 | differs: a join may carry a trigger, where UML's join takes none | the standard's gap | a join often waits for something to happen once its branches are done, as an approval does, which UML would hold in a state of its own |
| orthogonal regions | 14.2.3.2, 14.2.3.9.1 | the same: the branches between a fork and a join, one occurrence able to take one transition in each | | |
| ProtocolStateMachine | 14.4, 14.4.3.1 | the same: a machine whose Protocol is `Yes`, its states holding no work | | |
| ProtocolTransition | 14.4.3.2.4 | differs: taken on an actor's action alone, where UML allows other events | the canon's form | a protocol machine states what an actor may do, so its transitions are the actions it allows, and a machine another event moves is a behavioral machine |
| unexpected event | 14.4.3.2.1 | differs: in a protocol machine, an action no transition from the state takes is refused, where UML leaves it undefined | the standard's gap | an action a state does not allow needs an outcome a spec states, where undefined leaves the answer to the code |
| operation no transition refers to | 14.4.3.2.3 | differs: refused, as any action no transition from the state takes is, where UML leaves it callable in any state | the standard's gap | one rule then holds for every action a state does not allow, whether or not a transition names it |
| ProtocolTransition's precondition | 14.4.3.2.3 | the same: its guard | | |
| history Pseudostate | 14.2.3.4.4 | not written: a fact the entity records, guarding the transitions from the machine's initial state | the canon's form | a state to return to is something the entity knows, and a fact puts it where a guard and a check read it, where a history Pseudostate keeps it inside the machine |
| deferred event | 14.2.3.4.4 | not written: a fact the entity records | the canon's form | an occurrence held for later is something the entity keeps, and a fact shows it to every construct reading the entity |
| composite State | 14.2.3.4.7 | not written: UML calls it semantically equivalent to a submachine state, and a nested machine is a section of its own, governing a state as [`§ Constructs § State Machine § A Submachine State`](#a-submachine-state) has it | the canon's form | UML counts it equivalent to a submachine state, so one way of writing a nested machine keeps one way of saying it |
| entry point | 14.2.3.4.6, 14.2.3.7 | not written: a machine is entered at its initial state | the canon's form | a machine entered one way is read from its initial state, and another way in is another machine's initial state |
| exit point | 14.2.3.4.6, 14.2.3.7 | differs: a machine is left by its terminal states, a guard telling them apart by `exit` alone, as `exit = "approved"`, where UML tells a machine's ends apart by exit points, which the canon does not write | the canon's form | a guard on `exit` is a FEEL test a check reads, where exit points are a diagram's connectors, which a table does not draw |
| internal and local transitions | 14.2.3.8.1 | not written: an occurrence that moves the entity nowhere is no transition, and what it changes is a fact | the canon's form | a table of transitions lists where the entity moves, and what an occurrence changes without moving it is a fact, written by the construct changing it |
| exit Behavior | 14.2.3.4.3 | not written: the effect of the transitions leaving the state | the canon's form | work done on leaving is written on each transition leaving, so a reader of a row sees all the move does |
| choice and junction Pseudostates, compound transitions | 14.2.3.7, 14.2.3.8.4 | not written: a state whose work decides, its transitions an exclusive choice | the canon's form | a decision kept in one state's transitions has guards a check reads together, where pseudostates chain decisions across rows |
| terminate Pseudostate | 14.2.3.7 | not written: a terminal state | the canon's form | a terminal state already ends the run, and a second way of ending it would say one thing two ways |
| AnyReceiveEvent | 13.3.3.2 | not written: a class of occurrences, its members the machine's Trigger Classes table's rows | the canon's form | a trigger matching anything leaves unchecked which occurrences move the entity, where a class named with its members is read against the triggers written |
| Transition's triggers | 14.2.3.8, 14.2.4.8 | differs: one trigger to a row, several occurrences that move the entity alike named once as a class, its members the rows of the machine's Trigger Classes table, where UML lists a Transition's triggers on it, any one of them taking it | the canon's form | a row keyed by its trigger is cited and checked one occurrence at a time, and a class named once keeps its members in one home a check reads against the triggers written |
| state invariant | 14.2.3.4 | not written: a Constraint ([`§ Constructs § Constraint`](#constraint)) | the canon's form | a rule holding while a state is active is a Constraint like any other, written once in the construct whose checks read rules |
| ProtocolTransition's postcondition | 14.4.3.2.3 | not written: a Constraint ([`§ Constructs § Constraint`](#constraint)) | the canon's form | a rule holding after a move is a Constraint `after` the move, written once in the construct whose checks read rules |
| guard testing another object's state | 14.2.3.8.3 | not written: a test of that entity's recorded status | the canon's form | a guard reads facts, and another entity's state is a fact it records, so no machine reaches into another |
| ProtocolConformance | 14.4.3.3 | not written | no need yet | no spec here relates two protocol machines as one conforming to another, and a project needing it adds the form |

#### A Submachine State

A State Machine's state whose work is the run of another State Machine, started by entering the state, is UML's submachine State, its section 14.2.3.4.7, governed by that machine. A machine run apart from the state, another entity's or one started elsewhere, is no state's work. A state waiting on such a machine is left on a trigger, a part of that machine being reached. A governed state's description says it is governed: the words `governed by`, which name only a machine, then that machine's section cited. A description citing another machine's whole section always says them, so a state referring to a machine it is not governed by cites one of that machine's parts.

- **Machine.** One at most. A machine never governs itself, directly or through those it governs. A governed state is never terminal, since a terminal state has no work.
- **Entering it.** At the governing machine's initial state, by however many transitions reach it. The transitions from that initial state are guarded by why the state was entered, where that matters.
- **Leaving it by its machine's end.** By transitions with no trigger, as its table of exits has them, and `exit` is the one fact their guards test. A holder that routes on a fact as well leads each transition guarded by `exit` to a state with no work, whose own transitions route on that fact.
- **Leaving it on a trigger.** A transition with a trigger, taken from whatever state the governing machine is in: UML's group Transition, its sections 14.2.3.4.7 and 14.2.3.8.2. A trigger that every state of the work leaves the same way, to one state outside it, is written once. It is written on the outermost governed state whose every state it so leaves, and on no state inside it. A trigger that only some states of the work take, or take differently, is written inside the work, on each state taking it, and leads to a terminal state where it ends the work.

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

A precise, step-by-step computational procedure that produces a value or a transformation. A DAG or a State Machine orchestrates named tasks or services. An Algorithm specifies the computation inside one of those tasks, or any calculation that is not itself an orchestration. Each step written in one of its forms is checked, so a computation is stated exactly rather than described. It is UML's Activity ([`specs/methodology/external-references.md § External References [Name: UML]`](/specs/methodology/external-references.md#external-references)), adopted whole and written as a numbered table of steps taken one at a time, with no tie to any language or engine. [`§ Constructs § Algorithm § What It Means`](#what-it-means-2) states what UML means for what the table writes, and names each departure the canon makes from UML.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Ordered Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Step

**Locator:** a step, a row of its table matched by its Step column, its keys kept in one place, so a citation writes its key alone, `[Step: …]`

**Fields.** After those its interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Inputs | yes | | text | the facts it reads, each item a fact's name, or a fact's name, a colon and the citation of the Facts record declaring it in another file, as a Decision Table's Reads item is written; or none, written on the key's line |
| Output | yes | | text | the facts it gives, each item a fact's name; or none, written on the key's line, where the work its steps do is all it does |
| Runs When | yes | | text | what runs it: the citation of each construct running it, another Algorithm whose run cites it, a State Machine whose Effect cell or state's description cites it as the work done, a DAG whose task's work cites it, or a Decision Table whose computed outcome cites it as the Algorithm doing it, a citation of one of its steps or rows, a trigger, a plain outcome, an annotation and a Constraint's enforcement running nothing; or the occurrence it answers, written as a trigger of the kind something done is ([`§ Constructs § State Machine § What It Means`](#what-it-means-1)), a request or a job's run among them, a job's run saying what a missed and a late run do ([`§ Time`](#time)) |
| Precision | no | 34 | text | the significant digits each operation's result is rounded to, a whole number above zero and below 34, where its system's arithmetic holds fewer than FEEL's ([`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time)) |
| Rounding Mode | no | half even | text | the mode each operation's result is rounded by, and a value written to a fact holding decimal places: one of the modes [`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time) names, or the name of a fact the Algorithm knows whose Values hold only those modes, where the system's configuration chooses it |

**Facts.** A step names only a fact its Inputs or its Output name, a fact its file's Facts section declares, a fact a step sets, a loop's item and what it gathers, and a part of any of them, reached by FEEL's path, as `transaction.amount` ([`specs/methodology/expressions.md § Expressions § FEEL § Its Expressions`](/specs/methodology/expressions.md#its-expressions)). A fact its file's Facts section declares is typed by its record, and a list or a context by the type its record names, so a path into it is typed too. A fact read from another file, and any other fact, is known by name alone, and its kind is read.

**A stored value and a derived one.** A fact's value never changes once set, as a FEEL context never does ([`specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions`](/specs/methodology/expressions.md#lists-contexts-and-functions)). Setting a part gives the fact a new value, with that part replaced and every other part as it was. So:

- **A stored value.** Read by path, `{fact}.{part}`, as `period.emi`: a part a step sets or the system stores.
- **A value the system derives from others.** Read by a call, `{function}({value})`, given the current value, as `fully paid(period)`. It is never read by a path, as `period.fully paid`, which keeps what it held before a step changed what it derives from. In a filter the call is given `item`, as `periods[not(fully paid(item))]`.
- **An item copied from a list.** A value too. Once a step changes the list, the item is read from the list again, `{list}[{key} = {item}.{key}][1]`, as `periods[number = target.number][1]`, before it is changed, run or merged back. No step then works on, or merges back, a version older than the list's.

The function a step calls is a fact its file's Facts section declares ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)), with the Type `function<{parameters}> -> {type}`, or one a step sets. It is of one of these kinds:

- **A derived value.** Of what it is given, as whether a period is fully paid. Where the specs define it, its record's Derivation holds the FEEL function giving it.
- **A computation a system makes outside the specs.** As a library's or a service's. Its record holds no Derivation, and its Means says what computes it.
- **A function a computation sets.** FEEL's own function value, `Set {name} to function({parameters}) {expression}`, as `Set lowest to function(xs) xs[number = min(xs.number)][1]`, named within the Algorithm alone.
- **An operation giving a changed value.** Of what it is given, as `mapping added(transaction, installment.number, component, portion)`, a step writing what it gives back to a fact.

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

**Expressions.** A computation's expression, a comparison's condition, a loop's list and its order, a run's argument and a Terminates cell are FEEL ([`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel)). Each is judged with the facts the step may name in scope. The checks decide each expression's form, the names it holds, and the kinds it combines and gives: a condition's a yes or no, a loop's list a list, and a Terminates cell's a number. The checks also decide that a value written to a fact, a part or an Input is of the kind its record types it. Whether work computes or decides, and whether what it reads is what it means, is read.

An Algorithm is authored as a numbered table of steps, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Step` | the step's number, the steps numbered from 1 in order |
| `Action` | what the step does, one of the kinds Steps names |
| `Terminates` | why a step's loop ends, as A loop that must end has it, or `none` |

**Steps.** Each step is one of these, and nothing else. A loop or a comparison is a step of its own, never folded into another's work:

- **A computation.** `Set {fact} to {expression}` gives the fact the expression's value. `Set {fact}.{path} to {expression}` gives the fact its value with that part's replaced, as FEEL's `context put` gives it. The path's names are joined by `.`, each reaching into a context and none through a list. A value a later step reads is set so, never in words. A value a condition chooses is one computation, FEEL's `if … then … else`. It is never a comparison whose only work is setting one fact, on one branch or both.
- **A run.** `Run` and the citation of the Algorithm or the Decision Table it runs, and of nothing else. Then, for each fact the construct takes that the fact of the same name here does not give, ` with {input} as {expression}`, these separated by commas. Then, where the run gives facts a later step reads, `, giving` and what it gives, separated by commas. Each is a fact the construct run gives, written by its name, or `{output} as {fact}` where the fact here that holds it has another name. An Algorithm takes its Inputs and gives its Output. A Decision Table takes its conditions' facts, the facts of value its computed headers and computed outcomes name, and its Reads, and gives its outcomes. A function those headers and outcomes call is the table's own. Each fact the construct takes that no `with` gives is the fact of its name here. A run recurs where it runs the Algorithm it belongs to, or a construct running that Algorithm back, an Algorithm's run or a Decision Table's computed outcome.
- **A loop over a list.** `For each {item} of {list}, {order}: steps {n} to {m}`. Its body is the steps from the one after it to step m, and each pass takes the next item through them. The loop ends once every item has passed, and the step after step m follows. Its order is `by` a FEEL expression over the item and `ascending` or `descending`, a tie broken by `, then by` another; `in any order`, where no order changes what the loop gives; `in an order the system leaves open`, where an order changes it and none is fixed, the exception the Order field allows ([`§ Constructs § Ordered Construct`](#ordered-construct)); or `at once`, every pass running at the same time, a pass setting only its item and what it gathers, by a computation, a run or a loop it holds. A loop gathering a fact each pass sets writes `, gathering {fact} into {list}` before its colon. The list is set once the loop ends, and holds one value for each pass that set the fact. The gathered list's order is the order of the list walked as it stood when the loop began, sorted by the loop's keys where it has them, whatever order the passes ran in. A body reading the list reads what it held before the loop. A loop gathering its own item gathers it from every pass, changed or not, so updating some items keeps the rest. A body holds whole loops of its own, never the table's last step. It is entered only from its loop and left only at `End`: a jump from it names a step of it, and a jump from outside it names none. The order a loop walks its list is the loop's own. An Algorithm's Order field names the order it takes its Inputs and gives its Output.
- **A comparison.** `If {condition}, {branch}; otherwise, {branch}`. The condition is a FEEL boolean expression, as `unprocessed amount > 0 and processing type = "horizontal"`. Each branch is a computation, a run or work, or nothing, written `continue`.
- **Work.** Anything else the system does, written in words: posting, deleting, recording, sending. Work computes no value a later step reads, decides nothing and runs no construct. A value belongs to a computation, a choice to a comparison, and a construct's run to a run. Work cites no Algorithm or Decision Table whole: a citation of one of its steps or rows refers to it and runs nothing.

**Ends.** Each branch, and each step that is no comparison, ends `Go to step` and the number of a step the table holds, or `End`, or else continues to the next step. Where a loop's last step continues, it takes the next pass. `End` ends the run, inside a loop's body as anywhere. The Output's facts then hold the values set, and a list the loop was gathering is left as it stood before the loop. `End` is written alone, and a result is named by a computation before it. On every path to `End`, each fact the Output names is set by a computation, given by a run or gathered by a loop. The exception is a fact its Inputs also name: where no step on the path sets it, that fact holds the value it was given. The last step, and each branch of it where it is a comparison, ends `End` or goes to another step, so the Algorithm ends only at an `End`.

**A loop that must end.** A loop is a loop over a list, a comparison one of whose branches goes back to an earlier step or to its own, or a run recurring. A step that is no comparison never goes back, so a loop whose test falls in its middle is written with its test at the step going back. A loop over a list ends with its list, fixed as the loop begins. Every other loop states why it ends in a `Terminates` column after Action. The cell of each step going back or recurring holds either a FEEL expression giving the number that shrinks with each pass toward an end the step reaches, as `high - low`, or the citation of the Constraint its end rests on, one something keeps. Every other cell holds `none`. The column is written only where a step goes back or recurs.

**Arithmetic.** A number is FEEL's ([`specs/methodology/expressions.md § Expressions § FEEL § Its Values`](/specs/methodology/expressions.md#its-values)), unless the Algorithm's Precision and Rounding Mode state its system's. Each operation is then rounded as [`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time) has it. Under either, a value written to a fact holding decimal places is rounded to them by the Algorithm's Rounding Mode, as that section has it. Any other value is rounded only by a computation calling `decimal` or one of FEEL's rounding functions ([`specs/methodology/expressions.md § Expressions § FEEL § Its Functions`](/specs/methodology/expressions.md#its-functions)), never by the word `rounded`. The call's decimal places are a number or a fact choosing them. An Algorithm holds one precision and one rounding mode for every step. Steps its system computes with another are an Algorithm of their own, which is run and states theirs. One operation rounded otherwise is rounded by its computation's own call.

**Order.** A result that could depend on an order states the order, as the Order field has it ([`§ Constructs § Ordered Construct`](#ordered-construct)). A loop's order is stated with its ties broken, and a remainder's share is given by the order that takes it.

**Worked examples.** Algorithms written whole, as a file would hold them, are in `specs/methodology/examples/construct/algorithm/`.

**Name.** An Algorithm is named for its process as a thing, `Report Assembly`, never for an activity, `Running payroll`.

**Checks.** An instance is reported for:

- no Inputs, Output or Runs When field, an Inputs item that is neither a fact's name nor a name, a colon and a citation, an Output item that is no fact's name, or an Output fact its Inputs do not name that nothing sets;
- two steps sharing a number;
- a jump to a step the table does not hold;
- a Precision that is no whole number above zero and below 34, or a Rounding Mode that is neither a mode [`specs/methodology/expressions.md`](/specs/methodology/expressions.md) names nor a fact the Algorithm knows whose Values hold only modes;
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

An Algorithm means what UML's Activity means for what the Algorithm's table writes, element by element as this section's UML Elements table gives it, so neither an author nor a reader needs to recall the standard.

**A run.** Each run of the Algorithm takes its Inputs and gives its Output. Its Inputs and Output are its parameters. A fact both name holds what it was given where nothing sets it. A run of another construct is synchronous: the step waits until that construct's run ends. A Decision Table is run as another construct is. Each `with` is an argument, the value passed to a fact the run takes. Each fact the run takes that no `with` gives takes the value of the fact of that name. Each fact the run gives is written to the fact of that name, or to the fact `as` names. A run's arguments and what it gives are matched to the construct's facts by name. A run recurring states why it ends.

**A step.** The steps follow one another. A computation's language is FEEL. A computation writes its value to the fact, replacing what the fact held. A computation setting a part reads the fact and replaces the part's value for each name of its path. Because the fact's value is a data value, that replacement gives a modified copy. The computation then writes that copy back to the fact. Work is a step whose body is written in words. A value a later step reads is set only by a computation.

**A comparison and a jump.** A comparison has two outgoing flows, one guarded by its condition and one by `else`. A step that two flows reach, by a jump or by following another, is entered where the flows merge, so a jump back forms a loop. Such a loop states why it ends.

**A loop over a list.** A loop over a list runs its passes:

- one after another in the order of its `by` keys where the loop is ordered by them, the list sorted by them;
- one after another over an unordered collection where the loop is `in any order` or `in an order the system leaves open`;
- free to overlap where the loop is `at once`.

The loop's list is fixed as the loop begins. What the loop gathers is offered once every pass has completed. It holds the values of the passes that set it, in the order of the list walked, whatever order the passes ran in. It holds the item of a pass that set nothing where the loop gathers its own item. It is left as it stood where an `End` inside the body ends the run.

**An end.** The first `End` reached ends the run and every flow in it, and the Output's facts hold the values set. Inside a loop's body, `End` ends the whole run.

The mapping from UML's Activity to the Algorithm:

**Table Name:** UML Elements

**Reference Key:** UML

**Required:** Section, Treatment

| UML | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| Activity | 15.2.3.1 | the same: the Algorithm | | |
| execution | 15.2.3.6, 15.4.3.2 | the same: a run, taking its Inputs as its input parameters and giving its Output as its output parameters | | |
| Parameter | 15.2.3.6 | the same: the Inputs and the Output | | |
| inout Parameter | 15.2.3.6 | differs: a fact the Inputs and the Output both name holds what it was given where nothing sets it, where UML passes out only what flows to its output node | the standard's gap | an Algorithm updating a fact in place is common, as a balance is, and holding what it was given states what the fact holds on every path, where UML would leave it with no value |
| CallBehaviorAction | 16.3.3.1 | differs: a run of another construct, synchronous, each `with` an argument, the value its InputPin passes to a Parameter, and each fact the run gives the value on an OutputPin; a Decision Table is taken as the Behavior it calls, where a DMN Decision is no UML Behavior; pins are matched to parameters by name, where UML matches them by their order; and a run recurring states why it ends, where UML requires none | the standard's gap, the canon's form | a Decision Table is one of the canon's constructs a step runs, so it is called as one; a name is what a reader and a check match, where an order is easily got wrong; and a run recurring with no stated end has no stated outcome |
| ReadVariableAction | 16.9.3.2 | the same: reads the fact of that name, for each fact a run takes that no `with` gives, and for a computation setting a part | | |
| Variable | 15.2.3.5 | the same: a fact, held as a Variable is | | |
| AddVariableValueAction | 16.9.3.3 | the same: writes a value to the fact of that name, or to the fact `as` names, replacing what the fact held | | |
| Action | 16.2.3.1 | the same: a step | | |
| ControlFlow | 15.2.3.3 | the same: the steps following one another | | |
| ValueSpecificationAction | 16.4.3.5 | the same: a computation, FEEL its language | | |
| AddStructuralFeatureValueAction | 16.8.3.3 | the same: a computation setting a part replaces the part's value by one for each name of its path, `isReplaceAll` true | | |
| StructuralFeatureAction on a data value | 16.8.3.1 | the same: the action gives a modified copy on its result pin, which the computation writes back to the fact by an AddVariableValueAction | | |
| OpaqueAction | 16.2.3.2 | differs: work, its body written in words; a value a later step reads is set only by a computation, where UML lets an OpaqueAction write values | the canon's form | a value set by words alone is one nothing checks, so only a computation in FEEL sets what a later step reads |
| DecisionNode | 15.3.3.6 | the same: a comparison, its two outgoing flows guarded by its condition and by `else` | | |
| MergeNode | 15.3.3.5 | differs: a step two flows reach, by a jump or by following another, so a jump back forms a loop; such a loop states why it ends, where UML requires none | the standard's gap | a loop with no stated end has no outcome a reader can check |
| ExpansionRegion | 16.12.3 | the same: a loop over a list, iterative where the loop is ordered `by` keys, its passes run one after another in that order, the list sorted by them; iterative over an unordered collection where the loop is `in any order` or `in an order the system leaves open`; parallel where the loop is `at once`, its passes free to overlap; the loop's list its input collection, fixed as the loop begins | | |
| output ExpansionNode | 16.12.3 | differs: what the loop gathers, offered once every pass has completed, holding the values of the passes that set it in the order the input collection induces; it keeps the order of the list walked where the region is unordered or parallel, where UML leaves that order undefined; it holds the item of a pass that set nothing where the loop gathers its own item, where UML filters that pass out; and it is left as it stood where an `End` inside the body ends the run, where UML offers the list partly filled | the standard's gap | a result a spec states never hangs on how the passes were scheduled, so the list walked orders it, and keeping a pass's own item and a list as it stood gives every path a stated value |
| ActivityFinalNode | 15.3.3.2, 16.11.3.1, 16.12.3 | differs: `End`, the first reached ending the run and every flow in it; inside a loop's body, it ends the whole run, where UML's ActivityFinalNode inside a StructuredActivityNode or an ExpansionRegion ends that node or region alone | the canon's form | `End` reads as the end of the procedure wherever it stands, and ending only the loop would give one word two meanings |
| ForkNode and JoinNode | 15.3.3.3, 15.3.3.4 | not written: a fork and a join of steps, and steps run at once other than a loop's passes, are a DAG ([`§ Constructs § DAG`](#dag)) | the canon's form | work at once, with waits between tasks, is a DAG's, whose dependencies a check reads, and an Algorithm stays a sequence a reader follows a step at a time |
| AcceptEventAction | 16.10.3.1 | not written: a wait for an occurrence is a State Machine's trigger, the Algorithm running once it happens | the canon's form | waiting for something to happen is behavior over time, which a State Machine's trigger writes, and an Algorithm computes once it has what it needs |
| exception raised and handled | 16.13.3.2, 15.5.3.2 | not written: a failure is an outcome the Output gives, and the run ends at `End` with it | the canon's form | an outcome a caller handles is written in the Output, where a reader and a check see every way the run ends |
| InterruptibleActivityRegion and ActivityPartition | 15.6.3 | not written by an Algorithm's table: a task's timeout writes the region in a DAG's table ([`§ Constructs § DAG § What It Means`](#what-it-means)) | the canon's form | a timeout bounds a task's work, which a DAG schedules, and an Algorithm's steps compute and wait for nothing |
| stream, and ObjectFlow other than a named fact | 13.2, 16.12.3, 15.2.3.4 | not written: a fact passes between steps by its name | the canon's form | a fact named once is what a check follows from step to step, where flows between pins are drawn, which a table does not do |

### Constraint

A rule that must hold of a system's facts, independent of any single decision point or process step: an invariant on the state or output of something else, or a condition an operation requires as it begins or guarantees once it ends. Written so, what must hold and what keeps it are stated, and a rule nothing keeps is recorded rather than hidden. It is UML's Constraint ([`specs/methodology/external-references.md § External References [Name: UML]`](/specs/methodology/external-references.md#external-references)), adopted whole and written as a table of rules, each a FEEL boolean, with no tie to any language or engine. [`§ Constructs § Constraint § What It Means`](#what-it-means-3) states what UML means for what the table writes, and names what the canon adds to UML.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Configured Construct`
- `§ Constructs § Keyed Construct`

**Reference Key:** Name

**Locator:** a rule, a row of its table matched by its Name column, its keys kept in one place, so a citation writes its key alone, `[Name: …]`

A Constraint is authored as a table, its columns each headed by a field label:

| Column | Holds |
|---|---|
| `Name` | the rule's name ([`§ Constructs § Keyed Construct § Part Identifier`](#part-identifier)) |
| `Constraint` | the rule |
| `Applies To` | when the rule holds |
| `Enforced By` | what keeps the rule |

**Rule.** A rule is a FEEL boolean ([`specs/methodology/expressions.md § Expressions § FEEL`](/specs/methodology/expressions.md#feel)) over the facts its file declares, each named as its Facts record declares it ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)), as `sum(portions) + overpayment = amount`. A Constraint sits in the file whose Facts section declares the facts its rules name, so a rule names no fact another file declares. A rule reaches another construct's facts only as When it holds has it. A rule of every entity of a kind names the fact holding them all, a list, and quantifies over it, `every {item} in {list} satisfies {rule}`, as `every t in transactions satisfies t.debits = t.credits`. A value as it stood before an operation is a fact declared for it, as `balance before`. A rule reaching along a chain of entities calls a function fact that gives the chain, as `ancestors(record)`. A rule governing some values only tests them in itself, `if {condition} then {rule} else true`, as `if currency.decimal places = 0 then modulo(amount, currency.multiple) = 0 else true`, since Applies To says when a rule holds, never of which values. A State Machine's state invariant is such a rule, narrowed by the fact the machine's Recorded In names, as `if status = "active" then balance >= 0 else true`. A rule's explanation, where it needs one, is prose after the table.

**When it holds.** An operation is a run of an Algorithm or of a DAG, a transition taken with its effect, an occurrence a State Machine answers, or what a section's own text states is done. Each operation is all or none. It either completes, reaching its end, or fails, stopped by an error, a timeout or a precondition it cannot meet. What a failed operation wrote is undone, so a rule holding as the operation began holds as it ends ([`§ Constructs § Constraint § What It Means`](#what-it-means-3)). A request turned away completes, and keeps what it wrote, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it. A construct whose operation keeps less than all of its writes states so where it says what a failure does. Applies To is `always`, `after {citation}` or `before {citation}`, the citation an operation's. A rule `always` holds at every rest, whenever no operation is running. A rule `after` an operation holds once a run of it completes: the operation's postcondition. A rule that holds only once some part has run, as a summary a job recomputes, is `after` that operation. A rule `before` an operation holds as its run begins: its precondition, what the operation relies on. Such a rule is Enforced By the parts of what runs the operation that make it hold. Applies To draws the same line Design by Contract draws in programming, between an invariant, a precondition and a postcondition. A check the system makes of a request is no precondition, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it. Beside the file's facts, a rule `after` an Algorithm reads its Inputs and Output, one `before` it reads its Inputs, one `after` or `before` a transition reads those of the Algorithm its effect runs, one `before` a DAG reads what the work of its first tasks takes and one `after` it what the work of its tasks takes and gives, as [`§ Constructs § DAG`](#dag) has them, and one `after` or `before` an operation a section's own text states reads the file's facts alone. The citation names the operation whole, an Algorithm's or a DAG's section, a transition by its Name, or a section whose own text states what is done, never a step or a task.

**Enforcement.** Enforced By is the canon's addition to UML's Constraint, and names what keeps the rule. It holds the citation of each part that keeps the rule where a write could break it: a part of another construct, a step, a row, a transition or a task, or a section whose own text states the mechanism. Several are joined by `and`, `{citation} and {citation}`, since an invariant is kept only where every operation changing its facts keeps it. A rule that a Decision Table turning requests away keeps is Enforced By that table's rows, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it. A part that breaks the rule, tolerates its breach or runs on no path keeps nothing, and is no enforcement. A rule nothing keeps is written so the specs say what holds and what does not. Its Enforced By is `nothing: {what breaks it or leaves it unkept}`, citing after those words any part that keeps some of it. A rule some paths keep and others do not is written by its paths, each by when its rule holds. A path whose rule holds at every rest is an `always` row narrowed by the fact that tells the path apart, its source or its writer. A path whose rule holds only as its own operation completes is a row `after` that operation. The path nothing keeps is the row opening `nothing:`. A Constraint enforced by `nothing:` is listed on every audit run as a warning, never a finding. The gap is the system's, recorded, and the specs are complete in recording it.

**A derived value.** A stored fact the system derives from others is a Constraint whose rule is `{fact} = {expression}`: UML's derivation specified by a constraint. The rule is `always` where the system keeps it so, or `after` the operation that recomputes it where it lags between runs, and is Enforced By what writes it. A value the system derives on demand, stored nowhere, is a Facts record's Derivation ([`§ Constructs § Algorithm`](#algorithm)). No Constraint states a fact's value as its entity is created: that is the Facts record's Initial Value ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)).

**A case a Constraint rules out.** A Decision Table covers every case the Values of the facts it tests allow ([`§ Constructs § Decision Table`](#decision-table)). A Constraint narrows no table's cases, since a Constraint may fail. A value no fact ever holds is excluded by the fact's Values, where its type alone does not bound them. A table then need not cover it.

**An approximation.** A rule bounding an approximation states the bound as the rule, `abs({computed} - {intended}) <= {tolerance}`, Enforced By the step that approximates.

**Worked examples.** Constraints written whole, as a file would hold them, are in `specs/methodology/examples/construct/constraint/`.

**Checks.** A Constraint is checked once, across files, with its citations resolved. A citation that resolves to nothing is a finding of the citation checks. Some questions are read, never decided by the script: which part keeps a rule, whether a section an Applies To cites states an operation in its own text, whether every write able to break a rule is covered, and whether a bounded step keeps its bound.

An instance is reported for:

- a rule that, judged with the facts in scope, is in no form FEEL has, gives no yes or no, names a fact nothing declares, combines values of two kinds or reaches a part a fact does not hold;
- an Applies To that is neither `always` nor `after` or `before` a citation, or one citing a step or a task, a construct that is no operation, a record section, or a State Machine rather than a transition of it;
- an Enforced By that is neither citations joined by `and` nor `nothing:` and words;
- a rule that nothing keeps, listed as a warning, never as a finding.

#### What It Means

A Constraint means what UML's Constraint means for what its table writes, element by element as this section's UML Elements table gives it, so neither an author nor a reader needs to recall the standard.

**A rule.** A Constraint's rule is a Boolean expression, satisfied where it evaluates to true. The rule's language is FEEL. The facts the rule names are the elements it constrains. Its Applies To is its context, which decides when the Constraint is evaluated. `always` is every rest between operations.

**A precondition and a postcondition.** A rule `before` an operation is a precondition, and one `after` it a postcondition, of the Behavior that the Algorithm, the DAG or the transition's effect is. An Activity holds them as a Behavior does. A precondition holds as the Behavior is invoked, and an implementation may assume it. A postcondition holds once the Behavior's invocation completes successfully. An operation a section's own text states takes them too. A ProtocolTransition's precondition is its guard and its postcondition a Constraint, as [`§ Constructs § State Machine § What It Means`](#what-it-means-1) has it.

**A derived value.** A derived value's derivation may be specified by a constraint. The Constraint whose rule is `{fact} = {expression}` is that constraint.

**An operation all or none.** An occurrence a State Machine answers is dispatched only once the one before it is fully processed. An occurrence, a run of an Algorithm or of a DAG, or a transition taken is all or none. Where it fails, what it wrote is undone. Where it does not complete, it fails.

**Enforced By.** An unsatisfied Constraint makes the model's realization invalid. Enforced By names what keeps a Constraint satisfied.

The mapping from UML to the Constraint:

**Table Name:** UML Elements

**Reference Key:** UML

**Required:** Section, Treatment

| UML | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| Constraint | 7.6.3 | the same: its specification, a ValueSpecification of type Boolean satisfied where it evaluates to true, is the rule, and its constrainedElements are the facts the rule names | | |
| constraint language | 7.6.4 | the same: FEEL, a language UML leaves to the Constraint, so FEEL is no departure | | |
| context | 7.6.3 | differs: Applies To, which decides when the Constraint is evaluated, and the canon adds that `always` is every rest between operations, where UML names no such time | the standard's gap | a rule is checked at a time a spec states, and UML names none, so the canon's operations give it, `always` being every rest between them |
| precondition and postcondition | 13.2.3.1 | differs: a rule `before` or `after` the Behavior that the Algorithm, the DAG or the transition's effect is, and an operation a section's own text states takes them too, where UML holds them of a Behavior alone | the standard's gap | the canon's operations are its Algorithms, DAGs and effects, and an operation a section states in its own text, so the rules about an operation attach to it there |
| Activity's preconditions and postconditions | 15.2.3.6 | the same: an Activity holds them as a Behavior does | | |
| derived Property | 9.5.3 | the same: a derived value, its derivation specified by the Constraint whose rule is `{fact} = {expression}` | | |
| run-to-completion | 14.2.3.9.1 | differs: kept, and the canon adds that an occurrence, a run of an Algorithm or of a DAG, or a transition taken is all or none | the standard's gap | a Constraint holds between operations only where no operation is ever seen half done |
| unsatisfied Constraint | 7.6.3 | differs: the canon adds Enforced By, where UML holds that an unsatisfied Constraint makes the model's realization invalid and says nothing of what keeps one satisfied | the standard's gap | a rule nothing keeps is a suggestion ([`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills)), so the canon names the parts keeping it, which a check reads |

### Basic Table

A table of items of one kind, each row an item and each column one of the item's fields. It is the Record Form's pattern laid out in rows ([`§ Constructs § Record Form`](#record-form)), so items of one kind read at a glance and, where the table is keyed, each row can be cited. A Basic Table is recognized by its shape ([`§ Defining Constructs § Declaring a Construct`](#declaring-a-construct)). It is the one concrete construct implementing no [`§ Constructs § Declared Construct`](#declared-construct): a table outside a construct's block is a Basic Table, whatever it holds, and follows this section, never another construct's. Whether a table of entries should be one is the question [`§ When to Use Which § A Table's Construct`](#a-tables-construct) answers: a table there to define items needing no more than a row declares is one. A Basic Table is checked for its form, its key, its required columns and its citations, rather than for what it leaves out. It follows no outside standard, since none meets its need.

**Extends:** `§ Constructs § Tabular Construct`

**Implements:**
- `§ Constructs § Keyed Construct`

**Locator:** a row of the table its fields open, matched by the columns its Reference Key names, its keys kept in one place, so a citation writes its key alone, or, where the table declares a Table Name, the path its name and its key make

**Columns.** Every column is headed by a field label, except a header in backticks, which is literal text written as it is elsewhere ([`specs/methodology/spec-style.md § Literal Text`](/specs/methodology/spec-style.md#literal-text)), and a proper noun keeping its own casing, as `macOS`:

| Column | Holds |
|---|---|
| a field | the row's value of the field its header names, however Columns has the header written |

**Reference Key.** Wherever a table's rows have a natural key, the column or columns naming each row as its readers know it, a `**Reference Key:**` field ([`§ Constructs § Keyed Construct`](#keyed-construct)) names them, whether or not a row is cited. The field opens a paragraph of its own before the table, after the table's Table Name where it has one. A table whose rows have no natural key declares none. The key's columns are required, and their values are unique together, as [`§ Constructs § Keyed Construct`](#keyed-construct) has every key. A Reference Key names only columns its table holds. A citation names a row by its key, or by the path the Table Name and the key make. A Basic Table declaring no key has no row cited.

**Required.** The columns besides the key that every row must fill are named in a `**Required:**` field, separated by commas. The field opens a paragraph of its own before the table, after the table's Table Name and Reference Key where it has them. Any other cell may stand blank, meaning nothing ([`§ Constructs § Tabular Construct`](#tabular-construct)). The Required field itself, in a table of fields:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Required | no | none | text | the columns besides its key every row must fill, separated by commas |

**Checks.** An instance is reported for:

- a header that is no field label, except a header in backticks and a word in a proper noun's own casing;
- a Reference Key naming a column its table does not hold;
- a Required naming a column its table does not hold, or one its Reference Key names;
- a blank cell in a column its Reference Key or its Required names;
- its fields out of their order: Table Name, Reference Key, Required.

### Record Form

An entry of one kind written repeatedly into a methodology spec, an application spec, or a working file, each record stating the same named fields. What differs between records is each field's value, never which fields there are. Written so, every entry carries the fields its kind needs, each field is checked, and none goes missing. The Record Form follows no outside standard, since none meets its need. A closed set a spec defines may be one too ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), each member with fields saying what it is. A work order's statuses are such a set, settled as a vocabulary before, and apart from, the workflows that use it. An application's closed set sits in its product spec ([`specs/methodology/spec-placement.md § Product or Technical`](/specs/methodology/spec-placement.md#product-or-technical)). Whether entries are a record type's records or a Basic Table's rows is the question [`§ When to Use Which § A Table's Construct`](#a-tables-construct) answers. A set that changes while the product runs is data, a configured instance's ([`§ When to Use Which § A Configured Instance`](#a-configured-instance)). A schema of data the product stores is not a Record Form, however many records the product holds. The technical specs describe it as they describe data, and a closed set's technical counterpart cites the set rather than restating its records, as [`specs/methodology/spec-placement.md § Product or Technical`](/specs/methodology/spec-placement.md#product-or-technical) places it.

**Extends:** `§ Constructs § Construct`

**Implements:**
- `§ Constructs § Declared Construct`
- `§ Constructs § Keyed Construct`

**Locator:** a record of the record section a citation names, matched by its identifying fields, each record section keeping its keys in one place, so a citation writes its key alone

A record type is an instance of this form, as a Decision Table is an instance of its section, and the type's records are the type's instances ([`specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`](/specs/methodology/sourcing-and-citation.md#a-definition-and-its-instances)). A type is defined at the home of the rule it serves, in a section titled with the type's name, as a construct's section is titled with the construct's, `## Open Question` say. That section's prose says where the records go. The type is declared there as a construct is ([`§ Defining Constructs § Declaring a Construct`](#declaring-a-construct)): a `**Construct:**` field naming this form, then the type's fields, then its tables. A type extending another by Extends holds every field its base holds, in the base's order, and its own fields after them. A type's fields, after those this form's interfaces give:

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Plural Name | yes | | text | the plural of the type's name, which titles each section holding its records and no other section where they may sit, so a definition and a collection of records never share a title: a canon type's records may sit in any file, and an application spec's type's in the application specs, no two types reaching one file sharing a Plural Name |
| Reference Key | where it extends no type | | text | its key ([`§ Constructs § Keyed Construct`](#keyed-construct)), its identifying fields, a key of one field marking that field Unique; a type extending another declares none, taking its base's |

A type's tables come in this order, each a table of fields as [`§ Constructs § Construct`](#construct) gives one. Where the type declares section fields beyond a record section's own, Diagrams and Records, a table of those comes first. Then comes the table of its record fields, in the order a record gives them, with a column after `Field`, headed by a field label:

| Column | Holds |
|---|---|
| `Unique` | yes or no: whether the field's values are unique on their own across a record section's records |

**The record section.** A type's records sit together in a record section of their own, titled with the type's Plural Name. The section holds only fields. `**Diagrams:**` comes first. Then come any section fields of its own the type declares, facts about the collection as a whole, each given in the order the type's table of them sets, and each required one present. `**Records:**` comes after them, ending the section. A record section's own fields, in a table of fields ([`§ Constructs § Construct`](#construct)):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Diagrams | no | none | text | a list, a citation of each diagram rendering the section or any record in it, sorted in plain character order, so whoever edits a record meets every diagram drawing it |
| Records | yes | | text | a list, an item to each record, at least one |

A blank line separates one section field from the next, and one record from the next. Each list value ends as [`§ Fields`](#fields) states, so the Diagrams bullets and the records never run together.

**A record.** A record gives its fields ([`§ Fields`](#fields)), at most one per row of its type's table, in that order. The first sits on the list item's own line. Each of the rest sits on a line indented two spaces directly beneath the one before, and every line of the item belongs to one field's value. No blank line falls between a record's fields, since they are one record's facts serving one purpose, and white space separates only content that differs. Every record carries every field its type requires, and no field its type does not define. No two records in one section share the values of their identifying fields. An identifying field is required.

**An identifying value.** A record's identifying value is written as [`§ Constructs § Keyed Construct`](#keyed-construct) has any part's. A type whose records are cited and whose natural identifier is long, such as a question or a description, adds a short identifier as its key. The natural identifier is then a field marked Unique.

**Why a list.** Records are not table rows, because an entry needs what a row cannot declare, as the question More than a row declares? in [`§ When to Use Which § A Table's Construct`](#a-tables-construct) has it. Records are not headings either. A heading's section admits any content and further headings, where a list item holding only its fields is bounded, so a reader and a script can tell where one record ends and whether it holds exactly its type's fields.

**A closed set.** A fact whose values are a closed set's members takes them by its Values, the citation of the section holding them. That section is the set's record section or, where its members need no more than a row, its keyed Basic Table ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact), [`§ Constructs § Basic Table`](#basic-table)). So every construct testing the fact draws on the one set. A State Machine recording its state in the fact has each of its states one of the set, described as [`§ Constructs § State Machine`](#state-machine) has a state drawn from a closed set described. A Decision Table's condition testing the fact has each cell within the set. The set's members sit in the one section cited, the set's home. Another section of the set's type holding records where they may sit is reported. Several workflows may each draw on one set, using the members each needs.

**Worked examples.** Record types and their records written whole, as a file would hold them, are in `specs/methodology/examples/construct/record-form/`.

**Name.** A record type is named for the entity its records are, `Work Order Status`.

**Checks.** An instance is reported for:

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

**The clock.** A date or a time is read on a clock: the wall clock, unless a construct names another. A clock other than the wall clock, as a business date a job advances, is a fact of the Type date or date and time. It is declared once, in the Facts section of the file whose subject owns it ([`§ Defining Constructs § Declaring a Construct § Fact`](#fact)). Wherever a cell, a guard, a trigger or a step reads it, in any file, it is named by that fact's name. Where its time zone matters, the fact's Means states it. Which form a trigger takes on each clock is the trigger kinds' table's ([`§ Constructs § State Machine § What It Means`](#what-it-means-1)); a trigger reads the wall clock by `after` or `at` alone, never by `today()` or `now()`. On the wall clock a date stands for its midnight UTC, as FEEL has it ([`specs/methodology/expressions.md § Expressions § FEEL § Its Values`](/specs/methodology/expressions.md#its-values)), and an instant in another zone is a date and time in that zone, as `date and time(due date, @"00:00:00@America/New_York")`.

**The value in force.** A value that changes from a date on, as a rate or a limit does, is a fact whose Type is a function of the instant, as `function<date> -> number`, read by a call naming its instant, `{value}({instant})`, as `penalty rate(business date)`. Its Derivation gives it from the facts holding its changes, or its Means says what system holds it. A construct reads it only by such a call, so the instant each value is read at is written where it is read. A rule changed from a date is one construct testing the period's date, not two.

**A period a change falls within.** A construct computing over a period reads a value in force at the instants its rule fixes, and those reads say how the period is split. A value fixed for the whole period is read once, on the period's first day or its last, `{value}({period start})`, as `rate(period start)`. A value accruing day by day is read at each day of the period and the days' shares summed, an empty period accruing nothing, `if {end} > {start} then sum(for i in 0..({end} - {start}).days - 1 return {share}) else 0`, as `if period end > period start then sum(for i in 0..(period end - period start).days - 1 return balance * rate(period start + @"P1D" * i) / 365) else 0`. A value in force and a period's split are shown in `specs/methodology/examples/time/value-in-force/`.

**Backdated and withdrawn.** An instant computed from a fact follows the fact while the machine waits on it. The instant moves when the fact changes, and it is withdrawn when the fact is removed. This departs from UML, which leaves a TimeEvent fixed once activated ([`§ Constructs § State Machine § What It Means [UML Elements.UML: TimeEvent]`](#what-it-means-1)). A status that may change on past dates is derived from its facts each time it is read, never a machine's state.

**Calendars.** Date and time arithmetic is FEEL's, in the Gregorian calendar ([`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time)), a month's end pinned as its row records ([`specs/methodology/expressions.md § Expressions § FEEL [DMN Elements.DMN: years and months duration]`](/specs/methodology/expressions.md#feel)). A date kept on its month's last day, a date moved to a business day and a date moved by a count of business days are the canon's functions, and a calendar of business days is a fact of the type they take, as `trading calendar` ([`specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions`](/specs/methodology/expressions.md#the-canons-functions)). Another calendar, as a fiscal one, is a named input. A length counting both its first and its last day is written with `+ 1`.

**An instant already past.** An absolute instant already past when its state is entered is taken at once, within the bound [`§ Constructs § State Machine § What It Means`](#what-it-means-1) sets on one occurrence's step. This departs from UML, which leaves the case unsaid ([`§ Constructs § State Machine § What It Means [UML Elements.UML: TimeEvent]`](#what-it-means-1)).

**A relative amount.** The amount of relative time passing may be a fact, read each time its state is entered. It counts the wall clock's time, every day alike. Time counted in business days, or from anything but entering the state, is counted from a fact recording when it began, as `at overdue since + @"P30D"`, `at add business days(overdue since, 5, trading calendar)` or, on another clock, `when business date >= add business days(overdue since, 5, trading calendar)`. Where it is counted from entering the state, that fact records when the state was last entered, set by the effect of each transition entering it and, for the initial state, also as its machine's run begins.

**A job's run.** A time or a condition a periodic job detects, as a close of business does, is written as the job's run, something done. The trigger names the run, as `the close of business for a date` does, and the section of the construct it runs says what a missed run and a late run do: catch up each date missed, catch up only the latest, or lose it.

**Worked examples.** Constructs reading time, written whole as a file would hold them, are in `specs/methodology/examples/time/`.

## When to Use Which

A construct is used where a rule, a process, an entity's behavior, an entry written repeatedly into the specs or the working files, or a closed set a spec defines needs checkable completeness. Prose is used everywhere else. Prose that repeats one framing for each of several items holds items of one kind, however it reads. They are written as a table, its columns giving the framing once, its construct the one [`§ When to Use Which § A Table's Construct`](#a-tables-construct) gives. Prose states a rule one fact decides, sending its cases to at most two outcomes, the fact's and its otherwise, unless the rule is written as a table, which [`§ When to Use Which § A Table's Construct`](#a-tables-construct) decides. A rule reading two or more facts, or one fact sending its cases to more than two outcomes, takes the construct this section's table chooses, however it reads, since routing written in an author's own words never looks like a rule to the one writing it. A claim that something holds of the system's facts sends no case anywhere and is a Constraint's ([`§ Constructs § Constraint`](#constraint)). A request turned away for a reason is one of the outcomes counted.

A rule is counted whole, across every passage stating part of it. Passages are one rule where they decide the same outcome for cases told apart by the same facts. What becomes of an uncommitted change, told apart by its origin, is one such rule. Each passage may fix one more fact, such as an event, a state or a kind of case, and the rule counts each such fact among its own. So a rule may read two or more facts even where each of its passages reads only one. Its passages are gathered within the specs and [`specs/AGENTS.md`](/specs/AGENTS.md), from the files a passage may cite ([`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed)). No skill is a rule's home ([`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills)), so a skill holds no passage to gather. A materialized view and a product and technical counterpart are not gathered with the passages they restate ([`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync`](/specs/methodology/sourcing-and-citation.md#keeping-specs-in-sync)). A rule the count sends to a construct is written once, as that construct, and each passage that routed its cases cites it rather than restating its routing ([`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact)).

Choose the simplest construct that meets the need, by the questions this section's table asks, in order. The first question answered yes chooses, so prose is reached first. The State Machine comes after every other construct a rule or a process can take, since it is the most general of them. The Record Form, which holds entries and no logic, comes last. Each question is answered from the shape of the case, what it is made of and what it waits for, never from what it is called. The construct chosen is written as its section in [`§ Constructs`](#constructs) has it, and means what its standard says. A table is never prose. Where these questions send a table's case to no DAG, Algorithm, State Machine or Constraint, [`§ When to Use Which § A Table's Construct`](#a-tables-construct) decides which of a Decision Table, a record type's records and a Basic Table the table is. A definition whose need the construct it defines would meet takes a more basic one, as [`§ Defining Constructs`](#defining-constructs) has it. A table's construct is chosen as the table is written. An existing table keeps the construct its declaration gives, and a table declaring none stays a Basic Table, until the user decides to migrate it.

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

- **Decided by one fact?** The rule sends its cases to outcomes by one fact, to at most two of them, the fact's and its otherwise, as a claim paid on approval where its receipt is attached and held otherwise. Such a rule is prose, by the count this section sets. A list naming a set's values, each with what it means, is no rule and answers no.
- **Claimed of every reachable state?** The rule is claimed true in every state the system can reach, whatever was done to reach it and whether or not the system keeps it, or claimed of one operation as it begins or ends. Such a rule is a Constraint, `always`, `before` or `after` ([`§ Constructs § Constraint`](#constraint)). A precondition is one, and a check the system makes of a request answers no, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has them. A stored value claimed equal to what others give is one, a derivation. A value derived on demand, stored nowhere, is no construct's but a Facts record's Derivation where its expression chooses no case. Where its expression picks among cases, it takes a construct the questions after this one choose.
- **An outcome from conditions alone?** The case's conditions alone pick its outcome among several, by no steps of the case's own, with nothing keeping a status between one case and the next, whether or not anything acts on the outcome. Such a case takes a Decision Table ([`§ Constructs § Decision Table`](#decision-table)), and what becomes of a request is one, as [`§ Constructs § Decision Table § A Request Turned Away`](#a-request-turned-away) has it. A condition that takes steps to find is an Algorithm's, and the table tests the Algorithm's result. An outcome that must act, consume a counter or correct a value, is the step of the Algorithm running the table: the table decides, and the step does.
- **Tasks some of which run at once?** The case holds distinct units of work, each named, with what each waits for, some free to run at once, and every task considered on every run. Such a case takes a DAG. [`§ Constructs § DAG`](#dag) tells a DAG from an Algorithm's loop `at once`, from tables chained by Reads, from a process configured as data, and from a process that waits within a task.
- **Steps run in turn?** The case takes steps one after another, which may loop or take one path or another by a condition. Nothing in them waits for an occurrence from outside, and a retry until something holds is a loop stating why it ends. Such a case takes an Algorithm ([`§ Constructs § Algorithm`](#algorithm)). A run that parks until something outside it happens is split: each leg is an Algorithm, and the whole is a State Machine whose states are the legs, resuming where it left off by a fact.
- **Waits for occurrences?** Something keeps a status between occurrences from outside it (an action of an actor, a message, a time or a condition becoming true), and moves when one happens, however few of a machine's parts it needs. Such a case takes a State Machine ([`§ Constructs § State Machine`](#state-machine)). A field that actions set in some states and the system derives in another is such a machine, over the states the actions move between. It has one open state, whose description cites the function fact whose Derivation gives the field there. The states a machine moves between may be the members of a closed set a spec defines, a record type's records or a Basic Table's rows settled apart from the machine. The fact the machine records its state in cites that set ([`§ Constructs § Record Form`](#record-form)).
- **Entries of one kind?** The case is an entry of one kind written again and again into the specs or the working files, each stating the same named fields, or the members of a closed set a spec defines, each saying what it is. It is not the schema of data the product stores. Such a case takes a Record Form ([`§ Constructs § Record Form`](#record-form)). For a table of such entries, [`§ When to Use Which § A Table's Construct`](#a-tables-construct) chooses between a record type's records and a Basic Table.

### A Table's Construct

Which construct a table is, among a Decision Table, a record type's records and a Basic Table, decided by what the table is there for. A table is never prose, even one deciding two outcomes. These questions are asked of every table whose case the questions of [`§ When to Use Which`](#when-to-use-which), by its shape, send to no DAG, Algorithm, State Machine or Constraint. A process or a behavior written as a table takes the construct those questions choose. The author writing a table answers these questions in order, and the first answered yes chooses.

None of these questions is asked of:

- a plain table a definition writes before [`§ Constructs § Basic Table`](#basic-table), the base the constructs start from, which is a Basic Table declaring none of the additions, as [`§ Defining Constructs`](#defining-constructs) has it;
- a table defining FEEL, a Basic Table as [`§ Defining Constructs`](#defining-constructs) has it;
- a record type the canon declares, reached by the skills and their point-of-use citations.

**Construct:** `§ Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** There to decide an outcome?, More than a row declares?

| There to decide an outcome? | More than a row declares? | Construct |
|---|---|---|
| true | - | Decision Table |
| - | true | Record Form |
| - | - | Basic Table |

What each question asks its author:

- **There to decide an outcome?** The table is built so a case can be looked up by the criteria its earlier columns hold and given an outcome, whether or not anything acts on it, as a shipment is given its rate by its zone. A table built so a reader can look up what each item is answers no, as a table of a currency's symbol and its decimal places does. So does a table whose rows sample an open set of cases, since it cannot be checked for a case it leaves out.
- **More than a row declares?** An entry needs a field holding a list or more than one paragraph, values held to a list of allowed values or a test as a record type's Values declares them, a default where the value is absent, uniqueness on its own beside its key, or a natural key too long for a citation naming its entries. Where the natural key is too long, a short identifier is the key and the natural key a field marked Unique. Such entries are a record type's records ([`§ Constructs § Record Form`](#record-form)). It is the line a schema designer draws between a lookup table and an entity with constrained columns. A field an entry may leave blank is no reason, and neither is a value its type alone bounds.
- **Otherwise.** The table is a Basic Table. It declares its natural key where its rows have one, and the columns every row must fill ([`§ Constructs § Basic Table`](#basic-table)).

### A Configured Instance

An instance of a construct implementing [`§ Constructs § Configured Construct`](#configured-construct) may be a configured instance. Its rows, its states and transitions, or its steps are then data the system stores and its users change, held in the facts its `Held In` field names. The tables written are an example instance. The example shows the data's shape and is checked as the data is, and the system never falls back to it. A process whose tasks or their order are data is an Algorithm over that data, as [`§ Constructs § DAG`](#dag) has it.

A configured instance's construct is chosen by its shape, as any other is. These questions are asked of what the data does, never of the data's being stored. A value a rule reads (a setting, a threshold or a record's field) is an input and never structure. Records the system generates from its configuration are an Algorithm's Output, and each is then a run of the construct its shape chooses.

Logic a deployment supplies as code, or chooses among by a setting, is written as its default: an Algorithm run where the logic is used, running a Decision Table where one decides. The logic's contract is a Constraint `before` and `after` the Algorithm ([`§ Constructs § Constraint`](#constraint)), and its section's prose says another may be supplied. A choice among built-in ones by a setting is a Decision Table over the setting, the setting an input.

An instance is checked as it is saved, as the written construct is, and an instance the checks would report is turned away. The section holding the construct says so, since a check made only of the written example is no check of the instances. An instance someone outside the system's authors owns, as a clinic's own form or a tenant's own catalog, is a specification its owner keeps. The system's spec states what every instance obeys.

### Combining Constructs

Constructs are not mutually exclusive inside one spec. A part of one construct hands its work, or the deciding of its case's outcome, to another.

#### Construct Handoff

Where a part's handoff to another construct is written, decided by the part and the work:

**Construct:** `§ Constructs § Decision Table`

**Conditions:** The part, Its work

| The part | Its work | Written |
|---|---|---|
| a State Machine's state | the run of a State Machine | in its description, the words `governed by` and that machine's section cited, as [`§ Constructs § State Machine § A Submachine State`](#a-submachine-state) has it |
| a State Machine's state | "the run of an Algorithm", "the run of a Decision Table", "the run of a DAG" | in its description, that construct's section cited as the state's work |
| a State Machine's transition | "the run of an Algorithm", "the run of a Decision Table" | in its Effect cell, as [`§ Constructs § State Machine § What It Means`](#what-it-means-1) has an effect |
| a DAG's task | "the run of an Algorithm", "the run of a Decision Table", "the run of a DAG" | in its work cell, as [`§ Constructs § DAG`](#dag) has it |
| an Algorithm's step | "the run of an Algorithm", "the run of a Decision Table" | as a run, `Run` and the citation with its bindings, as [`§ Constructs § Algorithm`](#algorithm) has it |
| an Algorithm's step going back or recurring | the Constraint its end rests on | in its Terminates cell, as [`§ Constructs § Algorithm`](#algorithm) has it |
| a Decision Table | another table's outcome, read as a condition | as a Reads item, as [`§ Constructs § Decision Table`](#decision-table) has it |
| a Decision Table's computed outcome | a walk whose order changes it | the section of the Algorithm doing the walk cited in the cell, as [`§ Constructs § Decision Table`](#decision-table) has an outcome computed by a walk |

The citation says what the part does, and the part stays what its own construct makes it. A part of another construct being reached is a trigger, as a claim moves from under review to approved when a process's approval step is reached, where that process runs apart from the claim ([`§ Constructs § State Machine § What It Means`](#what-it-means-1), [`§ Constructs § State Machine § A Submachine State`](#a-submachine-state)). A Decision Table's choice among the moves a request may make reaches the machine as the fact the table gives, and the transition's guard tests that fact. An Algorithm cutting, ranking or reducing a table's hits runs the table under a policy taking every row a case matches, then works on the hits in the steps after. An Algorithm applying a table again to the input it altered is a loop stating why it ends. Where an Algorithm runs on successive parts of one quantity, a Constraint states what the parts' results owe the whole's. The step carrying one part's end into the next enforces that Constraint. A Constraint may bound what any construct produces ([`§ Constructs § Constraint`](#constraint)).

In an expense approval process, the step that routes a claim is a Decision Table over independent conditions: the claim's amount band, its category, and whether a receipt is attached. The step that works out the reimbursable total is an Algorithm: it sums the line items, applies each category's own cap, and deducts any advance already paid. A Constraint holds that the total is never negative, however far the caps and the advance deduction reduce it, enforced by that Algorithm's own step flooring the total at zero rather than left as an expectation. Use as many constructs as a spec needs, and never force one to do a job another is built for.

## Diagrams

A diagram is a materialized view of a fact. It is for a human reader, technical or not, who wants the shape of something before deciding whether to read the mechanism behind it. Like a materialized view, a diagram is precomputed for whoever consumes it and is never itself the source of truth. A diagram disagreeing with what it was rendered from is wrong, as a materialized view disagreeing with its tables is a bug rather than a second valid answer. An agent reads the construct behind a diagram with ease; many human readers do not. Nothing tells an author which reader will arrive, so a diagram is written for the human, and an agent benefits as well.

**Where it goes.** A diagram goes wherever it helps its reader most: beside the main section it renders, or above all the sections it renders, as an overview's diagram sits above its detail files. Where it goes is a judgment about the reader; its form is not.

**Form, wherever it goes.** A diagram has a heading of its own, directly followed by the diagram, then the diagram's fields ([`§ Fields`](#fields)) in the order of this table of fields ([`§ Constructs § Construct`](#construct)):

| Field | Required | Default Value | Values | Holds |
|---|---|---|---|---|
| Caption | yes | | text | what the diagram shows, in prose |
| Sources | yes | | text | a list, a citation of the home of each fact the diagram draws |

Nothing else is in the diagram's section, and its shape is the same wherever it appears, as a Decision Table's is. The caption carries no citation, so every citation the diagram rests on has one place. The Sources field's key stands on a line of its own. Its bullets are sorted in plain character order, so the order is mechanical and a script can check it. That order places same-file citations after cross-file ones. A diagram is authored as a Mermaid flowchart ([`specs/methodology/external-references.md § External References [Name: Mermaid]`](/specs/methodology/external-references.md#external-references)) and checked in as source rather than as an image, so it renders in plain text and diffs like everything else here. It is a flowchart even where a state diagram or sequence notation would be the more formal rendering, since one grammar across every diagram in this repo, boxes and arrows, is worth more to the readers diagrams exist for than notational precision on any single one. Authoring, rendering or changing a diagram follows `.ai/skills/author-mermaid-diagram/`.

**What it may show.** A diagram shows only what its host file's content, the file's prose or its tables, already names. What stands behind a diagram is often far more granular, such as a State Machine's every state or an Algorithm's every step, and that granularity stays where it is. Check each label against the host file before adding or editing a diagram. A name, step, or distinction the host file never states is either collapsed out of the diagram or, if it belongs at that altitude, stated in the host file first and only then rendered. Choosing between them is a judgment about the host file's completeness, not about the picture. The bound falls on the diagram and not on a table beside it, because a table can carry a citation in every cell and stays checkable however specific it gets. A rendering that descended into detail its host never states would show a reader things the text around it never explains.

**A diagram and its sources cite each other.**

- **The diagram lists its sources.** The Sources field cites the home of everything the diagram draws, a box, an arrow, or a label on either, in the same file or another. Each is cited at that fact's single home ([`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact)), at the most specific section or record whose own text states it: a child section rather than its parent where the child states it, and never a test scenario. A box naming a grouping draws the grouping, not its members, unless the diagram names them too. A summary restating a fact, an overview's included, is a materialized view of that home just as the diagram is, so it is not a source. A section stating something found nowhere else, as an overview's connecting prose can, is that fact's home, and it is a source. Together the citations are as specific as they can be without leaving out anything the diagram uses. The list lets a reader go deeper. Nothing on the picture can carry a citation of its own, so the list is the way from the picture to the checkable detail. The more specific each citation, the less a reader wades through to find what a box stands for. The list also lets the diagram be checked: an agent confirming that the picture represents its sources correctly reads exactly what the diagram draws on, and nothing it does not.
- **Each source cites the diagram back.** Every listed section cites the diagram's heading in its own text, not in a section nested inside it, in a sentence such as "`<the diagram's heading>` renders this." A record section, or a record, listed among a diagram's Sources cites the diagram in the record section's `**Diagrams:**` field instead ([`§ Constructs § Record Form`](#record-form)). The citation back keeps the diagram in sync. Whoever edits a source is the reader who must re-check the diagram, and the citation in the source names the diagram to them.

A section may be listed only where it may cite the diagram's file and be cited by it, per [`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed). So a diagram draws a fact only from a section able to name it back: a technical diagram draws a product fact from the technical section stating how the fact is made true, never from the product file.

A diagram's heading is an ordinary heading, citable like any other, per [`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation), and any file may cite it to point a reader at it. It is never cited as the source of a fact: a citation asserting something is true names the prose or construct the diagram renders, never the rendering.
