"""Conjuntos de datos de ejemplo para demostración y la guía APE 04."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExampleDataset:
    key: str
    title: str
    description: str
    x: tuple[float, ...]
    y: tuple[float, ...]


CANONICAL_LINEAR = ExampleDataset(
    key="canonical_linear",
    title="Lineal canónico (guía)",
    description="y = 1 + 2x. Debe producir SSE = 0, R² = 1, r = 1.",
    x=(0.0, 1.0, 2.0, 3.0, 4.0),
    y=(1.0, 3.0, 5.0, 7.0, 9.0),
)

CANONICAL_QUADRATIC = ExampleDataset(
    key="canonical_quadratic",
    title="Cuadrático canónico (guía)",
    description="y = 1 + x². El polinomio de grado 2 recupera la curva exacta.",
    x=(0.0, 1.0, 2.0, 3.0, 4.0),
    y=(1.0, 2.0, 5.0, 10.0, 17.0),
)

LAB_GROWTH = ExampleDataset(
    key="lab_growth",
    title="Crecimiento de laboratorio",
    description="Serie con tendencia curva suave para contrastar recta y parábola.",
    x=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0),
    y=(2.1, 3.8, 6.2, 9.1, 13.0, 17.6, 23.2, 29.5),
)

EXAMPLES: tuple[ExampleDataset, ...] = (
    CANONICAL_LINEAR,
    CANONICAL_QUADRATIC,
    LAB_GROWTH,
)


def example_by_key(key: str) -> ExampleDataset:
    for item in EXAMPLES:
        if item.key == key:
            return item
    raise KeyError(f"Ejemplo desconocido: {key}")
