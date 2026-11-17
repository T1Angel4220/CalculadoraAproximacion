"""Álgebra elemental a mano (sin NumPy): Gauss-Jordan con cada operación."""

from __future__ import annotations

from dataclasses import dataclass

_PIVOT_EPS = 1e-12


@dataclass(frozen=True, slots=True)
class GaussStep:
    """Una operación elemental y la matriz aumentada que queda después."""

    operation: str
    matrix: tuple[tuple[float, ...], ...]


def gauss_solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Resuelve A x = b y devuelve solo la solución."""
    solution, _steps = gauss_jordan_steps(matrix, rhs)
    return solution


def gauss_jordan_steps(
    matrix: list[list[float]], rhs: list[float]
) -> tuple[list[float], tuple[GaussStep, ...]]:
    """Gauss-Jordan de clase: pivote a 1, ceros debajo y luego ceros encima.

    No usa librerías. Cada operación elemental queda registrada.
    """
    n = len(rhs)
    aug = [row[:] + [float(rhs[i])] for i, row in enumerate(matrix)]
    steps: list[GaussStep] = []

    for col in range(n):
        _ensure_pivot(aug, col, steps)
        pivot = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= pivot
        steps.append(_step(f"F{col + 1} ← F{col + 1} / {_num(pivot)}", aug))
        for row in range(col + 1, n):
            _eliminate(aug, row, col, steps)

    for col in range(n - 1, -1, -1):
        for row in range(col - 1, -1, -1):
            _eliminate(aug, row, col, steps)

    return [aug[i][n] for i in range(n)], tuple(steps)


def _ensure_pivot(aug: list[list[float]], col: int, steps: list[GaussStep]) -> None:
    """Usa el pivote de la diagonal, como en clase. Solo intercambia si es cero."""
    if abs(aug[col][col]) >= _PIVOT_EPS:
        return
    pivot_row = None
    for row in range(col + 1, len(aug)):
        if abs(aug[row][col]) >= _PIVOT_EPS:
            pivot_row = row
            break
    if pivot_row is None:
        raise ZeroDivisionError("El sistema es singular.")
    aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
    steps.append(_step(f"Intercambio F{col + 1} ↔ F{pivot_row + 1}", aug))


def _eliminate(aug: list[list[float]], row: int, col: int, steps: list[GaussStep]) -> None:
    factor = aug[row][col]
    if abs(factor) < _PIVOT_EPS:
        return
    width = len(aug[row])
    for j in range(col, width):
        aug[row][j] -= factor * aug[col][j]
    steps.append(
        _step(
            f"F{row + 1} ← F{row + 1} − ({_num(factor)}) F{col + 1}",
            aug,
        )
    )


def _step(operation: str, aug: list[list[float]]) -> GaussStep:
    return GaussStep(operation, tuple(tuple(cell) for cell in aug))


def _num(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.8g}"
