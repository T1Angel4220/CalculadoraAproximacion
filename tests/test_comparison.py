"""Comparación de modelos por error de ajuste."""

import pytest

from aproxlab.core.comparison import compare_models
from aproxlab.core.metrics import compute_metrics
from aproxlab.core.regression.linear import LinearRegression
from aproxlab.core.regression.quadratic import QuadraticRegression

X = [0, 1, 2, 3, 4]
Y_QUAD = [1, 2, 5, 10, 17]


def test_quadratic_wins_on_curved_data_by_sse() -> None:
    linear = LinearRegression().fit(X, Y_QUAD)
    quadratic = QuadraticRegression().fit(X, Y_QUAD)
    m_lin = compute_metrics(Y_QUAD, linear.y_hat, parameter_count=2)
    m_quad = compute_metrics(Y_QUAD, quadratic.y_hat, parameter_count=3)

    comparison = compare_models(
        [
            ("Lineal", m_lin),
            ("Cuadrático", m_quad),
        ]
    )

    assert comparison.winner_name == "Cuadrático"
    assert comparison.criterion == "SSE"
    assert m_quad.sse < m_lin.sse
    assert "anidad" in comparison.caution.lower() or "particular" in comparison.caution.lower()


def test_perfect_line_has_equal_sse_for_both_models() -> None:
    y = [1, 3, 5, 7, 9]
    linear = LinearRegression().fit(X, y)
    quadratic = QuadraticRegression().fit(X, y)
    m_lin = compute_metrics(y, linear.y_hat, parameter_count=2)
    m_quad = compute_metrics(y, quadratic.y_hat, parameter_count=3)

    comparison = compare_models([("Lineal", m_lin), ("Cuadrático", m_quad)])

    assert m_lin.sse == pytest.approx(0.0)
    assert m_quad.sse == pytest.approx(0.0)
    assert comparison.winner_name in {"Lineal", "Empate"}
