# dinbrief

[![Latest Version](https://img.shields.io/pypi/v/dinbrief.svg)](https://pypi.org/project/dinbrief/)
[![CI](https://img.shields.io/github/actions/workflow/status/bikeshedder/dinbrief/ci.yml?logo=github&label=CI)](https://github.com/bikeshedder/dinbrief/actions?query=workflow%3ACI)
![Typed](https://img.shields.io/badge/typing-typed-success.svg "Typed")
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-lightgray.svg "Python 3.10+")](https://www.python.org/downloads/)

This package provides code for rendering PDF letters and invoices
compliant to DIN 5008 and DIN 676 using reportlab. A so called
"DIN Brief" fits into "DIN-lang" window envelopes.

## Installation

```sh
pip install dinbrief
```

## Usage

```python
from decimal import Decimal

from reportlab.platypus import Paragraph

from dinbrief.document import Document
from dinbrief.invoice import Invoice, Item, ItemTable, TotalTable
from dinbrief.styles import styles
from dinbrief.template import BriefTemplate

invoice = Invoice(
    items=[
        Item(1, "Donut", price=Decimal("1.00"), quantity=100, vat_rate=Decimal("0.07")),
        Item(2, "Coffee", price=Decimal("2.50"), quantity=20, vat_rate=Decimal("0.19")),
    ]
)
template = BriefTemplate()
document = Document(
    sender=["Musterfirma", "Finkengasse 1", "00000 Musterort"],
    recipient=["Max Mustermann", "Lärchenweg 22", "00000 Musterort"],
    date="01.01.1970",
    content=[
        Paragraph("Invoice 1970-0001", styles["Subject"]),
        ItemTable(template, invoice),
        TotalTable(template, invoice),
    ],
)
with open("invoice.pdf", "wb") as fh:
    template.render(document, fh)
```

See [`examples/invoice.py`](examples/invoice.py) for a more complete example
including discounts, item groups, a bank transfer form with SEPA QR code and
signature fields.

## Translations

Labels are available in English and German. When used within a Django
project, Django's translation and formatting functions are used. Add
`dinbrief` to `INSTALLED_APPS` for the bundled German translations to be
found. Without Django labels are rendered in English.

## Development

```sh
uv sync
uv run pytest
uv run ruff check
uv run ruff format
uv check
```

## License

Licensed under any of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- BSD 2-Clause License ([LICENSE-BSD](LICENSE-BSD))
- MIT License ([LICENSE-MIT](LICENSE-MIT))

at your option.
