## What a Finished Spec Reads Like

A finished spec describes a destination, not the conversation that produced it. A reader arriving cold, with no visibility into any draft, discussion, or rejected alternative that came before, should be able to read any sentence and take it at face value.

Content that only makes sense to someone present for the discussion that produced it does not belong in a spec, however useful it was to sort out at the time.

| Pattern | Example | Instead |
|---|---|---|
| Meta-commentary about the act of writing | "worth stating plainly," "worth being explicit about," "a principle worth stating rather than leaving implicit" | state the principle; do not narrate the decision to state it |
| Arguing against an alternative the document never proposed | defining a chosen approach by contrast with a technology mentioned nowhere else | state what was chosen and why it is right, on its own terms |
| Referencing the document's own revision history | "as discussed," "this corrects an earlier version," "now formalized," "the same way the current one did" | a spec has one state, the current one |
| Hedged framing left over from drafting | "for now," "at this point," attached to a settled decision | state a final decision as final; record a genuinely open one as a tracked question rather than hedging it inside settled prose |

## Trade-offs Are Not Journey Language

This is not a rule against explaining trade-offs. A genuine engineering trade-off belongs in the spec with its reasoning, because it teaches a reader how to make the same kind of call correctly in a new situation.

**The test:** does the comparison state a timeless design principle a cold reader can apply elsewhere, or does it only make sense to someone who watched the alternative get proposed and rejected?

Choosing a star schema over a snowflake schema passes: the reasoning transfers to the next schema decision. Choosing a DAG over a state machine for an acyclic process passes for the same reason. Ruling out a technology the document never otherwise mentions fails: nothing in the document gave a cold reader anything to reject.

A distinction drawn against something a reader has a live, document-supported reason to ask about also passes. The question is whether the reader could plausibly have arrived at the alternative themselves, not whether an author once did.
