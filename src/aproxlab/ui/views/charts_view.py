"""Tres gráficas de ajuste, sin encabezados decorativos."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.charts import plot_scatter_and_fits
from aproxlab.ui.widgets.mpl_canvas import MplCanvas

_LINEAR_COLOR = "#f59e0b"
_QUAD_COLOR = "#34d399"


class ChartsView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._linear = MplCanvas()
        self._quadratic = MplCanvas()
        self._both = MplCanvas()
        self._tabs = QTabWidget()
        self._tabs.addTab(self._linear, "Recta")
        self._tabs.addTab(self._quadratic, "Parábola")
        self._tabs.addTab(self._both, "Ambos")
        self.setMinimumHeight(260)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._tabs)

    def set_current(self, index: int) -> None:
        self._tabs.setCurrentIndex(index)

    def show_report(self, report: AnalysisReport) -> None:
        plot_scatter_and_fits(
            self._linear.axes,
            report.x,
            report.y,
            [(report.linear, _LINEAR_COLOR)],
            title="Datos originales y recta de ajuste lineal",
        )
        self._linear.draw()
        plot_scatter_and_fits(
            self._quadratic.axes,
            report.x,
            report.y,
            [(report.quadratic, _QUAD_COLOR)],
            title="Datos originales y curva de ajuste polinomial",
        )
        self._quadratic.draw()
        plot_scatter_and_fits(
            self._both.axes,
            report.x,
            report.y,
            [(report.linear, _LINEAR_COLOR), (report.quadratic, _QUAD_COLOR)],
            title="Datos originales y ambos modelos",
        )
        self._both.draw()

    def save_current_png(self, path: str) -> None:
        canvas = self._tabs.currentWidget()
        if isinstance(canvas, MplCanvas):
            canvas.save_png(path)

    def save_all_png(self, directory: str) -> list[str]:
        folder = Path(directory)
        written: list[str] = []
        for canvas, dest in (
            (self._linear, folder / "ajuste_lineal.png"),
            (self._quadratic, folder / "ajuste_cuadratico.png"),
            (self._both, folder / "comparativa.png"),
        ):
            canvas.save_png(str(dest))
            written.append(str(dest))
        return written
