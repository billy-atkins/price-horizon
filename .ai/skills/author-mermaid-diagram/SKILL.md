---
name: author-mermaid-diagram
description: Author or edit a Mermaid diagram. Use when adding a diagram to a document, changing an existing one, or when a content change may have left a diagram stale. Covers where a diagram goes and the form it takes, the altitude check that keeps it consistent with its host file, its sources and the citations back to it, the layout traps that only appear on render, and the render-before-shipping requirement.
---

# Authoring a Mermaid diagram

`specs/methodology/modeling-constructs.md § Diagrams` sets what a diagram is, where it goes, its form, what it may show, and how a diagram and its sources cite each other. This skill is how a diagram gets authored, rendered and checked within those rules: the steps, and the failures that recur along the way.

## Workflow

**Find where it helps its reader most.** Per `specs/methodology/modeling-constructs.md § Diagrams`.

**Altitude-check every label before drawing.** Per `specs/methodology/modeling-constructs.md § Diagrams`, list each node label and edge label you intend to use. Find where the host file's content names each one. The same section sets the notation, a Mermaid flowchart.

The most common failure is rendering the source faithfully. Faithful-to-the-source is the wrong target; consistent-with-the-host is the right one. A source rendered at full fidelity drags its detail up into a host file that never discusses it. The result reads as though the host covers things it does not. The opposite case occurs too. The diagram needs a fact at the host's own level of detail, and the host never states it. Such a fact is often a real gap in the host, worth closing on its own terms rather than as a workaround to license a picture.

**Then check each label out of its sentence.** Passing the altitude check is necessary, not sufficient. A label can be lifted verbatim from the host file and still be wrong in the diagram, because a diagram strips the sentence that qualified it. In one diagram, a phrase taken word for word from prose described how much some nightly job covers. It sat next to a branch for the cases that job does not cover, and read as a flat contradiction that the prose never contained. Ask whether each label still means the same thing with its sentence removed. Ask too whether the label is attached to the thing it describes. That phrase described the scope of a stored result, and it had been hung on the computation that produced the result.

**Check the diagram cannot contradict the host file's prose.** Read the prose around what the diagram renders, and ask whether the drawing denies anything the prose asserts. Containers are the usual culprit. Grouping nodes into subgraphs asserts that the grouping is the real structure. That assertion is wrong if the prose says two structures cut across one another.

**If you collapsed anything, re-check the source row by row.** Collapsing a construct's internal states into one box is legitimate, and it silently drops transitions. Walk the source table, and confirm every transition is either drawn or subsumed by the box you collapsed into. A node left outside the container it was meant to be grouped into loses its edges with no error and no warning.

**Give it its caption and its sources, and cite it from each source.** Per `specs/methodology/modeling-constructs.md § Diagrams`. The citation back is the one that gets forgotten, since it lands in a file the author was not otherwise editing. Add it in the same change. `.ai/skills/audit-specs/scripts/audit-specs.py` checks both.

**Render it and look at it.** Rendering is required. Hand-tracing Mermaid grammar catches parse errors and nothing else. Layout and semantic defects survive hand-tracing intact and die on first render. Run this skill's `scripts/author-mermaid-diagram.py` from the project root, then read the PNG it writes:

    python <skill-dir>/scripts/author-mermaid-diagram.py --render-diagrams path/to/file.md            # every block
    python <skill-dir>/scripts/author-mermaid-diagram.py --list-diagrams path/to/file.md              # what blocks exist, and the name each renders to
    python <skill-dir>/scripts/author-mermaid-diagram.py --render-diagrams path/to/file.md --block 2  # one block, by the number --list-diagrams shows

The script strips markdown blockquote prefixes, so a diagram drafted inside a quoted design note renders the same as one already checked in. It uses a local `mmdc` when one is on PATH, and falls back to rendering over the network otherwise. It reports which it used. If neither works, say so plainly rather than implying the diagram is verified.

