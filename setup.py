# pyright: reportMissingTypeStubs=false
from setuptools import setup, find_packages

setup(
    name="Victor",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pikepdf'
    ],
    entry_points={
        'console_scripts': [
            'victor = victor.cli:main'
        ]
    }
)
