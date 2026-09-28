Where a fact lives, how the place holding it is named, and how everywhere else points at it.

## One Home Per Fact

Every rule, definition, or design principle that could matter in more than one place has exactly one home: the file whose subject matter it most specifically belongs to. Every other place that needs it cites that home rather than restating it in its own words.

A citing location may add the context specific to its own use, the part that would not make sense anywhere else. It never re-derives or re-explains the rule itself.

Before adding a paragraph that states a general rule, check whether that rule already has a home. If it does, cite it as the paragraphs above describe. If it is being stated for the first time, decide its home deliberately: the file whose subject it is, not the file that happened to need it first, so the next place that needs it can cite rather than restate.

**Why the discipline is strict —** two correct copies of a rule read identically on the day they are written. They diverge later, when one is edited and the other is not, and nothing about reading either one reveals that the other exists. A rule with two homes is not redundant, it is a defect waiting for its first amendment.

**Pointers may repeat; rules may not —** several files may cite the same home, and having many citations to one home is the point of there being one home. What no file may do is restate what the cited file says.

## Which Citations Are Allowed

The specifications are layered by what governs what:

```
AGENTS.md
  └ specs/methodology/
      └ specs/application/
          └ product/
              └ technical/
```

`AGENTS.md`'s rules apply to the whole project and the methodology's to every spec (`AGENTS.md § Writing specs`); a product spec states what a user can rely on and a technical spec how it is made true (`specs/methodology/spec-placement.md § Product or Technical`).

A citation names where a fact lives. Cited down a layer, it directs the reader where to look for a specific reason. Cited up a layer, it gives background that benefits the local text.

| From | May cite |
|---|---|
| A product spec | another product spec; `AGENTS.md` |
| A technical spec | another technical spec, a product spec; `AGENTS.md` |
| A methodology spec | another methodology spec; `AGENTS.md` |
| `AGENTS.md` | any spec |

The table is the whole permission for citations among these specs and `AGENTS.md`. Files outside that set cite these specs under their own rules. No spec other than `specs/methodology/working-files.md` names a working file (`specs/methodology/working-files.md § The Working Files`): none is committed, so the name would point a reader at nothing.

A product spec citing a technical spec would make a promise depend on its own implementation; that direction is served instead by the `technical-specs` frontmatter field (`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`), deliberately file-level and coarse so it cannot carry a dependency at heading precision. A methodology spec citing an application spec would make a rule depend on the document it governs.

An application spec does not cite a methodology spec. Direction is not the reason, since that citation would point up; subject is. An application spec's subject is the product, and how a spec here is authored is no part of it, so a reader of the product has no use for the authoring rule behind a sentence. An application spec may still name a construct, because a construct is what its own content is authored as; what it does not do is reach into the methodology for the methodology's own claims. `AGENTS.md` is different in scope: its rules apply to the whole project, not only to specs (`AGENTS.md § Writing specs`), so a spec depending on one depends on it like any other file here.

## Titling a Heading

A heading's title is a stable slug for whatever the section covers, not prose to be refined later. Every citation depends on that exact text, so a title chosen well the first time is what keeps a citation from ever needing to change. If a title does change, update every citation naming it in the same edit; nothing else will catch one left pointing at a title that no longer exists.

| Rule | Form |
|---|---|
| No `§` in the heading itself | `## Vision`, never `## § Vision` |
| No `[` in the heading itself, which opens a record's identifying values in a citation | `## Retry Policy`, never `## Retry Policy [draft]` |
| Unique among headings sharing its parent | two headings under different parents may share a title |
| A file's top-level headings unique across the file | they have no parent but the file |

A numbered heading, or one counting its children, is the heading case of `AGENTS.md § Ordinals and Counts`. A heading pays for it twice, since its title is also the text of every citation naming it: renumbering sections, or retitling one whose count went stale, changes those citations as well.

**Bold lead-ins are not headings —** a bold lead-in (`specs/methodology/modeling-constructs.md § Bold Lead-ins`) has none of the guarantees a heading carries, starting with enforced uniqueness. It has no citation form either, per `§ Writing a Citation`, so a paragraph that is or needs to be a citation's target is authored as a child heading instead, which gets every rule above rather than needing a workaround. A record (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) is the one exception, cited by the form of its own `§ Writing a Citation` gives. Do not promote one pre-emptively on the chance it might be cited; only once it actually is, or once its section states that its entries exist to be cited.

## Writing a Citation

A citation must let a cold reader follow it without guessing or reopening files to re-derive the location.

The token for referencing a section is `§`, with a space on each side. Each form below is written inside a single backtick span, never split across spans and never left as bare prose:

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

## Keeping Companions in Step

Some facts are stated once and rendered in more than one place. Those renderings are not second homes, and they do not keep themselves current.

**A product spec and its technical counterpart —** when a fact changes in one, check whether the other needs a matching update. That the two name each other at all is `specs/methodology/spec-placement.md § Product or Technical`'s requirement; what it does not do is keep them current, which is this duty.

**A directory's own `architecture.md` —** it is a synchronization target, not a first-written source. Its prose, its citations, and its mapping tables each restate or render a fact whose real home is elsewhere. When that fact changes, check whether `architecture.md` needs a matching update too.

**A diagram, wherever it sits —** it renders the sections and records its Sources list names, each of which names it back (`specs/methodology/modeling-constructs.md § Diagrams`). When one of them changes, check whether the diagram needs a matching update too.
