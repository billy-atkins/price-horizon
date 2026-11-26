**Records:**
  - **Fixture:** index-of-a-ferry-guide \
    **Holds:** an index of the specifications titled The Ferry Guide, a table of one row naming a file `crossing.md` \
    **Snippet:**

      ```markdown
      # The Ferry Guide

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `crossing.md` | How the ferry crosses to the island |
      ```

  - **Fixture:** crossing-drawn-from-its-sections \
    **Holds:** a Markdown file on a ferry's crossing of three sections: Loading and Sailing, each a sentence citing the section Crossing Diagram of `specs/crossing.md`, and Crossing Diagram, holding a mermaid flowchart, its Caption, and its Sources listing those two sections in plain character order \
    **Snippet:**

      ````markdown
      # The Crossing

      ## Loading

      Cars board before foot passengers, as `specs/crossing.md § Crossing Diagram` shows.

      ## Sailing

      The ferry leaves the quay on the hour, as `specs/crossing.md § Crossing Diagram` shows.

      ## Crossing Diagram

      ```mermaid
      flowchart LR
        Quay --> Island
      ```

      **Caption:** A ferry loading at the quay and sailing to the island. \
      **Sources:**
        - `specs/crossing.md § Loading`
        - `specs/crossing.md § Sailing`
      ````

  - **Fixture:** crossing-drawn-without-a-caption \
    **Holds:** a Markdown file on a ferry's crossing of two sections: Sailing, a sentence citing the section Crossing Diagram of `specs/crossing.md`, and Crossing Diagram, holding a mermaid flowchart followed by a Sources field and no Caption \
    **Snippet:**

      ````markdown
      # The Crossing

      ## Sailing

      The ferry leaves the quay on the hour, as `specs/crossing.md § Crossing Diagram` shows.

      ## Crossing Diagram

      ```mermaid
      flowchart LR
        Quay --> Island
      ```

      **Sources:**
        - `specs/crossing.md § Sailing`
      ````

  - **Fixture:** crossing-drawn-from-a-silent-section \
    **Holds:** a Markdown file on a ferry's crossing of two sections: Sailing, a sentence citing nothing, and Crossing Diagram, holding a mermaid flowchart, its Caption, and its Sources listing the section Sailing \
    **Snippet:**

      ````markdown
      # The Crossing

      ## Sailing

      The ferry leaves the quay on the hour.

      ## Crossing Diagram

      ```mermaid
      flowchart LR
        Quay --> Island
      ```

      **Caption:** A ferry sailing from the quay to the island. \
      **Sources:**
        - `specs/crossing.md § Sailing`
      ````

  - **Fixture:** crossing-drawn-from-sections-out-of-order \
    **Holds:** a Markdown file on a ferry's crossing of three sections: Loading and Sailing, each a sentence citing the section Crossing Diagram of `specs/crossing.md`, and Crossing Diagram, holding a mermaid flowchart, its Caption, and its Sources listing Sailing before Loading \
    **Snippet:**

      ````markdown
      # The Crossing

      ## Loading

      Cars board before foot passengers, as `specs/crossing.md § Crossing Diagram` shows.

      ## Sailing

      The ferry leaves the quay on the hour, as `specs/crossing.md § Crossing Diagram` shows.

      ## Crossing Diagram

      ```mermaid
      flowchart LR
        Quay --> Island
      ```

      **Caption:** A ferry loading at the quay and sailing to the island. \
      **Sources:**
        - `specs/crossing.md § Sailing`
        - `specs/crossing.md § Loading`
      ````

  - **Fixture:** crossing-drawn-after-a-sentence \
    **Holds:** a Markdown file on a ferry's crossing of two sections: Sailing, a sentence citing the section Crossing Diagram of `specs/crossing.md`, and Crossing Diagram, holding a sentence, then a mermaid flowchart, its Caption, and its Sources listing the section Sailing \
    **Snippet:**

      ````markdown
      # The Crossing

      ## Sailing

      The ferry leaves the quay on the hour, as `specs/crossing.md § Crossing Diagram` shows.

      ## Crossing Diagram

      The ferry crosses in twenty minutes.

      ```mermaid
      flowchart LR
        Quay --> Island
      ```

      **Caption:** A ferry sailing from the quay to the island. \
      **Sources:**
        - `specs/crossing.md § Sailing`
      ````