Each render is named for where its diagram lives. The name is the source path as given from the project root, with its folders joined by `_`, then the headings above the block, joined by `--`. So a diagram in `docs/api/overview.md` under `## Diagrams` and `### Request Flow` renders to `docs_api_overview--diagrams--request-flow.png`. Hyphens only ever appear inside a name, never between folders, so `a/b-c.md` and `a-b/c.md` cannot collide. Names use only lowercase ASCII letters, digits and hyphens, so they are legal on Windows, macOS and Linux. Because they are lowercase, no two names can differ only in case, which Windows and macOS would treat as the same file. Rendering a file clears that file's earlier renders and no other file's. That is why the root matters. Naming by basename alone once let two files both called `architecture.md` write to the same PNG. Rendering one deleted the other's output as stale, while reporting success.

Look for the failures the source cannot show you: whether the reading order matches the story, whether anything floated somewhere misleading, whether a caveat landed before the thing it qualifies. The target is a diagram whose main path a reader with no technical background traces without a legend.

## Layout traps

Every one of these is invisible in the source and obvious on render.

**Reference Key:** Symptom \
**Required:** Cause, Fix

| Symptom | Cause | Fix |
|---|---|---|
| A node floats to the top, reading as the diagram's root | It has only outgoing edges, and `flowchart TD` puts sources at the top | Give it an incoming edge, if one is accurate. For something that applies *at* other nodes rather than flowing into them, undirected links (`A -.- B`) place it beside the spine instead of above it, and avoid asserting a direction the prose never claims |
| A caveat or exception renders above the flow it qualifies | It hangs off a node that itself floated to the top | Fix the floating node; the caveat follows it down |
| A crossed or negated edge still reads as a connection | Any line between two things says "related" louder than a small ✗ says "not" | Draw no edge at all and let the separation carry it, with the reason in the caption. Absence is the clearest way to render absence |
| A subgraph renders as a tall column dominating the image | Its nodes have no edges between them, so they stack along the flow direction | `direction LR` inside that subgraph *sometimes* works, and is unreliable for the reason `§ What you cannot control` gives. The durable fix is usually that those nodes are a list, not a structure: collapse them into one node |
| A node placed beside the flow by undirected links gets dragged back into it | It has a directed edge to something else. One directed child is enough to give it a rank, and it pulls its child down with it | Undirected links only keep a node beside the spine if *every* one of its edges is undirected. If it needs a child, it is part of the flow, not beside it |
| An explanation or caveat drawn as a node reads as a step | A box is a thing or a stage; nothing about it says "this is a remark about the other boxes" | Put statements *about* the diagram in the caption. A relationship between two nodes, a limit on the whole, a reason: none of these survive being boxed |
| An edge label becomes a floating text box in dead space | The label is too long for the edge's run | Shorten it, and move the detail to the caption |
| Two boxes meant to be the same thing read as two different things | Differentiating subtitles on each | Label them identically, and put the distinction in the container title or the caption |
| Styling vanishes or turns illegible under a dark theme | `fill:` with no `color:` | Always pair them |
| A success terminus looks like a failure | One `classDef` covering every terminal node | Give the success state its own class |
| Edges to or from a subgraph's own ID lay out oddly | Cluster-boundary edges are a known Mermaid weak spot | Valid, but confirm on render; retarget to a specific node inside if it looks wrong |

Put `classDef` before the `class` statements that reference it. Either order parses, but definition-first reads correctly.

## What you cannot control

**Subgraph placement order.** Mermaid has no mechanism for it. `A ~~~ B`, the invisible link, constrains node rank and does not move clusters. Tested directly against subgraphs, it did not change the placement at all. Flipping `TD` to `LR` only moves the problem to the other axis. So the layout engine may silently invert a diagram whose meaning depends on one cluster reading before another. The only reliable fixes are structural: merge the clusters, put the ordering in the labels where a reader cannot miss it, or accept that this subject does not want to be two clusters. If a diagram fights this more than twice, that is evidence about the diagram, not about the tool.

**`direction` inside a subgraph, reliably.** The documented rule is that if any node in a subgraph is linked from outside it, the subgraph's own `direction` is ignored, and the subgraph inherits the parent graph's. In practice, the directive may be honored anyway, depending on which layout engine is running. That is worse than its not working at all. The diagram looks right, and is one renderer change away from silently reflowing. Check the render rather than trusting the directive, and do not build a diagram whose readability rests on it.

