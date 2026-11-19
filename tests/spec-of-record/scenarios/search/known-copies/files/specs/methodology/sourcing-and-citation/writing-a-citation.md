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

**Where a citation sits.** A citation supporting a claim closes the clause it supports, or stands in a sentence of its own, so the reader meets the claim before its source. A sentence making several claims, each with its citation, is split into a sentence for each claim. A citation glossing a term stands just after the term, in parentheses, as "the design frame ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md))" does. A citation used as a name, the subject of its clause, as in "[`specs/methodology/spec-style/markdown.md § Emphasis`](/specs/methodology/spec-style/markdown.md#emphasis) sets the form of emphasis", stays where it is.

**What cannot be cited.** Of the content that is not a heading, only a part of a keyed instance has a form for citing it. A bold lead-in has none. [`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`](/specs/methodology/sourcing-and-citation/titling-a-heading.md#titling-a-heading) says when such content becomes a heading. A directory's `index.md` carries no heading lineage of its own.

**A title that names a kind of section rather than one particular section.** It resolves to no single heading anywhere, so it is not a citation and takes no `§`. A rule referring to `Test Scenarios` generally, where the level varies by context, names a kind. A rule referring to one file's own `## Glossary` names a section.

**A file name that names a kind of file rather than one particular file.** It names whatever file plays that part, in any directory or project the rule reaches, rather than the one file at a path. So it is not a citation. It is written as the bare file name, without a path. Where it matters whose file it is, the name is qualified by its owner, as in the product specs' `architecture.md`. A rule referring to any directory's `architecture.md` names a kind, and [`specs/methodology/architecture.md`](/specs/methodology/architecture.md) names one file.

### Referring to Other Text

Other text is cited, never pointed at by direction. A sentence referring to text elsewhere, whether a section, a table, a step or a rule, names it by citation or by containment. Where no citation is allowed there, the sentence names the text by name. It never points at the text as "above", "below", "the next step" or "the preceding table".

A direction holds only while nothing moves. Reorder steps, insert a section or move a table, and every direction pointing across the change silently points at the wrong text. A citation follows its heading wherever the heading moves under the same parent. Once the heading moves elsewhere or is retitled, the citation fails loudly, and the audit script reports it. A spec written with directions leaves that trap for whoever edits it next. A spec written with citations can be reordered freely. Text worth referring to sits in a section of its own. Where it does not, it is given a heading before it is cited ([`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`](/specs/methodology/sourcing-and-citation/titling-a-heading.md#titling-a-heading)).

#### Direction Wordings

Whether a wording is a direction:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Wording \
**Annotations:** Why, Such As

| Wording | A direction | Why | Such As |
|---|---|---|---|
| containment, naming what a section or file containing the text holds | no | text moved within what it names stays within it | "this section's life cycle", "this Workflow's steps" |
| a word whose subject is where something sits | no | it sends the reader to no text | a heading one level below another, a node drawn above the flow |
| a sentence introducing the block directly under it: a table, a list, a code block or a construct | no | its place joins the two | |
| any other word sending the reader to other text, however it is phrased | yes | it holds only while nothing moves | |

A sentence introducing the block under it says what the block is for, never where it is. Wordings such as "the following Algorithm" and "these parts" are dropped. Nothing goes between such a sentence and its block, since the reader would hear one thing introduced and see another. Text that must introduce something further away is not such a sentence. The content it introduces is given a section of its own and cited.

### Citing From Code

Code names a spec it relies on with a spec annotation. A spec annotation is a plain comment on a line of its own, in the comment syntax of the code's language, and never a documentation comment. It holds a tag, a space, and a citation. The citation takes the form [`§ Writing a Citation`](#writing-a-citation) gives for a section in another file, a part in another file or a whole file. It drops the backticks a citation takes in a spec, since the tag marks where the citation begins and the line marks where it ends. Each tag has a rule of its own saying what carries the tag, and [`specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation/which-citations-are-allowed.md#which-citations-are-allowed) says what each tag may cite:
- `@app-spec`, in the code the application specs govern, as [`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code) has it;
- `@canon-spec`, in a registered skill's scripts and the code the skills share, on a unit carrying out a check, citing the check's record, or, while the check's entry stands in a skill's table, the section it enforces, or on a copy of the canon's values, citing the area its values come from, as [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill) has it.

```
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct
```

In a language with block comments only, each annotation is a block comment of its own on one line, and its citation ends before the closer. A heading holding that language's comment closer cannot be cited from code in that language.

**A list, one line per citation, sorted.** A unit or a copy may answer to several specs, a product promise and the technical section making it true among them. It carries an annotation for each, on consecutive lines. The annotations are sorted in plain character order of the citation, so the list has one order whoever writes it, and two changes to it collide less often. One citation to a line keeps each citation readable and makes its change a line of its own in a diff. It also leaves a heading free to hold any punctuation.

**Why it is a citation.** An annotation makes the link one spec makes to another, so it is held to the same guarantee. It names a file, and a heading, that exist. A heading retitled updates every annotation naming it in the same edit, per [`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`](/specs/methodology/sourcing-and-citation/titling-a-heading.md#titling-a-heading). The annotation is kept in the code it describes, so it moves with that code through every refactor. A map kept in a file of its own would drift.

**A comment, not a language's own annotation.** A spec annotation is a comment. It is not a Java annotation, a C# attribute or a decorator, so it compiles the same in every language and needs no tool to know it.

### A Citation's Link

A citation in a file a person reads on GitHub is also a link the reader can follow. Those files are `README.md`, the files under `docs/`, and every spec but [`specs/AGENTS.md`](/specs/AGENTS.md). Agents read the skills and the `AGENTS.md` files, so their citations carry no link. The citation itself is the link's text:

```markdown
[`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Referring to Other Text`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#referring-to-other-text)
```

The citation identifies, and the link navigates. GitHub addresses a heading by a flat anchor, which loses the heading's lineage. So the citation stays the exact reference, and the link reaches the closest place GitHub can address. Where the two disagree, the citation is right.

**Reference Key:** Citation \
**Required:** Link Target

| Citation | Link Target |
|---|---|
| a section in another file | the path from the repository's root, then the cited heading's anchor: `/path#anchor` |
| a section in the same file | the cited heading's anchor: `#anchor` |
| a part of a keyed instance, a record or a row | the anchor of the section holding it, the citation's key naming the part |
| a whole file, named by its path from the repository's root, or a directory that is no document, as a skill's folder is | that path: `/path` |
| a Construct, an Extends or an Implements field's value | no link, since the value declares what a definition or an instance is |

A heading's anchor follows GitHub's convention, which GitHub Flavored Markdown does not define ([`specs/methodology/external-references.md § External References [Name: GFM]`](/specs/methodology/external-references.md#external-references)). The title is written in lowercase. Every character but a letter, a digit, a space, a hyphen or an underscore is dropped, and each space becomes a hyphen. A title met again in the same file takes `-1`, `-2` and so on, in the order the headings stand. A citation is resolved to its one heading by its lineage first, so its link reaches that heading even where titles repeat. A link reaches only a file GitHub serves, one version control tracks. It never reaches an `index.md`, which nothing cites. A bare file name is no citation and carries no link, as in an `index.md`'s row naming a file beside it, or in words naming a kind of file.

**Written by a script, never by an author.** An author writes only the citation. The `--refresh-links` option of `.ai/skills/design-specs/` writes and refreshes every link, and a design's apply runs it once the text its steps call for is written. Every script reading a citation sets its link aside first. `.ai/skills/audit-specs/` reports a citation missing its link, a link not reaching what its citation resolves to, and a link where none belongs.
