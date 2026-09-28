# Use functions provided by django but do not depend on it.

import gettext as _gettext

try:
    from django.conf import settings as _django_settings
except ImportError:
    _django_settings = None


def _use_django():
    # Django might be installed without being used, in which case
    # its settings are not configured. This is checked on every call
    # as the settings might be configured after importing this module.
    return _django_settings is not None and _django_settings.configured


def gettext(message):
    if _use_django():
        from django.utils.translation import gettext

        return gettext(message)
    return _gettext.gettext(message)


def number_format(value, decimal_places=None):
    if _use_django():
        from django.utils.formats import number_format

        return number_format(value, decimal_places)
    return f"{value:.{decimal_places or 0}f}"


def date_format(value, format=None):
    if _use_django():
        from django.utils.formats import date_format

        return date_format(value, format)
    return f"{value}"
