# Use functions provided by django but do not depend on it.

try:
    from django.utils.translation import gettext, ugettext
except:
    from gettext import gettext
    ugettext = gettext

try:
    from django.utils.formats import number_format
except:
    def number_format(value, decimal_places=''):
        format = '%%.%sf' % decimal_places
        return format % value
