## One Home Per Fact

Every rule, definition, or design principle that could matter in more than one place has exactly one home: the file whose subject matter it most specifically belongs to. Every other place that needs it cites that home rather than restating it in its own words.

**Citing a rule where it applies —** a place applying another file's rule, definition or principle gives it a point-of-use citation. It may add what only that place can say: how the rule applies there, and why it matters there. Clean-as-you-go is one principle in a home garage, a commercial kitchen and a medical facility, yet what it asks of the hands, and what hangs on it, differ in each. An agent meets the rule where it acts, so the citing place states the application wherever an agent reading only that place would apply the rule wrongly, and the reason wherever that agent would not see why the rule matters there. Where neither holds, a bare citation is enough.

**Each step carries the citation —** the citation belongs to each step applying the rule, the way a playbook's steps link to the detailed procedures they carry out, so the rule is in mind when the work is done rather than left to an earlier reading. A step carried out from a playbook entry or a table row that cites the rule has the citation there already. An index that only routes to rules stands in for no step's citation.

**What a citing place never adds —** it never re-derives or re-explains the rule, or adds a rule of its own about the cited subject, which would be a second home with a citation attached. A duty that would hold wherever the rule applies belongs in the rule's home; one that holds only because of the citing place's own subject is its application.

Before adding a paragraph that states a general rule, check whether that rule already has a home. If it does, cite it as this section describes. If not, place it deliberately, never in the file that happened to need it first, so the next place that needs it can cite rather than restate. A rule several files use and none owns has its home in the narrowest file covering every use, since a home above every use overstates how far the rule reaches.

**Why the discipline is strict —** two correct copies of a rule read identically on the day they are written. They diverge later, when one is edited and the other is not, and nothing about reading either one reveals that the other exists. A rule with two homes is not redundant, it is a defect waiting for its first amendment.

**Pointers may repeat —** several files may cite the same home; many citations to one home are the point of there being one.

## Which Citations Are Allowed

The specifications are layered by what governs what:

```
specs/AGENTS.md
  └ specs/methodology/
      └ specs/application/
          └ product/
              └ technical/
```

`specs/AGENTS.md`'s rules and the methodology's reach the files in Spec of Record's scope as `specs/methodology/scope.md § What Spec of Record Governs` sets; a product spec states what a user can rely on and a technical spec how it is made true (`specs/methodology/spec-placement.md § Product or Technical`).

A citation pointing down a layer sends the reader somewhere for a specific purpose; one pointing up a layer gives background that benefits the local text.

What a citation may name, every row its source matches granting what that row lists:

**Construct:** Decision Table

**Hit Policy:** Collect

**Conditions:** From

| From | May cite |
|---|---|
| A product spec | another product spec |
| A technical spec | another technical spec, a product spec |
| A methodology spec | another methodology spec; `specs/AGENTS.md`; the skills' directory, a registered skill or a file of one, and the code the skills share, naming what applies its rules |
| `specs/AGENTS.md` | any spec; a registered skill or a file of one |
| "A product spec", "A technical spec", "A methodology spec" | the project's root `AGENTS.md` as a whole file, never a section of it |
| Code the application specs govern | a product spec, a technical spec, or a section of one, never a record, naming what it carries out or checks with an app-spec annotation (`§ Writing a Citation § Citing From Code`) |
| A registered skill's script, or the code the skills share | `specs/AGENTS.md` or a methodology spec, or a section of one, naming where a copy it holds takes its values from with a canon-spec annotation (`§ Writing a Citation § Citing From Code`) |

Code is governed by the specs rather than a layer of them. The table is the whole permission for citations from these specs, code, the skills' scripts and `specs/AGENTS.md`. Files outside that set, the project's own root `AGENTS.md` among them, cite these specs under their own rules, the root `AGENTS.md`'s instructions being the project's rather than the method's. No spec other than `specs/methodology/working-files.md` names a working file (`specs/methodology/working-files.md § The Working Files`): none is committed, so the name would point a reader at nothing. `specs/AGENTS.md` is agent instructions rather than a spec, and names the working files its procedures act on.

A product spec citing a technical spec would make a promise depend on its own implementation; that direction is served instead by the `technical-specs` frontmatter key (`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`), deliberately file-level and coarse so it cannot carry a dependency at heading precision. A methodology spec citing an application spec would make a rule depend on the document it governs.

An application spec cites neither a methodology spec nor `specs/AGENTS.md`. Direction is not the reason, since such a citation would point up; subject is. An application spec's subject is the product, and how a spec is authored is no part of it, so a reader of the product has no use for the authoring rule behind a sentence. An application spec may still name a construct, because a construct is what its own content is authored as; what it does not do is reach into the methodology, or into `specs/AGENTS.md`, which holds the method's own rules, for their own claims.

## Titling a Heading

A heading's title is a stable slug for whatever the section covers, not prose to be refined later. Every citation depends on that exact text, so a title chosen well the first time is what keeps a citation from ever needing to change. If a title does change, update every citation naming it in the same edit; a citation left naming the old title is broken until it is updated.

