## One Home Per Fact

Every rule, definition, or design principle that could matter in more than one place has exactly one home: the file whose subject matter it most specifically belongs to. Every other place that needs it cites that home rather than restating it in its own words.

**Citing a rule where it applies.** A place applying another file's rule, definition or principle gives it a point-of-use citation. It may add what only that place can say: how the rule applies there, and why it matters there. Clean-as-you-go is one principle in a home garage, a commercial kitchen and a medical facility. What it asks of the hands, and what hangs on it, differ in each. An agent meets the rule where it acts, so the citing place states the application wherever an agent reading only that place would apply the rule wrongly. It states the reason wherever that agent would not see why the rule matters there. Where neither holds, a bare citation is enough.

**Each step carries the citation.** The citation belongs to each step applying the rule, so the rule is in mind when the work is done rather than left to an earlier reading. A playbook's steps link to the detailed procedures they carry out in the same way. A step carried out from a playbook entry or a table row that cites the rule has the citation there already. An index that only routes to rules stands in for no step's citation.

**What a citing place never adds.** A citing place never re-derives or re-explains the rule, and never adds a rule of its own about the cited subject. That would make a second home with a citation attached. A duty that would hold wherever the rule applies belongs in the rule's home. A duty that holds only because of the citing place's own subject is that place's application of the rule.

Before adding a paragraph that states a general rule, check whether that rule already has a home. If it does, cite it as this section describes. If not, place it deliberately, never in the file that happened to need it first, so the next place that needs it can cite it rather than restate it. A rule several files use and none owns has its home in the narrowest file covering every use, since a home above every use overstates how far the rule reaches.

**Why the discipline is strict.** Two correct copies of a rule read identically on the day they are written. They diverge later, when one is edited and the other is not. Nothing about reading either copy reveals that the other exists.

**Pointers may repeat.** Several files may cite the same home. One home exists so that many places can cite it.

### One Rule to a Sentence

