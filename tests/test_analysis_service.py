"""Orquestación del análisis completo sobre los datos canónicos de la guía."""

import pytest

from aproxlab.services.analysis import AnalysisService


def test_analyze_canonical_line_reports_perfect_linear_fit() -> None:
    report = AnalysisService().analyze([0, 1, 2, 3, 4], [1, 3, 5, 7, 9])

    assert report.linear.coefficients[1] == pytest.approx(2.0)
    assert report.linear_metrics.sse == pytest.approx(0.0)
    assert report.quadratic_metrics.sse == pytest.approx(0.0)
    assert report.comparison.winner_name == "Empate"
