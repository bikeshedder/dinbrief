from decimal import Decimal


class VatItem:
    def __init__(self, rate, amount=Decimal(0)):
        self.rate = rate
        self.amount = amount
