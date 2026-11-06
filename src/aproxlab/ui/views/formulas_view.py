"""Referencia de métodos numéricos: fórmulas renderizadas, no prosa suelta."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from aproxlab.ui.widgets.math_label import MathLabel

_BLOCKS: tuple[tuple[str, str, str], ...] = (
    (
        "Criterio",
        r"\min_a \|Xa - y\|_2^2",
        "Mínimos cuadrados ordinarios. X es la matriz de diseño; a el vector de parámetros.",
    ),
    (
        "Recta",
        r"\hat{y} = a_0 + a_1 x,\quad X=[1\mid x],\quad p=2,\ \nu=n-2",
        "Exige n ≥ 2 y al menos dos x distintos. Si x es constante, a₁ no está identificado.",
    ),
    (
        "Parábola",
        r"\hat{y} = a_0 + a_1 x + a_2 x^{2},\quad p=3,\ \nu=n-3",
        "Exige n ≥ 3 y tres x distintos. Contiene a la recta cuando a₂ = 0.",
    ),
    (
        "Residuos y SSE",
        r"e_i = y_i - \hat{y}_i,\quad SSE=\sum_{i=1}^{n} e_i^2",
        "Cantidad minimizada. Un SSE menor en la muestra no es, por sí solo, mejor modelo.",
    ),
    (
        "SST y R²",
        r"SST=\sum (y_i-\bar y)^2,\quad R^2=1-SSE/SST",
        "R² indefinido si y es constante (SST = 0). R² = 1 es ajuste perfecto a la muestra.",
    ),
    (
        "Error estándar",
        r"S_{yx}=\sqrt{SSE/(n-p)}",
        "Estima la dispersión residual por grado de libertad. Lineal: p=2. Cuadrático: p=3.",
    ),
    (
        "R² ajustado",
        r"R^2_{\mathrm{adj}}=1-\dfrac{SSE/(n-p)}{SST/(n-1)}",
        "Penaliza parámetros extra. Preferible a R² crudo para comparar modelos anidados.",
    ),
    (
        "Correlación r",
        r"r=\mathrm{corr}(x,y)",
        "Mide asociación lineal entre x e y. No describe la calidad de un polinomio de grado 2.",
    ),
    (
        "Solución numérica",
        r"a=\arg\min\|Xa-y\|_2\ \mathrm{(SVD/lstsq)}",
        "No se invierte XᵀX. lstsq es estable cuando X está mal condicionada.",
    ),
)


class _FormulaCard(QFrame):
    def __init__(self, title: str, latex: str, note: str, *, color: str) -> None:
        super().__init__()
        self.setObjectName("Card")
        self._latex = latex
        heading = QLabel(title.upper())
        heading.setObjectName("MetricName")
        self._math = MathLabel(latex, color=color, dpi=130)
        note_lbl = QLabel(note)
        note_lbl.setObjectName("Subtitle")
        note_lbl.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        layout.addWidget(heading)
        layout.addWidget(self._math)
        layout.addWidget(note_lbl)

    def set_ink(self, color: str) -> None:
        self._math.set_latex(self._latex, color=color)


class FormulasView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._cards: list[_FormulaCard] = []
        intro = QLabel("Referencia — mínimos cuadrados para aproximación funcional")
        intro.setObjectName("Title")
        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(8, 8, 8, 8)
        inner_layout.addWidget(intro)
        inner_layout.addLayout(grid)
        color = "#e7ecf3"
        for i, (title, latex, note) in enumerate(_BLOCKS):
            card = _FormulaCard(title, latex, note, color=color)
            self._cards.append(card)
            grid.addWidget(card, i // 2, i % 2)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(inner)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

    def set_ink(self, color: str) -> None:
        for card in self._cards:
            card.set_ink(color)
