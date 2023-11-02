from pydantic import Field

from iocontrol.tenants.models.tenants import CreateTenant
from iocontrol.tenants.provisioning.base import ProvisioningStructures
from iocontrol.tenants.provisioning.base import ProvisioningTask


class TenantProvisioningTask(ProvisioningTask):
    """A description of a tenant provisioning event."""

    structure: ProvisioningStructures = Field(
        default=ProvisioningStructures.tenant,
        description="the provisioning category",
    )
    detail: CreateTenant = Field(description="describes the tenant to create")
