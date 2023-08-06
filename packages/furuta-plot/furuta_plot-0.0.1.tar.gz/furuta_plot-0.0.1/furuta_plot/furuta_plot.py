"""
furuta_plot.py - High-level plotting interface
"""

from . import backend

from matplotlib import projections
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class FurutaPlotter:
    def __init__(self, fig, gridsize=(1, 1)):
        """
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The figure to plot on.

        gridsize : tuple, optional
            Size of the Figure grid, i.e. how many plots that can fit (default is (1, 1))
        """
        self.fig = fig
        self.gridsize = gridsize

        self.__3dplots = []
        self.__linearplots = []

    def add_3D(self, phi="phi", theta="theta", span=(1, 1),
               phi_transform=lambda a: a,
               theta_transform=lambda a: a,
               render_margin=0.0,
               include_legend=True):
        """
        Adds a 3D visualization plot.

        Parameters
        ----------
        phi : str, optional
            The name for the datafield to use for the phi angle data (default is "phi")

        theta : str, optional
            The name for the datafield to use for the theta angle data (default is "theta")

        span : tuple, optional
            The position span in the figure to draw the plot on (default is (1, 1))

        phi_transform : function, optional
            Transformation to apply to the phi values (default is identity function)

        theta_transform : function, optional
            Transformation to apply to the theta values (default is identity function)

        render_margin : float, optional
            Rendering margin for x, y, and z limits on the 3D plot (default is 0.0)

        include_legend : bool, optional
        """
        ax3d = self.fig.add_subplot(self.gridsize[0], self.gridsize[1], span, projection="3d")
        self.__3dplots.append((ax3d, {
            "phi": phi,
            "theta": theta,
            "phi_transform": phi_transform,
            "theta_transform": theta_transform,
            "render_margin": render_margin,
            "include_legend": include_legend
        }))

    def add_linear(self, y, x=None, span=(1, 1),
                   x_label=None,
                   y_label=None,
                   x_transform=lambda a: a,
                   y_transform=lambda a: a,
                   color="red",
                   max_lookback=None):
        """
        Parameters
        ----------
        y : str
            The name of the data field to use for the y-axis values

        x : str, optional
            The name of the data field to use for the x-axis values (default is to use index as x)

        span : tuple, optional
            The position span in the figure to draw the plot on (default is (1, 1))

        x_label : str, optional
            The label to use for the x-axis (default is to use x data field name)

        y_label : str, optional
            The label to use for the y-axis (default is to use y data field name)

        x_transform : function, optional
            Transformation to apply to the x-values (default is the identity function)

        y_transform : function, optional
            Transformation to apply to the y-values (default is the identity function)

        color : color, optional
            Color to use in the plot (default is "red")

        max_lookback : int, optional
            Limit on how many data points to plot from the last (default is no limit)
        """
        ax = self.fig.add_subplot(self.gridsize[0], self.gridsize[1], span, projection="rectilinear")
        if x_label is None and x is not None:
            x_label = x
        if y_label is None and y is not None:
            y_label = y
        self.__linearplots.append((ax, {
            "x": x,
            "y": y,
            "x_label": x_label,
            "y_label": y_label,
            "x_transform": x_transform,
            "y_transform": y_transform,
            "color": color,
            "max_lookback": max_lookback
        }))

    def _plot_axes(self, data, idx=None):
        """Internal function for plotting all the contained axes."""
        for ax3d, properties in self.__3dplots:
            ax3d.clear()
            phi = data[properties["phi"]]
            theta = data[properties["theta"]]
            if idx is not None:
                phi = phi[idx]
                theta = theta[idx]

            backend.plot_3D_axes(ax3d,
                                 properties["phi_transform"](phi),
                                 properties["theta_transform"](theta),
                                 render_margin=properties["render_margin"])
            if properties["include_legend"]:
                ax3d.legend()

        for ax, properties in self.__linearplots:
            ax.clear()

            ys = data[properties["y"]]
            if idx is not None:
                ys = ys[:idx+1]

            min_idx = 0 if properties["max_lookback"] is None else max(0, len(ys) - properties["max_lookback"])
            max_idx = len(ys)
            if properties["x"] is not None:
                xs = data[properties["x"]][min_idx:max_idx]
            else:
                xs = list(range(min_idx, max_idx))

            xs = [properties["x_transform"](x) for x in xs]
            ys = [properties["y_transform"](y) for y in ys[min_idx:max_idx]]

            ax.plot(xs, ys, color=properties["color"])
            if properties["x_label"] is not None:
                ax.set_xlabel(properties["x_label"])
            if properties["y_label"] is not None:
                ax.set_ylabel(properties["y_label"])

    def animate(self, fps=30, **data):
        """
        Animates the pendulum over the length of data.

        Parameters
        ----------
        fps : float, optional
            Frames per second (default is 30)

        data : keyword arguments
            The data to be plotted, must map to collections of the same length
        """
        if len(data) == 0:
            raise ValueError("No data provided")
        _datakeys = list(data.keys())
        _datalength = len(data[_datakeys[0]])
        for dkey in _datakeys[1:]:
            if len(data[dkey]) != _datalength:
                raise ValueError(f"length mismatch in input data \"{dkey}\", expected length {_datalength}")

        def iterate(i):
            self._plot_axes(data, i)

        ani = animation.FuncAnimation(
            self.fig,
            iterate,
            fargs=(),
            frames=_datalength,
            interval=(1000/fps),
            repeat=False
        )
        plt.show()
