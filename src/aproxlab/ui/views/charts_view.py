"""Tres representaciones gráficas exigidas por la guía."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.charts import plot_scatter_and_fits
from aproxlab.ui.widgets.mpl_canvas import MplCanvas

_LINEAR_COLOR = "#f59e0b"
_QUAD_COLOR = "#34d399"


class ChartsView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        title = QLabel("Gráficas")
        title.setObjectName("Title")
        self._empty = QLabel("Las curvas aparecen después de un cálculo exitoso.")
        self._empty.setObjectName("Subtitle")
        self._linear = MplCanvas()
        self._quadratic = MplCanvas()
        self._both = MplCanvas()
        tabs = QTabWidget()
        tabs.addTab(self._linear, "Datos y recta")
        tabs.addTab(self._quadratic, "Datos y parábola")
        tabs.addTab(self._both, "Comparativa")
        self._tabs = tabs
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self._empty)
        layout.addWidget(tabs, 1)

    def show_report(self, report: AnalysisReport) -> None:
        self._empty.setText("Puntos observados y modelos ajustados.")
        plot_scatter_and_fits(
            self._linear.axes,
            report.x,
            report.y,
            [(report.linear, _LINEAR_COLOR)],
            title="Datos originales y recta de ajuste",
        )
        self._linear.draw()
        plot_scatter_and_fits(
            self._quadratic.axes,
            report.x,
            report.y,
            [(report.quadratic, _QUAD_COLOR)],
            title="Datos originales y curva cuadrática",
        )
        self._quadratic.draw()
        plot_scatter_and_fits(
            self._both.axes,
            report.x,
            report.y,
            [(report.linear, _LINEAR_COLOR), (report.quadratic, _QUAD_COLOR)],
            title="Comparación de ambos modelos",
        )
        self._both.draw()

    def save_current_png(self, path: str) -> None:
        canvas = self._tabs.currentWidget()
        if isinstance(canvas, MplCanvas):
            canvas.save_png(path)

    def save_all_png(self, directory: str) -> list[str]:
        from pathlib import Path

        folder = Path(directory)
        paths = [
            (self._linear, folder / "ajuste_lineal.png"),
            (self._quadratic, folder / "ajuste_cuadratico.png"),
            (self._both, folder / "comparativa.png"),
        ]
        written: list[str] = []
        for canvas, dest in paths:
            canvas.save_png(str(dest))
            written.append(str(dest))
        return written
