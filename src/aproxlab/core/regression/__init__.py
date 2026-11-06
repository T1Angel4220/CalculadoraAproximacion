"""Estrategias de regresión por mínimos cuadrados."""

from aproxlab.core.regression.base import FitResult, RegressionStrategy
from aproxlab.core.regression.factory import create_strategy
from aproxlab.core.regression.linear import LinearRegression
from aproxlab.core.regression.quadratic import QuadraticRegression

__all__ = [
    "FitResult",
    "LinearRegression",
    "QuadraticRegression",
    "RegressionStrategy",
    "create_strategy",
]
