"""Los CSV de examples/ coinciden con los conjuntos embebidos."""

from pathlib import Path

from aproxlab.services.csv_io import load_xy_csv
from aproxlab.services.examples import CANONICAL_LINEAR, CANONICAL_QUADRATIC

ROOT = Path(__file__).resolve().parents[1] / "examples"


def test_example_csv_matches_canonical_linear() -> None:
    x, y = load_xy_csv(ROOT / "lineal_canonico.csv")
    assert x == list(CANONICAL_LINEAR.x)
    assert y == list(CANONICAL_LINEAR.y)


def test_example_csv_matches_canonical_quadratic() -> None:
    x, y = load_xy_csv(ROOT / "cuadratico_canonico.csv")
    assert x == list(CANONICAL_QUADRATIC.x)
    assert y == list(CANONICAL_QUADRATIC.y)
