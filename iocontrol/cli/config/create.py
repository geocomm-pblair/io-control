from pathlib import Path

import click
from rich.console import Console

from iocontrol.cli.config.group import config
from iocontrol.config.env import make


@config.command()
@click.option(
    "-p",
    "path",
    type=click.Path(
        dir_okay=False, writable=True, resolve_path=True, exists=False
    ),
)
def create(path: str):
    """Create a configuration file."""
    Console().print(f"{make(path=Path(path) if path else None)}")
