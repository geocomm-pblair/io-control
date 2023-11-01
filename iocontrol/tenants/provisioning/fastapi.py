from functools import lru_cache


@lru_cache(maxsize=1)
def provisioner():
    """Database session dependency."""
    # from .airflow import AirflowProvisioner
    # return AirflowProvisioner()

    from iocontrol.tenants.provisioning.mock import MockProvisioner

    return MockProvisioner()
