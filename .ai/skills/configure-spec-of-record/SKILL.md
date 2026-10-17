---
name: configure-spec-of-record
description: Set up the agent in use to carry out what Spec of Record leaves to it, such as running a review at the reasoning effort the user chose. Use when starting to work with the methodology in a checkout, when the agent or the models it offers change, or when a review's pass records that a chosen reasoning effort ran as the agent allows.
---

# Configuring Spec of Record for an agent

This skill sets up the agent in use for what Spec of Record leaves to it, as `specs/methodology/skills.md § Setting Up an Agent` has it.

## Workflow

### Find what you can apply

Establish whether you set a reviewer's model and reasoning effort as you start the reviewer, or set its reasoning effort only through a definition of your own. Establish too your nearest level to each of light, medium and high. `specs/methodology/design-workflow.md § A Review's Effort` sets out both.

### Confirm with the user before writing

Running this skill is the user's request to write what it sets, so ask only a simple confirmation before writing, offered as a choice. In one line, name the files and the level each is set to. What an agent knows of its own levels can be out of date, and the user can correct it in answering.

### Write the reviewer definitions

Where you apply reasoning effort only through a definition of your own, write one reviewer definition for each level in the place you load such definitions from. Name it, set it and keep it out of version control as `specs/methodology/skills.md § Setting Up an Agent` has it. Write each definition whether or not one is already there, so it is exactly what this skill and `specs/methodology/skills.md § Setting Up an Agent` now set. Both change over time, and a definition kept because it exists may follow an earlier version. Add to the exclude file only the lines not already in it. Where you apply reasoning effort as you start a reviewer, write nothing, and say so. Leave whatever is already there and is not one of these reviewer definitions as it is.

### Tell the user how to load them

Where you load such definitions only as a session starts, tell the user to restart you once they are written. Tell the user this even where the definitions were there before, since you cannot tell which version this session loaded. Where you let a conversation be resumed, tell the user to resume this one, so the work in hand is not lost. Until then, a review runs as you allow, as `specs/methodology/design-workflow.md § A Review's Effort` has it.

## A reasoning effort that never reached the reviewer

The agent took a reviewer's model as it started one, but took its reasoning effort only from a definition file. No definition file existed, so the review ran at the agent's default reasoning effort while the user had chosen another. A reviewer definition for each level closes the gap. Until one exists, the review runs as the agent allows, as `specs/methodology/design-workflow.md § A Review's Effort` has it.

## Reviewer definitions the session could not see

The first run of this skill wrote the reviewer definitions correctly, and then the agent could not start a reviewer. It loaded definitions only as a session started, so the ones written during the session did not exist for it. Nothing in the files showed the gap; only starting a reviewer did. Telling the user to restart closes the gap.
