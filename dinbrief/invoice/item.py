from decimal import Decimal


class Item(object):

    def __init__(self, position=0, text='', period='', price=Decimal(0),
            unit='', quantity=Decimal(1), discount=Decimal(0),
            vat_rate=Decimal(0)):
        self.position = position
        self.text = text
        self.period = period
        self.price = price
        self.unit = unit
        self.quantity = quantity
        self.discount = discount
        self.vat_rate = vat_rate

    def get_unit_display(self):
        return self.unit

    @property
    def subtotal(self):
        return self.price * self.quantity

    @property
    def discount_percentage(self):
        return self.discount * 100

    @property
    def discount_amount(self):
        return self.discount * self.subtotal

    @property
    def total(self):
        return self.subtotal - self.discount_amount