| Rule | Form |
|---|---|
| No `§` in the heading itself | `## Vision`, never `## § Vision` |
| No `[` in the heading itself, which opens a record's identifying values, or a part's identifier, in a citation | `## Session Timeout`, never `## Session Timeout [draft]` |
| Unique among headings sharing its parent, a top-level heading's parent being its file | two headings under different parents may share a title |

A numbered heading, or one counting its children, is the heading case of `specs/methodology/spec-style.md § Ordinals and Counts`. A heading pays for it twice, since its title is also the text of every citation naming it: renumbering sections, or retitling one whose count went stale, changes those citations as well.

**Bold lead-ins are not headings —** a bold lead-in (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) has none of the guarantees a heading carries, starting with enforced uniqueness, and no citation form (`§ Writing a Citation`). So a paragraph that is, or needs to be, a citation's target is authored as a child heading instead, which gets every rule this section sets rather than needing a workaround. Do not promote a lead-in to a heading pre-emptively, on the chance it might be cited; promote it only once it is cited. Entries that exist to be cited are records instead (`specs/methodology/modeling-constructs.md § Constructs § Record Form`).

## Writing a Citation

A citation must let a cold reader follow it without guessing or reopening files to re-derive the location, and find at its target what the citer attributes to it.

The token for referencing a section is `§`, followed by a space, and preceded by one wherever a path or a parent title comes before it. Each form this section gives is written inside a single backtick span, never split across spans and never left as bare prose:

```
A section in the same file           § Title
A nested section in the same file    § Parent § Child
A record                             § Type [Key: value]
A record in another file             path/from/root.md § Type [Key: value; Key: value]
A part of a construct                path/from/root.md § Section [Key: value]
A section in another file            path/from/root.md § Parent § Child
A whole file                         path/from/root.md
An index.md                          never a citation target
```

A cross-file citation gives the path from the project root, exactly as it would be written anywhere else, never a directory-relative path. A same-file citation omits the path entirely and starts at the section token.

A section is named by its full lineage of heading titles, one segment per level from the top of the file down to the target. A level-1 heading is the file's own title rather than a section, so a lineage starts below it; a top-level section is one segment on its own. A child heading is only guaranteed unique within its own parent's scope, so its citation carries every ancestor's title down to it.

A record (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) is named by the citation of the record section holding it, then a space and, in square brackets inside the same span, its identifying fields, like a query parameter selecting one record from the section. Each is written `Key: value`, in the order its type's table gives them, separated by a semicolon and a space: `[Name: Session Timeout]` after an `Open Questions` section's citation, or `[Country: Canada; Tax Year: 2025]` for a type identified by two fields. An identifying value holds no semicolon (`specs/methodology/modeling-constructs.md § Constructs § Record Form`), so the pairs are split at `; `. Each value is compared with the record's after trimming the space around it, and must match exactly, as a title does.

A part of a construct (`specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct`) is named the same way, by its construct's section and its identifier.

**What cannot be cited —** there is no form for citing a bold lead-in or any other non-heading content but a record or a part of a construct; `§ Titling a Heading` says when such content becomes a heading. A directory's `index.md` carries no heading lineage of its own.

**A title that names a kind of section rather than one particular section —** it resolves to no single heading anywhere, so it is not a citation and takes no `§`. A rule referring to `Test Scenarios` generally, where the level varies by context, names a kind; a rule referring to one file's own `## Glossary` names a section.

**A file name that names a kind of file rather than one particular file —** it names whatever file plays that part, in any directory or project the rule reaches, rather than the one file at a path, so it is not a citation. It is written as the bare file name, without a path, qualified by whose it is where that matters: the product specs' `architecture.md`, say. A rule referring to any directory's `architecture.md` names a kind; `specs/methodology/architecture.md` names one file.

### Referring to Other Text

Other text is cited, never pointed at by direction. A sentence referring to text elsewhere, whether a section, a table, a step or a rule, names it by citation, by containment, or, where no citation is allowed there, by name. It never points at it as "above", "below", "the next step" or "the preceding table".

A direction holds only while nothing moves. Reorder steps, insert a section or move a table, and every direction pointing across the change silently points at the wrong text. A citation follows its heading wherever it moves under the same parent, and once the heading moves elsewhere or is retitled, the citation fails loudly, reported by the audit script. A spec written with directions leaves that trap for whoever edits it next; one written with citations can be reordered freely. Text worth referring to sits in a section of its own; where it does not, it is given a heading before it is cited (`§ Titling a Heading`).

Whether a wording is a direction:

**Construct:** Decision Table

**Hit Policy:** First

**Conditions:** Wording

**Annotations:** Why, Such as

| Wording | A direction | Why | Such as |
|---|---|---|---|
| containment, naming what a section or file containing the text holds | no | text moved within what it names stays within it | "this section's lifecycle", "this Workflow's steps" |
| a word whose subject is where something sits | no | it sends the reader to no text | a heading one level below another, a node drawn above the flow |
| a sentence introducing the block directly under it: a table, a list, a code block or a construct | no | its place joins the two | |
| any other word sending the reader to other text, however it is phrased | yes | it holds only while nothing moves | |

