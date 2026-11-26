**Records:**
  - **Fixture:** project-specs-index \
    **Holds:** an index of the specifications titled The Harbor Guide, a table of two rows naming a file `moorings.md` and a folder `methodology/` \
    **Snippet:**

      ```markdown
      # The Harbor Guide

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `moorings.md` | Where a boat may lie |
      | `methodology/` | How the guide is kept |
      ```

  - **Fixture:** project-methodology-index \
    **Holds:** an index titled Keeping the Guide, a table of six rows naming the folders `skills/`, `glossary/`, `scope/`, `working-files/` and `spec-style/` and the file `external-references.md` \
    **Snippet:**

      ```markdown
      # Keeping the Guide

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `skills/` | The skills the guide is kept with |
      | `glossary/` | The guide's terms |
      | `scope/` | What checks each of the guide's rules |
      | `working-files/` | What the guide's keepers write as they work |
      | `spec-style/` | How the guide is written |
      | `external-references.md` | The standards the guide follows |
      ```

  - **Fixture:** project-skills-index \
    **Holds:** an index titled Skills, a table of one row naming a file `registered-skills.md` \
    **Snippet:**

      ```markdown
      # Skills

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `registered-skills.md` | The skills registered to keep the guide |
      ```

  - **Fixture:** project-glossary-index \
    **Holds:** an index titled Glossary, a table of one row naming a file `glossary.md` \
    **Snippet:**

      ```markdown
      # Glossary

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `glossary.md` | The guide's terms and what each means |
      ```

  - **Fixture:** project-registry-of-one-skill \
    **Holds:** a registry titled Registered Skills, a table headed Skill and The Rules It Serves of one row registering the skill `harbor-guide` \
    **Snippet:**

      ```markdown
      ## Registered Skills

      A skill is registered here.

      **Reference Key:** Skill \
      **Required:** The Rules It Serves

      | Skill | The Rules It Serves |
      |---|---|
      | `harbor-guide` | the guide's moorings |
      ```

  - **Fixture:** project-glossary-of-one-term \
    **Holds:** a glossary titled Glossary, one table headed Term, Abbreviation and Definition of one row defining the term mooring with no abbreviation \
    **Snippet:**

      ```markdown
      ## Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | mooring | | A place a boat is made fast to, laid on the harbor's bed. |
      ```

  - **Fixture:** project-skill-file \
    **Holds:** a skill's file opening with front matter naming the skill `harbor-guide` and describing it in one sentence, then a section titled Workflow of one sentence \
    **Snippet:**

      ```markdown
      ---
      name: harbor-guide
      description: Keep the harbor guide's moorings in step with the harbor.
      ---

      # Harbor Guide

      ## Workflow

      Read the moorings, then walk the harbor.
      ```

  - **Fixture:** project-ignore-file \
    **Holds:** an ignore file of one line naming the folder `.harbor/`, which holds the guide's working files \
    **Snippet:**

      ```text
      .harbor/
      ```

  - **Fixture:** project-moorings \
    **Holds:** a Markdown file on a harbor's moorings of a title and one sentence \
    **Snippet:**

      ```markdown
      # Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** project-moorings-numbered \
    **Holds:** a Markdown file on a harbor's moorings of a title and a section whose heading opens with a number and a period \
    **Snippet:**

      ```markdown
      # Moorings

      ## 1. Swinging Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** project-moorings-counting-boats \
    **Holds:** a Markdown file on a harbor's moorings of a title and one sentence counting three boats and pointing at the moorings described above \
    **Snippet:**

      ```markdown
      # Moorings

      Three boats take the moorings described above.
      ```

  - **Fixture:** project-moorings-with-no-blank-line \
    **Holds:** a Markdown file on a harbor's moorings whose title is followed on the next line by its sentence, with no blank line between \
    **Snippet:**

      ```markdown
      # Moorings
      Each boat takes one mooring.
      ```

  - **Fixture:** project-registry-of-three-skills \
    **Holds:** a registry titled Registered Skills, a table headed Skill and The Rules It Serves of three rows registering the skills `harbor-guide`, `audit-specs` and `verify-spec-implementation` \
    **Snippet:**

      ```markdown
      ## Registered Skills

      A skill is registered here.

      **Reference Key:** Skill \
      **Required:** The Rules It Serves

      | Skill | The Rules It Serves |
      |---|---|
      | `harbor-guide` | the guide's moorings |
      | `audit-specs` | each rule the guide's files alone decide |
      | `verify-spec-implementation` | the harbor's code |
      ```

  - **Fixture:** project-scope-index \
    **Holds:** an index titled Scope, a table of one row naming a file `rules-and-skills.md` \
    **Snippet:**

      ```markdown
      # Scope

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `rules-and-skills.md` | What checks each of the guide's rules |
      ```

  - **Fixture:** project-skipped-steps \
    **Holds:** a Markdown file whose section Rules and Skills holds one sentence and a section Skipped Steps of one record, a term left undefined, its Sections citing `specs/methodology/glossary/glossary.md § Glossary` \
    **Snippet:**

      ```markdown
      ## Rules and Skills

      Each rule of the guide is checked by an audit or kept by a skill's step.

      ### Skipped Steps

      **Records:**
        - **Failure:** a term left undefined \
          **Sections:**
            - [`specs/methodology/glossary/glossary.md § Glossary`](/specs/methodology/glossary/glossary.md#glossary)

          **Rule:** [`specs/methodology/glossary/glossary.md § Glossary`](/specs/methodology/glossary/glossary.md#glossary) \
          **Leaves:** a mooring named by a word no reader is given \
          **Caught By:**
            - the harbor master
      ```

  - **Fixture:** project-working-files-index \
    **Holds:** an index titled Working Files, a table of one row naming a file `main.md` \
    **Snippet:**

      ```markdown
      # Working Files

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `main.md` | The files the guide's keepers write as they work |
      ```

  - **Fixture:** project-working-files \
    **Holds:** a Markdown file titled Working Files whose section The Working Files holds a table of two rows naming the folder `.harbor/drafts/` and the file `.harbor/log.md` \
    **Snippet:**

      ```markdown
      # Working Files

      ## The Working Files

      | File | Holds |
      |---|---|
      | `.harbor/drafts/` | moorings being laid out |
      | `.harbor/log.md` | each boat's arrival |
      ```

  - **Fixture:** project-spec-style-index \
    **Holds:** an index titled Spec Style, a table of two rows naming the files `clear-prose.md` and `what-a-finished-spec-reads-like.md` \
    **Snippet:**

      ```markdown
      # Spec Style

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `clear-prose.md` | The words the guide is written without |
      | `what-a-finished-spec-reads-like.md` | The phrases a finished page holds none of |
      ```

  - **Fixture:** project-clear-prose \
    **Holds:** a Markdown file titled Clear Prose whose section Clear Prose holds one sentence, a table named Emphasis Words of one term, truly, and a table named Generic Terms of one term, thing \
    **Snippet:**

      ```markdown
      # Clear Prose

      ## Clear Prose

      The guide names each mooring plainly.

      **Table Name:** Emphasis Words \
      **Reference Key:** Term

      | Term | Instead |
      |---|---|
      | truly | the plain claim |

      **Table Name:** Generic Terms \
      **Reference Key:** Term

      | Term | Instead |
      |---|---|
      | thing | the mooring's name |
      ```

  - **Fixture:** project-finished-style \
    **Holds:** a Markdown file titled What a Finished Spec Reads Like whose section of that name holds one sentence and a table headed Pattern, Example and Instead of one row quoting "used to lie" \
    **Snippet:**

      ```markdown
      # What a Finished Spec Reads Like

      ## What a Finished Spec Reads Like

      A finished page says how the harbor stands.

      **Reference Key:** Pattern

      | Pattern | Example | Instead |
      |---|---|---|
      | A mooring's past | "used to lie" | where the mooring lies |
      ```

  - **Fixture:** project-register \
    **Holds:** a Markdown file whose section External References holds one record, a standard of tide tables the guide adopts \
    **Snippet:**

      ```markdown
      ## External References

      **Records:**
        - **Name:** Tide Tables \
          **Title:** the tide tables of the harbor's port authority \
          **Version:** 2026 \
          **URL:** `https://example.org/tide-tables` \
          **Access:** free \
          **Relation:** adopts \
          **Covers:** the times of each high and low water
      ```

  - **Fixture:** project-audit-skill \
    **Holds:** a skill's file opening with front matter naming the skill `audit-specs`, then a Workflow section of one step citing `specs/methodology/glossary/glossary.md § Glossary`, and a section The audits holding a table headed Audit and Enforces whose rows cite each section of the guide's methodology \
    **Snippet:**

      ```markdown
      ---
      name: audit-specs
      description: Audit the harbor guide against its rules. Use when the guide changes.
      ---

      # Audit the Harbor

      ## Workflow

      **Read the terms.** Walk the moorings knowing each term of `specs/methodology/glossary/glossary.md § Glossary`.

      ## The audits

      | Audit | Enforces |
      |---|---|
      | Registry | `specs/methodology/skills/registered-skills.md § Registered Skills` |
      | Glossary | `specs/methodology/glossary/glossary.md § Glossary` |
      | Rules and skills | `specs/methodology/scope/rules-and-skills.md § Rules and Skills` |
      | Working files | `specs/methodology/working-files/main.md § The Working Files` |
      | Clear prose | `specs/methodology/spec-style/clear-prose.md § Clear Prose` |
      | Finished style | `specs/methodology/spec-style/what-a-finished-spec-reads-like.md § What a Finished Spec Reads Like` |
      | External references | `specs/methodology/external-references.md § External References` |
      ```

  - **Fixture:** project-verify-skill \
    **Holds:** a skill's file opening with front matter naming the skill `verify-spec-implementation`, then a Workflow section of one sentence, and a section The checks holding a table headed Check and Enforces of one row citing `specs/methodology/glossary/glossary.md § Glossary` \
    **Snippet:**

      ```markdown
      ---
      name: verify-spec-implementation
      description: Check the harbor's code against the guide. Use when the code changes.
      ---

      # Verify the Harbor's Code

      ## Workflow

      Read the code, then the guide.

      ## The checks

      | Check | Enforces |
      |---|---|
      | Terms defined | `specs/methodology/glossary/glossary.md § Glossary` |
      ```
