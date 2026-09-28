from decimal import Decimal

from dinbrief.optional_django import date_format, number_format


def test_number_format():
    assert number_format(Decimal("1234.5"), 2) == "1234.50"
    assert number_format(Decimal("19.00")) == "19"
    assert number_format(Decimal("2.675"), 2) == "2.68"


def test_date_format():
    assert date_format("01.01.1970") == "01.01.1970"
