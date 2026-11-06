"""Construcción de gráficas científicas sobre ejes Matplotlib (sin Qt)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from matplotlib.axes import Axes

from aproxlab.core.regression.base import FitResult


@dataclass(frozen=True, slots=True)
class PlotPalette:
    face: str
    text: str
    grid: str
    scatter: str
    linear: str
    quadratic: str


def plot_palette(theme_name: str) -> PlotPalette:
    """Colores de Matplotlib para tema claro u oscuro."""
    if theme_name == "light":
        return PlotPalette(
            face="#f8fafc",
            text="#0f172a",
            grid="#cbd5e1",
            scatter="#0369a1",
            linear="#c2410c",
            quadratic="#047857",
        )
    return PlotPalette(
        face="#101418",
        text="#e7ecf3",
        grid="#334155",
        scatter="#38bdf8",
        linear="#f59e0b",
        quadratic="#34d399",
    )


_N_CURVE = 200


def dense_curve(x: np.ndarray, result: FitResult) -> tuple[np.ndarray, np.ndarray]:
    """Evalúa el polinomio ajustado en una malla densa para dibujar la curva."""
    x_min, x_max = float(np.min(x)), float(np.max(x))
    span = x_max - x_min
    padding = 0.08 * span if span > 0 else 1.0
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
    palette: PlotPalette | None = None,
) -> None:
    """Dibuja puntos observados y una o más curvas de ajuste."""
    style = palette or plot_palette("dark")
    ax.clear()
    ax.figure.patch.set_facecolor(style.face)
    ax.set_facecolor(style.face)
    ax.scatter(
        x,
        y,
        s=56,
        zorder=3,
        label="Datos observados",
        color=style.scatter,
        edgecolors=style.face,
        linewidths=0.6,
    )
    for result, color in fits:
        grid, y_grid = dense_curve(x, result)
        ax.plot(grid, y_grid, linewidth=2.4, color=color, label=result.name)
    ax.set_title(title, color=style.text, pad=10)
    ax.set_xlabel("x", color=style.text)
    ax.set_ylabel("y", color=style.text)
    ax.tick_params(colors=style.text)
    for spine in ax.spines.values():
        spine.set_color(style.grid)
    ax.grid(True, color=style.grid, alpha=0.55, linestyle="--")
    legend = ax.legend(
        loc="upper left",
        frameon=True,
        fancybox=False,
        framealpha=0.92,
        edgecolor=style.grid,
        facecolor=style.face,
    )
    for text in legend.get_texts():
        text.set_color(style.text)
