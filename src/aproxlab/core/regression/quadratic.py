"""Regresión polinomial de grado 2 por mínimos cuadrados (lstsq)."""

from __future__ import annotations

import numpy as np

from aproxlab.core.exceptions import DegenerateDesignError
from aproxlab.core.regression.base import FitResult, format_polynomial_equation
from aproxlab.core.validation import prepare_dataset, require_min_points


class QuadraticRegression:
    """Ajusta y = a0 + a1 x + a2 x² sin invertir explícitamente la matriz normal."""

    name = "Cuadrático"
    min_points = 3
    degree = 2

    def fit(self, x: np.ndarray | list[float], y: np.ndarray | list[float]) -> FitResult:
        x_arr, y_arr = prepare_dataset(x, y)
        require_min_points(x_arr.size, minimum=self.min_points, method="cuadrático")
        if np.unique(x_arr).size < 3:
            raise DegenerateDesignError(
                "El ajuste cuadrático requiere al menos tres valores distintos de x."
            )
        design = np.column_stack((np.ones(x_arr.size), x_arr, x_arr**2))
        if np.linalg.matrix_rank(design) < 3:
            raise DegenerateDesignError(
                "No se puede ajustar un polinomio de grado 2 de forma única con estos x."
            )
        coeffs, *_ = np.linalg.lstsq(design, y_arr, rcond=None)
        y_hat = design @ coeffs
        residuals = y_arr - y_hat
        return FitResult(
            name=self.name,
            degree=self.degree,
            coefficients=coeffs,
            y_hat=y_hat,
            residuals=residuals,
            equation=format_polynomial_equation(coeffs),
        )
