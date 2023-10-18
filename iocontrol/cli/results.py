from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class CliResponse(BaseModel):
    """A simple CLI response."""

    message: str = Field(description="the response message")


OK = CliResponse(message="OK")
