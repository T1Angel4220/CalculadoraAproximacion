"""Contrato compartido de las estrategias de regresión."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True, slots=True)
class FitResult:
    """Resultado de un ajuste por mínimos cuadrados."""

    name: str
    degree: int
    coefficients: np.ndarray
    y_hat: np.ndarray
    residuals: np.ndarray
    equation: str


class RegressionStrategy(Protocol):
    """Algoritmo intercambiable de aproximación funcional."""

    name: str
    min_points: int
    degree: int

    def fit(self, x: np.ndarray | list[float], y: np.ndarray | list[float]) -> FitResult:
        """Ajusta el modelo y devuelve coeficientes, ŷ y residuos."""
        ...


def format_polynomial_equation(coefficients: np.ndarray) -> str:
    """Formatea y = a0 + a1 x + a2 x^2 … omitiendo términos nulos."""
    terms: list[str] = []
    for power, coef in enumerate(coefficients):
        if abs(coef) < 1e-12:
            continue
        piece = _term(power, coef, leading=not terms)
        terms.append(piece)
    if not terms:
        return "y = 0"
    return "y = " + "".join(terms)


def _term(power: int, coef: float, *, leading: bool) -> str:
    mag = abs(coef)
    mag_txt = _format_number(mag)
    if power == 0:
        body = mag_txt
    elif abs(mag - 1.0) < 1e-12:
        body = "x" if power == 1 else f"x^{power}"
    else:
        body = f"{mag_txt}x" if power == 1 else f"{mag_txt}x^{power}"

    if leading:
        return f"-{body}" if coef < 0 else body
    sign = " - " if coef < 0 else " + "
    return sign + body


def _format_number(value: float) -> str:
    if abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    text = f"{value:.10g}"
    return text
