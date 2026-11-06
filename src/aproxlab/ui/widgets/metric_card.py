"""Tarjeta de indicador al estilo del mockup académico."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class MetricCard(QFrame):
    def __init__(self, symbol: str, caption: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        head = QHBoxLayout()
        self._symbol = QLabel(symbol)
        self._symbol.setObjectName("MetricSymbol")
        self._caption = QLabel(caption)
        self._caption.setObjectName("MetricName")
        self._caption.setWordWrap(True)
        head.addWidget(self._symbol)
        head.addWidget(self._caption, 1)

        self._value = QLabel("—")
        self._value.setObjectName("MetricValue")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        layout.addLayout(head)
        layout.addWidget(self._value)

    def set_value(self, text: str) -> None:
        self._value.setText(text)
