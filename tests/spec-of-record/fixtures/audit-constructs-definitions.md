**Records:**
  - **Fixture:** garden-forms-defining-and-construct \
    **Holds:** a file titled Garden Forms whose section Defining Constructs holds a table of fields, headed Field, Required, Default Value, Values and Holds, of three rows: Modifier, no, none, "Abstract", "Interface"; Extends, where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces, empty, text; and Implements, no, none, text; and whose section Constructs holds a subsection Construct, with a sentence, a Modifier field of Abstract and a Column | Holds table of five rows, `Field`, `Required`, `Default Value`, `Values` and `Holds` \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Defining Constructs

      The fields a form of the garden's gives itself:

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Modifier | no | none | "Abstract", "Interface" | the kind of form it is |
      | Extends | where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces | | text | the form it builds on |
      | Implements | no | none | text | the interfaces it takes |

      ## Constructs

      ### Construct

      The root every form of the garden's builds on.

      **Modifier:** Abstract

      A table of fields takes these columns:

      | Column | Holds |
      |---|---|
      | `Field` | the field's key |
      | `Required` | whether a bed must give it |
      | `Default Value` | what it holds where a bed gives none |
      | `Values` | what it may hold |
      | `Holds` | what it says of the bed |
      ```

  - **Fixture:** garden-forms-implements-required \
    **Holds:** a file titled Garden Forms whose section Defining Constructs holds a table of fields, headed Field, Required, Default Value, Values and Holds, of three rows, Modifier, Extends and Implements, the Implements row on line 11 holding Required yes and its Default Value empty; and whose section Constructs holds a subsection Construct, with a sentence and a Modifier field of Abstract \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Defining Constructs

      The fields a form of the garden's gives itself:

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Modifier | no | none | "Abstract", "Interface" | the kind of form it is |
      | Extends | where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces | | text | the form it builds on |
      | Implements | yes | | text | the interfaces it takes |

      ## Constructs

      ### Construct

      The root every form of the garden's builds on.

      **Modifier:** Abstract
      ```

  - **Fixture:** garden-forms-construct-without-a-modifier \
    **Holds:** a file titled Garden Forms whose section Defining Constructs holds a table of fields, headed Field, Required, Default Value, Values and Holds, of three rows: Modifier, no, none, "Abstract", "Interface"; Extends, where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces, empty, text; and Implements, no, none, text; and whose section Constructs holds a subsection Construct, headed on line 15, with a sentence and no field \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Defining Constructs

      The fields a form of the garden's gives itself:

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Modifier | no | none | "Abstract", "Interface" | the kind of form it is |
      | Extends | where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces | | text | the form it builds on |
      | Implements | no | none | text | the interfaces it takes |

      ## Constructs

      ### Construct

      The root every form of the garden's builds on.
      ```

  - **Fixture:** garden-forms-construct-columns-without-holds \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Construct, with a sentence, a Modifier field of Abstract and, on line 11, a Column | Holds table of four rows, `Field`, `Required`, `Default Value` and `Values` \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Construct

      The root every form of the garden's builds on.

      **Modifier:** Abstract

      | Column | Holds |
      |---|---|
      | `Field` | the field's key |
      | `Required` | whether a bed must give it |
      | `Default Value` | what it holds where a bed gives none |
      | `Values` | what it may hold |
      ```

  - **Fixture:** garden-forms-implements-values-in-words \
    **Holds:** a file titled Garden Forms whose section Defining Constructs holds a table of fields of three rows, Modifier, Extends and Implements, the Implements row on line 11 holding Values the names of some beds; and whose section Constructs holds a subsection Construct, with a sentence, a Modifier field of Abstract and a Column | Holds table of five rows, `Field`, `Required`, `Default Value`, `Values` and `Holds` \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Defining Constructs

      The fields a form of the garden's gives itself:

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Modifier | no | none | "Abstract", "Interface" | the kind of form it is |
      | Extends | where it is neither `§ Constructs § Construct` nor an interface, or is an interface extending interfaces | | text | the form it builds on |
      | Implements | no | none | the names of some beds | the interfaces it takes |

      ## Constructs

      ### Construct

      The root every form of the garden's builds on.

      **Modifier:** Abstract

      | Column | Holds |
      |---|---|
      | `Field` | the field's key |
      | `Required` | whether a bed must give it |
      | `Default Value` | what it holds where a bed gives none |
      | `Values` | what it may hold |
      | `Holds` | what it says of the bed |
      ```

  - **Fixture:** garden-forms-declared-construct \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Declared Construct, with a sentence, a Modifier field of Interface and a table of members, headed Field, Specified By, Required, Default Value, Values and Holds, of two rows: Construct, Instance, yes, empty, text; and Extends, Instance, no, none, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Declared Construct

      What a form of the garden's naming itself shares.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Construct | Instance | yes | | text | the form a bed is |
      | Extends | Instance | no | none | text | the bed's form it builds on |
      ```

  - **Fixture:** garden-forms-declared-construct-extends-required \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Declared Construct, with a sentence, a Modifier field of Interface and a table of members of two rows, Construct, Instance, yes, empty, text, and, on line 14, Extends, Instance, yes, empty, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Declared Construct

      What a form of the garden's naming itself shares.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Construct | Instance | yes | | text | the form a bed is |
      | Extends | Instance | yes | | text | the bed's form it builds on |
      ```

  - **Fixture:** garden-forms-declared-construct-extends-by-definition \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Declared Construct, with a sentence, a Modifier field of Interface and a table of members of two rows, Construct, Instance, yes, empty, text, and Extends, Definition, no, none, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Declared Construct

      What a form of the garden's naming itself shares.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Construct | Instance | yes | | text | the form a bed is |
      | Extends | Definition | no | none | text | the bed's form it builds on |
      ```

  - **Fixture:** garden-forms-ordered-construct \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Ordered Construct, with a sentence, a Modifier field of Interface and a table of members, headed Field, Specified By, Required, Default Value, Values and Holds, of one row: Order, Instance, where the construct leaves open the order it takes its inputs or gives its results in, empty, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Ordered Construct

      What a form of the garden's shares whose result could turn on the order the beds are taken in.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Order | Instance | where the construct leaves open the order it takes its inputs or gives its results in | | text | the order the beds are taken in |
      ```

  - **Fixture:** garden-forms-ordered-construct-order-optional \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Ordered Construct, with a sentence, a Modifier field of Interface and a table of members of one row, on line 13: Order, Instance, no, any, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Ordered Construct

      What a form of the garden's shares whose result could turn on the order the beds are taken in.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Order | Instance | no | any | text | the order the beds are taken in |
      ```

  - **Fixture:** garden-forms-configured-construct \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Configured Construct, with a sentence, a Modifier field of Interface and a table of members, headed Field, Specified By, Required, Default Value, Values and Holds, of one row: Held In, Instance, no, none, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Configured Construct

      What a form of the garden's shares whose rows the gardeners keep as data.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Held In | Instance | no | none | text | the facts the gardeners keep the rows in |
      ```

  - **Fixture:** garden-forms-configured-construct-held-in-required \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Configured Construct, with a sentence, a Modifier field of Interface and a table of members of one row, on line 13: Held In, Instance, yes, empty, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Configured Construct

      What a form of the garden's shares whose rows the gardeners keep as data.

      **Modifier:** Interface

      | Field | Specified By | Required | Default Value | Values | Holds |
      |---|---|---|---|---|---|
      | Held In | Instance | yes | | text | the facts the gardeners keep the rows in |
      ```

  - **Fixture:** garden-forms-decision-table-fields \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Decision Table, with a sentence and a table of fields, headed Field, Required, Default Value, Values and Holds, of eight rows: Hit Policy, no, Unique, `§ Constructs § Decision Table`; Reads, no, none, text; Conditions, yes, empty, text; Computed, no, none, text; Annotations, no, none, text; Input Values, no, none, text; Output Values, where its hit policy is Priority or Output order, empty, text; and Default Output, no, none, text \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Decision Table

      A table deciding what a garden bed is given.

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Hit Policy | no | Unique | `§ Constructs § Decision Table` | which matching rows give a bed its outcome |
      | Reads | no | none | text | the facts it reads from elsewhere |
      | Conditions | yes | | text | the columns it tests a bed by |
      | Computed | no | none | text | the outcome columns it works out |
      | Annotations | no | none | text | the columns that only describe a row |
      | Input Values | no | none | text | the values each condition may take |
      | Output Values | where its hit policy is Priority or Output order | | text | the outcomes in their rank |
      | Default Output | no | none | text | what a bed no row matches is given |
      ```

  - **Fixture:** garden-forms-decision-table-hit-policy-first \
    **Holds:** a file titled Garden Forms whose section Constructs holds a subsection Decision Table, with a sentence and a table of fields of eight rows, Hit Policy, Reads, Conditions, Computed, Annotations, Input Values, Output Values and Default Output, the Hit Policy row on line 11 holding Default Value First \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Decision Table

      A table deciding what a garden bed is given.

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Hit Policy | no | First | `§ Constructs § Decision Table` | which matching rows give a bed its outcome |
      | Reads | no | none | text | the facts it reads from elsewhere |
      | Conditions | yes | | text | the columns it tests a bed by |
      | Computed | no | none | text | the outcome columns it works out |
      | Annotations | no | none | text | the columns that only describe a row |
      | Input Values | no | none | text | the values each condition may take |
      | Output Values | where its hit policy is Priority or Output order | | text | the outcomes in their rank |
      | Default Output | no | none | text | what a bed no row matches is given |
      ```

  - **Fixture:** garden-forms-tabular-columns \
    **Holds:** a file titled Garden Forms whose section Constructs holds six subsections: Tabular Construct, with a table of fields of one row, Table Name, where its definition names its tables, empty, text; State Machine, with three Column | Holds tables, of the rows `State`, `Description`, `Initial` and `Terminal`, of the rows `Name`, `From`, `To`, `Trigger`, `Guard` and `Effect`, and of the rows `Member` and `Class`; DAG, with one Column | Holds table of the rows `Task`, `Work`, `Depends On`, `Guard`, `Timeout` and `Tolerated`; Algorithm, with one of the rows `Step`, `Action` and `Terminates`; Constraint, with one of the rows `Name`, `Constraint`, `Applies To` and `Enforced By`; and Decision Table, with one of the row `Name` and three rows naming a kind of column in words \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Tabular Construct

      The rows and columns every tabular form of the garden's takes.

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Table Name | where its definition names its tables | | text | the table's name |

      ### State Machine

      The seasons a bed passes through.

      | Column | Holds |
      |---|---|
      | `State` | a season of the bed |
      | `Description` | what the bed holds in it |
      | `Initial` | whether a bed starts in it |
      | `Terminal` | whether a bed ends in it |

      Its moves:

      | Column | Holds |
      |---|---|
      | `Name` | the move's name |
      | `From` | the season it leaves |
      | `To` | the season it reaches |
      | `Trigger` | what moves the bed |
      | `Guard` | what must hold first |
      | `Effect` | what the move does |

      Its kinds of trigger:

      | Column | Holds |
      |---|---|
      | `Member` | a trigger |
      | `Class` | its kind |

      ### DAG

      The jobs of a planting day.

      | Column | Holds |
      |---|---|
      | `Task` | the job |
      | `Work` | what is done |
      | `Depends On` | the jobs before it |
      | `Guard` | what must hold first |
      | `Timeout` | how long it may take |
      | `Tolerated` | whether its failure is let pass |

      ### Algorithm

      The steps of pruning a hedge.

      | Column | Holds |
      |---|---|
      | `Step` | the step's number |
      | `Action` | what is done |
      | `Terminates` | why a loop ends |

      ### Constraint

      A rule every bed keeps.

      | Column | Holds |
      |---|---|
      | `Name` | the rule's name |
      | `Constraint` | the rule |
      | `Applies To` | when it holds |
      | `Enforced By` | what keeps it |

      ### Decision Table

      A table deciding what a bed is given.

      | Column | Holds |
      |---|---|
      | `Name` | the row's name |
      | a condition | what it tests |
      | an outcome | what a bed is given |
      | an annotation | what describes the row |
      ```

  - **Fixture:** garden-forms-tabular-columns-decision-table-unnamed \
    **Holds:** a file titled Garden Forms whose section Constructs holds six subsections: Tabular Construct, with a table of fields of one row, Table Name, where its definition names its tables, empty, text; State Machine, with three Column | Holds tables, of the rows `State`, `Description`, `Initial` and `Terminal`, of the rows `Name`, `From`, `To`, `Trigger`, `Guard` and `Effect`, and of the rows `Member` and `Class`; DAG, with one Column | Holds table of the rows `Task`, `Work`, `Depends On`, `Guard`, `Timeout` and `Tolerated`; Algorithm, with one of the rows `Step`, `Action` and `Terminates`; Constraint, with one of the rows `Name`, `Constraint`, `Applies To` and `Enforced By`; and Decision Table, with one, headed on line 80, of no `Name` row, only three rows naming a kind of column in words \
    **Snippet:**

      ```markdown
      # Garden Forms

      ## Constructs

      ### Tabular Construct

      The rows and columns every tabular form of the garden's takes.

      | Field | Required | Default Value | Values | Holds |
      |---|---|---|---|---|
      | Table Name | where its definition names its tables | | text | the table's name |

      ### State Machine

      The seasons a bed passes through.

      | Column | Holds |
      |---|---|
      | `State` | a season of the bed |
      | `Description` | what the bed holds in it |
      | `Initial` | whether a bed starts in it |
      | `Terminal` | whether a bed ends in it |

      Its moves:

      | Column | Holds |
      |---|---|
      | `Name` | the move's name |
      | `From` | the season it leaves |
      | `To` | the season it reaches |
      | `Trigger` | what moves the bed |
      | `Guard` | what must hold first |
      | `Effect` | what the move does |

      Its kinds of trigger:

      | Column | Holds |
      |---|---|
      | `Member` | a trigger |
      | `Class` | its kind |

      ### DAG

      The jobs of a planting day.

      | Column | Holds |
      |---|---|
      | `Task` | the job |
      | `Work` | what is done |
      | `Depends On` | the jobs before it |
      | `Guard` | what must hold first |
      | `Timeout` | how long it may take |
      | `Tolerated` | whether its failure is let pass |

      ### Algorithm

      The steps of pruning a hedge.

      | Column | Holds |
      |---|---|
      | `Step` | the step's number |
      | `Action` | what is done |
      | `Terminates` | why a loop ends |

      ### Constraint

      A rule every bed keeps.

      | Column | Holds |
      |---|---|
      | `Name` | the rule's name |
      | `Constraint` | the rule |
      | `Applies To` | when it holds |
      | `Enforced By` | what keeps it |

      ### Decision Table

      A table deciding what a bed is given.

      | Column | Holds |
      |---|---|
      | a condition | what it tests |
      | an outcome | what a bed is given |
      | an annotation | what describes the row |
      ```
