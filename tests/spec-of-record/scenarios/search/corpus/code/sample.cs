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
