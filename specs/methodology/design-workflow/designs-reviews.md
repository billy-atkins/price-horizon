## A Design's Reviews

A design's Kind sizes its reviews and its audit. The effort they take grows with what a flaw in the design would cost where the review can find it: its decisions before the apply, and its text after it. A design whose Target names files or directories of more than one Kind takes, in each phase, the highest effort among them. Each Kind gives the effort this table names, which [`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort) has a review run at, by the answer to the question:
- **After the apply?** True for a review or an audit reading the applied work, and false for an adversarial round.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind, After the apply?

| Kind | After the apply? | Effort |
|---|---|---|
| `canon-specs` | false | medium |
| `canon-specs` | true | high |
| `application-specs` | - | medium |
| `code` | - | medium |
| `documentation` | - | light |
| `other` | - | medium |

A flaw in the canon is reproduced in every spec written under it. A mint's engraving plate works the same way: a flaw in it is reproduced on every banknote it prints. Like the plate's, the canon's flaw is reproduced only once the canon is put to use, at the commit. Before the commit, the post-apply review and the audit read a canon change's text. Before the apply, no text carrying the change yet exists, so a review judges its decisions and catches a wrong one before any text is written for it. A flaw in the documentation reaches no file beyond it. A flaw in the application specifications reaches the code built from them, and a flaw in code reaches what it runs, so each takes the middle effort. What another file reaches is not known in advance, so it takes the middle effort too.

A run of `.ai/skills/audit-specs/` is given one or more scopes, each a set of files of the kinds [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) defines:

**Table Name:** Audit Scopes \
**Reference Key:** Scope \
**Required:** Files

| Scope | Files |
|---|---|
| `skills` | each registered skill's directory and `.ai/skills/lib/`, as `canon-specs` bounds them |
| `canon` | every file of `canon-specs` |
| `canon-and-app` | every file of every kind but `code` and `none`, since a change to the canon can leave any such file in breach of it, the application specs among them |
| `app` | every file of `application-specs` |
| `documentation` | every file of `documentation` |
| `other` | every file of `other` |

A run given audit scopes covers their files alone. A run the user starts with no audit scope is the full run, covering every kind of the skill's scope, `none` among them, and not `code`, which is `.ai/skills/verify-spec-implementation/`'s. No audit reads a design: the `none` a run covers is the working files an audit's unit names, never a design document. Of the semantic checks whose Carried Out By names `.ai/skills/audit-specs/`, a run reads each whose Reads holds a kind of file it covers, a check another skill carries out being that skill's to run. It reads each reading audit whose Kind names a kind it covers, over each of the audit's units that holds a file it covers, reading beyond those files only as the unit needs to judge them. Its script's checks run over the whole of the skill's scope, and the run reports only the findings lying in the files it covers.

Each kind other than `code` orders the scopes holding its files, narrowest first:

**Table Name:** Scope Orders \
**Reference Key:** Kind \
**Required:** Scopes

| Kind | Scopes |
|---|---|
| `canon-specs` | `skills`, `canon`, `canon-and-app` |
| `application-specs` | `app`, `canon-and-app` |
| `documentation` | `documentation`, `canon-and-app` |
| `other` | `other`, `canon-and-app` |

### The Scopes of a Design's Audit

A design's audit runs one scope for each kind other than `code` that the files and directories its Target names are of. The files a kind's scope must hold are the files of that kind the design edits, and, for the design's own Kind, the files the rules the design changes govern too. A file those rules govern that no scope holds, a working file or code, counts toward no scope, the working files staying with the design script's checks and the full run's Working-file form audit. The builder recommends each kind's scope, the narrowest of that kind's order holding those files, by the answers to the questions:
- **Beyond the skills?** True where those files include a file of `canon-specs` that the `skills` scope does not hold.
- **Of another kind?** True where those files include a file of a kind other than the row's Kind.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind, Beyond the skills?, Of another kind?

| Kind | Beyond the skills? | Of another kind? | Scope |
|---|---|---|---|
| `canon-specs` | false | false | `skills` |
| `canon-specs` | true | false | `canon` |
| `canon-specs` | - | true | `canon-and-app` |
| `application-specs` | - | false | `app` |
| `application-specs` | - | true | `canon-and-app` |
| `documentation` | - | false | `documentation` |
| `documentation` | - | true | `canon-and-app` |
| `other` | - | false | `other` |
| `other` | - | true | `canon-and-app` |

The user keeps each recommended scope or widens it to a wider one of the same kind's order, and the audit is an `.ai/skills/audit-specs/` run given the scopes the user settles. The builder recommends them, and the user settles them, at the states [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) gives. Where the Target names `code`, the audit is `.ai/skills/verify-spec-implementation/`'s full run, and a design whose Target names `code` and another kind runs both.