**Which renderer the reader gets, unless you pin it.** Pin the layout engine in front matter on every checked-in diagram:

    ---
    config:
      layout: dagre
    ---
    flowchart TD

Where the engine is left unpinned, a preview extension, a hosted renderer and a local CLI can each pick a different engine. The diagram you verified is then not necessarily the one anyone else sees. Pin *before* tuning a layout, not after. Engines disagree enough that a layout perfected under one can arrive broken under another, and tuning against an unpinned default means tuning against a moving target. Expect pinning to change what you already have, and re-render immediately after adding it.

## When a render surprises you

The trap table covers what has already bitten this project. For anything else, look in the upstream documentation: the flowchart syntax, and a diagram's front matter configuration, at the version `specs/methodology/external-references.md § External References [Name: Mermaid]` pins, and the pages it links to.

Treat what you find there as a candidate, not an answer. Documented behavior and observed behavior diverge often enough to matter. The `direction` keyword inside a subgraph is documented as being ignored when any of that subgraph's nodes link outside it. One engine honors it anyway while another does not, so a diagram can look correct and be one renderer away from reflowing. Invisible links are documented as altering node positioning, and testing showed they do nothing at all to subgraph placement. Both of those cost less to test than to argue about. Render it and look.

## Embedding hazard

When a diagram is drafted inside a quoted block in another document, such as a proposal or a design note, do not end the fenced block with a closing quotation mark glued to the fence:

    ```"

That renders a phantom node containing the literal backticks and quote, both in the preview and in anything pasted out of it. Put the closing quote on its own line, or drop the quote wrapper around blocks that contain fences. Grep for the pattern before shipping.

## Draw structure, not lists

A diagram's job is showing relationships. A group of nodes with no edges between them has no relationships to show, so it is a list. Drawing a list as separate boxes spends heavy visual weight on something carrying no structural information, and crowds out the parts that do. Collapse it into one node whose label names the members. The diagram then gets smaller and reads faster. It also stops depending on layout behavior you cannot control, since a layout engine stacks unconnected nodes wherever it likes.

The check: if you deleted the edges between a set of nodes and lost nothing, they were never a structure.

## A new diagram changes the existing ones

Once a document set has more than one diagram, the diagrams are read as a family. A convention that shifts between them misleads a reader who has just learned it. Check a new diagram against every existing one for:
- **A concept drawn two ways.** The same cross-cutting thing was drawn with directed arrows in one diagram and undirected links in another. That told a reader it flowed *into* the pipeline in one place and *out of* it in another. Pick the grammar that matches what the prose claims. Then fix the other diagram in the same pass rather than leaving the pair inconsistent.
- **A color that means two things.** Green, established as "finished successfully" in one diagram and then reused for an intermediate output in another, teaches the reader something false the second time.
- **One thing under several names.** A start node called "Order placed", "An order", and "A customer order" across diagrams is as many concepts to a reader who does not already know they are one.
- **Shape drift.** If terminals are stadiums in one diagram, they are stadiums everywhere.

The cost of fixing this rises with each diagram added. The fix usually means editing something already shipped. Do it anyway. The alternative is a reader learning a grammar that is only locally true.

## When not to add one

A diagram is a standing liability. Whoever edits its sources must keep it in sync with whatever it renders, forever. That editor knows the diagram exists because each source cites it, as `specs/methodology/modeling-constructs.md § Diagrams` requires. This upkeep is a cost worth paying for a picture that shows something the prose cannot, and is not worth paying otherwise. Before adding one to a set that already has some, check whether most of it already exists elsewhere. A diagram whose only novel content is one decision, with the rest redrawn from two diagrams already in the same file, is redundancy carrying a maintenance cost.

Watch for the diagram that fights its own layout. If two or three honest attempts all render it misleadingly, that is usually the subject telling you it does not want to be a picture, not the tool being awkward. The prose that motivated it may already say the thing perfectly well.
