import json
import uuid
from functools import lru_cache
from pathlib import Path
from typing import List
from typing import Tuple

import jwt
from faker import Faker
from random_word import RandomWords

from iocontrol import logging
from iocontrol import strings
from iocontrol.api.auth.errors import UnauthorizedException
from iocontrol.api.auth.providers.base import SecurityProvider
from iocontrol.api.auth.users import User
from iocontrol.config import config
from iocontrol.config.deploy import DeployLevel
from iocontrol.errors import ConfigurationException


@lru_cache()
def debug_tags() -> Tuple[str, ...]:
    """Get logging tags."""
    return "api", "auth", "mocks"


@lru_cache(maxsize=1)
def default_user() -> str:
    """Get the name of the default user profile."""
    return "user"


@lru_cache()
def jwt_algorithm() -> str:
    """Get the JWT encoding algorithm."""
    return "HS256"


@lru_cache(maxsize=1)
def user_template() -> Path:
    """Get the path to the user template."""
    return Path(__file__).parent / "mock" / "user.json"


@lru_cache(maxsize=1)
def user() -> User:
    """Get the mock user."""
    # Let's see how the mocks are configured.
    config_ = config()
    # Where's the root?
    root = (
        (config_.api.auth.mock.root or config_.home / "mock")
        .expanduser()
        .resolve()
    )
    # Where do we store mock users?
    users = root / "auth" / "users"
    # Make sure the directory exists.
    users.mkdir(parents=True, exist_ok=True)
    user_ = (
        users / (config_.api.auth.mock.user or default_user())
    ).with_suffix(".json")
    # If the configuration doesn't specify a user, and our default doesn't
    # exist...
    if not config_.api.auth.mock.user and not user_.exists():
        # Let's get ready to make up some stuff.
        fake = Faker()
        words = RandomWords()
        # Get the template file and populate it with some random values.
        template = strings.render(
            user_template().read_text(),
            sub=str(uuid.uuid4()),
            tenant_id="-".join(
                word.lower()
                for word in [words.get_random_word() for _ in range(0, 3)]
            ),
            name=fake.name(),
            email=fake.email(),
        )
        # Convert the template to an object...
        user_json = json.loads(template)
        # ...so that we can generate a JWT access token.
        access_token = jwt.encode(
            user_json, strings.random(length=16), algorithm=jwt_algorithm()
        )
        # Now put the access token into the object...
        user_json["access_token"] = access_token
        # and write the file back out.  This should be everything we need
        # to create a ``User`` object.
        user_.write_text(json.dumps(user_json, indent=2))
    # Parse the user profile.
    return User.parse_file(str(user_))


class MockSecurityProvider(SecurityProvider):
    """A mock security provider for development and testing."""

    @classmethod
    @lru_cache(maxsize=1)
    def init(cls):
        """Initialize the mock environment."""
        deploy_level = DeployLevel[config().deploy.level.upper()]
        if deploy_level <= DeployLevel.TESTING:
            logging.info(
                "The API is using the mock security module.  (This is fine "
                "for development and testing deployments.)",
                deploy_level=deploy_level,
                tags=debug_tags(),
            )
        if deploy_level == DeployLevel.STAGING:
            logging.warn(
                "The API is using the mock security module in a staging "
                "deployment!",
                deploy_level=deploy_level,
                tags=debug_tags(),
            )
        if deploy_level >= DeployLevel.PRODUCTION:
            logging.error(
                "Detected an attempt to use the mock security module in a "
                "production (or higher) deployment!",
                deploy_level=deploy_level,
                tags=debug_tags(),
            )
            raise ConfigurationException(
                "Cannot use the mock security module in a production "
                "environment."
            )

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
        user_ = user()

        def check_perm():
            """Check user entitlements against the requirements."""
            if not auto_error:
                return user_
            if super_user and not user.super_user:
                raise UnauthorizedException("You are not a super user.")
            forbidden = False
            for set_, required, assigned in [
                (
                    "permissions",
                    set(permissions or ()),
                    set(user_.permissions or ()),
                ),
                ("roles", set(roles or ()), set(user_.roles or ())),
            ]:
                # If the elements in the required set don't match the assigned
                # set, the access is forbidden.
                if required & assigned != required:
                    forbidden = True
                logging.debug(
                    f'Mock user "{user_.name}" failed authorization due to '
                    f"insufficient {set_}.",
                    required=tuple(required),
                    assigned=tuple(assigned),
                )
            # If we detected insufficient roles or permissions.
            if forbidden:
                raise UnauthorizedException()
            # All good!
            return user_

        return check_perm
