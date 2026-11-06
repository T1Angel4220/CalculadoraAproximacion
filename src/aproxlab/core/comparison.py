"""Comparación de modelos de ajuste por error de entrenamiento."""

from __future__ import annotations

from dataclasses import dataclass

from aproxlab.core.metrics import FitMetrics

_SSE_TIE_TOLERANCE = 1e-12

_NESTED_CAUTION = (
    "El modelo cuadrático incluye a la recta como caso particular (a2 = 0). "
    "Un menor SSE sobre los mismos datos de entrenamiento no implica por sí solo "
    "mejor capacidad predictiva; conviene contrastar también el R² ajustado y el "
    "error estándar (Syx) que penalizan el parámetro extra."
)


@dataclass(frozen=True, slots=True)
class ModelScore:
    name: str
    metrics: FitMetrics


@dataclass(frozen=True, slots=True)
class ModelComparison:
    winner_name: str
    criterion: str
    caution: str
    scores: tuple[ModelScore, ...]


def compare_models(named_metrics: list[tuple[str, FitMetrics]]) -> ModelComparison:
    """Elige el modelo de menor SSE; declara empate si las diferencias son numéricas nulas."""
    if not named_metrics:
        raise ValueError("Se requiere al menos un modelo para comparar.")

    scores = tuple(ModelScore(name=name, metrics=metrics) for name, metrics in named_metrics)
    ranked = sorted(scores, key=lambda item: item.metrics.sse)
    best = ranked[0]
    winner = best.name
    if len(ranked) > 1 and abs(ranked[1].metrics.sse - best.metrics.sse) <= _SSE_TIE_TOLERANCE:
        winner = "Empate"
    return ModelComparison(
        winner_name=winner,
        criterion="SSE",
        caution=_NESTED_CAUTION,
        scores=scores,
    )
