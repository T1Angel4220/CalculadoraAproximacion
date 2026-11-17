"""Tarjeta de paso: fórmula, sustitución y resultado, sin aplastar el texto."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

from aproxlab.ui.widgets.math_label import MathLabel


class FormulaCard(QFrame):
    """Muestra un cálculo de clase: fórmula → reemplazo numérico → valor."""

    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self._formula_tex = ""
        self._ink = "#e7ecf3"

        self._title = QLabel(title)
        self._title.setObjectName("Title")
        self._title.setWordWrap(True)

        kick_f = QLabel("FÓRMULA")
        kick_f.setObjectName("StepKicker")
        self._formula = MathLabel(dpi=140)

        kick_s = QLabel("SUSTITUCIÓN")
        kick_s.setObjectName("StepKicker")
        self._subst = QLabel("—")
        self._subst.setObjectName("Analysis")
        self._subst.setWordWrap(True)

        kick_r = QLabel("RESULTADO")
        kick_r.setObjectName("StepKicker")
        self._result = QLabel("—")
        self._result.setObjectName("MetricValue")
        self._result.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)
        layout.addWidget(self._title)
        layout.addSpacing(4)
        layout.addWidget(kick_f)
        layout.addWidget(self._formula)
        layout.addSpacing(6)
        layout.addWidget(kick_s)
        layout.addWidget(self._subst)
        layout.addSpacing(6)
        layout.addWidget(kick_r)
        layout.addWidget(self._result)

    def set_step(self, *, formula: str, substitution: str, result: str) -> None:
        self._formula_tex = formula
        self._formula.set_latex(formula, color=self._ink)
        self._subst.setText(substitution)
        self._result.setText(result)

    def set_ink(self, color: str) -> None:
        self._ink = color
        if self._formula_tex:
            self._formula.set_latex(self._formula_tex, color=color)

    def clear(self) -> None:
        self._formula_tex = ""
        self._formula.clear_formula()
        self._subst.setText("—")
        self._result.setText("—")
