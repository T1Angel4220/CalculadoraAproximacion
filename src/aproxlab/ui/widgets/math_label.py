"""Etiqueta que renderiza LaTeX con mathtext de Matplotlib."""

from __future__ import annotations

from io import BytesIO

from matplotlib.mathtext import math_to_image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class MathLabel(QLabel):
    def __init__(
        self,
        latex: str = "",
        *,
        color: str = "#e7ecf3",
        dpi: int = 140,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._latex = latex
        self._color = color
        self._dpi = dpi
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        if latex:
            self.set_latex(latex, color=color)

    def set_latex(self, latex: str, *, color: str | None = None) -> None:
        self._latex = latex
        if color is not None:
            self._color = color
        expr = latex if "$" in latex else f"${latex}$"
        buf = BytesIO()
        try:
            math_to_image(expr, buf, dpi=self._dpi, format="png", color=self._color)
        except (ValueError, RuntimeError):
            self.setText(latex)
            return
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.setPixmap(pixmap)
        self.setMinimumHeight(pixmap.height())
