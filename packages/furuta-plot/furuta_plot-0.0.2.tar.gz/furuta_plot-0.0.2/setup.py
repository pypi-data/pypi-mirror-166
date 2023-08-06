from setuptools import setup, find_packages

__version__ = "0.0.2"

setup(
    name="furuta_plot",
    version=__version__,
    license="MIT License",
    author="John Wikman",
    url="https://github.com/johnwikman/furuta-plot",
    keywords=["ipm", "furuta", "plot", "visualizer"],
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
