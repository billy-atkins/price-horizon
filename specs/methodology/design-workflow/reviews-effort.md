## A Review's Effort

A review's reasoning effort is the level the user chose ([`specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort`](/specs/AGENTS.md#each-reviews-model-and-effort)). The level is applied in the way the agent in use can apply it. The builder offers only a level the agent in use can apply. Where the agent in use can apply none, the review runs as the agent allows. How a level is applied:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** How the agent applies a level, definition set up?

| How the agent applies a level | definition set up? | Applied |
|---|---|---|
| "as it starts a reviewer" | - | at the nearest level the agent offers, set as the reviewer starts |
| "through a reviewer definition" | true | through the definition the agent was set up with for that level ([`specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent`](/specs/methodology/skills/setting-up-an-agent.md#setting-up-an-agent)) |
| "through a reviewer definition" | false | as the agent allows, the agent's setting itself up offered to the user for the reviews after it, since a definition written now may load only once the agent restarts (`.ai/skills/configure-spec-of-record/`) |
| "not at all" | - | as the agent allows |
