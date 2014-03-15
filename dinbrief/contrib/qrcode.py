from __future__ import absolute_import

from functools import partial

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

from ..styles import styles


Head = partial(Paragraph, style=styles['TableHead'])
HeadRight = partial(Paragraph, style=styles['TableHeadRight'])
Cell = partial(Paragraph, style=styles['TableCell'])
Number = partial(Paragraph, style=styles['TableNumber'])


class QRCode(object):

    def __init__(self, data, color=colors.black):

        import qrcode
        code = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M)
        code.add_data(data)
        code.make()

        style = []
        col_widths = [1*mm] * code.modules_count
        self.table = Table(
            data=list(self._data(code)),
            colWidths=col_widths,
            rowHeights=col_widths,
            style=TableStyle(self._style(code, color)),
            repeatRows=0)

    def _style(self, code, color):
        modcount = code.modules_count
        for r in range(modcount):
            for c in range(modcount):
                if code.modules[r][c]:
                    yield ('BACKGROUND', (r, c), (r, c), color)
        yield ('NOSPLIT', (0, 0), (-1, -1))

    def _data(self, code):
        modcount = code.modules_count
        for r in range(modcount):
            yield [''] * modcount

    def __getattr__(self, name):
        return getattr(self.table, name)

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
