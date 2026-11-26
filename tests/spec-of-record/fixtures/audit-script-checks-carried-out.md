**Records:**
  - **Fixture:** index-of-the-bakery-specs \
    **Holds:** an index of a bakery's specifications, a title and a table of one row naming a file `loaves.md` \
    **Snippet:**

      ```markdown
      # The Bakery's Specifications

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `loaves.md` | How a loaf is made |
      ```

  - **Fixture:** bread-code-carrying-out-the-proving-check \
    **Holds:** a Python function finding the loaves not proved an hour, under one canon-spec annotation citing the Script Check record loaf-proved-an-hour of the subsection Script Checks of the section Proving of `specs/loaves.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/loaves.md § Proving § Script Checks [Name: loaf-proved-an-hour]
      def proving_findings(loaves):
          return [loaf for loaf in loaves if loaf.hours != 1]
      ```
