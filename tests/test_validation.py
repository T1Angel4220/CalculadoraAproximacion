"""Validación de pares (x, y) según la guía APE 04."""

import math

import numpy as np
import pytest

from aproxlab.core.exceptions import (
    DegenerateDesignError,
    InsufficientDataError,
    LengthMismatchError,
    NonNumericDataError,
)
from aproxlab.core.validation import prepare_dataset, require_min_points


def test_prepare_dataset_accepts_equal_length_numeric_pairs() -> None:
    x, y = prepare_dataset([0, 1, 2], [1.0, 3, 5])

    np.testing.assert_allclose(x, [0.0, 1.0, 2.0])
    np.testing.assert_allclose(y, [1.0, 3.0, 5.0])


def test_prepare_dataset_rejects_length_mismatch() -> None:
    with pytest.raises(LengthMismatchError):
        prepare_dataset([0, 1], [1, 2, 3])


def test_prepare_dataset_rejects_non_numeric_values() -> None:
    with pytest.raises(NonNumericDataError):
        prepare_dataset(["a", 1], [2, 3])


def test_prepare_dataset_rejects_nan_and_inf() -> None:
    with pytest.raises(NonNumericDataError):
        prepare_dataset([0, 1], [1, math.nan])
    with pytest.raises(NonNumericDataError):
        prepare_dataset([0, math.inf], [1, 2])


def test_require_min_points_rejects_insufficient_observations() -> None:
    with pytest.raises(InsufficientDataError):
        require_min_points(2, minimum=3, method="cuadrático")


def test_prepare_dataset_rejects_fewer_than_two_distinct_x() -> None:
    with pytest.raises(DegenerateDesignError):
        prepare_dataset([1, 1, 1], [2, 3, 4], min_distinct_x=2)
