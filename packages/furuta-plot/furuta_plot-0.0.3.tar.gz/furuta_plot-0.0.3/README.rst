===========
Furuta Plot
===========

A plot utility for a furuta pendulum based on matplotlib.


Usage
=====

Plots are best constructed using the ``FurutaPlotter`` wrapper class. Here is
an example of how to plot a 3D animation of the pendulum and arm swinging at a
constant rate for 10 seconds:

.. code-block:: python

    import matplotlib.pyplot as plt
    import numpy as np

    from furuta_plot import FurutaPlotter

    FPS = 30
    TOTAL_FRAMES = FPS * 10

    fig = plt.figure()
    p = FurutaPlotter(fig)
    p.add_3D()

    # One data point for each frame
    phis = [2 * np.pi * i / (2*FPS) for i in range(TOTAL_FRAMES)]
    thetas = [2 * np.pi * i / (FPS) for i in range(TOTAL_FRAMES)]

    p.animate(fps=FPS, phi=phis, theta=thetas)

See the ``examples/`` directory in the git repository for more usage examples.


Running Locally
===============

If matplotlib and numpy are installed, then you can run one of the examples
directly by putting the PYTHONPATH variable in front:

.. code-block::

    PYTHONPATH=. python3 examples/animated.py
