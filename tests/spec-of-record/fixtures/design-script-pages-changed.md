**Records:**
  - **Fixture:** guide-ferry-retitled-beside-a-harbor \
    **Holds:** a guide to an island whose section on the ferry is titled The Ferry and Its Times, naming the north quay, followed by a section The Lighthouse and a section The Harbor saying it was dredged \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry and Its Times

      The ferry leaves from the north quay.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.

      ## The Harbor

      The harbor was dredged last spring.
      ```

  - **Fixture:** guide-giving-the-first-ferry \
    **Holds:** a guide to an island, its sections The Ferry and The Lighthouse, ending in a line giving the hour the first ferry leaves \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.

      The first ferry leaves at seven.
      ```

  - **Fixture:** guide-holding-the-hours-table \
    **Holds:** a guide to an island whose section The Ferry holds a Decision Table of the ferry's hours by season, its Hit Policy First \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** First \
      **Conditions:** Season

      | Season | The ferry |
      |---|---|
      | "winter" | runs twice a day |
      | - | runs each hour |

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.
      ```

  - **Fixture:** guide-holding-a-table-of-no-hit-policy-given \
    **Holds:** a guide to an island whose section The Ferry holds a Decision Table of the ferry's hours by season, its Hit Policy Whenever \
    **Snippet:**

      ```markdown
      # The Island Guide

      A visitor reaches the island by water.

      ## The Ferry

      The ferry leaves from the north quay.

      **Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
      **Hit Policy:** Whenever \
      **Conditions:** Season

      | Season | The ferry |
      |---|---|
      | "winter" | runs twice a day |
      | - | runs each hour |

      ## The Lighthouse

      The lighthouse stands at the western point, and its keeper trims the lamp at dusk.
      ```

  - **Fixture:** birds-spec-repeating-the-heron \
    **Holds:** a spec titled Birds in two sections, The Heron and The Egret, its egret's sentence replaced by the heron's sentence again and a sentence saying a crane flies over \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk and waits.

      ## The Egret

      The heron stands in the reeds at dusk and waits.

      A crane flies over.
      ```

  - **Fixture:** birds-spec-carrying-links-and-a-crane \
    **Holds:** a spec titled Birds in two sections, each sentence citing the other section of specs/birds.md by a citation carrying its link, ending in a sentence saying a crane flies over \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk, where [`specs/birds.md § The Egret`](/specs/birds.md#the-egret) has its neighbour wade.

      ## The Egret

      The egret wades the shallows at first light, far from the reeds of [`specs/birds.md § The Heron`](/specs/birds.md#the-heron).

      A crane flies over.
      ```

  - **Fixture:** birds-spec-carrying-links-its-egret-at-dusk \
    **Holds:** a spec titled Birds in two sections, each sentence citing the other section of specs/birds.md by a citation carrying its link, the egret wading at dusk, ending in a sentence saying a crane flies over \
    **Snippet:**

      ```markdown
      # Birds

      ## The Heron

      The heron stands in the reeds at dusk, where [`specs/birds.md § The Egret`](/specs/birds.md#the-egret) has its neighbour wade.

      ## The Egret

      The egret wades the shallows at dusk, far from the reeds of [`specs/birds.md § The Heron`](/specs/birds.md#the-heron).

      A crane flies over.
      ```

  - **Fixture:** notes-citing-the-ferry-by-its-link \
    **Holds:** a page of notes whose one sentence cites the section The Ferry of docs/guide.md, the citation carrying its link \
    **Snippet:**

      ```markdown
      # Notes

      The ferry's quay is named in [`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry).
      ```
