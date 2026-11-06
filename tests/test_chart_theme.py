"""Las gráficas deben respetar el tema claro u oscuro en el propio eje."""

import numpy as np
from matplotlib.colors import to_hex
from matplotlib.figure import Figure

from aproxlab.core.regression.linear import LinearRegression
from aproxlab.services.charts import plot_palette, plot_scatter_and_fits


def test_light_palette_paints_axes_light() -> None:
    palette = plot_palette("light")
    fig = Figure()
    ax = fig.add_subplot(111)
    fit = LinearRegression().fit([0, 1, 2], [1, 3, 5])
    plot_scatter_and_fits(
        ax,
        np.array([0.0, 1.0, 2.0]),
        np.array([1.0, 3.0, 5.0]),
        [(fit, palette.linear)],
        title="prueba",
        palette=palette,
    )
    assert to_hex(ax.get_facecolor()) == palette.face.lower()
    assert to_hex(fig.get_facecolor()) == palette.face.lower()
