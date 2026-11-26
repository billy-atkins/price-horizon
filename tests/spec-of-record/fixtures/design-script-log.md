**Records:**
  - **Fixture:** ferry-diagnosis-holding-no-scope \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, and no Scope part \
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
      ```

  - **Fixture:** ferry-diagnosis-its-scope-holding-no-answer \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, and a Scope holding its Question alone \
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

      **Question:** Is the scope too narrow or too wide?
      ```

  - **Fixture:** ferry-diagnosis-naming-the-fourth-reassessment \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide whose Design Reassessment is design-reassessment-4, one Flaw citing a finding of an adversarial review's report, one Root Cause the Flaw names, and a Scope holding a question and its answer \
    **Snippet:**

      ```markdown
      # Diagnosis

      **Design:** ferry-times-in-the-guide \
      **Design Reassessment:** design-reassessment-4 \
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

  - **Fixture:** ferry-diagnosis-its-flaw-naming-another-root-cause \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, one-season-assumed, the Flaw naming the Root Cause another-cause, and a Scope holding a question and its answer \
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
          **Root Cause:** another-cause

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

  - **Fixture:** ferry-diagnosis-its-flaw-perhaps-still-applying \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, the Flaw's Still Applies perhaps, and a Scope holding a question and its answer \
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
          **Still Applies:** perhaps \
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

  - **Fixture:** ferry-diagnosis-its-flaw-no-longer-applying \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, the Flaw's Still Applies no and no Why Not, and a Scope holding a question and its answer \
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
          **Still Applies:** no \
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

  - **Fixture:** ferry-diagnosis-its-root-cause-holding-no-account \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment, one Flaw citing a finding of an adversarial review's report and one Root Cause, the Root Cause holding its Question and Description and no Account, and a Scope holding a question and its answer \
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
          **Description:** The design took the ferry to keep one set of hours all year.

      ## Scope

      **Question:** Is the scope too narrow or too wide? \
      **Answer:** Too narrow: it left the seasons out.
      ```

  - **Fixture:** ferry-diagnosis-of-the-second-reassessment \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide whose Design Reassessment is design-reassessment-2, one Flaw citing a finding of an adversarial review's report, one Root Cause the Flaw names, and a Scope holding a question and its answer \
    **Snippet:**

      ```markdown
      # Diagnosis

      **Design:** ferry-times-in-the-guide \
      **Design Reassessment:** design-reassessment-2 \
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

  - **Fixture:** ferry-diagnosis-its-flaw-citing-another-finding \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment: one Flaw citing the finding reviewer-1-another-finding of its first adversarial review's report, one Root Cause the Flaw names, and a Scope holding a question and its answer \
    **Snippet:**

      ```markdown
      # Diagnosis

      **Design:** ferry-times-in-the-guide \
      **Design Reassessment:** design-reassessment-1 \
      **Flaw Set:** none \
      **Earlier Diagnoses:** none

      ## Flaws

      **Records:**
        - **Flaw:** `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/1.md § Findings [Finding: reviewer-1-another-finding]` \
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

  - **Fixture:** ferry-design-drafted-its-review-logged \
    **Holds:** the design ferry-times-in-the-guide in progress at version 1.0.1, naming no other design, and a log of four entries: entered, goals-agreed, plan-change and an adversarial-review at version 1.0.1 \
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 1.0.1 \
          **Model:** a model \
          **Effort:** medium \
          **Design Flaws:** 0 \
          **Implementation Flaws:** 0 \
          **Nits:** 0 \
          **Dropped:** 0 \
          **Led To:** validating

      ## Out of Scope

      Nothing the research found is left out.
      ```

  - **Fixture:** log-of-a-reassessment-at-the-step-back \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment whose Cause is a step back for a run of flaws, holding its Decision and its Diagnosis, and a goals-agreed \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Cause:** step back: a run of flaws \
          **Decision:** split \
          **Diagnosis:** `.ai/tmp/design-specs/ferry-times-in-the-guide/diagnosis/1.md`

        - **Entry:** goals-agreed-2 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 2.0.0
      ```

  - **Fixture:** log-of-a-reassessment-for-a-changed-foundation \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment whose Cause is a changed foundation naming quay-rebuilt finished and pier-closed gone, holding neither a Decision nor a Diagnosis, and a goals-agreed \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Cause:** changed foundation: quay-rebuilt finished; pier-closed gone

        - **Entry:** goals-agreed-2 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 2.0.0
      ```

  - **Fixture:** log-of-a-reassessment-holding-no-cause \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment holding no Cause, its Decision and its Diagnosis alone, and a goals-agreed \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Decision:** rescope \
          **Diagnosis:** `.ai/tmp/design-specs/ferry-times-in-the-guide/diagnosis/1.md`

        - **Entry:** goals-agreed-2 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 2.0.0
      ```

  - **Fixture:** log-of-a-reassessment-entry-of-an-old-log \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a reassessment entry holding a Decision and a Running Work, a goals-agreed, and an entered entry whose Reason is sent back for a dependency \
    **Snippet:**

      ```markdown
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

        - **Entry:** reassessment-1 \
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Decision:** rescope \
          **Running Work:** none

        - **Entry:** goals-agreed-2 \
          **Timestamp:** 2026-01-01T00:00:04Z \
          **Design Version:** 2.0.0

        - **Entry:** entered-2 \
          **Timestamp:** 2026-01-01T00:00:05Z \
          **Design Version:** 2.0.0 \
          **Reason:** sent back for a dependency
      ```

  - **Fixture:** log-of-a-changed-foundation-holding-a-decision \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment whose Cause is a changed foundation naming quay-rebuilt finished and pier-closed gone, holding a Decision \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Cause:** changed foundation: quay-rebuilt finished; pier-closed gone \
          **Decision:** rescope
      ```

  - **Fixture:** log-of-a-step-back-holding-no-diagnosis \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment whose Cause is a step back for a run of flaws, holding its Decision and no Diagnosis \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Cause:** step back: a run of flaws \
          **Decision:** split
      ```

  - **Fixture:** log-of-a-reassessment-of-a-cause-in-neither-form \
    **Holds:** the Records of a design's Design Log Entries section, holding the entries entered, goals-agreed and plan-change, then a design-reassessment whose Cause is it seemed time, holding a Decision and a Diagnosis \
    **Snippet:**

      ```markdown
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
          **Timestamp:** 2026-01-01T00:00:03Z \
          **Design Version:** 2.0.0 \
          **Cause:** it seemed time \
          **Decision:** split \
          **Diagnosis:** `.ai/tmp/design-specs/ferry-times-in-the-guide/diagnosis/1.md`
      ```
