"""Modelo Qt de pares (x, y) editables."""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from aproxlab.core.exceptions import InsufficientDataError, NonNumericDataError

_HEADERS = ("x", "y")


class DatasetTableModel(QAbstractTableModel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._rows: list[list[str]] = [["", ""] for _ in range(5)]

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        if parent is not None and parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        if parent is not None and parent.isValid():
            return 0
        return 2

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return _HEADERS[section]
        return str(section + 1)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self._rows[index.row()][index.column()]
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole) -> bool:  # noqa: N802
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        self._rows[index.row()][index.column()] = str(value).strip()
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
        return True

    def add_row(self) -> None:
        row = len(self._rows)
        self.beginInsertRows(QModelIndex(), row, row)
        self._rows.append(["", ""])
        self.endInsertRows()

    def remove_rows_at(self, rows: list[int]) -> None:
        for row in sorted(set(rows), reverse=True):
            if 0 <= row < len(self._rows):
                self.beginRemoveRows(QModelIndex(), row, row)
                del self._rows[row]
                self.endRemoveRows()
        if not self._rows:
            self.add_row()

    def set_pairs(self, x: list[float], y: list[float]) -> None:
        self.beginResetModel()
        self._rows = [[_fmt(xi), _fmt(yi)] for xi, yi in zip(x, y, strict=True)]
        if not self._rows:
            self._rows = [["", ""]]
        self.endResetModel()

    def numeric_pairs(self) -> tuple[list[float], list[float]]:
        xs: list[float] = []
        ys: list[float] = []
        for i, (x_raw, y_raw) in enumerate(self._rows, start=1):
            if x_raw == "" and y_raw == "":
                continue
            if x_raw == "" or y_raw == "":
                raise NonNumericDataError(
                    f"La fila {i} está incompleta: x e y deben completarse juntos."
                )
            xs.append(_parse(x_raw, i, "x"))
            ys.append(_parse(y_raw, i, "y"))
        if not xs:
            raise InsufficientDataError("No hay pares (x, y) para analizar.")
        return xs, ys


def _parse(raw: str, row: int, axis: str) -> float:
    try:
        return float(raw.replace(",", "."))
    except ValueError as exc:
        raise NonNumericDataError(f"Valor no numérico en {axis} (fila {row}): '{raw}'.") from exc


def _fmt(value: float) -> str:
    if abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    return f"{value:g}"
