# -*- coding: utf-8 -*-

from decimal import Decimal
from functools import partial
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from ..optional_django import ugettext as _
from ..optional_django import number_format
from ..optional_django import date_format
from ..styles import styles


Head = partial(Paragraph, style=styles['TableHead'])
HeadRight = partial(Paragraph, style=styles['TableHeadRight'])
Cell = partial(Paragraph, style=styles['TableCell'])
Number = partial(Paragraph, style=styles['TableNumber'])
Title = partial(Paragraph, style=styles['TableTitle'])

title_bgcolor = colors.CMYKColor(black=0.1)


def ItemTable(brief_template, invoice):

    style = [
        ('VALIGN', (0, 0), (-1,  0), 'BOTTOM'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.3*mm, colors.black),
        #('LINEBELOW', (0, 1), (-1, -1), 0.1*mm, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2*mm),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3*mm),
        ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
        # no padding on the far left and far right
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
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
            21*mm, # unit price
            13*mm, # unit
            20*mm, # quantity
            26*mm  # sum price
    ]
    col_widths[1] = brief_template.CONTENT_WIDTH - sum(col_widths)

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
            item_type = getattr(item, 'type', 'item')
            if item_type == 'item':
                if not (item.period or item.date):
                    style.append(('SPAN', (1, row), (2, row)))
                yield (
                    Number(u'%s' % item.position),
                    Cell(escape(item.text)),
                    Cell(escape(item.period) if item.period else
                         escape(date_format(item.date, 'SHORT_DATE_FORMAT')) if item.date else u''),
                    Number(u'%s €' % number_format(item.price, 2)),
                    Cell((u'/%s' % escape(item.unit))
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
            elif item_type == 'title':
                style.append(('SPAN', (1, row), (6, row)))
                style.append(('BACKGROUND', (0, row), (-1, row),
                        title_bgcolor))
                style.append(('LINEBELOW', (0, row), (-1, row),
                        0.1*mm, colors.black))
                yield (
                    Number(u'%s' % item.position),
                    Title(escape(item.text)),
                )

    return Table(
        data=list(data_generator()),
        colWidths=col_widths,
        style=TableStyle(style),
        repeatRows=1)
