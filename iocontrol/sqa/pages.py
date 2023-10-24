from typing import Tuple

from pydantic import ConfigDict
from pydantic import conint

from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class Page(BaseModel):
    """A page of results."""

    model_config = ConfigDict(frozen=True)

    offset: conint(ge=0) = Field(description="the offset")
    limit: conint(ge=0) = Field(description="the limit")
    total: conint(ge=0) = Field(description="the total number of objects")


class NamesPage(Page):
    """A page that contains a list of strings."""

    names: Tuple[str, ...] = Field(
        default_factory=tuple, description="the values"
    )
