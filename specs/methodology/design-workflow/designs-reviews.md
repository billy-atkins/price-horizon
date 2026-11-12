## A Design's Reviews

A design's Kind sizes its reviews and its audit. The effort they take grows with what a flaw in the design would cost. A design whose Target names files or directories of more than one Kind takes the highest effort among them. The kinds of the files and directories its Target names pick its audit, each one's kind as [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) defines it. Where they include `code`, the audit is `.ai/skills/verify-spec-implementation/`'s full run. Where they include any other kind, it is an `.ai/skills/audit-specs/` run given those kinds as the skill's `--kind`. A design whose Target names both runs both. A run of `.ai/skills/audit-specs/` given kinds, `canon-specs` not among them, covers the files of those kinds. A run given `canon-specs` covers every kind but `code` and `none`, since a change to the canon can leave any such file in breach of it, the application specs among them. A run the user starts with no kind is the full run, covering every kind of the skill's scope, `none` among them, and not `code`, which is `.ai/skills/verify-spec-implementation/`'s. No audit reads a design: the `none` a run covers is the working files an audit's unit names, never a design document. Of the semantic checks whose Carried Out By names `.ai/skills/audit-specs/`, a run reads each whose Reads holds a kind of file it covers, a check another skill carries out being that skill's to run. It reads each reading audit whose Kind names a kind it covers. Each Kind gives the effort this table names, which [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has a review run at:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind

| Kind | Effort |
|---|---|
| `canon-specs` | high |
| `application-specs` | medium |
| `code` | medium |
| `documentation` | light |
| `other` | medium |

A flaw in the canon is reproduced in every spec written under it. A mint's engraving plate works the same way: a flaw in it is reproduced on every banknote it prints. A flaw in the documentation reaches no file beyond it. A flaw in the application specifications reaches the code built from them, and a flaw in code reaches what it runs, so each takes the middle effort. What another file reaches is not known in advance, so it takes the middle effort too.
