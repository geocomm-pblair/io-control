from abc import abstractmethod

from iocontrol.tenants.models.plans import Plan
from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningState
from iocontrol.tenants.provisioning.base import ProvisioningTask


class AirflowProvisioner(Provisioner):
    @abstractmethod
    def run(self, plan: Plan) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param plan: the plan
        :returns: a provisioning task definition
        """
        print("OK... I'm going to run this...")
        print(plan.model_dump_json(indent=2))

    @abstractmethod
    def status(self, id_: str) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param id_: the task identifier
        :returns: the provisioning task definition
        """
        print("Chugga chugga...")
        return ProvisioningTask(id=id_, state=ProvisioningState.success)
