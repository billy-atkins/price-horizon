Where a fact lives, how the place holding it is named, and how everywhere else points at it.

## One Home Per Fact

Every rule, definition, or design principle that could matter in more than one place has exactly one home: the file whose subject matter it most specifically belongs to. Every other place that needs it cites that home rather than restating it in its own words.

**Citing a rule where it applies —** a place applying another file's rule, definition or principle gives it a point-of-use citation, and may add what only that place can say: how the rule applies there, and why it matters there. Clean-as-you-go is one principle in a home garage, a commercial kitchen and a medical facility, yet what it asks of the hands and what hangs on it differ in each. An agent meets the rule where it acts, so the citing place states the application wherever an agent reading only that place would apply the rule wrongly, and the reason wherever that agent would not see why it matters there; a bare citation is enough where neither holds. The citation belongs to each step applying the rule, the way a playbook's steps link to the detailed procedures they carry out, so the rule is in mind when the work is done rather than left to an earlier reading of the rules; a step run from a playbook entry or a table row that cites the rule has it there, and an index that only routes to rules stands in for no step's citation. What a citing place never does is re-derive or re-explain the rule, or add a rule of its own about the cited subject, which would be a second home with a citation attached: a duty that would hold wherever the rule applies belongs in the rule's home, and one that holds only because of the citing place's own subject is its application.

Before adding a paragraph that states a general rule, check whether that rule already has a home. If it does, cite it as this section describes. If it is being stated for the first time, decide its home deliberately: the file whose subject it is, not the file that happened to need it first, so the next place that needs it can cite rather than restate. A rule several files use and none owns has its home in the narrowest file covering every use, since a home above every use overstates how far the rule reaches.

**Why the discipline is strict —** two correct copies of a rule read identically on the day they are written. They diverge later, when one is edited and the other is not, and nothing about reading either one reveals that the other exists. A rule with two homes is not redundant, it is a defect waiting for its first amendment.

**Pointers may repeat; rules may not —** several files may cite the same home, and having many citations to one home is the point of there being one home. What no file may do is restate what the cited file says.

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

Cited down a layer, a citation directs the reader where to look for a specific reason. Cited up a layer, it gives background that benefits the local text.

| From | May cite |
|---|---|
| A product spec | another product spec |
| A technical spec | another technical spec, a product spec |
| A methodology spec | another methodology spec; `specs/AGENTS.md` |
| `specs/AGENTS.md` | any spec |
| Code | a product spec, a technical spec, or a section of one, never a record, naming what it carries out in the form `specs/methodology/code.md § Citing the Specs From Code` gives, governed by the specs rather than a layer of them |

The table is the whole permission for citations among these specs, code and `specs/AGENTS.md`. Files outside that set, the project's own root `AGENTS.md` among them, cite these specs under their own rules, and no spec cites a section of the root `AGENTS.md`, whose instructions are the project's rather than the method's. No spec other than `specs/methodology/working-files.md` names a working file (`specs/methodology/working-files.md § The Working Files`): none is committed, so the name would point a reader at nothing. `specs/AGENTS.md` is agent instructions rather than a spec, and names the working files its procedures act on.

A product spec citing a technical spec would make a promise depend on its own implementation; that direction is served instead by the `technical-specs` frontmatter key (`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`), deliberately file-level and coarse so it cannot carry a dependency at heading precision. A methodology spec citing an application spec would make a rule depend on the document it governs.

An application spec does not cite a methodology spec. Direction is not the reason, since that citation would point up; subject is. An application spec's subject is the product, and how a spec here is authored is no part of it, so a reader of the product has no use for the authoring rule behind a sentence. An application spec may still name a construct, because a construct is what its own content is authored as; what it does not do is reach into the methodology for the methodology's own claims. Nor does it cite `specs/AGENTS.md`, which holds the method's own rules, for the same reason.

## Titling a Heading

A heading's title is a stable slug for whatever the section covers, not prose to be refined later. Every citation depends on that exact text, so a title chosen well the first time is what keeps a citation from ever needing to change. If a title does change, update every citation naming it in the same edit; nothing else will catch one left pointing at a title that no longer exists.

| Rule | Form |
|---|---|
| No `§` in the heading itself | `## Vision`, never `## § Vision` |
| No `[` in the heading itself, which opens a record's identifying values in a citation | `## Retry Policy`, never `## Retry Policy [draft]` |
| Unique among headings sharing its parent | two headings under different parents may share a title |
| A file's top-level headings unique across the file | they have no parent but the file |

A numbered heading, or one counting its children, is the heading case of `specs/AGENTS.md § Ordinals and Counts`. A heading pays for it twice, since its title is also the text of every citation naming it: renumbering sections, or retitling one whose count went stale, changes those citations as well.

