"""Álgebra elemental a mano (sin NumPy): eliminación gaussiana."""

from __future__ import annotations


def gauss_solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Resuelve A x = b por Gauss-Jordan con pivoteo parcial."""
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = col
        best = abs(aug[col][col])
        for row in range(col + 1, n):
            if abs(aug[row][col]) > best:
                best = abs(aug[row][col])
                pivot = row
        if best < 1e-15:
            raise ZeroDivisionError("El sistema es singular.")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            for j in range(col, n + 1):
                aug[row][j] -= factor * aug[col][j]
    return [aug[i][n] for i in range(n)]
