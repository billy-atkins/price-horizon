## Finished Style

This check reads the prose for whether it reads as a finished spec.

**The candidates, then the files in full.** Where a candidate list comes with the check, the reader takes it as a guide and then reads the files in full, as [`specs/methodology/making-a-semantic-check/main.md § Making a Semantic Check`](/specs/methodology/making-a-semantic-check/main.md#making-a-semantic-check) has a candidate list used. A candidate list holds nothing from a table or a heading, so the reader reads those whole.

**When a candidate is a finding.** A listed word is a finding only where it adds nothing to its sentence. An emphasis word is one example: if deleting it leaves the meaning the same, it adds nothing. A listed construction is a finding where it breaks the rule of [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose) that names it. A chain of "its" that leaves its noun unclear breaks one, and so does a semicolon that does not lean. A trade-off that passes the test of [`specs/methodology/spec-style/what-a-finished-spec-reads-like.md § Trade-offs Are Not Journey Language`](/specs/methodology/spec-style/what-a-finished-spec-reads-like.md#trade-offs-are-not-journey-language) is set aside, with that reason.

**What no list holds.** [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose) asks for things no script can list. The reader reads by meaning for:
- a sentence that says what a system or a person does without naming who does it;
- a term changed only for variety;
- a pattern of machine-written prose;
- an analogy that a rewrite removed, or one forced into a rule's clause;
- a spelling or a usage that is not American English, which is no finding in a quotation, a title or a name from outside the specs;
- an example in the canon taken from the application specs. Any listed path into the application specs is where to start. That section keeps one exception, which is no finding.

**The first read.** The reader reads each passage once, as the reader the passage is written for. A passage that takes a second read is a finding. Its fix rewords it without changing what it states.
