"""Resultados del ajuste polinomial de segundo grado."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.metric_card import MetricCard


class QuadraticView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("Ajuste cuadrático")
        title.setObjectName("Title")
        self._empty = QLabel("Ingrese al menos tres puntos con x distintos y calcule los ajustes.")
        self._empty.setObjectName("Subtitle")
        self._equation = QLabel("")
        self._equation.setObjectName("Equation")
        self._cards = {
            "a0": MetricCard("a0"),
            "a1": MetricCard("a1"),
            "a2": MetricCard("a2"),
            "sse": MetricCard("SSE (residuos)"),
        }
        grid = QGridLayout()
        for i, card in enumerate(self._cards.values()):
            grid.addWidget(card, 0, i)

        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels(["x", "y", "ŷ", "residuo", "residuo²"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.addWidget(title)
        inner_layout.addWidget(self._empty)
        inner_layout.addWidget(self._equation)
        inner_layout.addLayout(grid)
        inner_layout.addWidget(QLabel("Valores aproximados y residuos"))
        inner_layout.addWidget(self._table)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.quadratic
        self._empty.setText("Polinomio y = a0 + a1 x + a2 x²")
        self._equation.setText(fit.equation)
        for i, key in enumerate(("a0", "a1", "a2")):
            self._cards[key].set_value(fmt_number(float(fit.coefficients[i])))
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
                self._table.setItem(i, col, QTableWidgetItem(value))
