## Expressions

How an expression is written wherever a construct computes or tests a value, so an author and a reader need neither memory of the language nor a network to write or read one. Each construct writing expressions writes them in FEEL:

| Construct | Writes |
|---|---|
| Decision Table | a condition's cells, its Input Values, a computed header, an outcome's value, a computed outcome, its Output Values and its Default Output |
| State Machine | an exclusive choice's guards |
| Algorithm | a computation's value, a comparison's condition, a loop's list and its order, a run's argument and a Terminates cell |
| Constraint | its rule |
| Facts record | its Values, a function's Derivation and an Initial Value |

`§ Expressions § FEEL` states FEEL in the canon's own words, each statement citing the section of DMN it rests on, so nothing FEEL means is left to recall; where this file is silent, FEEL means what DMN's chapter 10 says (`specs/methodology/external-references.md § External References [Name: DMN]`). A construct's section says which of FEEL's forms its checks decide and which it leaves to reading, and states any writing of FEEL's it narrows to one, as `specs/methodology/sourcing-and-citation.md § An External Reference` has a section state it.

### FEEL

The Friendly Enough Expression Language, DMN's expression language (DMN 10.1), adopted whole. Its departures are a word written plain in a Decision Table's cell, which stands for the string FEEL writes in quotes (`specs/methodology/modeling-constructs.md § Constructs § Decision Table`); and a system's own arithmetic, a precision, a rounding mode and the decimal places a value is held to, as `§ Expressions § FEEL § Arithmetic and Time` states it.

#### Its Values

Each value is of one type, and the types never overlap (DMN 10.3.2.1, 10.3.2.3):

| Type | Written | What it holds |
|---|---|---|
| number | `12`, `-0.5`, `1.2e3` | a decimal of up to 34 significant digits, rounded to the nearest, a tie to the even neighbour; no infinity and no not-a-number, `null` standing for either; `1` and `1.00` equal (DMN 10.3.2.3.1) |
| string | `"Gold"`, a backslash before a quote, an apostrophe, a backslash, `n`, `r`, `t`, or a `u` and a code point | a sequence of characters (DMN 10.3.2.3.2) |
| boolean | `true`, `false` | a yes or a no (DMN 10.3.2.3.3) |
| date | `date("2024-07-01")`, `@"2024-07-01"`, `date(2024, 7, 1)` | a year, a month and a day of the Gregorian calendar (DMN 10.3.2.3.5, Table 79) |
| time | `time("09:00:00")`, `@"09:00:00Z"` | an hour, a minute, a second and, where it has one, an offset from UTC or a time zone; one with neither is a local time of day (DMN 10.3.2.3.4) |
| date and time | `date and time("2024-07-01T09:00:00Z")`, `@"2024-07-01T09:00:00@Europe/Paris"` | a date, and a time as a time holds one (DMN 10.3.2.3.6) |
| days and time duration | `duration("P3DT2H")`, `@"PT12H"` | days, hours, minutes and seconds (DMN 10.3.2.3.7) |
| years and months duration | `duration("P1Y6M")`, `@"P18M"` | years and months, `P18M` equal to `P1Y6M` (DMN 10.3.2.3.8) |
| list | `[1, 2, 3]`, `[]` | values in order, of any types, a list among them (DMN 10.3.2.5) |
| context | `{rate: 0.05, "due date": @"2024-07-01"}` | entries, each a name or a string and the value it holds, in order (DMN 10.3.2.6) |
| range | `[1..10)`, `]1..10[`, `>= 18`, `< @"2025-01-01"` | the values between two ends, an end included by a bracket facing the values and left out by a parenthesis or a bracket facing away; or every value on one side of one end, by a comparison and that end (DMN 10.3.2.7, grammar rules 7 to 12) |
| function | `function(amount, rate) amount * rate` | parameters and the expression they give a value by (DMN 10.3.2.8) |

A range open at one end is written as a comparison and its end, `< @"2025-01-01"`; the writing `(..x)` belongs to the string `range` reads, as `range("(..2)")`, never to an expression (DMN 10.3.1.2, grammar rule 66). `null` is the one value of no type: what is absent, unknown, or the result of an operation given values outside its domain (DMN 10.3.2.1, 10.3.2.16). The two kinds of duration are different types, and so are a date, a time and a date and time, a date standing for its midnight UTC where a date and time is wanted (DMN 10.3.2.9.4).

