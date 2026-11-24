# Design Document

**Name:** ferry-times-in-the-guide \
**Status:** in-progress \
**Source:** "The guide never says when the ferry runs." \
**Kind:** documentation \
**Target:** `docs/guide.md` \
**Spawned By:** none \
**Depends On Designs:** none \
**Validated:** none

## The Problem

The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs.

## Design Goals

**Records:**
  - **Name:** guide-says-when-the-ferry-runs \
    **Description:** The guide says when the ferry runs.

## The Design Frame

### Scope

**Cases:**
  - **Name:** visitor-planning-a-crossing \
    **Goals:**
      - guide-says-when-the-ferry-runs

    **Description:** A visitor reads the guide to plan a crossing. What tells it apart is that the visitor has not yet left the mainland.

The sweep read the guide whole.

### Assessed Areas

**Records:**
  - **Area:** `docs/guide.md § The Ferry` \
    **Impact:**
      - changes

    **Assessment:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/handed-off-judgment/1.md`

### Approach

**Principles:**
  - **Name:** times-stated-where-the-ferry-is-named \
    **Goals:**
      - guide-says-when-the-ferry-runs

    **Description:** The times stand in the section naming the ferry, and nowhere else.

### Frame Outcomes

**Records:**
  - **Name:** crossing-planned-from-the-guide \
    **Goals:**
      - guide-says-when-the-ferry-runs

    **Description:** A visitor plans a crossing from the guide alone. It is judged by reading the section naming the ferry.

## Design Plan Steps

**Records:**
  - **Name:** ferry-times-stated \
    **What:** `docs/guide.md § The Ferry` \
    **Why:** The section names the ferry and gives no time. \
    **Depends On Steps:** none \
    **Objectives:**
      - **Name:** section-gives-the-first-and-last-crossing \
        **Goals:**
          - guide-says-when-the-ferry-runs

        **Upholds Frame Outcomes:**
          - crossing-planned-from-the-guide

        **State:** The section naming the ferry gives the time of the first crossing and of the last.

## Out of Scope

Nothing the research found is left out.
