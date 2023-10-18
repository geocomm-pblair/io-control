def configure(profile: str = None):
    """
    Configure logging.

    :param profile: the logging configuration
    """
    from iocontrol.config import logging

    logging.configure(profile=profile)