#### Names

A name is words, each opening with a letter, `?` or `_` and holding letters, digits, `?` and `_`, the words separated by spaces, and any of `.`, `/`, `-`, `'`, `+` and `*` between them, as `days in arrears`, `loan's balance` or `Income+Expenses`; spaces between words count once, however many there are (DMN 10.3.1.2, grammar rules 25 to 30; 10.3.1.4). A name never opens with one of the words FEEL keeps for itself: `and`, `between`, `else`, `every`, `external`, `false`, `for`, `function`, `if`, `in`, `instance`, `not`, `null`, `of`, `or`, `return`, `satisfies`, `some`, `then` and `true`; a later word of it may be one (DMN 10.3.1.4). Where a name holds an operator or a word FEEL keeps, its words are matched from the left against the names in scope, the longest match winning, so `a-b` is the name `a-b` and `days in arrears` the name `days in arrears` where each is one, and `(a)-(b)` subtracts; parentheses around a name end it (DMN 10.3.1.6).

A name is in scope where the construct declares it, a fact, a Facts record or a Reads item, say; inside a filter, `item` names the item tested, and, where the item is a context, its entries are named too, `item` naming an entry rather than the item where the item holds one so named; inside a `for`, `partial` names the list of results already given; inside a function, its parameters name what it is given; and every built-in function is in scope everywhere (DMN 10.3.2.5, 10.3.2.11, 10.3.2.14).

#### Its Expressions

From the loosest to the tightest, an expression is one of these, so `a + b * c` multiplies first and `a = b + c` adds first (DMN 10.3.1.2, grammar rules 2, 4 and 44 to 52, and the precedence stated beneath them):

| Form | Written | Gives |
|---|---|---|
| a loop | `for x in list return e`, several `x in list` separated by commas, a list written `1..10` or `@"2024-01-01"..@"2024-12-31"` counting by one or by a day, down where its start is the greater | a list of `e` for each `x`, in order, the last list varying fastest (DMN 10.3.2.14) |
| a choice | `if c then a else b` | `a` where `c` is `true`, `b` otherwise, `null` and `false` alike (DMN Table 49) |
| a quantifier | `some x in list satisfies c`, `every x in list satisfies c` | `true` where `c` holds for some, or every, item; an empty list giving `false` for `some` and `true` for `every` (DMN Table 49) |
| a disjunction | `a or b` | as `§ Expressions § FEEL § Null and Three-Valued Logic` has it |
| a conjunction | `a and b` | as `§ Expressions § FEEL § Null and Three-Valued Logic` has it |
| a comparison | `a = b`, `a != b`, `a < b`, `a <= b`, `a > b`, `a >= b`; `a between b and c`; `a in t`, `a in (t, u)` | `true` or `false`, or `null` as `§ Expressions § FEEL § Null and Three-Valued Logic` has it; `between` being `a >= b and a <= c`; `in` testing `a` by a unary test, or any of several, neither `-` nor `not(…)`, which only a whole cell writes (DMN 10.3.1.2, grammar rule 49; Tables 52 to 55) |
| arithmetic | `a + b`, `a - b`, `a * b`, `a / b`, `a ** b`, `-a` | as `§ Expressions § FEEL § Arithmetic and Time` has it; `-4 ** 2` is `16`, the minus binding first, so a power of a negation is written in parentheses (DMN 10.3.1.2) |
| a test of type | `a instance of number`, `a instance of list<string>` | `true` where `a` is a value of the type, `null` being of none but `Null` (DMN Table 61) |
| a path | `loan.balance`, `due date.year` | a context's entry, a date's, a time's or a duration's part, or a range's end; on a list, a list of each item's (DMN Tables 64 to 67) |
| a filter or an index | `list[item > 2]`, `list[1]`, `list[-1]` | the items for which the test is `true`; or the item at that place, the first `1` and the last `-1`, `null` past the end (DMN 10.3.2.5, Table 68) |
| a call | `f(a, b)`, `f(rate: 0.05, amount: a)` | the function's value for those arguments, given by place, every one, or by its parameters' names, an unnamed one `null` (DMN 10.3.2.13.5, Table 63) |
| a value | a literal, a name, a list, a context, a range, a function, or an expression in parentheses | itself |

