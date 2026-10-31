# Design Document

**Name:** {the design's slug, its file name without .md} \
**Status:** {not-started, or in-progress once it is worked} \
**Source:** {the user's words, quoted, or the finding} \
**Kind:** {canon-specs, application-specs, documentation or other} \
**Target:** {`path`; `path`} \
**Spawned By:** {a design document's Name, as `implement-specs/{Name}` for one in that skill's plans folder, or none} \
**Depends On Designs:** {design documents' Names, in the same form, separated by semicolons, or none} \
**Validated:** none

## The Problem

{the problem}

## Design Goals

{`Not yet stated.` until the user agrees on the goals; then:}

**Records:**
  - **Name:** {a slug} \
    **Description:** {what the goal asks}

## The Design Frame

### Scope

{the cases the change governs and what tells them apart; then the sweep's method, the research it was, never the whole of what that research matched; and, where Depends On Designs names a design, what this design relies on from each: what it leaves in the files that this one cites or builds on}

### Assessed Areas

**Records:**
  - **Area:** {a file or a section, cited as a place, used once in the design} \
    **Impact:**
      - {applies or changes, one to an item, as the latest Read Assessment of its Area holds them}

    **Assessment:** {the report of the handed-off judgment holding that Read Assessment, as a place}

### Approach

{the principle the solution applies, citing each goal it rests on as a record is cited, by its record section and its Name}

### Frame Outcomes

**Records:**
  - **Name:** {a slug} \
    **Goals:**
      - {the Name of a goal it rests on, one to an item}

    **Description:** {what a successful solution achieves, and how that is judged}

## Steering Decisions

{this section only once the user has steered the design}

**Records:**
  - **Name:** {a short name} \
    **Prompted By:** {the builder's question, proposal or account and the options it offered, a finding's ID, or the user's own initiative} \
    **Type:** {selection or perspective} \
    **Steer:** {the user's words, quoted} \
    **Decision:** {the essence of what the steer decided}

## Design Plan Steps

{`Not yet drafted.` until drafting states the steps; then:}

**Records:**
  - **Name:** {a slug} \
    **What:** {each area the step changes, as a place, each an Assessed Area whose Impact holds changes, or a place within one} \
    **Why:** {why the step is needed} \
    **Depends On Steps:** {none, or a list of the Names of the steps it builds on, one to an item} \
    **Objectives:**
      - **Name:** {a slug} \
        **Goals:**
          - {the Name of a goal it serves, one to an item}

        **Upholds Frame Outcomes:**
          - {the Name of a Frame Outcome it upholds, one to an item}

        **State:** {what the step achieves toward the goals it names, a state the applied work holds, written as `specs/methodology/working-files.md § Design Plan Step § Step Objective` has an Objective's text written}

## Retired Phrases

{this section only where the design retires wording; then:}

**Records:**
  - **Phrase:** {a word or phrase the design stops using in one sense} \
    **Replacement:** {what the design uses instead} \
    **Stays Right:** {the places the phrase stays right, each a path, its section after it; left out where none}

## Impact on the Application Specs

{this section only in a canon design}

{each application file and section left out of sync, and what the application work must do there, or none found; and how the review was done}

## Design Log Entries

{appended through the design script's `--append-entry` from the design's entry into in-progress on, never written by hand, as `specs/methodology/working-files.md § Design Log Entry` has each entry appended}

## Out of Scope

{each thing the design deliberately leaves unaddressed, each change considered and declined and each piece of work handed on, with its reason, naming no other working file; an area assessed changes that the user leaves out holds its place right after its item's bold lead-in, and cites the steer}
