**Records:**
  - **Fixture:** review-handed-back \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** goals-all-met \
    **Holds:** an adversarial review of the ferry design where both questions are met for the design’s one goal and there are no findings \
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
      ```

  - **Fixture:** goals-upheld-failure \
    **Holds:** an adversarial review of the ferry design where one answer names a design flaw upheld on the goal \
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
          **Outcome Only:** reviewer-1-last-crossing-in-winter \
          **Genuine Change:** met

      ## Findings

      **Records:**
        - **Finding:** reviewer-1-last-crossing-in-winter \
          **Verdict:** design flaw \
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
      ```

  - **Fixture:** goals-historical-account \
    **Holds:** an adversarial review of the ferry design where the reviewer names an earlier goal through its own account and upholds a flaw on it \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** reviewer's account only

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
          **Outcome Only:** reviewer-1-last-crossing-in-winter \
          **Genuine Change:** met

      ## Findings

      **Records:**
        - **Finding:** reviewer-1-last-crossing-in-winter \
          **Verdict:** design flaw \
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
      ```

  - **Fixture:** goals-structure \
    **Holds:** an adversarial review of the ferry design where the reviewer stopped at the structure \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Stopped At:** the structure

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
      ```

  - **Fixture:** goals-missing \
    **Holds:** an adversarial review of the ferry design where the goal judgments are absent \
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
      ```

  - **Fixture:** goals-repeated \
    **Holds:** an adversarial review of the ferry design where the same goal is judged twice \
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

        - **Goal:** guide-says-when-the-ferry-runs \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** met \
          **Genuine Change:** met
      ```

  - **Fixture:** goals-stale \
    **Holds:** an adversarial review of the ferry design where the wording differs from the reviewed goal \
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
          **Wording:** The guide names the quay. \
          **Outcome Only:** met \
          **Genuine Change:** met
      ```

  - **Fixture:** goals-misattributed \
    **Holds:** an adversarial review of the ferry design where the judgment names a different goal \
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
        - **Goal:** guide-names-the-quay \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** met \
          **Genuine Change:** met
      ```

  - **Fixture:** goals-unsubstantiated \
    **Holds:** an adversarial review of the ferry design where the second answer names no finding \
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
          **Genuine Change:** reviewer-1-no-change
      ```

  - **Fixture:** goals-dropped \
    **Holds:** an adversarial review of the ferry design where the answer names a finding the reviewer dropped \
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
          **Outcome Only:** reviewer-1-last-crossing-in-winter \
          **Genuine Change:** met

      ## Findings

      **Records:**
        - **Finding:** reviewer-1-last-crossing-in-winter \
          **Verdict:** dropped \
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
      ```

  - **Fixture:** goals-different-goal \
    **Holds:** an adversarial review of the ferry design where the finding supports a different goal \
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
          **Outcome Only:** reviewer-1-last-crossing-in-winter \
          **Genuine Change:** met

      ## Findings

      **Records:**
        - **Finding:** reviewer-1-last-crossing-in-winter \
          **Verdict:** design flaw \
          **Decision:** the times the section gives \
          **Affected Goals:**
            - another-ferry-goal

          **Description:** The step's Objective gives one first and one last crossing, and the ferry keeps other hours in winter. \
          **Evidence:**
            - **Description:** The section names one quay and no season. \
              **Places:**
                - `docs/guide.md § The Ferry`

          **Rationale:** A visitor in winter plans a crossing the ferry does not make. \
          **Possible Fix:**
            - **Kind:** revision \
              **Delivers:** An Objective giving the first and the last crossing of each season.
      ```

  - **Fixture:** goals-structure-with-answers \
    **Holds:** an adversarial review of the ferry design where a stopped review nevertheless gives goal judgments \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Stopped At:** the structure

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
      ```


  - **Fixture:** goals-unexplained-stop \
    **Holds:** an adversarial review claiming a structural stop with no finding \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Stopped At:** the structure

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
      ```

  - **Fixture:** goals-before-agreement \
    **Holds:** an adversarial review naming a version from before the agreement of any goals \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** reviewer's account only

      ## Reading

      **Design Version:** 0.1.0 \
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
        - **Goal:** earlier-ferry-goal \
          **Wording:** The guide says when the ferry runs. \
          **Outcome Only:** reviewer-1-last-crossing-in-winter \
          **Genuine Change:** met

      ## Findings

      **Records:**
        - **Finding:** reviewer-1-last-crossing-in-winter \
          **Verdict:** design flaw \
          **Decision:** the times the section gives \
          **Affected Goals:**
            - earlier-ferry-goal

          **Description:** The step's Objective gives one first and one last crossing, and the ferry keeps other hours in winter. \
          **Evidence:**
            - **Description:** The section names one quay and no season. \
              **Places:**
                - `docs/guide.md § The Ferry`

          **Rationale:** A visitor in winter plans a crossing the ferry does not make. \
          **Possible Fix:**
            - **Kind:** revision \
              **Delivers:** An Objective giving the first and the last crossing of each season.
      ```

  - **Fixture:** goals-future \
    **Holds:** an adversarial review of the ferry design where the review names a later version \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** compared with reviewed goals

      ## Reading

      **Design Version:** 1.0.9 \
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
      ```

  - **Fixture:** research-handed-back \
    **Holds:** a handed-off judgment's report of research for the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.0: its Reads the guide's section The Ferry, one Search by meaning naming the design's goal and one Read Assessment of that section, and no part the builder writes \
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
      ```

  - **Fixture:** review-handed-back-making-no-search \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal, no Searches part, and no part the builder writes \
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
      ```

  - **Fixture:** review-handed-back-titled-for-another-entry \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its title's Entry adversarial-review-7 \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-7 \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-titled-for-another-design \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its title's Design another-design \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** another-design \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-holding-no-reading \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; it holds no Reading part \
    **Snippet:**

      ```markdown
      # Check's Report

      **Design:** ferry-times-in-the-guide \
      **Entry:** adversarial-review-1 \
      **Goal Comparison:** compared with reviewed goals

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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-its-parts-out-of-order \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its Searches part standing before its Findings part \
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
      ```

  - **Fixture:** review-handed-back-holding-a-part-of-no-form \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; and a last part Afterthoughts \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`

      ## Afterthoughts

      None.
      ```

  - **Fixture:** review-handed-back-its-marked-finding-holding-no-decision \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its Finding holding no Decision \
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
      ```

  - **Fixture:** review-handed-back-its-verdict-out-of-its-values \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding whose Verdict is a worry naming the design's goal and one Search by meaning, and no part the builder writes \
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
          **Verdict:** a worry \
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
      ```

  - **Fixture:** review-handed-back-holding-the-builders-part \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, followed by the builder's Causes and Settlement \
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

  - **Fixture:** review-handed-back-its-finding-naming-a-goal-not-held \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the goal guide-says-what-the-ferry-costs and one Search by meaning, and no part the builder writes \
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
            - guide-says-what-the-ferry-costs

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
      ```

  - **Fixture:** review-handed-back-its-marked-finding-naming-nothing \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw holding no Affected Goals and citing no rule and one Search by meaning, and no part the builder writes \
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
      ```

  - **Fixture:** review-handed-back-its-reads-holding-no-citation \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its reviewer's Collecting Reads holding the words the guide in place of a citation of the guide \
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
            - the guide

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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-landing-on-a-change-not-cited \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its Finding's Lands On naming times-by-season, a change no report it cites holds \
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

          **Lands On:** times-by-season

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
      ```

  - **Fixture:** review-handed-back-citing-a-report-no-entry-names \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its Evidence citing a Finding of the design's ninth adversarial review's report \
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
            - **Description:** The section names one quay and no season, as `.ai/tmp/design-specs/ferry-times-in-the-guide/reports/adversarial-review/9.md § Findings [Finding: reviewer-1-another]` found. \
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
      ```

  - **Fixture:** review-handed-back-its-ranking-part-none \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning whose Ranking Part is none and whose Places hold one place, and no part the builder writes \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** none \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-its-snapshot-no-code \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning whose Snapshot is yesterday, and no part the builder writes \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** yesterday \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** review-handed-back-a-field-line-unbroken \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; its Finding's Verdict line ending with no backslash before the field after it \
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
          **Verdict:** implementation flaw
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
      ```

  - **Fixture:** review-handed-back-no-blank-line-after-a-list \
    **Holds:** an adversarial review's report on the design ferry-times-in-the-guide as its cold agent hands it back, read at version 1.0.1, its Reading, one Finding marked an implementation flaw naming the design's goal and one Search by meaning, and no part the builder writes; no blank line after its Finding's Affected Goals list, before its Description \
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

          **Kind:** meaning \
          **Query:** In winter the ferry makes fewer crossings than in summer. \
          **Ranking Part:** 1 to 20 \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```
