from iocontrol.tenants.models.plans import Plan
from iocontrol.tenants.planning.base import Planner


class AwsPlanner(Planner):
    def create(self, *args, **kwargs) -> Plan:
        pass
