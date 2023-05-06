#!/usr/bin/env python3
"""Victor initiator script."""
from pathlib import Path
from typing import Optional

import click

from victor import generate
from victor import fill_sheet, fill_pdf


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    """Handle non-command."""
    if ctx.invoked_subcommand is None:
        try:
            from victor.gui import start_gui
            start_gui()
        except ImportError as exc:
            print(f"Could not import GUI libs: {exc}")


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
@click.argument('filename', type=click.Path(path_type=Path, exists=True))
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
        for key, value in character.items():
            if value is None:
                continue
            if isinstance(value, list):
                print(f"{key}: {', '.join([str(v) for v in value])}")
                continue
            if isinstance(value, dict):
                print(f"{key}:")
                for key, v in value.items():
                    print(f"- {key}: {v}")
                continue
            print(f"{key}: {value}")


if __name__ == '__main__':
    cli()
