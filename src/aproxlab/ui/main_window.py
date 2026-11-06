"""Ventana principal: menú, sidebar y páginas apiladas."""

from __future__ import annotations

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QWidget,
)

from aproxlab.services.analysis import AnalysisReport
from aproxlab.services.examples import EXAMPLES
from aproxlab.ui.controllers.analysis_presenter import AnalysisPresenter
from aproxlab.ui.styles.theme import apply_theme
from aproxlab.ui.views.charts_view import ChartsView
from aproxlab.ui.views.comparison_view import ComparisonView
from aproxlab.ui.views.data_view import DataView
from aproxlab.ui.views.formulas_view import FormulasView
from aproxlab.ui.views.linear_view import LinearView
from aproxlab.ui.views.quadratic_view import QuadraticView
from aproxlab.ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self, presenter: AnalysisPresenter | None = None) -> None:
        super().__init__()
        self.setWindowTitle("AproxLab — Calculadora de aproximación funcional")
        self.resize(1280, 800)
        self.setMinimumSize(1100, 700)
        self._presenter = presenter or AnalysisPresenter(parent=self)
        self._theme = "dark"

        self._data = DataView()
        self._linear = LinearView()
        self._quadratic = QuadraticView()
        self._comparison = ComparisonView()
        self._charts = ChartsView()
        self._formulas = FormulasView()

        self._stack = QStackedWidget()
        for page in (
            self._data,
            self._linear,
            self._quadratic,
            self._comparison,
            self._charts,
            self._formulas,
        ):
            self._stack.addWidget(page)

        sidebar = Sidebar()
        sidebar.page_changed.connect(self._stack.setCurrentIndex)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sidebar)
        layout.addWidget(self._stack, 1)
        self.setCentralWidget(central)

        self._build_menus()
        self.statusBar().showMessage("Listo. Ingrese datos o cargue un ejemplo.")
        self._connect_presenter()

    def _connect_presenter(self) -> None:
        presenter = self._presenter
        self._data.calculate_requested.connect(presenter.calculate)
        presenter.analysis_ready.connect(self._on_ready)
        presenter.analysis_failed.connect(self._on_failed)
        presenter.dataset_loaded.connect(self._on_dataset_loaded)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&Archivo")
        file_menu.addAction(
            self._action("Importar CSV…", self._import_csv, QKeySequence.StandardKey.Open)
        )
        file_menu.addAction(self._action("Exportar resultados…", self._export_report))
        file_menu.addAction(self._action("Exportar gráfica PNG…", self._export_chart))
        file_menu.addAction(self._action("Exportar las tres gráficas…", self._export_all_charts))
        file_menu.addSeparator()
        file_menu.addAction(self._action("Salir", self.close, QKeySequence.StandardKey.Quit))

        examples_menu = self.menuBar().addMenu("&Ejemplos")
        for example in EXAMPLES:
            examples_menu.addAction(
                self._action(
                    example.title, lambda checked=False, key=example.key: self._load_example(key)
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

    def _on_ready(self, report: AnalysisReport) -> None:
        self._data.clear_error()
        self._linear.show_report(report)
        self._quadratic.show_report(report)
        self._comparison.show_report(report)
        self._charts.show_report(report)
        winner = report.comparison.winner_name
        self.statusBar().showMessage(f"Ajuste calculado · n={report.x.size} · menor SSE: {winner}")

    def _on_failed(self, message: str) -> None:
        self._data.show_error(message)
        self.statusBar().showMessage(message)
        self._stack.setCurrentIndex(0)

    def _on_dataset_loaded(self, x: list, y: list, label: str) -> None:
        self._data.load_pairs(x, y)
        self.statusBar().showMessage(
            f"Datos cargados: {label} ({len(x)} puntos). Calcule los ajustes."
        )
        self._stack.setCurrentIndex(0)
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
            self.statusBar().showMessage(f"Reporte guardado en {path}")

    def _export_chart(self) -> None:
        if self._presenter.last_report is None:
            self._on_failed("Calcule un ajuste antes de exportar gráficas.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar gráfica", "grafica.png", "PNG (*.png)"
        )
        if path:
            self._charts.save_current_png(path)
            self.statusBar().showMessage(f"Gráfica guardada en {path}")

    def _export_all_charts(self) -> None:
        if self._presenter.last_report is None:
            self._on_failed("Calcule un ajuste antes de exportar gráficas.")
            return
        directory = QFileDialog.getExistingDirectory(self, "Carpeta para las tres PNG")
        if directory:
            written = self._charts.save_all_png(directory)
            self.statusBar().showMessage(f"Exportadas {len(written)} gráficas en {directory}")

    def _set_theme(self, name: str) -> None:
        from PySide6.QtWidgets import QApplication

        qt_app = QApplication.instance()
        if qt_app is None:
            return
        self._theme = name
        apply_theme(qt_app, name)
        if self._presenter.last_report is not None:
            self._charts.show_report(self._presenter.last_report)

    def _about(self) -> None:
        QMessageBox.about(
            self,
            "Acerca de AproxLab",
            "AproxLab 1.0 — calculadora de aproximación funcional.\n"
            "Regresión lineal y polinomio de grado 2 por mínimos cuadrados.\n"
            "Proyecto académico de Métodos Numéricos.",
        )
