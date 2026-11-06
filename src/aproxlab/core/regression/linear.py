"""Regresión lineal simple por mínimos cuadrados ordinarios."""

from __future__ import annotations

import numpy as np

from aproxlab.core.exceptions import DegenerateDesignError
from aproxlab.core.regression.base import FitResult, format_polynomial_equation
from aproxlab.core.validation import prepare_dataset, require_min_points


class LinearRegression:
    """Ajusta y = a0 + a1 x resolviendo el sistema sobredeterminado con lstsq."""

    name = "Lineal"
    min_points = 2
    degree = 1

    def fit(self, x: np.ndarray | list[float], y: np.ndarray | list[float]) -> FitResult:
        x_arr, y_arr = prepare_dataset(x, y)
        require_min_points(x_arr.size, minimum=self.min_points, method="lineal")
        if np.unique(x_arr).size < 2:
            raise DegenerateDesignError(
                "No se puede ajustar una recta: se requieren al menos dos valores distintos de x."
            )
        design = np.column_stack((np.ones(x_arr.size), x_arr))
        if np.linalg.matrix_rank(design) < 2:
            raise DegenerateDesignError(
                "No se puede ajustar una recta: las columnas de diseño son linealmente dependientes."
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
