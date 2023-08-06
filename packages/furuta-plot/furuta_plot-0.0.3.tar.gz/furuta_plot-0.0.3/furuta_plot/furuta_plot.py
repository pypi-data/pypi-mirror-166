"""
furuta_plot.py - High-level plotting interface
"""

import logging
import os

from collections import namedtuple

from matplotlib import projections
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from . import backend
from .types import TypeTuple, TypeInt, TypeFloat, TypeBool

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

Spec = namedtuple("Spec", ("default", "type"))


class FurutaPlotter:
    """
    FurutaPlotter can have its configuration controlled be getting and setting
    attributes on the created object. Like p.<option> = <value>

    Configuration Options
    ---------------------
    gridsize : tuple
        Size of the Figure grid, i.e. how many plots that can fit (default is (1, 1))

    negate_phi : float
        Whether to negate the phi angle (default is False)

    negate_theta : float
        Whether to negate the theta angle (default is False)

    scale_phi : float
        How much to scale the phi angle by (default is 1.0)

    scale_theta : float
        How much to scale the theta angle by (default is 1.0)

    translate_phi : float
        How much to translate the phi angle by (default is 0.0)

    translate_theta : float
        How much to translate the theta angle by (default is 0.0)
    """
    DEFAULT_OPTIONS = {
        "gridsize": Spec(default=(1, 1), type=TypeTuple(len=2, item_type=TypeInt(min=1))),
        "negate_phi": Spec(default=False, type=TypeBool()),
        "negate_theta": Spec(default=False, type=TypeBool()),
        "scale_phi": Spec(default=1.0, type=TypeFloat()),
        "scale_theta": Spec(default=1.0, type=TypeFloat()),
        "translate_phi": Spec(default=0.0, type=TypeFloat()),
        "translate_theta": Spec(default=0.0, type=TypeFloat()),
    }

    def __init__(self, fig, **optargs):
        """
        Constructor.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            The figure to plot on.
        """
        self.__fig = fig
        self.__3dplots = []
        self.__linearplots = []

        # These can later be accessed by self.<name>
        self.__options = {k: v.default for k,v in FurutaPlotter.DEFAULT_OPTIONS.items()}
        self.set_options(**optargs)

    def __getattr__(self, name):
        if name.startswith("_") or name not in self.__options:
            return super().__getattribute__(name)
        else:
            return self.__options[name]

    def __setattr__(self, name, value):
        if name.startswith("_") or name not in self.__options:
            return super().__setattr__(name, value)
        else:
            return self.set_options(**{name: value})

    def set_options(self, **optargs):
        """
        Sets the provided options, also performing some sanity checks.
        """
        for key, value in optargs.items():
            LOG.debug(f"Performing sanity check on \"{key}\"")
            try:
                FurutaPlotter.DEFAULT_OPTIONS[key].type.check(value)
            except TypeError as e:
                raise TypeError(f"type error on \"{key}\": {str(e)}")
            else:
                self.__options[key] = value

    def add_3D(self, phi="phi", theta="theta", span=(1, 1),
               phi_transform=None,
               theta_transform=None,
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
            Transformation to apply to the phi values (default is the plotter options defined transformation)

        theta_transform : function, optional
            Transformation to apply to the theta values (default is the plotter options defined transformation)

        render_margin : float, optional
            Rendering margin for x, y, and z limits on the 3D plot (default is 0.0)

        include_legend : bool, optional
        """
        ax3d = self.__fig.add_subplot(self.gridsize[0], self.gridsize[1], span, projection="3d")
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
                   x_transform=None,
                   y_transform=None,
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
            Transformation to apply to the x-values (default is no transformation)

        y_transform : function, optional
            Transformation to apply to the y-values (default is no transformation)

        color : color, optional
            Color to use in the plot (default is "red")

        max_lookback : int, optional
            Limit on how many data points to plot from the last (default is no limit)
        """
        ax = self.__fig.add_subplot(self.gridsize[0], self.gridsize[1], span, projection="rectilinear")
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

    def _builtin_phi_transform(self, phi):
        if self.negate_phi:
            phi = -phi

        return (phi * self.scale_phi) + self.translate_phi

    def _builtin_theta_transform(self, theta):
        if self.negate_theta:
            theta = -theta

        return (theta * self.scale_theta) + self.translate_theta

    def _plot_axes(self, data, idx=None):
        """Internal function for plotting all the contained axes."""
        for ax3d, properties in self.__3dplots:
            ax3d.clear()
            phi = data[properties["phi"]]
            theta = data[properties["theta"]]
            if idx is not None:
                phi = phi[idx]
                theta = theta[idx]

            phi_transform = properties["phi_transform"]
            theta_transform = properties["theta_transform"]
            if phi_transform is None:
                phi_transform = self._builtin_phi_transform
            if theta_transform is None:
                theta_transform = self._builtin_theta_transform

            backend.plot_3D_axes(ax3d,
                                 phi_transform(phi),
                                 theta_transform(theta),
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

            x_transform = properties["x_transform"]
            y_transform = properties["y_transform"]
            if x_transform is None:
                x_transform = lambda x: x
            if y_transform is None:
                y_transform = lambda y: y

            xs = [x_transform(x) for x in xs]
            ys = [y_transform(y) for y in ys[min_idx:max_idx]]

            ax.plot(xs, ys, color=properties["color"])
            if properties["x_label"] is not None:
                ax.set_xlabel(properties["x_label"])
            if properties["y_label"] is not None:
                ax.set_ylabel(properties["y_label"])

    def animate(self, fps=30, save_as=None, **data):
        """
        Animates the pendulum over the length of data.

        Parameters
        ----------
        fps : float, optional
            Frames per second (default is 30)

        save_as : str, optional
            Filename to save animation as, rather than to visualize it
            directly. Note that this require ffmpeg to be installed (default is None)

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
            self.__fig,
            iterate,
            fargs=(),
            frames=_datalength,
            interval=(1000/fps),
            repeat=False
        )
        if save_as is not None:
            LOG.debug("Saving animation as file")
            mp4_writer = animation.FFMpegWriter(fps=fps, codec="h264")

            contents = os.listdir(".")

            if save_as.endswith(".mp4"):
                save_as = save_as[:-4]

            filename = f"{save_as}.mp4"
            f_suffix = 1
            while filename in contents:
                filename = f"{save_as}-{f_suffix}.mp4"
                f_suffix += 1

            LOG.info(f"Saving as {filename}... (this may take a couple of minutes)")
            ani.save(filename, writer=mp4_writer)
            LOG.info("Movie clip saved.")
        else:
            LOG.info("Rendering animation")
            plt.show()
