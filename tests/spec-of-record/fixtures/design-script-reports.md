**Records:**
  - **Fixture:** ferry-research-report \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0: its Reads the guide's section The Ferry, one Search by meaning naming the design's goal and giving that section, one Read Assessment of that section whose Impact is changes, and a Settlement naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-1

      ## Reading

      **Design Version:** 1.0.0 \
      **Reads:**
        - `docs/guide.md § The Ferry`

      ## Searches

      **Records:**
        - **Search:** ferry-times-by-meaning \
          **For:** every place saying when the ferry runs \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** meaning \
          **Query:** The ferry makes its first crossing in the morning and its last in the evening. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Read Assessments

      **Records:**
        - **Area:** `docs/guide.md § The Ferry` \
          **Impact:**
            - changes

          **Reason:** The section names the ferry and is where its times are to stand. \
          **Goals:**
            - guide-says-when-the-ferry-runs

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none
      ```

  - **Fixture:** ferry-review-report \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide, read at version 1.0.1: one reviewer's Reading, one Finding marked an implementation flaw naming the design's goal, one Search by meaning naming no goal, one Cause holding a Miss and a revision of the design's step, and a Settlement keeping the finding on the builder's authority \
    **Snippet:**

      ```markdown
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
      ```

  - **Fixture:** ferry-self-review-report \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, three Builder Checks, of steers against the user's messages, of linked work and of the problem's re-evaluation, and a Settlement naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
        - `docs/guide.md`

      ## Builder Checks

      **Records:**
        - **Check:** steers-read-against-the-messages \
          **Kind:** steers against the user's messages \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Result:** The design records no steer, and the user gave none.

        - **Check:** work-handed-on \
          **Kind:** linked work \
          **Places Checked:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Out of Scope`

          **Result:** The design hands no work on.

        - **Check:** problem-read-against-the-guide \
          **Kind:** problem re-evaluation \
          **Places Checked:**
            - `docs/guide.md § The Ferry`

          **Result:** The section still names the ferry and gives no time.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** audit-report-finding-nothing \
    **Holds:** the report of a specs audit of the design ferry-times-in-the-guide, read at version 1.0.1, holding no finding: its Reads the guide, and a Settlement ended by its own settling, naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** audit-specs-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `docs/guide.md`

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none
      ```

  - **Fixture:** audit-report-holding-a-stale-stamp \
    **Holds:** the report of a specs audit of the design ferry-times-in-the-guide, read at version 1.0.1, holding no finding: its Reads the guide, and a Settlement whose Validated holds a stamp of a hash taken over no text it holds, ended by its own settling, naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** audit-specs-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `docs/guide.md`

      ## Settlement

      **Validated:** 2026-01-01T00:00:00Z sha256:0123456789abcdef \
      **Ending:** its own settling \
      **Earlier Reports:**
        - none
      ```

  - **Fixture:** audit-report-stamped-ending-otherwise \
    **Holds:** the report of a specs audit of the design ferry-times-in-the-guide, read at version 1.0.1, holding no finding: its Reads the guide, and a Settlement whose Validated holds a stamp, its Ending a coffee break, naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** audit-specs-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `docs/guide.md`

      ## Settlement

      **Validated:** 2026-01-01T00:00:00Z sha256:0123456789abcdef \
      **Ending:** a coffee break \
      **Earlier Reports:**
        - none
      ```
