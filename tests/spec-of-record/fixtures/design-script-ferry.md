**Records:**
  - **Fixture:** island-guide \
    **Holds:** a guide to an island: a line saying a visitor arrives by water, a section The Ferry naming the north quay the ferry leaves from, and a section The Lighthouse naming its keeper \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.
      ```

  - **Fixture:** ferry-design \
    **Holds:** a design document named ferry-times-in-the-guide, in progress, of the kind documentation, its Target the guide, naming no other design: one goal, one case, one principle, one Frame Outcome, one Assessed Area resting on a handed-off judgment's report, and one step holding one Objective, with no log and no stamp \
    **Snippet:**

      ```markdown
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
      ```

  - **Fixture:** ferry-diagnosis \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment: one Flaw citing a finding of an adversarial review's report, one Root Cause the Flaw names, and a Scope holding a question and its answer \
    **Snippet:**

      ```markdown
      # Diagnosis

      **Design:** ferry-times-in-the-guide \
      **Design Reassessment:** design-reassessment-1 \
      **Flaw Set:** none \
      **Earlier Diagnoses:** none

      ## Flaws

      **Records:**
        - **Flaw:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Findings [Finding: reviewer-1-last-crossing-in-winter]` \
          **Still Applies:** yes \
          **Root Cause:** one-season-assumed

      ## Root Causes

      **Records:**
        - **Root Cause:** one-season-assumed \
          **Question:** What did every flaw take for granted? \
          **Description:** The design took the ferry to keep one set of hours all year. \
          **Account:** The rebuilt goals name each season.

      ## Scope

      **Question:** Is the scope too narrow or too wide? \
      **Answer:** Too narrow: it left the seasons out.
      ```
