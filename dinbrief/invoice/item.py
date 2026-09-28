import datetime
from decimal import Decimal
from typing import Literal


class Item:
    def __init__(
        self,
        position: int | str = 0,
        text: str = "",
        period: str = "",
        date: datetime.date | None = None,
        price: Decimal = Decimal(0),
        unit: str = "",
        quantity: Decimal | int = Decimal(1),
        discount: Decimal = Decimal(0),
        vat_rate: Decimal = Decimal(0),
        type: Literal["item", "title"] = "item",
    ):
        self.position = position
        self.text = text
        self.period = period
        self.date = date
        self.price = price
        self.unit = unit
        self.quantity = quantity
        self.discount = discount
        self.vat_rate = vat_rate
        self.type = type

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity

    @property
    def discount_percentage(self) -> Decimal:
        return self.discount * 100

    @property
    def discount_amount(self) -> Decimal:
        return self.discount * self.subtotal

    @property
    def total(self) -> Decimal:
        return self.subtotal - self.discount_amount
