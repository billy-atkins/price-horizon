## Directory Summary Currency

This check reads a directory's summaries, its `index.md` and its `architecture.md`, against the files they summarize.

**Two summaries, read apart.** An `index.md` and an `architecture.md` cover different ground, as [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) gives each altitude. So the reader checks each on its own. The reader first reads, once, every file the summaries cover. The reader then checks the overview against all of those files, and each `index.md` row against its own file.

**The source beside each clause.** The reader compares each clause with its source open, as [`specs/methodology/semantic-check-methods/main.md § Semantic Check Methods`](/specs/methodology/semantic-check-methods/main.md#semantic-check-methods) has it. The reader reads for each fault that [`specs/methodology/semantic-check-methods/main.md § Semantic Check Methods § How a Summary Distorts Its Source`](/specs/methodology/semantic-check-methods/main.md#how-a-summary-distorts-its-source) names.

**What is easy to miss.** The finding most often missed in an overview is something left out: a fact the detail files establish that a reader of the overview alone would never learn. [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) has an overview written to stand alone. So the test is never "is it stated somewhere else". The test is: would a reader of this file alone get a false picture, or be unable to follow a later section?
