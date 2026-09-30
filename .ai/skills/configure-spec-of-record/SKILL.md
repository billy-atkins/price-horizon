---
name: configure-spec-of-record
description: Set up the agent in use to carry out what Spec of Record leaves to it, such as running a review at the reasoning effort the user chose. Use when starting to work with the method in a checkout, when the agent or the models it offers change, or when a review's pass records that a chosen reasoning effort ran as the agent allows.
---

# Configuring Spec of Record for an agent

This skill sets up the agent in use for what Spec of Record leaves to it, as `specs/methodology/skills.md § Setting Up an Agent` has it.

## Workflow

### Find what you can apply

Establish whether you set a reviewer's model and its reasoning effort as you start it, or its reasoning effort only through a definition of your own, and your nearest level to each of light, medium and high, per `specs/methodology/skills.md § Setting Up an Agent`.

### Confirm with the user before writing

Running this skill is the user's request to write what it sets, so ask only a simple confirmation before writing, offered as a choice: name the files and the level each is set to in a line, since what an agent knows of its own levels can be out of date and the user can correct it there.

### Write the reviewer definitions

Where you apply reasoning effort only through a definition of your own, write one reviewer definition for each level in the place you load such definitions from, named, set and kept out of version control as `specs/methodology/skills.md § Setting Up an Agent` has it. Write each whether or not one is already there, so it is exactly what this skill and `specs/methodology/skills.md § Setting Up an Agent` now set: both change over time, and a definition kept because it exists may follow an earlier version. Add to the exclude file only the lines not already in it. Where you apply reasoning effort as you start a reviewer, write nothing, and say so. Leave whatever is already there and is not one of these reviewer definitions as it is.

### Tell the user how to load them

Where you load such definitions only as a session starts, tell the user to restart you once they are written, even where they were there before, since you cannot tell which version this session loaded, and to resume the conversation where you offer that, so the work in hand is not lost. Until then, a review runs as you allow (`specs/AGENTS.md § Design, Refactor, Refine (DRR)`).

## A reasoning effort that never reached the reviewer

The agent took a reviewer's model as it started one, but its reasoning effort only from a definition file, and none existed, so the review ran at the agent's default reasoning effort while the user had chosen another. A reviewer definition for each level closes the gap; until one exists, the review runs as the agent allows (`specs/AGENTS.md § Design, Refactor, Refine (DRR)`).

## Reviewer definitions the session could not see

The first run of this skill wrote the reviewer definitions correctly, and the agent then could not start one: it loaded definitions only as a session started, so the ones written during the session did not exist for it. Nothing in the files showed the gap; only starting a reviewer did. Telling the user to restart closes it.
