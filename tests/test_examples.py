"""Los CSV de examples/ coinciden con los conjuntos embebidos."""

from pathlib import Path

from aproxlab.services.csv_io import load_xy_csv
from aproxlab.services.examples import (
    CANONICAL_LINEAR,
    CANONICAL_QUADRATIC,
    CLASS_LINEAR,
    example_by_key,
)

ROOT = Path(__file__).resolve().parents[1] / "examples"


def test_classroom_example_is_used_for_linear_and_quadratic() -> None:
    example = example_by_key("class_linear")
    assert example is CLASS_LINEAR
    assert list(example.x) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(example.y) == [1, 1.5, 2, 3, 4, 5, 8, 10, 13]
    assert "lineal" in example.title.lower()
    assert "cuadrático" in example.title.lower()


def test_example_csv_matches_canonical_linear() -> None:
    x, y = load_xy_csv(ROOT / "lineal_canonico.csv")
    assert x == list(CANONICAL_LINEAR.x)
    assert y == list(CANONICAL_LINEAR.y)


def test_example_csv_matches_canonical_quadratic() -> None:
    x, y = load_xy_csv(ROOT / "cuadratico_canonico.csv")
    assert x == list(CANONICAL_QUADRATIC.x)
    assert y == list(CANONICAL_QUADRATIC.y)
