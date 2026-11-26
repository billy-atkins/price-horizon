**Records:**
  - **Fixture:** heron-spec \
    **Holds:** a Markdown file titled Target File with one section, Target, of one sentence about a heron in the reeds \
    **Snippet:**

      ```markdown
      # Target File

      ## Target

      The heron stands in the reeds.
      ```

  - **Fixture:** heron-spec-cited-in-its-own-file \
    **Holds:** a Markdown file titled Target File with a section Target of one sentence about a heron, and a section Citing that cites `specs/target.md § Target` \
    **Snippet:**

      ```markdown
      # Target File

      ## Target

      The heron stands in the reeds.

      ## Citing

      The reeds are cited as `specs/target.md § Target`.
      ```

  - **Fixture:** stack-naming-one-code-root \
    **Holds:** a technical stack whose table names Python with the one code root `code` and excludes nothing \
    **Snippet:**

      ```markdown
      # Stack

      ## The Stack

      | Language | Code Roots | Excluded |
      |---|---|---|
      | Python | `code` | |
      ```

  - **Fixture:** heron-function \
    **Holds:** a Python function named heron returning a string that holds the word heron \
    **Snippet:**

      ```python
      def heron():
          return 'a heron in code'
      ```

  - **Fixture:** egret-function \
    **Holds:** a Python function named egret returning a string that holds the words egret and heron \
    **Snippet:**

      ```python
      def egret():
          return 'an egret and a heron in other code'
      ```

  - **Fixture:** heron-class \
    **Holds:** a Python class named Heron and a function named heron that constructs it \
    **Snippet:**

      ```python
      class Heron:
          pass


      def heron():
          return Heron()
      ```

  - **Fixture:** heron-kept-test \
    **Holds:** a Python function named heron_test returning a string that holds the word heron \
    **Snippet:**

      ```python
      def heron_test():
          return 'a heron in a kept test'
      ```

  - **Fixture:** design-citing-the-heron \
    **Holds:** a Markdown file titled Design Document whose one section, The Problem, names a heron and cites `specs/target.md § Target` \
    **Snippet:**

      ```markdown
      # Design Document

      ## The Problem

      The heron is cited as `specs/target.md § Target` from this design.
      ```

  - **Fixture:** plan-citing-the-heron \
    **Holds:** a Markdown file titled Another Plan whose one section, Notes, names a heron and cites `specs/target.md § Target` \
    **Snippet:**

      ```markdown
      # Another Plan

      ## Notes

      A heron in another plan, citing `specs/target.md § Target` too.
      ```

  - **Fixture:** plan-holding-a-class-line \
    **Holds:** a Markdown file titled Another Plan whose one section holds a sentence about a heron in the reeds and a line of Python opening a class Heron \
    **Snippet:**

      ```markdown
      # Another Plan

      ## Notes

      The heron stands in the reeds of another plan.

      class Heron:
      ```

  - **Fixture:** follow-ups-naming-a-heron \
    **Holds:** a Markdown file titled Follow-ups whose one section names a heron and cites nothing \
    **Snippet:**

      ```markdown
      # Follow-ups

      ## One

      A heron in the follow-ups.
      ```

  - **Fixture:** reeds-spec \
    **Holds:** a Markdown file titled Reeds with a section Herons of two sentences, on a heron waiting in the reeds for a fish and on an egret wading, and a section Cranes of one sentence \
    **Snippet:**

      ```markdown
      # Reeds

      ## Herons

      The heron stands in the reeds at the edge of the water and waits for a fish to pass.

      The egret wades through the shallow water and stirs the mud with one foot.

      ## Cranes

      The crane calls across the marsh at dawn, and the others answer from the far bank.
      ```

  - **Fixture:** herons-text-holding-a-sentence-of-the-reeds \
    **Holds:** a Markdown file titled Herons whose one section holds the first sentence of the fixture reeds-spec word for word, a sentence about a heron that cites `specs/target.md § Target`, and a sentence about a spoonbill \
    **Snippet:**

      ```markdown
      # Herons

      ## Herons

      The heron stands in the reeds at the edge of the water and waits for a fish to pass.

      A heron waits in the reeds for a fish, as `specs/target.md § Target` has one stand.

      The spoonbill sweeps its bill through the water of the fixture alone.
      ```

  - **Fixture:** bittern-spec \
    **Holds:** a Markdown file titled Inner with one section, Target, of one sentence about a bittern \
    **Snippet:**

      ```markdown
      # Inner

      ## Target

      The bittern is committed in a folder of the repository.
      ```

  - **Fixture:** seven-wading-birds \
    **Holds:** a Markdown file titled Birds of seven sections, each one sentence saying a named wading bird stands in the reeds at dusk and waits for the tide to turn, the sentences alike but for the bird \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk and waits for the tide to turn.

      ## The Egret

      The egret stands in the reeds at dusk and waits for the tide to turn.

      ## The Ibis

      The ibis stands in the reeds at dusk and waits for the tide to turn.

      ## The Stork

      The stork stands in the reeds at dusk and waits for the tide to turn.

      ## The Crane

      The crane stands in the reeds at dusk and waits for the tide to turn.

      ## The Bittern

      The bittern stands in the reeds at dusk and waits for the tide to turn.

      ## The Spoonbill

      The spoonbill stands in the reeds at dusk and waits for the tide to turn.
      ```

  - **Fixture:** head-git-cannot-read \
    **Holds:** one line of words that are no reference git reads as a repository's HEAD \
    **Snippet:**

      ```text
      no repository git can read
      ```
