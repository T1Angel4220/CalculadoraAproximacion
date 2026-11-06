"""Ajuste de tablas de reporte para que no se aplasten ni muestren scroll interno."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QTableWidget


def configure_report_table(table: QTableWidget) -> None:
    table.verticalHeader().hide()
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.setWordWrap(False)
    table.setTextElideMode(Qt.TextElideMode.ElideNone)
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    table.setAlternatingRowColors(True)
    table.setShowGrid(True)


def fit_table_height(table: QTableWidget) -> None:
    table.resizeRowsToContents()
    header = max(table.horizontalHeader().height(), 28)
    body = sum(max(table.rowHeight(i), 28) for i in range(table.rowCount()))
    frame = table.frameWidth() * 2
    table.setFixedHeight(header + body + frame + 8)
