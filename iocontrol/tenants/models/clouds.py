import enum
from functools import lru_cache
from typing import Tuple

from psycopg2 import OperationalError
from pydantic import ConfigDict
from pydantic import Field

from iocontrol import logging
from iocontrol.config import config
from iocontrol.sqa.engine import session_local
from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel
from iocontrol.tenants.orm import Cloud


@lru_cache(maxsize=1)
def tags() -> Tuple[str, ...]:
    """Logging tags."""
    return "sqa", "tenants", "clouds"


@lru_cache(maxsize=1)
def cloud_urns() -> Tuple[str]:
    """Get the list of cloud URNs from the database."""
    try:
        with session_local()() as db:
            query = db.query(Cloud)
            query.order_by(Cloud.urn)
            return tuple(str(c.urn) for c in query.all())
    except OperationalError as oe:
        logging.exception(
            "Failed to fetch cloud URNs.",
            reason=str(oe),
            sqa=config().db.as_sqa(hide_secrets=True),
        )
        raise


# Cloud URNs
CloudUrn = enum.Enum(
    "CloudUrns", {c: f"urn:io:clouds:{c}" for c in cloud_urns()}
)


class ReadCloud(BaseModel):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="identifies the cloud")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )


class CloudsPage(Page):
    """A page of ``Cloud`` models."""

    clouds: Tuple[ReadCloud, ...] = Field(
        default_factory=tuple, description="the clouds"
    )
