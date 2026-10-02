The rules that reach the code the application specs govern: which code is governed and which is wiring, and how governed code names the specs it carries out.

## Governed Code and Wiring Code

Governed code carries out a spec: it does what a product or technical spec states, and it names that spec with app-spec annotations (`§ Citing the Specs From Code`). Wiring code, the routing, configuration, dependency registration and glue that no spec states, carries no annotation. Wiring exists because the specs stop where more detail would no longer improve the code: the agent writing the code writes the wiring they leave to it, so that the whole delivers what they state.

## Citing the Specs From Code

Governed code names each spec it carries out with app-spec annotations: each a plain comment line of its own, never a documentation comment, holding the tag `@app-spec`, a space, and a citation in the form `specs/methodology/sourcing-and-citation.md § Writing a Citation` gives for a section in another file or for a whole file, written without the backticks a citation takes in a spec, since the tag marks where it begins and the line where it ends:

```
// @app-spec specs/application/product/example-domain/example.md § Example Capability
// @app-spec specs/application/technical/example-data-model.md
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
```

In a language with block comments only, each annotation is a block comment of its own on one line, its citation ending before the closer, and a heading holding that language's comment closer cannot be cited from it.

**What it cites —** a product spec or a technical spec, or a section of one, as `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` permits code.

**Cited no higher than needed —** the annotations are the narrowest citations that together state all of what the unit carries out: for each part, the deepest section holding it, or a whole file where the unit carries out the whole file, as a data repository class carrying out every entity of a data model file cites that file. A citation above what is needed claims the unit carries out more than it does; one below it leaves part of what governs the unit uncited.

**A list, one line per citation, sorted —** a unit answering to several specs, a product promise and the technical section making it true among them, carries an annotation for each, on consecutive lines, sorted in plain character order of the citation, so the list has one order whoever writes it, and two changes to it collide less often. One citation to a line keeps each readable, makes its change a line of its own in a diff, and leaves a heading free to hold any punctuation.

**Where it sits —** above everything belonging to the smallest unit whose behavior carries out the cited spec, or its part of it, its documentation comment, decorators, attributes and annotations included: a function, a method, a class, or a module, whose annotations open its file after whatever the language or its tools require first, a shebang, a licence header or a package clause among them. Where a language reads the comment directly above a unit as its documentation, as Go does, a blank line separates the annotations from the unit's own comment.

**Why it is a citation —** an annotation makes the link one spec makes to another, so it is held to the same guarantee: it names a file, and a heading, that exist, and a heading retitled updates every annotation naming it in the same edit, per `specs/methodology/sourcing-and-citation.md § Titling a Heading`. Kept in the code it describes, it moves with that code through every refactor, where a map kept in a file of its own would drift.

**A comment, not a language's own annotation —** it is not a Java annotation, a C# attribute or a decorator, so it compiles the same in every language and needs no tool to know it.
