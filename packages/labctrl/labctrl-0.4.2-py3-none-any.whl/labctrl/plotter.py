""" """

import numpy as np
from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg

from labctrl.dataset import Dataset
from labctrl.logger import logger


class PlottingError(Exception):
    """ """


"""
class LivePlot(QtWidgets.QMainWindow):
    A pyqtgraph-based plotter for real-time plotting on a 2D Cartesian grid.

    def __init__(
        self,
        title: str = None,
        xlabel: str = None,
        xunits: str = None,
        ylabel: str = None,
        yunits: str = None,
    ) -> None:
        """ """
        super().__init__()
        self.setWindowTitle("LivePlotter")

        self.widget = pg.PlotWidget()
        self.setCentralWidget(self.widget)

        self.plt = self.widget.getPlotItem()
        self.plt.setLabels(title=title, bottom=(xlabel, xunits), left=(ylabel, yunits))
        self.plt.showGrid(x=True, y=True, alpha=0.1)
        self.plt.setMenuEnabled(False)
        self.legend = self.plt.addLegend(offset=(1, 1))

class LiveLinePlot(LivePlot):
    for line and scatter plots, with fits and error bars

    def __init__(
        self,
        scatter: bool = True,
        legend: list[str] = None,  # labels to identify multiple y traces
        show_fit: bool = False,
        show_err: bool = False,
        **kwargs,
    ) -> None:
        """ """
        super().__init__(**kwargs)

        self.traces = {}
        legend = ["y"] if legend is None else legend  # to initialize plots in one loop
        i = 0  # to count plots for assigning color
        n = len(legend) * 2 if show_fit else len(legend)  # total number of plots
        for name in legend:
            self.traces[name] = dict.fromkeys(("data", "fit", "err"))

            if scatter:
                kwargs = {"name": name, "brush": (i, n), "pen": None, "size": 5}
                self.traces[name]["data"] = pg.ScatterPlotItem(**kwargs)
            else:
                kwargs = {"name": name, "pen": pg.mkPen(i, n, width=2)}
                self.traces[name]["data"] = pg.PlotCurveItem(**kwargs)
            if show_err:
                self.traces[name]["err"] = pg.ErrorBarItem(pen=(i, n))
            i += 1

            if show_fit:
                kwargs = {"name": f"{name}_fit", "pen": pg.mkPen(i, n, width=2)}
                self.traces[name]["fit"] = pg.PlotCurveItem(**kwargs)
                i += 1

        for traces in self.traces.values():
            for trace in traces.values():
                if trace is not None:
                    self.plt.addItem(trace)

    def plot(self, x, **kwargs) -> None:
        x must be a 1D np array
        kwarg is the trace label (for single trace, use 'y') and value is a dict with keys = data, fit, err and value must be a 1D np array. fit and err are always optional args.
        
        for name, traces in kwargs.items():
            y = traces["data"]
            self.traces[name]["data"].setData(x, y)
            if "fit" in traces:
                self.traces[name]["fit"].setData(x, traces["fit"])
            if "err" in traces:
                self.traces[name]["err"].setData(x=x, y=y, height=traces["err"])


class LiveImagePlot(LivePlot):
    for colormaps (linear scale)

    def __init__(
        self,
        xmin: float,
        xmax: float,
        xlen: int,
        ymin: float,
        ymax: float,
        ylen: int,
        cmap: str = "viridis",
        zlabel: str = None,
        **kwargs,
    ) -> None:
        """ """
        super().__init__(**kwargs)

        self.image = pg.ImageItem(
            image=np.zeros((ylen, xlen)),  # nominal z data
            axisOrder="row-major",
            rect=[xmin, ymin, xmax - xmin, ymax - ymin],  # bounding box for image
        )
        self.plt.addItem(self.image)
        cmap = pg.colormap.get(cmap, source="matplotlib")
        self.colorbar = pg.ColorBarItem(colorMap=cmap, label=zlabel, interactive=False)
        self.colorbar.setImageItem(self.image, insert_in=self.plt)

    def plot(self, z: np.ndarray) -> None:
        """ """
        self.image.setImage(image=z)
        self.colorbar.setLevels(low=z.min(), high=z.max())
"""


class LivePlot:
    """ """


class Plotter:
    """
    Context manager for live plotting. Responsible for signal/slot interaction between Experiment and LivePlots that are part of its plotting session. LivePlots run in their own thread, and are updated by calling the LivePlotter's plot() method with the Dataset and the new data to be plotted. Caller is responsible for ensuring the data sent to plot() is compatible with the Dataset axes.
    """

    # maximum number of plot items supported in one window
    maxplots: int = 4

    def __init__(self, *datasets: Dataset) -> None:
        """ """
        try:
            self._datasets = {dset.name: dset for dset in datasets if dset.plot}
        except (AttributeError, TypeError):
            message = f"Please check if you provided valid init args of type Dataset."
            logger.error(message)
            raise PlottingError(message)
        else:
            numplots, maxplots = len(self._datasets), Plotter.maxplots
            if numplots > maxplots:
                message = f"{numplots} plots specified, Plotter supports {maxplots = }."
                logger.error(message)
                raise PlottingError(message)

            if self._datasets:
                self._initialize_plots()

    def _initialize_plots(self) -> None:
        """ """
        view = pg.RemoteGraphicsView()
        view.pg.setConfigOptions(antialias=True)
        view.setWindowTitle("EXAMPLE")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    """
    lp = LiveImagePlot(
        title="live plot",
        xmin=0,
        xmax=2,
        xlen=10,
        ymin=1,
        ymax=4,
        ylen=8,
        xlabel="X",
        xunits="s",
        ylabel="Y",
        yunits="m",
        zlabel="test",
        cmap="twilight_shifted",
    )

    z = np.random.uniform(low=0.0, high=6.0, size=(8, 10))
    lp.plot(zdata=z)

    
    lp = LiveLinePlot(
        title="live plot",
        xlabel="X",
        xunits="s",
        ylabel="Y",
        yunits="m",
        scatter=False,
        legend=["A", "B"],
        show_fit=True,
        show_err=True,
    )

    x = np.linspace(0, 1, 50)
    kwargs = {
        "A": {
            "data": np.linspace(4, 5, 50),
            "fit": np.linspace(4.2, 4.9, 50),
            "err": 0.1,
        },
        "B": {
            "data": np.linspace(3, 4, 50),
            "fit": np.linspace(3.2, 3.9, 50),
            "err": np.linspace(0, 0.2, 50),
        },
    }
    lp.plot(x=x, **kwargs)

    lp.show()
    app.exec()
    """
