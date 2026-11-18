## Construct Choice and Form

This check reads two things. One is whether each rule is written in the right form, a construct or prose. The other is whether each construct means what its section in [`specs/methodology/modeling-constructs.md § Constructs`](/specs/methodology/modeling-constructs.md#constructs) says it means.

**What reading passage by passage misses.** Prose can read as complete where a construct would show a gap. So the reader gathers all of a rule's passages before judging its form, and reads each construct with its section open.

**The candidates, then every rule no script decides.** A script decides each declared construct's structure. Where a candidate list comes with the check, the reader takes it first. The reader then reads the files against every rule the check enforces that no script decides. A construct that extends another through its Extends field is read together with the one it extends, as one construct. Under each lead-in of this section stand questions the reader asks, each naming the section whose rule it asks about. The sections set what is asked, and no list of questions limits it.

**The choice of a form.** The reader asks:
- whether prose sends the cases of one rule by two or more facts, or by one fact to more than two outcomes. [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which) chooses a construct for such a rule. The reader judges this by meaning, since no fixed words mark it. The reader first gathers the rule's passages, as [`specs/methodology/modeling-constructs.md § When to Use Which § A Rule's Passages`](/specs/methodology/modeling-constructs.md#a-rules-passages) has a rule read whole;
- whether a table is the construct that [`specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct`](/specs/methodology/modeling-constructs.md#a-tables-construct) gives it. A table that is not is a finding wherever it stands. [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which) lets a table no change wrote keep its declaration until the user migrates it;
- whether the right construct models the rule;
- whether a part hands its work to another construct where [`specs/methodology/modeling-constructs.md § When to Use Which § Combining Constructs`](/specs/methodology/modeling-constructs.md#combining-constructs) writes the handoff;
- whether a configured instance's section says an instance is checked when it is saved, as the written construct is, and whether a value a rule reads is taken as the rule's input. [`specs/methodology/modeling-constructs.md § When to Use Which § A Configured Instance`](/specs/methodology/modeling-constructs.md#a-configured-instance) has both;
- whether a construct section's prose states a rule the files could check, where an outcome the spec states depends on that rule and no check decides it. [`specs/methodology/modeling-constructs.md § Defining Constructs`](/specs/methodology/modeling-constructs.md#defining-constructs) has such a rule written in a column, a field or a form of the construct. It also says how a construct gains one it lacks.

**Every construct.** The reader asks:
- whether each construct's section heading names a thing, never an activity, and whether its description says what it models to a reader meeting it for the first time, against [`specs/methodology/modeling-constructs.md § Constructs § Declared Construct`](/specs/methodology/modeling-constructs.md#declared-construct);
- whether the tables of a construct that extends another hold only what its base lacks, and whether the two read as one pass the checks of the construct's section, against [`specs/methodology/modeling-constructs.md § Constructs § Declared Construct`](/specs/methodology/modeling-constructs.md#declared-construct);
- whether a part's identifier, and a key a citation names, are short and stay the same for the part's life, against [`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct);
- whether each expression means what its construct says, as FEEL evaluates it. The reader checks `null` where a value may be absent or a type differs; `and`, `or` and `not` with their three values; how a date, a time or a duration combines; and how a list, a context or a function is read. [`specs/methodology/expressions.md § Expressions § FEEL § Null and Three-Valued Logic`](/specs/methodology/expressions.md#null-and-three-valued-logic), [`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time) and [`specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions`](/specs/methodology/expressions.md#lists-contexts-and-functions) say how FEEL evaluates each;
- where a construct reads time, whether it reads it as [`specs/methodology/modeling-constructs.md § Time`](/specs/methodology/modeling-constructs.md#time) says. The reader checks its clock, a value in force at an instant, a period a change falls within, a backdated or withdrawn instant, and a date kept on a month's last day or on a business day. For a job's run, the reader checks what a missed or a late run does. The table of trigger kinds in [`specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means`](/specs/methodology/modeling-constructs.md#what-it-means-1) says how a clock other than the wall clock is read.

**A Decision Table.** Against [`specs/methodology/modeling-constructs.md § Constructs § Decision Table`](/specs/methodology/modeling-constructs.md#decision-table) and the sections under it, the reader asks:
- whether a check of a request that [`specs/methodology/modeling-constructs.md § When to Use Which`](/specs/methodology/modeling-constructs.md#when-to-use-which) counts as a construct is written as [`specs/methodology/modeling-constructs.md § Constructs § Decision Table § A Request Turned Away`](/specs/methodology/modeling-constructs.md#a-request-turned-away) has it;
- whether a condition cell holds only the test of its condition, with no comment that belongs in an annotation;
- whether a Reads item that cites a construct names an outcome that construct decides;
- where a condition names its kinds in words only its table uses, whether its values cover every kind of case. If the kinds are defined by yes-or-no questions, [`specs/methodology/modeling-constructs.md § Constructs § Decision Table § A Condition's Fact`](/specs/methodology/modeling-constructs.md#a-conditions-fact) has the condition written as those questions;
- where a cell tests against a fact, which rows a case reaches, and whether every case matches a row;
- where a column's fact is declared in another file, whether its cells test values of that fact's Type;
- whether a computed header's kind agrees with the kind of its cells;
- whether a computed outcome cites an Algorithm where it needs a walk whose order changes it, and whether an outcome that other conditions decide is a table of its own;
- under each hit policy for which that section asks it, whether the outcomes two rows give one case can both be carried out;
- whether the table's outcomes are values, and nothing in its evaluation acts.

**A State Machine.** Against [`specs/methodology/modeling-constructs.md § Constructs § State Machine`](/specs/methodology/modeling-constructs.md#state-machine) and the sections under it, the reader asks:
- where a state cannot stay once its work is done, whether every case takes a transition out of it;
- what a guard's fact means, and what a state's work is;
- for an exclusive choice, whether two of its guards can hold at once, and, where its state cannot stay, whether together they cover every case. The reader asks this where a guard compares a fact with another, where a guard is in another of FEEL's forms, and where one occurrence can make several of the transitions' conditions true together;
- for a guard in another of FEEL's forms, whether each name in it is a fact that section lets a guard name;
- whether a trigger is of the kind that [`specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means`](/specs/methodology/modeling-constructs.md#what-it-means-1) gives its case, and whether an action whose outcome decides where the entity goes is written as a state's work, never as an effect;
- whether a terminal state's description states an outcome, never work, and whether a protocol machine's states, transitions and reasons are as that section has them;
- whether a trigger that recurs is written the same way each time, whether it names only what happens and leaves any condition to a guard, and whether any row lists several triggers;
- whether a Trigger Classes table lists every occurrence of its class and no other, and whether a state taking a class's trigger also takes one of the class's members, however its machine words that member;
- whether a state whose work is another machine's run says `governed by` it, and whether a trigger leaving that work is written where [`specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State`](/specs/methodology/modeling-constructs.md#a-submachine-state) places it.

**An Algorithm and a DAG.** Against [`specs/methodology/modeling-constructs.md § Constructs § Algorithm`](/specs/methodology/modeling-constructs.md#algorithm), [`specs/methodology/modeling-constructs.md § Constructs § Ordered Construct`](/specs/methodology/modeling-constructs.md#ordered-construct) and [`specs/methodology/modeling-constructs.md § Constructs § DAG`](/specs/methodology/modeling-constructs.md#dag), the reader asks:
- whether a loop or a comparison is folded into another step's work, and whether a branch with nothing to do is written `continue`;
- whether a step's work in words computes a value a later step reads, or decides something, which that section gives to a computation and a comparison;
- whether a loop written `in any order` gives the same result whatever its order, and whether a loop written `in an order the system leaves open` has the Constraint that records that its result depends on the order;
- whether every path to `End` sets each fact the Output names that the Inputs do not, and whether a fact read from another file is used as its record types it;
- whether a Terminates cell's number shrinks with each pass toward an end the step reaches, against [`specs/methodology/modeling-constructs.md § Constructs § Algorithm § A Loop That Must End`](/specs/methodology/modeling-constructs.md#a-loop-that-must-end);
- whether each value the system derives is read by a call given the current value. A path that still holds what the value was before a step changed its inputs is a finding;
- whether an Algorithm whose Runs When states an occurrence is in fact run on that occurrence;
- whether a value is rounded only where that section and [`specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`](/specs/methodology/expressions.md#arithmetic-and-time) let it be, and whether money computed by multiplying or dividing reaches a part through a fact that holds decimal places;
- whether a result that depends on an order states that order;
- whether an item copied from a list is read from the list again once a step changes the list, and whether each function a step calls is one of the kinds that section names;
- whether each task's work in a DAG is all of that task's work, whether a task whose work is `none` says whose work it is and when it is done, and whether whatever runs the DAG is in fact run on it.

**A Constraint.** Against [`specs/methodology/modeling-constructs.md § Constructs § Constraint`](/specs/methodology/modeling-constructs.md#constraint), the reader asks:
- whether each part the Enforced By cites keeps the rule at a place where a write could break it;
- whether every write that could break the rule is covered;
- whether a section a rule is `after` or `before` states an operation in its own text;
- whether a step that a rule limits an approximation by keeps that limit.

**A Basic Table and a record type.** The reader asks:
- whether a Basic Table no script reaches, one in a list item, a quote or an indented block, is headed by field labels;
- whether a header word that a script passed as a proper noun's own casing is a proper noun;
- whether a Basic Table declares its natural key where its rows have one, and the columns every row must fill, against [`specs/methodology/modeling-constructs.md § Constructs § Basic Table`](/specs/methodology/modeling-constructs.md#basic-table);
- whether a record type is an entry written repeatedly or a closed set a spec defines. [`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form) says a schema of data the product stores is no record type.
