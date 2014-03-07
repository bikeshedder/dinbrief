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


def BankTransferForm(account_holder, iban, bic, reference, amount, currency=u'€'):

    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 1*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        ('NOSPLIT', (0, 0), (-1, -1)),
        # right
        ('RIGHTPADDING', (-1, 0), (-1, -1), 2*mm),
        ('LINEAFTER', (-1, 0), (-1, -1), 0.2*mm, colors.black),
        # left
        ('LEFTPADDING', (0, 0), (0, -1), 2*mm),
        ('LINEBEFORE', (0, 0), (0, -1), 0.2*mm, colors.black),
        # top
        ('TOPPADDING', (0, 0), (-1, 0), 2*mm),
        ('LINEABOVE', (0, 0), (-1, 0), 0.2*mm, colors.black),
        # bottom
        ('BOTTOMPADDING', (0, -1), (-1, -1), 3*mm),
        ('LINEBELOW', (0, -1), (-1, -1), 0.2*mm, colors.black),
    ]

    col_widths = [40*mm, 60*mm]

    def data_generator():
        yield (
            Paragraph(_(u'Account holder') + ':', styles['TableCell']),
            Paragraph(account_holder, styles['TableCell']),
        )
        yield (
            Paragraph(_(u'IBAN') + ':', styles['TableCell']),
            Paragraph(iban, styles['TableCell']),
        )
        yield (
            Paragraph(_(u'BIC') + ':', styles['TableCell']),
            Paragraph(bic, styles['TableCell']),
        )
        yield (
            Paragraph(_(u'Amount') + ':', styles['TableCell']),
            Paragraph(u'%s %s' % (number_format(amount), currency), styles['TableCell']),
        )
        yield (
            Paragraph(_(u'Reference') + ':', styles['TableCell']),
            Paragraph(reference, styles['TableCell']),
        )

    return Table(
        data=list(data_generator()),
        colWidths=col_widths,
        style=TableStyle(table_style),
        hAlign='LEFT')
