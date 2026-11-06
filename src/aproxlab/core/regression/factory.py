"""Fábrica simple de estrategias de ajuste."""

from __future__ import annotations

from aproxlab.core.regression.base import RegressionStrategy
from aproxlab.core.regression.linear import LinearRegression
from aproxlab.core.regression.quadratic import QuadraticRegression

_STRATEGIES: dict[str, type] = {
    "linear": LinearRegression,
    "lineal": LinearRegression,
    "quadratic": QuadraticRegression,
    "cuadratico": QuadraticRegression,
    "cuadrático": QuadraticRegression,
}


def create_strategy(kind: str) -> RegressionStrategy:
    """Crea una estrategia por identificador (lineal / cuadrático)."""
    try:
        cls = _STRATEGIES[kind.lower()]
    except KeyError as exc:
        known = ", ".join(sorted(set(_STRATEGIES)))
        raise ValueError(f"Modelo desconocido '{kind}'. Opciones: {known}.") from exc
    return cls()
