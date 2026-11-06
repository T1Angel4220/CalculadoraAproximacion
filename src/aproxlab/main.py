"""Punto de entrada de AproxLab."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from aproxlab.ui.main_window import MainWindow
from aproxlab.ui.styles.theme import apply_theme


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv
    app = QApplication(args)
    app.setApplicationName("AproxLab")
    apply_theme(app, "dark")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
