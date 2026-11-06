"""Editor de celdas que solo admite números de laboratorio."""

from __future__ import annotations

import re

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit, QStyledItemDelegate

_NUMBER_PATTERN = re.compile(r"^-?[0-9]*[.,]?[0-9]*$")
_QT_PATTERN = r"^-?[0-9]*[.,]?[0-9]*$"


def is_allowed_number_text(text: str) -> bool:
    """True si el texto es vacío, signo o un real con punto o coma."""
    return _NUMBER_PATTERN.fullmatch(text) is not None


class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):  # noqa: N802, ARG002
        editor = QLineEdit(parent)
        editor.setValidator(QRegularExpressionValidator(QRegularExpression(_QT_PATTERN), editor))
        return editor
