from abc import ABC
from abc import abstractmethod

from iocontrol.tenants.models.plans import Plan


class Planner(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> Plan:
        """Create a plan."""
