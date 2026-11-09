"""Indicadores de error con bucles explícitos (sin NumPy)."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FitMetrics:
    """Métricas derivadas de y, ŷ y el número de parámetros p."""

    sse: float
    sst: float
    r_squared: float | None
    correlation: float | None
    std_error: float | None
    n: int
    parameter_count: int
    adjusted_r_squared: float | None


def compute_metrics(
    y: list[float],
    y_hat: list[float],
    *,
    parameter_count: int,
    x: list[float] | None = None,
) -> FitMetrics:
    """Calcula Sr/SSE, St/SST, R², Syx y r con sumatorias a mano."""
    ys = [float(v) for v in y]
    preds = [float(v) for v in y_hat]
    n = len(ys)
    residuals = [ys[i] - preds[i] for i in range(n)]
    sse = 0.0
    for e in residuals:
        sse += e * e
    mean_y = 0.0
    for value in ys:
        mean_y += value
    mean_y /= n
    sst = 0.0
    for value in ys:
        diff = value - mean_y
        sst += diff * diff

    r_squared = (sst - sse) / sst if sst > 1e-15 else None
    adjusted = None
    if sst > 1e-15 and n > parameter_count and n > 1:
        adjusted = 1.0 - (sse / (n - parameter_count)) / (sst / (n - 1))
    std_error = math.sqrt(sse / (n - parameter_count)) if n > parameter_count else None
    correlation = _signed_r(r_squared, x, ys) if x is not None else None

    return FitMetrics(
        sse=sse,
        sst=sst,
        r_squared=r_squared,
        correlation=correlation,
        std_error=std_error,
        n=n,
        parameter_count=parameter_count,
        adjusted_r_squared=adjusted,
    )


def _signed_r(r_squared: float | None, x: list[float], y: list[float]) -> float | None:
    """r = signo(cov x,y) · √r², como en el procedimiento de clase."""
    if r_squared is None:
        return None
    n = len(x)
    xs = [float(v) for v in x]
    mean_x = 0.0
    mean_y = 0.0
    for i in range(n):
        mean_x += xs[i]
        mean_y += y[i]
    mean_x /= n
    mean_y /= n
    cov = 0.0
    for i in range(n):
        cov += (xs[i] - mean_x) * (y[i] - mean_y)
    return math.copysign(math.sqrt(max(r_squared, 0.0)), cov if cov != 0 else 1.0)
