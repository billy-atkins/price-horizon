**Records:**
  - **Fixture:** bread-code-naming-the-canon-in-an-annotation-alone \
    **Holds:** a Python file for proving bread whose one canon-spec annotation, a comment of its own, cites the section Proving of `specs/methodology/loaves.md`, its docstrings and its comment after code naming no file and no section \
    **Snippet:**

      ```python
      """Proves each loaf before it is baked."""


      # @canon-spec specs/methodology/loaves.md § Proving
      def prove(loaf):
          """-> the loaf, proved for an hour."""
          return loaf  # an hour in the warm
      ```

  - **Fixture:** bread-code-naming-a-section-after-code \
    **Holds:** a Python file for proving bread whose comment after its code, on line 3, names a section by a section sign \
    **Snippet:**

      ```python
      def prove(loaf):
          """-> the loaf, proved for an hour."""
          return loaf  # as § Proving has it
      ```

  - **Fixture:** bread-code-naming-a-file-in-a-docstring \
    **Holds:** a Python file for proving bread whose function's docstring, on line 2, names the file `loaves.md` by its file name alone \
    **Snippet:**

      ```python
      def prove(loaf):
          """-> the loaf, proved as loaves.md has it."""
          return loaf
      ```

  - **Fixture:** bread-code-naming-a-path-in-a-comment \
    **Holds:** a Python file for proving bread holding, on line 1, a comment of its own, no spec annotation, naming the path `specs/methodology/loaves.md` \
    **Snippet:**

      ```python
      # the hour comes from specs/methodology/loaves.md
      def prove(loaf):
          return loaf
      ```
