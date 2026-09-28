# Checked by the type checkers in CI, not executed by pytest. Makes sure
# users of the package see the intended types.
import datetime
from decimal import Decimal
from typing import IO

from reportlab.platypus import Image, Table
from typing_extensions import assert_type

from dinbrief.contrib.form import SignatureField, TwoSignaturesField
from dinbrief.contrib.qrcode import sepa_credit_transfer
from dinbrief.document import Document
from dinbrief.invoice import BankTransferForm, Invoice, Item, ItemTable, TotalTable
from dinbrief.invoice.vat_item import VatItem
from dinbrief.optional_django import date_format, gettext, number_format
from dinbrief.template import BriefTemplate

item = Item(1, "Thing", price=Decimal(1), date=datetime.date(1970, 1, 1))
assert_type(item.subtotal, Decimal)
assert_type(item.discount_amount, Decimal)
assert_type(item.total, Decimal)

invoice = Invoice([item])
assert_type(invoice.items, list[Item])
assert_type(invoice.vat_items, list[VatItem])
assert_type(invoice.net, Decimal)
assert_type(invoice.gross, Decimal)

template = BriefTemplate()
assert_type(ItemTable(template, invoice), Table)
assert_type(TotalTable(template, invoice), Table)
assert_type(
    BankTransferForm("Muster AG", "DE00", "XXXXDEXX", "ref", invoice.gross), Table
)
assert_type(
    sepa_credit_transfer("Muster AG", "DE00", "XXXXDEXX", Decimal(1), "ref"), Image
)

# Form fields are accepted as content
document = Document(
    content=[
        ItemTable(template, invoice),
        SignatureField(),
        TwoSignaturesField("left", "right"),
    ]
)


def render(fh: IO[bytes]) -> None:
    template.render(document, fh)
    template.render(document, "invoice.pdf")


assert_type(gettext("VAT"), str)
assert_type(number_format(Decimal(1), 2), str)
assert_type(date_format(datetime.date(1970, 1, 1)), str)

# Must be rejected by all type checkers. mypy (strict) and pyright report
# unused ignores, which would catch the annotation getting lost.
Item(price=1.5)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
