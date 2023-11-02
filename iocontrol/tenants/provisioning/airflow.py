from sqlalchemy.orm import Session

from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask


class AirflowProvisioner(Provisioner):
    async def run(
        self, task: ProvisioningTask, db: Session
    ) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param task: the plan
        :param db: a database session
        :returns: an update provisioning task
        """

    async def task(self, uid: str, db: Session) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param uid: the task identifier
        :param db: a database session
        :returns: the provisioning task definition
        """
