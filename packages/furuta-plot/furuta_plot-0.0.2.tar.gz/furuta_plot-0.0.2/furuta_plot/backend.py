"""
backend.py - Backend callbacks for plotting
"""

import matplotlib
import mpl_toolkits
import numpy as np


def plot_3D_axes(ax, phi, theta,
                 l_arm=1.0,
                 l_pendulum=1.0,
                 lw_arm=5.0,
                 lw_pendulum=3.0,
                 color_arm="blue",
                 color_pendulum="orange",
                 render_margin=None):
    """
    Backend function used to plot a furuta pendulum on a 3D Axes.

    Assume that we are looking straight on to point on the arm while at a
    distance from the DC motor. Then theta is the angle from the positive
    y-axis towards the positive x-axis:
             . y
            /|\
             |
             |θ/
             |/
      ---------------> x
             |
             |
             |
    
    Starting at the position where phi = 0, the pendulum base is located at
    x=l_arm, y,z=0. Then x turns to y and y turn to z in the plot above.

    Adjust your phi and theta according to this reference above.

    Parameters
    ----------
    ax : mpl_toolkits.mplot3d.axes3d.Axes3D
        The axes to plot on.

    phi : float
        The angle of the swinging arm.

    theta : float
        The angle of the pendulum.

    l_arm : float, optional
        The length of the swinging arm (default is 1.0)

    l_pendulum : float, optional
        The length of the pendulum (default is 1.0)

    lw_arm : float, optional
        Width of the line representing the swinging arm (default is 5.0)

    lw_pendulum : float, optional
        Width of the line representing the pendulum (default is 3.0)

    color_arm : color, optional
        Matplotlib color for the swinging arm (default is "blue")

    color_pendulum : color, optional
        Matplotlib color for the swinging arm (default is "orange")

    render_margin : float, optional
        Margin to add to the edge of the plot. Has no effect is the value is
        None (default is None)
    """

    # See description in the docstring above.
    initial_pendulum_tip_coord = [
        l_arm,
        l_pendulum * np.cos((np.pi / 2) - theta),
        l_pendulum * np.sin((np.pi / 2) - theta)
    ]

    # Arm is in a level plane looking from above. Assume phi is angle from
    # x-axis in direction towards the positive y-axis (i.e. unit circle)
    # Now apply transformation to rotate the frame in accordance with phi. Our
    # new basis vectors are:
    phi_matrix = np.array([
        [np.cos(phi),  np.sin(phi), 0.0], # x-vector
        [-np.sin(phi), np.cos(phi), 0.0], # y-vector
        [0.0,          0.0,         1.0]  # z-vector (unaffected)
    ])

    initial_coords = np.array([
        [0.0,   0.0, 0.0], # origin
        [l_arm, 0.0, 0.0], # arm tip when phi=0
        initial_pendulum_tip_coord
    ])

    coords = np.transpose(np.matmul(
        phi_matrix,
        np.transpose(initial_coords)
    ))

    def split(coord_list):
        xs = [c[0] for c in coord_list]
        ys = [c[1] for c in coord_list]
        zs = [c[2] for c in coord_list]
        return xs, ys, zs

    ax.plot3D(*split(coords[0:2]), label="Arm", linewidth=lw_arm, color=color_arm)
    ax.plot3D(*split(coords[1:3]), label="Pendulum", linewidth=lw_pendulum, color=color_pendulum)

    if render_margin is not None:
        ax.set_xlim([-abs(l_arm) - render_margin, abs(l_arm) + render_margin])
        ax.set_ylim([-abs(l_arm) - render_margin, abs(l_arm) + render_margin])
        ax.set_zlim([-abs(l_pendulum) - render_margin, abs(l_pendulum) + render_margin])
