"""Temas claro/oscuro y sincronización con Matplotlib."""

from __future__ import annotations

from matplotlib import rcParams
from PySide6.QtWidgets import QApplication

INK_DARK = "#e7ecf3"
INK_LIGHT = "#0f172a"

DARK_QSS = """
QWidget {
    background-color: #101418;
    color: #e7ecf3;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 12px;
}
QMainWindow, QMenuBar, QMenu, QToolBar {
    background-color: #101418;
    color: #e7ecf3;
    border: none;
}
QToolBar {
    spacing: 6px;
    padding: 4px 8px;
    border-bottom: 1px solid #2a3440;
}
QMenuBar::item:selected, QMenu::item:selected { background-color: #1c2430; }
QStatusBar {
    background-color: #0c1014;
    color: #8b9aab;
    font-family: "Cascadia Mono", "Consolas", monospace;
    font-size: 11px;
}
QFrame#Card {
    background-color: #161c24;
    border: 1px solid #2a3440;
    border-radius: 6px;
}
QPushButton {
    background-color: #1c2430;
    color: #e7ecf3;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 4px 10px;
}
QPushButton:hover { background-color: #2a3440; }
QPushButton#Primary {
    background-color: #0e7490;
    border: none;
    font-weight: 600;
}
QPushButton#Primary:hover { background-color: #155e75; }
QPushButton#Danger { background-color: #7f1d1d; border: none; }
QTableView, QTableWidget {
    background-color: #12181f;
    alternate-background-color: #161c24;
    gridline-color: #2a3440;
    selection-background-color: #155e75;
    border: 1px solid #2a3440;
    border-radius: 4px;
    font-family: "Cascadia Mono", "Consolas", monospace;
    font-size: 12px;
}
QHeaderView::section {
    background-color: #1c2430;
    color: #c5d0dc;
    padding: 4px 6px;
    border: none;
    border-right: 1px solid #2a3440;
    font-family: "Segoe UI", sans-serif;
}
QLabel#Title { font-size: 13px; font-weight: 600; }
QLabel#Subtitle { color: #8b9aab; font-size: 11px; }
QLabel#Error { color: #fca5a5; }
QTabWidget::pane { border: 1px solid #2a3440; }
QTabBar::tab {
    background: #161c24;
    padding: 5px 10px;
    border: 1px solid #2a3440;
    border-bottom: none;
}
QTabBar::tab:selected { background: #0e7490; }
QScrollArea { border: none; }
QSplitter::handle { background: #2a3440; width: 1px; height: 1px; }
QComboBox {
    background: #1c2430;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 3px 8px;
    min-width: 180px;
}
QComboBox QAbstractItemView {
    background: #161c24;
    selection-background-color: #0e7490;
}
"""

LIGHT_QSS = """
QWidget {
    background-color: #f3f5f8;
    color: #0f172a;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 12px;
}
QMainWindow, QMenuBar, QMenu, QToolBar {
    background-color: #f3f5f8;
    color: #0f172a;
    border: none;
}
QToolBar {
    spacing: 6px;
    padding: 4px 8px;
    border-bottom: 1px solid #d5dde6;
}
QMenuBar::item:selected, QMenu::item:selected { background-color: #e2e8f0; }
QStatusBar {
    background-color: #e8edf3;
    color: #475569;
    font-family: "Cascadia Mono", "Consolas", monospace;
    font-size: 11px;
}
QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #d5dde6;
    border-radius: 6px;
}
QPushButton {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 4px 10px;
}
QPushButton:hover { background-color: #e2e8f0; }
QPushButton#Primary {
    background-color: #0e7490;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#Danger { background-color: #b91c1c; color: #ffffff; border: none; }
QTableView, QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    selection-background-color: #a5f3fc;
    selection-color: #0f172a;
    border: 1px solid #d5dde6;
    border-radius: 4px;
    font-family: "Cascadia Mono", "Consolas", monospace;
    font-size: 12px;
}
QHeaderView::section {
    background-color: #e8edf3;
    color: #334155;
    padding: 4px 6px;
    border: none;
    font-family: "Segoe UI", sans-serif;
}
QLabel#Title { font-size: 13px; font-weight: 600; }
QLabel#Subtitle { color: #64748b; font-size: 11px; }
QLabel#Error { color: #b91c1c; }
QTabBar::tab { background: #e8edf3; padding: 5px 10px; }
QTabBar::tab:selected { background: #0e7490; color: #ffffff; }
QScrollArea { border: none; }
QSplitter::handle { background: #d5dde6; }
QComboBox {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 3px 8px;
    min-width: 180px;
}
"""


def ink_color(theme_name: str) -> str:
    return INK_LIGHT if theme_name == "light" else INK_DARK


def apply_theme(app: QApplication, name: str) -> None:
    """Aplica QSS y colores de Matplotlib. `name` es 'dark' o 'light'."""
    dark = name != "light"
    app.setStyleSheet(DARK_QSS if dark else LIGHT_QSS)
    face = "#101418" if dark else "#f3f5f8"
    text = INK_DARK if dark else INK_LIGHT
    grid = "#2a3440" if dark else "#cbd5e1"
    rcParams.update(
        {
            "figure.facecolor": face,
            "axes.facecolor": face,
            "axes.edgecolor": grid,
            "axes.labelcolor": text,
            "xtick.color": text,
            "ytick.color": text,
            "text.color": text,
            "axes.titlecolor": text,
            "grid.color": grid,
            "legend.facecolor": face,
            "legend.edgecolor": face,
            "savefig.facecolor": face,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
        }
    )
