## Titling a Heading

A heading's title is a stable slug for whatever the section covers, not prose to be refined later. Every citation depends on that exact text. A title chosen well the first time keeps a citation from ever needing to change. If a title does change, every citation naming it is updated in the same edit. A citation left naming the old title is broken until it is updated.

**Reference Key:** Rule \
**Required:** Form

| Rule | Form |
|---|---|
| No `§` in the heading itself | `## Vision`, never `## § Vision` |
| No `[` in the heading itself, which opens a part's key, in a citation | `## Session Timeout`, never `## Session Timeout [draft]` |
| Unique among headings sharing its parent, a top-level heading's parent being its file | two headings under different parents may share a title |

A numbered heading, or one counting its children, is the heading case of [`specs/methodology/spec-style/ordinals-and-counts.md § Ordinals and Counts`](/specs/methodology/spec-style/ordinals-and-counts.md#ordinals-and-counts). A heading pays for a number twice, since its title is also the text of every citation naming it. Renumbering sections, or retitling one whose count went stale, changes those citations as well.

**Bold lead-ins are not headings.** A bold lead-in ([`specs/methodology/spec-style/markdown.md § Bold Lead-ins`](/specs/methodology/spec-style/markdown.md#bold-lead-ins)) has none of the guarantees a heading carries, starting with enforced uniqueness. It has no citation form either ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation)). So a paragraph that is, or needs to be, a citation's target is authored as a child heading instead. The child heading gets every rule this section sets, and needs no workaround. Entries that exist to be cited are records instead ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)).
