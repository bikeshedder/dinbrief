# Use functions provided by django but do not depend on it.

try:
    from django.utils.translation import gettext
except ImportError:
    from gettext import gettext

try:
    from django.utils.formats import number_format
except ImportError:
    def number_format(value, decimal_places=''):
        return f'{value:.{decimal_places or 0}f}'

try:
    from django.utils.formats import date_format
except ImportError:
    def date_format(value, format=None):
        return f'{value}'


__all__ = ['date_format', 'gettext', 'number_format']
