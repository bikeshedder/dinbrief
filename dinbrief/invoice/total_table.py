# -*- coding: utf-8 -*-

from decimal import Decimal
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from ..constants import CONTENT_WIDTH
from ..optional_django import ugettext as _
from ..optional_django import number_format
from ..styles import styles


def TotalTable(invoice):

    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 1*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
    ]

    col_widths = [0, 32*mm, 24*mm]
    col_widths[0] = CONTENT_WIDTH - sum(col_widths)

    if invoice.vat_items:
        net_row = 0
        vat_row = net_row+1
        gross_row = vat_row + len(invoice.vat_items)
        table_style += [
            ('BOTTOMPADDING', (0, gross_row-1), (-1, gross_row-1), 2*mm),
            #('TOPPADDING', (0, vat_row), (-1, gross_row), 1*mm),
            #('BOTTOMPADDING', (0, vat_row), (-1, gross_row), 1*mm),
            ('LINEABOVE', (0, net_row), (-1, net_row), 0.3*mm, colors.black),
            ('LINEABOVE', (1, gross_row), (-1, gross_row), 0.5*mm, colors.black),
        ]
        def data_generator():
            yield (
                Paragraph(u'', styles['TableCell']),
                Paragraph(_(u'Sum (net)'), styles['TableCell']),
                Paragraph(u'%s €' % number_format(invoice.net, 2),
                    styles['TableNumber']),
            )
            for vat_item in invoice.vat_items:
                yield (
                    Paragraph(u'', styles['TableCell']),
                    Paragraph((u'+%s%% ' % number_format(vat_item.rate * 100)) +
                        _('VAT'), styles['TableCell']),
                    Paragraph(u'%s €' % number_format(vat_item.amount, 2),
                        styles['TableNumber']),
                )
            yield (
                Paragraph(u'', styles['TableCell']),
                Paragraph(_(u'Sum (gross)'), styles['GrossTableCell']),
                Paragraph(u'%s €' % number_format(invoice.gross, 2),
                    styles['GrossValueTableCell']),
            )
    else:
        net_row = 0
        gross_row = 1
        table_style += [
            ('TOPPADDING', (0, net_row), (-1, net_row), 2*mm),
            ('BOTTOMPADDING', (0, net_row), (-1, net_row), 0),
            ('LINEABOVE', (0, net_row), (-1, net_row), 0.3*mm, colors.black),
            ('TOPPADDING', (0, gross_row), (-1, gross_row), 2*mm),
            ('LINEABOVE', (1, gross_row), (-1, gross_row), 0.5*mm, colors.black),
        ]
        def data_generator():
            yield (
                Spacer(0, 0),
                Spacer(0, 0),
                Spacer(0, 0),
            )
            yield (
                Paragraph(u'', styles['TableCell']),
                Paragraph(_(u'Sum (net)'), styles['GrossTableCell']),
                Paragraph(u'%s €' % number_format(invoice.gross, 2),
                    styles['GrossValueTableCell']),
            )

    return Table(
        data=list(data_generator()),
        colWidths=col_widths,
        style=TableStyle(table_style))