A sentence stating a rule at the rule's home states part of at most one rule, a rule as [`specs/methodology/glossary.md`](/specs/methodology/glossary.md) defines it. A change to one rule then edits no sentence stating another. A table cell and a list item are each a sentence, judged on its own, and so is each further sentence within one. A clause applying another section's rule, with its citation, is not a second rule. A reason is no rule. A sentence a careful reader could count either way meets the rule. A sentence holding several rules is split as [`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose) directs, its rules counted as [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which) counts them.

**Examples.** Each is judged by the questions it answers.

- "An approved claim is paid where its receipt is attached, and held otherwise." is one rule. It answers what becomes of an approved claim.
- "An approved claim is paid where its receipt is attached. Where its receipt is missing, the claim is held." is one rule in two sentences.
- "An approved claim is paid within ten days, by bank transfer, to the claimant's account." is three rules. They answer when, how and to whom it is paid. Written one rule to an item, it reads:
  - "An approved claim is paid within ten days."
  - "An approved claim is paid by bank transfer."
  - "An approved claim is paid to the claimant's account."
- "An approved claim is paid where its receipt is attached and held otherwise, and its receipt is kept for seven years." is two rules. It answers what becomes of an approved claim and how long a receipt is kept. Split, it reads: "An approved claim is paid where its receipt is attached, and held otherwise. Its receipt is kept for seven years."

## A Definition and Its Instances

A form, whether a construct or a record type, is defined once, at one home. Each use of the form is an instance, setting only the values its definition allows. Nothing is defined at the point of use. An object sets the properties its class defines in the same way. This is [`§ One Home Per Fact`](#one-home-per-fact) applied to forms. It is also DRY as Andrew Hunt and David Thomas first wrote it, in "The Pragmatic Programmer": every piece of knowledge has one authoritative representation.

**Knowledge, not shape.** What one definition holds is one piece of knowledge, whatever shape each use takes. A shape is one chosen view of the knowledge, and it decides nothing. The same knowledge in several shapes keeps one home, and the other shapes are kept in sync with it, as [`§ Keeping Specs in Sync`](#keeping-specs-in-sync) keeps them. Different knowledge sharing a shape keeps separate definitions, so each changes on its own. Sharing a definition between two things that only look alike couples them, and the first change to one breaks the other. As Sandi Metz has it, duplication is far cheaper than the wrong abstraction.

**Choosing how related things are defined.** Related things are defined by whether a change to one must reach the other. Where every change must, they are one definition, and each use is an instance of it. Where only some must, a base definition holds what they share, and each is a sub-definition of it. A sub-definition holds everything its base holds and more, never less, as a subclass extends its class. Where no change need reach the other, they keep separate definitions, however alike they look. A form is never typed by its looks, the way duck typing types an object. A use that leaves some of a definition's parts unused, its optional parts among them, is an instance of that definition, never a definition of its own. A sub-definition is earned by what it adds. An application's technical specs choose the same way: one service or class, a base and its specializations, or separate ones.

**A citation as composition.** A point-of-use citation is composition by reference. The rule it cites applies where it is cited, as if written there. The citation names the rule at the place it applies, and brings no structure of its own. So two citations never bring rival versions of one fact ([`§ One Home Per Fact`](#one-home-per-fact)), as two mixins can. A definition implementing an interface does so by such a citation: its Implements field ([`specs/methodology/modeling-constructs.md § Defining Constructs § Interfaces and Members`](/specs/methodology/modeling-constructs.md#interfaces-and-members)), which the audit checks.

## Which Citations Are Allowed

The specifications are layered by what governs what:

```
specs/AGENTS.md
  └ specs/methodology/
      └ specs/application/
          └ product/
              └ technical/
```

The rules of [`specs/AGENTS.md`](/specs/AGENTS.md) and of the methodology reach the files in Spec of Record's scope, as [`specs/methodology/scope.md § What Spec of Record Governs`](/specs/methodology/scope.md#what-spec-of-record-governs) sets. A product spec states what a user can rely on, and a technical spec states how it is made true ([`specs/methodology/spec-placement.md § Product or Technical`](/specs/methodology/spec-placement.md#product-or-technical)).

A citation pointing down a layer sends the reader somewhere for a specific purpose. A citation pointing up a layer gives background that benefits the local text.

What a citation may name depends on where it is written. Each row its source matches grants what that row lists:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Order:** any

**Hit Policy:** Collect

**Conditions:** From

| From | May cite |
|---|---|
| A product spec | another product spec |
| A technical spec | another technical spec, a product spec |
| A methodology spec | another methodology spec; [`specs/AGENTS.md`](/specs/AGENTS.md); [`specs/architecture.md`](/specs/architecture.md); the skills' directory, a registered skill or a file of one, and the code the skills share, naming what applies its rules |
| [`specs/AGENTS.md`](/specs/AGENTS.md) | any spec; a registered skill or a file of one |
| [`specs/architecture.md`](/specs/architecture.md) | [`specs/AGENTS.md`](/specs/AGENTS.md); any spec; a registered skill or a file of one |
| "A product spec", "A technical spec", "A methodology spec" | the project's root `AGENTS.md` as a whole file, never a section of it |
| A `**Construct:**` field, in any spec | the section defining the construct its instance is of, wherever it sits |
| Code the application specs govern | a product spec, a technical spec, or a section of one, never a record, naming what it carries out or checks with an app-spec annotation ([`§ Writing a Citation § Citing From Code`](#citing-from-code)) |
| A registered skill's script, or the code the skills share | [`specs/AGENTS.md`](/specs/AGENTS.md) or a methodology spec, or a section of one, naming where a copy it holds takes its values from with a canon-spec annotation ([`§ Writing a Citation § Citing From Code`](#citing-from-code)) |

Code is governed by the specs rather than being a layer of them. The table is the whole permission for citations from these specs, from code, from the skills' scripts, and from [`specs/AGENTS.md`](/specs/AGENTS.md) and [`specs/architecture.md`](/specs/architecture.md). Files outside that set, the project's own root `AGENTS.md` among them, cite these specs under their own rules. The root `AGENTS.md` holds the project's instructions rather than the methodology's. No spec other than [`specs/methodology/working-files.md`](/specs/methodology/working-files.md) names a working file ([`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files)). No working file is committed, so its name would point a reader at nothing. [`specs/AGENTS.md`](/specs/AGENTS.md) is agent instructions rather than a spec, and it names the working files its procedures act on.

