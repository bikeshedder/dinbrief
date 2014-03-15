#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal

import dinbrief.template

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.platypus.flowables import KeepTogether
from reportlab.platypus.flowables import Spacer

from dinbrief.constants import CONTENT_WIDTH
from dinbrief.contrib.qrcode import QRCode
from dinbrief.document import Document
from dinbrief.invoice import Invoice, Item, ItemTable, TotalTable
from dinbrief.invoice import BankTransferForm
from dinbrief.styles import styles
from dinbrief.template import BriefTemplate


FOOD_VAT = Decimal('0.07')
DEFAULT_VAT = Decimal('0.19')

with open('test.pdf', 'wb') as fh:
    invoice = Invoice(
        items=[
            Item(1, u'Donut', price=Decimal('1.00'), vat_rate=FOOD_VAT, quantity=100),
            Item(2, u'Brezel', price=Decimal('0.50'), vat_rate=FOOD_VAT, quantity=200, discount=Decimal('0.25')),
            Item(3, u'Backautomat miete', price=Decimal('50'), vat_rate=DEFAULT_VAT, quantity=4, unit='Tag', period=u'04.08.2012 - 07.10.2012'),
            Item(4, u'Versicherungspauschale: Personenschäden bis 100.000 EUR, Sachschäden bis 50.000 EUR.', price=Decimal('30'), vat_rate=DEFAULT_VAT),
        ])
    document = Document(
        sender=[
            u'Musterfirma',
            u'Finkengasse 1',
            u'00000 Musterort'
        ],
        recipient=[
            u'Max Mustermann',
            u'Lärchenweg 22',
            u'00000 Musterort'
        ],
        date='1.1.1970',
        content=[
            Paragraph(u'Rechnung 2012-0815', styles['Subject']),
            #Paragraph(u'Sehr geehrter Herr Mustermann,', styles['Greeting']),
            #Paragraph(u'Hiermit möchten wir Ihnen nachfolgende Posten in Rechnung stellen:', styles['Message']),
            Spacer(CONTENT_WIDTH, 2*mm),
            ItemTable(invoice),
            TotalTable(invoice),
            Spacer(CONTENT_WIDTH, 10*mm),
            BankTransferForm(
                account_holder='Muster AG',
                iban='DE00000000000000000000',
                bic='XXXXDE00XXX',
                amount=Decimal('6.66'),
                reference='2012-0815'),
            QRCode.sepa_credit_transfer(
                account_holder='Muster AG',
                iban='DE00000000000000000000',
                bic='XXXXDE00XXX',
                amount=Decimal(invoice.gross),
                reference='2012-0815'),
        ])
    template = BriefTemplate(fh, document)
    template.build(document.content)
