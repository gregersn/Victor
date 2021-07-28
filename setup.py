# pyright: reportMissingTypeStubs=false
from setuptools import setup, find_packages

setup(
    name="Victor",
    description="Tool for generating character stats for TTRPGs",
    version="0.1.0",
    author="Greger Stolt Nilsen",
    author_email="gregersn@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/gregersn/Victor",
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
