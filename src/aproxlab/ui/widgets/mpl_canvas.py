"""Canvas Matplotlib embebido en Qt."""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None) -> None:
        figure = Figure(figsize=(5.4, 3.1), layout="tight")
        super().__init__(figure)
        self.setParent(parent)
        self.axes = figure.add_subplot(111)

    def save_png(self, path: str) -> None:
        self.figure.savefig(path, dpi=140)
