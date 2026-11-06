"""Ajuste lineal: indicadores exigidos por la guía APE 04 §3."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.metric_card import MetricCard


class LinearView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel("Ingrese pares (x, y) y pulse Ajustar.")
        self._hint.setObjectName("Subtitle")
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x")
        eq_box = QFrame()
        eq_box.setObjectName("Card")
        eq_layout = QVBoxLayout(eq_box)
        eq_caption = QLabel("Ecuación de la recta de ajuste")
        eq_caption.setObjectName("MetricName")
        eq_layout.addWidget(eq_caption)
        eq_layout.addWidget(self._math)

        self._cards = {
            "a0": MetricCard("a₀", "Coeficiente de intersección"),
            "a1": MetricCard("a₁", "Pendiente"),
            "sse": MetricCard("SSE", "Suma de cuadrados de los residuos"),
            "sst": MetricCard("SST", "Suma total de cuadrados"),
            "syx": MetricCard("Syx", "Error estándar del estimado"),
            "r2": MetricCard("R²", "Coeficiente de determinación"),
            "r": MetricCard("r", "Coeficiente de correlación"),
        }
        grid = QGridLayout()
        grid.setSpacing(10)
        order = ("a0", "a1", "sse", "sst", "syx", "r2", "r")
        for i, key in enumerate(order):
            grid.addWidget(self._cards[key], i // 2, i % 2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        layout.addWidget(self._hint)
        layout.addWidget(eq_box)
        layout.addLayout(grid)
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
        self._cards["a0"].set_value(fmt_number(a0))
        self._cards["a1"].set_value(fmt_number(a1))
        self._cards["sse"].set_value(fmt_number(metrics.sse))
        self._cards["sst"].set_value(fmt_number(metrics.sst))
        self._cards["syx"].set_value(fmt_number(metrics.std_error))
        self._cards["r2"].set_value(fmt_number(metrics.r_squared))
        self._cards["r"].set_value(fmt_number(metrics.correlation))
