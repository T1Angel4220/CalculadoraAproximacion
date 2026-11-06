"""Construcción de gráficas científicas sobre ejes Matplotlib (sin Qt)."""

from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes

from aproxlab.core.regression.base import FitResult

_N_CURVE = 200


def dense_curve(x: np.ndarray, result: FitResult) -> tuple[np.ndarray, np.ndarray]:
    """Evalúa el polinomio ajustado en una malla densa para dibujar la curva."""
    x_min, x_max = float(np.min(x)), float(np.max(x))
    span = x_max - x_min
    padding = 0.05 * span if span > 0 else 1.0
    grid = np.linspace(x_min - padding, x_max + padding, _N_CURVE)
    y_grid = np.zeros_like(grid)
    for power, coef in enumerate(result.coefficients):
        y_grid += coef * grid**power
    return grid, y_grid


def plot_scatter_and_fits(
    ax: Axes,
    x: np.ndarray,
    y: np.ndarray,
    fits: list[tuple[FitResult, str]],
    *,
    title: str,
) -> None:
    """Dibuja puntos observados y una o más curvas de ajuste."""
    ax.clear()
    ax.scatter(x, y, s=42, zorder=3, label="Datos observados", color="#38bdf8")
    for result, color in fits:
        grid, y_grid = dense_curve(x, result)
        ax.plot(grid, y_grid, linewidth=2.2, color=color, label=result.name)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.25)
    ax.figure.tight_layout()
