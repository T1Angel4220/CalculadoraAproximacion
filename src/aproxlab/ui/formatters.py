"""Presentación numérica de laboratorio (sin notación científica innecesaria)."""

from __future__ import annotations

import math

_ZERO_ABS = 1e-12
_FIXED_DECIMALS = 8
_SCI_ABS = 1e7


def fmt_number(value: float | None, *, digits: int = _FIXED_DECIMALS) -> str:
    """Formatea un real para tablas de métodos numéricos.

    Residuos menores que 1e-12 se muestran como 0. Se evita `3.15e-16`.
    """
    if value is None or not math.isfinite(value):
        return "—"
    if abs(value) < _ZERO_ABS:
        return "0"
    if abs(value) >= _SCI_ABS:
        return f"{value:.{digits}g}"
    text = f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return text if text not in {"", "-0"} else "0"


def fmt_optional(value: float | None) -> str:
    return fmt_number(value)
