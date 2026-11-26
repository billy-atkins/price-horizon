**Records:**
  - **Fixture:** loaves-spec-of-a-script-check \
    **Holds:** a spec on loaves of two sections, Proving and Shaping, Proving holding a subsection Script Checks of one Script Check record, loaf-proved-an-hour, whose Carried Out By names the skill `bake-bread` and its flag `--check-proving` \
    **Snippet:**

      ```markdown
      # Loaves

      ## Proving

      A loaf proves for an hour.

      ### Script Checks

      **Records:**
        - **Name:** loaf-proved-an-hour \
          **Tests:** every loaf's proving lasts an hour, as the Proving rule has it \
          **Reads:**
            - `canon-specs`

          **Carried Out By:**
            - `.ai/skills/bake-bread/` `--check-proving`

      ## Shaping

      A loaf is shaped by hand.
      ```

  - **Fixture:** bread-script-annotated-in-form \
    **Holds:** a Python function for baking bread under three canon-spec annotations on consecutive lines, in plain character order, citing the section Proving of `specs/methodology/loaves.md`, the Script Check record loaf-proved-an-hour of its subsection Script Checks, and its section Shaping \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/loaves.md § Proving
      # @canon-spec specs/methodology/loaves.md § Proving § Script Checks [Name: loaf-proved-an-hour]
      # @canon-spec specs/methodology/loaves.md § Shaping
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-annotation-after-code \
    **Holds:** a line of Python counting loaves whose comment after its code is a canon-spec annotation citing the section Proving of `specs/methodology/loaves.md` \
    **Snippet:**

      ```python
      LOAVES = 12  # @canon-spec specs/methodology/loaves.md § Proving
      ```

  - **Fixture:** bread-script-citing-an-application-spec \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing the section Proving of `specs/bakery/loaves.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/bakery/loaves.md § Proving
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-citing-an-index \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing the section Loaves of `specs/methodology/index.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/index.md § Loaves
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-citing-cakes \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing the section Icing of `specs/methodology/cakes.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/cakes.md § Icing
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-citing-baking \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing the section Baking of `specs/methodology/loaves.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/loaves.md § Baking
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-citing-a-part-of-shaping \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing the part named by-hand of the section Shaping of `specs/methodology/loaves.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/loaves.md § Shaping [Name: by-hand]
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-citing-a-loaf-shaped-check \
    **Holds:** a Python function for baking bread under one canon-spec annotation citing a Script Check record named loaf-shaped in the subsection Script Checks of the section Proving of `specs/methodology/loaves.md` \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/loaves.md § Proving § Script Checks [Name: loaf-shaped]
      def bake(loaf):
          return loaf
      ```

  - **Fixture:** bread-script-annotations-shaping-first \
    **Holds:** a Python function for baking bread under two canon-spec annotations on consecutive lines, the first citing the section Shaping of `specs/methodology/loaves.md` and the second its section Proving \
    **Snippet:**

      ```python
      # @canon-spec specs/methodology/loaves.md § Shaping
      # @canon-spec specs/methodology/loaves.md § Proving
      def bake(loaf):
          return loaf
      ```
