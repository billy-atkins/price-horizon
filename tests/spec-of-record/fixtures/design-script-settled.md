**Records:**
  - **Fixture:** review-taken-up-and-settled \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-and-stamped \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority, its Settlement's Validated a stamp current with its text \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

      **Validated:** 2026-11-25T21:41:45Z sha256:a72d424c84c6a348 \
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

  - **Fixture:** ferry-design-drafted-after-its-first-round \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of four entries: entered, goals-agreed, plan-change and adversarial-review-1, the round's counts taken from its report \
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

        - **Entry:** adversarial-review-1 \
          **Timestamp:** 2026-11-25T21:41:45Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 1 \
          **Nits:** 0 \
          **Dropped:** 0 \
          **Led To:** validating

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** review-taken-up-its-finding-dropped \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement dropping the finding, giving its reason and naming no Cause \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

          **Verdict:** dropped \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Departure Reason:** The ferry keeps one set of hours. \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-rationale-changed \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; the Rationale of its Finding changed since the take-up to say a visitor in winter is left on the quay \
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

          **Rationale:** A visitor in winter is left on the quay. \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-its-searches-removed \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Searches part removed since the take-up \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-settling-its-finding-twice \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; a second Settlement, times-by-season-again, settling the same finding \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

        - **Settlement:** times-by-season-again \
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

  - **Fixture:** review-taken-up-its-settlement-naming-a-cause-not-held \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement naming the Cause times-by-tide, which the report does not hold \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **Cause:** times-by-tide \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-settlement-carried-by-a-step-not-held \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement carried by no-such-step, a step the design does not hold \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **Carried By:** no-such-step \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-justified-by-a-goal-not-held \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement's Justifying Goals naming guide-says-what-the-ferry-costs, no goal of the design \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
            - guide-says-what-the-ferry-costs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-required-by-the-rules-justified-by-goals \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement's Required By the rules, holding Justifying Goals and no Justifying Rules \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **Required By:** the rules \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-on-the-users-authority-with-no-decision \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the user's authority, holding no User Decision \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **Fix Authority:** the user's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-keeping-a-design-flaw-on-the-builders-authority \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement's Verdict design flaw \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

          **Verdict:** design flaw \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-settlement-stating-order-secondary \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement stating Order secondary, its finding landing on no earlier change \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **Order:** secondary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-changed-place-stating-order-tertiary \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; the place its Cause's change changes stating Order tertiary \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
                  **Order:** tertiary \
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

  - **Fixture:** review-taken-up-departing-from-its-verdict-unreasoned \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement's Verdict nit, departing from the Finding's with no Departure Reason \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

          **Verdict:** nit \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-settling-reads-leaving-out-the-evidence \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settling Reads the guide's section The Lighthouse alone, leaving out The Ferry its Finding's Evidence names \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
        - `docs/guide.md § The Lighthouse`

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

  - **Fixture:** review-taken-up-holding-no-causes \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, no Causes part, and a Settlement naming no Cause keeping the finding on the builder's authority \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-settlement-stating-no-ending \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Settlement stating no Ending \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-its-cause-holding-no-misses \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Cause holding no Misses \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

      ## Causes

      **Records:**
        - **Cause:** times-by-season \
          **Decision:** the times the section gives \
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

  - **Fixture:** review-taken-up-its-revision-rewriting-no-decision \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; its Cause's revision naming no Decision Rewritten \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-its-tactical-fix-naming-a-search-by-meaning \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause whose change is a tactical fix naming each-season-named, a Search by meaning the builder added to the Searches part after the reviewer's, and a Settlement keeping the finding on the builder's authority \
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

        - **Search:** each-season-named \
          **For:** every place naming one season alone \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** meaning \
          **Query:** The ferry keeps one set of hours. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
            - **Kind:** tactical fix \
              **Search:** each-season-named \
              **Reason:** The Objective's meaning stands, and only its wording names one season. \
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

  - **Fixture:** review-taken-up-its-tactical-fix-citing-a-search-not-held \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause whose change is a tactical fix naming no-such-search, which the report does not hold, beside a Search by meaning the builder added to the Searches part, and a Settlement keeping the finding on the builder's authority \
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

        - **Search:** each-season-named \
          **For:** every place naming one season alone \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** meaning \
          **Query:** The ferry keeps one set of hours. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
            - **Kind:** tactical fix \
              **Search:** no-such-search \
              **Reason:** The Objective's meaning stands, and only its wording names one season. \
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

  - **Fixture:** second-review-taken-up-landing-on-the-first \
    **Holds:** the second adversarial review's report on the design ferry-times-in-the-guide taken up, its reviewer reviewer-2, its Earlier Reports naming the first round's report, its one Finding landing on that round's Cause times-by-season, and its Settlement stating Order secondary \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-2

      ## Reading

      **Design Version:** 1.0.1 \
      **Reviewer Readings:**
        - **Reviewer:** reviewer-2 \
          **Collecting Reads:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
            - `docs/guide.md`

          **Earlier Reports:**
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md`

          **Weighing Reads:**
            - `docs/guide.md § The Ferry`

      ## Findings

      **Records:**
        - **Finding:** reviewer-2-last-crossing-in-winter \
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

          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`

      ## Searches

      **Records:**
        - **Search:** reviewer-2-winter-hours \
          **For:** every place giving the hours the ferry keeps in winter \
          **Goals:**
            - none

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: b029c728a2c79129051116cc17b29052d3a7fca766c1d99923cba2af931ea448
      - Reading: 7c5eede6bc1b565fcafc36abc47c93ace5979e65fbc402ea95bbc235c6a36b3d
      - Findings: ed7a092c080348e5750e248d037dd3bdce008bd024dfb6444b7d0199d7b6f6c6
      - Searches: 485198e8bf97f28b126fb36588c2efe78f6674ece38343fea15f6bdc121b254c, 14 lines

      ## Causes

      **Records:**
        - **Cause:** times-by-season-again \
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
                    - reviewer-2-last-crossing-in-winter

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md`

      **Settling Reads:**
        - `docs/guide.md § The Ferry`

      **Settlements:**
        - **Settlement:** times-by-season-again-kept \
          **Settled Findings:**
            - reviewer-2-last-crossing-in-winter

          **Verdict:** implementation flaw \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** secondary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season-again \
          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]` \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** second-review-taken-up-listing-no-earlier-report \
    **Holds:** the second adversarial review's report on the design ferry-times-in-the-guide taken up, its reviewer reviewer-2, its Earlier Reports none, its one Finding landing on the first round's Cause times-by-season, and its Settlement stating Order secondary \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-2

      ## Reading

      **Design Version:** 1.0.1 \
      **Reviewer Readings:**
        - **Reviewer:** reviewer-2 \
          **Collecting Reads:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
            - `docs/guide.md`

          **Earlier Reports:**
            - none

          **Weighing Reads:**
            - `docs/guide.md § The Ferry`

      ## Findings

      **Records:**
        - **Finding:** reviewer-2-last-crossing-in-winter \
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

          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`

      ## Searches

      **Records:**
        - **Search:** reviewer-2-winter-hours \
          **For:** every place giving the hours the ferry keeps in winter \
          **Goals:**
            - none

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: b029c728a2c79129051116cc17b29052d3a7fca766c1d99923cba2af931ea448
      - Reading: dc12480570b1cac2e9ef315b189f996f3b6c29f225304d565ce805d96db4769d
      - Findings: ed7a092c080348e5750e248d037dd3bdce008bd024dfb6444b7d0199d7b6f6c6
      - Searches: 485198e8bf97f28b126fb36588c2efe78f6674ece38343fea15f6bdc121b254c, 14 lines

      ## Causes

      **Records:**
        - **Cause:** times-by-season-again \
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
                    - reviewer-2-last-crossing-in-winter

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none

      **Settling Reads:**
        - `docs/guide.md § The Ferry`

      **Settlements:**
        - **Settlement:** times-by-season-again-kept \
          **Settled Findings:**
            - reviewer-2-last-crossing-in-winter

          **Verdict:** implementation flaw \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** secondary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season-again \
          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]` \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** second-review-taken-up-stating-primary \
    **Holds:** the second adversarial review's report on the design ferry-times-in-the-guide taken up, its reviewer reviewer-2, its Earlier Reports naming the first round's report, its one Finding landing on that round's Cause times-by-season, and its Settlement stating Order primary \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-2

      ## Reading

      **Design Version:** 1.0.1 \
      **Reviewer Readings:**
        - **Reviewer:** reviewer-2 \
          **Collecting Reads:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`
            - `docs/guide.md`

          **Earlier Reports:**
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md`

          **Weighing Reads:**
            - `docs/guide.md § The Ferry`

      ## Findings

      **Records:**
        - **Finding:** reviewer-2-last-crossing-in-winter \
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

          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`

      ## Searches

      **Records:**
        - **Search:** reviewer-2-winter-hours \
          **For:** every place giving the hours the ferry keeps in winter \
          **Goals:**
            - none

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: b029c728a2c79129051116cc17b29052d3a7fca766c1d99923cba2af931ea448
      - Reading: 7c5eede6bc1b565fcafc36abc47c93ace5979e65fbc402ea95bbc235c6a36b3d
      - Findings: ed7a092c080348e5750e248d037dd3bdce008bd024dfb6444b7d0199d7b6f6c6
      - Searches: 485198e8bf97f28b126fb36588c2efe78f6674ece38343fea15f6bdc121b254c, 14 lines

      ## Causes

      **Records:**
        - **Cause:** times-by-season-again \
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
                    - reviewer-2-last-crossing-in-winter

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md`

      **Settling Reads:**
        - `docs/guide.md § The Ferry`

      **Settlements:**
        - **Settlement:** times-by-season-again-kept \
          **Settled Findings:**
            - reviewer-2-last-crossing-in-winter

          **Verdict:** implementation flaw \
          **Required By:** the goals \
          **Justifying Goals:**
            - guide-says-when-the-ferry-runs

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season-again \
          **Lands On:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]` \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** research-taken-up-its-searches-added-after \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, handed back holding no Searches part and taken up, its Hand-back part holding no fingerprint of one, and a Searches part of one Search by meaning added after the take-up \
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

      ## Hand-back

      - Title: bd170efe703e0fe9bfb4bb2282411467169c792819febf653416223ced887a59
      - Reading: d09c580559a7934a8b2489384503c29d1a108cb31eb8cced18358a9ceaf131e6
      - Read Assessments: 8c0b8bda58043e615846ef27d64154688b69cd2589e97a705d928a98851756ef

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none
      ```

  - **Fixture:** review-taken-up-its-reviewers-search-changed \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, read at version 1.0.1: one Finding marked an implementation flaw, the reviewer's one Search by meaning, one Cause revising the design's step, and a Settlement keeping the finding on the builder's authority; the For of the reviewer's Search changed since the take-up to every place giving the hours the ferry keeps \
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
          **For:** every place giving the hours the ferry keeps \
          **Goals:**
            - none

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

  - **Fixture:** review-taken-up-making-no-search-its-builder-adding-one-and-its-rationale-changed \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide whose reviewer handed no Searches part back, taken up and settled, a Searches part holding the builder's own Search by meaning each-season-named added after it, and the Rationale of its Finding changed since the take-up \
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

          **Rationale:** A visitor in winter is left on the quay. \
          **Possible Fix:**
            - **Kind:** revision \
              **Delivers:** An Objective giving the first and the last crossing of each season.

      ## Searches

      **Records:**
        - **Search:** each-season-named \
          **For:** every place naming one season alone \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** meaning \
          **Query:** The ferry keeps one set of hours. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475

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

  - **Fixture:** review-settling-the-winter-judgment \
    **Holds:** the settled review whose primary change also settles the winter judgment's finding \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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
                    - winter-crossing

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

  - **Fixture:** winter-judgment-adversarial-cause \
    **Holds:** the winter crossing's marked Settlement citing the Cause in adversarial-review round 1 \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-1

      ## Settlement

      **Settlements:**
        - **Settlement:** winter-hours \
          **Settled Findings:**
            - winter-crossing

          **Verdict:** implementation flaw \
          **Cause:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`
      ```

  - **Fixture:** winter-judgment-post-apply-cause \
    **Holds:** the winter crossing's marked Settlement citing the Cause in post-apply-review round 1 \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-1

      ## Settlement

      **Settlements:**
        - **Settlement:** winter-hours \
          **Settled Findings:**
            - winter-crossing

          **Verdict:** implementation flaw \
          **Cause:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/post-apply-review/1.md § Causes [Cause: times-by-season]`
      ```

  - **Fixture:** winter-judgment-another-rounds-cause \
    **Holds:** the winter crossing's marked Settlement citing the Cause in adversarial-review round 2 \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-1

      ## Settlement

      **Settlements:**
        - **Settlement:** winter-hours \
          **Settled Findings:**
            - winter-crossing

          **Verdict:** implementation flaw \
          **Cause:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/2.md § Causes [Cause: times-by-season]`
      ```

  - **Fixture:** winter-judgment-no-cause \
    **Holds:** the winter crossing's marked Settlement without a Cause citation \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-1

      ## Settlement

      **Settlements:**
        - **Settlement:** winter-hours \
          **Settled Findings:**
            - winter-crossing

          **Verdict:** implementation flaw
      ```

  - **Fixture:** winter-judgment-later-no-cause \
    **Holds:** the winter crossing's marked Settlement without a Cause citation in a later judgment \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** handed-off-judgment-2

      ## Settlement

      **Settlements:**
        - **Settlement:** winter-hours \
          **Settled Findings:**
            - winter-crossing

          **Verdict:** implementation flaw
      ```

  - **Fixture:** adversarial-round-before-independent-judgment \
    **Holds:** an earlier-form adversarial round followed by a separately logged winter judgment \
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

        - **Entry:** adversarial-review-1 \
          **Timestamp:** 2026-11-25T21:41:45Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 1 \
          **Nits:** 0 \
          **Dropped:** 0 \
          **Led To:** validating

        - **Entry:** handed-off-judgment-1 \
          **Timestamp:** 2026-11-25T21:42:45Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 1 \
          **Nits:** 0 \
          **Dropped:** 0

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** post-apply-round-before-independent-judgment \
    **Holds:** an earlier-form post-apply round followed by a separately logged winter judgment \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `docs/notes.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:3359fa6fb8f631f4

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

        - **Entry:** plan-approval-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1 \
          **Approval:** approved

        - **Entry:** apply-1 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 1.0.1

        - **Entry:** post-apply-review-1 \
          **Timestamp:** 2026-11-25T21:41:45Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 1 \
          **Nits:** 0 \
          **Dropped:** 0 \
          **Led To:** validating

        - **Entry:** handed-off-judgment-1 \
          **Timestamp:** 2026-11-25T21:42:45Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 1 \
          **Nits:** 0 \
          **Dropped:** 0

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** review-holding-misses-for-the-judgments-cause \
    **Holds:** the round with Misses on a Cause that only a handed-off judgment justified \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: f65373ca24a6137d34ca60e8f006d7b17385ff594e8437e93baf4190dffa4068, 14 lines

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

        - **Cause:** night-crossing \
          **Decision:** the times the section gives \
          **Misses:**
            - **Miss:** winter-hours-not-read \
              **Kind:** place not read \
              **Place:** `docs/guide.md § The Ferry` \
              **Reads:**
                - `docs/guide.md § The Ferry`

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

  - **Fixture:** review-changing-the-guide-for-the-judgment-alone \
    **Holds:** a round with no Findings or Settlements of its own whose primary changed place settles the winter judgment alone \
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

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f

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
                    - winter-crossing

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none

      **Settling Reads:**
        - `docs/guide.md § The Ferry`
      ```
