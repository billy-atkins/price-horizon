## Diagram Currency

This check reads a diagram against the sections it draws from and against the file that holds it, by the rules of [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams). The same judgments are made of a diagram before it is added or changed, and of a diagram whose sources have changed.

**The citations first.** Where the diagram's Sources, or a citation back to the diagram, is in the wrong form, that is fixed first. Until then there is nothing to compare.

**The render and the sources.** The reader renders the diagram, through `.ai/skills/author-mermaid-diagram/`, and reads every section the diagram's Sources list names. A wrong diagram cannot be seen in its source and is plain once rendered, so tracing the source by hand does not replace the render. Where the reader has a change's diff, a source the change edited is where to look first.

The reader then makes each of these judgments.

**The picture against its sources.** Does the picture say anything its sources do not? The reader reads it for each fault that [`specs/methodology/semantic-check-methods/main.md § Semantic Check Methods § How a Summary Distorts Its Source`](/specs/methodology/semantic-check-methods/main.md#how-a-summary-distorts-its-source) names.

**Each label against the host file.** The reader lists each node label and each edge label, and finds where the host file's content names each one. [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams) has a diagram show only what its host file names. The most common failure is a diagram that copies its source faithfully. The right aim is a diagram that agrees with its host file. A source drawn in full detail pulls that detail up into a host file that never discusses it, so the host file looks as if it covers things it does not. The opposite case happens too: the diagram needs a fact at the host file's own level of detail, and the host file never states it. That is often a real gap in the host file, and that section has it closed in the host file first.

**Each label out of its sentence.** A label copied word for word from the host file can still be wrong in the diagram, because the diagram drops the sentence that limited it. Take a phrase saying how much a nightly job covers. Set beside a branch for the cases the job does not cover, it reads as a contradiction the prose never held. The reader asks whether each label still means the same thing without its sentence, and whether it is attached to the thing it describes.

**The drawing against the host file's prose.** The reader reads the prose around what the diagram shows, and asks whether the drawing denies anything the prose says. Containers are the usual cause. Grouping nodes into a subgraph says the grouping is the real structure. That is wrong where the prose says two structures cut across each other.

**What a collapse dropped.** Collapsing a construct's inner states into one box is allowed, and it drops transitions without warning. The reader walks the source table row by row and confirms that each transition is drawn or is covered by the box. A node left outside the container meant for it loses its edges with no error.

**The Sources list against where each thing lives.** Is a source missing from the list? Is a listed section only a summary of the home, or broader than [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams) asks? The citation back is the one most often forgotten, because it goes in a file the author was not otherwise editing.

**What only the render shows.** Does the reading order match the story the sources tell? Has a node floated to a place that misleads? Has a caveat landed before the thing it limits? A reader with no technical background should be able to trace the diagram's main path without a legend.
