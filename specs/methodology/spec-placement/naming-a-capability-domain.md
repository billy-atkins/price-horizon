## Naming a Capability Domain

The product specs are organized by capability domain ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)), rather than by file.

Before writing or extending a product spec, ask what a product owner, or a salesperson pitching the system, would call the capability domain it belongs to. Never ask which open file already talks about something similar.

### Home of New Product Content

The capability domain new product content belongs to decides which file it goes in. Read the product specs' `architecture.md` first. It gives each domain a section of its own, which describes what the domain covers and closes with the files that serve it. Its sections are therefore the domains the specs recognize. Then find the content's home:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Extends a listed domain?, Grows what one of its files holds?

| Extends a listed domain? | Grows what one of its files holds? | Its home |
|---|---|---|
| true | true | that file |
| true | false | a new file in the domain's subfolder, the content a genuinely separate sub-capability |
| false | - | a new domain, named as a plain noun phrase for something the product durably does or governs, never a sprint, a milestone, or a technical mechanism's name, added to the product specs' `architecture.md` as its own section, subfolder or root file decided by [`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes) |

### Traps Before a New Product File

Check for these traps before finalizing any new product file:

**The same mechanism, split by audience, masquerading as two capabilities.** One role's view of a thing and another role's view of the same thing may be one underlying mechanism seen at two scopes. They then belong in one document describing both scopes, not in two documents that will drift apart. The technical spec's language is a useful signal. When it describes what look like two product-facing capabilities as one mechanism serving several audiences, treat that as a reason to consolidate on the product side too.

**A cross-domain concern written into whichever domain needed it first.** A definition, principle, or distinction used by more than one domain and owned by none belongs at the directory's root ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)), never in the domain that happened to need it first ([`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact)).
