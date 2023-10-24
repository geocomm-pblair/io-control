from iocontrol.api.auth.providers.vendorized import frontegg_security
from pydantic import ConfigDict


class User(frontegg_security.User):
    """
    Describes a user.

    The ``User`` model is based on Frontegg's ``User``.
    """

    model_config = ConfigDict(populate_by_name=True)
