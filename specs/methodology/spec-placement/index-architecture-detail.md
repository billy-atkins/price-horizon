## Index, Architecture, Detail

Every directory under `specs/` organizes its files by altitude. New content belongs at the altitude that matches what it is.

**Reference Key:** Altitude \
**Required:** File, Holds

| Altitude | File | Holds |
|---|---|---|
| Navigation | `index.md` | a title and a table naming each file and subdirectory with its description, no content of its own |
| Main | `main.md` | what the directory's specs share, its front matter among it, and, in a document laid out as a folder, the document's text not laid out as file units ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)); held only where the directory has such content to hold |
| Overview | `architecture.md` | a self-contained description of the directory's shape, every directory beneath it included, and of what [`§ What an Overview Describes`](#what-an-overview-describes) names beyond it, in its own words, naming every major piece and how they relate; only where that shape is worth describing as a whole, which not every directory's is |
| Detail | everything else | one file per file unit ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)), holding the actual mechanism, schema, or experience, at whatever depth the subject needs |

**The test for new content.** Does it connect pieces, how they relate, why they are arranged as they are, what they add up to? That is overview. Does it specify what one piece does, shows or promises? That is detail, however much it says about the pieces around it.

**What an `architecture.md` is, and is not.** It is written so it can be read, understood, and shared in isolation. An architecture document stands apart from the system it describes in the same way, rather than being a portal into it. A closing mention of where fuller detail lives is fine, but the overview does not get its meaning from that mention.

**It holds no detail of its own.** An overview is the view of the whole from altitude. Zooming in reaches the detail files. By this section's test for new content, a detail has its home in one of those files, and an overview stating the detail restates it from there. What the overview states as its own is what only that height shows: how the pieces connect, the forest a reader of any one file cannot see for the trees.

An overview fails in opposite ways, and each has the same fix. One that accumulates full detail has stopped being an overview. One that thins into a table of citations cannot be understood without opening the files it points at. In either case, write the overview so it stands alone. Move genuine step-by-step or field-level detail into a file of its own ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)), and repath every citation that pointed at the old location in the same pass.

A directory's own mapping table, where it has one, is the one exception: a deliberately citation-heavy traceability artifact is legitimate *beside* an overview that stands on its own, not *instead* of one.

**Where a diagram goes.** Set at any altitude by [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams).

## What an Overview Describes

An overview describes its directory, every directory beneath it, and what this table names for its directory ([`§ Index, Architecture, Detail`](#index-architecture-detail)). It is kept in sync with all it describes ([`specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md § Keeping Specs in Sync § Materialized Views`](/specs/methodology/sourcing-and-citation/keeping-specs-in-sync.md#materialized-views)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Directory \
**Default Output:** nothing beyond its directory

| Directory | Describes beyond it |
|---|---|
| `specs/methodology/` | the skills registered as Spec of Record's, and the code their scripts share ([`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills), [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill)) |
| `specs/application/technical/` | the code carrying out the application specs, within the code roots its technical stack names ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack), [`specs/methodology/code.md`](/specs/methodology/code.md)) |
