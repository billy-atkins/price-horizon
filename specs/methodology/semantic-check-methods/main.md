## Semantic Check Methods

A semantic check ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) is made by reading. This document says how each semantic check that more than one skill needs is made: how its reader finds what to judge, what is easy to miss, how the reader judges, and how a finding is fixed. It is written for a reader who has been given files to read.

This document leaves to where the reader's run is set which files the reader is given, where the reader's candidate lists come from, and what the reader reports. It states no rule the files must follow. [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over`](/specs/AGENTS.md#the-scope-a-check-runs-over) says where each check's entry is found, and the entry names the sections whose rules the check reads the files against. A check's text here cites a section only where one of its judgments uses that section's rule.

Each check has a file of its own in this document's folder, named for the check. This file holds what the checks share.

**Reading in full.** The reader reads the files themselves, as [`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure) has a file read. Headings alone, an earlier read and memory are not enough. A summary built from headings and memory misses the largest gap in what it summarizes.

**The source beside the passage.** Some checks compare a passage with the text it restates. The reader opens that text and reads the two side by side. Reading the passage alone shows only that it reads well, and a restatement always reads well. The defect shows only with the source beside it.

**A candidate list.** Where a candidate list comes with a check, the reader takes it first and then reads the files in full. [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over`](/specs/AGENTS.md#the-scope-a-check-runs-over) has the list guide the reading and never limit it. A breach the list missed is a finding like any other.

**The side that is wrong.** A finding names the rule it breaks and the place breaking it. Where two places disagree, the reader says which one is wrong, since the fix goes there.

### How a Summary Distorts Its Source

A summary shortens its source. Each clause that turns a paragraph into a phrase can say something the source does not. An overview has to shorten, as [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) has an `architecture.md` describe its tree in its own words. A diagram shortens too, and so does a passage that says in its own words what another section states. The ways shortening goes wrong, the most common first:
- **A dropped condition that mattered.** The source says a capability works "though never carrying X". The summary says it works. The exception was the protection, so the summary now promises more than the system does.
- **A default turned into the only way.** The source says a path is "the default" among several. The summary says it is how the thing works.
- **A count given where the source lists.** The source names two behaviors and points at a third elsewhere. The summary says "two ways", which reads as the full set and is not.
- **A reference left pointing at nothing.** The summary keeps "than that window allows" after deleting the clause that named the window.

The reader takes each clause of the summary with its source open and asks two questions. What did the source say that the clause does not? Does the difference change what a reader concludes?

The checks that read for these faults are [`specs/methodology/semantic-check-methods/directory-summary-currency.md § Directory Summary Currency`](/specs/methodology/semantic-check-methods/directory-summary-currency.md#directory-summary-currency), [`specs/methodology/semantic-check-methods/diagram-currency.md § Diagram Currency`](/specs/methodology/semantic-check-methods/diagram-currency.md#diagram-currency), and [`specs/methodology/semantic-check-methods/whether-the-home-holds-the-fact.md § Whether the Home Holds the Fact`](/specs/methodology/semantic-check-methods/whether-the-home-holds-the-fact.md#whether-the-home-holds-the-fact) wherever a citing passage says in its own words what the cited section states. The other checks compare no two versions of one passage, so they do not read for them.

### A Passage Still Stating Replaced Wording

A change to what a section states leaves two kinds of place to read again. Each takes a search of its own:
- **By citation.** The reader gathers every citation of the changed section. This finds each passage that cites it. It does not find a passage that restates the fact and cites nothing.
- **By wording.** The reader takes a distinctive phrase from the wording the change replaced and searches the files for it. This finds each passage still stating the old fact, whether or not the passage cites anything.

The reader makes both searches, because each finds what the other misses. A passage that restates without citing is common in the places meant to follow a change: a diagram, the prose of an `architecture.md`, and a table row showing a rule stated elsewhere. A search by citation alone can come back clean while copies of the old wording still stand in a paragraph and in a diagram's node, neither of them citing anything.
