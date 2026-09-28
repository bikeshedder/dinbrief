from decimal import Decimal

from dinbrief.invoice import Invoice, Item

FOOD_VAT = Decimal("0.07")
DEFAULT_VAT = Decimal("0.19")


def test_item_totals():
    item = Item(price=Decimal("10.00"), quantity=3, discount=Decimal("0.1"))
    assert item.subtotal == Decimal("30.00")
    assert item.discount_percentage == Decimal("10.0")
    assert item.discount_amount == Decimal("3.000")
    assert item.total == Decimal("27.000")


def test_empty_invoice():
    invoice = Invoice()
    assert invoice.net == 0
    assert invoice.vat_items == []
    assert invoice.gross == 0


def test_vat_is_grouped_and_sorted_by_rate():
    invoice = Invoice(
        items=[
            Item(price=Decimal(100), vat_rate=DEFAULT_VAT),
            Item(price=Decimal(10), vat_rate=FOOD_VAT),
            Item(price=Decimal(50), vat_rate=DEFAULT_VAT),
            Item(price=Decimal(5)),
        ]
    )
    assert [(v.rate, v.amount) for v in invoice.vat_items] == [
        (FOOD_VAT, Decimal("0.70")),
        (DEFAULT_VAT, Decimal("28.50")),
    ]
    assert invoice.net == Decimal(165)
    assert invoice.gross == Decimal("194.20")


def test_vat_is_calculated_on_discounted_amount():
    invoice = Invoice(
        items=[Item(price=Decimal(100), discount=Decimal("0.1"), vat_rate=DEFAULT_VAT)]
    )
    assert invoice.net == Decimal(90)
    assert invoice.vat_items[0].amount == Decimal("17.10")
    assert invoice.gross == Decimal("107.10")


def test_vat_reflects_items_added_later():
    invoice = Invoice()
    invoice.items.append(Item(price=Decimal(100), vat_rate=DEFAULT_VAT))
    assert invoice.vat_items[0].amount == Decimal(19)
    assert invoice.gross == Decimal(119)


def test_title_items_do_not_affect_totals():
    invoice = Invoice(
        items=[
            Item(1, "Group", type="title"),
            Item(2, "Thing", price=Decimal(10), vat_rate=DEFAULT_VAT),
        ]
    )
    assert invoice.net == Decimal(10)
    assert invoice.gross == Decimal("11.90")
