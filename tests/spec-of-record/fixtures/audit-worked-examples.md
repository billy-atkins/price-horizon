**Records:**
  - **Fixture:** methodology-index-of-loaves \
    **Holds:** an index of a bakery's methodology, a title and a table of one row naming a file `loaves.md` \
    **Snippet:**

      ```markdown
      # The Bakery's Methodology

      **Reference Key:** File \
      **Required:** Description

      | File | Description |
      |---|---|
      | `loaves.md` | How a loaf is made |
      ```

  - **Fixture:** loaves-naming-the-sourdough-examples \
    **Holds:** a methodology file on loaves whose one section names, on line 5, the folder of worked examples `specs/methodology/examples/bread/sourdough/` \
    **Snippet:**

      ```markdown
      # Loaves

      ## Sourdough

      The worked examples of a sourdough loaf stand in `specs/methodology/examples/bread/sourdough/`.
      ```

  - **Fixture:** loaves-naming-sourdough-and-rye-examples \
    **Holds:** a methodology file on loaves whose one section names the folder of worked examples `specs/methodology/examples/bread/sourdough/` on line 5 and the folder `specs/methodology/examples/bread/rye/` on line 7 \
    **Snippet:**

      ```markdown
      # Loaves

      ## Sourdough

      The worked examples of a sourdough loaf stand in `specs/methodology/examples/bread/sourdough/`.

      The worked examples of a rye loaf stand in `specs/methodology/examples/bread/rye/`.
      ```

  - **Fixture:** loaves-naming-a-levain-example \
    **Holds:** a methodology file on loaves whose one section names the folder of worked examples `specs/methodology/examples/bread/sourdough/` on line 5 and the file `specs/methodology/examples/bread/sourdough/levain.md` on line 7 \
    **Snippet:**

      ```markdown
      # Loaves

      ## Sourdough

      The worked examples of a sourdough loaf stand in `specs/methodology/examples/bread/sourdough/`.

      Its levain is worked through in `specs/methodology/examples/bread/sourdough/levain.md`.
      ```

  - **Fixture:** sourdough-starter-example \
    **Holds:** a worked example of feeding a sourdough starter, a title and one sentence \
    **Snippet:**

      ```markdown
      # Feeding a Starter

      The starter takes equal weights of flour and water each morning.
      ```

  - **Fixture:** rye-proving-example \
    **Holds:** a worked example of proving a rye loaf, a title and one sentence \
    **Snippet:**

      ```markdown
      # Proving a Rye Loaf

      A rye loaf proves in a floured basket for two hours.
      ```
