"""Ajuste lineal paso a paso (sumatorias, a0, a1, tabla de errores, Sr, St, r)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.core.regression.linear import LinearWorksheet
from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.metric_card import MetricCard
from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height


class LinearView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._hint = QLabel(
            "Ingrese pares (x, y) y pulse Ajustar. El cálculo es a mano (sin NumPy)."
        )
        self._hint.setObjectName("Subtitle")
        self._hint.setWordWrap(True)
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x")
        eq_box = QFrame()
        eq_box.setObjectName("Card")
        eq_layout = QVBoxLayout(eq_box)
        eq_caption = QLabel("Ecuación de la recta de ajuste")
        eq_caption.setObjectName("MetricName")
        eq_layout.addWidget(eq_caption)
        eq_layout.addWidget(self._math)

        self._interp = QLabel("")
        self._interp.setObjectName("WinnerText")
        self._interp.setWordWrap(True)
        interp_box = QFrame()
        interp_box.setObjectName("Winner")
        interp_layout = QVBoxLayout(interp_box)
        interp_title = QLabel("Interpretación de r")
        interp_title.setObjectName("Title")
        interp_layout.addWidget(interp_title)
        interp_layout.addWidget(self._interp)

        self._cards = {
            "a0": MetricCard("a₀", "Intersección"),
            "a1": MetricCard("a₁", "Pendiente"),
            "sr": MetricCard("Sr", "Suma de cuadrados de residuos"),
            "st": MetricCard("St", "Suma total de cuadrados"),
            "syx": MetricCard("Sy/x", "Error estándar del estimado"),
            "r2": MetricCard("r²", "Coeficiente de determinación"),
            "r": MetricCard("r", "Coeficiente de correlación"),
            "n": MetricCard("n", "Número de observaciones"),
        }
        grid = QGridLayout()
        grid.setSpacing(10)
        order = ("n", "a0", "a1", "sr", "st", "syx", "r2", "r")
        for i, key in enumerate(order):
            grid.addWidget(self._cards[key], i // 2, i % 2)

        self._sum_title = QLabel("1. Tabla de sumatorias")
        self._sum_title.setObjectName("Title")
        self._sums = QTableWidget(0, 4)
        self._sums.setHorizontalHeaderLabels(["x", "y", "x²", "xy"])
        configure_report_table(self._sums)
        self._sums.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._sums.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self._means = QLabel("")
        self._means.setObjectName("Analysis")
        self._means.setWordWrap(True)

        self._err_title = QLabel("4. Tabla de errores")
        self._err_title.setObjectName("Title")
        self._errors = QTableWidget(0, 5)
        self._errors.setHorizontalHeaderLabels(["x", "y", "ŷ", "e", "e²"])
        configure_report_table(self._errors)
        self._errors.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._errors.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        layout.addWidget(self._hint)
        layout.addWidget(eq_box)
        layout.addWidget(interp_box)
        layout.addLayout(grid)
        layout.addWidget(self._sum_title)
        layout.addWidget(self._sums)
        layout.addWidget(self._means)
        layout.addWidget(self._err_title)
        layout.addWidget(self._errors)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._math._latex, color=color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.linear
        ws = fit.worksheet
        a0 = float(fit.coefficients[0])
        a1 = float(fit.coefficients[1])
        self._hint.setText(
            f"Ajuste lineal por mínimos cuadrados · n = {int(report.x.size)}"
        )
        self._math.set_latex(rf"\hat{{y}} = {fmt_number(a0)} + ({fmt_number(a1)})\,x")
        if isinstance(ws, LinearWorksheet):
            self._fill_from_worksheet(ws)
            return
        metrics = report.linear_metrics
        self._cards["a0"].set_value(fmt_number(a0))
        self._cards["a1"].set_value(fmt_number(a1))
        self._cards["sr"].set_value(fmt_number(metrics.sse))
        self._cards["st"].set_value(fmt_number(metrics.sst))
        self._cards["syx"].set_value(fmt_number(metrics.std_error))
        self._cards["r2"].set_value(fmt_number(metrics.r_squared))
        self._cards["r"].set_value(fmt_number(metrics.correlation))
        self._cards["n"].set_value(str(int(report.x.size)))

    def _fill_from_worksheet(self, ws: LinearWorksheet) -> None:
        self._cards["n"].set_value(str(ws.n))
        self._cards["a0"].set_value(fmt_number(ws.a0))
        self._cards["a1"].set_value(fmt_number(ws.a1))
        self._cards["sr"].set_value(fmt_number(ws.sr))
        self._cards["st"].set_value(fmt_number(ws.st))
        self._cards["syx"].set_value(fmt_number(ws.syx))
        self._cards["r2"].set_value(fmt_number(ws.r_squared))
        self._cards["r"].set_value(fmt_number(ws.r))
        self._interp.setText(ws.r_interpretation)
        self._means.setText(
            "2. Medias:  "
            f"x̄ = Σx / n = {fmt_number(ws.sum_x)} / {ws.n} = {fmt_number(ws.mean_x)}    ·    "
            f"ȳ = Σy / n = {fmt_number(ws.sum_y)} / {ws.n} = {fmt_number(ws.mean_y)}\n"
            "3. Coeficientes:  "
            f"a₁ = (n Σxy − Σx Σy) / (n Σx² − (Σx)²) = {fmt_number(ws.a1)}    ·    "
            f"a₀ = ȳ − a₁ x̄ = {fmt_number(ws.a0)}"
        )
        rows = list(ws.error_rows)
        self._fill_table(
            self._sums,
            [[fmt_number(r.x), fmt_number(r.y), fmt_number(r.x2), fmt_number(r.xy)] for r in rows],
            [
                fmt_number(ws.sum_x),
                fmt_number(ws.sum_y),
                fmt_number(ws.sum_x2),
                fmt_number(ws.sum_xy),
            ],
        )
        self._fill_table(
            self._errors,
            [
                [
                    fmt_number(r.x),
                    fmt_number(r.y),
                    fmt_number(r.y_hat),
                    fmt_number(r.residual),
                    fmt_number(r.residual_sq),
                ]
                for r in rows
            ],
            ["", "", "", "Sr", fmt_number(ws.sr)],
        )

    def _fill_table(
        self,
        table: QTableWidget,
        body: list[list[str]],
        totals: list[str],
    ) -> None:
        table.setRowCount(len(body) + 1)
        for i, row in enumerate(body):
            for col, value in enumerate(row):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(i, col, item)
        last = len(body)
        for col, value in enumerate(totals):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            table.setItem(last, col, item)
        fit_table_height(table)
        if table.height() > 300:
            table.setFixedHeight(300)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
