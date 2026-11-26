**Records:**
  - **Fixture:** mermaid-flowchart-after-its-configuration \
    **Holds:** a Markdown file on a harbor holding a mermaid block that opens with a block of configuration and then declares a flowchart of two nodes \
    **Snippet:**

      ````markdown
      # The Harbor

      ```mermaid
      ---
      config:
        layout: elk
      ---
      flowchart TD
        Quay --> Pontoon
      ```
      ````

  - **Fixture:** mermaid-sequence-diagram \
    **Holds:** a Markdown file on a harbor holding a mermaid block that declares a sequence diagram of one message between two participants \
    **Snippet:**

      ````markdown
      # The Harbor

      ```mermaid
      sequenceDiagram
        Skipper->>Harbormaster: asks for a berth
      ```
      ````
