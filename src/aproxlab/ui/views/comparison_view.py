"""Comparación de modelos en tabla de laboratorio."""

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


class ComparisonView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._verdict = QLabel("Sin modelos calculados.")
        self._verdict.setObjectName("Title")
        self._math = MathLabel(r"\min SSE,\quad SSE=\sum_i(y_i-\hat{y}_i)^2")
        self._table = QTableWidget(2, 7)
        self._table.setHorizontalHeaderLabels(["Modelo", "p", "ν", "SSE", "Sᵧₓ", "R²", "R²_adj"])
        self._table.verticalHeader().hide()
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setFixedHeight(24 * 2 + 32)
        self._note = QLabel(
            "El polinomio de grado 2 contiene a la recta (a₂ = 0). "
            "Menor SSE de entrenamiento no implica mejor predicción. "
            "Use Sᵧₓ y R² ajustado, que penalizan el parámetro extra."
        )
        self._note.setObjectName("Subtitle")
        self._note.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addWidget(self._verdict)
        layout.addWidget(self._math)
        layout.addWidget(self._table)
        layout.addWidget(self._note)
        layout.addStretch(1)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._math._latex, color=color)

    def show_report(self, report: AnalysisReport) -> None:
        winner = report.comparison.winner_name
        if winner == "Empate":
            self._verdict.setText("SSE idéntico: la parábola colapsa a la recta (a₂ ≈ 0).")
        else:
            self._verdict.setText(f"Menor SSE de entrenamiento: {winner}.")
        rows = [
            (report.linear.name, report.linear_metrics),
            (report.quadratic.name, report.quadratic_metrics),
        ]
        for i, (name, metrics) in enumerate(rows):
            values = [
                name,
                str(metrics.parameter_count),
                str(metrics.n - metrics.parameter_count),
                fmt_number(metrics.sse),
                fmt_number(metrics.std_error),
                fmt_number(metrics.r_squared),
                fmt_number(metrics.adjusted_r_squared),
            ]
            for col, value in enumerate(values):
                self._table.setItem(i, col, QTableWidgetItem(value))