A product spec citing a technical spec would make a promise depend on its own implementation. The `technical-specs` front matter key serves that direction instead ([`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement.md#naming-the-technical-files-behind-a-capability)). The key is file-level and coarse by design, so it cannot carry a dependency at heading precision. A methodology spec citing an application spec would make a rule depend on the document it governs.

An application spec cites no methodology spec, and neither [`specs/AGENTS.md`](/specs/AGENTS.md) nor [`specs/architecture.md`](/specs/architecture.md). The reason is subject, not direction, since such a citation would point up. An application spec's subject is the product, and how a spec is authored is no part of it. So a reader of the product has no use for the authoring rule behind a sentence. An application spec may still name a construct, because a construct is what its own content is authored as. Its Construct field cites the construct's definition, since the definition is what the instance is held to ([`specs/methodology/modeling-constructs.md § Defining Constructs § References and Names`](/specs/methodology/modeling-constructs.md#references-and-names)). That field is the one citation of the methodology an application spec makes. An application spec does not reach into the methodology, [`specs/AGENTS.md`](/specs/AGENTS.md) or [`specs/architecture.md`](/specs/architecture.md) for their own claims. [`specs/AGENTS.md`](/specs/AGENTS.md) holds the methodology's own rules, and [`specs/architecture.md`](/specs/architecture.md) describes how the methodology lays the specifications out.

## Titling a Heading

A heading's title is a stable slug for whatever the section covers, not prose to be refined later. Every citation depends on that exact text. A title chosen well the first time keeps a citation from ever needing to change. If a title does change, every citation naming it is updated in the same edit. A citation left naming the old title is broken until it is updated.

**Reference Key:** Rule

**Required:** Form

| Rule | Form |
|---|---|
| No `§` in the heading itself | `## Vision`, never `## § Vision` |
| No `[` in the heading itself, which opens a part's key, in a citation | `## Session Timeout`, never `## Session Timeout [draft]` |
| Unique among headings sharing its parent, a top-level heading's parent being its file | two headings under different parents may share a title |

A numbered heading, or one counting its children, is the heading case of [`specs/methodology/spec-style.md § Ordinals and Counts`](/specs/methodology/spec-style.md#ordinals-and-counts). A heading pays for a number twice, since its title is also the text of every citation naming it. Renumbering sections, or retitling one whose count went stale, changes those citations as well.

**Bold lead-ins are not headings.** A bold lead-in ([`specs/methodology/spec-style.md § Bold Lead-ins`](/specs/methodology/spec-style.md#bold-lead-ins)) has none of the guarantees a heading carries, starting with enforced uniqueness. It has no citation form either ([`§ Writing a Citation`](#writing-a-citation)). So a paragraph that is, or needs to be, a citation's target is authored as a child heading instead. The child heading gets every rule this section sets, and needs no workaround. Entries that exist to be cited are records instead ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)).

## Writing a Citation

A citation must let a cold reader follow it without guessing and without reopening files to re-derive the location. At the citation's target, the reader must find what the citer attributes to it.

The token for referencing a section is `§`. A space follows it, and a space precedes it wherever a path or a parent title comes before it. Each form this section gives is written inside a single backtick span, never split across spans and never left as bare prose:

```
A section in the same file           § Title
A nested section in the same file    § Parent § Child
A part of a keyed instance           § Section [Key: value]
A part in another file               path/from/root.md § Section [Key: value; Key: value]
A section in another file            path/from/root.md § Parent § Child
A whole file                         path/from/root.md
An index.md                          never a citation target
```

A cross-file citation gives the path from the project root, exactly as it would be written anywhere else, never a directory-relative path. A same-file citation omits the path entirely and starts at the section token.

A section is named by its full lineage of heading titles, one segment per level from the top of the file down to the target. A level-1 heading is the file's own title rather than a section, so a lineage starts below it. A top-level section is one segment on its own. A child heading is guaranteed unique only within its own parent's scope, so its citation carries every ancestor's title down to it. The `§` sign comes from statute citation, which walks a hierarchy from a title down to a subsection, as `42 U.S.C. § 1983(a)(2)` does.

A part of an instance of a construct implementing Keyed Construct ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)) is a record, a row of a Basic Table or a part of a construct. Such a part is named by the citation of the section holding its parts: a construct's section, a Basic Table's or a record section. A space follows, then the part's key values in square brackets inside the same span, like a query parameter selecting one part from the section. Each pair is written `Key: value`, in the order the Reference Key gives them, and the pairs are separated by a semicolon and a space. For example, `[Name: Session Timeout]` follows an `Open Questions` section's citation, and `[Country: Canada; Tax Year: 2025]` names a key of two fields. `[States.State: open]` names a part of a table its `**Table Name:**` names, a State Machine's or a Basic Table's, by the path the table's name and its key make, as [`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct) has a key written as a path. A value a citation names holds no semicolon ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)), so the pairs are split at `; `. Each value is compared with the part's value after trimming the space around it. It must match exactly, as a title does, markup and all. A citation naming a value that holds a backtick opens and closes its span with one more backtick than the longest run in the value, so the value stands in the span verbatim. GitHub Flavored Markdown writes a code span holding backticks the same way.

**Where a citation sits.** A citation supporting a claim closes the clause it supports, or stands in a sentence of its own, so the reader meets the claim before its source. A sentence making several claims, each with its citation, is split into a sentence for each claim. A citation glossing a term stands just after the term, in parentheses, as "the design frame ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md))" does. A citation used as a name, the subject of its clause, as in "[`specs/methodology/spec-style.md § Emphasis`](/specs/methodology/spec-style.md#emphasis) sets the form of emphasis", stays where it is.

**What cannot be cited.** Of the content that is not a heading, only a part of a keyed instance has a form for citing it. A bold lead-in has none. [`§ Titling a Heading`](#titling-a-heading) says when such content becomes a heading. A directory's `index.md` carries no heading lineage of its own.

**A title that names a kind of section rather than one particular section.** It resolves to no single heading anywhere, so it is not a citation and takes no `§`. A rule referring to `Test Scenarios` generally, where the level varies by context, names a kind. A rule referring to one file's own `## Glossary` names a section.

**A file name that names a kind of file rather than one particular file.** It names whatever file plays that part, in any directory or project the rule reaches, rather than the one file at a path. So it is not a citation. It is written as the bare file name, without a path. Where it matters whose file it is, the name is qualified by its owner, as in the product specs' `architecture.md`. A rule referring to any directory's `architecture.md` names a kind, and [`specs/methodology/architecture.md`](/specs/methodology/architecture.md) names one file.

### Referring to Other Text

Other text is cited, never pointed at by direction. A sentence referring to text elsewhere, whether a section, a table, a step or a rule, names it by citation or by containment. Where no citation is allowed there, the sentence names the text by name. It never points at the text as "above", "below", "the next step" or "the preceding table".

A direction holds only while nothing moves. Reorder steps, insert a section or move a table, and every direction pointing across the change silently points at the wrong text. A citation follows its heading wherever the heading moves under the same parent. Once the heading moves elsewhere or is retitled, the citation fails loudly, and the audit script reports it. A spec written with directions leaves that trap for whoever edits it next. A spec written with citations can be reordered freely. Text worth referring to sits in a section of its own. Where it does not, it is given a heading before it is cited ([`§ Titling a Heading`](#titling-a-heading)).

#### Direction Wordings

Whether a wording is a direction:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** Wording

**Annotations:** Why, Such As

| Wording | A direction | Why | Such As |
|---|---|---|---|
| containment, naming what a section or file containing the text holds | no | text moved within what it names stays within it | "this section's life cycle", "this Workflow's steps" |
| a word whose subject is where something sits | no | it sends the reader to no text | a heading one level below another, a node drawn above the flow |
| a sentence introducing the block directly under it: a table, a list, a code block or a construct | no | its place joins the two | |
| any other word sending the reader to other text, however it is phrased | yes | it holds only while nothing moves | |

A sentence introducing the block under it says what the block is for, never where it is. Wordings such as "the following Algorithm" and "these parts" are dropped. Nothing goes between such a sentence and its block, since the reader would hear one thing introduced and see another. Text that must introduce something further away is not such a sentence. The content it introduces is given a section of its own and cited.

### Citing From Code

Code names a spec it relies on with a spec annotation. A spec annotation is a plain comment on a line of its own, in the comment syntax of the code's language, and never a documentation comment. It holds a tag, a space, and a citation. The citation takes the form [`§ Writing a Citation`](#writing-a-citation) gives for a section in another file or for a whole file. It drops the backticks a citation takes in a spec, since the tag marks where the citation begins and the line marks where it ends. Each tag has a rule of its own saying what carries the tag, and [`§ Which Citations Are Allowed`](#which-citations-are-allowed) says what each tag may cite:

- `@app-spec`, in the code the application specs govern, as [`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code) has it;
- `@canon-spec`, in a registered skill's scripts and the code the skills share, as [`specs/methodology/skills.md § Authoring a Skill`](/specs/methodology/skills.md#authoring-a-skill) has it.

```
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct
```

In a language with block comments only, each annotation is a block comment of its own on one line, and its citation ends before the closer. A heading holding that language's comment closer cannot be cited from code in that language.

**A list, one line per citation, sorted.** A unit or a copy may answer to several specs, a product promise and the technical section making it true among them. It carries an annotation for each, on consecutive lines. The annotations are sorted in plain character order of the citation, so the list has one order whoever writes it, and two changes to it collide less often. One citation to a line keeps each citation readable and makes its change a line of its own in a diff. It also leaves a heading free to hold any punctuation.

**Why it is a citation.** An annotation makes the link one spec makes to another, so it is held to the same guarantee. It names a file, and a heading, that exist. A heading retitled updates every annotation naming it in the same edit, per [`§ Titling a Heading`](#titling-a-heading). The annotation is kept in the code it describes, so it moves with that code through every refactor. A map kept in a file of its own would drift.

**A comment, not a language's own annotation.** A spec annotation is a comment. It is not a Java annotation, a C# attribute or a decorator, so it compiles the same in every language and needs no tool to know it.

### A Citation's Link

A citation in a file a person reads on GitHub is also a link the reader can follow. Those files are `README.md`, the files under `docs/`, and every spec but [`specs/AGENTS.md`](/specs/AGENTS.md). Agents read the skills and the `AGENTS.md` files, so their citations carry no link. The citation itself is the link's text:

```markdown
[`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`](/specs/methodology/sourcing-and-citation.md#referring-to-other-text)
```

The citation identifies, and the link navigates. GitHub addresses a heading by a flat anchor, which loses the heading's lineage. So the citation stays the exact reference, and the link reaches the closest place GitHub can address. Where the two disagree, the citation is right.

**Reference Key:** Citation

**Required:** Link Target

| Citation | Link Target |
|---|---|
| a section in another file | the path from the repository's root, then the cited heading's anchor: `/path#anchor` |
| a section in the same file | the cited heading's anchor: `#anchor` |
| a part of a keyed instance, a record or a row | the anchor of the section holding it, the citation's key naming the part |
| a whole file, named by its path from the repository's root, a directory among it | that path: `/path` |
| a Construct, an Extends or an Implements field's value | no link, since the value declares what a definition or an instance is |

A heading's anchor follows GitHub's convention, which GitHub Flavored Markdown does not define ([`specs/methodology/external-references.md § External References [Name: GFM]`](/specs/methodology/external-references.md#external-references)). The title is written in lowercase. Every character but a letter, a digit, a space, a hyphen or an underscore is dropped, and each space becomes a hyphen. A title met again in the same file takes `-1`, `-2` and so on, in the order the headings stand. A citation is resolved to its one heading by its lineage first, so its link reaches that heading even where titles repeat. A link reaches only a file GitHub serves, one version control tracks. It never reaches an `index.md`, which nothing cites. A bare file name is no citation and carries no link, as in an `index.md`'s row naming a file beside it, or in words naming a kind of file.

**Written by a script, never by an author.** An author writes only the citation. The `--refresh-links` option of `.ai/skills/design-specs/` writes and refreshes every link, and a design's apply runs it once the text its steps call for is written. Every script reading a citation sets its link aside first. `.ai/skills/audit-specs/` reports a citation missing its link, a link not reaching what its citation resolves to, and a link where none belongs.

## External Reference

The canon adopts an outside standard where an agent or a software engineer already knows it from training or experience, so a form or a meaning the canon relies on reads without the canon teaching it. A standard is registered where a rule adopts it, or maps the rule's own forms onto it, for something an author writes or an agent reads by. It is registered once, as a record of this type in [`specs/methodology/external-references.md § External References`](/specs/methodology/external-references.md#external-references). The record pins the standard to the version or revision the canon relies on, so what the canon means holds still as the standard moves on, and an author reaching for the name finds the one text it means.

**What is not registered.** A digest or an encoding a script computes, as SHA-256 and UTF-8, is named in the rule using it. A convention no one publishes, as kebab-case, is defined where it is used. A standard a registered one adopts in turn, as GFM extends CommonMark, is covered by the registered standard's record. A tool or a product is not registered where a rule names it only as an example of what one of the rule's forms maps onto.

**Citing it.** The section whose rule adopts a registered standard, or maps onto it, cites the standard's record where it first names the standard. It states no version or link of its own, so the record is the one home of both ([`§ One Home Per Fact`](#one-home-per-fact)). A section using that rule's forms relies on the rule. Where it needs a citation, it cites the rule's section, not the record. The section whose rule adopts or maps onto the standard maps each departure from it as [`§ External Reference § A Mapping onto a Standard`](#a-mapping-onto-a-standard) has it, since the standard's own text cannot tell a reader that. Where the standard's text is free to read, the standard is cited for the rest, and for what the section's forms mean where the section is silent. Where it is paid, the section states in its own words everything the canon relies on, quoting none of the standard's text, and cites the standard's record alone, so a reader recognizes it by the name and version the record gives. A paid standard the canon relies on as a lookup, a dictionary or a code list, is cited for its entries, which a reader looks up, its text never quoted. Everything the canon means is then readable in the repository or in a free standard, by a person and an agent alike. A section naming an element of a registered standard writes it in the standard's own casing and terms. A mention of one of the standard's classes writes the class's name, as CallBehaviorAction. A property, or a concept the standard describes only in prose, is written in the standard's own words, as run-to-completion. An agent or an engineer then recognizes it, and finds it in the standard verbatim.

**Moving a version.** Relying on another version of a standard, or on more of it than its record covers, is a change to the canon. That change updates the record, each section citing it, and the checks of what those sections state, together. Its departures are judged again as [`§ External Reference § A Mapping onto a Standard`](#a-mapping-onto-a-standard) has them, and a part the new version adds is taken as any need is, as [`§ External Reference § Which Form a Need Takes`](#which-form-a-need-takes) has it.

External Reference is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), whose records give these fields, in this order:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** External References

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

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

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

**Its table.** A mapping is one table, in the section whose rule adopts or maps onto the standard, after that section's prose on what the mapping means. A standard several sections depart from has a table in each, each mapping that section's forms. The table maps each element the section's forms write otherwise than the standard does; an element the canon writes the same takes a row where the canon names it its own way, so a reader finds the standard's term for it. Its Table Name is the standard's Name and the word `Elements`, as `UML Elements`. Its Reference Key is the standard's Name, and its Required is `Section, Treatment`. Its columns, in this order:

| Column | Holds |
|---|---|
| the standard's Name | the element, in the standard's own casing and terms |
| Section | the standard's clause or clauses holding the element, or, for a product's convention, the type, message or setting its documentation defines the element in |
| Treatment | `the same`, `differs:` or `not written`, then what the canon writes for the element, where its forms write it |
| Departs For | where the Treatment differs or is not written, the kind of its reason: `the standard's gap`, `the canon's form` or `no need yet`, or two of them in that order, where the reason holds two kinds; empty where it is the same |
| Why | where the Treatment differs or is not written, why the departure was needed: what the standard leaves the canon lacking, what the canon's way of writing a spec requires, or that no spec needs the part; empty where it is the same |

**A departure's one home.** That an element departs, and why, is stated in its row alone. A section's prose states the canon's rule for the element, and a sentence naming the rule a departure cites the row and gives no reason of its own, as [`specs/methodology/modeling-constructs.md § Time`](/specs/methodology/modeling-constructs.md#time) cites [`specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means [UML Elements.UML: TimeEvent]`](/specs/methodology/modeling-constructs.md#what-it-means-1). A departure with no reason is not made.

**Deliberate.** A reader applies a departure as the canon's rule, never as an error to bring back to the standard, and it changes only by its reason judged again. Its Departs For says which reason it is. `the standard's gap`: the standard lacks what the canon needs, which a later version or another standard may supply. `the canon's form`: the departure follows from how the canon writes a spec, as a table wiring no pins does, which no standard's version changes. `no need yet`: no spec here needs the part, which a need arising changes.

**Judged again.** Whenever the canon moves a registered standard's version, or registers a standard, each row whose Departs For holds `the standard's gap` is judged again against that standard. Where it now supplies what the row's Why says the canon needed, the departure is dropped and that standard's form taken, as [`§ External Reference § Which Form a Need Takes`](#which-form-a-need-takes) has a need's form chosen. The judgment of each row is recorded in the design that moves or registers the standard.

## Keeping Specs in Sync

A change reaches more than the facts it edits. It reaches each materialized view restating them, and the counterpart drawing their subject from the other perspective. None of these keeps itself current, so each place a change reaches is checked for a matching update. This section's children say what each kind is kept in sync with.

### Materialized Views

A materialized view ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) is never a second home. It is kept in sync with its sources, the homes of what it restates:

**A directory's own `architecture.md`.** Its sources are the files in its directory and in every directory beneath it, and what [`specs/methodology/spec-placement.md § What an Overview Describes`](/specs/methodology/spec-placement.md#what-an-overview-describes) names beyond it ([`specs/methodology/spec-placement.md § Index, Architecture, Detail`](/specs/methodology/spec-placement.md#index-architecture-detail)). Everything the file restates of its sources, in its prose, its citations and its mapping tables, is kept in sync with them. So is everything it connects among them.

**A diagram, wherever it sits.** Its sources are explicit: the sections and records its Sources list names. Each source names the diagram back ([`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams)).

### Product and Technical Counterparts

A product spec and its technical counterpart are two drawings of one subject, each from its own perspective. Neither is a summary of the other, and each names the other ([`specs/methodology/spec-placement.md § Product or Technical`](/specs/methodology/spec-placement.md#product-or-technical)). They are kept aligned.
