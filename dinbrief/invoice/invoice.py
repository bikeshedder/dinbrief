from decimal import Decimal

from .vat_item import VatItem


class Invoice(object):

    def __init__(self, items=None, currency=u'€'):
        self.items = items or []
        self.currency = currency
        self.vat_items = []
        self.recalculate()

    def recalculate(self):
        self.vat_items = []
        d = {}
        for item in self.items:
            if not item.vat_rate:
                continue
            try:
                vat_item = d[item.vat_rate]
            except KeyError:
                vat_item = VatItem(rate=item.vat_rate)
                d[item.vat_rate] = vat_item
            vat_item.amount += item.vat_rate * item.subtotal
        self.vat_items = sorted(d.values(), key=lambda item: item.rate)

    @property
    def gross(self):
        return self.net + sum(vat_item.amount for vat_item in self.vat_items)

    @property
    def net(self):
        return sum(item.total for item in self.items)
