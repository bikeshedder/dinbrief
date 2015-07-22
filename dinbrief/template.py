# -*- coding: utf-8 -*-

from xml.sax.saxutils import escape

from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.platypus import Frame
from reportlab.platypus import PageTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import KeepInFrame
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from .styles import styles


class BasePageTemplate(PageTemplate, object):

    def __init__(self, brief_template, document, *args, **kwargs):
        self.brief_template = brief_template
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
        p.moveTo(4*mm, self.brief_template.PAGE_HEIGHT-105*mm)
        p.lineTo(8*mm, self.brief_template.PAGE_HEIGHT-105*mm)
        canvas.drawPath(p)

        # lower fold mark
        p = canvas.beginPath()
        p.moveTo(4*mm, self.brief_template.PAGE_HEIGHT-210*mm)
        p.lineTo(8*mm, self.brief_template.PAGE_HEIGHT-210*mm)
        canvas.drawPath(p)

        # center mark
        p = canvas.beginPath()
        p.moveTo(6*mm, self.brief_template.PAGE_HEIGHT / 2)
        p.lineTo(13*mm, self.brief_template.PAGE_HEIGHT / 2)
        canvas.drawPath(p)

        canvas.restoreState()

    def draw_footer(self, canvas):
        pass


class FirstPageTemplate(BasePageTemplate):

    def __init__(self, brief_template, document):
        super(FirstPageTemplate, self).__init__(
            brief_template=brief_template,
            document=document,
            id='First', frames=[
                # left=25mm, right=10mm, top=115mm, bottom=15mm
                Frame(
                    x1=brief_template.CONTENT_LEFT, y1=45*mm,
                    width=brief_template.CONTENT_WIDTH, height=brief_template.PAGE_HEIGHT-140*mm,
                    leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
            ])

    def draw_address(self, canvas):

        '''
        canvas.saveState()

        # sender line
        canvas.setStrokeColor(self.brief_template.SENDER_LINE_COLOR)
        canvas.setLineWidth(self.brief_template.SENDER_LINE_WIDTH)
        p = canvas.beginPath()
        p.moveTo(0, self.brief_template.SENDER_LINE_Y)
        p.lineTo(self.brief_template.PAGE_WIDTH, self.brief_template.SENDER_LINE_Y)
        canvas.drawPath(p)

        canvas.restoreState()
        '''

        # sender text
        sender = Frame(
                self.brief_template.SENDER_X, self.brief_template.SENDER_Y,
                self.brief_template.SENDER_WIDTH, self.brief_template.SENDER_HEIGHT,
                0, 0, 0, 0)
        sender.add(
                Paragraph(
                    u' · '.join(map(escape, self.document.sender)),
                    styles['Sender']),
                canvas)

        # recipient text
        recipient = Frame(
                self.brief_template.RECIPIENT_X, self.brief_template.RECIPIENT_Y,
                self.brief_template.RECIPIENT_WIDTH, self.brief_template.RECIPIENT_HEIGHT,
                0, 0, 0, 0)
        recipient.add(
                Paragraph(
                    u'<br/>'.join(map(escape, self.document.recipient)),
                    styles['Recipient']),
                canvas)

    def draw_infobox(self, canvas):
        infobox = Frame(
                self.brief_template.INFOBOX_X, self.brief_template.INFOBOX_Y,
                self.brief_template.INFOBOX_WIDTH, self.brief_template.INFOBOX_HEIGHT,
                0, 0, 0, 0)
        for floatable in self.document.infobox:
            infobox.add(floatable, canvas)

    def draw_date(self, canvas):
        frame = Frame(
                self.brief_template.CONTENT_LEFT, self.brief_template.DATE_Y,
                self.brief_template.CONTENT_WIDTH, self.brief_template.DATE_HEIGHT,
                0, 0, 0, 0)
        frame.add(
                Paragraph(
                    escape(self.document.date),
                    styles['Date']),
                canvas)

    def afterDrawPage(self, canvas, document):
        BasePageTemplate.afterDrawPage(self, canvas, document)
        self.draw_address(canvas)
        self.draw_infobox(canvas)
        self.draw_date(canvas)


class LaterPageTemplate(BasePageTemplate):

    def __init__(self, brief_template, document):
        super(LaterPageTemplate, self).__init__(
            brief_template=brief_template,
            document=document,
            id='Later', frames=[
                # left=20mm, right=10mm, top=20mm, bottom=15mm
                Frame(25*mm, 40*mm,
                    brief_template.PAGE_WIDTH-35*mm,
                    brief_template.PAGE_HEIGHT-90*mm)
            ])


class BriefDocTemplate(platypus.BaseDocTemplate):

    def __init__(self, brief_template, fh, document):
        # super can not be used as BaseDocTemplate is an old style class.
        platypus.BaseDocTemplate.__init__(self,
            fh,
            pagesize=brief_template.PAGE_SIZE,
            pageTemplates=[
                brief_template.get_first_page_template(document),
                brief_template.get_later_page_template(document)
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


class BriefTemplate(object):

    PAGE_SIZE = A4
    PAGE_WIDTH = PAGE_SIZE[0]
    PAGE_HEIGHT = PAGE_SIZE[1]

    CONTENT_LEFT = 24.1*mm
    CONTENT_RIGHT = 8.1*mm
    CONTENT_WIDTH = PAGE_WIDTH - CONTENT_LEFT - CONTENT_RIGHT

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

    INFOBOX_WIDTH = 85*mm
    INFOBOX_HEIGHT = 100*mm
    INFOBOX_X = PAGE_WIDTH - INFOBOX_WIDTH - CONTENT_RIGHT
    INFOBOX_Y = PAGE_HEIGHT - INFOBOX_HEIGHT - 20*mm

    DATE_Y = 45*mm
    DATE_HEIGHT = PAGE_HEIGHT-140*mm

    def render(self, document, fh):
        # FIXME add support for document lists
        document_template = BriefDocTemplate(self, fh, document)
        document_template.build(document.content)

    def get_first_page_template(self, document):
        return FirstPageTemplate(self, document)

    def get_later_page_template(self, document):
        return LaterPageTemplate(self, document)
