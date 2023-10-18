import asyncio
from functools import wraps


def coroutine(f):
    """Decorator for asynchronous ``click`` commands."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Function wrapper."""
        return asyncio.run(f(*args, **kwargs))

    return wrapper
