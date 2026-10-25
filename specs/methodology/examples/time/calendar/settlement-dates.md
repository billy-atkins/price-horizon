## Settlement Dates

A trade's settlement date and a coupon's payment date, written whole as a file would hold it, each counted on a calendar of business days. The settlement falls two business days after the trade, passing over a weekend and the calendar's holidays. A coupon date on no business day moves to the following business day, unless that falls in the next month, and then to the preceding one, the convention FpML names MODFOLLOWING:

```markdown
## Trade Dates

A trade's settlement date and its coupon's payment date.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - trade date
  - coupon date
  - trading calendar

**Output:**
  - settlement date
  - payment date

**Runs When:** a trade is booked

| Step | Action |
|---|---|
| 1 | Set settlement date to add business days(trade date, 2, trading calendar) |
| 2 | Set payment date to adjust(coupon date, "MODFOLLOWING", trading calendar) |
| 3 | End |

## Facts

**Records:**
  - **Name:** trade date \
    **Type:** date \
    **Means:** the date the trade was made

  - **Name:** coupon date \
    **Type:** date \
    **Means:** the date the coupon falls due by its schedule, before any move to a business day

  - **Name:** trading calendar \
    **Type:** context<weekend: list<number>, holidays: list<date>> \
    **Means:** the market's business days, its weekend Saturday and Sunday, `[6, 7]`, and its holidays the market's

  - **Name:** settlement date \
    **Type:** date \
    **Means:** the date the trade settles

  - **Name:** payment date \
    **Type:** date \
    **Means:** the date the coupon is paid
```

The dates each step gives, the calendar's holidays December 25 and 26, 2024:

| Input | Gives |
|---|---|
| a trade date of `@"2024-12-23"`, a Monday | a settlement date of 2024-12-27, the holidays passed over |
| a coupon date of `@"2024-08-31"`, a Saturday | a payment date of 2024-08-30, the following business day falling in September |
| a coupon date of `@"2024-12-25"`, a holiday | a payment date of 2024-12-27 |
