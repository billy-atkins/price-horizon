**Records:**
  - **Fixture:** method-tides \
    **Holds:** a Markdown file on reading a tide table of a title and one section, Low Water, of one sentence \
    **Snippet:**

      ```markdown
      # Tides

      ## Low Water

      A tide table gives the hour of low water.
      ```

  - **Fixture:** method-tides-citing-berths \
    **Holds:** a Markdown file on reading a tide table whose one sentence cites the section Visiting Berths of `specs/application/product/berths.md` \
    **Snippet:**

      ```markdown
      # Tides

      A boat waits for the tide as `specs/application/product/berths.md § Visiting Berths` has it.
      ```

  - **Fixture:** product-berths \
    **Holds:** a Markdown file on a harbor's berths of a title and one section, Visiting Berths, of one sentence \
    **Snippet:**

      ```markdown
      # Berths

      ## Visiting Berths

      A visiting boat takes a berth for the night.
      ```

  - **Fixture:** moorings-citing-berths \
    **Holds:** a Markdown file on a harbor's moorings whose one sentence cites the section Visiting Berths of `specs/application/product/berths.md` \
    **Snippet:**

      ```markdown
      # Moorings

      A boat without a mooring takes a berth, as `specs/application/product/berths.md § Visiting Berths` has it.
      ```

  - **Fixture:** moorings-citing-tides \
    **Holds:** a Markdown file on a harbor's moorings whose one sentence cites the section Low Water of `specs/methodology/tides.md` \
    **Snippet:**

      ```markdown
      # Moorings

      A mooring is laid at low water, as `specs/methodology/tides.md § Low Water` has it.
      ```

  - **Fixture:** moorings-naming-the-tides-file \
    **Holds:** a Markdown file on a harbor's moorings whose one sentence names the whole file `specs/methodology/tides.md` \
    **Snippet:**

      ```markdown
      # Moorings

      A mooring is laid at low water, which `specs/methodology/tides.md` tells.
      ```
