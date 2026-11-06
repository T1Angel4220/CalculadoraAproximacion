"""Formato de números y métricas para la interfaz."""

from __future__ import annotations


def fmt_number(value: float | None, *, digits: int = 6) -> str:
    if value is None:
        return "No definido"
    if abs(value) == 0:
        return "0"
    text = f"{value:.{digits}g}"
    return text


def fmt_optional(value: float | None) -> str:
    return fmt_number(value) if value is not None else "No definido"
