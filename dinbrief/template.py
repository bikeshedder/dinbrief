# -*- coding: utf-8 -*-

from xml.sax.saxutils import escape

from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Frame
from reportlab.platypus import PageTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import KeepInFrame
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .constants import PAGE_SIZE, PAGE_WIDTH, PAGE_HEIGHT
from .constants import CONTENT_LEFT, CONTENT_WIDTH
from .styles import styles


# Address according to DIN 676 und DIN 5008
ADDRESS_WIDTH = 85*mm
ADDRESS_HEIGHT = 55*mm
ADDRESS_X = CONTENT_LEFT # correct would be 20mm, but this looks very strange
ADDRESS_Y = PAGE_HEIGHT - ADDRESS_HEIGHT - 45*mm - 3*mm

SENDER_X = ADDRESS_X
SENDER_Y = ADDRESS_Y + ADDRESS_HEIGHT - 13*mm
SENDER_HEIGHT = 10*mm
SENDER_WIDTH = ADDRESS_WIDTH

SENDER_LINE_Y = PAGE_HEIGHT - 55*mm
SENDER_LINE_COLOR = colors.black
SENDER_LINE_WIDTH = 0.1*mm

RECIPIENT_X = ADDRESS_X
RECIPIENT_Y = ADDRESS_Y
RECIPIENT_HEIGHT = ADDRESS_HEIGHT - 10*mm
RECIPIENT_WIDTH = PAGE_WIDTH - ADDRESS_X

DATE_Y = 45*mm
DATE_HEIGHT = PAGE_HEIGHT-140*mm


class BasePageTemplate(PageTemplate, object):

    def __init__(self, document, *args, **kwargs):
        self.document = document
        super(BasePageTemplate, self).__init__(
            *args, **kwargs)

    def afterDrawPage(self, canvas, document):
        self.draw_header(canvas)
        self.draw_footer(canvas)
        self.draw_marks(canvas)

    def draw_header(self, canvas):
        pass

    def draw_marks(self, canvas):
        canvas.saveState()
        canvas.setLineWidth(0.1*mm)

        # upper fold mark
        p = canvas.beginPath()
        p.moveTo(4*mm, PAGE_HEIGHT-105*mm)
        p.lineTo(8*mm, PAGE_HEIGHT-105*mm)
        canvas.drawPath(p)

        # lower fold mark
        p = canvas.beginPath()
        p.moveTo(4*mm, PAGE_HEIGHT-210*mm)
        p.lineTo(8*mm, PAGE_HEIGHT-210*mm)
        canvas.drawPath(p)

        # center mark
        p = canvas.beginPath()
        p.moveTo(6*mm, PAGE_HEIGHT / 2)
        p.lineTo(13*mm, PAGE_HEIGHT / 2)
        canvas.drawPath(p)

        canvas.restoreState()

    def draw_footer(self, canvas):
        pass

    
class FirstPageTemplate(BasePageTemplate):

    def __init__(self, document):
        super(FirstPageTemplate, self).__init__(
            document=document,
            id='First', frames=[
                # left=25mm, right=10mm, top=115mm, bottom=15mm
                Frame(
                    x1=CONTENT_LEFT, y1=45*mm,
                    width=CONTENT_WIDTH, height=PAGE_HEIGHT-140*mm,
                    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
            ])

    def draw_address(self, canvas):

        '''
        canvas.saveState()

        # sender line
        canvas.setStrokeColor(SENDER_LINE_COLOR)
        canvas.setLineWidth(SENDER_LINE_WIDTH)
        p = canvas.beginPath()
        p.moveTo(0, SENDER_LINE_Y)
        p.lineTo(PAGE_WIDTH, SENDER_LINE_Y)
        canvas.drawPath(p)

        canvas.restoreState()
        '''

        # sender text
        sender = Frame(
                SENDER_X, SENDER_Y,
                SENDER_WIDTH, SENDER_HEIGHT,
                0, 0, 0, 0)
        sender.add(
                Paragraph(
                    u' · '.join(map(escape, self.document.sender)),
                    styles['Sender']),
                canvas)

        # recipient text
        recipient = Frame(
                RECIPIENT_X, RECIPIENT_Y,
                RECIPIENT_WIDTH, RECIPIENT_HEIGHT,
                0, 0, 0, 0)
        recipient.add(
                Paragraph(
                    u'<br/>'.join(map(escape, self.document.recipient)),
                    styles['Recipient']),
                canvas)

    def draw_date(self, canvas):
        frame = Frame(
                CONTENT_LEFT, DATE_Y,
                CONTENT_WIDTH, DATE_HEIGHT,
                0, 0, 0, 0)
        frame.add(
                Paragraph(
                    escape(self.document.date),
                    styles['Date']),
                canvas)


    def afterDrawPage(self, canvas, document):
        BasePageTemplate.afterDrawPage(self, canvas, document)
        self.draw_address(canvas)
        self.draw_date(canvas)


class LaterPageTemplate(BasePageTemplate):

    def __init__(self, document):
        super(LaterPageTemplate, self).__init__(
                document=document,
                id='Later', frames=[
                    # left=20mm, right=10mm, top=20mm, bottom=15mm
                    Frame(25*mm, 40*mm, PAGE_WIDTH-35*mm, PAGE_HEIGHT-90*mm)
                ])


class BriefTemplate(platypus.BaseDocTemplate):

    def __init__(self, fh, document):
        # super can not be used as BaseDocTemplate is an old style class.
        platypus.BaseDocTemplate.__init__(self,
            fh,
            pagesize=PAGE_SIZE,
            pageTemplates=[
                FirstPageTemplate(document),
                LaterPageTemplate(document)
            ],
            title=document.title,
            subject=document.subject,
            author=document.author,
            keywords=document.keywords,
            creator=document.creator
        )
    
    def handle_pageBegin(self):
        self._handle_pageBegin()
        self._handle_nextPageTemplate('Later')