A sentence introducing the block under it says what the block is for, never where it is: "the following Algorithm" and "these parts" are dropped, not kept. Nothing goes between such a sentence and its block, since the reader would hear one thing introduced and see another. Text that must introduce something further away is no such sentence: the content it introduces is given a section of its own and cited.

### Citing From Code

Code names a spec it relies on with a spec annotation: a plain comment line of its own, in the comment syntax of the code's language, never a documentation comment, holding a tag, a space, and a citation. The citation takes the form `§ Writing a Citation` gives for a section in another file or for a whole file, without the backticks a citation takes in a spec, since the tag marks where it begins and the line where it ends. Each tag has a rule of its own saying what carries one, and `§ Which Citations Are Allowed` what each may cite:

- `@app-spec`, in the code the application specs govern, as `specs/methodology/code.md § Citing the Specs From Code` has it;
- `@canon-spec`, in a registered skill's scripts and the code the skills share, as `specs/methodology/skills.md § Authoring a Skill` has it.

```
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct
```

In a language with block comments only, each annotation is a block comment of its own on one line, its citation ending before the closer, and a heading holding that language's comment closer cannot be cited from it.

**A list, one line per citation, sorted —** a unit or a copy answering to several specs, a product promise and the technical section making it true among them, carries an annotation for each, on consecutive lines. They are sorted in plain character order of the citation, so the list has one order whoever writes it, and two changes to it collide less often. One citation to a line keeps each readable, makes its change a line of its own in a diff, and leaves a heading free to hold any punctuation.

**Why it is a citation —** an annotation makes the link one spec makes to another, so it is held to the same guarantee. It names a file, and a heading, that exist, and a heading retitled updates every annotation naming it in the same edit, per `§ Titling a Heading`. Kept in the code it describes, it moves with that code through every refactor, where a map kept in a file of its own would drift.

**A comment, not a language's own annotation —** it is not a Java annotation, a C# attribute or a decorator, so it compiles the same in every language and needs no tool to know it.

## An External Reference

The canon adopts an outside standard where an agent or a software engineer already knows it from training or experience, so a form or a meaning the canon relies on reads without the canon teaching it. A standard is registered where a rule adopts it, or maps the rule's own forms onto it, for something an author writes or an agent reads by. It is registered once, as a record of the type named External References in `specs/methodology/external-references.md § External References`, pinned to the version or revision the canon relies on, so what the canon means holds still as the standard moves on, and an author reaching for the name finds the one text it means.

**What is not registered —** a digest or an encoding a script computes, as SHA-256 and UTF-8, named in the rule using it; a convention no one publishes, as kebab-case, defined where it is used; a standard a registered one adopts in turn, as GFM extends CommonMark, which that record covers; and a tool or a product a rule names only as an example of what one of its forms maps onto.

**Citing it —** the section whose rule adopts a registered standard, or maps onto it, cites its record where it first names the standard, and states no version or link of its own, so the record is the one home of both (`§ One Home Per Fact`); a section using that rule's forms relies on the rule, and cites the rule's section, not the record, where it needs to. The section states what it narrows, adds to or changes in the standard, which the standard's own text cannot tell a reader; the standard is cited for the rest, and for what the section's forms mean where it is silent.

**Moving a version —** relying on another version of a standard, or on more of it than its record covers, is a change to the canon that changes the record, each section citing it, and the checks of what those sections state, together.

A record gives these fields, in this order:

| Field | Identifies | Required | Default Value | Holds |
|---|---|---|---|---|
| Name | yes | yes | | the standard's short name, as its readers know it |
| Title | no | yes | | its full title, and who publishes or stewards it |
| Version | no | yes | | the version relied on, or, for a standard publishing none, the revision relied on, named by its date |
| URL | no | yes | | a link to the text of that version or revision, never to whatever is current, written as literal text |
| Relation | no | yes | | how the canon relies on it: `adopts`, the canon's forms being the standard's own; or `maps onto`, the canon's forms being its own, each mapping onto one of the standard's, and the canon's rules holding wherever they differ |
| Covers | no | yes | | the part of the standard the canon relies on |

## Keeping Renderings in Step

Some facts are stated once and rendered in more than one place. Those renderings are not second homes, and they do not keep themselves current.

**A product spec and its technical counterpart —** when a fact changes in one, check whether the other needs a matching update. `specs/methodology/spec-placement.md § Product or Technical` requires the two to name each other; keeping them current is this duty.

**A directory's own `architecture.md` —** everything it restates of its detail files, in its prose, its citations and its mapping tables, and everything it connects among them, is kept in step with them (`specs/methodology/spec-placement.md § Index, Architecture, Detail`). When a fact in one of its detail files changes, check whether `architecture.md` needs a matching update too.

**A diagram, wherever it sits —** it renders the sections and records its Sources list names, each of which names it back (`specs/methodology/modeling-constructs.md § Diagrams`). When one of them changes, check whether the diagram needs a matching update too.
