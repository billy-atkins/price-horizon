**Records:**
  - **Fixture:** image-syntax-in-code \
    **Holds:** a Markdown file on a harbor holding a code span of the image syntax and a fenced block holding an image tag and the image syntax, and no image outside them \
    **Snippet:**

      ````markdown
      # The Harbor

      A chart is written `![chart](chart.png)` in a page.

      ```html
      <img src="chart.png">
      ![chart](chart.png)
      ```
      ````

  - **Fixture:** image-inline \
    **Holds:** a Markdown file on a harbor whose second paragraph embeds an image by a link to its file \
    **Snippet:**

      ```markdown
      # The Harbor

      Each boat takes one mooring.

      ![The moorings](moorings.png)
      ```

  - **Fixture:** image-by-reference \
    **Holds:** a Markdown file on a harbor whose second paragraph embeds an image by a reference label, the label defined after it \
    **Snippet:**

      ```markdown
      # The Harbor

      Each boat takes one mooring.

      ![The moorings][chart]

      [chart]: moorings.png
      ```

  - **Fixture:** image-tag \
    **Holds:** a Markdown file on a harbor whose second paragraph embeds an image by an HTML image tag \
    **Snippet:**

      ```markdown
      # The Harbor

      Each boat takes one mooring.

      <img src="moorings.png" alt="The moorings">
      ```
