**Records:**
  - **Fixture:** walkers-notes \
    **Holds:** a page of notes, one sentence saying the north quay is slippery after rain \
    **Snippet:**

      ```markdown
      # Notes

      A walker's notes: the north quay is slippery after rain.
      ```

  - **Fixture:** notes-citing-nothing \
    **Holds:** a page of notes holding one sentence, no citation and no word of a quay \
    **Snippet:**

      ```markdown
      # Notes

      No citation stands here.
      ```

  - **Fixture:** notes-citing-the-ferry \
    **Holds:** a page of notes whose one sentence cites the section The Ferry of docs/guide.md, the citation carrying no link \
    **Snippet:**

      ```markdown
      # Notes

      The ferry's quay is named in `docs/guide.md § The Ferry`.
      ```

  - **Fixture:** spring-tides-page \
    **Holds:** a page titled Spring Tides, holding one sentence \
    **Snippet:**

      ```markdown
      # Spring Tides

      The spring tide runs high.
      ```

  - **Fixture:** guide-draft \
    **Holds:** a draft of a guide, holding a section The Ferry of one sentence \
    **Snippet:**

      ```markdown
      # A Draft of the Guide

      ## The Ferry

      A draft kept among the skills' own output.
      ```

  - **Fixture:** birds-spec \
    **Holds:** a spec titled Birds in two sections, The Heron and The Egret, each one sentence of nine words or more, with no citation \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk and waits.

      ## The Egret

      The egret wades the shallows at first light alone.
      ```

  - **Fixture:** birds-spec-carrying-links \
    **Holds:** a spec titled Birds in two sections, The Heron and The Egret, each one sentence citing the other section of specs/birds.md, each citation carrying its link \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk, where [`specs/birds.md § The Egret`](/specs/birds.md#the-egret) has its neighbour wade.

      ## The Egret

      The egret wades the shallows at first light, far from the reeds of [`specs/birds.md § The Heron`](/specs/birds.md#the-heron).
      ```
