**Records:**
  - **Fixture:** ferry-design-drafted-its-goal-renamed \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its one goal named guide-gives-each-seasons-hours wherever the design names it \
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
        - **Name:** guide-gives-each-seasons-hours \
          **Description:** The guide says when the ferry runs.

      ## The Design Frame

      ### Scope

      **Cases:**
        - **Name:** visitor-planning-a-crossing \
          **Goals:**
            - guide-gives-each-seasons-hours

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
            - guide-gives-each-seasons-hours

          **Description:** The times stand in the section naming the ferry, and nowhere else.

      ### Frame Outcomes

      **Records:**
        - **Name:** crossing-planned-from-the-guide \
          **Goals:**
            - guide-gives-each-seasons-hours

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
                - guide-gives-each-seasons-hours

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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-drafted-its-objective-revised \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its step's one Objective named section-gives-each-seasons-crossings \
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
            - **Name:** section-gives-each-seasons-crossings \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** review-taken-up-its-goal-renamed-by-the-builder \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, its Finding naming the goal guide-says-when-the-ferry-runs, and the builder's Causes and Settlement naming that goal guide-gives-each-seasons-hours \
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
            - guide-gives-each-seasons-hours

          **Assessment:** The guide says when the ferry runs only where it gives each season's hours. \
          **Order:** primary \
          **Fix Authority:** the builder's \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** review-taken-up-its-finding-naming-an-objective \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, its Finding naming the design's goal and its step Objective section-gives-the-first-and-last-crossing, and the builder's Causes and Settlement \
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

          **Affected Step Objectives:**
            - section-gives-the-first-and-last-crossing

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
      - Findings: 79886c1ac5cda6b5ca4db7a89402132051b348b93cfce9521b7e3afcd87976ec
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

  - **Fixture:** review-taken-up-settling-another-finding \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote, its one Finding reviewer-1-last-crossing-in-winter, and the builder's Settlement settling reviewer-1-another-finding in its place \
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
            - reviewer-1-another-finding

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

  - **Fixture:** ferry-design-freed-of-a-complete-design \
    **Holds:** the design ferry-times-in-the-guide at version 2.0.0, freed of the design harbor-dredged: its Depends On Designs none, and a log of four entries, entered, goals-agreed, plan-change and a design-reassessment for a changed foundation naming harbor-dredged finished \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 2.0.0 \
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

        - **Entry:** design-reassessment-1 \
          **Timestamp:** 2026-11-25T21:29:15Z \
          **Design Version:** 2.0.0 \
          **Cause:** changed foundation: harbor-dredged finished

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** review-taken-up-cut-short-by-a-freeing \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide read at version 1.0.1, handed back before the design was freed and taken up after, its Hand-back part holding each cold part's fingerprint, its Settlement ended cut short by a design reassessment for a changed foundation, its finding's Fix Authority the user's, taken by a changed foundation \
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

      **Ending:** cut short, a design reassessment for a changed foundation \
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
          **User Decision:** taken by a changed foundation \
          **How Settled:** The design was freed, and is made afresh.
      ```
