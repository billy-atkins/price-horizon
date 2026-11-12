## Markdown

Each Markdown file in scope is written in GitHub Flavored Markdown ([`specs/methodology/external-references.md § External References [Name: GFM]`](/specs/methodology/external-references.md#external-references)). [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) sets a field's form. [`§ Bold Lead-ins`](#bold-lead-ins), [`§ Emphasis`](#emphasis), [`§ Literal Text`](#literal-text) and [`§ Blank Lines`](#blank-lines) set the forms of a bold lead-in, emphasis, literal text and a blank line. A line continuing a list item is indented to the item's text ([`§ Markdown [GFM Elements.GFM: lazy continuation line]`](#markdown)). A list item ends before the first line that is not blank and is indented less than its text. A fenced block whose info string is `markdown` holds a file of its own. Each check reading the block reads that file from the line directly beneath the opening fence to the line directly above the closing one. Toward what stands outside it, the block is one code block.

**What the mapping means.** The canon writes GFM's blocks as GFM does. Where a form of the canon's is one of GFM's elements, as each paragraph of a block of fields is GFM's paragraph, the canon names the element its own way. It writes one element otherwise: a list item's continuation line, as [`§ Markdown [GFM Elements.GFM: lazy continuation line]`](#markdown) has it. GFM Elements maps each element the canon names its own way, and the one it writes otherwise, as [`specs/methodology/sourcing-and-citation/external-reference.md § External Reference § A Mapping onto a Standard`](/specs/methodology/sourcing-and-citation/external-reference.md#a-mapping-onto-a-standard) has a mapping written, so a reader finds the standard's term for each form and the reason for the departure:

**Table Name:** GFM Elements \
**Reference Key:** GFM \
**Required:** Section, Treatment

| GFM | Section | Treatment | Departs For | Why |
|---|---|---|---|---|
| paragraph | 4.8 | the same, a block of fields' paragraph | | |
| hard line break | 6.12 | the same, a field's end, written as a backslash, a space before it | | |
| list item | 5.2 | the same, a record, a list item opening a field's key | | |
| lazy continuation line | 5.2 | not written, a line continuing a list item indented to the item's text | the canon's form | a reader and a script tell where an item ends by its indentation alone |

## Blank Lines

Items of one kind stand together, in the order they are read, and a blank line separates groups that differ, so a reader sees a file's shape at a glance and chooses which group to read in detail. A code style groups like statements the same way. Each line of a file opens or continues one of these elements:
- a heading;
- a field: a line opening a field's key, as [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) has one;
- a record: a list item opening a field's key;
- a list item: any other;
- a table;
- a code block, fenced or indented;
- a thematic break;
- front matter;
- a paragraph: any other text, a lead-in among it.

The table's condition Ends a list item? is true where the element above is a list item's last line and the element below stands outside that item, as [`§ Markdown`](#markdown) has a list item end. A nested record's last field ends its item before the outer record's next field, and a record's last field ends its item before the next record. The condition Nested beneath the field above? is true where the element below is a field whose key stands two spaces beyond the key of the field above, as [`specs/methodology/modeling-constructs.md § Fields § A Nested Construct`](/specs/methodology/modeling-constructs.md#a-nested-construct) has a nested block stand. The table's row for groups that differ gives each blank line GFM needs. Where a blank line falls:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** The element above, The element below, Ends a list item?, Nested beneath the field above? \
**Annotations:** Why \
**Input Values:**
  - The element above: "front matter", "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break"
  - The element below: "a heading", "a paragraph", "a field", "a record", "a list item", "a table", "a code block", "a thematic break"

| The element above | The element below | Ends a list item? | Nested beneath the field above? | A blank line between? | Why |
|---|---|---|---|---|---|
| "a field", "a record" | "a field" | false | true | true | a field's text and the construct nested beneath it, the block standing as [`specs/methodology/modeling-constructs.md § Fields § A Nested Construct`](/specs/methodology/modeling-constructs.md#a-nested-construct) has it. Where no blank line stands, GFM reads the block's first field as continuing the field's paragraph |
| "a field", "a record" | a field | false | - | false | one block's fields, a paragraph whose hard line breaks render each field on a line of its own |
| "a field", "a record" | "a list item", "a record" | false | - | false | a field's list, of plain items or of records, directly beneath its key |
| "a paragraph", "a list item" | a list item | - | - | false | a list beneath the sentence or the lead-in introducing it, and the items of one plain list |
| - | - | - | - | true | groups that differ, records one after another and a field after a list or after a nested record among them. Where no blank line stands, GFM joins two paragraphs, reads a paragraph's line after a list item as continuing it and adds a row to a table |

A blank line missing where the table gives true, or standing where it gives false, is reported. A fenced block whose info string is `markdown` is read as [`§ Markdown`](#markdown) has it, so it is one element toward the lines around it. Any other code block is one element.

## Bold Lead-ins

A bold lead-in labels a paragraph or a list item for a reader scanning the page. It is a bold phrase opening the paragraph or the item, and it ends in a period inside the bold, as the run-in heading of edited writing does: `**The test.**`. A lead-in phrased as a question ends in its question mark. The sentence after it opens with a capital.

A lead-in is not a field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)). The character closing the bold tells the two apart: a colon makes a field, and a period or a question mark a lead-in. A bold phrase opening a line closes on nothing else.

A lead-in is written in sentence case, as a requirement of style. Its first word opens with a capital, and every other word is lowercase but a name keeping its own casing: a construct's or a field's, a term an outside standard names, or a proper noun. The closing character alone tells a lead-in from a field, whose key is a field label ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), whatever the casing.

A lead-in introducing the block beneath it (a list, a table or paragraphs) stands on a line of its own. Otherwise the text it introduces follows it on its line.

A lead-in at a rule's home names what it labels. It states no rule.

A lead-in's words are the author's own, defined by no form, so nothing looks one up by name, and nothing cites one ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation)).

## Emphasis

Emphasis is italic, `*word*`, on a word or a short phrase inside a sentence, where stress changes what the sentence means. Italic is the one emphasis. Bold marks only a field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)) or a bold lead-in ([`§ Bold Lead-ins`](#bold-lead-ins)), both opening a line. A line never opens with italic, since a phrase opening a line to label it is a lead-in. A point that needs more than italic is given structure instead: a sentence of its own, a lead-in, or, for a rule that must hold, a Constraint ([`specs/methodology/modeling-constructs.md § Constructs § Constraint`](/specs/methodology/modeling-constructs.md#constraint)).

## Literal Text

Backticks mark literal text: something written exactly so elsewhere, such as a path, a citation, an identifier, a field's key, a heading's title, a value or a command, so a reader can copy it and a script can match it. A span opens and closes with one backtick, so literal text holds no backtick. The exception is a citation carrying a key value that holds one, whose span [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) widens. A name is not literal text: a product, a method, a company, or a role is written plain, capitalized as a proper noun. A record type's Plural Name is literal where it stands for a section's title, `Open Questions`. The idea it names is plain prose, an open question.
