"""Regresión polinomial de grado 2 con ecuaciones normales y Gauss, sin lstsq."""

from __future__ import annotations

from aproxlab.core.algebra import gauss_solve
from aproxlab.core.exceptions import DegenerateDesignError
from aproxlab.core.regression.base import FitResult, format_polynomial_equation
from aproxlab.core.validation import prepare_dataset, require_min_points


def _sum(values: list[float]) -> float:
    total = 0.0
    for value in values:
        total += value
    return total


class QuadraticRegression:
    """Ajusta ŷ = a0 + a1 x + a2 x² resolviendo el sistema 3×3 a mano."""

    name = "Cuadrático"
    min_points = 3
    degree = 2

    def fit(self, x: list[float], y: list[float]) -> FitResult:
        x_arr, y_arr = prepare_dataset(x, y)
        xs = [float(v) for v in x_arr]
        ys = [float(v) for v in y_arr]
        n = len(xs)
        require_min_points(n, minimum=self.min_points, method="cuadrático")
        if len(set(xs)) < 3:
            raise DegenerateDesignError(
                "El ajuste cuadrático requiere al menos tres valores distintos de x."
            )

        sum_x = _sum(xs)
        sum_y = _sum(ys)
        sum_x2 = _sum([xi * xi for xi in xs])
        sum_x3 = _sum([xi**3 for xi in xs])
        sum_x4 = _sum([xi**4 for xi in xs])
        sum_xy = _sum([xs[i] * ys[i] for i in range(n)])
        sum_x2y = _sum([(xs[i] ** 2) * ys[i] for i in range(n)])

        # Sistema normal 3×3 (sin invertir matrices con librerías).
        matrix = [
            [float(n), sum_x, sum_x2],
            [sum_x, sum_x2, sum_x3],
            [sum_x2, sum_x3, sum_x4],
        ]
        rhs = [sum_y, sum_xy, sum_x2y]
        try:
            a0, a1, a2 = gauss_solve(matrix, rhs)
        except ZeroDivisionError as exc:
            raise DegenerateDesignError(
                "No se puede ajustar un polinomio de grado 2 de forma única con estos x."
            ) from exc

        y_hat = [a0 + a1 * xs[i] + a2 * xs[i] * xs[i] for i in range(n)]
        residuals = [ys[i] - y_hat[i] for i in range(n)]
        coeffs = (a0, a1, a2)
        return FitResult(
            name=self.name,
            degree=self.degree,
            coefficients=coeffs,
            y_hat=tuple(y_hat),
            residuals=tuple(residuals),
            equation=format_polynomial_equation(coeffs),
        )
