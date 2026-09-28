from typing import TYPE_CHECKING, Any

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, Paragraph
from reportlab.platypus.tables import Table, TableStyle

from ..optional_django import gettext as _
from ..styles import styles

if TYPE_CHECKING:
    # Proxies can be used wherever reportlab expects a flowable.
    _FlowableProxyBase = Flowable
else:
    _FlowableProxyBase = object


class FlowableProxy(_FlowableProxyBase):
    flowable: Flowable

    def __getattr__(self, name: str) -> Any:
        return getattr(self.flowable, name)


class Field(FlowableProxy):
    field_height: float = 5 * mm

    def __init__(
        self, label: str, field_height: float | None = None, value: str | None = None
    ):
        if field_height is not None:
            self.field_height = field_height
        self.flowable = Table(
            data=[
                [value or ""],  # empty row for the text
                [Paragraph(label, styles["FieldLabel"])],
            ],
            colWidths=[80 * mm],
            rowHeights=[self.field_height, None],
            style=TableStyle(
                [
                    ("NOSPLIT", (0, 0), (-1, -1)),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("LINEBELOW", (0, 0), (0, 0), 0.2 * mm, colors.black),
                    # ('TOPPADDING', (0, 0), (0, 0), 5*mm),
                ]
            ),
            hAlign="LEFT",
        )


class SignatureField(Field):
    field_height = 15 * mm

    def __init__(
        self,
        label: str | None = None,
        field_height: float | None = None,
        value: str | None = None,
    ):
        if label is None:
            label = _("Place, date and signature")
        super().__init__(label, field_height, value)


class TwoSignaturesField(FlowableProxy):
    field_height: float = 15 * mm

    def __init__(
        self,
        label_left: str,
        label_right: str,
        field_height: float | None = None,
        value_left: str | None = None,
        value_right: str | None = None,
    ):
        if field_height is not None:
            self.field_height = field_height
        self.flowable = Table(
            data=[
                [value_left or "", "", value_right or ""],  # empty row for the text
                [
                    Paragraph(label_left, styles["FieldLabel"]),
                    "",
                    Paragraph(label_right, styles["FieldLabel"]),
                ],
            ],
            colWidths=[80 * mm, 10 * mm, 80 * mm],
            rowHeights=[self.field_height, None],
            style=TableStyle(
                [
                    ("NOSPLIT", (0, 0), (-1, -1)),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("LINEBELOW", (0, 0), (0, 0), 0.2 * mm, colors.black),
                    ("LINEBELOW", (2, 0), (2, 0), 0.2 * mm, colors.black),
                ]
            ),
            hAlign="LEFT",
        )


class PostalCodeAndCityField(FlowableProxy):
    field_height: float = 5 * mm

    def __init__(self) -> None:
        self.flowable = Table(
            data=[
                ["", "", ""],  # empty row for the text
                [
                    Paragraph(_("Postal code"), styles["FieldLabel"]),
                    "",  # Space between postal code and city
                    Paragraph(_("City"), styles["FieldLabel"]),
                ],
            ],
            colWidths=[20 * mm, 5 * mm, 55 * mm],
            rowHeights=[self.field_height, None],
            style=TableStyle(
                [
                    ("NOSPLIT", (0, 0), (-1, -1)),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("LINEBELOW", (0, 0), (0, 0), 0.2 * mm, colors.black),
                    ("LINEBELOW", (2, 0), (2, 0), 0.2 * mm, colors.black),
                ]
            ),
            hAlign="LEFT",
        )