**Bold lead-ins are not headings —** a bold lead-in (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) has none of the guarantees a heading carries, starting with enforced uniqueness. It has no citation form either, per `§ Writing a Citation`, so a paragraph that is or needs to be a citation's target is authored as a child heading instead, which gets every rule this section sets rather than needing a workaround. A record (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) is the one exception, cited in the form `§ Writing a Citation` gives for it. Do not promote one pre-emptively on the chance it might be cited; only once it actually is, or once its section states that its entries exist to be cited.

## Writing a Citation

A citation must let a cold reader follow it without guessing or reopening files to re-derive the location, and find at its target what the citer attributes to it.

The token for referencing a section is `§`, with a space on each side. Each form this section gives is written inside a single backtick span, never split across spans and never left as bare prose:

```
A section in the same file           § Title
A nested section in the same file    § Parent § Child
A record                             § Type [Key: value]
A record in another file             path/from/root.md § Type [Key: value; Key: value]
A section in another file            path/from/root.md § Parent § Child
A whole file                         path/from/root.md
An index.md                          never a citation target
```

A cross-file citation gives the path from the project root, exactly as it would be written anywhere else, never a directory-relative path. A same-file citation omits the path entirely and starts at the section token.

A section is named by its full lineage of heading titles, one segment per level from the top of the file down to the target. A level-1 heading is the file's own title rather than a section, so a lineage starts below it; a top-level section is one segment on its own. A child heading is only guaranteed unique within its own parent's scope, so its citation carries every ancestor's title down to it.

A record (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) is named by the citation of the record section holding it, then a space and, in square brackets inside the same span, each of its identifying fields as `Key: value`, in the order its type's table gives them, separated by a semicolon and a space, like a query parameter selecting one record from the section: `[Name: Retry Policy]` after an Open Questions section's citation, or `[Region: Texas; Horizon: 6 Months]` for a type identified by two fields. An identifying value holds no semicolon (`specs/methodology/modeling-constructs.md § Constructs § Record Form`), so each pair is split at `; `, and each value is compared with the record's after trimming the space around it, and must match exactly, as a title does.

**What cannot be cited —** there is no form for citing a bold lead-in or any other non-heading content but a record; `§ Titling a Heading` says when such content becomes a heading. A directory's `index.md` carries no heading lineage of its own, and it is not a place a citation is written either.

**A title that names a kind of section rather than one particular section —** it resolves to no single heading anywhere, so it is not a citation and takes no `§`. A rule referring to `Test Scenarios` generally, where the level varies by context, names a kind; a rule referring to one file's own `## Diagrams` names a section.

### Referring to Other Text

Other text is cited, never pointed at by direction: a sentence referring to text elsewhere, a section, a table, a step or a rule, names it by citation or by containment, or, where no citation is allowed there, by name, never as "above", "below", "the next step" or "the preceding table". A direction holds only while nothing moves: reorder steps, insert a section or move a table, and every direction pointing across the change now points at the wrong text, silently, where a citation follows its heading wherever it moves under the same parent, and fails loudly, reported by the audit script, once it moves elsewhere or is retitled. A spec written with directions leaves that trap for whoever edits it next; one written with citations can be reordered freely. Text worth referring to sits in a section of its own, and where it does not, it is given a heading before it is cited, per `§ Titling a Heading`. Text may name what a section or file containing it holds by containment, "this section's lifecycle", "this Workflow's steps", since text moved within what it names stays within it. A word whose subject is where something sits, a heading one level below another, a node drawn above the flow, sends the reader to no text and is none of this; a word sending the reader to other text is a direction, however it is phrased. A sentence introducing the block directly under it, a table, a list, a code block or a construct, points at nothing: its place joins the two, so it says what the block is for, never where it is, "the following Algorithm" and "these parts" dropped rather than kept. Nothing goes between such a sentence and its block, since the reader would hear one thing introduced and see another; text that must introduce something further away is no such sentence, and the content it introduces is given a section of its own and cited.

## Keeping Renderings in Step

Some facts are stated once and rendered in more than one place. Those renderings are not second homes, and they do not keep themselves current.

**A product spec and its technical counterpart —** when a fact changes in one, check whether the other needs a matching update. That the two name each other at all is `specs/methodology/spec-placement.md § Product or Technical`'s requirement; what it does not do is keep them current, which is this duty.

**A directory's own `architecture.md` —** what it restates of its detail files, in its prose, its citations and its mapping tables, and what it connects among them, is a synchronization target (`specs/methodology/spec-placement.md § Index, Architecture, Detail`). When a fact in one of its detail files changes, check whether `architecture.md` needs a matching update too.

**A diagram, wherever it sits —** it renders the sections and records its Sources list names, each of which names it back (`specs/methodology/modeling-constructs.md § Diagrams`). When one of them changes, check whether the diagram needs a matching update too.
