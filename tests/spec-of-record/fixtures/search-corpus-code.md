**Records:**
  - **Fixture:** ledger-python \
    **Holds:** a Python module with a class Ledger extending Base, a method that constructs a Receipt and calls append_entry, the same names inside a string and a comment, a canon-spec annotation over a constant and two app-spec annotations of `specs/target.md` over the class \
    **Snippet:**

      ```python
      """A sample of Python the search reads as code."""

      # @canon-spec specs/target.md § Table
      LIMIT = 3


      class Base:
          pass


      # @app-spec specs/target.md § Target
      # @app-spec specs/target.md § Target § Child
      class Ledger(Base):
          """Posts each entry exactly once."""

          def post(self, entry):
              text = "Fake() and calls_in_a_string()"  # calls_in_a_comment()
              receipt = Receipt(entry)
              return append_entry(receipt)


      class Receipt:
          def __init__(self, entry):
              self.entry = entry


      def append_entry(receipt):
          return receipt
      ```

  - **Fixture:** ledger-typescript \
    **Holds:** a TypeScript file with a class Ledger extending Base and implementing Auditable, a method that constructs a Receipt and calls appendEntry, the same names inside a string and a comment, and an app-spec annotation of `specs/target.md` over the class \
    **Snippet:**

      ```typescript
      interface Auditable {
        audit(): void;
      }

      class Base {}

      // @app-spec specs/target.md § Target
      export class Ledger extends Base implements Auditable {
        post(entry: Entry): Receipt {
          const text = "new Fake() and callsInAString()"; // callsInAComment()
          const receipt = new Receipt(entry);
          return appendEntry(receipt);
        }

        audit(): void {}
      }

      function appendEntry(receipt: Receipt): Receipt {
        return receipt;
      }
      ```

  - **Fixture:** ledger-csharp \
    **Holds:** a C# file with a class Ledger extending Base and implementing IAuditable, a method that constructs a Receipt and calls AppendEntry, the same names inside a string and a comment, and an app-spec annotation of `specs/target.md` over the class \
    **Snippet:**

      ```csharp
      namespace Sample;

      public class Base { }

      // @app-spec specs/target.md § Target § Child
      public class Ledger : Base, IAuditable
      {
          public Receipt Post(Entry entry)
          {
              var text = "new Fake() and CallsInAString()"; // CallsInAComment()
              var receipt = new Receipt(entry);
              return AppendEntry(receipt);
          }

          private Receipt AppendEntry(Receipt receipt)
          {
              return receipt;
          }
      }
      ```

  - **Fixture:** ledger-table-sql \
    **Holds:** an SQL file creating one table under an app-spec annotation of `specs/target.md § Table` \
    **Snippet:**

      ```sql
      -- @app-spec specs/target.md § Table
      create table ledger_entry (id integer primary key);
      ```

  - **Fixture:** ledger-settings-yaml \
    **Holds:** a YAML file of one setting under an app-spec annotation of `specs/target.md § Target` \
    **Snippet:**

      ```yaml
      # @app-spec specs/target.md § Target
      ledger:
        retries: 3
      ```
