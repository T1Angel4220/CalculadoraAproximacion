"""Explicación de fórmulas e indicadores para el usuario académico."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

_TEXT = """
<h2>Métodos numéricos utilizados</h2>
<p>Ambos ajustes minimizan la <b>suma de cuadrados de los residuos</b>
SSE = Σ (yᵢ − ŷᵢ)². El sistema normal se resuelve con
<code>numpy.linalg.lstsq</code> (descomposición SVD), no con la inversa
explícita de XᵀX, que es numéricamente inestable.</p>

<h3>Recta de mínimos cuadrados</h3>
<p>Modelo: ŷ = a₀ + a₁ x. Requiere n ≥ 2 y al menos dos x distintos.
Si todos los x coinciden, la pendiente no está identificada.</p>
<ul>
<li><b>Intersección a₀</b> y <b>pendiente a₁</b>: coeficientes del polinomio de grado 1.</li>
<li><b>SST</b> = Σ (yᵢ − ȳ)², variabilidad total de y.</li>
<li><b>R²</b> = 1 − SSE/SST. No está definido si y es constante (SST = 0).</li>
<li><b>Error estándar Syx</b> = √(SSE / (n − 2)) en el caso lineal (p = 2 parámetros).</li>
<li><b>Correlación r</b>: Pearson entre x e y (asociación lineal, no del polinomio).</li>
</ul>

<h3>Polinomio de segundo grado</h3>
<p>Modelo: ŷ = a₀ + a₁ x + a₂ x². Requiere n ≥ 3 y tres x distintos.
Syx usa n − 3 grados de libertad.</p>

<h3>Comparación</h3>
<p>El criterio mostrado como “menor error” es el SSE de entrenamiento.
El modelo cuadrático <i>contiene</i> al lineal (a₂ = 0). Por eso un SSE menor
no garantiza mejor predicción fuera de la muestra. El R² ajustado
penaliza el parámetro extra: 1 − (SSE/(n−p)) / (SST/(n−1)).</p>
"""


class FormulasView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        label = QLabel(_TEXT)
        label.setWordWrap(True)
        label.setOpenExternalLinks(False)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(label)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
