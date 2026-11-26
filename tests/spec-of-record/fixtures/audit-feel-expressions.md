**Records:**
  - **Fixture:** bakery-facts-in-scope \
    **Holds:** a bakery's facts with their kinds, as a JSON object: the pickup day a date, the crust a string, and the loaves in stock a number \
    **Snippet:**

      ```json
      {"pickup day": "date", "crust": "string", "loaves in stock": "number"}
      ```

  - **Fixture:** pickup-day-instance-of-date \
    **Holds:** a FEEL expression asking whether the pickup day is an instance of date \
    **Snippet:**

      ```feel
      pickup day instance of date
      ```

  - **Fixture:** pickup-day-instance-of-loaf \
    **Holds:** a FEEL expression asking whether the pickup day is an instance of loaf \
    **Snippet:**

      ```feel
      pickup day instance of loaf
      ```

  - **Fixture:** loaves-in-stock-and-one \
    **Holds:** a FEEL expression adding 1 to the loaves in stock \
    **Snippet:**

      ```feel
      loaves in stock + 1
      ```

  - **Fixture:** in-stock-and-one \
    **Holds:** a FEEL expression adding 1 to a name, in stock, that opens with the word in \
    **Snippet:**

      ```feel
      in stock + 1
      ```

  - **Fixture:** pickup-day-month \
    **Holds:** a FEEL expression naming the month of the pickup day \
    **Snippet:**

      ```feel
      pickup day.month
      ```

  - **Fixture:** pickup-day-hour \
    **Holds:** a FEEL expression naming the hour of the pickup day \
    **Snippet:**

      ```feel
      pickup day.hour
      ```

  - **Fixture:** crust-length \
    **Holds:** a FEEL expression calling string length with the crust \
    **Snippet:**

      ```feel
      string length(crust)
      ```

  - **Fixture:** crust-length-of-two \
    **Holds:** a FEEL expression calling string length with the crust and 2 \
    **Snippet:**

      ```feel
      string length(crust, 2)
      ```

  - **Fixture:** pickup-month-end \
    **Holds:** a FEEL expression calling last day of month with the pickup day \
    **Snippet:**

      ```feel
      last day of month(pickup day)
      ```

  - **Fixture:** pickup-day-two-business-days-on \
    **Holds:** a FEEL expression calling add business days with the pickup day and 2 \
    **Snippet:**

      ```feel
      add business days(pickup day, 2)
      ```

  - **Fixture:** pickup-day-adjusted-sideways \
    **Holds:** a FEEL expression calling adjust with the pickup day, the string SIDEWAYS and a context of a weekend of 6 and 7 and no holidays \
    **Snippet:**

      ```feel
      adjust(pickup day, "SIDEWAYS", {weekend: [6, 7], holidays: []})
      ```
