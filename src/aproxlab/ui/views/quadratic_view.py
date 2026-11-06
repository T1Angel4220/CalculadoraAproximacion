"""Ajuste cuadrático: coeficientes, ecuación, ŷ, residuos y SSE (guía §4)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
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
from aproxlab.ui.widgets.metric_card import MetricCard
from aproxlab.ui.widgets.table_fit import configure_report_table


class QuadraticView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel("Requiere n ≥ 3 y al menos tres valores distintos de x.")
        self._hint.setObjectName("Subtitle")
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}")
        eq_box = QFrame()
        eq_box.setObjectName("Card")
        eq_layout = QVBoxLayout(eq_box)
        eq_caption = QLabel("Ecuación polinomial obtenida")
        eq_caption.setObjectName("MetricName")
        eq_layout.addWidget(eq_caption)
        eq_layout.addWidget(self._math)

        self._cards = {
            "a0": MetricCard("a₀", "Primer coeficiente"),
            "a1": MetricCard("a₁", "Segundo coeficiente"),
            "a2": MetricCard("a₂", "Tercer coeficiente"),
            "sse": MetricCard("SSE", "Suma de cuadrados de los residuos"),
        }
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self._cards["a0"], 0, 0)
        grid.addWidget(self._cards["a1"], 0, 1)
        grid.addWidget(self._cards["a2"], 1, 0)
        grid.addWidget(self._cards["sse"], 1, 1)

        self._residuos_label = QLabel("Valores aproximados (ŷ) y residuos")
        self._residuos_label.setObjectName("Title")
        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(["x", "y", "ŷ aproximado", "residuo", "residuo²"])
        configure_report_table(self._table)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        layout.addWidget(self._hint)
        layout.addWidget(eq_box)
        layout.addLayout(grid)
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
        self._cards["a0"].set_value(fmt_number(coeffs[0]))
        self._cards["a1"].set_value(fmt_number(coeffs[1]))
        self._cards["a2"].set_value(fmt_number(coeffs[2]))
        self._cards["sse"].set_value(fmt_number(report.quadratic_metrics.sse))
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
