import json

import click
import yaml
from rich.console import Console
from rich.syntax import Syntax

from iocontrol.cli.api.group import api


@api.command()
@click.option(
    "-f",
    "--format",
    "format_",
    type=click.Choice(["yaml", "json"]),
    show_default=True,
    default="yaml",
    help="Export format.",
)
@click.option(
    "-s",
    "--syntax",
    "syntax_",
    is_flag=True,
    help="Highlight syntax.",
)
def export(format_: str, syntax_: int):
    """Export the API specification."""
    # Don't load the FastAPI app unless we're actually using it.
    from iocontrol.api import app

    openapi = app.openapi()
    output = {
        "yaml": lambda: yaml.dump(openapi, sort_keys=False),
        "json": lambda: json.dumps(openapi, indent=2),
    }[format_]()
    if syntax_:
        console = Console()
        syntax = Syntax(output, format_)
        console.print(syntax)
    else:
        print(output)
