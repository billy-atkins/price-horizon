**Records:**
  - **Fixture:** fences-headings-and-citations \
    **Holds:** a Markdown text of forty lines holding a tilde fence with a heading and a backtick fence line inside it, a fence indented in a list item, a three-backtick fence nested in a six-backtick one, a fenced block quoted in a note, an indented code line, a table, two headings sharing the path Twice, a citation with two keys, a same-file citation keyed by a path, and a code span of three backticks within a line \
    **Snippet:**

      ```````markdown
      # Title

      ## First

      ~~~text
      ## Not A Heading
      ```
      still inside
      ~~~

      - an item

        ```markdown
        ## Drafted
        ```

      ``````outer
      ```inner
      held
      ```
      ``````

      > ```mermaid
      > flowchart LR
      >   a --> b
      > ```

          indented code

      | a | b |
      |---|---|

      ## Twice

      one

      ## Twice

      two `specs/a.md § A § B [Country: Canada; Tax Year: 2025]` and
      `§ Table [States.State: open]` with ```x``` inline
      ```````

  - **Fixture:** one-diagram-block \
    **Holds:** a text that is one fenced block of the language mermaid, holding one line \
    **Snippet:**

      ````markdown
      ```mermaid
      flowchart TD
      ```
      ````

  - **Fixture:** diagram-lines-unfenced \
    **Holds:** two lines of a flowchart standing in no fenced block \
    **Snippet:**

      ```text
      flowchart TD
        a --> b
      ```
