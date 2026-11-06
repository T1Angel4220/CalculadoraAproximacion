"""Navegación lateral del menú principal."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout

PAGES = (
    "Datos",
    "Ajuste lineal",
    "Ajuste cuadrático",
    "Comparación",
    "Gráficas",
    "Fórmulas",
)


class Sidebar(QFrame):
    page_changed = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(228)
        brand = QLabel("AproxLab")
        brand.setObjectName("Title")
        caption = QLabel("Aproximación funcional")
        caption.setObjectName("Subtitle")
        self._list = QListWidget()
        for title in PAGES:
            QListWidgetItem(title, self._list)
        self._list.setCurrentRow(0)
        self._list.currentRowChanged.connect(self.page_changed.emit)
        layout = QVBoxLayout(self)
        layout.addWidget(brand)
        layout.addWidget(caption)
        layout.addSpacing(12)
        layout.addWidget(self._list)
        layout.addStretch()
