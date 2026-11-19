## External Reference

The canon adopts an outside standard where an agent or a software engineer already knows it from training or experience, so a form or a meaning the canon relies on reads without the canon teaching it. A standard is registered where a rule adopts it, or maps the rule's own forms onto it, for something an author writes or an agent reads by. It is registered once, as a record of this type in [`specs/methodology/external-references.md § External References`](/specs/methodology/external-references.md#external-references). The record pins the standard to the version or revision the canon relies on, so what the canon means holds still as the standard moves on, and an author reaching for the name finds the one text it means.

**What is not registered.** A digest or an encoding a script computes, as SHA-256 and UTF-8, is named in the rule using it. A convention no one publishes is defined in the canon, as kebab-case is once ([`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion)). A standard a registered one adopts in turn, as GFM extends CommonMark, is covered by the registered standard's record. A tool or a product is not registered where a rule names it only as an example of what one of the rule's forms maps onto.

**Citing it.** The section whose rule adopts a registered standard, or maps onto it, cites the standard's record where it first names the standard. It states no version or link of its own, so the record is the one home of both ([`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact)). A section using that rule's forms relies on the rule. Where it needs a citation, it cites the rule's section, not the record. The section whose rule adopts or maps onto the standard maps each departure from it as [`§ External Reference § A Mapping onto a Standard`](#a-mapping-onto-a-standard) has it, since the standard's own text cannot tell a reader that. Where the standard's text is free to read, the standard is cited for the rest, and for what the section's forms mean where the section is silent. Where it is paid, the section states in its own words everything the canon relies on, quoting none of the standard's text, and cites the standard's record alone, so a reader recognizes it by the name and version the record gives. A paid standard the canon relies on as a lookup, a dictionary or a code list, is cited for its entries, which a reader looks up, its text never quoted. Everything the canon means is then readable in the repository or in a free standard, by a person and an agent alike. A section naming an element of a registered standard writes it in the standard's own casing and terms. A mention of one of the standard's classes writes the class's name, as CallBehaviorAction. A property, or a concept the standard describes only in prose, is written in the standard's own words, as run-to-completion. An agent or an engineer then recognizes it, and finds it in the standard verbatim.

**Moving a version.** Relying on another version of a standard, or on more of it than its record covers, is a change to the canon. That change updates the record, each section citing it, and the checks of what those sections state, together. Its departures are judged again as [`§ External Reference § A Mapping onto a Standard`](#a-mapping-onto-a-standard) has them, and a part the new version adds is taken as any need is, as [`§ External Reference § Which Form a Need Takes`](#which-form-a-need-takes) has it.

External Reference is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), whose records give these fields, in this order:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** External References \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the standard's short name, as its readers know it |
| Title | no | yes | | text | its full title, and who publishes or stewards it |
| Version | no | yes | | text | the version relied on, or, for a standard publishing none, the revision relied on, named by its date |
| URL | no | yes | | text | a link to the text of that version or revision, never to whatever is current, written as literal text |
| Access | no | yes | | "free", "paid" | whether the text at its URL is free to read: `free`, anyone reading it at no charge, or `paid`, the text sold, its URL the publisher's page for the version, or a library's record of it where the publisher sells the version no longer |
| Relation | no | yes | | "adopts", "maps onto" | how the canon relies on the standard as a whole: `adopts`, the canon's forms being the standard's own, its departures aside, as UML's are; or `maps onto`, the canon's forms being its own, each standing for one of the standard's, as a key's path stands for JSONPath's dot notation |
| Covers | no | yes | | text | the part of the standard the canon relies on |

### Which Form a Need Takes

A need a form meets takes a standard's form before one of the canon's own, as [`specs/methodology/modeling-constructs.md § Purpose`](/specs/methodology/modeling-constructs.md#purpose) has the constructs lean on the industry's standards. A standard fits a need where its form states what the need decides. The field a need comes from is the domain whose engineers meet it, as scheduling is for a job's run. A product's convention counts where the product is widely used in that field and its documentation publishes the convention, its record pinning a release and linking to that release's documentation. Of several that fit on one row, the one most used in the field is taken. A standard whose form cannot state what the need decides does not fit, however widely used: cron's five fields name no month's last day, so a schedule needing one takes RFC 5545's recurrence rule:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** a registered standard fits?, a published standard fits?, a product's convention fits?

| a registered standard fits? | a published standard fits? | a product's convention fits? | Form |
|---|---|---|---|
| true | - | - | the registered standard's, adopted or mapped onto as its record's Relation has it |
| - | true | - | the published standard's, the standard registered |
| - | - | true | the convention's, its product registered as its standard |
| - | - | - | the canon's own, made as [`specs/methodology/modeling-constructs.md § Purpose`](/specs/methodology/modeling-constructs.md#purpose) has the set extended |

A need whose parts fit different standards takes each part's form by its own row, as a job's recurrence and its policy for a missed run may. A need FEEL's built-in functions do not meet takes a function of the canon's own, its body FEEL, as [`specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions`](/specs/methodology/expressions.md#the-canons-functions) has one written. A standard whose text is paid fits as a free one does, relied on as [`§ External Reference`](#external-reference) has a paid standard cited.

### A Mapping onto a Standard

**When a mapping is owed.** A registered standard has a mapping wherever the canon writes one of its elements otherwise than the standard does: departing from it, leaving it unwritten where the canon's forms meet it, or writing a form of the canon's own in its place. A standard the canon writes nowhere otherwise owes none. A narrowing that stays inside the standard's own form, taking part of what the standard allows so that all the canon writes is still the standard's, is no departure. Such a narrowing is shown by the record's Covers, as RFC 3339's covers a date and time in UTC.

**Its Relation.** A standard's record says once, by its Relation field, how the canon relies on the standard as a whole, as [`§ External Reference`](#external-reference) defines the field. Under either Relation, each departure is a row of its mapping.

**Its table.** A mapping is one table, in the section whose rule adopts or maps onto the standard, after that section's prose on what the mapping means. A standard several sections depart from has a table in each, each mapping that section's forms. A section of `modeling-constructs.md` that comes before [`specs/methodology/modeling-constructs.md § Constructs § Basic Table`](/specs/methodology/modeling-constructs.md#basic-table) writes no Basic Table, since a table declaring an addition comes after that section ([`specs/methodology/modeling-constructs.md § Defining Constructs`](/specs/methodology/modeling-constructs.md#defining-constructs)). Its mapping's rows are held in the table of the section whose rule adopts the standard for the whole canon, and the section cites them, as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) cites GFM Elements. The table maps each element the section's forms write otherwise than the standard does; an element the canon writes the same takes a row where the canon names it its own way, so a reader finds the standard's term for it. Its Table Name is the standard's Name and the word `Elements`, as `UML Elements`. Its Reference Key is the standard's Name, and its Required is `Section, Treatment`. Its columns, in this order:

| Column | Holds |
|---|---|
| the standard's Name | the element, in the standard's own casing and terms |
| Section | the standard's clause or clauses holding the element, or, for a product's convention, the type, message or setting its documentation defines the element in |
| Treatment | `the same`, `differs:` or `not written`, then what the canon writes for the element, where its forms write it |
| Departs For | where the Treatment differs or is not written, the kind of its reason: `the standard's gap`, `the canon's form` or `no need yet`, or two of them in that order, where the reason holds two kinds; empty where it is the same |
| Why | where the Treatment differs or is not written, why the departure was needed: what the standard leaves the canon lacking, what the canon's way of writing a spec requires, or that no spec needs the part; empty where it is the same |

**A departure's one home.** That an element departs, and why, is stated in its row alone. A section's prose states the canon's rule for the element, and a sentence naming the rule a departure cites the row and gives no reason of its own, as [`specs/methodology/modeling-constructs.md § Time`](/specs/methodology/modeling-constructs.md#time) cites [`specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means [UML Elements.UML: TimeEvent]`](/specs/methodology/modeling-constructs.md#what-it-means-1). The script check of such a sentence reads the methodology's files, a document laid out as a folder's files among them, since they hold every mapping, and reads no other file. A departure with no reason is not made.

**Deliberate.** A reader applies a departure as the canon's rule, never as an error to bring back to the standard, and it changes only by its reason judged again. Its Departs For says which reason it is. `the standard's gap`: the standard lacks what the canon needs, which a later version or another standard may supply. `the canon's form`: the departure follows from how the canon writes a spec, as a table wiring no pins does, which no standard's version changes. `no need yet`: no spec here needs the part, which a need arising changes.

**Judged again.** Whenever the canon moves a registered standard's version, or registers a standard, each row whose Departs For holds `the standard's gap` is judged again against that standard. Where it now supplies what the row's Why says the canon needed, the departure is dropped and that standard's form taken, as [`§ External Reference § Which Form a Need Takes`](#which-form-a-need-takes) has a need's form chosen. The judgment of each row is recorded in the design that moves or registers the standard.
