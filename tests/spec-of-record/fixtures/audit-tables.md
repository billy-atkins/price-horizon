**Records:**
  - **Fixture:** visiting-boats-table \
    **Holds:** a Markdown file on boats of one section, Visiting Boats, holding a table opened by a Reference Key of Boat and a Required of Length, its columns Boat and Length, and two rows, Curlew and Tern, each giving a length \
    **Snippet:**

      ```markdown
      # Boats

      ## Visiting Boats

      **Reference Key:** Boat \
      **Required:** Length

      | Boat | Length |
      |---|---|
      | Curlew | 9 m |
      | Tern | 7 m |
      ```

  - **Fixture:** visiting-boats-table-with-a-lowercase-header \
    **Holds:** a Markdown file on boats of one section, Visiting Boats, holding a table opened by a Reference Key of Boat and a Required of Length, its columns Boat, Length and home port, and two rows, Curlew and Tern \
    **Snippet:**

      ```markdown
      # Boats

      ## Visiting Boats

      **Reference Key:** Boat \
      **Required:** Length

      | Boat | Length | home port |
      |---|---|---|
      | Curlew | 9 m | Wells |
      | Tern | 7 m | Blakeney |
      ```

  - **Fixture:** visiting-boats-table-keyed-by-name \
    **Holds:** a Markdown file on boats of one section, Visiting Boats, holding a table opened by a Reference Key of Name and a Required of Length, its columns Boat and Length, and two rows, Curlew and Tern \
    **Snippet:**

      ```markdown
      # Boats

      ## Visiting Boats

      **Reference Key:** Name \
      **Required:** Length

      | Boat | Length |
      |---|---|
      | Curlew | 9 m |
      | Tern | 7 m |
      ```

  - **Fixture:** visiting-boats-table-naming-curlew-twice \
    **Holds:** a Markdown file on boats of one section, Visiting Boats, holding a table opened by a Reference Key of Boat and a Required of Length, its columns Boat and Length, and two rows both naming Curlew \
    **Snippet:**

      ```markdown
      # Boats

      ## Visiting Boats

      **Reference Key:** Boat \
      **Required:** Length

      | Boat | Length |
      |---|---|
      | Curlew | 9 m |
      | Curlew | 7 m |
      ```

  - **Fixture:** visiting-boats-table-missing-a-length \
    **Holds:** a Markdown file on boats of one section, Visiting Boats, holding a table opened by a Reference Key of Boat and a Required of Length, its columns Boat and Length, and two rows, Curlew giving a length and Tern giving none \
    **Snippet:**

      ```markdown
      # Boats

      ## Visiting Boats

      **Reference Key:** Boat \
      **Required:** Length

      | Boat | Length |
      |---|---|
      | Curlew | 9 m |
      | Tern | |
      ```

  - **Fixture:** register-of-harborml \
    **Holds:** a register titled External References whose Records hold one record, its Name HarborML and its Title the Harbor Markup Language \
    **Snippet:**

      ```markdown
      ## External References

      **Records:**
        - **Name:** HarborML \
          **Title:** the Harbor Markup Language
      ```

  - **Fixture:** harborml-mapping \
    **Holds:** a Markdown file on tide records of one section, HarborML, holding a table opened by a Table Name of HarborML Elements, a Reference Key of HarborML and a Required of Section and Treatment, its columns HarborML, Section, Treatment, Departs For and Why, and two rows: tide, whose Treatment is the same, and berth, whose Treatment differs, departing for the canon's form with a Why \
    **Snippet:**

      ```markdown
      # Tide Records

      ## HarborML

      **Table Name:** HarborML Elements \
      **Reference Key:** HarborML \
      **Required:** Section, Treatment

      | HarborML | Section | Treatment | Departs For | Why |
      |---|---|---|---|---|
      | tide | High Water | the same | | |
      | berth | Berths | differs: a berth is named, not numbered | the canon's form | a name reads plainly to a visitor |
      ```

  - **Fixture:** harborml-mapping-opened-by-no-field \
    **Holds:** a Markdown file on tide records of one section, HarborML, holding a table with no field before it, its columns HarborML, Section, Treatment, Departs For and Why, and one row, tide, whose Treatment is the same \
    **Snippet:**

      ```markdown
      # Tide Records

      ## HarborML

      | HarborML | Section | Treatment | Departs For | Why |
      |---|---|---|---|---|
      | tide | High Water | the same | | |
      ```

  - **Fixture:** harborml-mapping-without-a-why-column \
    **Holds:** a Markdown file on tide records of one section, HarborML, holding a table opened by a Table Name of HarborML Elements, a Reference Key of HarborML and a Required of Section and Treatment, its columns HarborML, Section, Treatment and Departs For, and one row, tide, whose Treatment is the same \
    **Snippet:**

      ```markdown
      # Tide Records

      ## HarborML

      **Table Name:** HarborML Elements \
      **Reference Key:** HarborML \
      **Required:** Section, Treatment

      | HarborML | Section | Treatment | Departs For |
      |---|---|---|---|
      | tide | High Water | the same | |
      ```

  - **Fixture:** harborml-mapping-of-a-loose-treatment \
    **Holds:** a Markdown file on tide records of one section, HarborML, holding a table opened by a Table Name of HarborML Elements, a Reference Key of HarborML and a Required of Section and Treatment, its columns HarborML, Section, Treatment, Departs For and Why, and one row, tide, whose Treatment reads kept much as written \
    **Snippet:**

      ```markdown
      # Tide Records

      ## HarborML

      **Table Name:** HarborML Elements \
      **Reference Key:** HarborML \
      **Required:** Section, Treatment

      | HarborML | Section | Treatment | Departs For | Why |
      |---|---|---|---|---|
      | tide | High Water | kept much as written | | |
      ```

  - **Fixture:** harborml-mapping-of-a-departure-without-a-why \
    **Holds:** a Markdown file on tide records of one section, HarborML, holding a table opened by a Table Name of HarborML Elements, a Reference Key of HarborML and a Required of Section and Treatment, its columns HarborML, Section, Treatment, Departs For and Why, and one row, berth, whose Treatment differs, departing for the canon's form with no Why \
    **Snippet:**

      ```markdown
      # Tide Records

      ## HarborML

      **Table Name:** HarborML Elements \
      **Reference Key:** HarborML \
      **Required:** Section, Treatment

      | HarborML | Section | Treatment | Departs For | Why |
      |---|---|---|---|---|
      | berth | Berths | differs: a berth is named, not numbered | the canon's form | |
      ```
