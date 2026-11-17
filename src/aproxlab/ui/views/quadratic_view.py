"""Ajuste cuadrático paso a paso: sumatorias, sistema, Gauss-Jordan, Sr y r²."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QLabel,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.core.algebra import GaussStep
from aproxlab.core.regression.quadratic import QuadraticWorksheet
from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.widgets.formula_card import FormulaCard
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height


def _tex(value: float | None) -> str:
    return fmt_number(value)


class QuadraticView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._ink = "#e7ecf3"
        self._hint = QLabel("Requiere n ≥ 3 y al menos tres valores distintos de x.")
        self._hint.setObjectName("Subtitle")
        self._hint.setWordWrap(True)
        self._math = MathLabel(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}")
        eq_box = QFrame()
        eq_box.setObjectName("Card")
        eq_layout = QVBoxLayout(eq_box)
        eq_layout.setContentsMargins(16, 14, 16, 14)
        eq_caption = QLabel("Ecuación de la parábola")
        eq_caption.setObjectName("MetricName")
        eq_layout.addWidget(eq_caption)
        eq_layout.addWidget(self._math)

        self._sum_title = QLabel("1. Tabla de sumatorias")
        self._sum_title.setObjectName("Title")
        self._sums = self._make_table(["x", "y", "x²", "x³", "x⁴", "xy", "x²y"])

        self._system = FormulaCard("2 y 3. Ecuaciones normales y matriz aumentada")
        self._matrix = self._make_table(["a₀", "a₁", "a₂", "término"])

        self._gauss_title = QLabel("4. Gauss-Jordan, operación por operación")
        self._gauss_title.setObjectName("Title")
        self._gauss_host = QWidget()
        self._gauss_layout = QVBoxLayout(self._gauss_host)
        self._gauss_layout.setContentsMargins(0, 0, 0, 0)
        self._gauss_layout.setSpacing(12)

        self._matrix_visible = True
        self._matrix_btn = QPushButton("Ocultar cálculo de la matriz")
        self._matrix_btn.setEnabled(False)
        self._matrix_btn.clicked.connect(self._toggle_matrix)
        self._matrix_box = QWidget()
        matrix_layout = QVBoxLayout(self._matrix_box)
        matrix_layout.setContentsMargins(0, 0, 0, 0)
        matrix_layout.setSpacing(16)
        matrix_layout.addWidget(self._system)
        matrix_layout.addWidget(self._matrix)
        matrix_layout.addWidget(self._gauss_title)
        matrix_layout.addWidget(self._gauss_host)

        self._coeffs = FormulaCard("5. Coeficientes de la parábola")
        self._err_title = QLabel("6. Tabla de errores")
        self._err_title.setObjectName("Title")
        self._errors = self._make_table(["xᵢ", "yᵢ", "ŷᵢ", "eᵢ = yᵢ − ŷᵢ", "eᵢ²"])

        self._sr = FormulaCard("7. Suma de residuos Sr")
        self._st = FormulaCard("8. Suma total St")
        self._syx = FormulaCard("9. Error estándar Sy/x")
        self._r2 = FormulaCard("10. Coeficiente de determinación r²")
        self._note = QLabel("")
        self._note.setObjectName("WinnerText")
        self._note.setWordWrap(True)
        note_box = QFrame()
        note_box.setObjectName("Winner")
        note_layout = QVBoxLayout(note_box)
        note_layout.setContentsMargins(16, 14, 16, 14)
        note_title = QLabel("Lectura de r²")
        note_title.setObjectName("Title")
        note_layout.addWidget(note_title)
        note_layout.addWidget(self._note)

        self._step_cards = (self._system, self._coeffs, self._sr, self._st, self._syx, self._r2)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(16)
        layout.addWidget(self._hint)
        layout.addWidget(eq_box)
        layout.addWidget(self._sum_title)
        layout.addWidget(self._sums)
        layout.addWidget(self._matrix_btn)
        layout.addWidget(self._matrix_box)
        layout.addWidget(self._coeffs)
        layout.addWidget(self._err_title)
        layout.addWidget(self._errors)
        for card in (self._sr, self._st, self._syx, self._r2):
            layout.addWidget(card)
        layout.addWidget(note_box)

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
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return table

    def clear(self) -> None:
        self._hint.setText("Requiere n ≥ 3 y al menos tres valores distintos de x.")
        self._math.set_latex(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}", color=self._ink)
        self._sums.setRowCount(0)
        self._matrix.setRowCount(0)
        self._errors.setRowCount(0)
        self._show_gauss(())
        self._matrix_btn.setEnabled(False)
        for card in self._step_cards:
            card.clear()
        self._note.setText("")

    def _toggle_matrix(self) -> None:
        self._matrix_visible = not self._matrix_visible
        self._matrix_box.setVisible(self._matrix_visible)
        if self._matrix_visible:
            self._matrix_btn.setText("Ocultar cálculo de la matriz")
        else:
            self._matrix_btn.setText("Mostrar cálculo de la matriz")

    def set_ink(self, color: str) -> None:
        self._ink = color
        self._math.set_latex(self._math._latex, color=color)
        for card in self._step_cards:
            card.set_ink(color)

    def show_report(self, report: AnalysisReport) -> None:
        fit = report.quadratic
        coeffs = [float(c) for c in fit.coefficients]
        self._hint.setText(f"Ajuste polinomial de segundo grado · n = {int(report.x.size)}")
        self._math.set_latex(
            rf"\hat{{y}} = {fmt_number(coeffs[0])}"
            rf" + ({fmt_number(coeffs[1])})\,x"
            rf" + ({fmt_number(coeffs[2])})\,x^{{2}}",
            color=self._ink,
        )
        ws = fit.worksheet
        if isinstance(ws, QuadraticWorksheet):
            self._fill_from_worksheet(ws)
            self._matrix_btn.setEnabled(True)

    def _fill_from_worksheet(self, ws: QuadraticWorksheet) -> None:
        rows = list(ws.power_rows)
        self._fill_table(
            self._sums,
            [
                [
                    _tex(r.x),
                    _tex(r.y),
                    _tex(r.x2),
                    _tex(r.x3),
                    _tex(r.x4),
                    _tex(r.xy),
                    _tex(r.x2y),
                ]
                for r in rows
            ],
            [
                _tex(ws.sum_x),
                _tex(ws.sum_y),
                _tex(ws.sum_x2),
                _tex(ws.sum_x3),
                _tex(ws.sum_x4),
                _tex(ws.sum_xy),
                _tex(ws.sum_x2y),
            ],
            show_sigma=True,
        )
        n, sx, sy = _tex(float(ws.n)), _tex(ws.sum_x), _tex(ws.sum_y)
        sx2, sx3, sx4 = _tex(ws.sum_x2), _tex(ws.sum_x3), _tex(ws.sum_x4)
        sxy, sx2y = _tex(ws.sum_xy), _tex(ws.sum_x2y)
        self._system.set_step(
            formula=(r"n a_0 + \sum x\,a_1 + \sum x^2 a_2 = \sum y"),
            substitution=(
                f"{n} a₀ + {sx} a₁ + {sx2} a₂ = {sy}\n"
                f"{sx} a₀ + {sx2} a₁ + {sx3} a₂ = {sxy}\n"
                f"{sx2} a₀ + {sx3} a₁ + {sx4} a₂ = {sx2y}"
            ),
            result="Matriz aumentada debajo",
        )
        self._fill_table(
            self._matrix,
            [[_tex(cell) for cell in row] for row in ws.augmented],
            None,
            show_sigma=False,
        )
        self._show_gauss(ws.gauss_steps)
        a0, a1, a2 = _tex(ws.a0), _tex(ws.a1), _tex(ws.a2)
        self._coeffs.set_step(
            formula=r"\hat{y} = a_0 + a_1 x + a_2 x^2",
            substitution=(
                "La última columna de la matriz identidad es a₀, a₁, a₂.\n"
                f"ŷ = {a0} + ({a1}) x + ({a2}) x²"
            ),
            result=f"a₀ = {a0}    a₁ = {a1}    a₂ = {a2}",
        )
        errors = list(ws.error_rows)
        sum_yhat = sum(row.y_hat for row in errors)
        sum_e = sum(row.residual for row in errors)
        self._fill_table(
            self._errors,
            [
                [
                    _tex(row.x),
                    _tex(row.y),
                    _tex(row.y_hat),
                    _tex(row.residual),
                    _tex(row.residual_sq),
                ]
                for row in errors
            ],
            [
                _tex(ws.sum_x),
                _tex(ws.sum_y),
                _tex(sum_yhat),
                _tex(sum_e),
                _tex(ws.sr),
            ],
            show_sigma=True,
        )
        sr, st = _tex(ws.sr), _tex(ws.st)
        first_sq = _tex(errors[0].residual_sq) if errors else "0"
        last_sq = _tex(errors[-1].residual_sq) if errors else "0"
        self._sr.set_step(
            formula=r"S_r = \sum (y_i - \hat{y}_i)^2",
            substitution=f"Sr = {first_sq} + ⋯ + {last_sq} = {sr}",
            result=f"Sr = {sr}",
        )
        self._st.set_step(
            formula=r"S_t = \sum (y_i - \bar{y})^2",
            substitution=(f"Mismos datos que la recta.  ȳ = {_tex(ws.mean_y)}.  St no cambia."),
            result=f"St = {st}",
        )
        if ws.syx is None:
            self._syx.set_step(
                formula=r"s_{y/x} = \sqrt{S_r / (n - 3)}",
                substitution="n ≤ 3 → no definido",
                result="Sy/x = —",
            )
        else:
            self._syx.set_step(
                formula=r"s_{y/x} = \sqrt{S_r / (n - 3)}",
                substitution=(f"Sy/x = √({sr} / ({n} − 3)) = {_tex(ws.syx)}"),
                result=f"Sy/x = {_tex(ws.syx)}",
            )
        if ws.r_squared is None:
            self._r2.set_step(
                formula=r"r^2 = (S_t - S_r) / S_t",
                substitution="St = 0 → no definido",
                result="r² = —",
            )
            self._note.setText("r² no está definido para estos datos.")
            return
        r2 = _tex(ws.r_squared)
        percent = _tex(ws.r_squared * 100)
        self._r2.set_step(
            formula=r"r^2 = (S_t - S_r) / S_t",
            substitution=f"r² = ({st} − {sr}) / {st} = {r2}",
            result=f"r² = {r2}",
        )
        self._note.setText(
            f"r² = {r2}. La parábola explica el {percent}% de la variabilidad. "
            "En el ajuste cuadrático se lee r², no el coeficiente de correlación lineal r."
        )

    def _show_gauss(self, steps: tuple[GaussStep, ...]) -> None:
        while self._gauss_layout.count():
            item = self._gauss_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        for index, step in enumerate(steps, start=1):
            box = QFrame()
            box.setObjectName("Card")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(14, 12, 14, 12)
            box_layout.setSpacing(8)
            title = QLabel(f"Operación {index}. {step.operation}")
            title.setObjectName("Analysis")
            title.setWordWrap(True)
            table = self._make_table(["a₀", "a₁", "a₂", "término"])
            self._fill_table(
                table,
                [[_tex(cell) for cell in row] for row in step.matrix],
                None,
                show_sigma=False,
            )
            box_layout.addWidget(title)
            box_layout.addWidget(table)
            self._gauss_layout.addWidget(box)

    def _fill_table(
        self,
        table: QTableWidget,
        body: list[list[str]],
        totals: list[str] | None,
        *,
        show_sigma: bool,
    ) -> None:
        extra = 1 if totals is not None else 0
        table.setRowCount(len(body) + extra)
        if show_sigma:
            table.verticalHeader().show()
            labels = [str(i + 1) for i in range(len(body))]
            if totals is not None:
                labels.append("Σ")
            table.setVerticalHeaderLabels(labels)
        else:
            table.verticalHeader().hide()
        for i, row in enumerate(body):
            for col, value in enumerate(row):
                _put(table, i, col, value, bold=False)
        if totals is not None:
            for col, value in enumerate(totals):
                _put(table, len(body), col, value, bold=True)
        fit_table_height(table)


def _put(table: QTableWidget, row: int, col: int, value: str, *, bold: bool) -> None:
    item = QTableWidgetItem(value)
    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    if bold:
        font = item.font()
        font.setBold(True)
        item.setFont(font)
    table.setItem(row, col, item)
