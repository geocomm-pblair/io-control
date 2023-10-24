from abc import ABC
from abc import abstractmethod
from typing import List


class SecurityProvider(ABC):
    """Base class for security provider implementations."""

    @classmethod
    @abstractmethod
    def init(cls):
        """Initialize the provider."""

    @classmethod
    @abstractmethod
    def security(
        cls,
        permissions: List[str] = None,
        auto_error: bool = True,
        roles: List[str] = None,
        super_user: bool = None,
    ):
        """
        Configure endpoint security.

        :param permissions: required permissions
        :param auto_error: raise errors if security fails
        :param roles: required roles
        :param super_user: requires super-user permissions
        """
