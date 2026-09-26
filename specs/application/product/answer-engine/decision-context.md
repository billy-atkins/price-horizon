---
technical-specs:
  - specs/application/technical/data-model.md
  - specs/application/technical/engineering-and-production-considerations.md
  - specs/application/technical/query-service/intent-and-retrieval.md
---

## Decision Context

Every answer is shaped by the decision it serves, so PriceHorizon settles that before the first question rather than guessing it from each one. When a Query user signs in, PriceHorizon asks what they are working on: a brand pricing decision, on list price or the brand's price position, or a retailer or promotional decision. A Query user with access to more than one business unit picks which one they are working in at the same point; one with access to a single business unit is never asked. A Query user who skips the greeting and asks a question straight away is asked the same thing before anything is computed, unless the question itself says, and their answer counts for the session the same way.

Both choices hold until the Query user signs out, and every answer shows the business unit and kind of decision it was given for. Either can be changed at any time from where they are shown, which offers the same choices as the greeting, only the business units the Query user can access among them, and the change holds from then on.

A question can still say something different for itself. A decision word in it about Brand A's own decision, such as "promotion", "retailer", "list price" or "price position", applies that kind of decision to that question alone, though a particular retailer's name does not, and neither does a word about the competitor's own price; and a brand or competitor belonging only to another of the Query user's business units applies that business unit to that question alone. The session's choices stay as they were. A question using decision words of both kinds is asked about before anything is computed, rather than one being picked for it, and the answer applies to that question alone. Which options each kind of decision brings is `specs/application/product/answer-engine/position.md § Position — where Brand A should sit`.

### Test Scenarios

```gherkin
Scenario: A session starts by asking what kind of decision the Query user is working on.
  Given a Query user whose access holds only North America Snacks signs in
  When PriceHorizon greets them
  Then it asks whether they are working on a brand pricing decision or a retailer or promotional decision
  And it does not ask which business unit they are working in

Scenario: A Query user with more than one business unit picks one when the session starts.
  Given a Query user whose access holds North America Snacks and Europe Beverages signs in
  When PriceHorizon greets them
  Then it asks which business unit they are working in, as well as what kind of decision

Scenario: A Query user who skips the greeting is asked before anything is computed.
  Given a Query user whose access holds only North America Snacks has signed in and not answered the greeting
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, and what will happen
  Then they are asked whether it is a brand pricing decision or a retailer or promotional decision, before anything is computed
  And their answer holds for the rest of the session

Scenario: A Query user with more than one business unit who skips the greeting is asked which one.
  Given a Query user whose access holds North America Snacks and Europe Beverages, both of which track Competitor Brand, has signed in and not answered the greeting
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, for Brand A's list price
  Then they are asked which business unit they are working in, before anything is computed
  And their answer holds for the rest of the session

Scenario: A Query user who skips the greeting is not asked when the question says what kind of decision it is.
  Given a Query user whose access holds only North America Snacks has signed in and not answered the greeting
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, for Brand A's next promotion
  Then that answer is given, and shown, as a retailer or promotional decision, without asking
  And their next question without a decision word is asked about

Scenario: The session's choices hold and are shown with every answer.
  Given a Query user's session is set to North America Snacks and a brand pricing decision
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, and what will happen
  Then the answer is computed for North America Snacks as a brand pricing decision, without asking
  And the answer shows North America Snacks and a brand pricing decision

Scenario: Changing the kind of decision where it is shown holds from then on.
  Given a Query user's session is set to a brand pricing decision
  When they change it to a retailer or promotional decision where it is shown
  And then ask where Competitor Brand's effective price will be in Texas in 6 months
  Then that answer is given, and shown, as a retailer or promotional decision

Scenario: Changing the business unit where it is shown offers only the Query user's own business units.
  Given a Query user whose access holds North America Snacks and Europe Beverages has a session set to North America Snacks and a brand pricing decision
  When they change the business unit where it is shown
  Then they are offered North America Snacks and Europe Beverages, and no other business unit
  And after they choose Europe Beverages and ask where Rival Cola's effective price will be in Germany in 6 months, that answer is given, and shown, for Europe Beverages

Scenario: A question's own words about a retailer decision apply to that question only.
  Given a Query user's session is set to a brand pricing decision
  When they ask where Competitor Brand's effective price will be in Texas in 6 months, for Brand A's next promotion
  Then that answer is given, and shown, as a retailer or promotional decision
  And the session stays set to a brand pricing decision for the next question

Scenario: A question's own words about a brand pricing decision apply to that question only.
  Given a Query user's session is set to a retailer or promotional decision
  When they ask where Brand A's list price should sit against Competitor Brand's effective price in Texas in 6 months
  Then that answer is given, and shown, as a brand pricing decision
  And the session stays set to a retailer or promotional decision

Scenario: A question about another of the Query user's business units applies to that question only.
  Given a Query user whose access holds North America Snacks and Europe Beverages has a session set to North America Snacks and a brand pricing decision
  When they ask where Rival Cola, a competitor only Europe Beverages tracks, will price in Germany in 6 months
  Then that answer is given, and shown, for Europe Beverages
  And the session stays set to North America Snacks

Scenario: A retailer's name alone does not change the kind of decision.
  Given a Query user's session is set to a brand pricing decision
  When they ask where Competitor Brand's effective price will be at Lone Star Grocers in Texas in 6 months
  Then that answer is given, and shown, as a brand pricing decision, without asking

Scenario: A word about the competitor's own price does not change the kind of decision.
  Given a Query user's session is set to a retailer or promotional decision
  When they ask where Competitor Brand's list price will be in Texas in 6 months
  Then that answer is given, and shown, as a retailer or promotional decision, without asking

Scenario: A question naming both kinds of decision is asked about.
  Given a Query user's session is set to a brand pricing decision
  When they ask whether Brand A's list price or its next promotion should respond to Competitor Brand's effective price in Texas in 6 months
  Then they are asked which kind of decision the question is about
  And nothing is computed until they answer
  And their answer applies to that question alone, the session staying set to a brand pricing decision
```
