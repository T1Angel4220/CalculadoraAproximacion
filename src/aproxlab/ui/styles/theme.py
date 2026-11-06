"""Temas claro/oscuro y sincronización con Matplotlib."""

from __future__ import annotations

from matplotlib import rcParams
from PySide6.QtWidgets import QApplication

DARK_QSS = """
QWidget {
    background-color: #0f1419;
    color: #e7ecf3;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}
QMainWindow, QMenuBar, QMenu {
    background-color: #0f1419;
    color: #e7ecf3;
}
QMenuBar::item:selected, QMenu::item:selected {
    background-color: #1e293b;
}
QStatusBar {
    background-color: #0b1015;
    color: #94a3b8;
}
QFrame#Card, QFrame#Banner {
    background-color: #171e27;
    border: 1px solid #243040;
    border-radius: 12px;
}
QFrame#Sidebar {
    background-color: #121821;
    border-right: 1px solid #243040;
}
QListWidget {
    background: transparent;
    border: none;
    outline: none;
    padding: 8px;
}
QListWidget::item {
    padding: 10px 12px;
    margin: 4px 8px;
    border-radius: 8px;
    color: #cbd5e1;
}
QListWidget::item:selected {
    background-color: #0e7490;
    color: #f8fafc;
}
QListWidget::item:hover {
    background-color: #1e293b;
}
QPushButton {
    background-color: #1e293b;
    color: #e7ecf3;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 14px;
}
QPushButton:hover { background-color: #334155; }
QPushButton#Primary {
    background-color: #0891b2;
    border: none;
    font-weight: 600;
}
QPushButton#Primary:hover { background-color: #0e7490; }
QPushButton#Danger {
    background-color: #7f1d1d;
    border: none;
}
QTableView {
    background-color: #121821;
    alternate-background-color: #171e27;
    gridline-color: #243040;
    selection-background-color: #0e7490;
    border: 1px solid #243040;
    border-radius: 8px;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #cbd5e1;
    padding: 6px;
    border: none;
    border-right: 1px solid #243040;
}
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#Subtitle { color: #94a3b8; }
QLabel#MetricValue { font-size: 20px; font-weight: 600; color: #67e8f9; }
QLabel#MetricName { color: #94a3b8; font-size: 12px; }
QLabel#Equation { font-size: 18px; font-family: "Cascadia Mono", "Consolas", monospace; }
QLabel#Error { color: #fca5a5; }
QTabWidget::pane { border: 1px solid #243040; border-radius: 8px; }
QTabBar::tab {
    background: #171e27;
    padding: 8px 14px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected { background: #0e7490; }
QScrollArea { border: none; }
"""

LIGHT_QSS = """
QWidget {
    background-color: #f4f6f9;
    color: #0f172a;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}
QMainWindow, QMenuBar, QMenu { background-color: #f4f6f9; color: #0f172a; }
QMenuBar::item:selected, QMenu::item:selected { background-color: #e2e8f0; }
QStatusBar { background-color: #e8edf3; color: #475569; }
QFrame#Card, QFrame#Banner {
    background-color: #ffffff;
    border: 1px solid #d7dee8;
    border-radius: 12px;
}
QFrame#Sidebar {
    background-color: #eef2f6;
    border-right: 1px solid #d7dee8;
}
QListWidget { background: transparent; border: none; padding: 8px; }
QListWidget::item {
    padding: 10px 12px;
    margin: 4px 8px;
    border-radius: 8px;
    color: #334155;
}
QListWidget::item:selected { background-color: #0e7490; color: #ffffff; }
QListWidget::item:hover { background-color: #e2e8f0; }
QPushButton {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 14px;
}
QPushButton:hover { background-color: #e2e8f0; }
QPushButton#Primary {
    background-color: #0e7490;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#Danger { background-color: #b91c1c; color: #ffffff; border: none; }
QTableView {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    gridline-color: #e2e8f0;
    selection-background-color: #67e8f9;
    selection-color: #0f172a;
    border: 1px solid #d7dee8;
    border-radius: 8px;
}
QHeaderView::section {
    background-color: #e8edf3;
    color: #334155;
    padding: 6px;
    border: none;
}
QLabel#Title { font-size: 22px; font-weight: 700; }
QLabel#Subtitle { color: #64748b; }
QLabel#MetricValue { font-size: 20px; font-weight: 600; color: #0e7490; }
QLabel#MetricName { color: #64748b; font-size: 12px; }
QLabel#Equation { font-size: 18px; font-family: "Cascadia Mono", "Consolas", monospace; }
QLabel#Error { color: #b91c1c; }
QTabBar::tab { background: #e8edf3; padding: 8px 14px; }
QTabBar::tab:selected { background: #0e7490; color: #ffffff; }
QScrollArea { border: none; }
"""


def apply_theme(app: QApplication, name: str) -> None:
    """Aplica QSS y colores de Matplotlib. `name` es 'dark' o 'light'."""
    dark = name != "light"
    app.setStyleSheet(DARK_QSS if dark else LIGHT_QSS)
    face = "#0f1419" if dark else "#f4f6f9"
    text = "#e7ecf3" if dark else "#0f172a"
    grid = "#334155" if dark else "#cbd5e1"
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
        }
    )
