"""Tres gráficas de ajuste, ampliables y coherentes con el tema."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.charts import PlotPalette, plot_palette, plot_scatter_and_fits
from aproxlab.ui.widgets.mpl_canvas import MplCanvas


class ChartsView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._report: AnalysisReport | None = None
        self._palette: PlotPalette = plot_palette("dark")
        self._linear = MplCanvas()
        self._quadratic = MplCanvas()
        self._both = MplCanvas()
        self._tabs = QTabWidget()
        self._tabs.addTab(self._linear, "Recta")
        self._tabs.addTab(self._quadratic, "Parábola")
        self._tabs.addTab(self._both, "Ambos")
        self.setMinimumHeight(300)

        enlarge = QPushButton("Ampliar gráfica")
        enlarge.setObjectName("Primary")
        enlarge.setMinimumHeight(32)
        enlarge.clicked.connect(self._enlarge_current)
        all_btn = QPushButton("Ver las tres")
        all_btn.clicked.connect(self._enlarge_all)
        bar = QHBoxLayout()
        bar.addWidget(enlarge)
        bar.addWidget(all_btn)
        bar.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addLayout(bar)
        layout.addWidget(self._tabs, 1)

    def set_palette(self, palette: PlotPalette) -> None:
        self._palette = palette
        if self._report is not None:
            self.show_report(self._report)

    def set_current(self, index: int) -> None:
        self._tabs.setCurrentIndex(index)

    def show_report(self, report: AnalysisReport) -> None:
        self._report = report
        pal = self._palette
        plot_scatter_and_fits(
            self._linear.axes,
            report.x,
            report.y,
            [(report.linear, pal.linear)],
            title="Datos originales y recta de ajuste lineal",
            palette=pal,
        )
        self._linear.draw()
        plot_scatter_and_fits(
            self._quadratic.axes,
            report.x,
            report.y,
            [(report.quadratic, pal.quadratic)],
            title="Datos originales y curva de ajuste polinomial",
            palette=pal,
        )
        self._quadratic.draw()
        plot_scatter_and_fits(
            self._both.axes,
            report.x,
            report.y,
            [(report.linear, pal.linear), (report.quadratic, pal.quadratic)],
            title="Datos originales y ambos modelos",
            palette=pal,
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

    def _enlarge_current(self) -> None:
        if self._report is None:
            return
        index = self._tabs.currentIndex()
        titles = (
            "Datos originales y recta de ajuste lineal",
            "Datos originales y curva de ajuste polinomial",
            "Datos originales y ambos modelos",
        )
        pal = self._palette
        report = self._report
        fits_options = (
            [(report.linear, pal.linear)],
            [(report.quadratic, pal.quadratic)],
            [(report.linear, pal.linear), (report.quadratic, pal.quadratic)],
        )
        dialog = _ExpandedChartDialog(
            titles[index],
            report,
            fits_options[index],
            pal,
            self,
        )
        dialog.exec()

    def _enlarge_all(self) -> None:
        if self._report is None:
            return
        dialog = _ExpandedAllDialog(self._report, self._palette, self)
        dialog.exec()


class _ExpandedChartDialog(QDialog):
    def __init__(
        self,
        title: str,
        report: AnalysisReport,
        fits: list,
        palette: PlotPalette,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(1100, 720)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        canvas = MplCanvas(width=11.0, height=6.8)
        plot_scatter_and_fits(
            canvas.axes,
            report.x,
            report.y,
            fits,
            title=title,
            palette=palette,
        )
        layout = QVBoxLayout(self)
        layout.addWidget(canvas)


class _ExpandedAllDialog(QDialog):
    def __init__(self, report: AnalysisReport, palette: PlotPalette, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Las tres representaciones gráficas")
        self.resize(1180, 860)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        tabs = QTabWidget()
        specs = (
            (
                "Recta",
                [(report.linear, palette.linear)],
                "Datos originales y recta de ajuste lineal",
            ),
            (
                "Parábola",
                [(report.quadratic, palette.quadratic)],
                "Datos originales y curva de ajuste polinomial",
            ),
            (
                "Ambos",
                [(report.linear, palette.linear), (report.quadratic, palette.quadratic)],
                "Datos originales y ambos modelos",
            ),
        )
        for name, fits, title in specs:
            canvas = MplCanvas(width=11.0, height=6.6)
            plot_scatter_and_fits(
                canvas.axes, report.x, report.y, fits, title=title, palette=palette
            )
            tabs.addTab(canvas, name)
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
