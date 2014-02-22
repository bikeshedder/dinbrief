# -*- coding: utf-8 -*-

from decimal import Decimal
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from ..optional_django import ugettext as _
from ..styles import styles


class FlowableProxy(object):

    def __getattr__(self, name):
        return getattr(self.flowable, name)


class Field(FlowableProxy):
    field_height = 5*mm
    def __init__(self, label):
        self.flowable = Table(
            data=[
                [''], # empty row for the text
                [Paragraph(label, styles['FieldLabel'])],
            ],
            colWidths=[80*mm],
            rowHeights=[self.field_height, None],
            style=TableStyle([
                ('NOSPLIT', (0, 0), (-1, -1)),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('LINEBELOW', (0, 0), (0, 0), 0.2*mm, colors.black),
                #('TOPPADDING', (0, 0), (0, 0), 5*mm),
            ]),
            hAlign='LEFT'
        )


class SignatureField(Field):
    field_height = 15*mm

    def __init__(self):
        super(SignatureField, self).__init__(_('Place, date and signature'))


class PostalCodeAndCityField(FlowableProxy):
    field_height = 5*mm
    def __init__(self):
        self.flowable = Table(
            data=[
                ['', '', ''], # empty row for the text
                [
                    Paragraph(_('Postal code'), styles['FieldLabel']),
                    '', # Space between postal code and city
                    Paragraph(_('City'), styles['FieldLabel']),
                ],
            ],
            colWidths=[20*mm, 5*mm, 55*mm],
            rowHeights=[self.field_height, None],
            style=TableStyle([
                ('NOSPLIT', (0, 0), (-1, -1)),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('LINEBELOW', (0, 0), (0, 0), 0.2*mm, colors.black),
                ('LINEBELOW', (2, 0), (2, 0), 0.2*mm, colors.black),
            ]),
            hAlign='LEFT'
        )
