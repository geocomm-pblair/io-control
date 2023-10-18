from pathlib import Path

import click

from iocontrol.cli.api.group import api
from iocontrol.config import config


@api.command()
@click.option(
    "-R",
    "--reload",
    is_flag=True,
    show_default=True,
    default=False,
    help="Monitor the source for changes and reload.",
)
def start(reload: bool):
    """Start the API service."""
    import uvicorn

    cfg = config()
    _api = cfg.api
    uvicorn.run(
        app=_api.app,
        host=str(_api.bind),
        port=_api.port,
        log_level=cfg.logging.level.lower(),
        reload=reload,
        reload_dirs=(
            [str(Path(__file__).parent.parent.parent)] if reload else None
        ),
        # NOTE TO THE FUTURE: The lines below represent an attempt to reload
        # automatically when the environment file changes.  It hasn't worked
        # out so far, but if you're keen to try... here's what's been tried
        # so far...
        # reload_dirs=[Path(__file__).parent.parent.parent, home() / "config"]
        # if reload
        # else None,
        # reload_includes=["*.env"],
        # env_file=str(env_file()),
    )
