**Records:**
  - **Fixture:** island-guide \
    **Holds:** a guide to an island: a line saying a visitor arrives by water, a section The Ferry naming the north quay the ferry leaves from, and a section The Lighthouse naming its keeper \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.
      ```

  - **Fixture:** ferry-diagnosis \
    **Holds:** a diagnosis of the design ferry-times-in-the-guide for its first design reassessment: one Flaw citing a finding of an adversarial review's report, one Root Cause the Flaw names, and a Scope holding a question and its answer \
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

      **Question:** Is the scope too narrow or too wide? \
      **Answer:** Too narrow: it left the seasons out.
      ```
