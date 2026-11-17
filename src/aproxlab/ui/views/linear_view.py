"""Ajuste lineal paso a paso (sumatorias, a0, a1, tabla de errores, Sr, St, r)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
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
from aproxlab.ui.widgets.formula_card import FormulaCard
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height


def _tex(value: float | None) -> str:
    return fmt_number(value)


class LinearView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._ink = "#e7ecf3"
        self._hint = QLabel(
            "Ingrese pares (x, y) y pulse Ajustar. El cálculo es a mano (sin NumPy)."
        )
        self._hint.setObjectName("Subtitle")
        self._hint.setWordWrap(True)
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x")
        eq_box = QFrame()
        eq_box.setObjectName("Card")
        eq_layout = QVBoxLayout(eq_box)
        eq_layout.setContentsMargins(16, 14, 16, 14)
        eq_layout.setSpacing(8)
        eq_caption = QLabel("Ecuación de la recta de ajuste")
        eq_caption.setObjectName("MetricName")
        eq_layout.addWidget(eq_caption)
        eq_layout.addWidget(self._math)

        self._sum_title = QLabel("1. Tabla de sumatorias")
        self._sum_title.setObjectName("Title")
        self._sums = self._make_table(["x", "y", "x²", "xy"])

        self._mean_x = FormulaCard("2. Media de x")
        self._mean_y = FormulaCard("2. Media de y")
        self._a1 = FormulaCard("3. Pendiente a₁")
        self._a0 = FormulaCard("3. Intersección a₀")

        self._err_title = QLabel("4. Tabla de errores")
        self._err_title.setObjectName("Title")
        self._err_note = QLabel(
            "ŷᵢ = a₀ + a₁xᵢ  (recta).  eᵢ = yᵢ − ŷᵢ.  ȳ es la media de y.  "
            "Sr = Σ eᵢ².  St = Σ(yᵢ − ȳ)²."
        )
        self._err_note.setObjectName("Subtitle")
        self._err_note.setWordWrap(True)
        self._errors = self._make_table(
            ["xᵢ", "yᵢ", "ŷᵢ", "eᵢ = yᵢ − ŷᵢ", "eᵢ²", "yᵢ − ȳ", "(yᵢ − ȳ)²"]
        )

        self._sr = FormulaCard("5. Suma de residuos Sr")
        self._st = FormulaCard("5. Suma total St")
        self._syx = FormulaCard("6. Error estándar Sy/x")
        self._r2 = FormulaCard("7. Coeficiente de determinación r²")
        self._r = FormulaCard("8. Coeficiente de correlación r")

        self._interp = QLabel("")
        self._interp.setObjectName("WinnerText")
        self._interp.setWordWrap(True)
        interp_box = QFrame()
        interp_box.setObjectName("Winner")
        interp_layout = QVBoxLayout(interp_box)
        interp_layout.setContentsMargins(16, 14, 16, 14)
        interp_layout.setSpacing(8)
        interp_title = QLabel("Interpretación de la correlación")
        interp_title.setObjectName("Title")
        interp_layout.addWidget(interp_title)
        interp_layout.addWidget(self._interp)

        self._step_cards = (
            self._mean_x,
            self._mean_y,
            self._a1,
            self._a0,
            self._sr,
            self._st,
            self._syx,
            self._r2,
            self._r,
        )

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(16)
        layout.addWidget(self._hint)
        layout.addWidget(eq_box)
        layout.addWidget(self._sum_title)
        layout.addWidget(self._sums)
        for card in (self._mean_x, self._mean_y, self._a1, self._a0):
            layout.addWidget(card)
        layout.addWidget(self._err_title)
        layout.addWidget(self._err_note)
        layout.addWidget(self._errors)
        for card in (self._sr, self._st, self._syx, self._r2, self._r):
            layout.addWidget(card)
        layout.addWidget(interp_box)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _make_table(self, headers: list[str]) -> QTableWidget:
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        configure_report_table(table)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return table

    def clear(self) -> None:
        self._hint.setText(
            "Ingrese pares (x, y) y pulse Ajustar. El cálculo es a mano (sin NumPy)."
        )
        self._math.set_latex(r"\hat{y} = a_0 + a_1 x", color=self._ink)
        self._sums.setRowCount(0)
        self._errors.setRowCount(0)
        for card in self._step_cards:
            card.clear()
        self._interp.setText("")

    def set_ink(self, color: str) -> None:
        self._ink = color
        self._math.set_latex(self._math._latex, color=color)
        for card in self._step_cards:
            card.set_ink(color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.linear
        ws = fit.worksheet
        a0 = float(fit.coefficients[0])
        a1 = float(fit.coefficients[1])
        self._hint.setText(f"Ajuste lineal por mínimos cuadrados · n = {int(report.x.size)}")
        self._math.set_latex(
            rf"\hat{{y}} = {fmt_number(a0)} + ({fmt_number(a1)})\,x",
            color=self._ink,
        )
        if isinstance(ws, LinearWorksheet):
            self._fill_from_worksheet(ws)

    def _fill_from_worksheet(self, ws: LinearWorksheet) -> None:
        n = _tex(float(ws.n))
        sx = _tex(ws.sum_x)
        sy = _tex(ws.sum_y)
        sx2 = _tex(ws.sum_x2)
        sxy = _tex(ws.sum_xy)
        mx = _tex(ws.mean_x)
        my = _tex(ws.mean_y)
        a0 = _tex(ws.a0)
        a1 = _tex(ws.a1)
        sr = _tex(ws.sr)
        st = _tex(ws.st)
        num = ws.n * ws.sum_xy - ws.sum_x * ws.sum_y
        den = ws.n * ws.sum_x2 - ws.sum_x * ws.sum_x
        rows = list(ws.error_rows)

        self._mean_x.set_step(
            formula=r"\bar{x} = \dfrac{\sum x}{n}",
            substitution=f"x̄ = Σx / n = {sx} / {n} = {mx}",
            result=f"x̄ = {mx}",
        )
        self._mean_y.set_step(
            formula=r"\bar{y} = \dfrac{\sum y}{n}",
            substitution=f"ȳ = Σy / n = {sy} / {n} = {my}",
            result=f"ȳ = {my}",
        )
        self._a1.set_step(
            formula=(
                r"a_1 = \dfrac{n\sum xy - \sum x\sum y}"
                r"{n\sum x^2 - (\sum x)^2}"
            ),
            substitution=(
                f"a₁ = (n Σxy − Σx Σy) / (n Σx² − (Σx)²)\n"
                f"a₁ = ({n} × {sxy} − {sx} × {sy}) / ({n} × {sx2} − {sx}²)\n"
                f"a₁ = {_tex(num)} / {_tex(den)} = {a1}"
            ),
            result=f"a₁ = {a1}",
        )
        self._a0.set_step(
            formula=r"a_0 = \bar{y} - a_1 \bar{x}",
            substitution=f"a₀ = ȳ − a₁ x̄ = {my} − ({a1}) × {mx} = {a0}",
            result=f"a₀ = {a0}",
        )

        first_sq = _tex(rows[0].residual_sq) if rows else "0"
        last_sq = _tex(rows[-1].residual_sq) if rows else "0"
        first_dev = _tex(rows[0].dev_mean_sq) if rows else "0"
        last_dev = _tex(rows[-1].dev_mean_sq) if rows else "0"

        self._sr.set_step(
            formula=r"S_r = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            substitution=f"Sr = {first_sq} + ⋯ + {last_sq} = {sr}",
            result=f"Sr = {sr}",
        )
        self._st.set_step(
            formula=r"S_t = \sum_{i=1}^{n}(y_i - \bar{y})^2",
            substitution=f"St = {first_dev} + ⋯ + {last_dev} = {st}",
            result=f"St = {st}",
        )

        if ws.syx is None:
            self._syx.set_step(
                formula=r"s_{y/x} = \sqrt{\dfrac{S_r}{n-2}}",
                substitution="n = 2 → no definido",
                result="Sy/x = —",
            )
        else:
            self._syx.set_step(
                formula=r"s_{y/x} = \sqrt{\dfrac{S_r}{n-2}}",
                substitution=(f"Sy/x = √(Sr / (n − 2)) = √({sr} / ({n} − 2)) = {_tex(ws.syx)}"),
                result=f"Sy/x = {_tex(ws.syx)}",
            )

        if ws.r_squared is None:
            self._r2.set_step(
                formula=r"r^2 = \dfrac{S_t - S_r}{S_t}",
                substitution="St = 0 → no definido",
                result="r² = —",
            )
            self._r.set_step(
                formula=r"r = \mathrm{signo}(a_1)\,\sqrt{r^2}",
                substitution="r² no definido",
                result="r = —",
            )
            self._interp.setText("r no está definido para estos datos.")
        else:
            r2 = _tex(ws.r_squared)
            rr = _tex(ws.r)
            self._r2.set_step(
                formula=r"r^2 = \dfrac{S_t - S_r}{S_t}",
                substitution=f"r² = (St − Sr) / St = ({st} − {sr}) / {st} = {r2}",
                result=f"r² = {r2}",
            )
            self._r.set_step(
                formula=r"r = \mathrm{signo}(a_1)\,\sqrt{r^2}",
                substitution=f"r = signo(a₁) × √(r²) = signo({a1}) × √({r2}) = {rr}",
                result=f"r = {rr}",
            )
            self._interp.setText(f"r = {rr}  →  {ws.r_interpretation}")

        self._fill_table(
            self._sums,
            [[_tex(r.x), _tex(r.y), _tex(r.x2), _tex(r.xy)] for r in rows],
            [_tex(ws.sum_x), _tex(ws.sum_y), _tex(ws.sum_x2), _tex(ws.sum_xy)],
        )
        sum_yhat = sum(r.y_hat for r in rows)
        sum_e = sum(r.residual for r in rows)
        sum_dev = sum(r.dev_mean for r in rows)
        self._fill_table(
            self._errors,
            [
                [
                    _tex(r.x),
                    _tex(r.y),
                    _tex(r.y_hat),
                    _tex(r.residual),
                    _tex(r.residual_sq),
                    _tex(r.dev_mean),
                    _tex(r.dev_mean_sq),
                ]
                for r in rows
            ],
            [
                _tex(ws.sum_x),
                _tex(ws.sum_y),
                _tex(sum_yhat),
                _tex(sum_e),
                _tex(ws.sr),
                _tex(sum_dev),
                _tex(ws.st),
            ],
        )

    def _fill_table(
        self,
        table: QTableWidget,
        body: list[list[str]],
        totals: list[str],
    ) -> None:
        table.verticalHeader().show()
        table.verticalHeader().setDefaultSectionSize(34)
        table.setRowCount(len(body) + 1)
        table.setVerticalHeaderLabels([str(i + 1) for i in range(len(body))] + ["Σ"])
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
        if table.height() > 340:
            table.setFixedHeight(340)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
