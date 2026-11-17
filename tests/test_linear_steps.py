"""Ajuste lineal a mano: sumatorias, medias, a0, a1, Sr, St, Sy/x, r² y r."""

import pytest

from aproxlab.core.regression.linear import LinearRegression, interpret_correlation

# Datos del procedimiento del profesor (literal a).
X = [1, 2, 3, 4, 5, 6, 7, 8, 9]
Y = [1, 1.5, 2, 3, 4, 5, 8, 10, 13]


def test_summations_match_classroom_worksheet() -> None:
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.n == 9
    assert steps.sum_x == pytest.approx(45)
    assert steps.sum_y == pytest.approx(47.5)
    assert steps.sum_x2 == pytest.approx(285)
    assert steps.sum_xy == pytest.approx(325)


def test_means_a0_and_a1_match_classroom_worksheet() -> None:
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.mean_x == pytest.approx(5)
    assert steps.mean_y == pytest.approx(5.277778, rel=1e-6)
    assert steps.a1 == pytest.approx(1.458333, rel=1e-5)
    assert steps.a0 == pytest.approx(-2.013889, rel=1e-5)


def test_sr_st_syx_r2_and_r_match_classroom_worksheet() -> None:
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.sr == pytest.approx(11.951389, rel=1e-5)
    assert steps.st == pytest.approx(139.555556, rel=1e-5)
    assert steps.syx == pytest.approx(1.306653, rel=1e-5)
    assert steps.r_squared == pytest.approx(0.914361, rel=1e-5)
    assert steps.r == pytest.approx(0.956222, rel=1e-5)


def test_error_table_has_yhat_residual_and_squared_residual() -> None:
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    first = steps.error_rows[0]
    assert first.x == pytest.approx(1)
    assert first.y == pytest.approx(1)
    assert first.y_hat == pytest.approx(-0.555556, rel=1e-4)
    assert first.residual == pytest.approx(1.555556, rel=1e-4)
    assert first.residual_sq == pytest.approx(2.4198, rel=1e-3)
    assert len(steps.error_rows) == 9


def test_error_table_matches_classroom_columns() -> None:
    """Una sola tabla: ŷ de la recta, ei, ei², yi−ȳ y (yi−ȳ)²."""
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    first = steps.error_rows[0]
    last = steps.error_rows[-1]
    assert first.y_hat == pytest.approx(-0.555556, rel=1e-4)
    assert first.residual == pytest.approx(1.555556, rel=1e-4)
    assert first.dev_mean == pytest.approx(-4.277778, rel=1e-5)
    assert first.dev_mean_sq == pytest.approx(18.29938, rel=1e-4)
    assert last.y_hat == pytest.approx(11.111111, rel=1e-4)
    assert last.residual == pytest.approx(1.888889, rel=1e-4)
    assert last.dev_mean == pytest.approx(7.722222, rel=1e-5)
    assert last.dev_mean_sq == pytest.approx(59.63272, rel=1e-4)


def test_error_table_includes_deviation_from_mean_y() -> None:
    steps = LinearRegression().fit(X, Y).worksheet
    assert steps is not None
    first = steps.error_rows[0]
    assert first.mean_y == pytest.approx(5.277778, rel=1e-6)
    assert first.dev_mean == pytest.approx(1 - 5.277778, rel=1e-5)
    assert first.dev_mean_sq == pytest.approx((1 - 5.277778) ** 2, rel=1e-5)
    total_st = sum(row.dev_mean_sq for row in steps.error_rows)
    assert total_st == pytest.approx(steps.st, rel=1e-9)


def test_interpret_correlation_bands() -> None:
    assert interpret_correlation(0.95) == "Correlación positiva fuerte"
    assert interpret_correlation(0.3) == "Correlación positiva débil"
    assert interpret_correlation(-0.2) == "Correlación negativa débil"
    assert interpret_correlation(-0.8) == "Correlación negativa fuerte"
    for sample in (0.95, 0.3, -0.2, -0.8):
        text = interpret_correlation(sample)
        assert "0.5" not in text
        assert "≤" not in text
        assert ">=" not in text
