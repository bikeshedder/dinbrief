import datetime
import subprocess
import sys
from decimal import Decimal

from dinbrief.optional_django import date_format, number_format


def test_number_format() -> None:
    assert number_format(Decimal("1234.5"), 2) == "1234.50"
    assert number_format(Decimal("19.00")) == "19"
    assert number_format(Decimal("2.675"), 2) == "2.68"


def test_date_format() -> None:
    assert date_format(datetime.date(1970, 1, 1)) == "1970-01-01"


DJANGO = """
import datetime
from decimal import Decimal

from dinbrief.optional_django import date_format, gettext, number_format

import django
from django.conf import settings

settings.configure(INSTALLED_APPS=["dinbrief"], LANGUAGE_CODE="de")
django.setup()

print(gettext("Sum (gross)"))
print(number_format(Decimal("1234.5"), 2))
print(date_format(datetime.date(1970, 1, 1), "SHORT_DATE_FORMAT"))
"""


def test_django() -> None:
    # Settings are configured after importing dinbrief, which must still
    # result in Django being used.
    output = subprocess.run(
        [sys.executable, "-c", DJANGO],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert output == ["Summe (brutto)", "1234,50", "01.01.1970"]
