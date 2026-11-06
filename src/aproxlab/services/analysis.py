"""Orquesta validación, ajustes y comparación sin depender de la GUI."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from aproxlab.core.comparison import ModelComparison, compare_models
from aproxlab.core.metrics import FitMetrics, compute_metrics
from aproxlab.core.regression.base import FitResult
from aproxlab.core.regression.factory import create_strategy
from aproxlab.core.validation import prepare_dataset


@dataclass(frozen=True, slots=True)
class AnalysisReport:
    x: np.ndarray
    y: np.ndarray
    linear: FitResult
    quadratic: FitResult
    linear_metrics: FitMetrics
    quadratic_metrics: FitMetrics
    comparison: ModelComparison


class AnalysisService:
    """Caso de uso: analizar un conjunto de pares (x, y)."""

    def analyze(self, x: list[float] | np.ndarray, y: list[float] | np.ndarray) -> AnalysisReport:
        x_arr, y_arr = prepare_dataset(x, y, min_distinct_x=2)
        linear = create_strategy("linear").fit(x_arr, y_arr)
        quadratic = create_strategy("quadratic").fit(x_arr, y_arr)
        linear_metrics = compute_metrics(y_arr, linear.y_hat, parameter_count=2, x=x_arr)
        quadratic_metrics = compute_metrics(y_arr, quadratic.y_hat, parameter_count=3, x=x_arr)
        comparison = compare_models(
            [
                (linear.name, linear_metrics),
                (quadratic.name, quadratic_metrics),
            ]
        )
        return AnalysisReport(
            x=x_arr,
            y=y_arr,
            linear=linear,
            quadratic=quadratic,
            linear_metrics=linear_metrics,
            quadratic_metrics=quadratic_metrics,
            comparison=comparison,
        )
