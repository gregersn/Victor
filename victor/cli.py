#!/usr/bin/env python3
import click
from victor import generate
from victor import fill_sheet, fill_pdf
from typing import Optional
from victor.gui import start_gui


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        start_gui()


@cli.command()
@click.argument('charactersheet', type=click.Path(exists=True))
@click.argument('datafile', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), required=False,
              help="Destination file")
def fill(charactersheet: str, datafile: str, output: str = "output.pdf"):
    """Fill CHARACTERSHEET with DATA

    CHARACTERSHEET is a file to fill, or metadata describing the file to fill.
    DATA is yaml or json file containing the data to fill in.
    """
    fill_pdf(charactersheet, datafile, output)


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--average/--no-average', default=False, required=False,
              help="Output the average values instead of random.")
@click.option('--fill', type=click.Path(exists=True), required=False,
              help="Template to fill with generated data.")
@click.option('--output', type=click.Path(), required=False,
              help="Where to save filled template.")
def create(filename: str, average: bool = False, fill: Optional[str] = None,
           output: Optional[str] = None):
    character = generate(filename, average=average)

    if fill is not None:
        fill_sheet(fill, character, output)

    else:
        print(character)


if __name__ == '__main__':
    cli()
