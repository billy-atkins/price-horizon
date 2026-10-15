## What a Finished Spec Reads Like

A finished spec describes a destination, not the conversation that produced it. A reader arriving cold, with no visibility into any draft, discussion, or rejected alternative that came before, should be able to read any sentence and take it at face value.

Content that only makes sense to someone present for the discussion that produced it does not belong in a spec, however useful it was to sort out at the time.

**Reference Key:** Pattern

**Required:** Example, Instead

| Pattern | Example | Instead |
|---|---|---|
| Meta-commentary about the act of writing | "worth stating plainly," "worth being explicit about," "a principle worth stating rather than leaving implicit" | state the principle; do not narrate the decision to state it |
| Arguing against an alternative the document never proposed | defining a chosen approach by contrast with a technology mentioned nowhere else | state what was chosen and why it is right, on its own terms |
| Referencing the document's own revision history | "as discussed," "this corrects an earlier version," "now formalized," "the same way the current one did" | a spec has one state, the current one |
| Hedged framing left over from drafting | "for now," "at this point," attached to a settled decision | state a final decision as final; record a genuinely open one as an open question (`specs/methodology/spec-placement.md § Open Question`) rather than hedging it inside settled prose |

## Trade-offs Are Not Journey Language

`§ What a Finished Spec Reads Like` is not a rule against explaining trade-offs. A genuine engineering trade-off belongs in the spec with its reasoning, because it teaches a reader how to make the same kind of call correctly in a new situation.

**The test —** a comparison passes when either holds:

- it states a timeless design principle a cold reader can apply elsewhere;
- it is drawn against something the reader has a live, document-supported reason to ask about, an alternative the reader could plausibly have arrived at themselves, whether or not an author once did.

It fails when it makes sense only to someone who watched the alternative get proposed and rejected.

Choosing a star schema over a snowflake schema passes: the reasoning transfers to the next schema decision. Choosing a DAG over a State Machine for an acyclic process passes for the same reason. Ruling out a technology the document never otherwise mentions fails: nothing in the document gave a cold reader anything to reject.

## Clear Prose

Clear prose is measured by the effort it costs its primary reader, not by its count of words. Each kind of file this section reaches is written for a primary reader, without failing its secondary one:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Files

| Files | Primary reader | Secondary reader |
|---|---|---|
| The specs | a person, the designer who must read and steer them | an agent |
| "The agent instructions", "The skills" | a cold agent | a person |

The methodology is among the specs. The working files are outside this section, since each serves the work in progress rather than a reader of the specs, and none is committed (`specs/methodology/working-files.md § The Working Files`).

A person designs the agent instructions and the skills, deciding what they say and approving them, and an agent writes them for a cold agent. They are judged, in the end, by how an agent behaves under them.

**Cut what carries nothing —** every word read costs the reader, and costs an agent tokens too. So filler, a point made twice, and commentary on the writing itself are cut; `§ What a Finished Spec Reads Like` covers the commentary.

**Keep what carries the reader —** a word that carries meaning, or carries the reader from one idea to the next, stays. Prose cut too far fails as surely as prose padded out. Minified code is shorter than its source and unreadable, because minifying removes what a reader uses and a machine does not need:

**Reference Key:** Minified Code Removes

**Required:** Too-terse Prose Drops, Instead

| Minified Code Removes | Too-terse Prose Drops | Instead |
|---|---|---|
| meaningful names, leaving `a` and `b` | the term itself, a pronoun standing far from what it names | name the term again |
| comments saying why | "because" and "so", the reason linking two facts | state the reason |
| one statement per line | one idea per sentence, several packed into one | give each idea a sentence of its own |
| whitespace and structure | paragraph breaks, lists and headings showing how ideas relate | give the ideas their structure |

**A chain of qualifying clauses —** the usual way one sentence comes to hold several ideas: a main clause, then clause after clause joined by commas, each qualifying the one before. Each clause is easy to write, and the whole is hard to read. Split the chain into sentences, or into a list when its parts are alike.

**An example in the canon —** an example maps what a reader does not yet know onto what it does. One from outside the house lands with any agent, from its training. One drawn from the application specs, their own files, domains or vocabulary, lands only with an agent that has already read them, which a cold agent loading only what its step needs often has not. So an example in the canon is never drawn from the application specs, unless it names the project the canon is checked in rather than illustrating a rule; the methodology may illustrate itself.

