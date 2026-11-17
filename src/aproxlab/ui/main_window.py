"""Banco de trabajo: datos | resultados | gráficas, siempre visibles."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTabWidget,
    QToolBar,
)

from aproxlab.core.exceptions import DatasetError
from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.charts import plot_palette
from aproxlab.services.examples import EXAMPLES
from aproxlab.ui.controllers.analysis_presenter import AnalysisPresenter
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.styles.theme import apply_theme, ink_color
from aproxlab.ui.views.charts_view import ChartsView
from aproxlab.ui.views.comparison_view import ComparisonView
from aproxlab.ui.views.data_view import DataView
from aproxlab.ui.views.linear_view import LinearView
from aproxlab.ui.views.quadratic_view import QuadraticView


class MainWindow(QMainWindow):
    def __init__(self, presenter: AnalysisPresenter | None = None) -> None:
        super().__init__()
        self.setWindowTitle("AproxLab — Mínimos cuadrados")
        self.resize(1360, 820)
        self.setMinimumSize(1080, 680)
        self._presenter = presenter or AnalysisPresenter(parent=self)
        self._theme = "dark"

        self._data = DataView()
        self._linear = LinearView()
        self._quadratic = QuadraticView()
        self._comparison = ComparisonView()
        self._charts = ChartsView()
        self._charts.set_palette(plot_palette(self._theme))

        self._results = QTabWidget()
        self._results.addTab(self._linear, "Lineal")
        self._results.addTab(self._quadratic, "Cuadrático")
        self._results.addTab(self._comparison, "Comparación")
        self._results.tabBar().setExpanding(True)
        self._results.setDocumentMode(True)

        self._results.setMinimumHeight(300)
        self._charts_visible = True
        self._chart_sizes = [420, 380]
        self._results_split = QSplitter(Qt.Orientation.Vertical)
        self._results_split.addWidget(self._results)
        self._results_split.addWidget(self._charts)
        self._results_split.setStretchFactor(0, 3)
        self._results_split.setStretchFactor(1, 2)
        self._results_split.setSizes(self._chart_sizes)
        self._results_split.setChildrenCollapsible(True)

        self._data.setMinimumWidth(250)
        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self._data)
        split.addWidget(self._results_split)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setSizes([280, 1080])
        split.setChildrenCollapsible(False)
        self.setCentralWidget(split)
        self._results.currentChanged.connect(self._sync_chart_tab)

        self._build_toolbar()
        self._build_menus()
        self.statusBar().showMessage("n=0 · sin ajuste")
        self._connect_presenter()
        self._load_classroom_example()

    def _connect_presenter(self) -> None:
        presenter = self._presenter
        presenter.analysis_ready.connect(self._on_ready)
        presenter.analysis_failed.connect(self._on_failed)
        presenter.dataset_loaded.connect(self._on_dataset_loaded)
        self._data.fit_requested.connect(self._fit_from_table)
        self._data.clear_requested.connect(self._clear_workspace)
        fit_shortcut = QAction(self)
        fit_shortcut.setShortcut(QKeySequence("F5"))
        fit_shortcut.triggered.connect(self._fit_from_table)
        self.addAction(fit_shortcut)

    def _build_toolbar(self) -> None:
        bar = QToolBar("Principal")
        bar.setMovable(False)
        self.addToolBar(bar)
        bar.addWidget(QLabel(" Ejemplos "))
        self._examples = QComboBox()
        self._examples.addItem("Conjunto de ejemplo…", "")
        for example in EXAMPLES:
            self._examples.addItem(example.title, example.key)
        self._examples.currentIndexChanged.connect(self._example_chosen)
        bar.addWidget(self._examples)
        bar.addSeparator()
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self._clear_workspace)
        bar.addWidget(clear_btn)
        self._toggle_charts_btn = QPushButton("Ocultar gráficas")
        self._toggle_charts_btn.clicked.connect(self._toggle_charts)
        bar.addWidget(self._toggle_charts_btn)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&Archivo")
        file_menu.addAction(self._action("Exportar resultados…", self._export_report))
        file_menu.addAction(self._action("Exportar gráfica PNG…", self._export_chart))
        file_menu.addAction(self._action("Exportar las tres gráficas…", self._export_all_charts))
        file_menu.addSeparator()
        file_menu.addAction(self._action("Limpiar", self._clear_workspace))
        file_menu.addSeparator()
        file_menu.addAction(self._action("Salir", self.close, QKeySequence.StandardKey.Quit))

        examples_menu = self.menuBar().addMenu("&Ejemplos")
        for example in EXAMPLES:
            examples_menu.addAction(
                self._action(
                    example.title,
                    lambda checked=False, key=example.key: self._load_example(key),
                )
            )

        view_menu = self.menuBar().addMenu("&Ver")
        view_menu.addAction(self._action("Tema oscuro", lambda: self._set_theme("dark")))
        view_menu.addAction(self._action("Tema claro", lambda: self._set_theme("light")))
        view_menu.addSeparator()
        view_menu.addAction(self._action("Ocultar/mostrar gráficas", self._toggle_charts))

        help_menu = self.menuBar().addMenu("A&yuda")
        help_menu.addAction(self._action("Acerca de AproxLab", self._about))

    def _action(self, text: str, slot, shortcut=None) -> QAction:
        action = QAction(text, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        action.triggered.connect(slot)
        return action

    def _fit_from_table(self) -> None:
        try:
            x, y = self._data.current_pairs()
        except DatasetError as exc:
            self._on_failed(str(exc))
            return
        self._presenter.calculate(x, y)

    def _example_chosen(self, index: int) -> None:
        key = self._examples.itemData(index)
        if key:
            self._load_example(str(key))

    def _on_ready(self, report: AnalysisReport) -> None:
        self._data.clear_error()
        self._linear.show_report(report)
        self._quadratic.show_report(report)
        self._comparison.show_report(report)
        self._charts.show_report(report)
        self._sync_chart_tab(self._results.currentIndex())
        lin = report.linear_metrics
        quad = report.quadratic_metrics
        self.statusBar().showMessage(
            f"n={report.x.size}  ·  SSE_lin={fmt_number(lin.sse)}  ·  "
            f"SSE_quad={fmt_number(quad.sse)}  ·  min SSE: {report.comparison.winner_name}"
        )

    def _sync_chart_tab(self, index: int) -> None:
        self._charts.set_current({0: 0, 1: 1, 2: 2}.get(index, 0))

    def _on_failed(self, message: str) -> None:
        self._data.show_error(message)
        self.statusBar().showMessage(message)

    def _on_dataset_loaded(self, x: list, y: list, label: str) -> None:
        self._data.load_pairs(x, y)
        self.statusBar().showMessage(f"{label} · {len(x)} puntos")
        self._presenter.calculate(x, y)

    def _load_example(self, key: str) -> None:
        self._presenter.load_example(key)

    def _clear_workspace(self) -> None:
        self._examples.blockSignals(True)
        self._examples.setCurrentIndex(0)
        self._examples.blockSignals(False)
        self._data.clear_all()
        self._linear.clear()
        self._quadratic.clear()
        self._comparison.clear()
        self._charts.clear()
        self._presenter.clear()
        self.statusBar().showMessage("n=0 · sin ajuste")

    def _load_classroom_example(self) -> None:
        index = self._examples.findData("class_linear")
        if index < 0:
            self._load_example("class_linear")
            return
        self._examples.setCurrentIndex(index)

    def _export_report(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar resultados", "reporte_aproxlab.txt", "Texto (*.txt)"
        )
        if path:
            self._presenter.export_report(path)
            self.statusBar().showMessage(f"Reporte: {path}")

    def _export_chart(self) -> None:
        if self._presenter.last_report is None:
            self._on_failed("Calcule un ajuste antes de exportar gráficas.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar gráfica", "grafica.png", "PNG (*.png)"
        )
        if path:
            self._charts.save_current_png(path)
            self.statusBar().showMessage(f"PNG: {path}")

    def _export_all_charts(self) -> None:
        if self._presenter.last_report is None:
            self._on_failed("Calcule un ajuste antes de exportar gráficas.")
            return
        directory = QFileDialog.getExistingDirectory(self, "Carpeta para las tres PNG")
        if directory:
            written = self._charts.save_all_png(directory)
            self.statusBar().showMessage(f"{len(written)} PNG en {directory}")

    def _toggle_charts(self) -> None:
        if self._charts_visible:
            self._chart_sizes = self._results_split.sizes()
            self._charts.hide()
            self._charts_visible = False
            self._toggle_charts_btn.setText("Mostrar gráficas")
            return
        self._charts.show()
        self._results_split.setSizes(self._chart_sizes)
        self._charts_visible = True
        self._toggle_charts_btn.setText("Ocultar gráficas")

    def _set_theme(self, name: str) -> None:
        from PySide6.QtWidgets import QApplication

        qt_app = QApplication.instance()
        if qt_app is None:
            return
        self._theme = name
        apply_theme(qt_app, name)
        color = ink_color(name)
        self._charts.set_palette(plot_palette(name))
        self._linear.set_ink(color)
        self._quadratic.set_ink(color)
        self._comparison.set_ink(color)

    def _about(self) -> None:
        QMessageBox.about(
            self,
            "Acerca de AproxLab",
            "AproxLab — banco de trabajo de mínimos cuadrados.\n"
            "Regresión lineal y polinomio de grado 2.\n"
            "Métodos Numéricos.",
        )
