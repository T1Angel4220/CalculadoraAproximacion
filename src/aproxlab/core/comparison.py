"""Comparación de modelos de ajuste por error de entrenamiento."""

from __future__ import annotations

from dataclasses import dataclass

from aproxlab.core.metrics import FitMetrics
from aproxlab.core.regression.linear import interpret_correlation

_RELATIVE_SSE_TOLERANCE = 1e-9
_ABSOLUTE_SSE_FLOOR = 1e-12
_SMALL_REDUCTION_PERCENT = 5.0

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


@dataclass(frozen=True, slots=True)
class ComparisonNarrative:
    """Texto de la comparación. No altera los SSE calculados."""

    winner_name: str
    recommended_name: str
    tied: bool
    perfect_fit: bool
    small_improvement: bool
    sse_reduction_percent: float | None
    featured_r_squared: float | None
    other_r_squared: float | None
    correlation: float | None
    correlation_text: str
    conclusion: str


def narrate_comparison(linear: FitMetrics, quadratic: FitMetrics) -> ComparisonNarrative:
    """Arma la lectura de SSE, R² y r para cualquier par de ajustes."""
    verdict = compare_models([("Lineal", linear), ("Cuadrático", quadratic)])
    tolerance = _sse_tolerance(linear, quadratic)
    tied = verdict.winner_name == "Empate"
    perfect = _practically_zero(linear.sse, tolerance) and _practically_zero(
        quadratic.sse, tolerance
    )
    reduction = None if perfect else _sse_reduction(linear.sse, quadratic.sse, tolerance)
    small = _is_small_improvement(verdict.winner_name, reduction, tied)
    recommended = "Lineal" if tied or verdict.winner_name == "Lineal" else "Cuadrático"
    featured, other = _featured_r2(recommended, linear, quadratic)
    correlation_text = _correlation_text(linear.correlation)
    conclusion = _conclusion(
        winner=verdict.winner_name,
        perfect=perfect,
        small=small,
        linear=linear,
        quadratic=quadratic,
        correlation_text=correlation_text,
        reduction=reduction,
    )
    return ComparisonNarrative(
        winner_name=verdict.winner_name,
        recommended_name=recommended,
        tied=tied,
        perfect_fit=perfect,
        small_improvement=small,
        sse_reduction_percent=reduction,
        featured_r_squared=featured,
        other_r_squared=other,
        correlation=linear.correlation,
        correlation_text=correlation_text,
        conclusion=conclusion,
    )


def _sse_tolerance(linear: FitMetrics, quadratic: FitMetrics) -> float:
    """Tolerancia relativa a SST y a los SSE, más un piso absoluto diminuto."""
    scale = max(abs(linear.sst), abs(quadratic.sst), abs(linear.sse), abs(quadratic.sse), 1.0)
    return max(_ABSOLUTE_SSE_FLOOR, _RELATIVE_SSE_TOLERANCE * scale)


def _practically_zero(value: float, tolerance: float) -> bool:
    return abs(value) <= tolerance


def _sse_reduction(sse_linear: float, sse_quadratic: float, tolerance: float) -> float | None:
    if abs(sse_linear) <= tolerance:
        return None
    return (sse_linear - sse_quadratic) / sse_linear * 100.0


def _is_small_improvement(winner: str, reduction: float | None, tied: bool) -> bool:
    if tied or winner != "Cuadrático" or reduction is None:
        return False
    return 0.0 < reduction < _SMALL_REDUCTION_PERCENT


def _featured_r2(
    recommended: str, linear: FitMetrics, quadratic: FitMetrics
) -> tuple[float | None, float | None]:
    if recommended == "Lineal":
        return linear.r_squared, quadratic.r_squared
    return quadratic.r_squared, linear.r_squared


def _correlation_text(r: float | None) -> str:
    if r is None:
        return "r no está definido"
    return f"r = {r:.4f}: {interpret_correlation(r)}"


def _fmt4(value: float | None) -> str:
    if value is None:
        return "no definido"
    if value < 0 and abs(value) <= 1e-8:
        value = 0.0
    return f"{value:.4f}"


def _indicators(linear: FitMetrics, quadratic: FitMetrics) -> str:
    return (
        f"SSE lineal = {_fmt4(linear.sse)}, SSE cuadrático = {_fmt4(quadratic.sse)}, "
        f"R² lineal = {_fmt4(linear.r_squared)} y R² cuadrático = {_fmt4(quadratic.r_squared)}."
    )


def _r2_clause(metrics: FitMetrics) -> str:
    if metrics.sst <= _ABSOLUTE_SSE_FLOOR or metrics.r_squared is None:
        return "R² no está definido porque SST = 0."
    return ""


def _conclusion(
    *,
    winner: str,
    perfect: bool,
    small: bool,
    linear: FitMetrics,
    quadratic: FitMetrics,
    correlation_text: str,
    reduction: float | None,
) -> str:
    numbers = _indicators(linear, quadratic)
    undefined = _r2_clause(linear)
    correlation = f"El coeficiente de correlación lineal es {correlation_text}."
    if perfect:
        return (
            "Ambos modelos representan los datos dentro de la tolerancia numérica: "
            "el ajuste es perfecto. "
            "Se recomienda el modelo lineal por simplicidad, porque utiliza menos parámetros. "
            "El cuadrático no aporta una mejora en el ajuste observado. "
            f"{numbers} {undefined} {correlation}"
        )
    if winner == "Empate":
        return (
            "Ambos modelos presentan un ajuste equivalente. "
            "La diferencia de SSE es numéricamente insignificante y no se declara ganador "
            "al cuadrático. Se recomienda el modelo lineal por simplicidad, "
            "porque utiliza menos parámetros. "
            "El cuadrático no aporta una mejora significativa en el ajuste observado. "
            f"{numbers} {undefined} {correlation}"
        )
    if winner == "Lineal":
        return (
            "El modelo lineal presenta un menor SSE y un mejor ajuste a los datos analizados. "
            f"{numbers} {undefined} {correlation} "
            "Se recomienda el modelo lineal para representar los datos analizados."
        )
    if small:
        shown = _fmt4(reduction)
        return (
            "El modelo cuadrático tiene un SSE menor, así que ajusta mejor estos datos, "
            f"pero la reducción es pequeña ({shown} %). "
            "No se presenta como una mejora grande ni se aplica una prueba estadística. "
            f"{numbers} {correlation}"
        )
    return (
        "El modelo cuadrático presenta un menor SSE y un mejor ajuste a los datos analizados. "
        f"{numbers} {correlation} "
        "Se recomienda el modelo cuadrático para representar los datos analizados."
    )


def _within_tolerance(first: ModelScore, second: ModelScore) -> bool:
    tolerance = _sse_tolerance(first.metrics, second.metrics)
    return abs(first.metrics.sse - second.metrics.sse) <= tolerance


def compare_models(named_metrics: list[tuple[str, FitMetrics]]) -> ModelComparison:
    """Elige el modelo de menor SSE; declara empate si las diferencias son numéricas nulas."""
    if not named_metrics:
        raise ValueError("Se requiere al menos un modelo para comparar.")

    scores = tuple(ModelScore(name=name, metrics=metrics) for name, metrics in named_metrics)
    ranked = sorted(scores, key=lambda item: item.metrics.sse)
    best = ranked[0]
    winner = best.name
    if len(ranked) > 1 and _within_tolerance(ranked[0], ranked[1]):
        winner = "Empate"
    return ModelComparison(
        winner_name=winner,
        criterion="SSE",
        caution=_NESTED_CAUTION,
        scores=scores,
    )
