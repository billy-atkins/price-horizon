# Design Document

**Name:** {a few words}
**Status:** {not-started, or in-progress once it is worked}
**Source:** {the user's words, quoted, or the finding that raised it}
**Kind:** code
**Target:** {`path`; `path`, the code it writes or changes}
**Spawned By:** {a design document's file name without .md, as `design-specs/{file name}` for one in that skill's plans folder, or none}
**Depends On:** {design documents' file names, in the same form, separated by semicolons, or none}
**Validated:** none

## The Problem

{the product module it carries out, then the specs it carries into code, cited, and what the code lacks}

## Design Goals

{`Not yet stated.` until the user agrees the goals; then:}

**Records:**

- **Name:** {a slug}
  **Description:** {what the goal asks}

## The Design Frame

### Scope

{the cases the change governs and what tells them apart; then the sweep of the specs and the code, and what it found}

### Approach

{the principle the solution applies, citing by Name the goals it rests on}

### Outcomes

{what a successful solution achieves, and how that is judged, each outcome citing by Name the goals it rests on}

## Steering Decisions

{this section only once the user has steered the design}

**Records:**

- **Name:** {a short name}
  **Prompted By:** {the builder's question, proposal or account and the options it offered, a finding's ID, or the user's own initiative}
  **Type:** {selection or perspective}
  **Steer:** {the user's words, quoted}
  **Decision:** {the essence of what the steer decided}

## The Design

{what the design does; then each unit of governed code, where it is, its app-spec annotations, sorted, and what it does; the wiring, and what it connects; and the tests, and what each checks; quoting existing code only where it changes it, each such edit in the forms `specs/methodology/working-files.md § A Design Document` gives}

## The Builder's Passes

{each pass and each review under a bold lead-in naming it, each review but the validation review named with its report, an adversarial review's opening Adversarial review and a post-apply audit's Post-apply audit, each of those two naming the model and reasoning effort it ran on, and recording the design flaws among its findings with the user's triage of each; an adversarial review's pass also recording how its implementation flaws were settled, the causes the round's change addressed, a mechanism it rewrote whole where its findings clustered, and the worked case proving it, or the user's approval of the text where it ended the review, with the round it ended; a post-apply audit's pass how each finding settled; the nits a round left and each judgment handed off; the trace, before a review, of each mechanism with states or routes the design changes; and each ephemeral differential test of a script the design changes, or each of the local environment's tasks it ran on code, and what it showed}

## Deliberately Left Alone

{each change considered and declined, with the reason, and each piece of work deferred}
