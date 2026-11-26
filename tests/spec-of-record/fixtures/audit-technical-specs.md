**Records:**
  - **Fixture:** moorings-naming-two-technical-files \
    **Holds:** a Markdown file on a harbor's moorings whose front matter's technical-specs list names `specs/application/technical/berth-ledger.md` and then `specs/application/technical/chain-survey.md` \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/application/technical/berth-ledger.md
        - specs/application/technical/chain-survey.md
      ---
      # Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** moorings-naming-itself \
    **Holds:** a Markdown file on a harbor's moorings whose front matter's technical-specs list names `specs/application/product/moorings.md` \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/application/product/moorings.md
      ---
      # Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** moorings-naming-two-technical-files-backwards \
    **Holds:** a Markdown file on a harbor's moorings whose front matter's technical-specs list names `specs/application/technical/chain-survey.md` and then `specs/application/technical/berth-ledger.md` \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/application/technical/chain-survey.md
        - specs/application/technical/berth-ledger.md
      ---
      # Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** moorings-naming-a-fuel-dock-file \
    **Holds:** a Markdown file on a harbor's moorings whose front matter's technical-specs list names `specs/application/technical/fuel-dock.md` \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/application/technical/fuel-dock.md
      ---
      # Moorings

      Each boat takes one mooring.
      ```

  - **Fixture:** berth-ledger \
    **Holds:** a Markdown file on a harbor's berth ledger of a title and one sentence \
    **Snippet:**

      ```markdown
      # Berth Ledger

      Each berth let is written in the ledger.
      ```

  - **Fixture:** chain-survey \
    **Holds:** a Markdown file on a harbor's chain survey of a title and one sentence \
    **Snippet:**

      ```markdown
      # Chain Survey

      Each mooring chain is surveyed each spring.
      ```

  - **Fixture:** chain-survey-naming-the-berth-ledger \
    **Holds:** a Markdown file on a harbor's chain survey whose front matter's technical-specs list names `specs/application/technical/berth-ledger.md` \
    **Snippet:**

      ```markdown
      ---
      technical-specs:
        - specs/application/technical/berth-ledger.md
      ---
      # Chain Survey

      Each mooring chain is surveyed each spring.
      ```
