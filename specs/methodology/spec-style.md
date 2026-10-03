## What a Finished Spec Reads Like

A finished spec describes a destination, not the conversation that produced it. A reader arriving cold, with no visibility into any draft, discussion, or rejected alternative that came before, should be able to read any sentence and take it at face value.

Content that only makes sense to someone present for the discussion that produced it does not belong in a spec, however useful it was to sort out at the time.

| Pattern | Example | Instead |
|---|---|---|
| Meta-commentary about the act of writing | "worth stating plainly," "worth being explicit about," "a principle worth stating rather than leaving implicit" | state the principle; do not narrate the decision to state it |
| Arguing against an alternative the document never proposed | defining a chosen approach by contrast with a technology mentioned nowhere else | state what was chosen and why it is right, on its own terms |
| Referencing the document's own revision history | "as discussed," "this corrects an earlier version," "now formalized," "the same way the current one did" | a spec has one state, the current one |
| Hedged framing left over from drafting | "for now," "at this point," attached to a settled decision | state a final decision as final; record a genuinely open one as an open question (`specs/methodology/spec-placement.md § An Open Question`) rather than hedging it inside settled prose |

## Trade-offs Are Not Journey Language

This is not a rule against explaining trade-offs. A genuine engineering trade-off belongs in the spec with its reasoning, because it teaches a reader how to make the same kind of call correctly in a new situation.

**The test —** does the comparison state a timeless design principle a cold reader can apply elsewhere, or does it only make sense to someone who watched the alternative get proposed and rejected?

Choosing a star schema over a snowflake schema passes: the reasoning transfers to the next schema decision. Choosing a DAG over a state machine for an acyclic process passes for the same reason. Ruling out a technology the document never otherwise mentions fails: nothing in the document gave a cold reader anything to reject.

A distinction drawn against something a reader has a live, document-supported reason to ask about also passes. The question is whether the reader could plausibly have arrived at the alternative themselves, not whether an author once did.

## Clear Prose

Clear prose is measured by the effort it costs its primary reader, not by its count of words. Each kind of file this section reaches is written for a primary reader, without failing its secondary one:

| Files | Primary reader | Secondary reader |
|---|---|---|
| The specs, the methodology among them | a person, the designer who must read and steer them | an agent |
| The agent instructions and the skills | a cold agent | a person |

The working files are outside this section. A person designs the agent instructions and the skills, deciding what they say and approving them, and an agent writes them for a cold agent. They are judged, in the end, by how an agent behaves under them.

**Cut what carries nothing —** every word read costs the reader, and costs an agent tokens too. So filler, a point made twice, and commentary on the writing itself are cut; `§ What a Finished Spec Reads Like` covers the commentary.

**Keep what carries the reader —** a word that carries meaning, or carries the reader from one idea to the next, stays. Prose cut too far fails as surely as prose padded out. Minified code is shorter than its source and unreadable, because minifying removes what a reader uses and a machine does not need:

| Minified code removes | Too-terse prose drops | Instead |
|---|---|---|
| meaningful names, leaving `a` and `b` | the term itself, a pronoun standing far from what it names | name the term again |
| comments saying why | "because" and "so", the reason linking two facts | state the reason |
| one statement per line | one idea per sentence, several packed into one | give each idea a sentence of its own |
| whitespace and structure | paragraph breaks, lists and headings showing how ideas relate | give the ideas their structure |

**A chain of qualifying clauses —** the usual way one sentence comes to hold several ideas: a main clause, then clause after clause joined by commas, each qualifying the one before. Each clause is easy to write, and the whole is hard to read. Split the chain into sentences, or into a list when its parts are alike.

**The test —** the primary reader, arriving cold, understands the passage on the first read.
