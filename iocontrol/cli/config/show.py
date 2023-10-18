from iocontrol import config
from iocontrol.cli.config.group import config as config_
from iocontrol.cli.console import pprint


@config_.command()
def show():
    """Show the current configuration."""
    pprint(config.config())
