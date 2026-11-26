**Records:**
  - **Fixture:** specs-index-of-the-methodology \
    **Holds:** an index of a bakery's specifications, a title and a table of one row naming a folder `methodology/` \
    **Snippet:**

      ```markdown
      # The Bakery's Specifications

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `methodology/` | How the bakery writes its specifications |
      ```

  - **Fixture:** methodology-index-of-crusts-and-sourcing \
    **Holds:** an index of a bakery's methodology, a title and a table of two rows naming a file `crusts.md` and a folder `sourcing-and-citation/` \
    **Snippet:**

      ```markdown
      # The Bakery's Methodology

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `crusts.md` | How a crust is written down |
      | `sourcing-and-citation/` | Where a rule comes from |
      ```

  - **Fixture:** sourcing-index-of-external-reference \
    **Holds:** an index titled Sourcing and Citation, a table of one row naming a file `external-reference.md` \
    **Snippet:**

      ```markdown
      # Sourcing and Citation

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `external-reference.md` | How a standard from outside is named |
      ```

  - **Fixture:** departure-reasons-row-in-order \
    **Holds:** a file on naming a standard from outside, its section A Mapping onto a Standard holding a table of fields whose Departs For row names, in backticks and in this order, `the standard's gap`, `the canon's form` and `no need yet` \
    **Snippet:**

      ```markdown
      # External Reference

      ## External Reference

      ### A Mapping onto a Standard

      | Field | Holds |
      |---|---|
      | Departs For | the kind of a departure's reason: `the standard's gap`, `the canon's form` or `no need yet` |
      ```

  - **Fixture:** departure-reasons-row-of-two-kinds \
    **Holds:** a file on naming a standard from outside, its section A Mapping onto a Standard holding a table of fields whose Departs For row names, in backticks and in this order, `the standard's gap` and `no need yet` \
    **Snippet:**

      ```markdown
      # External Reference

      ## External Reference

      ### A Mapping onto a Standard

      | Field | Holds |
      |---|---|
      | Departs For | the kind of a departure's reason: `the standard's gap` or `no need yet` |
      ```

  - **Fixture:** register-of-one-standard \
    **Holds:** a register of the standards a bakery's methodology names, a title and one record whose Name is BreadML \
    **Snippet:**

      ```markdown
      # External References

      **Records:**
        - **Name:** BreadML \
          **Holds:** a markup for writing down recipes
      ```

  - **Fixture:** crusts-departing-citing-the-row \
    **Holds:** a methodology file on crusts whose one section holds a sentence saying a crust's colour departs from BreadML and citing the row colour of a table BreadML Elements, then a sentence ending at a colon saying where a crust's fields differ from BreadML, then a table named BreadML Elements of one row \
    **Snippet:**

      ```markdown
      # Crusts

      ## Crust

      A crust's colour departs from BreadML (`§ Crust [BreadML Elements.BreadML: colour]`).

      Where a crust's fields differ from BreadML:

      **Table Name:** BreadML Elements \
      **Reference Key:** BreadML

      | BreadML | Treatment |
      |---|---|
      | colour | named by the baker |
      ```

  - **Fixture:** crusts-departing-citing-no-row \
    **Holds:** a methodology file on crusts whose one section holds, on line 5, a sentence saying a crust's colour departs from BreadML, citing nothing \
    **Snippet:**

      ```markdown
      # Crusts

      ## Crust

      A crust's colour departs from BreadML, as the ovens need.
      ```
