import sys
import traceback
from functools import wraps
from typing import Tuple
from typing import Type

from iocontrol.cli.console import pprint
from iocontrol.errors import AppException
from iocontrol.errors import ErrorMessage


def handled(handle: Tuple[Type[Exception], ...] = (Exception,)):
    """
    Common exception handler decorator.

    :param handle: handled exception types
    """

    def decorator(func):
        """
        Create the function wrapper.

        :param func: the function
        :return: the function result
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except handle as ex:
                # Whatever we got, we want a structured exception.
                if isinstance(ex, AppException):
                    gex = ex
                else:
                    gex = AppException(event=str(ex))
                # Prepare the content of the response.
                msg = ErrorMessage(
                    status_code=gex.status_code,
                    event=gex.event,
                    traceback=tuple(traceback.format_exc().split("\n")),
                )
                pprint(msg, error=True)
                sys.exit(1)

        return wrapper

    return decorator
