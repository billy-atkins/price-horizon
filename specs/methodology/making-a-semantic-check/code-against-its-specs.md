## The Code Against Its Specs

This check reads the application's code against the application specs it cites. This file says how the reading is made. It states nothing the code must do. [`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs) has the rules of [`specs/methodology/code.md`](/specs/methodology/code.md), and the rules that file cites for code, alone reach the code. Each judgment here cites the section of that file it is made by.

**Each annotated unit.** The reader reads the sections the unit cites. The reader judges whether the unit carries them out, or checks them as a test does, no more and no less, by [`specs/methodology/code.md § Governed Code and Wiring Code`](/specs/methodology/code.md#governed-code-and-wiring-code) and [`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests). The reader also judges whether the unit's annotations sit where [`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code) puts them. No script can judge where they sit.

**Each file citing no spec.** The reader judges whether it is wiring, or governed code missing its annotations, by [`specs/methodology/code.md § Governed Code and Wiring Code`](/specs/methodology/code.md#governed-code-and-wiring-code). That section also says what a file in a format with no comments is.

**Each spec section no code cites.** The reader judges which of two things it is. It may state something code must carry out, so it is not yet implemented. Or it may state something no code carries out, as an index and an overview do. [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) says what each of those holds.

**American English.** The reader reads the code for it, by [`specs/methodology/code.md § Changing Code`](/specs/methodology/code.md#changing-code).

A list of the files citing no spec and of the sections no code cites is a candidate list. It gives the reader places to look and decides nothing.
