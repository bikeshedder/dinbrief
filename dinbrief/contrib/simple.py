from functools import partial

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from ..styles import styles


P = partial(Paragraph, style=styles['Text'])
H2 = partial(Paragraph, style=styles['H2'])
Subject = partial(Paragraph, style=styles['Subject'])
SmallSpacer = partial(Spacer, width=0, height=5*mm)
MediumSpacer = partial(Spacer, width=0, height=10*mm)
LargeSpacer = partial(Spacer, width=0, height=20*mm)
