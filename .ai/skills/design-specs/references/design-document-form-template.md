# Design Document

**Name:** {a slug (`specs/methodology/working-files/main.md § A Design Document`)} \
**Version:** {this field only once the design script writes it: the version it works out from the log, left out at its default (`specs/methodology/working-files/main.md § A Design Document § The Design's Version`)} \
**Status:** {a state (`specs/methodology/working-files/main.md § A Design Document § The States It Moves Through`)} \
**Source:** {the user's words, quoted, or the finding (`specs/methodology/working-files/main.md § A Design Document`)} \
**Kind:** {a kind of change (`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`)} \
**Target:** {paths in backticks, separated by semicolons (`specs/methodology/working-files/main.md § A Design Document`)} \
**Spawned By:** {a design document's Name, or none (`specs/methodology/working-files/main.md § A Design Document § Spawning a Change of Its Own`)} \
**Depends On Designs:** {design documents' Names, separated by semicolons, or none (`specs/methodology/working-files/main.md § A Design Document`)} \
**Validated:** none

## The Problem

{the problem (`specs/methodology/working-files/main.md § A Design Document`)}

## Design Goals

{`Not yet stated.` until the user agrees on the goals, as `specs/methodology/working-files/main.md § A Design Document` has it; then:}

**Records:**
  - **Name:** {a slug (`specs/methodology/working-files/main.md § Design Goal`)} \
    **Description:** {what the goal asks (`specs/methodology/working-files/main.md § Design Goal`)}

## The Design Frame

### Scope

{the cases the change governs, each citing the goals it rests on, and the sweep's method (`specs/methodology/working-files/main.md § A Design Document`)}

**Reliances:** {this field only where the design relies on another design (`specs/methodology/working-files/main.md § A Design Document § Reliance`)}
  - **Design:** {the Name of a design relied on (`specs/methodology/working-files/main.md § A Design Document § Reliance`)} \
    **Relies On:** {what the design relies on from it (`specs/methodology/working-files/main.md § A Design Document § Reliance`)} \
    **Version:** {this field only where the design relied on stands past its default version: the version the design script gives in that design's header as the reliance is stated (`specs/methodology/working-files/main.md § A Design Document § Reliance`)}

### Assessed Areas

**Records:**
  - **Area:** {a place (`specs/methodology/working-files/main.md § A Design Document § Assessed Area`)} \
    **Impact:**
      - {an impact, one to an item (`specs/methodology/working-files/main.md § A Design Document § Assessed Area`)}

    **Assessment:** {a report, as a place (`specs/methodology/working-files/main.md § A Design Document § Assessed Area`)}

### Approach

{the principle the solution applies (`specs/methodology/glossary.md`), citing the goals it rests on (`specs/methodology/working-files/main.md § A Design Document`)}

### Frame Outcomes

**Records:**
  - **Name:** {a slug (`specs/methodology/working-files/main.md § A Design Document § Frame Outcome`)} \
    **Goals:**
      - {a goal's Name, one to an item (`specs/methodology/working-files/main.md § A Design Document § Frame Outcome`)}

    **Description:** {what the applied work achieves, and how that is judged (`specs/methodology/working-files/main.md § A Design Document § Frame Outcome`)}

## Steering Decisions

{this section only once the user has steered the design, as `specs/methodology/working-files/main.md § A Design Document` has it}

**Records:**
  - **Name:** {a short name (`specs/methodology/working-files/main.md § Steering Decision`)} \
    **Prompted By:** {what prompted the steer (`specs/methodology/working-files/main.md § Steering Decision`)} \
    **Type:** {a steer's type (`specs/methodology/working-files/main.md § Steering Decision § A Steer's Type`)} \
    **Steer:** {the user's words, quoted (`specs/methodology/working-files/main.md § Steering Decision`)} \
    **Decision:** {the essence of what the steer decided (`specs/methodology/working-files/main.md § Steering Decision`)} \
    **Changes:** {the highest part whose decision the steer changes, or `none` (`specs/methodology/working-files/main.md § Steering Decision`)}

## Design Plan Steps

{`Not yet drafted.` until drafting states the steps, as `specs/methodology/working-files/main.md § A Design Document` has it; then:}

**Records:**
  - **Name:** {a slug (`specs/methodology/working-files/main.md § Design Plan Step`)} \
    **What:** {places (`specs/methodology/working-files/main.md § Design Plan Step`)} \
    **Why:** {why the step is needed (`specs/methodology/working-files/main.md § Design Plan Step`)} \
    **Depends On Steps:** {none, or a list of steps' Names, one to an item (`specs/methodology/working-files/main.md § Design Plan Step`)} \
    **Draft:** {this field only where the step carries a Draft, its fenced blocks beneath the key (`specs/methodology/working-files/main.md § Design Plan Step § A Draft`)}

      ```{markdown, or the code's language}
      {the means its builder works out (`specs/methodology/working-files/main.md § Design Plan Step § A Draft`)}
      ```

    **Objectives:**
      - **Name:** {a slug (`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`)} \
        **Goals:**
          - {a goal's Name, one to an item (`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`)}

        **Upholds Frame Outcomes:**
          - {a Frame Outcome's Name, one to an item (`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`)}

        **State:** {a state the applied work holds (`specs/methodology/working-files/main.md § Design Plan Step § Step Objective`)}

## Retired Phrases

{this section only where the design retires wording, as `specs/methodology/working-files/main.md § A Design Document` has it; then:}

**Records:**
  - **Phrase:** {a word or phrase (`specs/methodology/working-files/main.md § Retired Phrase`)} \
    **Replacement:** {the wording used instead (`specs/methodology/working-files/main.md § Retired Phrase`)} \
    **Stays Right:** {places, each a path, its section after it (`specs/methodology/working-files/main.md § Retired Phrase`)}

## Impact on the Application Specs

{this section only in a canon design, as `specs/methodology/working-files/main.md § A Design Document` has it}

{a list of items, or that none was found and how the research covered the application specs (`specs/methodology/working-files/main.md § A Design Document`)}

## Design Log Entries

{the entries `--log-entry` appends (`specs/methodology/working-files/main.md § Design Log Entry`)}

## Out of Scope

{a list of items (`specs/methodology/working-files/main.md § A Design Document`)}
