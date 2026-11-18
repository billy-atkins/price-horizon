## Placement

This check reads whether each file sits where the rules of placement put it, and is named as they name it.

The reader reads a directory together with its `index.md` and every file in it. What is easy to miss:
- one particular file named by a bare filename that another directory also uses, against [`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes);
- a kind of file named by a path, against [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation);
- an open question recorded in a file that cannot cite everything it affects, against [`specs/methodology/spec-placement/open-question.md § Open Question`](/specs/methodology/spec-placement/open-question.md#open-question);
- a spec of a system that already exists saying what its author intended. [`specs/methodology/spec-placement/open-question.md § Open Question`](/specs/methodology/spec-placement/open-question.md#open-question) has such a spec say what is built, and record a suspected defect as an open question.
