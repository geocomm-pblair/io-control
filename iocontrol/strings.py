import random as random_
import string

import jinja2

_jinja = jinja2.Environment(autoescape=True)  #: the Jinja2 environment


def render(template: str, **kwargs) -> str:
    """
    Render a ``Jinja`` template string.

    :param template: the template string
    :returns: the rendered string

    .. seealso::

        * https://jinja.palletsprojects.com/en/3.1.x/
    """
    return _jinja.from_string(template).render(**kwargs)


def random(length: int = 32) -> str:
    """
    Get a randomized string.

    :returns: the tracking identifier
    """
    return "".join(
        random_.choices(  # nosec B311
            string.ascii_uppercase + string.ascii_lowercase, k=length
        )
    )
