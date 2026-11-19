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
