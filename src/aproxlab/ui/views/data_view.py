"""Ingreso, edición y validación visual de pares (x, y)."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from aproxlab.core.exceptions import DatasetError
from aproxlab.ui.widgets.dataset_model import DatasetTableModel


class DataView(QWidget):
    calculate_requested = Signal(list, list)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.model = DatasetTableModel(self)
        title = QLabel("Ingreso de datos")
        title.setObjectName("Title")
        subtitle = QLabel(
            "Agregue pares (x, y) numéricos. Ambos vectores deben tener la misma longitud."
        )
        subtitle.setObjectName("Subtitle")
        subtitle.setWordWrap(True)

        self._error = QLabel("")
        self._error.setObjectName("Error")
        self._error.setWordWrap(True)

        self._table = QTableView()
        self._table.setModel(self.model)
        self._table.setAlternatingRowColors(True)
        self._table.horizontalHeader().setStretchLastSection(True)

        add_btn = QPushButton("Agregar fila")
        del_btn = QPushButton("Eliminar fila")
        del_btn.setObjectName("Danger")
        calc_btn = QPushButton("Calcular ajustes")
        calc_btn.setObjectName("Primary")
        add_btn.clicked.connect(self.model.add_row)
        del_btn.clicked.connect(self._remove_selected)
        calc_btn.clicked.connect(self._emit_calculate)

        buttons = QHBoxLayout()
        buttons.addWidget(add_btn)
        buttons.addWidget(del_btn)
        buttons.addStretch()
        buttons.addWidget(calc_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self._error)
        layout.addWidget(self._table, 1)
        layout.addLayout(buttons)

    def show_error(self, message: str) -> None:
        self._error.setText(message)

    def clear_error(self) -> None:
        self._error.setText("")

    def load_pairs(self, x: list[float], y: list[float]) -> None:
        self.model.set_pairs(x, y)
        self.clear_error()

    def current_pairs(self) -> tuple[list[float], list[float]]:
        return self.model.numeric_pairs()

    def _remove_selected(self) -> None:
        rows = {index.row() for index in self._table.selectionModel().selectedIndexes()}
        if not rows:
            current = self._table.currentIndex().row()
            if current >= 0:
                rows = {current}
        self.model.remove_rows_at(list(rows))

    def _emit_calculate(self) -> None:
        try:
            x, y = self.model.numeric_pairs()
        except DatasetError as exc:
            self.show_error(str(exc))
            return
        self.clear_error()
        self.calculate_requested.emit(x, y)
