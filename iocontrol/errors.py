import http
from typing import Any
from typing import Optional
from typing import Tuple

from pydantic import ConfigDict

from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class ErrorMessage(BaseModel):
    """An exception message."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=False)

    status_code: int = Field(default=500, description="the status status_code")
    event: str = Field(description="the exception event message")
    tags: Optional[Tuple[str, ...]] = Field(
        default=None, description="additional tags"
    )
    traceback: Optional[Tuple[str, ...]] = Field(
        default=None,
        description="the traceback",
    )


class AppException(Exception):
    """Base class for exceptions in this library."""

    status_code: int = 500  #: the corresponding HTTP status status_code
    headers: dict[str, Any] = None

    def __init__(
        self,
        event=None,
        *,
        status_code: int = None,
        headers: dict[str, Any] = None,
        tags: Tuple[str, ...] = None
    ):
        """
        Create a new instance.

        :param event: the error detail
        :param status_code: the status status_code
        :param headers: the headers
        :param tags: the _tags
        """
        self.status_code = (
            status_code
            or self.status_code
            or http.HTTPStatus(status_code).phrase
        )
        self.event = event or self.__doc__
        self.headers = headers or self.headers
        self.tags = tags

    def message(self) -> ErrorMessage:
        """Create an exception message object from this exception."""
        return ErrorMessage(
            status_code=self.status_code, event=self.event, tags=self.tags
        )

    @classmethod
    def from_exception(cls, ex: Exception):
        """Convert an exception to an exception message of this type."""
        if isinstance(ex, AppException):
            return ex

        return cls(event=str(ex))


class ConfigurationException(AppException):
    """An error exists in the current configurtion."""


class NotFoundException(AppException):
    """The resource was not found."""

    status_code: int = 404


class ValueException(AppException):
    """Bad request."""

    status_code = 400
