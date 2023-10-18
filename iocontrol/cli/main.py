import click
import rich
from rich import pretty

from iocontrol.cli.errors import handled
from iocontrol.meta import this
from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class Context(BaseModel):
    """General context."""

    verbose: bool = Field(default=False, description="verbose output")
    yes: bool = Field(default=False, description='answer "yes" to all prompts')

    class Config:
        """Class configuration information."""

        arbitrary_types_allowed = True


@click.group()
@click.pass_context
@click.option("-v", "--verbose", help="verbose output", is_flag=True)
@click.option("-y", "--yes", is_flag=True, help='answer "yes" to all prompts')
def main(ctx, verbose: bool, yes: bool):
    f"""Run {this().name}."""
    pretty.install()
    ctx.obj = Context(verbose=verbose, yes=yes)


@main.command()
@click.pass_context
@handled()
def version(ctx):
    """Get the current version."""
    meta = this()

    if ctx.obj.verbose:
        rich.print_json(
            data=meta.dict(
                exclude_defaults=True, exclude_unset=True, exclude_none=True
            )
        )
    else:
        rich.print(f"[cyan]{meta.name}[/cyan] [green]{meta.version}[/green]")
