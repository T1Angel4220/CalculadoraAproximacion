"""Comparación visual de la recta y la parábola sobre los mismos datos."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from aproxlab.core.comparison import narrate_comparison
from aproxlab.core.metrics import FitMetrics
from aproxlab.services.analysis import AnalysisReport
from aproxlab.ui.widgets.math_label import MathLabel
from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height

_DIGITS = 4
_GOOD_DARK = "#4ade80"
_GOOD_LIGHT = "#15803d"
_HELP = (
    "SSE: suma de (y − ŷ)². El menor valor es el mejor ajuste en estos datos.",
    "SST: suma de (y − ȳ)². No depende del modelo y es igual en ambas columnas.",
    "Syx: error estándar del estimado. La recta usa n − 2 y la parábola n − 3.",
    "R²: fracción de la variabilidad de y que el modelo explica en la muestra.",
)


def _fixed(value: float | None, digits: int = _DIGITS, *, blank: str = "—") -> str:
    if value is None:
        return blank
    if value < 0 and abs(value) <= 1e-8:
        value = 0.0
    return f"{value:.{digits}f}"


def _equation_latex(coefficients: tuple[float, ...]) -> str:
    parts = [f"{coefficients[0]:.{_DIGITS}f}"]
    bodies = ("x", "x^{2}")
    for power, body in enumerate(bodies, start=1):
        if power >= len(coefficients):
            break
        coef = coefficients[power]
        sign = "-" if coef < 0 else "+"
        parts.append(f" {sign} {abs(coef):.{_DIGITS}f}\\,{body}")
    return r"\hat{y} = " + "".join(parts)


class ComparisonView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._ink = "#e7ecf3"
        self._good = _GOOD_DARK
        self._report: AnalysisReport | None = None

        self._title = QLabel("Comparación de modelos")
        self._title.setObjectName("Title")
        self._badge = QLabel("Sin ajuste")
        self._badge.setObjectName("Badge")
        head = QHBoxLayout()
        head.addWidget(self._title)
        head.addStretch(1)
        head.addWidget(self._badge)

        self._subtitle = QLabel("Evaluación del ajuste lineal y cuadrático")
        self._subtitle.setObjectName("Subtitle")

        self._reduction_name = QLabel("Reducción del error SSE")
        self._reduction_name.setObjectName("MetricName")
        self._reduction = QLabel("—")
        self._reduction.setObjectName("HeroValue")
        self._reduction_note = QLabel("Respecto al modelo lineal")
        self._reduction_note.setObjectName("Subtitle")
        self._reduction_note.setWordWrap(True)
        self._r2_name = QLabel("Coeficiente R²")
        self._r2_name.setObjectName("MetricName")
        self._r2 = QLabel("—")
        self._r2.setObjectName("HeroValue")
        self._r2_note = QLabel("")
        self._r2_note.setObjectName("Subtitle")
        cards = QGridLayout()
        cards.setSpacing(10)
        cards.addWidget(
            self._card(self._reduction_name, self._reduction, self._reduction_note), 0, 0
        )
        cards.addWidget(self._card(self._r2_name, self._r2, self._r2_note), 0, 1)

        section = QLabel("Indicadores del ajuste")
        section.setObjectName("Title")
        self._table = QTableWidget(4, 3)
        self._table.setHorizontalHeaderLabels(["Indicador", "Lineal", "Cuadrático"])
        configure_report_table(self._table)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._help = QLabel("\n".join(_HELP))
        self._help.setObjectName("Subtitle")
        self._help.setWordWrap(True)

        eq_title = QLabel("Ecuaciones obtenidas")
        eq_title.setObjectName("Title")
        self._linear_eq = MathLabel(r"\hat{y} = a_0 + a_1 x")
        self._quadratic_eq = MathLabel(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}")

        interp_title = QLabel("Interpretación de resultados")
        interp_title.setObjectName("Title")
        self._conclusion = QLabel("Calcule un ajuste para comparar los dos modelos.")
        self._conclusion.setObjectName("Analysis")
        self._conclusion.setWordWrap(True)
        self._conclusion.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addLayout(head)
        layout.addWidget(self._subtitle)
        layout.addLayout(cards)
        layout.addWidget(section)
        layout.addWidget(self._table)
        layout.addWidget(self._help)
        layout.addWidget(eq_title)
        layout.addWidget(self._equation_block("LINEAL", self._linear_eq))
        layout.addWidget(self._equation_block("CUADRÁTICO", self._quadratic_eq))
        layout.addWidget(interp_title)
        layout.addWidget(self._conclusion)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def clear(self) -> None:
        self._report = None
        self._badge.setText("Sin ajuste")
        self._reduction.setText("—")
        self._reduction_note.setText("Respecto al modelo lineal")
        self._paint_hero(self._reduction, good=False)
        self._r2_name.setText("Coeficiente R²")
        self._r2.setText("—")
        self._r2_note.setText("")
        self._paint_hero(self._r2, good=False)
        self._table.setRowCount(0)
        self._linear_eq.set_latex(r"\hat{y} = a_0 + a_1 x", color=self._ink)
        self._quadratic_eq.set_latex(r"\hat{y} = a_0 + a_1 x + a_2 x^{2}", color=self._ink)
        self._conclusion.setText("Calcule un ajuste para comparar los dos modelos.")

    def set_ink(self, color: str) -> None:
        self._ink = color
        self._good = _GOOD_LIGHT if color == "#0f172a" else _GOOD_DARK
        self._linear_eq.set_latex(self._linear_eq._latex, color=color)
        self._quadratic_eq.set_latex(self._quadratic_eq._latex, color=color)
        if self._report is not None:
            self.show_report(self._report)

    def show_report(self, report: AnalysisReport) -> None:
        self._report = report
        linear = report.linear_metrics
        quadratic = report.quadratic_metrics
        story = narrate_comparison(linear, quadratic)
        self._badge.setText(_badge(story))
        self._show_reduction(story)
        self._show_r2(story)
        self._fill_table(linear, quadratic, winner=story.winner_name, tied=story.tied)
        self._linear_eq.set_latex(_equation_latex(report.linear.coefficients), color=self._ink)
        self._quadratic_eq.set_latex(
            _equation_latex(report.quadratic.coefficients), color=self._ink
        )
        self._conclusion.setText(story.conclusion)

    def _show_reduction(self, story) -> None:
        if story.perfect_fit:
            self._reduction.setText("No aplica")
            self._reduction_note.setText("No aplica: ambos modelos presentan ajuste perfecto")
            self._paint_hero(self._reduction, good=False)
            return
        percent = story.sse_reduction_percent
        if percent is None:
            self._reduction.setText("—")
            self._reduction_note.setText("El SSE lineal es nulo y no se divide entre cero")
            self._paint_hero(self._reduction, good=False)
            return
        self._reduction.setText(f"{percent:.2f} %")
        self._reduction_note.setText("Respecto al modelo lineal")
        self._paint_hero(self._reduction, good=percent > 0 and not story.tied)

    def _show_r2(self, story) -> None:
        if story.tied:
            self._r2_name.setText("Coeficiente R²")
            note = "Mismo ajuste en la muestra"
        elif story.winner_name == "Lineal":
            self._r2_name.setText("Coeficiente R² lineal")
            note = f"Cuadrático: {_fixed(story.other_r_squared)}"
        else:
            self._r2_name.setText("Coeficiente R² cuadrático")
            note = f"Lineal: {_fixed(story.other_r_squared)}"
        self._r2.setText(_fixed(story.featured_r_squared, blank="no definido"))
        self._r2_note.setText(note)
        self._paint_hero(self._r2, good=not story.tied)

    def _fill_table(
        self,
        linear: FitMetrics,
        quadratic: FitMetrics,
        *,
        winner: str,
        tied: bool,
    ) -> None:
        rows = (
            ("SSE", linear.sse, quadratic.sse, False),
            ("SST", linear.sst, quadratic.sst, None),
            ("Syx", linear.std_error, quadratic.std_error, False),
            ("R²", linear.r_squared, quadratic.r_squared, True),
        )
        self._table.setRowCount(len(rows))
        for row, (name, left, right, higher_wins) in enumerate(rows):
            self._put(row, 0, name, good=False)
            mark_left, mark_right = _marks(left, right, higher_wins=higher_wins, tied=tied)
            blank = "no definido" if name == "R²" else "—"
            self._put(row, 1, _fixed(left, blank=blank), good=mark_left and winner == "Lineal")
            self._put(
                row, 2, _fixed(right, blank=blank), good=mark_right and winner == "Cuadrático"
            )
        fit_table_height(self._table)

    def _put(self, row: int, col: int, text: str, *, good: bool) -> None:
        item = QTableWidgetItem(text)
        if col > 0:
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        if good:
            item.setForeground(QBrush(QColor(self._good)))
        self._table.setItem(row, col, item)

    def _paint_hero(self, label: QLabel, *, good: bool) -> None:
        label.setStyleSheet(f"color: {self._good};" if good else "")

    @staticmethod
    def _card(*widgets: QLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        for widget in widgets:
            layout.addWidget(widget)
        return frame

    @staticmethod
    def _equation_block(name: str, formula: MathLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 10)
        caption = QLabel(name)
        caption.setObjectName("MetricName")
        layout.addWidget(caption)
        layout.addWidget(formula)
        return frame


def _badge(story) -> str:
    if story.perfect_fit:
        return "Lineal: ajuste perfecto"
    if story.tied:
        return "Lineal: recomendado"
    return f"{story.recommended_name}: mejor ajuste"


def _marks(
    left: float | None,
    right: float | None,
    *,
    higher_wins: bool | None,
    tied: bool,
) -> tuple[bool, bool]:
    if tied or higher_wins is None or left is None or right is None:
        return False, False
    if abs(left - right) <= 1e-12:
        return False, False
    if higher_wins:
        return left > right, right > left
    return left < right, right < left
