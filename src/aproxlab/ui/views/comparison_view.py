"""Comparación de lineal vs cuadrático (requisito 5 y 11 de la guía)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height


class ComparisonView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._verdict = QLabel("Mejor ajuste")
        self._verdict.setObjectName("Title")
        self._winner = QLabel("Calcule un ajuste para comparar los dos modelos.")
        self._winner.setObjectName("WinnerText")
        self._winner.setWordWrap(True)
        badge = QFrame()
        badge.setObjectName("Winner")
        badge_layout = QVBoxLayout(badge)
        badge_layout.addWidget(self._verdict)
        badge_layout.addWidget(self._winner)

        self._table = QTableWidget(2, 5)
        self._table.setHorizontalHeaderLabels(["Modelo", "Ecuación", "SSE (error)", "Syx", "R²"])
        configure_report_table(self._table)
        fit_table_height(self._table)

        self._analysis = QLabel("")
        self._analysis.setObjectName("Analysis")
        self._analysis.setWordWrap(True)
        self._analysis.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        layout.addWidget(badge)
        layout.addWidget(self._table)
        layout.addWidget(self._analysis)
        layout.addStretch(1)

    def set_ink(self, color: str) -> None:  # noqa: ARG002
        return

    def show_report(self, report: AnalysisReport) -> None:
        lin = report.linear
        quad = report.quadratic
        m_lin = report.linear_metrics
        m_quad = report.quadratic_metrics
        winner = report.comparison.winner_name

        rows = [
            [
                lin.name,
                lin.equation,
                fmt_number(m_lin.sse),
                fmt_number(m_lin.std_error),
                fmt_number(m_lin.r_squared),
            ],
            [
                quad.name,
                quad.equation,
                fmt_number(m_quad.sse),
                fmt_number(m_quad.std_error),
                fmt_number(m_quad.r_squared),
            ],
        ]
        for i, values in enumerate(rows):
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col >= 2:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                self._table.setItem(i, col, item)

        header = self._table.horizontalHeader()
        self._table.resizeColumnsToContents()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        fit_table_height(self._table)

        if winner == "Empate":
            self._winner.setText("Empate: mismo SSE. La parábola se reduce a la recta (a₂ ≈ 0).")
        else:
            self._winner.setText(f"El modelo {winner} presenta menor SSE para estos datos.")

        self._analysis.setText(
            _analysis_text(winner, m_lin.sse, m_quad.sse, m_lin.r_squared, m_quad.r_squared)
        )


def _analysis_text(
    winner: str,
    sse_lin: float,
    sse_quad: float,
    r2_lin: float | None,
    r2_quad: float | None,
) -> str:
    return (
        f"SSE lineal = {fmt_number(sse_lin)}   ·   SSE cuadrático = {fmt_number(sse_quad)}\n"
        f"R² lineal = {fmt_number(r2_lin)}   ·   R² cuadrático = {fmt_number(r2_quad)}\n\n"
        "El polinomio de grado 2 incluye a la recta como caso particular (a₂ = 0). "
        "Un SSE menor en la muestra no garantiza por sí solo mejor predicción fuera de ella. "
        f"Con los indicadores y la gráfica comparativa, el menor error de ajuste es: {winner}."
    )
