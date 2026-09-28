import datetime
import io
from decimal import Decimal

import pytest

from dinbrief.document import Document
from dinbrief.invoice import Invoice, Item, ItemTable
from dinbrief.template import BriefTemplate


@pytest.mark.parametrize(
    "item",
    [
        Item(1, "Thing", price=Decimal(1)),
        Item(1, "Thing", price=Decimal(1), date=datetime.date(1970, 1, 1)),
        Item(1, "Thing", price=Decimal(1), period="01.01.1970 - 31.01.1970"),
    ],
    ids=["no-date-or-period", "date", "period"],
)
def test_render(item: Item) -> None:
    template = BriefTemplate()
    invoice = Invoice(items=[item])
    document = Document(content=[ItemTable(template, invoice)])
    fh = io.BytesIO()
    template.render(document, fh)
    assert fh.getvalue().startswith(b"%PDF-")


def test_render_does_not_consume_content() -> None:
    template = BriefTemplate()
    invoice = Invoice(items=[Item(1, "Thing", price=Decimal(1))])
    content = [ItemTable(template, invoice)]
    document = Document(content=content)
    for _ in range(2):
        fh = io.BytesIO()
        template.render(document, fh)
    assert len(content) == 1
