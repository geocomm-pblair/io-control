from pydantic import conint

from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class Result(BaseModel):
    """A structured result object."""

    message: str = Field(description="the result message")
    code: conint(ge=100, le=599) = Field(
        default=200, description="the associated HTTP status_code"
    )


class OK(Result):
    """A positive acknowledgement."""

    message: str = Field(default="OK.", description="the result message")
