"""Ajuste cuadrático: coeficientes, ecuación, ŷ, residuos y SSE (guía §4)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.parameter_table import ParameterTable
from aproxlab.ui.widgets.table_fit import configure_report_table

_ROWS = [
    ("a₀", "Primer coeficiente"),
    ("a₁", "Segundo coeficiente"),
    ("a₂", "Tercer coeficiente"),
    ("Ecuación", "Polinomio obtenido"),
    ("SSE", "Suma de cuadrados de los residuos"),
]


class QuadraticView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel("Requiere n ≥ 3 y al menos tres valores distintos de x.")
        self._hint.setObjectName("Subtitle")
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}")
        self._params = ParameterTable(_ROWS)
        self._residuos_label = QLabel("Valores aproximados (ŷ) y residuos")
        self._residuos_label.setObjectName("Title")
        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(["x", "y", "ŷ aproximado", "residuo", "residuo²"])
        configure_report_table(self._table)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self._hint)
        layout.addWidget(self._math)
        layout.addWidget(self._params)
        layout.addWidget(self._residuos_label)
        layout.addWidget(self._table, 1)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._math._latex, color=color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.quadratic
        coeffs = [float(c) for c in fit.coefficients]
        self._hint.setText(f"Ajuste polinomial de segundo grado · n = {report.x.size}")
        self._math.set_latex(
            rf"\hat{{y}} = {fmt_number(coeffs[0])}"
            rf" + ({fmt_number(coeffs[1])})\,x"
            rf" + ({fmt_number(coeffs[2])})\,x^{{2}}"
        )
        self._params.set_values(
            [
                fmt_number(coeffs[0]),
                fmt_number(coeffs[1]),
                fmt_number(coeffs[2]),
                fit.equation,
                fmt_number(report.quadratic_metrics.sse),
            ]
        )
        n = report.x.size
        self._table.setRowCount(n)
        for i in range(n):
            residual = float(fit.residuals[i])
            values = [
                fmt_number(float(report.x[i])),
                fmt_number(float(report.y[i])),
                fmt_number(float(fit.y_hat[i])),
                fmt_number(residual),
                fmt_number(residual**2),
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self._table.setItem(i, col, item)
        self._table.resizeRowsToContents()
