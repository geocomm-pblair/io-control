from abc import ABC
from abc import abstractmethod

from iocontrol.tenants.models.plans import Plan


class Planner(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> Plan:
        """Create a plan."""


# class CellPlanner(Planner, ABC):
#     """A cell planner prepares plans for cell creation."""
#
#
# class TenantPlanner(Planner, ABC):
#     """A tenant planner prepares plans for tenants creation."""
