from iocontrol.config.logging.main import LoggingConfig
from iocontrol.config.logging.profiles import default


def configure(config: LoggingConfig):
    """
    Default logging configuration.

    :param config: the logging config
    """
    # We can mostly use the standard configuration, we just don't want to see
    # logging output unless things are *really* bad.
    default.configure(config=config, level="critical")
