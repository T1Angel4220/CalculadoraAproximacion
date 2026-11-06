"""Ajuste polinomial de segundo grado."""

import numpy as np
import pytest

from aproxlab.core.exceptions import InsufficientDataError
from aproxlab.core.metrics import compute_metrics
from aproxlab.core.regression.quadratic import QuadraticRegression

CANONICAL_X = [0, 1, 2, 3, 4]
CANONICAL_Y = [1, 2, 5, 10, 17]  # y = 1 + x^2


def test_canonical_quadratic_recovers_one_plus_x_squared() -> None:
    result = QuadraticRegression().fit(CANONICAL_X, CANONICAL_Y)

    assert result.coefficients[0] == pytest.approx(1.0)
    assert result.coefficients[1] == pytest.approx(0.0, abs=1e-9)
    assert result.coefficients[2] == pytest.approx(1.0)


def test_canonical_quadratic_predictions_residuals_and_sse() -> None:
    result = QuadraticRegression().fit(CANONICAL_X, CANONICAL_Y)
    metrics = compute_metrics(CANONICAL_Y, result.y_hat, parameter_count=3)

    np.testing.assert_allclose(result.y_hat, CANONICAL_Y, atol=1e-9)
    np.testing.assert_allclose(result.residuals, np.zeros(5), atol=1e-9)
    assert metrics.sse == pytest.approx(0.0)


def test_quadratic_requires_at_least_three_points() -> None:
    with pytest.raises(InsufficientDataError):
        QuadraticRegression().fit([0, 1], [1, 2])