A comment is `//` to the line's end or `/*` to `*/` (DMN 10.3.1.2).

#### Unary Tests

A unary test is what a Decision Table's condition cell, an Input Values item and a Facts record's Values hold: a test of one value, which that value meets or not, written without the value (DMN 10.3.1.2, grammar rules 7, 8, 13 to 16; Table 55):

- `-`, met by any value;
- a comparison and an end, `< 10`, `>= date("2024-01-01")`, `= base rate`, `!= "Gold"`;
- a range, `[1..10)`, its ends values or expressions of one type;
- an expression, met where the value equals it, where it is a list holding the value, where it is a range holding the value, or, where the expression names `?`, the value tested, where it is `true`, as `? > minimum and ? < maximum`;
- several of these separated by commas, met by any one;
- `not(…)` around several of these, met by what none of them is.

#### Null and Three-Valued Logic

`and`, `or` and `not` take `true`, `false` and anything else, giving `null` only where the answer turns on what is not a boolean, the table read in either order (DMN 10.3.2.4, Tables 50 and 51):

| `a` | `b` | `a and b` | `a or b` |
|---|---|---|---|
| `true` | `true` | `true` | `true` |
| `true` | `false` | `false` | `true` |
| `true` | another | `null` | `true` |
| `false` | `false` | `false` | `false` |
| `false` | another | `false` | `null` |
| another | another | `null` | `null` |

`not(true)` is `false`, `not(false)` is `true`, and `not` of anything else `null`. An equality with `null` is never `null`: `a = null` is `true` where `a` is `null` and `false` otherwise, and `a != null` the opposite (DMN Table 49). Any other comparison of two values not of one type, `"1" = 1`, `null < 5` and `null` tested against a range among them, is `null` (DMN Tables 52 to 54). So an absent value tested by a value, as a unary test `"Gold"` tests it, is `false`, and tested by a comparison or a range is `null`, which no test meets. A function given a value outside its parameters' domain gives `null` (DMN 10.3.2.16).

#### Arithmetic and Time

Numbers add, subtract, multiply and divide exactly to 34 significant digits, a division by zero or a result too large or too small to hold giving `null`; `decimal` and the rounding functions of `§ Expressions § FEEL § Its Functions` give a number the decimal places they are asked for (DMN Tables 57, 59, 60 and 76). Two strings added are joined, the first then the second (DMN Table 57).

**A system's own arithmetic —** FEEL's numbers hold 34 significant digits, rounded to the nearest, a tie to the even neighbour, as `§ Expressions § FEEL § Its Values` states: IEEE 754's decimal128 (DMN 10.3.2.3.1; `specs/methodology/external-references.md § External References [Name: IEEE 754]`). A system computing otherwise is specified by what follows, a departure, DMN fixing FEEL's context where this lets a construct state another:

- **A precision and a rounding mode —** a construct whose section gives the fields states the significant digits its system holds each operation's result to, and the mode it rounds by; each operation's result is then rounded to the decimal places that many significant digits leave, by the mode's function. An operation is each arithmetic operator applied, and each step a function aggregating numbers takes, as `sum` adds and `product` multiplies its items one by one in their order, each result rounded.
- **Decimal places —** a value written to a fact whose Facts record states its decimal places (`specs/methodology/modeling-constructs.md § Constructs § Declaring a Construct § A Fact`) is rounded to them by the writing construct's rounding mode, half even where it states none, a Decision Table's outcome among the values written; DMN's item definitions round nothing, so this too departs from DMN. A part of a fact holds no decimal places of its own, so money a step computes by multiplying or dividing is written to a fact holding them before a part takes it; a sum or difference of money already held to them, or money a function gives, needs none.
- **The modes —** each named for the function DMN gives it (DMN Table 76), the value rounded as that function rounds it:

