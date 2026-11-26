"""The reading of FEEL expressions: a type `instance of` names, a name opening with no word FEEL keeps, a part a path
names on a date, and a call giving a function, FEEL's own or the canon's, what it takes; and the copies the checks
keep of FEEL's kept words, its built-in functions and the canon's functions, each held to its table where the texts
checked hold the file it stands in."""
import json

import pytest

import expressions
from audit_set import constructs, messages

HOME = "specs/methodology/expressions.md"
FEEL = "expressions.md § Expressions § FEEL"

pytestmark = [pytest.mark.reads("audit-feel-expressions.md", "bakery-facts-in-scope", "pickup-day-instance-of-date",
                                "pickup-day-instance-of-loaf", "loaves-in-stock-and-one", "in-stock-and-one",
                                "pickup-day-month", "pickup-day-hour", "crust-length", "crust-length-of-two",
                                "pickup-month-end", "pickup-day-two-business-days-on", "pickup-day-adjusted-sideways"),
              pytest.mark.reads("audit-feel-tables.md", "kept-words-listed-whole", "kept-words-listed-with-unless",
                                "built-in-functions-listed-whole", "built-in-functions-counting-in-words",
                                "calendar-functions-listed-whole", "calendar-functions-without-adjust")]


def checked(fixtures, key):
    """-> (kind, problems) of the fixture's expression, the bakery's facts in scope."""
    return expressions.check(fixtures[key], json.loads(fixtures["bakery-facts-in-scope"]))


def held_to_home(fixtures, key, rule):
    """-> the messages of the construct checks over the fixture placed at the file the copies are held to, of one rule."""
    found, _, _ = constructs.run_checks({HOME: fixtures[key]})
    return messages(found, rule)


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Values
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_instance_of_a_type_feel_names_passes(fixtures):
    assert checked(fixtures, "pickup-day-instance-of-date") == ("boolean", [])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Values
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_instance_of_a_type_feel_does_not_name_is_reported(fixtures):
    assert checked(fixtures, "pickup-day-instance-of-loaf") == ("boolean", ["no type FEEL names: loaf"])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Names
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_name_holding_a_kept_word_after_its_first_passes(fixtures):
    assert checked(fixtures, "loaves-in-stock-and-one") == ("number", [])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Names
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_name_opening_with_a_kept_word_is_reported(fixtures):
    assert checked(fixtures, "in-stock-and-one") == (
        None, ["an expression in no form FEEL has: a name opening with a word FEEL keeps: in"])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Names
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_kept_words_listed_as_the_copy_holds_them_pass(fixtures):
    assert held_to_home(fixtures, "kept-words-listed-whole", f"{FEEL} § Names") == []


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Names
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_kept_words_listed_out_of_step_with_the_copy_are_reported(fixtures):
    assert held_to_home(fixtures, "kept-words-listed-with-unless", f"{FEEL} § Names") == [
        "a word FEEL keeps the script's copy does not hold: unless",
        "a word the script keeps the file does not list: satisfies"]


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_part_a_date_holds_passes(fixtures):
    assert checked(fixtures, "pickup-day-month") == ("number", [])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_part_a_date_does_not_hold_is_reported(fixtures):
    assert checked(fixtures, "pickup-day-hour") == (None, ["a date holding no part named hour"])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Functions
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_built_in_call_given_what_it_takes_passes(fixtures):
    assert checked(fixtures, "crust-length") == ("number", [])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Functions
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_built_in_call_given_more_than_it_takes_is_reported(fixtures):
    assert checked(fixtures, "crust-length-of-two") == (
        "number", ["a call giving string length 2 arguments, which it does not take"])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Functions
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_built_in_functions_tabled_as_the_copy_holds_them_pass(fixtures):
    assert held_to_home(fixtures, "built-in-functions-listed-whole", f"{FEEL} § Its Functions") == []


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § Its Functions
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_built_in_function_tabled_out_of_step_with_the_copy_is_reported(fixtures):
    assert held_to_home(fixtures, "built-in-functions-counting-in-words", f"{FEEL} § Its Functions") == [
        "a function row the script's copy does not hold: ['count', 'list', 'string']",
        "a function row the table does not hold, of the script's copy: ['count', 'list', 'number']"]


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_canon_function_call_given_what_it_takes_passes(fixtures):
    assert checked(fixtures, "pickup-month-end") == ("date", [])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, problem", [
    ("pickup-day-two-business-days-on", "a call giving add business days 2 arguments, which it does not take"),
    ("pickup-day-adjusted-sideways", "a call giving adjust's convention a value it is not held to: SIDEWAYS"),
])
def test_a_canon_function_call_given_what_it_does_not_take_is_reported(fixtures, key, problem):
    assert checked(fixtures, key) == ("date", [problem])


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_canon_functions_tabled_as_the_copy_holds_them_pass(fixtures):
    assert held_to_home(fixtures, "calendar-functions-listed-whole", f"{FEEL} § The Canon's Functions") == []


# @canon-spec specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_canon_function_left_out_of_its_table_is_reported(fixtures):
    assert held_to_home(fixtures, "calendar-functions-without-adjust", f"{FEEL} § The Canon's Functions") == [
        "a function row the table does not hold, of the script's copy: ['adjust', 'day: date, convention: string, "
        "calendar: context<weekend: list<number>, holidays: list<date>>', 'date', '`convention`: `\"FOLLOWING\"`, "
        "`\"MODFOLLOWING\"`, `\"PRECEDING\"`, `\"MODPRECEDING\"`, `\"NONE\"`']"]
