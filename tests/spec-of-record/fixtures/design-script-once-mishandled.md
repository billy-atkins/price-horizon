**Records:**
  - **Fixture:** ferry-design-holding-the-old-depends-on-field \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its header holding a field Depends On naming quay-rebuilt in place of Depends On Designs \
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
      **Depends On:** quay-rebuilt \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-drafted-naming-a-gone-design \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Depends On Designs naming tide-tables-printed \
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
      **Depends On Designs:** tide-tables-printed \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-drafted-naming-a-complete-design \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Depends On Designs naming harbor-dredged \
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
      **Depends On Designs:** harbor-dredged \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** harbor-dredged-complete \
    **Holds:** the design harbor-dredged, complete at version 1.0.1, its Validated a stamp current with its content, a log of five entries ending in apply, naming no other design \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** harbor-dredged \
      **Version:** 1.0.1 \
      **Status:** complete \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:6e99903130131061

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

          **Assessment:** `.ai/tmp/design-specs/harbor-dredged/reports/handed-off-judgment/1.md`

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

  - **Fixture:** ferry-research-report-reading-the-lighthouse \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide, read at version 1.0.0: one Search by meaning naming the design's goal and giving the guide's sections The Ferry and The Lighthouse, and one Read Assessment, of The Ferry alone \
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
            - `docs/guide.md § The Lighthouse`

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
