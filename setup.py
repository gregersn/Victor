# pyright: reportMissingTypeStubs=false
from setuptools import setup, find_packages

setup(
    name="Victor",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "PyMuPDF",
        "pyaml",
        "PySimpleGUI==5.0.0",
        "trill",
        "ringneck",
    ],
    entry_points={"console_scripts": ["victor = victor.cli:cli"]},
)