**Words its reader already uses —** a rule is written in words its reader can apply without looking anything up, and gives an example of what passes and what fails wherever its words alone leave the reader unsure: a heading "names a thing, as `Payroll Run`, or asks the question its construct answers, never an activity, as `Running payroll`" (`specs/methodology/modeling-constructs.md § Constructs § Declared Construct`), not a grammarian's term for either. A term the canon adopts from a standard it registers, or defines in its glossary, is the reader's own once cited; a term from a discipline the reader need not know is not.

**The test —** the primary reader, arriving cold, understands the passage on the first read.

## Ordinals and Counts

Avoid numbers that add nothing a reader cannot already see but create friction when the set changes. A number restating a list's order or its size goes stale silently the moment an item is added or moved, and so does everything that refers to it. Say what things are, what they mean, or cite where they are; whoever needs a count can count them when they do the work.

- Nothing is numbered: not a heading, a bold lead-in, or a list item.
- Nothing refers to an item by its position, by number or by word ("step 5", "the second", "the latter"). Refer to it by its name.
- Nothing says how many things a list or the repo holds. Name them, describe them, or cite them.

Numbers that carry value stay. Algorithm tables keep their numbered steps, and references to those steps, because that numbering is an industry standard a cold agent reads without further instruction, as a software engineer would (`specs/methodology/modeling-constructs.md`). A Gherkin scenario states its own test case in full, and its numbers are that case's data. A value is not a count: a two-week window, a floor of two options, exactly one home. Neither is naming a pair, "both", "either" or "the two". Where something sits on the page is no count, and no way to refer to it either: other text is cited (`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`).

## Markdown

Each Markdown file in scope is written in GitHub Flavored Markdown (`specs/methodology/external-references.md § External References [Name: GFM]`). A field's form is `specs/methodology/modeling-constructs.md § Fields`'; a bold lead-in's, emphasis's and literal text's are `§ Bold Lead-ins`', `§ Emphasis`' and `§ Literal Text`'.

## Bold Lead-ins

A bold lead-in is a bold phrase, not a field (`specs/methodology/modeling-constructs.md § Fields`), opening a paragraph or a list item to label it for a reader scanning the page. It ends in an em dash inside the bold, with a space before the dash: `**The test —**`. Its words are in sentence case: the first word opens with a capital, and every other word is lower case but a name keeping its own casing, a construct's or a field's, a term an outside standard names or a proper noun. Sentence case is a requirement of style; what closes the bold, never its casing, tells a lead-in from a field, whose key is a field label (`specs/methodology/glossary.md`). When it introduces the block beneath it, a list, a table or paragraphs, it stands on a line of its own; otherwise the text it introduces follows it on its line. The character closing the bold tells the two apart: a colon makes a field, a dash a lead-in, and a bold phrase opening a line closes on nothing else. Unlike a field, its words are the author's own, defined by no form, so nothing looks one up by name, and nothing cites one (`specs/methodology/sourcing-and-citation.md § Writing a Citation`).

## Emphasis

Emphasis is italic, `*word*`, on a word or a short phrase inside a sentence, where stress changes what the sentence means. Italic is the one emphasis. Bold marks only a field (`specs/methodology/modeling-constructs.md § Fields`) or a bold lead-in (`§ Bold Lead-ins`), both opening a line. A line never opens with italic, since a phrase opening a line to label it is a lead-in. A point that needs more than italic is given structure instead: its own sentence, a lead-in, or, for a rule that must hold, a Constraint (`specs/methodology/modeling-constructs.md § Constructs § Constraint`).

## Literal Text

Backticks mark literal text: something written exactly so elsewhere, a path, a citation, an identifier, a field's key, a heading's title, a value, or a command, so a reader can copy it and a script can match it. A span opens and closes with one backtick, so literal text holds no backtick, but for a citation carrying a key value that holds one, whose span `specs/methodology/sourcing-and-citation.md § Writing a Citation` widens. A name is not literal text: a product, a method, a company, or a role is written plain, capitalized as a proper noun. A record type's Plural Name is literal where it stands for a section's title, `Open Questions`; the idea it names is plain prose, an open question.
