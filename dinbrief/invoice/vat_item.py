from decimal import Decimal


class VatItem:
    def __init__(self, rate: Decimal, amount: Decimal = Decimal(0)):
        self.rate = rate
        self.amount = amount
