"""Regresión de grado 2: sumatorias, sistema normal y Gauss-Jordan, sin librerías."""

from __future__ import annotations

import math
from dataclasses import dataclass

from aproxlab.core.algebra import GaussStep, gauss_jordan_steps
from aproxlab.core.exceptions import DegenerateDesignError
from aproxlab.core.regression.base import FitResult, format_polynomial_equation
from aproxlab.core.validation import prepare_dataset, require_min_points


@dataclass(frozen=True, slots=True)
class PowerRow:
    x: float
    y: float
    x2: float
    x3: float
    x4: float
    xy: float
    x2y: float


@dataclass(frozen=True, slots=True)
class QuadErrorRow:
    x: float
    y: float
    y_hat: float
    residual: float
    residual_sq: float


@dataclass(frozen=True, slots=True)
class QuadraticWorksheet:
    """Trazas de clase: sumatorias → sistema 3×3 → Gauss-Jordan → Sr, St, r²."""

    n: int
    sum_x: float
    sum_y: float
    sum_x2: float
    sum_x3: float
    sum_x4: float
    sum_xy: float
    sum_x2y: float
    mean_y: float
    power_rows: tuple[PowerRow, ...]
    augmented: tuple[tuple[float, float, float, float], ...]
    gauss_steps: tuple[GaussStep, ...]
    a0: float
    a1: float
    a2: float
    error_rows: tuple[QuadErrorRow, ...]
    sr: float
    st: float
    syx: float | None
    r_squared: float | None


def _sum(values: list[float]) -> float:
    total = 0.0
    for value in values:
        total += value
    return total


class QuadraticRegression:
    """Ajusta ŷ = a0 + a1 x + a2 x² con el procedimiento escrito a mano."""

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

        # 1. Sumatorias de potencias y productos
        x2 = [xi * xi for xi in xs]
        x3 = [x2[i] * xs[i] for i in range(n)]
        x4 = [x2[i] * x2[i] for i in range(n)]
        xy = [xs[i] * ys[i] for i in range(n)]
        x2y = [x2[i] * ys[i] for i in range(n)]
        sum_x = _sum(xs)
        sum_y = _sum(ys)
        sum_x2 = _sum(x2)
        sum_x3 = _sum(x3)
        sum_x4 = _sum(x4)
        sum_xy = _sum(xy)
        sum_x2y = _sum(x2y)
        power_rows = tuple(
            PowerRow(
                x=xs[i],
                y=ys[i],
                x2=x2[i],
                x3=x3[i],
                x4=x4[i],
                xy=xy[i],
                x2y=x2y[i],
            )
            for i in range(n)
        )

        # 2 y 3. Ecuaciones normales y matriz aumentada
        matrix = [
            [float(n), sum_x, sum_x2],
            [sum_x, sum_x2, sum_x3],
            [sum_x2, sum_x3, sum_x4],
        ]
        rhs = [sum_y, sum_xy, sum_x2y]
        augmented = tuple((matrix[i][0], matrix[i][1], matrix[i][2], rhs[i]) for i in range(3))

        # 4. Gauss-Jordan, operación por operación
        try:
            solution, gauss_steps = gauss_jordan_steps(matrix, rhs)
        except ZeroDivisionError as exc:
            raise DegenerateDesignError(
                "No se puede ajustar un polinomio de grado 2 de forma única con estos x."
            ) from exc
        a0, a1, a2 = solution

        # 5 y 6. ŷ = a0 + a1 x + a2 x², residuo y residuo²
        y_hat = [a0 + a1 * xs[i] + a2 * x2[i] for i in range(n)]
        residuals = [ys[i] - y_hat[i] for i in range(n)]
        residual_sq = [residuals[i] * residuals[i] for i in range(n)]
        error_rows = tuple(
            QuadErrorRow(
                x=xs[i],
                y=ys[i],
                y_hat=y_hat[i],
                residual=residuals[i],
                residual_sq=residual_sq[i],
            )
            for i in range(n)
        )

        # 7 y 8. Sr y St (St usa la media de y, igual que en la recta)
        sr = _sum(residual_sq)
        mean_y = sum_y / n
        st = _sum([(ys[i] - mean_y) * (ys[i] - mean_y) for i in range(n)])

        # 9. Error estándar del polinomio de grado 2: √(Sr / (n − 3))
        syx = math.sqrt(sr / (n - 3)) if n > 3 else None

        # 10. r² = (St − Sr) / St
        r_squared = (st - sr) / st if st > 1e-15 else None

        worksheet = QuadraticWorksheet(
            n=n,
            sum_x=sum_x,
            sum_y=sum_y,
            sum_x2=sum_x2,
            sum_x3=sum_x3,
            sum_x4=sum_x4,
            sum_xy=sum_xy,
            sum_x2y=sum_x2y,
            mean_y=mean_y,
            power_rows=power_rows,
            augmented=augmented,
            gauss_steps=gauss_steps,
            a0=a0,
            a1=a1,
            a2=a2,
            error_rows=error_rows,
            sr=sr,
            st=st,
            syx=syx,
            r_squared=r_squared,
        )
        coeffs = (a0, a1, a2)
        return FitResult(
            name=self.name,
            degree=self.degree,
            coefficients=coeffs,
            y_hat=tuple(y_hat),
            residuals=tuple(residuals),
            equation=format_polynomial_equation(coeffs),
            worksheet=worksheet,
        )
