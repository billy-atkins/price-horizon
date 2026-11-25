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

A run of `.ai/skills/audit-specs/` is given one or more sub-scopes ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)). Each sub-scope holds a set of files a design can change, and no two sub-scopes share a file. The sub-scopes are drawn from the kinds [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) defines, with `canon-specs` split into the core canon and the skills:

**Table Name:** Sub-scopes \
**Reference Key:** Sub-scope \
**Required:** Files

| Sub-scope | Files |
|---|---|
| `core-canon` | every file of `canon-specs` but each registered skill's directory, `.ai/skills/lib/` and `tests/spec-of-record/` |
| `skills` | each registered skill's directory, `.ai/skills/lib/` and `tests/spec-of-record/`, as `canon-specs` bounds them |
| `application-specs` | every file of `application-specs` |
| `documentation` | every file of `documentation` |
| `other` | every file of `other` |

A run given sub-scopes covers their files alone. A run the user starts with no sub-scope is the full run. It covers every sub-scope and the working files, and not `code`, which is `.ai/skills/verify-spec-implementation/`'s. No audit reads a design document: the working files a run covers are those an audit's unit names.

A run covers kinds of file, as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) names them: the kinds of change its sub-scopes are drawn from, each for its operative files, `fixture-files` where it covers the `skills` sub-scope, whose files hold the fixture files, and `working-files` where it is the full run. Of the semantic checks whose Carried Out By names `.ai/skills/audit-specs/`, a run reads each whose Reads holds a kind of file it covers, a check another skill carries out being that skill's to run. It reads each reading audit whose Kind names a kind it covers, over each of the audit's units that holds a file it covers, reading beyond those files only as the unit needs to judge them. So a run covering the `skills` sub-scope reads the fixture files, and only by the checks and the audits that name `fixture-files`. Its script's checks run over the whole of the skill's scope, and the run reports only the findings lying in the files it covers.

### The Sub-scopes a Design Settles

Every design settles the sub-scopes of its audit at the apply. The settling gives its required sub-scopes and its default, as [`§ A Design's Reviews § The Sub-scopes a Design Settles § The Sub-scopes of a Design's Audit`](#the-sub-scopes-of-a-designs-audit) has them. The user keeps the default, drops any sub-scope but a required one, or adds any sub-scope. The builder brings the user the choice in this form, as [`specs/AGENTS.md § Design, Refactor, Refine § Who Decides`](/specs/AGENTS.md#who-decides) has a recommendation brought:
- **Changed.** Each sub-scope holding a file the design changed, with the count of its files that changed, never the files themselves.
- **Required sub-scopes.** The required sub-scopes, which the user cannot drop.
- **Options.** Lettered, each written as "Required + " the sub-scopes it adds to the required sub-scopes, or "Required only". Option A adds every sub-scope the default holds beyond the required sub-scopes, and is tagged "(Default)". Option B adds none. Where the default holds two or more such sub-scopes, each further letter adds one of them alone. Where the default holds no sub-scope beyond the required sub-scopes, the one option is A, "Required only". The option the builder recommends is tagged "(Recommended)".
- **Why.** The builder's reason for what it recommends, an option or letters combined.

The user answers with a letter, or with letters after B combined, and may name any other sub-scope to add.

#### The Sub-scopes of a Design's Audit

A design's default audit is decided by the sub-scopes holding a file it changed. The files are read when the audit runs, as [`specs/methodology/working-files/main.md § A Design Document § Applying and Committing`](/specs/methodology/working-files/main.md#applying-and-committing) has a design's changes read. The questions:
- **Core canon changed?** Whether a file of the `core-canon` sub-scope changed.
- **Skills changed?** Whether a file of the `skills` sub-scope changed.
- **Application specs changed?** Whether a file of the `application-specs` sub-scope changed.
- **Documentation changed?** Whether a file of the `documentation` sub-scope changed.
- **Other files changed?** Whether a file of the `other` sub-scope changed.

Each row names a sub-scope holding a changed file and the sub-scopes downstream of it. The core canon reaches every other sub-scope, since its rules govern every file in them. The skills reach the core canon, since the core canon cites the skills' steps.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Order:** any \
**Hit Policy:** Collect \
**Conditions:** Core canon changed?, Skills changed?, Application specs changed?, Documentation changed?, Other files changed?

| Core canon changed? | Skills changed? | Application specs changed? | Documentation changed? | Other files changed? | Sub-scopes |
|---|---|---|---|---|---|
| true | - | - | - | - | `core-canon`, `skills`, `application-specs`, `documentation`, `other` |
| - | true | - | - | - | `skills`, `core-canon` |
| - | - | true | - | - | `application-specs` |
| - | - | - | true | - | `documentation` |
| - | - | - | - | true | `other` |

The default is the sub-scopes of every row the design matches. Where no row matches, the default is empty. The required sub-scopes are those holding a file the design changed.

Before the audit's run starts, the builder checks that the sub-scopes the user settles keep every sub-scope holding a file the design changed, and the audit's log entry is refused where they do not, as [`specs/methodology/working-files/main.md § Design Log Entry`](/specs/methodology/working-files/main.md#design-log-entry) has it. The audit is an `.ai/skills/audit-specs/` run given the sub-scopes the user settles. Where the user settles none, the design runs no audit of the specs, and settling no sub-scope never means the full run. A design that changed code also runs `.ai/skills/verify-spec-implementation/`'s full run. The user settles the audit's sub-scopes at the state [`specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § The Apply`](/specs/methodology/design-workflow/order-of-a-designs-work.md#the-apply) gives.
