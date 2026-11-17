"""Comparación de modelos por error de ajuste."""

import pytest

from aproxlab.core.comparison import compare_models, narrate_comparison
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


def test_classroom_narrative_reports_sse_drop_and_strong_correlation() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [1, 1.5, 2, 3, 4, 5, 8, 10, 13]
    linear = LinearRegression().fit(x, y)
    quadratic = QuadraticRegression().fit(x, y)
    m_lin = compute_metrics(y, linear.y_hat, parameter_count=2, x=x)
    m_quad = compute_metrics(y, quadratic.y_hat, parameter_count=3, x=x)

    story = narrate_comparison(m_lin, m_quad)

    assert story.winner_name == "Cuadrático"
    assert story.tied is False
    assert story.sse_reduction_percent == pytest.approx(94.03, abs=0.05)
    assert story.featured_r_squared == pytest.approx(m_quad.r_squared)
    assert "fuerte" in story.correlation_text.lower()
    assert "0.956" in story.correlation_text or "r" in story.correlation_text.lower()
    assert "datos analizados" in story.conclusion.lower()
    assert "garantiza" not in story.conclusion.lower()
    assert "fuera" not in story.conclusion.lower()


def test_equal_sse_is_a_tie_and_does_not_pick_quadratic() -> None:
    y = [1, 3, 5, 7, 9]
    linear = LinearRegression().fit(X, y)
    quadratic = QuadraticRegression().fit(X, y)
    m_lin = compute_metrics(y, linear.y_hat, parameter_count=2, x=X)
    m_quad = compute_metrics(y, quadratic.y_hat, parameter_count=3, x=X)

    story = narrate_comparison(m_lin, m_quad)

    assert story.tied is True
    assert story.winner_name == "Empate"
    assert story.recommended_name == "Lineal"
    assert story.perfect_fit is True
    assert story.sse_reduction_percent is None
    text = story.conclusion.lower()
    assert "perfecto" in text
    assert "simplicidad" in text
    assert "lineal" in text


def test_linear_wins_when_its_sse_is_smaller() -> None:
    from aproxlab.core.metrics import FitMetrics

    linear = FitMetrics(
        sse=1.0,
        sst=10.0,
        r_squared=0.9,
        correlation=0.2,
        std_error=0.5,
        n=5,
        parameter_count=2,
        adjusted_r_squared=0.85,
    )
    quadratic = FitMetrics(
        sse=4.0,
        sst=10.0,
        r_squared=0.6,
        correlation=None,
        std_error=1.1,
        n=5,
        parameter_count=3,
        adjusted_r_squared=0.4,
    )

    story = narrate_comparison(linear, quadratic)

    assert story.winner_name == "Lineal"
    assert story.tied is False
    assert story.recommended_name == "Lineal"
    assert story.featured_r_squared == pytest.approx(0.9)
    assert story.sse_reduction_percent == pytest.approx(-300.0)
    assert "débil" in story.correlation_text.lower()
    assert "lineal" in story.conclusion.lower()


def _pair(x: list[float], y: list[float]):
    linear = LinearRegression().fit(x, y)
    quadratic = QuadraticRegression().fit(x, y)
    return (
        compute_metrics(y, linear.y_hat, parameter_count=2, x=x),
        compute_metrics(y, quadratic.y_hat, parameter_count=3, x=x),
    )


def test_exact_line_recommends_linear_and_does_not_divide_by_zero() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [3, 5, 7, 9, 11, 13, 15, 17, 19]
    linear, quadratic = _pair(x, y)
    story = narrate_comparison(linear, quadratic)

    assert linear.sse == pytest.approx(0.0, abs=1e-8)
    assert quadratic.sse == pytest.approx(0.0, abs=1e-8)
    assert linear.r_squared == pytest.approx(1.0)
    assert quadratic.r_squared == pytest.approx(1.0)
    assert story.perfect_fit is True
    assert story.recommended_name == "Lineal"
    assert story.sse_reduction_percent is None
    assert "perfecto" in story.conclusion.lower()
    assert "simplicidad" in story.conclusion.lower()


def test_constant_y_leaves_r_squared_undefined() -> None:
    x = [1, 2, 3, 4, 5, 6]
    y = [4, 4, 4, 4, 4, 4]
    linear, quadratic = _pair(x, y)
    story = narrate_comparison(linear, quadratic)

    assert linear.sst == pytest.approx(0.0)
    assert linear.r_squared is None
    assert quadratic.r_squared is None
    assert story.recommended_name == "Lineal"
    assert "no está definido" in story.conclusion.lower()
    assert story.sse_reduction_percent is None


def test_clear_quadratic_and_small_real_improvement_use_different_wording() -> None:
    from aproxlab.core.metrics import FitMetrics

    clear_linear = FitMetrics(20, 100, 0.8, 0.9, 1.5, 9, 2, 0.75)
    clear_quadratic = FitMetrics(1, 100, 0.99, None, 0.4, 9, 3, 0.98)
    clear = narrate_comparison(clear_linear, clear_quadratic)
    assert clear.recommended_name == "Cuadrático"
    assert clear.small_improvement is False
    assert "menor sse" in clear.conclusion.lower()
    assert "considerable" not in clear.conclusion.lower()

    mild_quadratic = FitMetrics(19.6, 100, 0.804, None, 1.4, 9, 3, 0.76)
    mild = narrate_comparison(clear_linear, mild_quadratic)
    assert mild.recommended_name == "Cuadrático"
    assert mild.small_improvement is True
    assert mild.sse_reduction_percent == pytest.approx(2.0)
    text = mild.conclusion.lower()
    assert "pequeña" in text
    assert "considerable" not in text
    assert "es significativa" not in text


def test_negligible_sse_gap_recommends_linear_on_large_and_small_scales() -> None:
    from aproxlab.core.metrics import FitMetrics

    large_scale = 1e12
    large = narrate_comparison(
        FitMetrics(large_scale * 1e-12, large_scale, 1.0, 1.0, 0.0, 9, 2, 1.0),
        FitMetrics(large_scale * 1e-12 + 1e-3, large_scale, 1.0, None, 0.0, 9, 3, 1.0),
    )
    small = narrate_comparison(
        FitMetrics(1e-16, 1e-10, 1.0, 1.0, 0.0, 9, 2, 1.0),
        FitMetrics(2e-16, 1e-10, 1.0, None, 0.0, 9, 3, 1.0),
    )
    for story in (large, small):
        assert story.tied is True
        assert story.recommended_name == "Lineal"
        assert (
            "cuadrático" not in story.conclusion.lower() or "no aporta" in story.conclusion.lower()
        )


def test_positive_tie_reports_the_real_tiny_reduction() -> None:
    from aproxlab.core.metrics import FitMetrics

    story = narrate_comparison(
        FitMetrics(10.0, 40.0, 0.75, 0.8, 1.0, 8, 2, 0.7),
        FitMetrics(10.0 + 1e-9, 40.0, 0.75, None, 1.0, 8, 3, 0.7),
    )
    assert story.tied is True
    assert story.perfect_fit is False
    assert story.sse_reduction_percent == pytest.approx(-1e-8, rel=1e-6)
    assert story.recommended_name == "Lineal"
