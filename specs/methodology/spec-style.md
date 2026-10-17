## What a Finished Spec Reads Like

A finished spec describes a destination. The conversation that produced it stays out of it. A reader arriving cold has seen no draft, discussion or rejected alternative that came before. That reader should be able to read any sentence and take it at face value.

Content that only makes sense to someone present for the discussion that produced it does not belong in a spec, however useful it was to sort out at the time.

**Reference Key:** Pattern

**Required:** Example, Instead

| Pattern | Example | Instead |
|---|---|---|
| Meta-commentary about the act of writing | "worth stating plainly," "worth being explicit about," "a principle worth stating rather than leaving implicit" | state the principle, without narrating the decision to state it |
| Arguing against an alternative the document never proposed | defining a chosen approach by contrast with a technology mentioned nowhere else | state what was chosen and why it is right, on its own terms |
| Referencing the document's own revision history | "as discussed," "this corrects an earlier version," "now formalized," "the same way the current one did" | a spec has one state, the current one |
| Hedged framing left over from drafting | "for now," "at this point," attached to a settled decision | state a final decision as final, and record a genuinely open one as an open question ([`specs/methodology/spec-placement.md § Open Question`](/specs/methodology/spec-placement.md#open-question)) instead of hedging it inside settled prose |

## Trade-offs Are Not Journey Language

[`§ What a Finished Spec Reads Like`](#what-a-finished-spec-reads-like) is not a rule against explaining trade-offs. A genuine engineering trade-off belongs in the spec with its reasoning, because it teaches a reader how to make the same kind of call correctly in a new situation.

**The test.** A comparison passes when either holds:

- it states a timeless design principle a cold reader can apply elsewhere;
- it is drawn against something the reader has a live, document-supported reason to ask about: an alternative the reader could plausibly have arrived at alone, whether or not an author once did.

It fails when it makes sense only to someone who watched the alternative get proposed and rejected.

Choosing a star schema over a snowflake schema passes: the reasoning transfers to the next schema decision. Choosing a DAG over a State Machine for an acyclic process passes for the same reason. Ruling out a technology the document never otherwise mentions fails: nothing in the document gave a cold reader anything to reject.

## Clear Prose

Clear prose is measured by the effort it costs its primary reader. The shorter passage is not always the clearer one. Each kind of file this section reaches is written for a primary reader, without failing its secondary one:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Files

| Files | Primary reader | Secondary reader | Can Assume |
|---|---|---|---|
| The product specs | a product owner | an agent | the domain and the product's own terms, and no implementation vocabulary |
| The technical specs | a software engineer | an agent | common engineering terms, and the product specs it cites |
| "The methodology", "[`specs/architecture.md`](/specs/architecture.md)", "`specs/index.md`", "`specs/application/index.md`" | a practitioner, a software engineer designing a project's specs | an agent | software engineering and the standards the canon registers, and no term of the methodology's own until it is defined |
| "The agent instructions", "The skills" | a cold agent | a software engineer | only what the step cites |
| The documentation | a person evaluating the project's work, an engineering leader among them | a software engineer deciding whether to adopt it | software engineering, and nothing of the project's own until it is introduced |
| The working files | the user steering the work | a cold agent reviewing it | the work in hand and its own record |

The working files are written to this section like any other file, but no audit reads them for it, as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) records. Each serves the work in progress, and none is committed ([`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files)).

A software engineer designs the agent instructions and the skills, deciding what they say and approving them. An agent writes them for a cold agent. In the end, they are judged by how an agent behaves under them.

**Documentation's voice.** Documentation is written for its reader. A guide walking the reader through a task speaks to them as "you", and an explanation of how something works takes a neutral voice. The author writes "I" only where the author is the subject: an introduction of the author, or a signed account of the work's origins, kept apart from the rest of the documentation. Documentation may draw its examples from the application specs, the worked example a newcomer learns the methodology from.

**A formal register.** Spec of Record writes formally, the documentation included, so no file in scope uses a contraction: "does not", never "doesn't". A contraction suits informal writing between people, and these files are professional work. A title, a name or a quotation is written as it stands, contraction and all. Quotation marks are straight, the form a script matches. A sentence takes a period, a comma, a colon or parentheses where a dash might stand. The em dash has become a mark of machine-written text.

**American English.** Spec of Record is written in American English, in both its spelling and its usage. A script's comments and the messages the script prints are written in it too. One spelling throughout lets a reader meet one author. It also lets a search for a word find every use of the word. A word is spelled as Merriam-Webster spells it. Where Merriam-Webster gives two spellings, the word takes the first ([`specs/methodology/external-references.md § External References [Name: Merriam-Webster]`](/specs/methodology/external-references.md#external-references)). So "behavior", "color", "installment" and "organize" are written, never "behaviour", "colour", "instalment" or "organise". A usage that turns on context is written as American English has it. Parties agree on what they decide together, and one agrees to what another proposes: the user and the builder agree on the goals, and the user agrees to the frame, never "agrees the goals". What comes later comes "in the future", never "in future".

**A name from outside keeps its spelling.** A name from outside the specs keeps its spelling, a British form or a typo included, as a title and a quotation do. Such a name is a standard's, a product's, or one that code already holds, whether in a skill's scripts or in the product's code: an identifier, a database column, an API field or a package. Respelling a name the project holds changes what other code, stored data, a test or a user relies on, as an extract feeding a data warehouse relies on a column's name. A name the specs give, such as a heading's, a state's or a fact's, is written in American English. A name the specs take from code, such as a state named for a value code holds, is spelled as the code holds it. An agent that notices a British form or a typo in a name the project holds tells the user what a respelling would change. Before the system ships, a respelling changes little but the code and its specs, so the agent recommends it. Once the system is in production, a respelling changes every consumer of the name, so the user weighs whether it is worth its cost. A name is respelled only when the user requests or approves it.

**Cut what carries nothing.** Every word read costs the reader, and costs an agent tokens too. So filler, a point made twice, and commentary on the writing itself are cut. [`§ What a Finished Spec Reads Like`](#what-a-finished-spec-reads-like) covers the commentary.

**Keep what carries the reader.** A word that carries meaning, or carries the reader from one idea to the next, stays. Prose cut too far fails as surely as prose padded out. Minified code is shorter than its source and unreadable, because minifying removes what a reader uses and a machine does not need:

**Reference Key:** Minified Code Removes

**Required:** Too-terse Prose Drops, Instead

| Minified Code Removes | Too-terse Prose Drops | Instead |
|---|---|---|
| meaningful names, leaving `a` and `b` | the term itself, a pronoun standing far from what it names | name the term again |
| comments saying why | "because" and "so", the reason linking two facts | state the reason |
| one statement per line | one idea per sentence, several packed into one | give each idea a sentence of its own |
| whitespace and structure | paragraph breaks, lists and headings showing how ideas relate | give the ideas their structure |

**One idea per sentence.** A sentence usually comes to hold several ideas through a chain of qualifying clauses: a main clause, then clause after clause joined by commas, each qualifying the one before. Each clause is easy to write, and the whole is hard to read. "The job reads the queue, which the loader fills, whose records carry a batch number, used to order them" becomes "The job reads the queue. The loader fills it, and each record carries a batch number. The job orders the records by it." A finished sentence can also grow a tail: a clause opening with ", meaning", ", ensuring" or ", unlike". The chain and the tail are split into sentences, or into a list when the parts are alike. A long sentence that ends on its reason, opened by a word such as ", so" or ", because", gives the reason a sentence of its own that keeps the link: "The service retries each request, because the network drops packets" becomes "The network drops packets. So the service retries each request."

**Rhythm.** A paragraph of long sentences with no short one between reads as machine-made, and tires the reader. People mix short sentences with long ones. A short sentence gives the reader a place to rest, as "The cache is cold." does between two long ones explaining why a request is slow.

**No comma splice.** Two complete statements joined only by a comma become two sentences. A reader takes a comma for a pause inside one statement, and stumbles when a second statement follows it. "The index is rebuilt nightly, it is stale by noon" becomes "The index is rebuilt nightly. It is stale by noon."

**A semicolon that leans.** A sentence ends with a period by default. A semicolon joins a clause that leans on the one before it. Standing as a sentence of its own, such a clause would have to restate what the clause before it established. "Reads go to the replica; writes, to the primary" earns its semicolon: the clause on writes borrows "go" from the clause on reads. "The cache is warm; requests return quickly" does not, since "requests return quickly" is a sentence on its own: "The cache is warm. Requests return quickly." A semicolon never separates items in running prose. Items that hold commas of their own become a list.

**Say what a thing is.** A sentence states what a thing is. What it is not is stated only where a reader would otherwise assume it, and then in a sentence of its own. A contrast such as "X, not Y", "rather than" or "not just X, but Y", piled into one sentence, makes the reader hold two things to learn one. "The cache holds pages, not queries" becomes "The cache holds pages" where no reader would think it held queries. [`§ Trade-offs Are Not Journey Language`](#trade-offs-are-not-journey-language) tests a contrast that earns its place.

**State a rule positively.** A rule says what holds, since the reader acts on what holds. "Never" is kept for a prohibition that is itself the rule. A "never X, always Y" pair drops whichever half the other already says, because each half adds a thing for the reader to hold: "A field is always filled and never left empty" becomes "A field is always filled".

**Name the actor.** A sentence describing what a system or a person does names who does it: "the payroll service writes the payslip", rather than "the payslip is written". The reader then knows where to look when the payslip is wrong. A rule may take the passive, since what matters in a rule is the thing it governs: "a citation is written inside a single backtick span" makes the citation its subject.

**Name the noun again.** A chain of "its" makes the reader work out which noun each pronoun means. Where two nouns could be meant, or the noun is more than a clause back, the noun is named again. "Its own" and "itself" are dropped wherever "its", or nothing, says the same. "A definition sets its fields and its defaults, and each instance sets its own values within its bounds" becomes "A definition sets the fields and their defaults. Each instance sets values within what the definition allows."

**One term, one meaning.** A term is defined where it first appears and used the same way after it. A word is never varied for variety: a reader and an agent alike take a new word to mean a new thing. A spec calling a thing "the queue" calls it "the queue" throughout, never "the backlog" a paragraph later. So "step" names a step of a workflow and nothing else. A thing kept logically the same as what it follows, as a materialized view is kept with its sources, is in sync or out of sync with it, never in step.

**Words kept only for their value.** A word or phrase stays only where it is natural and adds real value to its sentence. An emphasis word goes when deleting it does not change the meaning. "Fundamentally, this is really about deliberately creating a more robust and scalable engineering organization" becomes "This requires building an engineering organization that can scale": with the emphasis and the vague claims gone, what the sentence asks for is plain. No term in the Emphasis Words and Generic Terms tables is banned. None has a stock replacement either, because a stock word soon becomes the next overused term. Each table names a term and why it tends to go wrong. The author finds the right words for the sentence, often none.

**Table Name:** Emphasis Words

**Reference Key:** Term

**Required:** Why

| Term | Why |
|---|---|
| actually | adds an unneeded correction or contrast |
| exactly | validates or reinforces a point, where it states no count or match |
| just | softens a statement or makes a complex thing sound small |
| genuinely | adds artificial sincerity or enthusiasm |
| deliberately | makes an ordinary decision sound strategic |
| simply | presents a complex topic as straightforward |
| really | adds generic emphasis |
| truly | adds emotional emphasis without substance |
| clearly | asserts certainty instead of showing it |
| obviously | assumes something is self-evident |
| crucially | emphasizes a point artificially |
| importantly | introduces information as significant without showing why |
| essentially | summarizes or simplifies |
| fundamentally | makes an observation sound more profound than it is |
| basically | introduces a simplified explanation |

**Table Name:** Generic Terms

**Reference Key:** Term

**Required:** Why

| Term | Why |
|---|---|
| leverage | a grander word for using something |
| robust | a vague claim of quality |
| seamless | generic marketing language |
| transformative | exaggerates significance |
| elevate | a vague claim of improvement |
| unlock | marketing-style exaggeration |
| navigate | a worn metaphor for handling complexity |
| landscape | a vague reference to an industry or a setting |
| nuanced | an unneeded qualification |
| underscore | a grander word for showing |
| foster | a corporate-sounding word for encouraging |
| delve | a tell of machine-written text |
| pivotal | exaggerates significance |
| comprehensive | a vague claim of completeness |
| holistic | a vague claim of completeness |
| streamline | a vague claim of improvement |
| crucial | emphasizes artificially |
| serves as | a roundabout "is" |
| stands as | a roundabout "is" |
| in short | a formulaic summary |
| it is worth noting | an unneeded introduction |
| at its core | an artificially profound introduction |
| the key takeaway | a formulaic summary |

**Patterns of machine-written prose.** Each is read for and removed, since each spends the reader's attention on cadence instead of content:

- a slogan closing a paragraph, a point already made restated in a form no reader can apply, as "Two copies of a rule are not redundancy; they are a defect waiting to happen";
- a matching triplet listed for its cadence where one item is meant, as "fast, reliable and scalable" for a service only ever said to be fast;
- stacked abstractions where a concrete noun would do, as "an enablement of cross-team alignment" for "the teams agree on the schema".

**An analogy.** An analogy brings a reader to a new rule through something already familiar. What is familiar depends on who is reading. The author chooses one for the file's primary reader, as the table of readers in this section names that reader and what it can assume. Analogies are kept, and added where a rule's reason is not obvious. An analogy that follows its rule is no slogan and no point made twice: it carries the rule to the reader by another road, where a slogan only restates it. So a rewrite never removes one to shorten a passage. The specs, the agent instructions and the skills are read for reference. In them, an analogy follows the rule it explains, in a sentence of its own. The documentation is read to learn, and in it an analogy may lead. An analogy is never wedged into a rule's clause, where it competes with the rule.

**An example in the canon.** An example maps what a reader does not yet know onto what it does. An example from outside the house lands with any agent, from the agent's training. An example drawn from the application specs, from their files, domains or vocabulary, lands only with an agent that has already read them. A cold agent loads only what its step needs, and often has not read them. So an example in the canon is never drawn from the application specs. The one exception names the project the canon is checked in, and illustrates no rule. The methodology may illustrate itself.

**Words its reader already uses.** A rule is written in words its reader can apply without looking anything up. Where its words alone leave the reader unsure, it gives an example of what passes and what fails: a heading "names a thing, as `Payroll Run`, or asks the question its construct answers, never an activity, as `Running payroll`" ([`specs/methodology/modeling-constructs.md § Constructs § Declared Construct`](/specs/methodology/modeling-constructs.md#declared-construct)). A grammarian's term for either would leave the reader looking it up. A term the canon adopts from a standard it registers, or defines in its glossary, is the reader's own once cited. A term from a discipline the reader need not know is not.

**What a rewrite keeps.** A rewrite for clarity changes how a passage reads. What the passage states stays as it was. A passage that cannot be made clear without changing what it states needs a change to the design. A rewrite keeps the reason with each rule, so a cold reader can apply the rule to a case its author did not foresee. It keeps the structure: the constructs, the fields, the lead-ins and the citations make the text checkable. They serve the agent, while the sentences serve the person. In the documentation, it keeps the author's own voice: the first person where the author is the subject, and the author's plain phrasing. A rewrite that is shorter but needs a second read has failed, as minified code does.

**The test.** The primary reader, arriving cold, understands the passage on the first read.

## Ordinals and Counts

Avoid numbers that add nothing a reader cannot already see but create friction when the set changes. A number restating a list's order or its size goes stale silently the moment an item is added or moved, and so does everything that refers to it. Say what things are, what they mean, or cite where they are. Whoever needs a count can count them when they do the work.

- Nothing is numbered: not a heading, a bold lead-in, or a list item.
- Nothing refers to an item by its position, by number or by word ("step 5", "the second", "the latter"). Refer to it by its name.
- Nothing says how many things a list or the repo holds. Name them, describe them, or cite them.

Numbers that carry value stay. Algorithm tables keep their numbered steps, and references to those steps, because that numbering is an industry standard a cold agent reads without further instruction, as a software engineer would ([`specs/methodology/modeling-constructs.md`](/specs/methodology/modeling-constructs.md)). A Gherkin scenario states its own test case in full, and its numbers are that case's data. A value is not a count: a two-week window, a floor of two options, exactly one home. Neither is naming a pair, "both", "either" or "the two". Where something sits on the page is no count, and no way to refer to it either: other text is cited ([`specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`](/specs/methodology/sourcing-and-citation.md#referring-to-other-text)).

## Markdown

Each Markdown file in scope is written in GitHub Flavored Markdown ([`specs/methodology/external-references.md § External References [Name: GFM]`](/specs/methodology/external-references.md#external-references)). [`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields) sets a field's form. [`§ Bold Lead-ins`](#bold-lead-ins), [`§ Emphasis`](#emphasis) and [`§ Literal Text`](#literal-text) set the forms of a bold lead-in, emphasis and literal text.

## Bold Lead-ins

A bold lead-in labels a paragraph or a list item for a reader scanning the page. It is a bold phrase opening the paragraph or the item, and it ends in a period inside the bold, as the run-in heading of edited writing does: `**The test.**`. A lead-in phrased as a question ends in its question mark. The sentence after it opens with a capital.

A lead-in is not a field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)). The character closing the bold tells the two apart: a colon makes a field, and a period or a question mark a lead-in. A bold phrase opening a line closes on nothing else.

A lead-in is written in sentence case, as a requirement of style. Its first word opens with a capital, and every other word is lower case but a name keeping its own casing: a construct's or a field's, a term an outside standard names, or a proper noun. The closing character alone tells a lead-in from a field, whose key is a field label ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), whatever the casing.

