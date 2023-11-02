from abc import ABC
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

from pydantic import AnyHttpUrl
from pydantic import Field
from requests import Session

from iocontrol.pydantic import BaseModel


class ProvisioningState(Enum):
    """
    Provisioning task status.

    The possible states are based on the defined Apache Airflow DAG run states.

    .. seealso::

        https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html
    """

    created = "created"
    queued = "queued"
    running = "running"
    success = "success"
    failed = "failed"


class ProvisioningStructures(Enum):
    """Provisioning types."""

    tenant = "tenant"
    cell = "cell"


class ProvisioningRef(BaseModel):
    """A provisioning task URL reference."""

    category: str = Field(description="the reference type")
    url: AnyHttpUrl = Field(default=None, description="a reference URL")


class ProvisioningTask(BaseModel):
    """A provisioning task."""

    uid: Optional[str] = Field(
        default=None,
        description="identifies the provisioning task",
    )
    structure: ProvisioningStructures = Field(
        description="the provisioning type"
    )
    created: datetime = Field(
        default_factory=datetime.utcnow,
        description="the task creation timestamp",
    )
    state: ProvisioningState = Field(
        default=ProvisioningState.created,
        description="the state of the provisioning task",
    )
    refs: Tuple[ProvisioningRef, ...] = Field(
        default_factory=tuple, description="a reference URL"
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None, description="provisioner metadata"
    )
    detail: Dict[str, Any] = Field(
        default_factory=dict, description="provisioning task details"
    )
    result: Optional[Dict[str, Any]] = Field(
        default=None, description="the provisioning result"
    )


class Provisioner(ABC):
    """A provisioning service."""

    @classmethod
    def type(cls) -> str:
        """Get the identifier for the provisioner type."""
        return f"{cls.__module__}.{cls.__name__}"

    @abstractmethod
    async def run(
        self, task: ProvisioningTask, db: Session
    ) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param task: the plan
        :param db: a database session
        :returns: an update provisioning task
        """

    @abstractmethod
    async def task(self, uid: str, db: Session) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param uid: the task identifier
        :param db: a database session
        :returns: the provisioning task definition
        """
