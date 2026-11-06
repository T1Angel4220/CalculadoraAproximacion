"""Indicadores de error y bondad de ajuste."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


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
    y: np.ndarray | list[float],
    y_hat: np.ndarray | list[float],
    *,
    parameter_count: int,
    x: np.ndarray | list[float] | None = None,
) -> FitMetrics:
    """Calcula SSE, SST, R², Syx y, si hay x, la correlación de Pearson r(x, y)."""
    y_arr = np.asarray(y, dtype=float)
    y_hat_arr = np.asarray(y_hat, dtype=float)
    n = int(y_arr.size)
    residuals = y_arr - y_hat_arr
    sse = float(np.dot(residuals, residuals))
    centered = y_arr - float(np.mean(y_arr))
    sst = float(np.dot(centered, centered))

    r_squared = _r_squared(sse, sst)
    adjusted = _adjusted_r_squared(sse, sst, n, parameter_count)
    std_error = _std_error(sse, n, parameter_count)
    correlation = _pearson(x, y_arr) if x is not None else None

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


def _r_squared(sse: float, sst: float) -> float | None:
    if sst <= 1e-15:
        return None
    return 1.0 - sse / sst


def _adjusted_r_squared(sse: float, sst: float, n: int, p: int) -> float | None:
    if sst <= 1e-15 or n <= p or n <= 1:
        return None
    return 1.0 - (sse / (n - p)) / (sst / (n - 1))


def _std_error(sse: float, n: int, p: int) -> float | None:
    dof = n - p
    if dof <= 0:
        return None
    return float(np.sqrt(sse / dof))


def _pearson(x: np.ndarray | list[float], y: np.ndarray) -> float | None:
    x_arr = np.asarray(x, dtype=float)
    if x_arr.size != y.size:
        return None
    if np.std(x_arr) <= 1e-15 or np.std(y) <= 1e-15:
        return None
    corr = float(np.corrcoef(x_arr, y)[0, 1])
    if not np.isfinite(corr):
        return None
    return corr
