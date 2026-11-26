**Records:**
  - **Fixture:** harbor-office-environments \
    **Holds:** an environments document titled Environments of two sections, Laptop, opening with a Kind field of local and holding a table of tools headed Tool, Version, Purpose and Install and a table of tasks headed Task, Command and Does, and Harbor Office, opening with a Kind field of production \
    **Snippet:**

      ```markdown
      # Environments

      ## Laptop

      **Kind:** local

      The harbor master's own laptop.

      | Tool | Version | Purpose | Install |
      |---|---|---|---|
      | tide-reader | 2.1 | reads the tide tables | `pip install tide-reader` |

      | Task | Command | Does |
      |---|---|---|
      | Tides | `tide-reader today` | prints the day's tides |

      ## Harbor Office

      **Kind:** production

      The office's server, which each boat's booking reaches.
      ```

  - **Fixture:** harbor-office-environments-none-local \
    **Holds:** an environments document titled Environments of two sections, Test Bench, opening with a Kind field of shared, and Harbor Office, opening with a Kind field of production \
    **Snippet:**

      ```markdown
      # Environments

      ## Test Bench

      **Kind:** shared

      A server the harbor's staff try bookings on.

      ## Harbor Office

      **Kind:** production

      The office's server, which each boat's booking reaches.
      ```

  - **Fixture:** harbor-office-environment-without-a-kind \
    **Holds:** an environments document titled Environments of two sections, Laptop, opening with a Kind field of local, and Harbor Office, opening with a sentence and holding no Kind field \
    **Snippet:**

      ```markdown
      # Environments

      ## Laptop

      **Kind:** local

      The harbor master's own laptop.

      ## Harbor Office

      The office's server, which each boat's booking reaches.
      ```

  - **Fixture:** harbor-office-tools-out-of-order \
    **Holds:** an environments document titled Environments of two sections, Laptop, opening with a Kind field of local and holding a table of tools headed Tool, Purpose, Version and Install, and Harbor Office, opening with a Kind field of production \
    **Snippet:**

      ```markdown
      # Environments

      ## Laptop

      **Kind:** local

      The harbor master's own laptop.

      | Tool | Purpose | Version | Install |
      |---|---|---|---|
      | tide-reader | reads the tide tables | 2.1 | `pip install tide-reader` |

      ## Harbor Office

      **Kind:** production

      The office's server, which each boat's booking reaches.
      ```

  - **Fixture:** harbor-office-tasks-out-of-order \
    **Holds:** an environments document titled Environments of two sections, Laptop, opening with a Kind field of local and holding a table of tasks headed Task, Does and Command, and Harbor Office, opening with a Kind field of production \
    **Snippet:**

      ```markdown
      # Environments

      ## Laptop

      **Kind:** local

      The harbor master's own laptop.

      | Task | Does | Command |
      |---|---|---|
      | Tides | prints the day's tides | `tide-reader today` |

      ## Harbor Office

      **Kind:** production

      The office's server, which each boat's booking reaches.
      ```
