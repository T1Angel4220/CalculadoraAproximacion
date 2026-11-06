"""Tabla compacta símbolo / significado / valor."""

from __future__ import annotations

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem


class ParameterTable(QTableWidget):
    def __init__(self, rows: list[tuple[str, str]], parent=None) -> None:
        super().__init__(len(rows), 3, parent)
        self.setHorizontalHeaderLabels(["Símbolo", "Significado", "Valor"])
        self.verticalHeader().hide()
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.setShowGrid(True)
        for i, (symbol, meaning) in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(symbol))
            self.setItem(i, 1, QTableWidgetItem(meaning))
            self.setItem(i, 2, QTableWidgetItem("—"))
            self.setRowHeight(i, 24)
        self._fit_height()

    def set_values(self, values: list[str]) -> None:
        for i, value in enumerate(values):
            self.setItem(i, 2, QTableWidgetItem(value))
        self._fit_height()

    def _fit_height(self) -> None:
        header = self.horizontalHeader().height()
        rows = sum(self.rowHeight(i) for i in range(self.rowCount()))
        self.setFixedHeight(header + rows + 4)
