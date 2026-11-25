**Records:**
  - **Fixture:** hours-decision-table \
    **Holds:** a Decision Table of the ferry's hours by season, its Hit Policy First and its one condition Season, in two rows \
    **Snippet:**

      ```markdown
      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** First \
      **Conditions:** Season

      | Season | The ferry |
      |---|---|
      | "winter" | runs twice a day |
      | - | runs each hour |
      ```

  - **Fixture:** steering-decisions-of-one-steer \
    **Holds:** the Steering Decisions section of a design, holding one steer, winter-hours-count, a directive changing nothing \
    **Snippet:**

      ```markdown
      ## Steering Decisions

      **Records:**
        - **Name:** winter-hours-count \
          **Prompted By:** the first share's assessment \
          **Type:** directive \
          **Steer:** "Give the winter hours too." \
          **Decision:** The guide gives each season's hours. \
          **Changes:**
            - none
      ```

  - **Fixture:** retired-phrases-of-one-phrase \
    **Holds:** the Retired Phrases section of a design, retiring the phrase north quay for north pier, staying right nowhere \
    **Snippet:**

      ```markdown
      ## Retired Phrases

      **Records:**
        - **Phrase:** north quay \
          **Replacement:** north pier \
          **Stays Right:** none
      ```

  - **Fixture:** traces-of-one-mechanism \
    **Holds:** the Traces part of a self-review's report, holding one Trace, hours-by-season, of the mechanism at the guide's section The Ferry, its Outcome that the goals and the frame name the mechanism \
    **Snippet:**

      ```markdown
      ## Traces

      **Records:**
        - **Trace:** hours-by-season \
          **Mechanism:** `docs/guide.md § The Ferry` \
          **Outcome:** name the mechanism
      ```

  - **Fixture:** reliances-on-one-design \
    **Holds:** a Reliances field as a design's Scope held one under earlier rules, holding one Reliance, on the design quay-rebuilt at version 1.0.0 \
    **Snippet:**

      ```markdown
      **Reliances:**
        - **Design:** quay-rebuilt \
          **Version:** 1.0.0 \
          **Relies On:** The quay stands where the ferry leaves.
      ```

  - **Fixture:** search-by-meaning-for-one-season \
    **Holds:** one Search record of a report, each-season-named, a search by meaning naming the goal guide-says-when-the-ferry-runs, its Places the guide's section The Ferry \
    **Snippet:**

      ```markdown
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
      ```

  - **Fixture:** search-by-terms-for-the-quay \
    **Holds:** one Search record of a report, ferry-times-by-terms, a search by terms for north quay naming the goal guide-says-when-the-ferry-runs, naming no target and narrowed to no path, its Places the guide's section The Ferry \
    **Snippet:**

      ```markdown
        - **Search:** ferry-times-by-terms \
          **For:** every use of the quay the ferry leaves from \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** north quay \
          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `docs/guide.md § The Ferry`
      ```

  - **Fixture:** search-by-terms-of-the-design \
    **Holds:** one Search record of a report, first-crossing-named, a search by terms for first crossing over the working files, narrowed to the design document of ferry-times-in-the-guide, its Places the Objective of that design's one step \
    **Snippet:**

      ```markdown
        - **Search:** first-crossing-named \
          **For:** every place of the design naming the first crossing \
          **Goals:**
            - guide-says-when-the-ferry-runs

          **Kind:** terms \
          **Query:** first crossing \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md`

          **Snapshot:** 0123456789abcdef \
          **Places:**
            - `.ai/plans/design-specs/ferry-times-in-the-guide.md § Design Plan Steps [Name: section-gives-the-first-and-last-crossing]`
      ```
