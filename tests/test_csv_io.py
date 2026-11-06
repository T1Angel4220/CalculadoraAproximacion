"""Importación y exportación de pares (x, y) en CSV."""

from pathlib import Path

import pytest

from aproxlab.core.exceptions import NonNumericDataError
from aproxlab.services.csv_io import export_xy_csv, load_xy_csv


def test_load_xy_csv_reads_header_and_rows(tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text("x,y\n0,1\n1,3\n2,5\n", encoding="utf-8")

    x, y = load_xy_csv(path)

    assert x == [0.0, 1.0, 2.0]
    assert y == [1.0, 3.0, 5.0]


def test_load_xy_csv_rejects_non_numeric_cells(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("x,y\n1,foo\n", encoding="utf-8")

    with pytest.raises(NonNumericDataError):
        load_xy_csv(path)


def test_export_xy_csv_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    export_xy_csv(path, [0, 1], [1, 3])
    x, y = load_xy_csv(path)
    assert x == [0.0, 1.0]
    assert y == [1.0, 3.0]
