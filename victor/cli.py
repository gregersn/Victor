#!/usr/bin/env python3
import click
from . import generate
from . import fill_sheet
from typing import Optional


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--average/--no-average', default=False, required=False,
              help="Output the average values instead of random.")
@click.option('--fill', type=click.Path(exists=True), required=False,
              help="Template to fill with generated data.")
@click.option('--output', type=click.Path(), required=False,
              help="Where to save filled template.")
def main(filename: str, average: bool = False, fill: Optional[str] = None,
         output: Optional[str] = None):
    character = generate(filename, average=average)

    if fill is not None:
        fill_sheet(fill, character, output)

    else:
        print(character)


if __name__ == '__main__':
    main()
