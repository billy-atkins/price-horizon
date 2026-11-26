**Records:**
  - **Fixture:** scenarios-one-level-below-their-capability \
    **Holds:** a Markdown file on a bakery whose capability holds a Test Scenarios section one level below it, holding a gherkin block of two scenarios, each with a Given, a When and a Then, one with an And after its Given \
    **Snippet:**

      ````markdown
      # The Bakery

      ## Ordering a Loaf

      A customer orders a loaf for the next morning.

      ### Test Scenarios

      ```gherkin
      Scenario: A loaf is ordered
        Given a customer at the counter
        When the customer orders a rye loaf
        Then the order is written in the book

      Scenario: A loaf is collected
        Given an order in the book
        And the loaf is baked
        When the customer calls
        Then the loaf is handed over
      ```
      ````

  - **Fixture:** scenarios-two-levels-below-their-capability \
    **Holds:** a Markdown file on a bakery whose Test Scenarios section stands two levels below its capability, holding a gherkin block of one scenario with a Given, a When and a Then \
    **Snippet:**

      ````markdown
      # The Bakery

      ## Ordering a Loaf

      #### Test Scenarios

      ```gherkin
      Scenario: A loaf is ordered
        Given a customer at the counter
        When the customer orders a rye loaf
        Then the order is written in the book
      ```
      ````

  - **Fixture:** scenarios-without-a-gherkin-block \
    **Holds:** a Markdown file on a bakery whose Test Scenarios section one level below its capability holds a sentence and no fenced block \
    **Snippet:**

      ```markdown
      # The Bakery

      ## Ordering a Loaf

      ### Test Scenarios

      A customer orders a rye loaf and the order is written in the book.
      ```

  - **Fixture:** scenario-without-a-when \
    **Holds:** a Markdown file on a bakery whose Test Scenarios section holds a gherkin block of one scenario with a Given and a Then and no When \
    **Snippet:**

      ````markdown
      # The Bakery

      ## Ordering a Loaf

      ### Test Scenarios

      ```gherkin
      Scenario: A loaf is ordered
        Given a customer at the counter
        Then the order is written in the book
      ```
      ````

  - **Fixture:** gherkin-outside-scenarios-without-a-given \
    **Holds:** a Markdown file on a bakery with no Test Scenarios section, holding a gherkin block of one scenario with a When and a Then and no Given \
    **Snippet:**

      ````markdown
      # The Bakery

      An example of an order:

      ```gherkin
      Scenario: A loaf is ordered
        When the customer orders a rye loaf
        Then the order is written in the book
      ```
      ````
