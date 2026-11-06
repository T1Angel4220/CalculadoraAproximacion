"""Indicadores de error: SSE, SST, Syx, R² y correlación."""

import numpy as np
import pytest

from aproxlab.core.metrics import compute_metrics


def test_sse_is_sum_of_squared_residuals() -> None:
    y = np.array([1.0, 2.0, 3.0])
    y_hat = np.array([1.0, 1.0, 1.0])

    metrics = compute_metrics(y, y_hat, parameter_count=2)

    assert metrics.sse == pytest.approx(0 + 1 + 4)


def test_sst_is_sum_of_squares_about_the_mean() -> None:
    y = np.array([1.0, 3.0, 5.0])
    y_hat = y.copy()

    metrics = compute_metrics(y, y_hat, parameter_count=2)

    # mean = 3 → ( -2 )^2 + 0 + 2^2 = 8
    assert metrics.sst == pytest.approx(8.0)
    assert metrics.r_squared == pytest.approx(1.0)


def test_standard_error_uses_n_minus_parameter_count() -> None:
    y = np.array([1.0, 2.0, 4.0, 8.0])
    y_hat = np.array([1.0, 2.0, 3.0, 7.0])
    sse = 0 + 0 + 1 + 1

    metrics = compute_metrics(y, y_hat, parameter_count=2)

    assert metrics.std_error == pytest.approx((sse / 2) ** 0.5)


def test_std_error_undefined_when_n_not_greater_than_parameters() -> None:
    y = np.array([1.0, 2.0])
    metrics = compute_metrics(y, y, parameter_count=2)

    assert metrics.std_error is None


def test_pearson_correlation_from_x_and_y() -> None:
    x = [0, 1, 2, 3, 4]
    y = [1, 3, 5, 7, 9]
    metrics = compute_metrics(y, y, parameter_count=2, x=x)

    assert metrics.correlation == pytest.approx(1.0)
