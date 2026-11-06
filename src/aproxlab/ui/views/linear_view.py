"""Resultados del ajuste lineal por mínimos cuadrados."""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.metric_card import MetricCard


class LinearView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("Ajuste lineal")
        title.setObjectName("Title")
        self._empty = QLabel("Ingrese datos y pulse Calcular ajustes para ver la recta.")
        self._empty.setObjectName("Subtitle")
        self._equation = QLabel("")
        self._equation.setObjectName("Equation")
        self._cards = {
            "a0": MetricCard("Intersección (a0)"),
            "a1": MetricCard("Pendiente (a1)"),
            "sse": MetricCard("Suma de cuadrados de residuos (SSE)"),
            "sst": MetricCard("Suma total de cuadrados (SST)"),
            "syx": MetricCard("Error estándar del estimado (Syx)"),
            "r2": MetricCard("Coeficiente de determinación (R²)"),
            "r": MetricCard("Coeficiente de correlación (r)"),
        }
        grid = QGridLayout()
        for i, card in enumerate(self._cards.values()):
            grid.addWidget(card, i // 2, i % 2)

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.addWidget(title)
        inner_layout.addWidget(self._empty)
        inner_layout.addWidget(self._equation)
        inner_layout.addLayout(grid)
        inner_layout.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.linear
        metrics = report.linear_metrics
        self._empty.setText("Recta de mínimos cuadrados y = a0 + a1 x")
        self._equation.setText(fit.equation)
        self._cards["a0"].set_value(fmt_number(float(fit.coefficients[0])))
        self._cards["a1"].set_value(fmt_number(float(fit.coefficients[1])))
        self._cards["sse"].set_value(fmt_number(metrics.sse))
        self._cards["sst"].set_value(fmt_number(metrics.sst))
        self._cards["syx"].set_value(fmt_number(metrics.std_error))
        self._cards["r2"].set_value(fmt_number(metrics.r_squared))
        self._cards["r"].set_value(fmt_number(metrics.correlation))
