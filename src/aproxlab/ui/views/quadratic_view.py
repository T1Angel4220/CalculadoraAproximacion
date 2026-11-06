"""Resultados del polinomio de grado 2, con residuos en tabla."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
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

_ROWS = [
    ("a₀", "Término independiente"),
    ("a₁", "Coeficiente lineal"),
    ("a₂", "Coeficiente cuadrático"),
    ("SSE", "Suma de cuadrados de residuos"),
    ("Sᵧₓ", "Error estándar, ν = n − 3"),
    ("R²", "Coeficiente de determinación"),
]


class QuadraticView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel("Requiere n ≥ 3 y al menos tres x distintos.")
        self._hint.setObjectName("Subtitle")
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}")
        self._params = ParameterTable(_ROWS)
        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(["x", "y", "ŷ", "eᵢ", "eᵢ²"])
        self._table.verticalHeader().hide()
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.verticalHeader().setDefaultSectionSize(22)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addWidget(self._hint)
        layout.addWidget(self._math)
        layout.addWidget(self._params)
        layout.addWidget(QLabel("Residuos eᵢ = yᵢ − ŷᵢ"))
        layout.addWidget(self._table, 1)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._math._latex, color=color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.quadratic
        metrics = report.quadratic_metrics
        coeffs = [float(c) for c in fit.coefficients]
        self._hint.setText(f"MCO grado 2 · n = {report.x.size} · p = 3")
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
                fmt_number(metrics.sse),
                fmt_number(metrics.std_error),
                fmt_number(metrics.r_squared),
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
                self._table.setItem(i, col, QTableWidgetItem(value))