A lead-in introducing the block beneath it (a list, a table or paragraphs) stands on a line of its own. Otherwise the text it introduces follows it on its line.

A lead-in's words are the author's own, defined by no form, so nothing looks one up by name, and nothing cites one ([`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation)).

## Emphasis

Emphasis is italic, `*word*`, on a word or a short phrase inside a sentence, where stress changes what the sentence means. Italic is the one emphasis. Bold marks only a field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)) or a bold lead-in ([`§ Bold Lead-ins`](#bold-lead-ins)), both opening a line. A line never opens with italic, since a phrase opening a line to label it is a lead-in. A point that needs more than italic is given structure instead: a sentence of its own, a lead-in, or, for a rule that must hold, a Constraint ([`specs/methodology/modeling-constructs.md § Constructs § Constraint`](/specs/methodology/modeling-constructs.md#constraint)).

## Literal Text

Backticks mark literal text: something written exactly so elsewhere, such as a path, a citation, an identifier, a field's key, a heading's title, a value or a command, so a reader can copy it and a script can match it. A span opens and closes with one backtick, so literal text holds no backtick. The exception is a citation carrying a key value that holds one, whose span [`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation) widens. A name is not literal text: a product, a method, a company, or a role is written plain, capitalized as a proper noun. A record type's Plural Name is literal where it stands for a section's title, `Open Questions`. The idea it names is plain prose, an open question.
