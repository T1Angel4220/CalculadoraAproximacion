"""Tabla compacta símbolo / significado / valor."""

from __future__ import annotations

from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from aproxlab.ui.widgets.table_fit import configure_report_table, fit_table_height


class ParameterTable(QTableWidget):
    def __init__(self, rows: list[tuple[str, str]], parent=None) -> None:
        super().__init__(len(rows), 3, parent)
        self.setHorizontalHeaderLabels(["Indicador", "Descripción", "Valor"])
        configure_report_table(self)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        for i, (symbol, meaning) in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(symbol))
            self.setItem(i, 1, QTableWidgetItem(meaning))
            self.setItem(i, 2, QTableWidgetItem("—"))
        fit_table_height(self)

    def set_values(self, values: list[str]) -> None:
        for i, value in enumerate(values):
            self.setItem(i, 2, QTableWidgetItem(value))
        self.resizeColumnToContents(2)
        fit_table_height(self)