| Mode | Rounds as | A tie, or any value between two neighbours |
|---|---|---|
| half even | `decimal` | to the nearest, a tie to the even neighbour |
| half up | `round half up` | to the nearest, a tie away from zero |
| half down | `round half down` | to the nearest, a tie toward zero |
| up | `round up` | away from zero |
| down | `round down` | toward zero |
| ceiling | `ceiling` | upward |
| floor | `floor` | downward |

Dates, times and durations combine as this table has it, every other pairing giving `null` (DMN Tables 57 and 59):

| `a` | `b` | gives |
|---|---|---|
| date and time, or date | date and time, or date | `a - b`, a days and time duration; both with an offset, or neither |
| time | time | `a - b`, a days and time duration |
| date, date and time or time | days and time duration | `a + b` and `a - b`, the instant that long after, or before; `b + a` as `a + b` |
| date or date and time | years and months duration | `a + b` and `a - b`, the same day of the month that many months after, or before, the year carrying; `null` where that month has no such day, as `@"2024-01-31" + @"P1M"`; `b + a` as `a + b` |
| a duration | a duration of its kind | `a + b` and `a - b`, their sum or difference; `a / b`, a number |
| a duration | a number | `a * b`, `b * a` and `a / b`, the duration that many times |

A date, a date and time and a time have parts named by a path: `year`, `month`, `day` and `weekday`, Monday `1`; `hour`, `minute`, `second`, `time offset` and `timezone`; a years and months duration its `years` and `months`, a days and time duration its `days`, `hours`, `minutes` and `seconds`; and a range its `start`, `end`, `start included` and `end included` (DMN Tables 65 to 67).

#### Lists, Contexts and Functions

A list never changes: a function gives a new one. A value where a list is wanted is a list of it alone, and a list of one value where a value is wanted is that value (DMN 10.3.2.9.4). A filter's test reads its item as `§ Expressions § FEEL § Names` has it, as `installments[due date < today()]` (DMN 10.3.2.5).

A context never changes either: `context put` gives a new one, every entry it does not set holding what it held, so an entry derived from others is not derived again when they change. A context's entry may read the entries before it, never itself or one after it (DMN 10.3.2.6). A function's body reads its parameters and whatever is in scope where it is written; a function written as a context's entry is named by its entry's name (DMN 10.3.2.13.2, 10.3.2.13.4).

A type in `instance of` or a function's parameter is a type's name from `§ Expressions § FEEL § Its Values`, `Any`, `Null`, `list<T>`, `range<T>`, `context<name: T, …>` or `function<T, …> -> U` (DMN 10.3.1.2, grammar rule 52; 10.3.2.9).

#### Its Functions

Every function FEEL builds in, each called by its name and its arguments in parentheses, by place or by its parameters' names as this table gives them; a parameter marked `?` given or left out, one marked `…` given any number of times; a number giving a place, as `position`, a whole number counting from `1` at the start or `-1` at the end; and a function whose signatures differ in their parameters' names given a row for each (DMN 10.3.4):

