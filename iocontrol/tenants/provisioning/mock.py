from sqlalchemy.orm import Session

from iocontrol import strings
from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask


class MockProvisioner(Provisioner):
    def run(self, task: ProvisioningTask, db: Session) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param task: the plan
        :param db: a database session
        :returns: an update provisioning task
        """
        task_ = type(task)(
            **{**dict(id=task.id_ or strings.random(12)), **task.model_dump()}
        )
        return task_

    def status(self, id_: str, db: Session) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param id_: the task identifier
        :param db: a database session
        :returns: the provisioning task definition
        """
