**Records:**
  - **Fixture:** library-membership \
    **Holds:** a Markdown file on who may join a community lending library, written to stand at `specs/library/membership.md`: sections on joining, a member's card, lapsed membership and junior members, a table of four kinds of card keyed by Card, and citations of the loans and overdue files of the same library \
    **Snippet:**

      ```markdown
      # Membership

      Who may join the library, what a member's card is for, and how membership ends.

      ## Joining

      Anyone who lives, works or studies in the parish may join the library free of charge.

      A new member shows one proof of address at the desk, and a volunteer fills in the membership form with them. A person with no fixed address joins on the word of a support worker, who signs the form in place of the proof.

      The form is filed the same day, and the member may borrow at once, as `specs/library/loans.md § Borrowing` allows.

      ## A Member's Card

      Each member is given one card, printed with a number and no name. A card is for its holder alone and may not be lent to another person.

      A lost card is replaced at the desk for one pound, and the old number is cancelled so that nobody can borrow on it.

      The member shows the card for every loan. A volunteer who knows the member by sight still asks for it.

      ## Lapsed Membership

      Membership is renewed each January by confirming the member's address at the desk. A membership not renewed by the end of March lapses, and the card stops working until the address is confirmed.

      A lapsed member keeps any item already on loan until its due date, and owes whatever `specs/library/overdue.md § Fines` charges after it.

      Records of a member who has not borrowed for three years are destroyed, and the card number is never issued again.

      ## Junior Members

      A child under sixteen joins with the signature of a parent or guardian, who answers for the items the child borrows.

      Children are never asked to pay for bringing a book back late.

      A junior card borrows from the children's shelves and the general shelves, but not from the film collection, whose loans `specs/library/loans.md § Loan Periods [Item: film]` keeps short.

      On a member's sixteenth birthday the junior card becomes a full card without a new form.

      **Reference Key:** Card

      | Card | Issued To | Borrows |
      |---|---|---|
      | full | a member of sixteen or over | from every collection |
      | junior | a member under sixteen | from every collection but film |
      | group | a school, a care home or a club | up to thirty items for a term |
      | housebound | a member who cannot come in | by a volunteer's home visit |
      ```

  - **Fixture:** library-loans \
    **Holds:** a Markdown file on what a member of a community lending library may borrow and for how long, written to stand at `specs/library/loans.md`: sections on borrowing, loan periods, renewals and returns, a table of five kinds of item keyed by Item, one paragraph shorter than forty characters, and citations of the overdue and holds files of the same library \
    **Snippet:**

      ```markdown
      # Loans

      What a member may borrow, for how long, and how an item comes back.

      ## Borrowing

      A member may have eight items on loan at one time, of which no more than two are films.

      Nobody borrows on someone else's card.

      Reference books, the local history collection and the current issue of each newspaper are read in the library and are never lent.

      A member owing more than five pounds borrows nothing until the debt is cleared.

      Each loan is written to the member's record at the desk, with the date the item is due.

      ## Loan Periods

      How long an item is lent for depends on what kind of item it is:

      **Reference Key:** Item

      | Item | Period | Renewals |
      |---|---|---|
      | book | three weeks | two |
      | large-print book | six weeks | two |
      | audiobook | three weeks | two |
      | film | one week | none |
      | jigsaw | six weeks | one |

      An item borrowed on a group card is due on the last day of term, whatever its kind. The due date is stamped on the slip inside the cover, so the member need not remember it.

      ## Renewals

      A loan may be renewed twice, unless another member is waiting for the item.

      A renewal is made at the desk, by telephone or by a note through the door, and the item need not be brought in. A renewed loan runs for a full period from the day it is renewed, not from the old due date.

      After its last renewal an item is brought back and shown at the desk before the same member borrows it again.

      ## Returns

      An item is returned to the desk during opening hours, or through the flap in the front door when the library is shut. An item put through the flap counts as returned on the last day the library was open.

      Nothing falls due on a day the doors are shut: such an item is due when the library is next open.

      A volunteer looks through each returned item for damage before it goes back on the shelf, as `specs/library/overdue.md § Lost and Damaged Items` has damage dealt with.

      A returned item that another member is waiting for goes to the hold shelf and not to its own, as `specs/library/holds.md § The Queue` orders the waiting.
      ```

  - **Fixture:** library-overdue \
    **Holds:** a Markdown file on what a community lending library does when an item is not back by its due date, written to stand at `specs/library/overdue.md`: sections on reminders, fines, lost and damaged items and waiving a fine, a table of five charges keyed by Charge, and citations of the loans and opening files of the same library \
    **Snippet:**

      ```markdown
      # Overdue Items

      What happens when an item is not back by its due date.

      ## Reminders

      A reminder is posted or telephoned when an item is one week overdue, and again at three weeks. A reminder names the item and its due date and says nothing of money.

      A reminder says how the loan may still be extended, as `specs/library/loans.md § Renewals` allows it.

      After six weeks a volunteer calls at the member's address, if it lies within the parish.

      No reminder is sent for an item due during a closure, since `specs/library/opening.md § Closures` moves its due date.

      ## Fines

      An overdue item is charged at ten pence for each day the library was open, up to two pounds for one item.

      No fine is charged on an item borrowed on a junior card.

      No fine is charged to a housebound member, whose items a volunteer collects.

      Fines are paid at the desk in cash, and the volunteer writes a receipt from the duplicate book.

      **Reference Key:** Charge

      | Charge | Amount |
      |---|---|
      | daily fine | ten pence for each open day |
      | most for one item | two pounds |
      | replacement card | one pound |
      | lost item | its price in the catalogue |
      | mendable damage | nothing |

      ## Lost and Damaged Items

      A member who loses an item pays the price the catalogue holds for it, and the fine on it stops on the day it is reported lost.

      A lost item found within a year is taken back, and what the member paid for it is returned. A book that cannot be found at two yearly checks in a row is written off as lost.

      Damage a volunteer can mend with tape or glue costs the member nothing. A book that cannot be mended is charged as a lost one.

      Lost property left in the library is kept for a month in the box under the desk and then given to the charity shop.

      ## Waiving a Fine

      The librarian may waive a fine where illness, bereavement or a closure kept the member from returning the item.

      A volunteer does not waive a fine alone, but notes the member's reason for the librarian to decide. A waived fine is written in the duplicate book as waived, with the librarian's initials, and is not simply left out.

      Each September the librarian reports to the committee how much was waived over the year.
      ```

  - **Fixture:** library-holds \
    **Holds:** a Markdown file on how a member of a community lending library asks for an item that is out on loan, written to stand at `specs/library/holds.md`: sections on placing a hold, the queue, collecting a held item and expired holds, one paragraph shorter than forty characters, and citations of the loans and catalogue files of the same library \
    **Snippet:**

      ```markdown
      # Holds

      How a member asks for an item that is out on loan, and how the item reaches them.

      ## Placing a Hold

      A member may place a hold on any item that is out on loan, at the desk or by telephone. A member may have three holds waiting at one time.

      No hold is placed on an item standing on the shelf: the member is told where it stands and fetches it.

      A hold costs nothing.

      ## The Queue

      Holds on one item are served in the order they were placed. Once somebody has asked for a book that is out, whoever has it cannot extend their time with it.

      What a waiting member means for the borrower who has the item is set out in `specs/library/loans.md § Renewals`.

      A housebound member's hold is served in its turn like any other.

      ## Collecting a Held Item

      When a held item comes back, a volunteer telephones the member at the head of the queue the same day.

      A held item is kept at the desk for seven days and then goes to the next member in the queue.

      The member collects the item with their own card, or sends a written note with whoever comes for it.

      ## Expired Holds

      A reservation not picked up within a week passes to whoever is next in line.

      A hold nobody has collected and nobody else waits for goes back to its shelf. A member who leaves three holds uncollected in a year is asked to place holds only in person.

      A hold on an item later withdrawn from stock is cancelled, and the member is told, as `specs/library/catalogue.md § Withdrawing an Item` has an item withdrawn.
      ```

  - **Fixture:** library-catalogue \
    **Holds:** a Markdown file on the record a community lending library keeps of what it holds, written to stand at `specs/library/catalogue.md`: sections on records, shelf marks, withdrawing an item and the stock check, six records of collections keyed by Name, and citations of the donations and opening files of the same library \
    **Snippet:**

      ```markdown
      # The Catalogue

      The record of what the library holds and where each item stands.

      ## Records

      Every item the library lends has one record in the catalogue, made before the item first goes on a shelf.

      A record holds the item's title, its author or maker, its shelf mark, its price when new and the date it was added. The catalogue is kept in a ledger at the desk, and a copy is made on the first Monday of each month and kept at the treasurer's house.

      The old card index is kept in the back room for local historians and no longer records what is in stock.

      **Records:**
        - **Name:** fiction \
          **Holds:** novels and short stories, shelved by the author's surname

        - **Name:** non-fiction \
          **Holds:** books of fact, shelved by subject number

        - **Name:** large-print \
          **Holds:** books in large type, shelved together by the door

        - **Name:** audio \
          **Holds:** audiobooks on disc, kept behind the desk

        - **Name:** film \
          **Holds:** films on disc, kept behind the desk

        - **Name:** local-history \
          **Holds:** maps, parish records and photographs, read in the library only

      ## Shelf Marks

      Every item carries its shelf mark on a label at the foot of its spine. Fiction is marked with the first three letters of the author's surname, and non-fiction with a subject number.

      A label that has faded is rewritten when the item is next returned, before it is shelved.

      An item found on the wrong shelf is moved to its own, and no note is made of it.

      ## Withdrawing an Item

      An item is withdrawn when it is too worn to lend, out of date, or has not been borrowed in five years.

      An item withdrawn from stock is struck from the catalogue the same day.

      A withdrawn item is stamped inside its cover and goes to the book sale, as `specs/library/donations.md § The Book Sale` runs it.

      Nothing from the local history collection is withdrawn without the committee's vote.

      ## Stock Check

      Each shelf is counted once a year against the catalogue, and an item missing at two counts running is marked lost.

      The stock check is made in the first week of February, when the library is closed to members, as `specs/library/opening.md § Closures` lists.

      Two volunteers check each shelf together, one reading the shelf and one reading the catalogue. An item on the shelf with no record is given one, and the catalogue is not altered in any other way during the check.
      ```