| Function | Takes | Gives | Does |
|---|---|---|---|
| date | from | date | the date a date string or a date and time holds (DMN Table 72) |
| date | year, month, day | date | the date of those numbers (DMN Table 72) |
| date and time | date, time | date and time | the date at that time (DMN Table 72) |
| date and time | from | date and time | the date and time a string holds (DMN Table 72) |
| time | from | time | the time a string, a time or a date and time holds (DMN Table 72) |
| time | hour, minute, second, offset? | time | the time of those numbers, at that offset (DMN Table 72) |
| number | from, grouping separator, decimal separator | number | the number a string writes with those separators (DMN Table 72) |
| string | from | string | a value written as a string (DMN Table 72) |
| duration | from | duration | the duration a string holds, of either kind (DMN Table 72) |
| years and months duration | from, to | years and months duration | the whole years and months between two dates (DMN Table 72) |
| range | from | range | the range a string writes, `(..x)` and `[x..)` among its writings (DMN Table 72) |
| not | negand | boolean | its negation (DMN Table 73) |
| substring | string, start position, length? | string | the characters from that place on, or that many (DMN Table 74) |
| string length | string | number | how many characters it holds (DMN Table 74) |
| upper case | string | string | it in capitals (DMN Table 74) |
| lower case | string | string | it in small letters (DMN Table 74) |
| substring before | string, match | string | what comes before the match, or `""` (DMN Table 74) |
| substring after | string, match | string | what comes after the match, or `""` (DMN Table 74) |
| replace | input, pattern, replacement, flags? | string | each match of a regular expression replaced (DMN Table 74) |
| contains | string, match | boolean | whether it holds the match (DMN Table 74) |
| starts with | string, match | boolean | whether it opens with the match (DMN Table 74) |
| ends with | string, match | boolean | whether it ends with the match (DMN Table 74) |
| matches | input, pattern, flags? | boolean | whether a regular expression matches it (DMN Table 74) |
| split | string, delimiter | list | the parts between each match of a regular expression (DMN Table 74) |
| string join | list, delimiter? | string | the strings joined, by the delimiter where given, a `null` among them left out (DMN Table 74) |
| list contains | list, element | boolean | whether the list holds the element (DMN Table 75) |
| count | list | number | how many items it holds (DMN Table 75) |
| min | list | item | the least item, or `null` where it is empty; also given its items as arguments (DMN Table 75) |
| max | list | item | the greatest item, or `null` where it is empty; also given its items as arguments (DMN Table 75) |
| sum | list | number | the numbers' sum, or `null` where it is empty; also given its items as arguments (DMN Table 75) |
| mean | list | number | the numbers' mean; also given its items as arguments (DMN Table 75) |
| all | list | boolean | `false` where an item is `false`, `true` where it is empty or every item is `true`, `null` otherwise; also given its items as arguments (DMN Table 75) |
| any | list | boolean | `true` where an item is `true`, `false` where it is empty or every item is `false`, `null` otherwise; also given its items as arguments (DMN Table 75) |
| sublist | list, start position, length? | list | the items from that place on, or that many (DMN Table 75) |
| append | list, item… | list | the list with the items added at its end (DMN Table 75) |
| concatenate | list… | list | the lists joined in order (DMN Table 75) |
| insert before | list, position, newItem | list | the list with the item put before that place (DMN Table 75) |
| remove | list, position | list | the list without the item at that place (DMN Table 75) |
| list replace | list, position, newItem | list | the list with the item at that place replaced (DMN Table 75) |
| list replace | list, match, newItem | list | the list with each item replaced that the function `match`, given the item and the new item, finds `true` for (DMN Table 75) |
| reverse | list | list | its items in the opposite order (DMN Table 75) |
| index of | list, match | list | the places, ascending, of each item equal to the match (DMN Table 75) |
| union | list… | list | the lists joined, each item once (DMN Table 75) |
| distinct values | list | list | its items, each once, in the order first met (DMN Table 75) |
| flatten | list | list | its items with every list among them opened into its own items (DMN Table 75) |
| product | list | number | the numbers' product; also given its items as arguments (DMN Table 75) |
| median | list | number | the middle number once sorted, or the mean of the two middle ones; also given its items as arguments (DMN Table 75) |
| stddev | list | number | the sample standard deviation, `null` for fewer than two; also given its items as arguments (DMN Table 75) |
| mode | list | list | the numbers occurring most, ascending; also given its items as arguments (DMN Table 75) |
| decimal | n, scale | number | it to that many decimal places, a tie to the even neighbour (DMN Table 76) |
| floor | n, scale? | number | it rounded down, to that many decimal places where given (DMN Table 76) |
| ceiling | n, scale? | number | it rounded up, to that many decimal places where given (DMN Table 76) |
| round up | n, scale | number | it rounded away from zero to that many decimal places (DMN Table 76) |
| round down | n, scale | number | it rounded toward zero to that many decimal places (DMN Table 76) |
| round half up | n, scale | number | it to that many decimal places, a tie away from zero (DMN Table 76) |
| round half down | n, scale | number | it to that many decimal places, a tie toward zero (DMN Table 76) |
| abs | n | n's type | its value without its sign, a number's or a duration's (DMN Table 76) |
| modulo | dividend, divisor | number | the remainder, of the divisor's sign (DMN Table 76) |
| sqrt | number | number | its square root, `null` for a negative (DMN Table 76) |
| log | number | number | its natural logarithm (DMN Table 76) |
| exp | number | number | e to its power (DMN Table 76) |
| odd | number | boolean | whether it is odd (DMN Table 76) |
| even | number | boolean | whether it is even (DMN Table 76) |
| is | value1, value2 | boolean | whether the two are the same value, a time with an offset never the same as one without (DMN Table 77) |
| before | point1, point2 | boolean | whether the first comes before the second (DMN Table 78) |
| before | point, range | boolean | whether the point comes before every value of the range (DMN Table 78) |
| before | range, point | boolean | whether every value of the range comes before the point (DMN Table 78) |
| before | range1, range2 | boolean | whether every value of the first comes before every value of the second (DMN Table 78) |
| after | point1, point2 | boolean | whether the first comes after the second (DMN Table 78) |
| after | point, range | boolean | whether the point comes after every value of the range (DMN Table 78) |
| after | range, point | boolean | whether every value of the range comes after the point (DMN Table 78) |
| after | range1, range2 | boolean | whether every value of the first comes after every value of the second (DMN Table 78) |
| meets | range1, range2 | boolean | whether the first ends, included, where the second starts, included (DMN Table 78) |
| met by | range1, range2 | boolean | whether the second ends, included, where the first starts, included (DMN Table 78) |
| overlaps | range1, range2 | boolean | whether the two share a value (DMN Table 78) |
| overlaps before | range1, range2 | boolean | whether the two share a value, the first starting before and ending within the second (DMN Table 78) |
| overlaps after | range1, range2 | boolean | whether the two share a value, the first starting within and ending after the second (DMN Table 78) |
| finishes | point, range | boolean | whether the range ends, included, at the point (DMN Table 78) |
| finishes | range1, range2 | boolean | whether the first ends where the second ends and lies within it (DMN Table 78) |
| finished by | range, point | boolean | whether the range ends, included, at the point (DMN Table 78) |
| finished by | range1, range2 | boolean | whether the second ends where the first ends and lies within it (DMN Table 78) |
| includes | range, point | boolean | whether the range holds the point (DMN Table 78) |
| includes | range1, range2 | boolean | whether the first holds every value of the second (DMN Table 78) |
| during | point, range | boolean | whether the range holds the point (DMN Table 78) |
| during | range1, range2 | boolean | whether the second holds every value of the first (DMN Table 78) |
| starts | point, range | boolean | whether the range starts, included, at the point (DMN Table 78) |
| starts | range1, range2 | boolean | whether the first starts where the second starts and lies within it (DMN Table 78) |
| started by | range, point | boolean | whether the range starts, included, at the point (DMN Table 78) |
| started by | range1, range2 | boolean | whether the second starts where the first starts and lies within it (DMN Table 78) |
| coincides | point1, point2 | boolean | whether the two are equal (DMN Table 78) |
| coincides | range1, range2 | boolean | whether the two have the same ends, each included alike (DMN Table 78) |
| day of year | date | number | the day's number in its year (DMN Table 79) |
| day of week | date | string | the day's name, `"Monday"` to `"Sunday"` (DMN Table 79) |
| month of year | date | string | the month's name, `"January"` to `"December"` (DMN Table 79) |
| week of year | date | number | the ISO 8601 week's number (DMN Table 79) |
| sort | list, precedes | list | its items in the order the function `precedes`, given two items, finds `true` for where the first comes first (DMN 10.3.4.9) |
| get value | m, key | item | the entry of that name a context holds (DMN Table 81) |
| get entries | m | list | a context's entries, each a context of its `key` and its `value` (DMN Table 81) |
| context | entries | context | the context those entries hold, each a context of a `key` and a `value` (DMN Table 81) |
| context put | context, key, value | context | the context with that entry set (DMN Table 81) |
| context put | context, keys, value | context | the context with the entry a list of keys names set, nested within (DMN Table 81) |
| context merge | contexts | context | the contexts' entries in one, a later one winning (DMN Table 81) |
| now | | date and time | the instant it is read (DMN Table 82) |
| today | | date | the day it is read (DMN Table 82) |

`now()` and `today()` read the wall clock, so a construct reading time reads them as `specs/methodology/modeling-constructs.md § Time` has a construct read the wall clock, and a construct whose clock is another names that clock's fact instead.
