from functools import lru_cache
from typing import List

from fastapi import Depends
from frontegg.fastapi import frontegg

from iocontrol import logging
from iocontrol.api.auth.errors import UnauthorizedException
from iocontrol.api.auth.providers.base import SecurityProvider
from iocontrol.api.auth.providers.vendorized import (
    frontegg_security as vendorized,
)
from iocontrol.api.auth.users import User
from iocontrol.config import config
from iocontrol.errors import ConfigurationException


class FronteggSecurityProvider(SecurityProvider):
    """Security provider for Frontegg."""

    @classmethod
    @lru_cache(maxsize=1)
    def init(cls):
        """Initialize Frontegg."""
        # Get the Frontegg configuration.
        config_ = config().api.auth.frontegg
        # Make sure everything is configured.
        errors = []
        if not config_.client.client_id:
            errors.append("The Frontegg client ID is not configured.")
        if not config_.api.api_key:
            errors.append("The Frontegg API key is not configured.")
        try:
            # If we detected any missing configuration, raise an exception so
            # that we may...
            if errors:
                raise ConfigurationException(
                    "The Frontegg security provider is not configured."
                )
        except ConfigurationException as ce:
            # ...log it, with all the details.
            logging.exception(ce.event, errors=errors)
            raise
        try:
            frontegg.init_app(
                client_id=config_.client.client_id,
                api_key=config_.api.api_key.get_secret_value(),
            )
        except Exception as ex:
            raise ConfigurationException(
                "Frontegg initialization failed."
            ) from ex

    @classmethod
    def security(
        cls,
        permissions: List[str] = None,
        auto_error: bool = True,
        roles: List[str] = None,
        super_user: bool = False,
    ):
        """
        Configure endpoint security.

        :param permissions: required permissions
        :param auto_error: raise errors if security fails
        :param roles: required roles
        :param super_user: requires super-user permissions
        """

        def security_(
            user: User = Depends(
                vendorized.FronteggHTTPAuthentication(
                    auto_error=auto_error, roles=roles, permissions=permissions
                )
            )
        ) -> User:
            if super_user and not user.super_user:
                raise UnauthorizedException("You are not a super user.")
            return user

        return security_
