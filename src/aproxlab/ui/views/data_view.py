"""Ingreso y validación visual de pares (x, y)."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTableView, QVBoxLayout, QWidget

from aproxlab.core.exceptions import DatasetError
from aproxlab.ui.widgets.dataset_model import DatasetTableModel


class DataView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.model = DatasetTableModel(self)
        heading = QLabel("Datos (x, y)")
        heading.setObjectName("Title")
        self._count = QLabel("n = 0")
        self._count.setObjectName("Subtitle")
        header = QHBoxLayout()
        header.addWidget(heading)
        header.addStretch()
        header.addWidget(self._count)

        self._error = QLabel("")
        self._error.setObjectName("Error")
        self._error.setWordWrap(True)

        self._table = QTableView()
        self._table.setModel(self.model)
        self._table.setAlternatingRowColors(True)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setDefaultSectionSize(26)
        self.model.dataChanged.connect(lambda *_: self._refresh_count())
        self.model.modelReset.connect(self._refresh_count)
        self.model.rowsInserted.connect(lambda *_: self._refresh_count())
        self.model.rowsRemoved.connect(lambda *_: self._refresh_count())

        add_btn = QPushButton("Agregar fila")
        del_btn = QPushButton("Eliminar fila")
        del_btn.setObjectName("Danger")
        add_btn.clicked.connect(self.model.add_row)
        del_btn.clicked.connect(self._remove_selected)

        buttons = QHBoxLayout()
        buttons.addWidget(add_btn)
        buttons.addWidget(del_btn)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        layout.addLayout(header)
        layout.addWidget(self._error)
        layout.addWidget(self._table, 1)
        layout.addLayout(buttons)
        self._refresh_count()

    def show_error(self, message: str) -> None:
        self._error.setText(message)

    def clear_error(self) -> None:
        self._error.setText("")

    def load_pairs(self, x: list[float], y: list[float]) -> None:
        self.model.set_pairs(x, y)
        self.clear_error()
        self._refresh_count()

    def current_pairs(self) -> tuple[list[float], list[float]]:
        return self.model.numeric_pairs()

    def _refresh_count(self) -> None:
        try:
            x, y = self.model.numeric_pairs()
        except DatasetError:
            filled = 0
            for row in range(self.model.rowCount()):
                x_raw = str(self.model.data(self.model.index(row, 0)) or "").strip()
                y_raw = str(self.model.data(self.model.index(row, 1)) or "").strip()
                if x_raw or y_raw:
                    filled += 1
            self._count.setText(f"filas = {filled}")
            return
        self._count.setText(f"n = {len(x)}")

    def _remove_selected(self) -> None:
        rows = {index.row() for index in self._table.selectionModel().selectedIndexes()}
        if not rows:
            current = self._table.currentIndex().row()
            if current >= 0:
                rows = {current}
        self.model.remove_rows_at(list(rows))
