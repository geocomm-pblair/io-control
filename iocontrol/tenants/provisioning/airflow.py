from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask


class AirflowProvisioner(Provisioner):
    def run(self, task: ProvisioningTask) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param task: the plan
        :returns: an update provisioning task
        """

    def status(self, id_: str) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param id_: the task identifier
        :returns: the provisioning task definition
        """
