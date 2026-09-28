#!/usr/bin/env python

from decimal import Decimal

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.platypus.flowables import Spacer

from dinbrief.contrib.form import SignatureField, TwoSignaturesField
from dinbrief.document import Document
from dinbrief.invoice import BankTransferForm, Invoice, Item, ItemTable, TotalTable
from dinbrief.styles import styles
from dinbrief.template import BriefTemplate

FOOD_VAT = Decimal('0.07')
DEFAULT_VAT = Decimal('0.19')

with open('test.pdf', 'wb') as fh:
    invoice = Invoice(
        items=[
            Item(1, 'Material', type='title'),
            Item(2, 'Donut', price=Decimal('1.00'), vat_rate=FOOD_VAT, quantity=100),
            Item(3, 'Brezel', price=Decimal('0.50'), vat_rate=FOOD_VAT, quantity=200, discount=Decimal('0.25')),
            Item(4, 'Backautomat miete', price=Decimal(50), vat_rate=DEFAULT_VAT, quantity=4, unit='Tag', period='04.08.2012 - 07.10.2012'),
            Item(5, 'Dienstleistungen und Versicherungen', type='title'),
            Item(6, 'Servicepauschale', price=Decimal(150), vat_rate=DEFAULT_VAT, quantity=3, unit='Monat', period='04.08.2012 - 03.12.2012'),
            Item(7, 'Versicherungspauschale: Personenschäden bis 100.000 EUR, Sachschäden bis 50.000 EUR.', price=Decimal(30), vat_rate=DEFAULT_VAT),
        ])
    template = BriefTemplate()
    document = Document(
        sender=[
            'Musterfirma',
            'Finkengasse 1',
            '00000 Musterort',
            'Extra Lange Adresse',
            'Die in zwei Zeilen umbricht',
        ],
        recipient=[
            'Adresse zurück',
            'Max Mustermann',
            'Raum 5',
            'Gebäude 1',
            'Lärchenweg 22',
            '00000 Musterort'
        ],
        date='1.1.1970',
        content=[
            Paragraph('Rechnung 2012-0815', styles['Subject']),
            #Paragraph(u'Sehr geehrter Herr Mustermann,', styles['Greeting']),
            #Paragraph(u'Hiermit möchten wir Ihnen nachfolgende Posten in Rechnung stellen:', styles['Message']),
            Spacer(template.CONTENT_WIDTH, 2*mm),
            ItemTable(template, invoice),
            TotalTable(template, invoice),
            Spacer(template.CONTENT_WIDTH, 10*mm),
            BankTransferForm(
                account_holder='Muster AG',
                iban='DE36 0000 0000 0000 0000 00',
                bic='XXXXDEXX',
                amount=invoice.gross,
                reference='2012-0815',
                show_qrcode=True),
            SignatureField('Default signature'),
            SignatureField('Big signature', 35*mm),
            SignatureField('Big signature', 35*mm),
            TwoSignaturesField('Signature1', 'Signature2'),
            TwoSignaturesField('Signature1', 'Signature2', value_left='Birstein, 01.01.1970', value_right='Hainburg 01.01.1970'),
        ]
    )
    template.render(document, fh)
