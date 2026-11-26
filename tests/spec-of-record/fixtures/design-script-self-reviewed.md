**Records:**
  - **Fixture:** self-review-holding-no-check-of-linked-work \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and two Builder Checks, of steers against the user's messages and of the problem's re-evaluation, none of linked work \
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

        - **Check:** problem-read-against-the-guide \
          **Kind:** problem re-evaluation \
          **Places Checked:**
            - `docs/guide.md § The Ferry`

          **Result:** The section still names the ferry and gives no time.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** self-review-holding-no-check-of-steers \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and two Builder Checks, of linked work and of the problem's re-evaluation, none of steers against the user's messages \
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

  - **Fixture:** self-review-holding-no-re-evaluation \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and two Builder Checks, of steers against the user's messages and of linked work, none of the problem's re-evaluation \
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

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** self-review-re-evaluating-the-ferry-and-the-lighthouse \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and three Builder Checks, of steers against the user's messages, of linked work and of the problem's re-evaluation, its re-evaluation checking the guide's sections The Ferry and The Lighthouse \
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
            - `docs/guide.md § The Lighthouse`

          **Result:** The section still names the ferry and gives no time.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** ferry-design-drafted-its-problem-citing-the-lighthouse \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of three entries, its Problem citing the guide's section The Lighthouse beside The Ferry \
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

      The guide tells a visitor how to reach the island, and `docs/guide.md § The Ferry` names the ferry without saying when it runs, though `docs/guide.md § The Lighthouse` gives the keeper's hours.

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

  - **Fixture:** ferry-design-drafted-self-reviewed \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, a log of four entries: entered, goals-agreed, plan-change and self-review-1 \
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

        - **Entry:** self-review-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** second-self-review-holding-no-re-evaluation \
    **Holds:** the second self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and two Builder Checks, of steers against the user's messages and of linked work, none of the problem's re-evaluation \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-2

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

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** ferry-design-reassessed-after-a-self-review \
    **Holds:** the design ferry-times-in-the-guide in progress at version 2.0.1, a log of seven entries: entered, goals-agreed, plan-change, self-review-1, a design-reassessment for a changed foundation, goals-agreed and plan-change \
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

  - **Fixture:** second-self-review-at-the-next-major-version-holding-no-re-evaluation \
    **Holds:** the second self-review's report on the design ferry-times-in-the-guide, read at version 2.0.1: its Reads the design and the guide, and two Builder Checks, of steers against the user's messages and of linked work, none of the problem's re-evaluation \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-2

      ## Reading

      **Design Version:** 2.0.1 \
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

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** self-review-tracing-the-hours \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, a Traces part tracing the mechanism at the guide's section The Ferry, its Outcome that the goals and the frame name the mechanism, and three Builder Checks, of steers against the user's messages, of linked work and of the problem's re-evaluation \
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

      ## Traces

      **Records:**
        - **Trace:** hours-by-season \
          **Mechanism:** `docs/guide.md § The Ferry` \
          **Outcome:** name the mechanism

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

  - **Fixture:** self-review-tracing-the-hours-with-no-outcome \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, a Traces part tracing the mechanism at the guide's section The Ferry and holding no Outcome, and three Builder Checks, of steers against the user's messages, of linked work and of the problem's re-evaluation \
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

      ## Traces

      **Records:**
        - **Trace:** hours-by-season \
          **Mechanism:** `docs/guide.md § The Ferry`

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

  - **Fixture:** self-review-working-the-rounds-case \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and four Builder Checks: of steers against the user's messages, of linked work and of the problem's re-evaluation, and a worked case of the first adversarial review's Cause times-by-season and its Finding \
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

        - **Check:** round-worked \
          **Kind:** worked case \
          **Places Checked:**
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Findings [Finding: reviewer-1-last-crossing-in-winter]`

          **Result:** It holds.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** self-review-working-the-rounds-case-reading-no-guide \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design alone, and four Builder Checks: of steers against the user's messages, of linked work and of the problem's re-evaluation, and a worked case of the first adversarial review's Cause times-by-season and its Finding \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** self-review-1

      ## Reading

      **Design Version:** 1.0.1 \
      **Reads:**
        - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

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

        - **Check:** round-worked \
          **Kind:** worked case \
          **Places Checked:**
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Findings [Finding: reviewer-1-last-crossing-in-winter]`

          **Result:** It holds.

      ## Settlement

      **Earlier Reports:**
        - none
      ```

  - **Fixture:** self-review-working-the-rounds-cause-alone \
    **Holds:** a self-review's report on the design ferry-times-in-the-guide, read at version 1.0.1: its Reads the design and the guide, and four Builder Checks: of steers against the user's messages, of linked work and of the problem's re-evaluation, and a worked case of the first adversarial review's Cause times-by-season alone \
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

        - **Check:** round-worked \
          **Kind:** worked case \
          **Places Checked:**
            - `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Causes [Cause: times-by-season]`

          **Result:** It holds.

      ## Settlement

      **Earlier Reports:**
        - none
      ```
