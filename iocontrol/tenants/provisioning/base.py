from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic import Field

from iocontrol.pydantic import BaseModel
from iocontrol.tenants.models.plans import Plan


class ProvisioningState(Enum):
    """
    Provisioning task status.

    The possible states are based on the defined Apache Airflow DAG run states.

    .. seealso::

        https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html
    """

    success = "success"
    failed = "failed"
    skipped = "skipped"


class ProvisioningTask(BaseModel):
    """A provisioning task."""

    id_: str = Field(
        alias="id", description="identifies the provisioning task"
    )
    state: ProvisioningState = Field(
        description="the state of the provisioning task"
    )
    ref: Optional[AnyHttpUrl] = Field(
        default=None, description="a reference URL"
    )


class Provisioner(ABC):
    @abstractmethod
    def run(self, plan: Plan) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param plan: the plan
        :returns: a provisioning task definition
        """

    @abstractmethod
    def status(self, id_: str) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param id_: the task identifier
        :returns: the provisioning task definition
        """
