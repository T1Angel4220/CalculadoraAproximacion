"""Parábola a mano: sumatorias, sistema normal, Gauss-Jordan, Sr, St, Sy/x y r²."""

import pytest

from aproxlab.core.regression.quadratic import QuadraticRegression

X = [1, 2, 3, 4, 5, 6, 7, 8, 9]
Y = [1, 1.5, 2, 3, 4, 5, 8, 10, 13]


def test_quadratic_summations_match_classroom() -> None:
    steps = QuadraticRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.n == 9
    assert steps.sum_x == pytest.approx(45)
    assert steps.sum_y == pytest.approx(47.5)
    assert steps.sum_x2 == pytest.approx(285)
    assert steps.sum_x3 == pytest.approx(2025)
    assert steps.sum_x4 == pytest.approx(15333)
    assert steps.sum_xy == pytest.approx(325)
    assert steps.sum_x2y == pytest.approx(2438)
    assert len(steps.power_rows) == 9
    assert steps.power_rows[1].x3 == pytest.approx(8)
    assert steps.power_rows[1].x2y == pytest.approx(6)


def test_normal_system_and_first_gauss_pivot() -> None:
    steps = QuadraticRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.augmented[0] == pytest.approx((9, 45, 285, 47.5))
    assert steps.augmented[1] == pytest.approx((45, 285, 2025, 325))
    assert steps.augmented[2] == pytest.approx((285, 2025, 15333, 2438))
    assert len(steps.gauss_steps) >= 2
    first = steps.gauss_steps[0]
    assert "F1" in first.operation
    assert first.matrix[0][0] == pytest.approx(1)
    assert first.matrix[0][1] == pytest.approx(5)
    assert first.matrix[0][3] == pytest.approx(5.277778, rel=1e-5)


def test_gauss_jordan_reaches_classroom_coefficients() -> None:
    steps = QuadraticRegression().fit(X, Y).worksheet
    assert steps is not None
    assert steps.a0 == pytest.approx(1.488095, rel=1e-5)
    assert steps.a1 == pytest.approx(-0.451840, rel=1e-4)
    assert steps.a2 == pytest.approx(0.191017, rel=1e-4)
    identity = steps.gauss_steps[-1].matrix
    assert identity[0][0] == pytest.approx(1)
    assert identity[0][1] == pytest.approx(0, abs=1e-8)
    assert identity[1][2] == pytest.approx(0, abs=1e-8)
    assert identity[2][2] == pytest.approx(1)
    assert identity[2][3] == pytest.approx(steps.a2)


def test_quadratic_errors_sr_st_syx_and_r2() -> None:
    steps = QuadraticRegression().fit(X, Y).worksheet
    assert steps is not None
    first = steps.error_rows[0]
    assert first.y_hat == pytest.approx(1.227273, rel=1e-4)
    assert first.residual == pytest.approx(-0.227273, rel=1e-4)
    assert steps.sr == pytest.approx(0.713203, rel=1e-4)
    assert steps.st == pytest.approx(139.555556, rel=1e-5)
    assert steps.syx == pytest.approx(0.344771, rel=1e-4)
    assert steps.r_squared == pytest.approx(0.994889, rel=1e-5)
