**Records:**
  - **Fixture:** result-as-the-search-wrote-it \
    **Holds:** a search's result of the word reeds over the operative files as they stand, one place, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-e72fd3-8ae3b806.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** result-whose-place-was-changed \
    **Holds:** that result of the word reeds with its one place naming line 4 where it named line 5, under the same name \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-e72fd3-8ae3b806.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 4
      ```

  - **Fixture:** cited-sections-listing \
    **Holds:** a listing of cited sections over the operative files as they stand, one place saying what it cites, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** cited-sections-query-de57d7-a235776b.md \
          **Kind:** cited sections \
          **Query:**  \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each citing place, by what it cites \
          **Completeness:** complete \
          **Places:**
            - `specs/forms.md § Citations` line 7 cites `specs/target.md § Target`
      ```

  - **Fixture:** cited-sections-listing-of-the-kind-citers \
    **Holds:** that listing with its Kind written as citers, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** cited-sections-query-de57d7-db91e802.md \
          **Kind:** citers \
          **Query:**  \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each citing place, by what it cites \
          **Completeness:** complete \
          **Places:**
            - `specs/forms.md § Citations` line 7 cites `specs/target.md § Target`
      ```

  - **Fixture:** result-whose-snapshot-is-no-code \
    **Holds:** the result of the word reeds with its Snapshot written as words, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-e72fd3-732af77b.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** current-operative-files \
          **Snapshot:** the-files-as-i-found-them \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** result-holding-no-snapshot \
    **Holds:** the result of the word reeds holding no Snapshot, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-e72fd3-69f90aef.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** current-operative-files \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** committed-result-naming-its-last-commit \
    **Holds:** a result of the word reeds over the operative files as a commit held them, holding the Last Commit it read and no Commit \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-37ab1e-0de8b2bd.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** committed-operative-files \
          **Last Commit:** 4b825dc642cb6eb9a060e54bf8d69288fbee4904 \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** committed-result-naming-the-commit-asked-for \
    **Holds:** a result of the word reeds over the operative files as a commit held them, holding the Commit its asker named and no Last Commit \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-1b2436-0cf9805e.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** committed-operative-files \
          **Commit:** 4b825dc642cb6eb9a060e54bf8d69288fbee4904 \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** committed-result-naming-no-commit \
    **Holds:** a result of the committed operative files holding neither a Commit nor a Last Commit, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-37ab1e-306ba3c5.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** committed-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** committed-result-naming-both-commits \
    **Holds:** a result of the committed operative files holding both a Commit and a Last Commit, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-37ab1e-5a2d0e90.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** committed-operative-files \
          **Commit:** 4b825dc642cb6eb9a060e54bf8d69288fbee4904 \
          **Last Commit:** 4b825dc642cb6eb9a060e54bf8d69288fbee4904 \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** current-result-naming-a-commit \
    **Holds:** a result of the operative files as they stand holding a Commit, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-reeds-1b2436-a806006d.md \
          **Kind:** terms \
          **Query:** reeds \
          **Target:** current-operative-files \
          **Commit:** 4b825dc642cb6eb9a060e54bf8d69288fbee4904 \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** working-files-result-naming-its-paths \
    **Holds:** a result of the word heron over the working files, narrowed to the one path it was given \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-heron-9f08a0-412ed10e.md \
          **Kind:** terms \
          **Query:** heron \
          **Target:** working-files \
          **Narrowed To:**
            - `.ai/plans/design-specs`

          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `.ai/plans/design-specs/a-design.md § The Problem` line 5
      ```

  - **Fixture:** working-files-result-naming-no-path \
    **Holds:** a result of the working files holding no Narrowed To, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-heron-9f08a0-9b3dea29.md \
          **Kind:** terms \
          **Query:** heron \
          **Target:** working-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `reeds`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `.ai/plans/design-specs/a-design.md § The Problem` line 5
      ```

  - **Fixture:** ranked-result-holding-its-part \
    **Holds:** a ranked result by meaning holding two places as the part 41 to 42 of its ranking \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are a part of a ranking, and never every place.

      **Records:**
        - **Result:** meaning-the-heron-waits-8d8de2-1883da23.md \
          **Kind:** meaning \
          **Query:** The heron waits. \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** as asked \
          **Completeness:** ranked \
          **Ranking Part:** 41 to 42 \
          **Places:**
            - `specs/birds.md § The Heron` line 5
            - `specs/birds.md § The Egret` line 9
      ```

  - **Fixture:** ranked-result-whose-part-holds-more-places \
    **Holds:** that ranked result saying its part is 41 to 70 while it holds two places, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are a part of a ranking, and never every place.

      **Records:**
        - **Result:** meaning-the-heron-waits-8d8de2-f8dfd608.md \
          **Kind:** meaning \
          **Query:** The heron waits. \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** as asked \
          **Completeness:** ranked \
          **Ranking Part:** 41 to 70 \
          **Places:**
            - `specs/birds.md § The Heron` line 5
            - `specs/birds.md § The Egret` line 9
      ```

  - **Fixture:** ranked-result-past-the-ranking \
    **Holds:** a ranked result by meaning holding no place, its Ranking Part none \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are a part of a ranking, and never every place.

      **Records:**
        - **Result:** meaning-the-heron-waits-8d8de2-d678aba2.md \
          **Kind:** meaning \
          **Query:** The heron waits. \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** as asked \
          **Completeness:** ranked \
          **Ranking Part:** none \
          **Places:** none
      ```

  - **Fixture:** terms-result-holding-a-place-words-apart \
    **Holds:** a search's result of the phrase run again over the operative files as they stand, asked by default, one place where its words stand together and one marked words apart, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-run-again-802564-9339e5e5.md \
          **Kind:** terms \
          **Query:** run again \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `run again`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
            - `specs/target.md § Target` line 7 words apart
      ```

  - **Fixture:** terms-result-asked-for-exact \
    **Holds:** a search's result of the phrase run again over the operative files as they stand, asked for exact, one place, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-run-again-e159df-5bd21e56.md \
          **Kind:** terms \
          **Query:** run again \
          **Exact:** yes \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `run again`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** terms-result-whose-exact-is-neither-yes-nor-no \
    **Holds:** a search's result of the phrase run again whose Exact is maybe, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are every place the search found.

      **Records:**
        - **Result:** terms-run-again-e159df-66b53e60.md \
          **Kind:** terms \
          **Query:** run again \
          **Exact:** maybe \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** each form searched as a phrase, every word reduced to its stem and every identifier split into its words: `run again`. The glossary gives the term no other name \
          **Completeness:** complete \
          **Places:**
            - `specs/target.md § Target` line 5
      ```

  - **Fixture:** meaning-result-asked-for-exact \
    **Holds:** a ranked result by meaning holding an Exact of yes, which only a search by terms holds, its name ending with the hash of its content \
    **Snippet:**

      ```markdown
      # Search Result

      The places are places to read, never findings. They are a part of a ranking, and never every place.

      **Records:**
        - **Result:** meaning-the-heron-waits-b9afa7-d361fb49.md \
          **Kind:** meaning \
          **Query:** The heron waits. \
          **Exact:** yes \
          **Target:** current-operative-files \
          **Snapshot:** 2f509deed56230ca \
          **Run As:** as asked \
          **Completeness:** ranked \
          **Ranking Part:** 1 to 1 \
          **Places:**
            - `specs/target.md § Target` lines 3-5
      ```
