"""Comparación de modelos lineal y cuadrático."""

from __future__ import annotations

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


class ComparisonView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("Comparación de modelos")
        title.setObjectName("Title")
        self._empty = QLabel("Calcule los ajustes para identificar el modelo de menor error.")
        self._empty.setObjectName("Subtitle")
        self._empty.setWordWrap(True)
        self._winner = QLabel("")
        self._winner.setObjectName("Equation")
        self._caution = QLabel("")
        self._caution.setObjectName("Subtitle")
        self._caution.setWordWrap(True)
        self._table = QTableWidget(2, 5)
        self._table.setHorizontalHeaderLabels(["Modelo", "SSE", "Syx", "R²", "R² ajustado"])
        self._table.setVerticalHeaderLabels(["", ""])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self._empty)
        layout.addWidget(self._winner)
        layout.addWidget(self._table)
        layout.addWidget(self._caution)
        layout.addStretch()

    def show_report(self, report: AnalysisReport) -> None:
        comparison = report.comparison
        self._empty.setText(f"Criterio principal: menor {comparison.criterion} de entrenamiento.")
        if comparison.winner_name == "Empate":
            self._winner.setText("Empate: ambos modelos explican los datos con el mismo SSE.")
        else:
            self._winner.setText(f"Menor error de ajuste: {comparison.winner_name}.")
        self._caution.setText(comparison.caution)
        rows = [
            (report.linear.name, report.linear_metrics),
            (report.quadratic.name, report.quadratic_metrics),
        ]
        for i, (name, metrics) in enumerate(rows):
            values = [
                name,
                fmt_number(metrics.sse),
                fmt_number(metrics.std_error),
                fmt_number(metrics.r_squared),
                fmt_number(metrics.adjusted_r_squared),
            ]
            for col, value in enumerate(values):
                self._table.setItem(i, col, QTableWidgetItem(value))
