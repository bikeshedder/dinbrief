from __future__ import absolute_import

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

import qrcode
from reportlab.platypus.flowables import Image

from ..styles import styles


def qrcode_image(data):
    # create QRCode object
    code = qrcode.QRCode(
            box_size=1,
            border=0,
            error_correction=qrcode.constants.ERROR_CORRECT_M)
    code.add_data(data)
    code.make()
    # render QRCode as PNG into memory
    img = code.make_image()
    img_data = BytesIO()
    img.save(img_data, 'PNG')
    img_data.seek(0)
    img_data.__repr__ = lambda: 'qrcode.png'
    # create image floatable
    return Image(img_data)


def sepa_credit_transfer(account_holder, iban, bic, amount, reference,
        purpose='', currency='EUR'):
    '''
    Create QRCode object according to EPC069-12:
    http://www.europeanpaymentscouncil.eu/knowledge_bank_detail.cfm?documents_id=607
    A list of purpose options can be found online:
    http://www.hettwer-beratung.de/sepa-spezialwissen/sepa-technische-anforderungen/sepa-purpose-codes-vs-dta-textschl%C3%BCssel/
    '''
    assert 1 <= len(account_holder) < 70
    assert len(currency) == 3
    assert len(bic) in (8, 11)
    assert ' ' not in bic
    assert 1 <= len(iban) <= 34
    assert ' ' not in iban
    assert len(purpose) <= 4
    assert len(reference) <= 35
    return qrcode_image('\n'.join((
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
        '')))
