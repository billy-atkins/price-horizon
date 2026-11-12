## What a Finished Spec Reads Like

A finished spec describes a destination. The conversation that produced it stays out of it. A reader arriving cold has seen no draft, discussion or rejected alternative that came before. That reader should be able to read any sentence and take it at face value.

Content that only makes sense to someone present for the discussion that produced it does not belong in a spec, however useful it was to sort out at the time.

**Reference Key:** Pattern \
**Required:** Example, Instead

| Pattern | Example | Instead |
|---|---|---|
| Meta-commentary about the act of writing | "worth stating plainly," "worth being explicit about," "a principle worth stating rather than leaving implicit" | state the principle, without narrating the decision to state it |
| Arguing against an alternative the document never proposed | defining a chosen approach by contrast with a technology mentioned nowhere else | state what was chosen and why it is right, on its own terms |
| Referencing the document's own revision history | "as discussed," "this corrects an earlier version," "now formalized," "the same way the current one did" | a spec has one state, the current one |
| Hedged framing left over from drafting | "for now," "at this point," attached to a settled decision | state a final decision as final, and record a genuinely open one as an open question ([`specs/methodology/spec-placement/open-question.md § Open Question`](/specs/methodology/spec-placement/open-question.md#open-question)) instead of hedging it inside settled prose |

## Trade-offs Are Not Journey Language

[`§ What a Finished Spec Reads Like`](#what-a-finished-spec-reads-like) is not a rule against explaining trade-offs. A genuine engineering trade-off belongs in the spec with its reasoning, because it teaches a reader how to make the same kind of call correctly in a new situation.

**The test.** A comparison passes when either holds:
- it states a timeless design principle a cold reader can apply elsewhere;
- it is drawn against something the reader has a live, document-supported reason to ask about: an alternative the reader could plausibly have arrived at alone, whether or not an author once did.

It fails when it makes sense only to someone who watched the alternative get proposed and rejected.

Choosing a star schema over a snowflake schema passes: the reasoning transfers to the next schema decision. Choosing a DAG over a State Machine for an acyclic process passes for the same reason. Ruling out a technology the document never otherwise mentions fails: nothing in the document gave a cold reader anything to reject.
