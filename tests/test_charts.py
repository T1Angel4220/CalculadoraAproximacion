"""La curva densa evalúa el polinomio ajustado."""

import numpy as np

from aproxlab.core.regression.quadratic import QuadraticRegression
from aproxlab.services.charts import dense_curve


def test_dense_curve_recovers_one_plus_x_squared() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = np.array([1.0, 2.0, 5.0, 10.0, 17.0])
    result = QuadraticRegression().fit(x, y)
    grid, y_grid = dense_curve(x, result)
    np.testing.assert_allclose(y_grid, 1.0 + grid**2, atol=1e-8)
