**Records:**
  - **Fixture:** walkers-notes-naming-the-north-wall-of-the-quay \
    **Holds:** a page of notes, one sentence holding the words north and quay with other words between them \
    **Snippet:**

      ```markdown
      # Notes

      A walker's notes: the north wall of the quay is slippery after rain.
      ```

  - **Fixture:** ferry-design-drafted-retiring-the-north-quay \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Retired Phrases retiring north quay for north pier \
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

      ## Retired Phrases

      **Records:**
        - **Phrase:** north quay \
          **Replacement:** north pier \
          **Stays Right:** none

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

  - **Fixture:** ferry-design-drafted-retiring-the-south-quay \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Retired Phrases retiring south quay for north pier \
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

      ## Retired Phrases

      **Records:**
        - **Phrase:** south quay \
          **Replacement:** north pier \
          **Stays Right:** none

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

  - **Fixture:** ferry-design-applying-retiring-the-north-quay \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide, a log of five entries ending in apply, its Retired Phrases retiring north quay for north pier \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:7013bf55c36d31e2

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

      ## Retired Phrases

      **Records:**
        - **Phrase:** north quay \
          **Replacement:** north pier \
          **Stays Right:** none

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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-retiring-the-north-quay-in-a-fixture-file \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide and the fixture file tests/spec-of-record/fixtures/guide.md, a log of five entries ending in apply, its Retired Phrases retiring north quay for north pier \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `tests/spec-of-record/fixtures/guide.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:5aefc191af4c587b

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

      ## Retired Phrases

      **Records:**
        - **Phrase:** north quay \
          **Replacement:** north pier \
          **Stays Right:** none

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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** island-guide-naming-the-north-pier \
    **Holds:** a guide to an island: a line saying a visitor arrives by water, a section The Ferry naming the north pier the ferry leaves from, and a section The Lighthouse naming its keeper \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north pier.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.
      ```

  - **Fixture:** island-guide-its-lighthouse-beam-reaching-the-north-quay \
    **Holds:** a guide to an island: a section The Ferry naming the north quay the ferry leaves from, and a section The Lighthouse saying its keeper trims the lamp at dusk and its beam reaches the north quay \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk, and its beam reaches the north quay.
      ```

  - **Fixture:** index-listing-two-files \
    **Holds:** the index of a fixtures folder, a title and a table listing two files, guide.md and harbor.md, with their descriptions \
    **Snippet:**

      ```markdown
      # The Kept Tests' Fixtures

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `guide.md` | One sentence naming the quay a ferry leaves from |
      | `harbor.md` | The same sentence, kept a second time |
      ```

  - **Fixture:** review-handed-back-searching-by-terms \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, its reviewer's one Search a Search by terms for north quay, its Places the guide's section The Ferry and docs/notes.md \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** compared with reviewed goals

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

      ## Goal Judgments

      **Records:**
        - **Goal:** guide-says-when-the-ferry-runs \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** met \
          **Genuine Change:** met

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

          **Kind:** terms \
          **Query:** north quay \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`
      ```

  - **Fixture:** review-handed-back-searching-by-terms-its-places-none \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, its reviewer's one Search a Search by terms for north quay, its Places none \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** compared with reviewed goals

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

      ## Goal Judgments

      **Records:**
        - **Goal:** guide-says-when-the-ferry-runs \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** met \
          **Genuine Change:** met

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

          **Kind:** terms \
          **Query:** north quay \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - none
      ```

  - **Fixture:** review-taken-up-searching-by-terms \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up and settled, its reviewer's one Search a Search by terms for north quay, its Places the guide's section The Ferry and docs/notes.md, its Settlement settling its one Finding \
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

          **Kind:** terms \
          **Query:** north quay \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: 9f87836b4d90bf0d3f2efbfd5925c61e9cf2588b2805f225810474583110dc61, 14 lines

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

  - **Fixture:** review-taken-up-searching-by-terms-its-finding-unsettled \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up and settled, its reviewer's one Search a Search by terms for north quay, its Places the guide's section The Ferry and docs/notes.md, its Settlement settling reviewer-1-another-finding in place of its one Finding \
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

          **Kind:** terms \
          **Query:** north quay \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`

      ## Hand-back

      - Title: 995211494468f397e04f1afc8673dc0b73832bdfee063eae0b341f25ef92381e
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: d6abcb124a030a819207797c7e369642db26ccd7497be747687ca1a138e62475
      - Searches: 9f87836b4d90bf0d3f2efbfd5925c61e9cf2588b2805f225810474583110dc61, 14 lines

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

  - **Fixture:** research-handed-back-searching-both-ways \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for north quay, as its cold agent hands it back \
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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
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
      ```

  - **Fixture:** research-taken-up-searching-both-ways \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for north quay, taken up, its Hand-back part holding the fingerprint of each part its cold agent wrote \
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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
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
      - Searches: b8c4f12b2a2e287df50bc7877e12f5062afb09d5b67e807cc5bae2f7d6282c55
      - Read Assessments: 8c0b8bda58043e615846ef27d64154688b69cd2589e97a705d928a98851756ef

      ## Settlement

      **Ending:** its own settling \
      **Earlier Reports:**
        - none
      ```

  - **Fixture:** research-searching-both-ways-narrowed-to-the-guide \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for north quay, its Search by terms narrowed to docs/guide.md, with a Settlement and no Hand-back part \
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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Narrowed To:**
            - `docs/guide.md`

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

  - **Fixture:** research-searching-both-ways-its-meaning-narrowed-to-the-guide \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for north quay, its Search by meaning narrowed to docs/guide.md, with a Settlement and no Hand-back part \
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
          **Narrowed To:**
            - `docs/guide.md`

          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
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

  - **Fixture:** research-handed-back-searching-by-terms-for-no-word \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for three dots, as its cold agent hands it back \
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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** ... \
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
      ```

  - **Fixture:** research-searching-both-ways-under-an-earlier-target-name \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0, its one Read Assessment of the guide's section The Ferry, naming the design's goal in a Search by meaning giving that section and in ferry-times-by-terms, a Search by terms for north quay, each Search naming its target current-durable-files and narrowed to docs and specs, with a Settlement and no Hand-back part \
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
          **Target:** current-durable-files \
          **Narrowed To:**
            - `docs`
            - `specs`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Target:** current-durable-files \
          **Narrowed To:**
            - `docs`
            - `specs`

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

  - **Fixture:** review-taken-up-its-tactical-fix-changing-what-its-search-of-the-design-found \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up and settled by a tactical fix naming first-crossing-named, a Search by terms of the design document the builder added to the Searches part, its Places and the fix's the Objective of the design's step \
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

        - **Search:** first-crossing-named \
          **For:** every place of the design naming the first crossing \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** first crossing \
          **Exact:** yes \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`

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
              **Search:** first-crossing-named \
              **Reason:** The Objective's meaning stands, and only its wording names one season. \
              **Places:**
                - **Place:** `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]` \
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

  - **Fixture:** review-taken-up-its-tactical-fix-changing-the-step-alone \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up and settled by a tactical fix naming first-crossing-named, a Search by terms of the design document the builder added to the Searches part, its Places the Objective of the design's step, the fix's the step alone \
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

        - **Search:** first-crossing-named \
          **For:** every place of the design naming the first crossing \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** first crossing \
          **Exact:** yes \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`

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
              **Search:** first-crossing-named \
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

  - **Fixture:** review-taken-up-its-tactical-fix-naming-a-search-of-the-design-placing-none \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide taken up and settled by a tactical fix naming first-crossing-named, a Search by terms of the design document the builder added to the Searches part, its Places none, the fix's the Objective of the design's step \
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

        - **Search:** first-crossing-named \
          **For:** every place of the design naming the first crossing \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** first crossing \
          **Exact:** yes \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - none

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
              **Search:** first-crossing-named \
              **Reason:** The Objective's meaning stands, and only its wording names one season. \
              **Places:**
                - **Place:** `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]` \
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

  - **Fixture:** review-taken-up-making-no-search-its-builder-adding-a-search-of-the-design \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide whose reviewer handed no Searches part back, taken up and settled by a tactical fix naming first-crossing-named, and a Searches part holding that Search by terms of the design document added after the take-up, its Places and the fix's the Objective of the design's step \
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
        - **Search:** first-crossing-named \
          **For:** every place of the design naming the first crossing \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** first crossing \
          **Exact:** yes \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`

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
            - **Kind:** tactical fix \
              **Search:** first-crossing-named \
              **Reason:** The Objective's meaning stands, and only its wording names one season. \
              **Places:**
                - **Place:** `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]` \
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

  - **Fixture:** ferry-design-applying-to-the-guide-the-notes-and-the-fixtures \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide, docs/notes.md and the folder tests/spec-of-record/fixtures/, and a log of five entries ending in apply \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `docs/notes.md`; `tests/spec-of-record/fixtures/` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:6dbf8df848a9a8af

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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-to-the-guide-and-the-notes \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide and docs/notes.md, and a log of five entries ending in apply \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** post-apply-review-taken-up-searching-the-operative-files-alone \
    **Holds:** a post-apply review's report on the design ferry-times-in-the-guide taken up, its finding and the finding's Settlement each lying in the writing, settled by a tactical fix naming ferry-times-by-terms, a Search by terms for north quay of the operative files giving the guide's section The Ferry and docs/notes.md, no Search of the fixture files beside it, the fix changing those two places \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** post-apply-review-1

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

          **Lies In:** the writing

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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Exact:** yes \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`

      ## Hand-back

      - Title: ca91fe73369d04df2a5030b9c2c36bfff06b023de176ece50845786cc2f67ea2
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: 9fe6f51b15e67999f6f9d9cd1291a7942f49f48421d4a31e5ca1cea5ed822199
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
              **Search:** ferry-times-by-terms \
              **Reason:** The section's meaning stands, and only its wording names the quay. \
              **Places:**
                - **Place:** `docs/guide.md § The Ferry` \
                  **Order:** primary \
                  **Settles:**
                    - reviewer-1-last-crossing-in-winter

                - **Place:** `docs/notes.md` \
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
          **Lies In:** the writing \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** post-apply-review-taken-up-searching-the-fixture-files-beside-changing-the-operative-places \
    **Holds:** a post-apply review's report on the design ferry-times-in-the-guide taken up, its finding and the finding's Settlement each lying in the writing, settled by a tactical fix naming ferry-times-by-terms, a Search by terms for north quay of the operative files giving the guide's section The Ferry and docs/notes.md, beside it ferry-times-by-terms-in-the-fixtures, the same asked of the current fixture files and giving the fixture files guide.md and harbor.md, the fix changing the two operative places alone \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** post-apply-review-1

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

          **Lies In:** the writing

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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Exact:** yes \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`

        - **Search:** ferry-times-by-terms-in-the-fixtures \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Exact:** yes \
          **Target:** current-fixture-files \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `tests/spec-of-record/fixtures/guide.md`
            - `tests/spec-of-record/fixtures/harbor.md`

      ## Hand-back

      - Title: ca91fe73369d04df2a5030b9c2c36bfff06b023de176ece50845786cc2f67ea2
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: 9fe6f51b15e67999f6f9d9cd1291a7942f49f48421d4a31e5ca1cea5ed822199
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
              **Search:** ferry-times-by-terms \
              **Reason:** The section's meaning stands, and only its wording names the quay. \
              **Places:**
                - **Place:** `docs/guide.md § The Ferry` \
                  **Order:** primary \
                  **Settles:**
                    - reviewer-1-last-crossing-in-winter

                - **Place:** `docs/notes.md` \
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
          **Lies In:** the writing \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```

  - **Fixture:** post-apply-review-taken-up-searching-the-fixture-files-beside-changing-every-place \
    **Holds:** a post-apply review's report on the design ferry-times-in-the-guide taken up, its finding and the finding's Settlement each lying in the writing, settled by a tactical fix naming ferry-times-by-terms, a Search by terms for north quay of the operative files giving the guide's section The Ferry and docs/notes.md, beside it ferry-times-by-terms-in-the-fixtures, the same asked of the current fixture files and giving the fixture files guide.md and harbor.md, the fix changing each of the four places \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** post-apply-review-1

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

          **Lies In:** the writing

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

        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Exact:** yes \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
            - `docs/notes.md`

        - **Search:** ferry-times-by-terms-in-the-fixtures \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Exact:** yes \
          **Target:** current-fixture-files \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `tests/spec-of-record/fixtures/guide.md`
            - `tests/spec-of-record/fixtures/harbor.md`

      ## Hand-back

      - Title: ca91fe73369d04df2a5030b9c2c36bfff06b023de176ece50845786cc2f67ea2
      - Reading: b3717fe41e62ad79543a93fdbdf93b42650fdb0f7fc56982b7e8eafd7fc54c2f
      - Findings: 9fe6f51b15e67999f6f9d9cd1291a7942f49f48421d4a31e5ca1cea5ed822199
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
              **Search:** ferry-times-by-terms \
              **Reason:** The section's meaning stands, and only its wording names the quay. \
              **Places:**
                - **Place:** `docs/guide.md § The Ferry` \
                  **Order:** primary \
                  **Settles:**
                    - reviewer-1-last-crossing-in-winter

                - **Place:** `docs/notes.md` \
                  **Order:** primary \
                  **Settles:**
                    - reviewer-1-last-crossing-in-winter

                - **Place:** `tests/spec-of-record/fixtures/guide.md` \
                  **Order:** primary \
                  **Settles:**
                    - reviewer-1-last-crossing-in-winter

                - **Place:** `tests/spec-of-record/fixtures/harbor.md` \
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
          **Lies In:** the writing \
          **Cause:** times-by-season \
          **How Settled:** The Objective was revised to give each season's first and last crossing.
      ```
