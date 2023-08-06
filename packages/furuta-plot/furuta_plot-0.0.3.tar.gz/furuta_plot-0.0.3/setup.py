import os
from setuptools import setup, find_packages

__version__ = "0.0.3"

WORKDIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(WORKDIR, "README.rst"), "r") as f:
    README_TEXT = f.read()

setup(
    name="furuta_plot",
    version=__version__,
    license="MIT License",
    author="John Wikman",
    url="https://github.com/johnwikman/furuta-plot",
    keywords=["ipm", "furuta", "plot", "visualizer"],
    description="A furuta pendulum plotter based on matplotlib.",
    long_description=README_TEXT,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib", "numpy"],
    packages=find_packages(
        where=".",
        include=["furuta_plot"],
    ),
)
