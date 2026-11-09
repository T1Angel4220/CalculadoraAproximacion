"""Regresión lineal por mínimos cuadrados, paso a paso, sin librerías numéricas."""

from __future__ import annotations

import math
from dataclasses import dataclass

from aproxlab.core.exceptions import DegenerateDesignError
from aproxlab.core.regression.base import FitResult, format_polynomial_equation
from aproxlab.core.validation import prepare_dataset, require_min_points


@dataclass(frozen=True, slots=True)
class ErrorRow:
    x: float
    y: float
    x2: float
    xy: float
    y_hat: float
    residual: float
    residual_sq: float


@dataclass(frozen=True, slots=True)
class LinearWorksheet:
    """Trazas del procedimiento de clase: sumatorias → a0, a1 → errores → Sr, St, r."""

    n: int
    sum_x: float
    sum_y: float
    sum_x2: float
    sum_xy: float
    mean_x: float
    mean_y: float
    a0: float
    a1: float
    sr: float
    st: float
    syx: float | None
    r_squared: float | None
    r: float | None
    r_interpretation: str
    error_rows: tuple[ErrorRow, ...]


def interpret_correlation(r: float | None) -> str:
    """Interpreta r según las bandas pedidas por el curso."""
    if r is None:
        return "No definido (St = 0 o x constante)"
    if r >= 0.5:
        return "Correlación positiva fuerte (0.5 ≤ r ≤ 1)"
    if r >= 0:
        return "Correlación positiva débil (0 ≤ r < 0.5)"
    if r > -0.5:
        return "Correlación negativa débil (-0.5 < r < 0)"
    return "Correlación negativa fuerte (-1 ≤ r ≤ -0.5)"


def _sum(values: list[float]) -> float:
    total = 0.0
    for value in values:
        total += value
    return total


class LinearRegression:
    """Ajusta ŷ = a0 + a1 x con sumatorias explícitas (no NumPy, no lstsq)."""

    name = "Lineal"
    min_points = 2
    degree = 1

    def fit(self, x: list[float], y: list[float]) -> FitResult:
        x_arr, y_arr = prepare_dataset(x, y)
        xs = [float(v) for v in x_arr]
        ys = [float(v) for v in y_arr]
        n = len(xs)
        require_min_points(n, minimum=self.min_points, method="lineal")
        if len(set(xs)) < 2:
            raise DegenerateDesignError(
                "No se puede ajustar una recta: se requieren al menos dos valores distintos de x."
            )

        # 1. Sumatorias
        sum_x = _sum(xs)
        sum_y = _sum(ys)
        x2 = [xi * xi for xi in xs]
        xy = [xs[i] * ys[i] for i in range(n)]
        sum_x2 = _sum(x2)
        sum_xy = _sum(xy)

        # 2. Medias aritméticas
        mean_x = sum_x / n
        mean_y = sum_y / n

        # 3. Coeficientes a1 (pendiente) y a0 (intersección)
        denom = n * sum_x2 - sum_x * sum_x
        if abs(denom) < 1e-15:
            raise DegenerateDesignError(
                "No se puede ajustar una recta: el denominador de a1 es cero."
            )
        a1 = (n * sum_xy - sum_x * sum_y) / denom
        a0 = mean_y - a1 * mean_x

        # 4. Tabla de errores: ŷ, e, e²
        y_hat = [a0 + a1 * xs[i] for i in range(n)]
        residuals = [ys[i] - y_hat[i] for i in range(n)]
        residual_sq = [residuals[i] * residuals[i] for i in range(n)]
        error_rows = tuple(
            ErrorRow(
                x=xs[i],
                y=ys[i],
                x2=x2[i],
                xy=xy[i],
                y_hat=y_hat[i],
                residual=residuals[i],
                residual_sq=residual_sq[i],
            )
            for i in range(n)
        )

        # 5. Sr (suma de residuos al cuadrado) y St (suma total)
        sr = _sum(residual_sq)
        st = _sum([(ys[i] - mean_y) ** 2 for i in range(n)])

        # 6. Error estándar Sy/x
        syx = math.sqrt(sr / (n - 2)) if n > 2 else None

        # 7. Coeficiente de determinación r² = (St - Sr) / St
        r_squared = (st - sr) / st if st > 1e-15 else None

        # 8. Coeficiente de correlación r = signo(a1) √r²
        if r_squared is None:
            r = None
        else:
            r = math.copysign(math.sqrt(max(r_squared, 0.0)), a1)

        worksheet = LinearWorksheet(
            n=n,
            sum_x=sum_x,
            sum_y=sum_y,
            sum_x2=sum_x2,
            sum_xy=sum_xy,
            mean_x=mean_x,
            mean_y=mean_y,
            a0=a0,
            a1=a1,
            sr=sr,
            st=st,
            syx=syx,
            r_squared=r_squared,
            r=r,
            r_interpretation=interpret_correlation(r),
            error_rows=error_rows,
        )
        coeffs = (a0, a1)
        return FitResult(
            name=self.name,
            degree=self.degree,
            coefficients=coeffs,
            y_hat=tuple(y_hat),
            residuals=tuple(residuals),
            equation=format_polynomial_equation(coeffs),
            worksheet=worksheet,
        )
