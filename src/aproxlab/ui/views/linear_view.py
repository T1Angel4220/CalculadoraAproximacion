"""Ajuste lineal: indicadores exigidos por la guía APE 04 §3."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.parameter_table import ParameterTable

_ROWS = [
    ("Intersección", "Coeficiente a₀ (corte con y)"),
    ("Pendiente", "Coeficiente a₁"),
    ("Ecuación", "Recta de ajuste"),
    ("SSE", "Suma de cuadrados de los residuos"),
    ("SST", "Suma total de cuadrados"),
    ("Syx", "Error estándar del estimado"),
    ("R²", "Coeficiente de determinación"),
    ("r", "Coeficiente de correlación (Pearson x, y)"),
]


class LinearView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel("Sin ajuste. Ingrese pares (x, y) y pulse Ajustar (F5).")
        self._hint.setObjectName("Subtitle")
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x")
        self._table = ParameterTable(_ROWS)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self._hint)
        layout.addWidget(self._math)
        layout.addWidget(self._table)
        layout.addStretch(1)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._math._latex, color=color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.linear
        metrics = report.linear_metrics
        a0 = float(fit.coefficients[0])
        a1 = float(fit.coefficients[1])
        self._hint.setText(f"Ajuste lineal por mínimos cuadrados · n = {report.x.size}")
        self._math.set_latex(rf"\hat{{y}} = {fmt_number(a0)} + ({fmt_number(a1)})\,x")
        self._table.set_values(
            [
                fmt_number(a0),
                fmt_number(a1),
                fit.equation,
                fmt_number(metrics.sse),
                fmt_number(metrics.sst),
                fmt_number(metrics.std_error),
                fmt_number(metrics.r_squared),
                fmt_number(metrics.correlation),
            ]
        )
