**Records:**
  - **Fixture:** bakery-glossary \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and three rows in sorted order: Crust, its definition ending Also called rind; Proving Drawer, abbreviated PD; and Sourdough Starter, its definition ending Also called leaven, mother \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf. Also called rind. |
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      | Sourdough Starter | | A ferment of flour and water kept between bakes. Also called leaven, mother. |
      ```

  - **Fixture:** bakery-glossary-unsorted \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and two rows, Proving Drawer then Crust \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      | Crust | | The baked outer layer of a loaf. |
      ```

  - **Fixture:** bakery-glossary-citing \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and two rows, Crust and Proving Drawer, Crust's definition on the fifth line citing `docs/loaves.md § Baking` \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf, as `docs/loaves.md § Baking` has it. |
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      ```

  - **Fixture:** bakery-glossary-under-another-header \
    **Holds:** a glossary titled Glossary, one table with the header Word, Short Form and Meaning and two rows, Crust and Proving Drawer \
    **Snippet:**

      ```markdown
      # Glossary

      | Word | Short Form | Meaning |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf. |
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      ```

  - **Fixture:** bakery-glossary-of-two-tables \
    **Holds:** a glossary titled Glossary, two tables each with the header Term, Abbreviation and Definition, of one row each, Crust then Proving Drawer \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf. |

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      ```

  - **Fixture:** bakery-glossary-other-name-a-term \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and two rows, Crust, its definition ending Also called proving drawer, and Proving Drawer, on the fifth and sixth lines \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf. Also called proving drawer. |
      | Proving Drawer | PD | A warm cabinet where dough rises. |
      ```

  - **Fixture:** bakery-glossary-other-name-shared \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and two rows, Crust and Sourdough Starter, each definition ending Also called rind, on the fifth and sixth lines \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | The baked outer layer of a loaf. Also called rind. |
      | Sourdough Starter | | A ferment of flour and water kept between bakes. Also called rind. |
      ```

  - **Fixture:** bakery-glossary-abbreviated-in-a-definition \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and one row on the fifth line, Proving Drawer, an empty Abbreviation and a definition ending Abbreviated PD \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Proving Drawer | | A warm cabinet where dough rises. Abbreviated PD. |
      ```

  - **Fixture:** bakery-glossary-other-name-mid-definition \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and one row on the fifth line, Crust, whose definition opens Also called rind and goes on with a second sentence \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust | | Also called rind. The baked outer layer of a loaf. |
      ```

  - **Fixture:** bakery-glossary-term-not-bare \
    **Holds:** a glossary titled Glossary, one table with the header Term, Abbreviation and Definition and one row on the fifth line, its term Crust (baked) \
    **Snippet:**

      ```markdown
      # Glossary

      | Term | Abbreviation | Definition |
      |---|---|---|
      | Crust (baked) | | The baked outer layer of a loaf. |
      ```
