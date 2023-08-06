from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent


def find_requirements(filename):
    with (ROOT / filename).open() as requirements_file:
        lines = map(str.strip, requirements_file)

        return [line for line in lines if not line.startswith("#")]


setup(
    name="cpflows",
    version="0.1.2",
    author="CWHuang",
    packages=find_packages("."),
    description="Convex Potential Flows package",
    include_package_data=True,
    install_requires=[
        "backports.functools-lru-cache>=1.6.1",
        "cycler>=0.10.0",
        "future>=0.17.1",
        "kiwisolver>=1.1.0",
        "matplotlib>=3.0",
        "numpy>=1.16",
        "pandas>=1.0",
        "pyparsing>=2.4.7",
        "python-dateutil>=2.8.1",
        "pytz>=2020.1",
        "scikit-learn",
        "scipy",
        "seaborn>=0.9.1",
        "six>=1.15.0",
        "subprocess32>=3.5.3",
        "torch>=1.9",
        "torchvision",
        "tqdm>=4.23",
        "h5py",
    ],
    license="MIT",
    url="https://github.com/KelvinKan/CP-Flow",
    entry_points={},
)