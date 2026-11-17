"""Recorridos reales de limpieza y visibilidad de la matriz en Qt."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QScrollArea, QToolBar
from pytestqt.qtbot import QtBot

from aproxlab.ui.main_window import MainWindow
from aproxlab.ui.views.quadratic_view import QuadraticView
from aproxlab.ui.widgets.formula_card import FormulaCard


@pytest.fixture
def window(qtbot: QtBot) -> Iterator[MainWindow]:
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.show()
    yield widget
    widget.close()


@pytest.mark.parametrize("entry_point", ["data", "toolbar", "menu"])
def test_clear_removes_data_results_and_exportable_report(
    window: MainWindow, qtbot: QtBot, tmp_path: Path, entry_point: str
) -> None:
    assert window._presenter.last_report is not None
    assert window._quadratic._gauss_layout.count() > 0
    window._data.model.setData(window._data.model.index(0, 1), "")
    window._fit_from_table()
    assert window._data._error.text()
    if entry_point == "toolbar":
        window._toggle_charts()
        assert window._charts.isHidden()

    if entry_point == "menu":
        file_menu = window.menuBar().actions()[0].menu()
        action = next(action for action in file_menu.actions() if action.text() == "Limpiar")
        action.trigger()
    else:
        host = window._data if entry_point == "data" else window.findChild(QToolBar)
        button = next(btn for btn in host.findChildren(QPushButton) if btn.text() == "Limpiar")
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert window._presenter.last_report is None
    assert window._examples.currentData() == ""
    assert window._data._error.text() == ""
    model = window._data.model
    assert all(
        model.data(model.index(row, col)) == ""
        for row in range(model.rowCount())
        for col in range(model.columnCount())
    )
    for table in (
        window._linear._sums,
        window._linear._errors,
        window._quadratic._sums,
        window._quadratic._matrix,
        window._quadratic._errors,
        window._comparison._table,
    ):
        assert table.rowCount() == 0
    for card in window.findChildren(FormulaCard):
        assert card._formula._latex == ""
        assert card._subst.text() == "—"
        assert card._result.text() == "—"
    assert window._quadratic._gauss_layout.count() == 0
    assert not window._quadratic._matrix_btn.isEnabled()
    assert window._linear._interp.text() == ""
    assert window._quadratic._note.text() == ""
    assert window._comparison._report is None
    assert window._comparison._badge.text() == "Sin ajuste"
    assert window._charts._report is None
    for canvas in (window._charts._linear, window._charts._quadratic, window._charts._both):
        assert not canvas.axes.lines
        assert not canvas.axes.collections
        assert canvas.axes.get_legend() is None
    assert window.statusBar().currentMessage() == "n=0 · sin ajuste"
    assert window._data._count.text() == "n = 0"
    destination = tmp_path / "stale-report.txt"
    window._presenter.export_report(str(destination))
    assert not destination.exists()
    assert window._data._error.text()


def test_clear_recovers_from_empty_input_and_allows_a_new_analysis(
    window: MainWindow, qtbot: QtBot
) -> None:
    button = next(btn for btn in window._data.findChildren(QPushButton) if btn.text() == "Limpiar")
    fit = next(btn for btn in window._data.findChildren(QPushButton) if "Ajustar" in btn.text())
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    qtbot.keyClick(window, Qt.Key.Key_F5)
    assert window._data._error.text()
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert not window._data._error.text()

    window._data.load_pairs([0, 1, 2, 3, 4], [1, 2, 5, 10, 17])
    qtbot.mouseClick(fit, Qt.MouseButton.LeftButton)

    assert window._presenter.last_report.quadratic.coefficients == pytest.approx(
        [1, 0, 1], abs=1e-9
    )
    assert window._data._count.text() == "n = 5"
    assert window._quadratic._matrix.rowCount() == 3
    assert window._quadratic._gauss_layout.count() > 0
    assert window._charts._report is window._presenter.last_report


def test_matrix_toggle_preserves_results_without_recalculating(
    window: MainWindow, qtbot: QtBot
) -> None:
    window._results.setCurrentIndex(1)
    view = window._quadratic
    view.findChild(QScrollArea).ensureWidgetVisible(view._matrix_btn)
    report = window._presenter.last_report
    reports = []
    window._presenter.analysis_ready.connect(reports.append)
    steps = view._gauss_layout.count()

    qtbot.mouseClick(view._matrix_btn, Qt.MouseButton.LeftButton)
    assert view._matrix_box.isHidden()
    assert view._matrix_btn.text() == "Mostrar cálculo de la matriz"
    assert view._sums.isVisible()
    assert view._errors.isVisible()
    assert view._coeffs.isVisible()

    qtbot.mouseClick(view._matrix_btn, Qt.MouseButton.LeftButton)
    assert not view._matrix_box.isHidden()
    assert view._matrix_btn.text() == "Ocultar cálculo de la matriz"
    assert view._gauss_layout.count() == steps
    assert window._presenter.last_report is report
    assert not reports


def test_matrix_toggle_requires_a_calculation_and_preserves_visibility_preference(
    window: MainWindow, qtbot: QtBot
) -> None:
    empty_view = QuadraticView()
    qtbot.addWidget(empty_view)
    assert not empty_view._matrix_btn.isEnabled()

    window._results.setCurrentIndex(1)
    view = window._quadratic
    assert view._matrix_btn.isEnabled()
    view.findChild(QScrollArea).ensureWidgetVisible(view._matrix_btn)
    qtbot.mouseClick(view._matrix_btn, Qt.MouseButton.LeftButton)
    window._clear_workspace()
    assert not view._matrix_btn.isEnabled()
    assert view._matrix_box.isHidden()

    window._presenter.load_example("canonical_quadratic")
    assert view._matrix_btn.isEnabled()
    assert view._matrix_box.isHidden()
    assert view._gauss_layout.count() > 0
