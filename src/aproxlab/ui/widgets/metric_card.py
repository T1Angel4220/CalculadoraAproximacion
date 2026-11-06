"""Tarjeta compacta para un indicador numérico."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    def __init__(self, name: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self._name = QLabel(name)
        self._name.setObjectName("MetricName")
        self._value = QLabel("—")
        self._value.setObjectName("MetricValue")
        layout = QVBoxLayout(self)
        layout.addWidget(self._name)
        layout.addWidget(self._value)

    def set_value(self, text: str) -> None:
        self._value.setText(text)
