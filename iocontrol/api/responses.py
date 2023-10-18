from pydantic import ConfigDict

from iocontrol.errors import ErrorMessage
from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field

errors = {
    403: {"model": ErrorMessage},
    500: {"model": ErrorMessage},
}


class Response(BaseModel):
    """A general response message."""

    model_config = ConfigDict(frozen=True)

    status_code: int = Field(default=200, description="the status code")
    message: str = Field(descripton="the message")


class OK(Response):
    """The request was handled successfully."""

    message: str = Field(default="ok", description="the message")
