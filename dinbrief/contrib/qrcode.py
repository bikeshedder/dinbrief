from __future__ import absolute_import

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Flowable
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing

from ..styles import styles


class QRCode(Flowable):

    def __init__(self, data, color=colors.black):
        Flowable.__init__(self)
        self.data = data
        self.widget = QrCodeWidget(data, barLevel='M')

    def wrap(self, availWidth, availHeight):
        size = min(availWidth, availHeight)
        size = max(size, 30*mm)
        self.width = self.height = size
        return (size, size)

    def draw(self):
        bounds = self.widget.getBounds()
        drawing = Drawing(
                self.width, self.height,
                transform=[self.width/bounds[2], 0, 0,
                           self.height/bounds[3], 0, 0])
        drawing.add(self.widget)
        renderPDF.draw(drawing, self.canv, 0, 0)
        self.widget.draw()

    # purpose: http://www.hettwer-beratung.de/sepa-spezialwissen/sepa-technische-anforderungen/sepa-purpose-codes-vs-dta-textschl%C3%BCssel/
    # SCVE = dienstleistungen
    @classmethod
    def sepa_credit_transfer(cls, account_holder, iban, bic, amount, reference,
            purpose='', currency='EUR', color=colors.black):
        '''
        Create QRCode object according to EPC069-12
        http://www.europeanpaymentscouncil.eu/knowledge_bank_detail.cfm?documents_id=607
        '''
        assert 1 <= len(account_holder) < 70
        assert len(currency) == 3
        assert len(bic) in (7, 11)
        assert ' ' not in bic
        assert 1 <= len(iban) <= 34
        assert ' ' not in iban
        assert len(purpose) <= 4
        assert len(reference) <= 35
        data = '\n'.join((
            # Service Tag
            'BCD',
            # Version
            '001',
            # Character set (1=utf-8)
            '1',
            # identification code
            'SCT',
            # BIC
            bic,
            # name
            account_holder,
            # IBAN
            iban,
            # Amount
            '%s%.2f' % (currency, amount),
            # Purpose
            purpose,
            # Reference
            reference,
            # Unstructured Remittance Information
            '',
            # Beneficiary to originator information
            ''))
        return cls(data, color)
