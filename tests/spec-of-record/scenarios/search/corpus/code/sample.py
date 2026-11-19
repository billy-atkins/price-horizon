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
