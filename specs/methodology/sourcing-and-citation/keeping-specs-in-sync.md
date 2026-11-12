## Keeping Specs in Sync

A change reaches more than the facts it edits. It reaches each materialized view restating them, and the counterpart drawing their subject from the other perspective. None of these keeps itself current, so each place a change reaches is checked for a matching update. This section's children say what each kind is kept in sync with.

### Materialized Views

A materialized view ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) is never a second home. It is kept in sync with its sources, the homes of what it restates:

**A directory's own `architecture.md`.** Its sources are the files in its directory and in every directory beneath it, and what [`specs/methodology/spec-placement/index-architecture-detail.md § What an Overview Describes`](/specs/methodology/spec-placement/index-architecture-detail.md#what-an-overview-describes) names beyond it ([`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail)). Everything the file restates of its sources, in its prose, its citations and its mapping tables, is kept in sync with them. So is everything it connects among them.

**A diagram, wherever it sits.** Its sources are explicit: the sections and records its Sources list names. Each source names the diagram back ([`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams)).

### Product and Technical Counterparts

A product spec and its technical counterpart are two drawings of one subject, each from its own perspective. Neither is a summary of the other, and each names the other ([`specs/methodology/spec-placement/product-or-technical.md § Product or Technical`](/specs/methodology/spec-placement/product-or-technical.md#product-or-technical)). They are kept aligned.
