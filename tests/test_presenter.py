"""El presenter orquesta el servicio sin widgets."""

import pytest

from aproxlab.ui.controllers.analysis_presenter import AnalysisPresenter


def test_presenter_emits_report_for_canonical_line() -> None:
    presenter = AnalysisPresenter()
    reports: list = []
    presenter.analysis_ready.connect(reports.append)

    presenter.calculate([0, 1, 2, 3, 4], [1, 3, 5, 7, 9])

    assert len(reports) == 1
    assert reports[0].linear_metrics.sse == pytest.approx(0.0)
    assert reports[0].linear.coefficients[1] == pytest.approx(2.0)


def test_presenter_emits_failure_for_insufficient_data() -> None:
    presenter = AnalysisPresenter()
    errors: list[str] = []
    presenter.analysis_failed.connect(errors.append)

    presenter.calculate([1], [2])

    assert errors
    assert presenter.last_report is None
