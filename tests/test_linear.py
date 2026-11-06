"""Ajuste lineal por mínimos cuadrados — casos de la guía y degenerados."""

import numpy as np
import pytest

from aproxlab.core.exceptions import DegenerateDesignError, InsufficientDataError
from aproxlab.core.metrics import compute_metrics
from aproxlab.core.regression.linear import LinearRegression

CANONICAL_X = [0, 1, 2, 3, 4]
CANONICAL_Y = [1, 3, 5, 7, 9]


def test_canonical_line_has_slope_two_and_intercept_one() -> None:
    result = LinearRegression().fit(CANONICAL_X, CANONICAL_Y)

    assert result.coefficients[0] == pytest.approx(1.0)
    assert result.coefficients[1] == pytest.approx(2.0)
    assert result.equation == "y = 1 + 2x"


def test_canonical_line_has_zero_sse_unit_r_squared_and_correlation() -> None:
    result = LinearRegression().fit(CANONICAL_X, CANONICAL_Y)
    metrics = compute_metrics(CANONICAL_Y, result.y_hat, parameter_count=2, x=CANONICAL_X)

    assert metrics.sse == pytest.approx(0.0)
    assert metrics.r_squared == pytest.approx(1.0)
    assert metrics.correlation == pytest.approx(1.0)
    assert metrics.std_error == pytest.approx(0.0)


def test_linear_fit_rejects_single_point() -> None:
    with pytest.raises(InsufficientDataError):
        LinearRegression().fit([1], [2])


def test_linear_fit_rejects_identical_x_values() -> None:
    with pytest.raises(DegenerateDesignError):
        LinearRegression().fit([3, 3, 3], [1, 2, 4])


def test_constant_y_leaves_r_squared_undefined() -> None:
    result = LinearRegression().fit([0, 1, 2], [5, 5, 5])
    metrics = compute_metrics([5, 5, 5], result.y_hat, parameter_count=2, x=[0, 1, 2])

    assert metrics.sst == pytest.approx(0.0)
    assert metrics.r_squared is None
    assert metrics.correlation is None
    np.testing.assert_allclose(result.y_hat, [5, 5, 5])
