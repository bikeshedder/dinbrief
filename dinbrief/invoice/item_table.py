# -*- coding: utf-8 -*-

from decimal import Decimal
from functools import partial
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from ..constants import CONTENT_WIDTH
from ..optional_django import ugettext as _
from ..optional_django import number_format
from ..optional_django import date_format
from ..styles import styles


Head = partial(Paragraph, style=styles['TableHead'])
HeadRight = partial(Paragraph, style=styles['TableHeadRight'])
Cell = partial(Paragraph, style=styles['TableCell'])
Number = partial(Paragraph, style=styles['TableNumber'])


def ItemTable(invoice):

    style = [
        ('VALIGN', (0, 0), (-1,  0), 'BOTTOM'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
        ('LINEBELOW', (0, 0), (-1, 0), 0.3*mm, colors.black),
        #('LINEBELOW', (0, 1), (-1, -1), 0.1*mm, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        # no padding between net price and unit
        ('RIGHTPADDING', (3, 0), (3, -1), 0),
        ('LEFTPADDING', (4, 0), (4, -1), 0),
    ]

    show_period_column = any(item.period for item in invoice.items)
    show_date_column = any(item.date for item in invoice.items) and \
            not show_period_column

    col_widths = [
            8*mm, # position
            0,    # description
            46*mm if show_period_column else # period
            24*mm if show_date_column else # date
            0, # neither period nor date
            18*mm, # unit price
            10*mm, # unit
            14*mm, # quantity
            24*mm  # sum price
    ]
    col_widths[1] = CONTENT_WIDTH - sum(col_widths)

    def data_generator():
        # header
        yield (
            HeadRight(u'#'),
            Head(_('Description')),
            Head(_('Period') if show_period_column else
                 _('Date') if show_date_column else ''),
            HeadRight(_('Unit Price')),
            Head(u''),
            HeadRight(_('Quantity')),
            HeadRight(_('Line Total')),
        )
        # items
        row = 0
        for item in invoice.items:
            row += 1
            if not (item.period or item.date):
                style.append(('SPAN', (1, row), (2, row)))
            yield (
                Number(unicode(item.position)),
                Cell(escape(item.text)),
                Cell(escape(item.period) if item.period else
                     escape(date_format(item.date, 'SHORT_DATE_FORMAT')) if item.date else u''),
                Number(u'%s €' % number_format(item.price, 2)),
                Cell((u'/%s' % escape(item.get_unit_display()))
                    if item.unit else u''),
                Number(number_format(item.quantity, 2)),
                Number(u'%s €' % number_format(item.subtotal, 2)),
            )
            if item.discount:
                row += 1
                percentage = number_format(item.discount_percentage)
                yield (
                    Cell(u''),
                    Cell((u'%s%% ' % percentage) + _('discount')),
                    Cell(u''),
                    Cell(u''),
                    Cell(u''),
                    Cell(u''),
                    Number(u'–%s €' % number_format(item.discount_amount, 2)),
                )
                style.append(('TOPPADDING', (0, row), (-1, row), 0))
            # draw line below item
            style.append(('LINEBELOW', (0, row), (-1, row),
                0.1*mm, colors.black))

    return Table(
        data=list(data_generator()),
        colWidths=col_widths,
        style=TableStyle(style),
        repeatRows=1)
