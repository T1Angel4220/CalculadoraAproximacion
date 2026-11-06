"""Ingreso y validación de pares (x, y)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from aproxlab.core.exceptions import (
    DegenerateDesignError,
    InsufficientDataError,
    LengthMismatchError,
    NonNumericDataError,
)

ArrayLike = Sequence[object] | np.ndarray


def prepare_dataset(
    x: ArrayLike,
    y: ArrayLike,
    *,
    min_distinct_x: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    """Convierte y valida vectores x, y de igual longitud, numéricos y finitos."""
    x_arr = _to_finite_vector(x, axis_name="x")
    y_arr = _to_finite_vector(y, axis_name="y")
    if x_arr.size != y_arr.size:
        raise LengthMismatchError(
            f"x tiene {x_arr.size} valores e y tiene {y_arr.size}; deben coincidir."
        )
    distinct = np.unique(x_arr).size
    if distinct < min_distinct_x:
        raise DegenerateDesignError(
            f"Se requieren al menos {min_distinct_x} valores distintos de x (hay {distinct})."
        )
    return x_arr, y_arr


def require_min_points(n: int, *, minimum: int, method: str) -> None:
    """Exige un número mínimo de observaciones para un método de ajuste."""
    if n < minimum:
        raise InsufficientDataError(
            f"El ajuste {method} requiere al menos {minimum} puntos; se recibieron {n}."
        )


def _to_finite_vector(values: ArrayLike, *, axis_name: str) -> np.ndarray:
    try:
        array = np.asarray(list(values), dtype=float)
    except (TypeError, ValueError) as exc:
        raise NonNumericDataError(f"Todos los valores de {axis_name} deben ser numéricos.") from exc
    if array.ndim != 1:
        raise NonNumericDataError(f"{axis_name} debe ser un vector unidimensional.")
    if not np.all(np.isfinite(array)):
        raise NonNumericDataError(
            f"Los valores de {axis_name} deben ser finitos (sin NaN ni infinitos)."
        )
    return array
