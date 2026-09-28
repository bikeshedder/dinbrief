from decimal import Decimal

from .item import Item
from .vat_item import VatItem


class Invoice:
    def __init__(self, items: list[Item] | None = None, currency: str = "€"):
        self.items = items or []
        self.currency = currency

    def recalculate(self) -> None:
        # VAT items are computed on demand. This method is kept for
        # backwards compatibility.
        pass

    @property
    def vat_items(self) -> list[VatItem]:
        d: dict[Decimal, VatItem] = {}
        for item in self.items:
            if not item.vat_rate:
                continue
            try:
                vat_item = d[item.vat_rate]
            except KeyError:
                vat_item = VatItem(rate=item.vat_rate)
                d[item.vat_rate] = vat_item
            vat_item.amount += item.vat_rate * item.total
        return sorted(d.values(), key=lambda item: item.rate)

    @property
    def gross(self) -> Decimal:
        return self.net + sum(
            (vat_item.amount for vat_item in self.vat_items), Decimal(0)
        )

    @property
    def net(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal(0))
