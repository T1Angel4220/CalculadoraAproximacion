"""Presenter MVP: traduce eventos de UI a casos de uso del núcleo."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from aproxlab.core.exceptions import DatasetError
from aproxlab.services.analysis import AnalysisReport, AnalysisService
from aproxlab.services.csv_io import export_report_text, export_xy_csv, load_xy_csv
from aproxlab.services.examples import example_by_key


class AnalysisPresenter(QObject):
    analysis_ready = Signal(object)
    analysis_failed = Signal(str)
    dataset_loaded = Signal(list, list, str)

    def __init__(self, service: AnalysisService | None = None, parent=None) -> None:
        super().__init__(parent)
        self._service = service or AnalysisService()
        self._last_report: AnalysisReport | None = None

    @property
    def last_report(self) -> AnalysisReport | None:
        return self._last_report

    def calculate(self, x: list[float], y: list[float]) -> None:
        try:
            report = self._service.analyze(x, y)
        except DatasetError as exc:
            self._last_report = None
            self.analysis_failed.emit(str(exc))
            return
        self._last_report = report
        self.analysis_ready.emit(report)

    def load_csv(self, path: str) -> None:
        try:
            x, y = load_xy_csv(path)
        except (OSError, DatasetError) as exc:
            self.analysis_failed.emit(str(exc))
            return
        self.dataset_loaded.emit(x, y, Path(path).name)

    def load_example(self, key: str) -> None:
        try:
            example = example_by_key(key)
        except KeyError as exc:
            self.analysis_failed.emit(str(exc))
            return
        self.dataset_loaded.emit(list(example.x), list(example.y), example.title)

    def export_report(self, path: str) -> None:
        if self._last_report is None:
            self.analysis_failed.emit("Calcule un ajuste antes de exportar resultados.")
            return
        export_report_text(path, self._last_report)

    def export_dataset(self, path: str, x: list[float], y: list[float]) -> None:
        export_xy_csv(path, x, y)
