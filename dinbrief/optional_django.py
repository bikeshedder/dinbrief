# Use functions provided by django but do not depend on it.

import datetime
import gettext as _gettext
from decimal import Decimal

try:
    from django.conf import settings as _django_settings
except ImportError:
    _django_settings = None


def _use_django() -> bool:
    # Django might be installed without being used, in which case
    # its settings are not configured. This is checked on every call
    # as the settings might be configured after importing this module.
    return _django_settings is not None and _django_settings.configured


def gettext(message: str) -> str:
    if _use_django():
        from django.utils.translation import gettext

        return str(gettext(message))
    return _gettext.gettext(message)


def number_format(value: Decimal | float, decimal_places: int | None = None) -> str:
    if _use_django():
        from django.utils.formats import number_format

        return str(number_format(value, decimal_places))
    return f"{value:.{decimal_places or 0}f}"


def date_format(value: datetime.date, format: str | None = None) -> str:
    if _use_django():
        from django.utils.formats import date_format

        return str(date_format(value, format))
    return f"{value}"
