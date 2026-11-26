**Records:**
  - **Fixture:** kept-words-listed-whole \
    **Holds:** a file of one section on FEEL's names, its one sentence listing the twenty words a name never opens with: and, between, else, every, external, false, for, function, if, in, instance, not, null, of, or, return, satisfies, some, then and true \
    **Snippet:**

      ```markdown
      ## Names

      A name never opens with one of the words FEEL keeps for itself: `and`, `between`, `else`, `every`, `external`, `false`, `for`, `function`, `if`, `in`, `instance`, `not`, `null`, `of`, `or`, `return`, `satisfies`, `some`, `then` and `true`; any later word may be one.
      ```

  - **Fixture:** kept-words-listed-with-unless \
    **Holds:** a file of one section on FEEL's names, its one sentence listing the words a name never opens with: the twenty words and, between, else, every, external, false, for, function, if, in, instance, not, null, of, or, return, some, then, true and unless, without satisfies \
    **Snippet:**

      ```markdown
      ## Names

      A name never opens with one of the words FEEL keeps for itself: `and`, `between`, `else`, `every`, `external`, `false`, `for`, `function`, `if`, `in`, `instance`, `not`, `null`, `of`, `or`, `return`, `some`, `then`, `true` and `unless`; any later word may be one.
      ```

  - **Fixture:** built-in-functions-listed-whole \
    **Holds:** a file of one section on FEEL's built-in functions, a table headed Function, Takes, Gives and Does of 104 rows, from date taking from to today taking `()`, each Does cell saying as FEEL builds it in, and those of min, max, sum, mean, all, any, product, median, stddev and mode adding that each is also given its items as arguments \
    **Snippet:**

      ```markdown
      ## Its Functions

      | Function | Takes | Gives | Does |
      |---|---|---|---|
      | date | from | date | as FEEL builds it in |
      | date | year, month, day | date | as FEEL builds it in |
      | date and time | date, time | date and time | as FEEL builds it in |
      | date and time | from | date and time | as FEEL builds it in |
      | time | from | time | as FEEL builds it in |
      | time | hour, minute, second, offset? | time | as FEEL builds it in |
      | number | from, grouping separator, decimal separator | number | as FEEL builds it in |
      | string | from | string | as FEEL builds it in |
      | duration | from | duration | as FEEL builds it in |
      | years and months duration | from, to | years and months duration | as FEEL builds it in |
      | range | from | range | as FEEL builds it in |
      | not | negand | boolean | as FEEL builds it in |
      | substring | string, start position, length? | string | as FEEL builds it in |
      | string length | string | number | as FEEL builds it in |
      | upper case | string | string | as FEEL builds it in |
      | lower case | string | string | as FEEL builds it in |
      | substring before | string, match | string | as FEEL builds it in |
      | substring after | string, match | string | as FEEL builds it in |
      | replace | input, pattern, replacement, flags? | string | as FEEL builds it in |
      | contains | string, match | boolean | as FEEL builds it in |
      | starts with | string, match | boolean | as FEEL builds it in |
      | ends with | string, match | boolean | as FEEL builds it in |
      | matches | input, pattern, flags? | boolean | as FEEL builds it in |
      | split | string, delimiter | list | as FEEL builds it in |
      | string join | list, delimiter? | string | as FEEL builds it in |
      | list contains | list, element | boolean | as FEEL builds it in |
      | count | list | number | as FEEL builds it in |
      | min | list | item | as FEEL builds it in, also given its items as arguments |
      | max | list | item | as FEEL builds it in, also given its items as arguments |
      | sum | list | number | as FEEL builds it in, also given its items as arguments |
      | mean | list | number | as FEEL builds it in, also given its items as arguments |
      | all | list | boolean | as FEEL builds it in, also given its items as arguments |
      | any | list | boolean | as FEEL builds it in, also given its items as arguments |
      | sublist | list, start position, length? | list | as FEEL builds it in |
      | append | list, item… | list | as FEEL builds it in |
      | concatenate | list… | list | as FEEL builds it in |
      | insert before | list, position, newItem | list | as FEEL builds it in |
      | remove | list, position | list | as FEEL builds it in |
      | list replace | list, position, newItem | list | as FEEL builds it in |
      | list replace | list, match, newItem | list | as FEEL builds it in |
      | reverse | list | list | as FEEL builds it in |
      | index of | list, match | list | as FEEL builds it in |
      | union | list… | list | as FEEL builds it in |
      | distinct values | list | list | as FEEL builds it in |
      | flatten | list | list | as FEEL builds it in |
      | product | list | number | as FEEL builds it in, also given its items as arguments |
      | median | list | number | as FEEL builds it in, also given its items as arguments |
      | stddev | list | number | as FEEL builds it in, also given its items as arguments |
      | mode | list | list | as FEEL builds it in, also given its items as arguments |
      | decimal | n, scale | number | as FEEL builds it in |
      | floor | n, scale? | number | as FEEL builds it in |
      | ceiling | n, scale? | number | as FEEL builds it in |
      | round up | n, scale | number | as FEEL builds it in |
      | round down | n, scale | number | as FEEL builds it in |
      | round half up | n, scale | number | as FEEL builds it in |
      | round half down | n, scale | number | as FEEL builds it in |
      | abs | n | n's type | as FEEL builds it in |
      | modulo | dividend, divisor | number | as FEEL builds it in |
      | sqrt | number | number | as FEEL builds it in |
      | log | number | number | as FEEL builds it in |
      | exp | number | number | as FEEL builds it in |
      | odd | number | boolean | as FEEL builds it in |
      | even | number | boolean | as FEEL builds it in |
      | is | value1, value2 | boolean | as FEEL builds it in |
      | before | point1, point2 | boolean | as FEEL builds it in |
      | before | point, range | boolean | as FEEL builds it in |
      | before | range, point | boolean | as FEEL builds it in |
      | before | range1, range2 | boolean | as FEEL builds it in |
      | after | point1, point2 | boolean | as FEEL builds it in |
      | after | point, range | boolean | as FEEL builds it in |
      | after | range, point | boolean | as FEEL builds it in |
      | after | range1, range2 | boolean | as FEEL builds it in |
      | meets | range1, range2 | boolean | as FEEL builds it in |
      | met by | range1, range2 | boolean | as FEEL builds it in |
      | overlaps | range1, range2 | boolean | as FEEL builds it in |
      | overlaps before | range1, range2 | boolean | as FEEL builds it in |
      | overlaps after | range1, range2 | boolean | as FEEL builds it in |
      | finishes | point, range | boolean | as FEEL builds it in |
      | finishes | range1, range2 | boolean | as FEEL builds it in |
      | finished by | range, point | boolean | as FEEL builds it in |
      | finished by | range1, range2 | boolean | as FEEL builds it in |
      | includes | range, point | boolean | as FEEL builds it in |
      | includes | range1, range2 | boolean | as FEEL builds it in |
      | during | point, range | boolean | as FEEL builds it in |
      | during | range1, range2 | boolean | as FEEL builds it in |
      | starts | point, range | boolean | as FEEL builds it in |
      | starts | range1, range2 | boolean | as FEEL builds it in |
      | started by | range, point | boolean | as FEEL builds it in |
      | started by | range1, range2 | boolean | as FEEL builds it in |
      | coincides | point1, point2 | boolean | as FEEL builds it in |
      | coincides | range1, range2 | boolean | as FEEL builds it in |
      | day of year | date | number | as FEEL builds it in |
      | day of week | date | string | as FEEL builds it in |
      | month of year | date | string | as FEEL builds it in |
      | week of year | date | number | as FEEL builds it in |
      | sort | list, precedes | list | as FEEL builds it in |
      | get value | m, key | item | as FEEL builds it in |
      | get entries | m | list | as FEEL builds it in |
      | context | entries | context | as FEEL builds it in |
      | context put | context, key, value | context | as FEEL builds it in |
      | context put | context, keys, value | context | as FEEL builds it in |
      | context merge | contexts | context | as FEEL builds it in |
      | now | `()` | date and time | as FEEL builds it in |
      | today | `()` | date | as FEEL builds it in |
      ```

  - **Fixture:** built-in-functions-counting-in-words \
    **Holds:** a file of one section on FEEL's built-in functions, a table headed Function, Takes, Gives and Does of 104 rows, from date taking from to today taking `()`, its row of count taking a list and giving a string, each Does cell saying as FEEL builds it in, and those of min, max, sum, mean, all, any, product, median, stddev and mode adding that each is also given its items as arguments \
    **Snippet:**

      ```markdown
      ## Its Functions

      | Function | Takes | Gives | Does |
      |---|---|---|---|
      | date | from | date | as FEEL builds it in |
      | date | year, month, day | date | as FEEL builds it in |
      | date and time | date, time | date and time | as FEEL builds it in |
      | date and time | from | date and time | as FEEL builds it in |
      | time | from | time | as FEEL builds it in |
      | time | hour, minute, second, offset? | time | as FEEL builds it in |
      | number | from, grouping separator, decimal separator | number | as FEEL builds it in |
      | string | from | string | as FEEL builds it in |
      | duration | from | duration | as FEEL builds it in |
      | years and months duration | from, to | years and months duration | as FEEL builds it in |
      | range | from | range | as FEEL builds it in |
      | not | negand | boolean | as FEEL builds it in |
      | substring | string, start position, length? | string | as FEEL builds it in |
      | string length | string | number | as FEEL builds it in |
      | upper case | string | string | as FEEL builds it in |
      | lower case | string | string | as FEEL builds it in |
      | substring before | string, match | string | as FEEL builds it in |
      | substring after | string, match | string | as FEEL builds it in |
      | replace | input, pattern, replacement, flags? | string | as FEEL builds it in |
      | contains | string, match | boolean | as FEEL builds it in |
      | starts with | string, match | boolean | as FEEL builds it in |
      | ends with | string, match | boolean | as FEEL builds it in |
      | matches | input, pattern, flags? | boolean | as FEEL builds it in |
      | split | string, delimiter | list | as FEEL builds it in |
      | string join | list, delimiter? | string | as FEEL builds it in |
      | list contains | list, element | boolean | as FEEL builds it in |
      | count | list | string | as FEEL builds it in |
      | min | list | item | as FEEL builds it in, also given its items as arguments |
      | max | list | item | as FEEL builds it in, also given its items as arguments |
      | sum | list | number | as FEEL builds it in, also given its items as arguments |
      | mean | list | number | as FEEL builds it in, also given its items as arguments |
      | all | list | boolean | as FEEL builds it in, also given its items as arguments |
      | any | list | boolean | as FEEL builds it in, also given its items as arguments |
      | sublist | list, start position, length? | list | as FEEL builds it in |
      | append | list, item… | list | as FEEL builds it in |
      | concatenate | list… | list | as FEEL builds it in |
      | insert before | list, position, newItem | list | as FEEL builds it in |
      | remove | list, position | list | as FEEL builds it in |
      | list replace | list, position, newItem | list | as FEEL builds it in |
      | list replace | list, match, newItem | list | as FEEL builds it in |
      | reverse | list | list | as FEEL builds it in |
      | index of | list, match | list | as FEEL builds it in |
      | union | list… | list | as FEEL builds it in |
      | distinct values | list | list | as FEEL builds it in |
      | flatten | list | list | as FEEL builds it in |
      | product | list | number | as FEEL builds it in, also given its items as arguments |
      | median | list | number | as FEEL builds it in, also given its items as arguments |
      | stddev | list | number | as FEEL builds it in, also given its items as arguments |
      | mode | list | list | as FEEL builds it in, also given its items as arguments |
      | decimal | n, scale | number | as FEEL builds it in |
      | floor | n, scale? | number | as FEEL builds it in |
      | ceiling | n, scale? | number | as FEEL builds it in |
      | round up | n, scale | number | as FEEL builds it in |
      | round down | n, scale | number | as FEEL builds it in |
      | round half up | n, scale | number | as FEEL builds it in |
      | round half down | n, scale | number | as FEEL builds it in |
      | abs | n | n's type | as FEEL builds it in |
      | modulo | dividend, divisor | number | as FEEL builds it in |
      | sqrt | number | number | as FEEL builds it in |
      | log | number | number | as FEEL builds it in |
      | exp | number | number | as FEEL builds it in |
      | odd | number | boolean | as FEEL builds it in |
      | even | number | boolean | as FEEL builds it in |
      | is | value1, value2 | boolean | as FEEL builds it in |
      | before | point1, point2 | boolean | as FEEL builds it in |
      | before | point, range | boolean | as FEEL builds it in |
      | before | range, point | boolean | as FEEL builds it in |
      | before | range1, range2 | boolean | as FEEL builds it in |
      | after | point1, point2 | boolean | as FEEL builds it in |
      | after | point, range | boolean | as FEEL builds it in |
      | after | range, point | boolean | as FEEL builds it in |
      | after | range1, range2 | boolean | as FEEL builds it in |
      | meets | range1, range2 | boolean | as FEEL builds it in |
      | met by | range1, range2 | boolean | as FEEL builds it in |
      | overlaps | range1, range2 | boolean | as FEEL builds it in |
      | overlaps before | range1, range2 | boolean | as FEEL builds it in |
      | overlaps after | range1, range2 | boolean | as FEEL builds it in |
      | finishes | point, range | boolean | as FEEL builds it in |
      | finishes | range1, range2 | boolean | as FEEL builds it in |
      | finished by | range, point | boolean | as FEEL builds it in |
      | finished by | range1, range2 | boolean | as FEEL builds it in |
      | includes | range, point | boolean | as FEEL builds it in |
      | includes | range1, range2 | boolean | as FEEL builds it in |
      | during | point, range | boolean | as FEEL builds it in |
      | during | range1, range2 | boolean | as FEEL builds it in |
      | starts | point, range | boolean | as FEEL builds it in |
      | starts | range1, range2 | boolean | as FEEL builds it in |
      | started by | range, point | boolean | as FEEL builds it in |
      | started by | range1, range2 | boolean | as FEEL builds it in |
      | coincides | point1, point2 | boolean | as FEEL builds it in |
      | coincides | range1, range2 | boolean | as FEEL builds it in |
      | day of year | date | number | as FEEL builds it in |
      | day of week | date | string | as FEEL builds it in |
      | month of year | date | string | as FEEL builds it in |
      | week of year | date | number | as FEEL builds it in |
      | sort | list, precedes | list | as FEEL builds it in |
      | get value | m, key | item | as FEEL builds it in |
      | get entries | m | list | as FEEL builds it in |
      | context | entries | context | as FEEL builds it in |
      | context put | context, key, value | context | as FEEL builds it in |
      | context put | context, keys, value | context | as FEEL builds it in |
      | context merge | contexts | context | as FEEL builds it in |
      | now | `()` | date and time | as FEEL builds it in |
      | today | `()` | date | as FEEL builds it in |
      ```

  - **Fixture:** calendar-functions-listed-whole \
    **Holds:** a file of one section on a library's calendar functions, a table headed Function, Takes, Gives, Values, Does and Body of six rows, last day of month, business day?, following business day, preceding business day, adjust and add business days, each body a FEEL expression over its parameters \
    **Snippet:**

      ```markdown
      ## Calendar Functions

      | Function | Takes | Gives | Values | Does | Body |
      |---|---|---|---|---|---|
      | last day of month | day: date | date | none | the day before the first of the next month | `date(if day.month = 12 then day.year + 1 else day.year, if day.month = 12 then 1 else day.month + 1, 1) - @"P1D"` |
      | business day? | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | boolean | none | whether the day falls on neither a weekend day nor a holiday | `not(day.weekday in calendar.weekend) and not(day in calendar.holidays)` |
      | following business day | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the earliest business day on or after the day | `min((for i in 0..7 * (count(calendar.holidays) + 1) return day + @"P1D" * i)[business day?(item, calendar)])` |
      | preceding business day | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the latest business day on or before the day | `max((for i in 0..7 * (count(calendar.holidays) + 1) return day - @"P1D" * i)[business day?(item, calendar)])` |
      | adjust | day: date, convention: string, calendar: context<weekend: list<number>, holidays: list<date>> | date | `convention`: `"FOLLOWING"`, `"MODFOLLOWING"`, `"PRECEDING"`, `"MODPRECEDING"`, `"NONE"` | the day kept, or moved forward or back to a business day | `if convention = "NONE" then day else if convention = "FOLLOWING" then following business day(day, calendar) else preceding business day(day, calendar)` |
      | add business days | from: date, days: number, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the business day the count of business days away from the day | `if days = 0 then from else (for i in 1..7 * (abs(days) + count(calendar.holidays) + 1) return from + @"P1D" * i * (if days > 0 then 1 else -1))[business day?(item, calendar)][abs(days)]` |
      ```

  - **Fixture:** calendar-functions-without-adjust \
    **Holds:** a file of one section on a library's calendar functions, a table headed Function, Takes, Gives, Values, Does and Body of five rows, last day of month, business day?, following business day, preceding business day and add business days, each body a FEEL expression over its parameters \
    **Snippet:**

      ```markdown
      ## Calendar Functions

      | Function | Takes | Gives | Values | Does | Body |
      |---|---|---|---|---|---|
      | last day of month | day: date | date | none | the day before the first of the next month | `date(if day.month = 12 then day.year + 1 else day.year, if day.month = 12 then 1 else day.month + 1, 1) - @"P1D"` |
      | business day? | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | boolean | none | whether the day falls on neither a weekend day nor a holiday | `not(day.weekday in calendar.weekend) and not(day in calendar.holidays)` |
      | following business day | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the earliest business day on or after the day | `min((for i in 0..7 * (count(calendar.holidays) + 1) return day + @"P1D" * i)[business day?(item, calendar)])` |
      | preceding business day | day: date, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the latest business day on or before the day | `max((for i in 0..7 * (count(calendar.holidays) + 1) return day - @"P1D" * i)[business day?(item, calendar)])` |
      | add business days | from: date, days: number, calendar: context<weekend: list<number>, holidays: list<date>> | date | none | the business day the count of business days away from the day | `if days = 0 then from else (for i in 1..7 * (abs(days) + count(calendar.holidays) + 1) return from + @"P1D" * i * (if days > 0 then 1 else -1))[business day?(item, calendar)][abs(days)]` |
      ```
