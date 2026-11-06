"""Banco de trabajo: datos | resultados | gráficas, siempre visibles."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QTabWidget,
    QToolBar,
)

from aproxlab.core.exceptions import DatasetError
from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.examples import EXAMPLES
from aproxlab.ui.controllers.analysis_presenter import AnalysisPresenter
from aproxlab.ui.formatters import fmt_number
from aproxlab.ui.styles.theme import apply_theme, ink_color
from aproxlab.ui.views.charts_view import ChartsView
from aproxlab.ui.views.comparison_view import ComparisonView
from aproxlab.ui.views.data_view import DataView
from aproxlab.ui.views.formulas_view import FormulasView
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
        self._formulas = FormulasView()
        self._charts = ChartsView()

        self._results = QTabWidget()
        self._results.addTab(self._linear, "Lineal")
        self._results.addTab(self._quadratic, "Cuadrático")
        self._results.addTab(self._comparison, "Comparación")
        self._results.addTab(self._formulas, "Referencia")

        results_split = QSplitter(Qt.Orientation.Vertical)
        results_split.addWidget(self._results)
        results_split.addWidget(self._charts)
        results_split.setStretchFactor(0, 3)
        results_split.setStretchFactor(1, 2)
        results_split.setSizes([480, 320])

        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self._data)
        split.addWidget(results_split)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setSizes([300, 1060])
        self.setCentralWidget(split)

        self._build_toolbar()
        self._build_menus()
        self.statusBar().showMessage("n=0 · sin ajuste")
        self._connect_presenter()

    def _connect_presenter(self) -> None:
        presenter = self._presenter
        self._data.calculate_requested.connect(presenter.calculate)
        presenter.analysis_ready.connect(self._on_ready)
        presenter.analysis_failed.connect(self._on_failed)
        presenter.dataset_loaded.connect(self._on_dataset_loaded)

    def _build_toolbar(self) -> None:
        bar = QToolBar("Principal")
        bar.setMovable(False)
        self.addToolBar(bar)
        bar.addAction(self._action("Ajustar", self._fit_from_table, QKeySequence("F5")))
        bar.addSeparator()
        bar.addAction(self._action("CSV…", self._import_csv, QKeySequence.StandardKey.Open))
        bar.addAction(self._action("Exportar…", self._export_report))
        bar.addAction(self._action("PNG…", self._export_chart))
        bar.addSeparator()
        self._examples = QComboBox()
        self._examples.addItem("Conjunto de ejemplo…", "")
        for example in EXAMPLES:
            self._examples.addItem(example.title, example.key)
        self._examples.currentIndexChanged.connect(self._example_chosen)
        bar.addWidget(self._examples)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&Archivo")
        file_menu.addAction(self._action("Importar CSV…", self._import_csv))
        file_menu.addAction(self._action("Exportar resultados…", self._export_report))
        file_menu.addAction(self._action("Exportar gráfica PNG…", self._export_chart))
        file_menu.addAction(self._action("Exportar las tres gráficas…", self._export_all_charts))
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
        lin = report.linear_metrics
        quad = report.quadratic_metrics
        self.statusBar().showMessage(
            f"n={report.x.size}  ·  SSE_lin={fmt_number(lin.sse)}  ·  "
            f"SSE_quad={fmt_number(quad.sse)}  ·  min SSE: {report.comparison.winner_name}"
        )

    def _on_failed(self, message: str) -> None:
        self._data.show_error(message)
        self.statusBar().showMessage(message)

    def _on_dataset_loaded(self, x: list, y: list, label: str) -> None:
        self._data.load_pairs(x, y)
        self.statusBar().showMessage(f"{label} · {len(x)} puntos")
        self._presenter.calculate(x, y)

    def _load_example(self, key: str) -> None:
        self._presenter.load_example(key)

    def _import_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Importar CSV", "", "CSV (*.csv);;Todos (*.*)")
        if path:
            self._presenter.load_csv(path)

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

    def _set_theme(self, name: str) -> None:
        from PySide6.QtWidgets import QApplication

        qt_app = QApplication.instance()
        if qt_app is None:
            return
        self._theme = name
        apply_theme(qt_app, name)
        color = ink_color(name)
        self._linear.set_ink(color)
        self._quadratic.set_ink(color)
        self._comparison.set_ink(color)
        self._formulas.set_ink(color)
        if self._presenter.last_report is not None:
            self._charts.show_report(self._presenter.last_report)

    def _about(self) -> None:
        QMessageBox.about(
            self,
            "Acerca de AproxLab",
            "AproxLab — banco de trabajo de mínimos cuadrados.\n"
            "Regresión lineal y polinomio de grado 2.\n"
            "Métodos Numéricos.",
        )
