# Check's Report

**Design:** ferry-times-in-the-guide \
**Entry:** adversarial-review-1

## Reading

**Design Version:** 1.0.1 \
**Reviewer Readings:**
  - **Reviewer:** reviewer-1 \
    **Collecting Reads:**
      - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
      - `docs/guide.md`

    **Earlier Reports:**
      - none

    **Weighing Reads:**
      - `docs/guide.md § The Ferry`

## Findings

**Records:**
  - **Finding:** reviewer-1-last-crossing-in-winter \
    **Verdict:** implementation flaw \
    **Decision:** the times the section gives \
    **Affected Goals:**
      - guide-says-when-the-ferry-runs

    **Description:** The step's Objective gives one first and one last crossing, and the ferry keeps other hours in winter. \
    **Evidence:**
      - **Description:** The section names one quay and no season. \
        **Places:**
          - `docs/guide.md § The Ferry`

    **Rationale:** A visitor in winter plans a crossing the ferry does not make. \
    **Possible Fix:**
      - **Kind:** revision \
        **Delivers:** An Objective giving the first and the last crossing of each season.

## Searches

**Records:**
  - **Search:** reviewer-1-winter-hours \
    **For:** every place giving the hours the ferry keeps in winter \
    **Goals:**
      - none

    **Kind:** meaning \
    **Query:** In winter the ferry makes fewer crossings than in summer. \
    **Ranking Part:** 1 to 20 \
    **Snapshot:** 0123456789abcdef \
    **Places:**
      - `docs/guide.md § The Ferry`

## Causes

**Records:**
  - **Cause:** times-by-season \
    **Decision:** the times the section gives \
    **Misses:**
      - **Miss:** winter-hours-not-read \
        **Kind:** place not read \
        **Place:** `docs/guide.md § The Ferry` \
        **Reads:**
          - `docs/guide.md § The Ferry`

    **Proposed Change:**
      - **Kind:** revision \
        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \
        **Places:**
          - **Place:** `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: ferry-times-stated]` \
            **Order:** primary \
            **Settles:**
              - reviewer-1-last-crossing-in-winter

## Settlement

**Ending:** its own settling \
**Earlier Reports:**
  - none

**Settling Reads:**
  - `docs/guide.md § The Ferry`

**Settlements:**
  - **Settlement:** times-by-season-kept \
    **Settled Findings:**
      - reviewer-1-last-crossing-in-winter

    **Verdict:** implementation flaw \
    **Required By:** the goals \
    **Justifying Goals:**
      - guide-says-when-the-ferry-runs

    **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
    **Order:** primary \
    **Fix Authority:** the builder's \
    **Cause:** times-by-season \
    **How Settled:** The Objective was revised to give each season's first and last crossing.
