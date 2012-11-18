from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm


PAGE_SIZE = A4
PAGE_WIDTH = PAGE_SIZE[0]
PAGE_HEIGHT = PAGE_SIZE[1]

CONTENT_LEFT = 24.1*mm
CONTENT_RIGHT = 8.1*mm
CONTENT_WIDTH = PAGE_WIDTH - CONTENT_LEFT - CONTENT_RIGHT
