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

  - **Fixture:** ferry-self-review-structural-stop \
    **Holds:** a self-review that stops at the structure before approval \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1 \
      **Stopped At:** the structure

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
        - `docs/guide.md`

      ## Findings

      **Records:**
        - **Finding:** objective-specifies-typesetting \
          **Verdict:** implementation flaw \
          **Decision:** The result the ferry step promises. \
          **Affected Step Objectives:**
            - section-gives-the-first-and-last-crossing

          **Description:** The Objective specifies typesetting the section in blue ink. \
          **Evidence:**
            - **Description:** The section can be printed in blue without giving any ferry times. \
              **Places:**
                - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps`

          **Rationale:** The Objective prescribes a means and leaves the intended change untested. \
          **Possible Fix:**
            - **Kind:** revision \
              **Delivers:** An Objective stating the crossing times the visitor can learn from the guide.

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

      **Settlements:**
        - **Settlement:** restore-the-outcome \
          **Settled Findings:**
            - objective-specifies-typesetting

          **Verdict:** implementation flaw \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The visitor needs the first and last ferry times. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Places:**
            - **Place:** `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps` \
              **Order:** primary \
              **Settles:**
                - objective-specifies-typesetting

          **How Settled:** Rewrite the Objective to state what the visitor learns.
      ```


  - **Fixture:** ferry-self-review-unexplained-stop \
    **Holds:** a pre-approval self-review claiming a structural stop with no finding \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1 \
      **Stopped At:** the structure

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

  - **Fixture:** ferry-design-with-means-for-objective \
    **Holds:** the drafted ferry design with a step Objective that prescribes a means \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
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

              **State:** The ferry section is typeset in blue ink.

      ## Design Log Entries

      **Records:**
        - **Entry:** entered-1 \
          **Timestamp:** 2026-01-01T00:00:00Z \
          **Reason:** taken up

        - **Entry:** goals-agreed-1 \
          **Timestamp:** 2026-01-01T00:00:01Z \
          **Design Version:** 1.0.0

        - **Entry:** plan-change-1 \
          **Timestamp:** 2026-01-01T00:00:02Z \
          **Design Version:** 1.0.1

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-with-replaced-goal \
    **Holds:** the reassessed ferry design with the replacement goal agreed in its second major version \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 2.0.1 \
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
        - **Name:** guide-identifies-available-crossings \
          **Description:** The guide identifies which crossings are available.

      ## The Design Frame

      ### Scope

      **Cases:**
        - **Name:** visitor-planning-a-crossing \
          **Goals:**
            - guide-identifies-available-crossings

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
            - guide-identifies-available-crossings

          **Description:** The times stand in the section naming the ferry, and nowhere else.

      ### Frame Outcomes

      **Records:**
        - **Name:** crossing-planned-from-the-guide \
          **Goals:**
            - guide-identifies-available-crossings

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
                - guide-identifies-available-crossings

              **Upholds Frame Outcomes:**
                - crossing-planned-from-the-guide

              **State:** The section naming the ferry gives the time of the first crossing and of the last.

      ## Design Log Entries

      **Records:**
        - **Entry:** entered-1 \
          **Timestamp:** 2026-01-01T00:00:00Z \
          **Reason:** taken up

        - **Entry:** goals-agreed-1 \
          **Timestamp:** 2026-01-01T00:00:01Z \
          **Design Version:** 1.0.0

        - **Entry:** plan-change-1 \
          **Timestamp:** 2026-01-01T00:00:02Z \
          **Design Version:** 1.0.1

        - **Entry:** self-review-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0

        - **Entry:** design-reassessment-1 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 2.0.0 \
          **Cause:** changed foundation: quay-rebuilt finished

        - **Entry:** goals-agreed-2 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 2.0.0

        - **Entry:** plan-change-2 \
          **Timestamp:** 2026-01-01T00:00:06Z \
          **Design Version:** 2.0.1

      ## Out of Scope

      Nothing the research found is left out.
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

  - **Fixture:** ferry-self-review-before-approval \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Goal Judgments cover the goal before approval, its Reads the design and the guide, three Builder Checks, of steers against the user's messages, of linked work and of the problem's re-evaluation, and a Settlement naming no earlier report \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1 \
      **Goal Comparison:** compared with reviewed goals

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
        - `docs/guide.md`

      ## Goal Judgments

      **Records:**
        - **Goal:** guide-says-when-the-ferry-runs \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** met \
          **Genuine Change:** met

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
