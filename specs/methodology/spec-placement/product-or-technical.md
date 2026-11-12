## Product or Technical

**Reference Key:** Spec \
**Required:** Covers

| Spec | Covers |
|---|---|
| Product | What a user or an integrating caller can experience, rely on, or build against: what a user sees and does, the guarantees the system makes, the roles and access model a buyer would evaluate, the shape of any contract an integrating caller depends on. Stated as a capability or a guarantee, never as an implementation choice. |
| Technical | How each of those facts is made true: the algorithms, schemas, service boundaries, models, and infrastructure. |

**The test.** Could an end user or an integrating caller observe this as something they can rely on, rather than as a byte in a response payload or a line in a schema?

A guarantee, a role, a piece of what a user sees and does, and a term a user needs defined to trust what the product shows them all pass. Each belongs in the product spec, even when its mechanism is technical-only. A data model field, an algorithm's steps, a database's shape and a choice of API convention do not pass on their own. They belong in the technical spec.

**Two drawings of one building.** A product spec is the architect's drawing and a technical spec is the structural engineer's. The architect draws what the building is and everything the people in it will experience. The engineer draws how it can be built and keep working for them. Both drawings are of the same building, drawn twice for two purposes. Neither summarizes the other.

This is why a product spec states facts that sound like infrastructure. The architect draws a wall rated to hold back fire for two hours, because someone occupying the building relies on that. The engineer states the assembly that achieves the rating. A customer's data encrypted at rest is the same case. A buyer relies on it, so it belongs on the architect's drawing. Which keys encrypt it, and how often they rotate, belongs on the engineer's.

The two drawings also divide the building differently. An architect organizes by room and an engineer by structural system, so the sheets do not correspond one to one. Finding which beam carries which room takes a drawing made for that purpose. The specs are the same. Product and technical specs do not decompose alike, so the usual way to keep them in view at once is a traceability table tying each product-facing capability to the mechanism producing it.

**When a fact needs both.** State the plain form in the product spec and the exact mechanism in the technical spec. Have each name the other, so the two cannot drift apart silently.

**Different renderings, not two levels of detail.** A construct modeling one fact may render differently on each side:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Construct

| Construct | Product spec | Technical spec |
|---|---|---|
| "DAG", "State Machine for a process" | a business-readable table of its steps, decision points and outcomes | the DAG or State Machine that carries it out |
| Constraint | the plain guarantee | its enforcement, what its Enforced By names |
| "State Machine for an entity's or a system's status", "Decision Table" | the construct itself | the same construct |
| Record Form of entries written repeatedly | the construct itself | the same construct |
| "Record Form of a closed set", "Basic Table of a closed set" | the closed set: its type and its records, or its Basic Table | the data storing it, its database design and any enum naming its members, citing the set |
| Algorithm | no rendering, since a business reader has no use for step-by-step computation | the Algorithm |

**A promise that cannot be built.** Writing the technical spec tests a product promise against what is possible. A promise no mechanism can make true is amended in the product spec, as the user decides ([`specs/methodology/spec-placement/personas.md § Personas`](/specs/methodology/spec-placement/personas.md#personas)), rather than left standing.
