## Open Question

An open question is recorded in the specs whose area it applies to: methodology, product or technical. Within those specs, it is recorded at the lowest altitude covering everything the question impacts, where [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact) places a rule several places use, and where it is recorded gives its scope as that section has a rule's place give it. The file recording it must be able to cite every section the question's Impacts names ([`specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation/which-citations-are-allowed.md#which-citations-are-allowed)). Open Question is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), and a file's open questions sit in its record section of this type. In a document kept as one file ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)), that record section is the file's last top-level section, so a reader finds them all in one place, after the settled content they qualify:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Open Questions \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | a short name for what is undecided |
| Open Question | no | yes | | text | what is undecided, asked as a question |
| Provisional Answer | no | yes | | text | what the specs rely on until it is settled, stated as settled prose would state it |
| Impacts | no | yes | | text | prose naming each thing that relies on the provisional answer, with a citation of the section holding it, or, where that section holds more, of the part of a construct that relies on it ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)); a data field that relies on it is named by what it says beside its section's citation |

A sentence that relies on the provisional answer, and would otherwise read as settled, cites the record wherever [`specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation/which-citations-are-allowed.md#which-citations-are-allowed) allows that citation, so a reader meets the question from the text that depends on it. A spec of a system that exists states the system as it is built. Where its author suspects a defect, what the system should do is an open question, and its Provisional Answer is the behavior as built. So the spec states as built nothing the system does not do.

The provisional answer is stated in the record alone. The text relying on it states only what does not depend on it. Settling an open question is a change like any other. The settled answer is written, wherever it is needed, into each section the record's Impacts names and each section citing the record. There it replaces any citation of the record. Then the record is removed, and its record section too once that section holds no record.
