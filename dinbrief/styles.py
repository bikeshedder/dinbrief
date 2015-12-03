from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import StyleSheet1
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER


styles = StyleSheet1()

styles.add(ParagraphStyle(
    name='Normal',
    fontName='Helvetica',
    fontSize=10,
    leading=12
))

styles.add(ParagraphStyle(
    name='InfoboxH1',
    parent=styles['Normal'],
    fontSize=16,
    leading=8,
    spaceAfter=10*mm))

styles.add(ParagraphStyle(
    name='InfoboxTitle',
    parent=styles['Normal'],
    fontSize=8,
    leading=8,
    spaceAfter=0.5*mm))

styles.add(ParagraphStyle(
    name='InfoboxText',
    parent=styles['Normal'],
    fontSize=10,
    leading=12,
    spaceAfter=2*mm))

styles.add(ParagraphStyle(
    name='InfoboxNotice',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    spaceBefore=4*mm,
    spaceAfter=4*mm))

styles.add(ParagraphStyle(
    name='Footer',
    fontSize=8,
    leading=9,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='FooterTitle',
    fontSize=7,
    leading=10,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='FooterText',
    fontSize=9,
    leading=10,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Sender',
    fontSize=8,
    leading=8,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Recipient',
    fontSize=12,
    leading=14,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Text',
    spaceBefore=2*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Subject',
    fontSize=12,
    leading=12,
    spaceAfter=8*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Date',
    alignment=TA_RIGHT,
    parent=styles['Subject']))

styles.add(ParagraphStyle(
    name='Greeting',
    spaceBefore=2*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Message',
    spaceBefore=2*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='H2',
    fontName='Helvetica-Bold',
    fontSize=10,
    spaceBefore=4*mm,
    spaceAfter=4*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='TableCell',
    fontSize=10,
    leading=10,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='TableHead',
    fontName='Helvetica-Bold',
    parent=styles['TableCell']))

styles.add(ParagraphStyle(
    name='TableHeadRight',
    alignment=TA_RIGHT,
    parent=styles['TableHead']))

styles.add(ParagraphStyle(
    name='TableNumber',
    alignment=TA_RIGHT,
    parent=styles['TableCell']))

styles.add(ParagraphStyle(
    name='TableTitle',
    fontName='Helvetica-Bold',
    parent=styles['TableCell']))

styles.add(ParagraphStyle(
    name='GrossTableCell',
    fontName='Helvetica-Bold',
    parent=styles['TableCell']))

styles.add(ParagraphStyle(
    name='GrossValueTableCell',
    alignment=TA_RIGHT,
    parent=styles['GrossTableCell']))

styles.add(ParagraphStyle(
    name='Terms',
    spaceAfter=2*mm,
    parent=styles['Normal']))

styles.add(ParagraphStyle(
    name='Closing',
    spaceBefore=8*mm,
    parent=styles['Text']))

styles.add(ParagraphStyle(
    name='Signature',
    parent=styles['Text']))

styles.add(ParagraphStyle(
    name='FieldLabel',
    parent=styles['Normal'],
    fontSize=8,
    spaceAfter=0))
