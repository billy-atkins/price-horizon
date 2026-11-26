**Records:**
  - **Fixture:** ferry-design-not-started \
    **Holds:** the design ferry-times-in-the-guide not yet started: its Target none, its goals, each part of its frame and its steps not yet stated or drafted, and no log \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Status:** not-started \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** none \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** none

      ## The Problem

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs.

      ## Design Goals

      Not yet stated.

      ## The Design Frame

      ### Scope

      Not yet stated.

      ### Assessed Areas

      Not yet stated.

      ### Approach

      Not yet stated.

      ### Frame Outcomes

      Not yet stated.

      ## Design Plan Steps

      Not yet drafted.

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-drafted \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, its goals, frame and one step as the design of the ferry's times holds them, and a log of three entries: entered, goals-agreed and plan-change \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-agreed-undrafted \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.0, its goals and frame agreed and its steps not yet drafted, and a log of two entries: entered and goals-agreed \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.0 \
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

      Not yet drafted.

      ## Design Log Entries

      **Records:**
        - **Entry:** entered-1 \
          **Timestamp:** 2026-01-01T00:00:00Z \
          **Reason:** taken up

        - **Entry:** goals-agreed-1 \
          **Timestamp:** 2026-01-01T00:00:01Z \
          **Design Version:** 1.0.0

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-approved \
    **Holds:** the design ferry-times-in-the-guide approved at version 1.0.1, its Validated a stamp current with its content, and a log of four entries: entered, goals-agreed, plan-change and plan-approval \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** approved \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-approved-researched \
    **Holds:** the design ferry-times-in-the-guide approved at version 1.0.1, its Validated a stamp current with its content, and a log of five entries: entered, goals-agreed, a handed-off-judgment naming its first research report, plan-change and plan-approval \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** approved \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:6af162ca56010af9

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

        - **Entry:** handed-off-judgment-1 \
          **Timestamp:** 2026-01-01T00:00:02Z \
          **Design Version:** 1.0.0 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0

        - **Entry:** plan-change-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1

        - **Entry:** plan-approval-1 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 1.0.1 \
          **Approval:** approved

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-edited-since-its-stamp \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its log of six entries: entered, goals-agreed, a handed-off-judgment naming its first research report, plan-change, plan-approval and apply, and its Validated a stamp taken before its Problem gained the words or from where \
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
      **Validated:** 2026-01-01T00:00:00Z sha256:6af162ca56010af9

      ## The Problem

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs, or from where.

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

        - **Entry:** handed-off-judgment-1 \
          **Timestamp:** 2026-01-01T00:00:02Z \
          **Design Version:** 1.0.0 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0

        - **Entry:** plan-change-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1

        - **Entry:** plan-approval-1 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 1.0.1 \
          **Approval:** approved

        - **Entry:** apply-1 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 1.0.1

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-holding-a-field-out-of-its-form \
    **Holds:** the design ferry-times-in-the-guide in progress with no log, its header holding a field Reviewed By beside its own \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Status:** in-progress \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Reviewed By:** nobody \
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

  - **Fixture:** ferry-design-citing-a-heading-standing-nowhere \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Problem citing a section The Harbor of the guide in place of The Ferry \
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

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Harbor` names the ferry without saying when it runs.

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

  - **Fixture:** ferry-design-targeting-a-canon-file \
    **Holds:** the design ferry-times-in-the-guide of the kind documentation in progress at version 1.0.1, its Target naming the guide and the canon's file specs/methodology/code.md \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** in-progress \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `specs/methodology/code.md` \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-targeting-a-working-file \
    **Holds:** the design ferry-times-in-the-guide of the kind documentation in progress at version 1.0.1, its Target naming the working file .ai/follow-ups.md \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** in-progress \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `.ai/follow-ups.md` \
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

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** code-design-drafted \
    **Holds:** the design code-design of the kind code in progress at version 1.0.1, its Target `src/ferry.py`, its one Assessed Area and its step's What that file, its reports under the implementation skill's working files, and a log of three entries \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** code-design \
      **Version:** 1.0.1 \
      **Status:** in-progress \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** code \
      **Target:** `src/ferry.py` \
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
        - **Area:** `src/ferry.py` \
          **Impact:**
            - changes

          **Assessment:** `.ai/tmp/implement-specs/code-design/reports/handed-off-judgment/1.md`

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
          **What:** `src/ferry.py` \
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

  - **Fixture:** ferry-design-of-an-older-form \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1 as an older form wrote it: no Kind field, a Depends On field naming quay-rebuilt in place of Depends On Designs, and its goals a sentence of prose with no records \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** in-progress \
      **Source:** "The guide never says when the ferry runs." \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Depends On:** quay-rebuilt \
      **Validated:** none

      ## The Problem

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs.

      ## Design Goals

      The guide is to say when the ferry runs.

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

  - **Fixture:** design-holding-no-goals \
    **Holds:** the design no-goals in progress at version 1.0.1, holding no Design Goals section, and a log of three entries \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** no-goals \
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

          **Assessment:** `.ai/tmp/design-specs/no-goals/reports/handed-off-judgment/1.md`

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

  - **Fixture:** ferry-design-applying \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Validated a stamp current with its content, and a log of five entries: entered, goals-agreed, plan-change, plan-approval and apply \
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

  - **Fixture:** harbor-cited-applying \
    **Holds:** the design harbor-cited applying at version 1.0.1, its Problem citing a section The Harbor of the guide, its Validated a stamp current with its content, and a log of five entries ending in apply \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** harbor-cited \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:1c8aca0051b89bce

      ## The Problem

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Harbor` names the ferry without saying when it runs.

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

          **Assessment:** `.ai/tmp/design-specs/harbor-cited/reports/handed-off-judgment/1.md`

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

  - **Fixture:** ferry-design-applying-to-the-guide-and-the-tides \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide and the folder docs/tides/, and a log of five entries ending in apply \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `docs/tides/` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:88e4258484e8abd7

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

  - **Fixture:** ferry-design-applying-to-the-guide-and-the-tides-noting-a-user-edit \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its Target the guide and the folder docs/tides/, and a log of six entries ending in apply and a user-edit naming docs/notes.md \
    **Snippet:**

      ```markdown
      # Design Document

      **Name:** ferry-times-in-the-guide \
      **Version:** 1.0.1 \
      **Status:** applying \
      **Source:** "The guide never says when the ferry runs." \
      **Kind:** documentation \
      **Target:** `docs/guide.md`; `docs/tides/` \
      **Spawned By:** none \
      **Depends On Designs:** none \
      **Validated:** 2026-01-01T00:00:00Z sha256:88e4258484e8abd7

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

        - **Entry:** user-edit-1 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 1.0.1 \
          **Places:** `docs/notes.md`

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-its-audit-bypassed \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, a log of six entries ending in apply and an audit-bypass of the specs audit \
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

        - **Entry:** audit-bypass-1 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 1.0.1 \
          **Audit:** specs

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-its-audit-run \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, a log of six entries ending in apply and an audit-specs entry at version 1.0.1 \
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

        - **Entry:** audit-specs-1 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0 \
          **Led To:** validating \
          **Settled Sub-scopes:** documentation

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-applying-again-after-its-audit-bypassed \
    **Holds:** the design ferry-times-in-the-guide applying, a log ending in apply, an audit-bypass of the specs audit, an entered entry for a send-back, a plan-approval and a second apply \
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

        - **Entry:** audit-bypass-1 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 1.0.1 \
          **Audit:** specs

        - **Entry:** entered-2 \
          **Timestamp:** 2026-01-01T00:00:06Z \
          **Design Version:** 1.0.1 \
          **Reason:** sent back

        - **Entry:** plan-approval-2 \
          **Timestamp:** 2026-01-01T00:00:07Z \
          **Design Version:** 1.0.1 \
          **Approval:** approved

        - **Entry:** apply-2 \
          **Timestamp:** 2026-01-01T00:00:08Z \
          **Design Version:** 1.0.1

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** ferry-design-citing-the-guide-in-shorthand \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Problem citing the section The Ferry of guide.md by the file's name alone \
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

      The guide tells a visitor how to reach the island, and `guide.md § The Ferry` names the ferry without saying when it runs.

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

  - **Fixture:** ferry-design-applying-its-goals-frame-and-steps-out-of-their-form \
    **Holds:** the design ferry-times-in-the-guide applying at version 1.0.1, its header and its log of five entries ending in apply written as a design's are, and its goals, frame and steps not: a goal record holding no field, a stray line in its Frame Outcome between its Goals and its Description, and a step holding no Objectives \
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
      **Validated:** 2026-01-01T00:00:00Z sha256:0123456789abcdef

      ## The Problem

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs.

      ## Design Goals

      **Records:**
        - the guide says when the ferry runs

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

          and the winter timetable, perhaps

          **Description:** A visitor plans a crossing from the guide alone. It is judged by reading the section naming the ferry.

      ## Design Plan Steps

      **Records:**
        - **Name:** ferry-times-stated \
          **What:** `docs/guide.md § The Ferry` \
          **Why:** The section names the ferry and gives no time. \
          **Depends On Steps:** none

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
