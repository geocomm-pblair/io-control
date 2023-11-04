from datetime import datetime
from typing import List

from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import deferred
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

import iocontrol.sqa.models
from iocontrol.sqa import types


class Orm(iocontrol.sqa.models.Base):
    """ORM base class for tenant models."""

    __abstract__ = True

    @declared_attr
    def doc(self):
        """An entity document."""
        return deferred(Column(types.JSONB))


class Cloud(Orm):
    __tablename__ = "clouds"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    regions: Mapped[List["Region"]] = relationship(back_populates="cloud")


class Region(Orm):
    __tablename__ = "regions"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column()
    cloud_urn: Mapped[str] = mapped_column(ForeignKey("clouds.urn"))
    cloud: Mapped[Cloud] = relationship(back_populates="regions")
    cells: Mapped[List["Cell"]] = relationship(back_populates="region")

    # Region names must be unique within a cloud.
    UniqueConstraint("cloud_id", "display_name", name="unq__regions")


class IpV4Network(Orm):
    __abstract__ = True

    urn: Mapped[str] = mapped_column(primary_key=True)
    network = Column(types.IPv4Network, unique=True)


class CellIpV4Network(IpV4Network):
    __tablename__ = "cell_ipv4networks"

    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped["Cell"] = relationship(back_populates="ipv4networks")


class TenantIpV4Network(IpV4Network):
    __tablename__ = "tenant_ipv4networks"

    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped["Cell"] = deferred(relationship())
    tenant_urn: Mapped[str] = mapped_column(ForeignKey("tenants.urn"))
    tenant: Mapped["Tenant"] = relationship(back_populates="ipv4networks")

    UniqueConstraint(
        "cell_urn", "tenant_urn", "network", name="unq__tenant_ipv4networks"
    )


class Cell(Orm):
    __tablename__ = "cells"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    max_tenants: Mapped[int] = mapped_column(default=500, server_default="500")
    region_urn: Mapped[str] = mapped_column(ForeignKey("regions.urn"))
    region: Mapped[Region] = relationship(back_populates="cells")
    tenants: Mapped[List["Tenant"]] = relationship(back_populates="cell")
    ipv4networks: Mapped[List["CellIpV4Network"]] = relationship(
        back_populates="cell"
    )
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))


class Tenant(Orm):
    __tablename__ = "tenants"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped[Cell] = relationship(back_populates="tenants")
    ipv4networks: Mapped[List["TenantIpV4Network"]] = relationship(
        back_populates="tenant"
    )
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))


class ProvisioningTask(Orm):
    __tablename__ = "provisioning_tasks"

    uid: Mapped[str] = mapped_column(primary_key=True)
    provisioner: Mapped[str] = mapped_column(nullable=False, index=True)
    created: Mapped[datetime] = mapped_column(nullable=False, index=True)
