from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from geoalchemy2 import Geometry
from pydantic import ConfigDict
from pydantic import Field
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import deferred
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

import iocontrol.pydantic
import iocontrol.sqa.models
from iocontrol.sqa import types
from iocontrol.sqa.pages import Page


class Orm(iocontrol.sqa.models.Base):
    """ORM base class for tenant models."""

    __abstract__ = True

    @declared_attr
    def doc(self):
        """An entity document."""
        return deferred(Column(types.JSONB))


class Model(iocontrol.pydantic.BaseModel):
    """Pydantic model base class for tenant models."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    doc: Optional[Dict[str, Any]] = Field(
        default=None, description="an entity document"
    )


class CloudOrm(Orm):
    __tablename__ = "clouds"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    regions: Mapped[List["RegionOrm"]] = relationship(back_populates="cloud")


class ReadCloudModel(Model):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="identifies the cloud")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    # regions: Optional[Tuple["ReadRegionModel", ...]] = Field(
    #     default=None,
    #     description="These are the available regions within the cloud.",
    # )


class CloudModelsPage(Page):
    """A page of ``Cloud`` models."""

    clouds: Tuple[ReadCloudModel, ...] = Field(
        default_factory=tuple, description="the clouds"
    )


class RegionOrm(Orm):
    __tablename__ = "regions"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column()
    cloud_id: Mapped[str] = mapped_column(ForeignKey("clouds.urn"))
    cloud: Mapped[CloudOrm] = relationship(back_populates="regions")
    cells: Mapped[List["CellOrm"]] = relationship(back_populates="region")

    # Region names must be unique within a cloud.
    UniqueConstraint("cloud_id", "display_name", name="unq__regions")


class IpV4NetworkOrm(Orm):
    __abstract__ = True

    urn: Mapped[str] = mapped_column(primary_key=True)
    # public: Mapped[bool] = mapped_column()
    network = Column(types.IPv4Network, unique=True)


class CellIpV4NetworkOrm(IpV4NetworkOrm):
    __tablename__ = "cell_ipv4networks"

    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped["CellOrm"] = relationship(back_populates="ipv4networks")


class TenantIpV4NetworkOrm(IpV4NetworkOrm):
    __tablename__ = "tenant_ipv4networks"

    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped["CellOrm"] = deferred(relationship())
    tenant_urn: Mapped[str] = mapped_column(ForeignKey("tenants.urn"))
    tenant: Mapped["TenantOrm"] = relationship(back_populates="ipv4networks")

    UniqueConstraint(
        "cell_urn", "tenant_urn", "network", name="unq__tenant_ipv4networks"
    )


class CellOrm(Orm):
    __tablename__ = "cells"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    max_tenants: Mapped[int] = mapped_column(default=500, server_default="500")
    region_id: Mapped[str] = mapped_column(ForeignKey("regions.urn"))
    region: Mapped[RegionOrm] = relationship(back_populates="cells")
    tenants: Mapped[List["TenantOrm"]] = relationship(back_populates="cell")
    ipv4networks: Mapped[List["CellIpV4NetworkOrm"]] = relationship(
        back_populates="cell"
    )
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))


class TenantOrm(Orm):
    __tablename__ = "tenants"

    urn: Mapped[str] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(unique=True)
    cell_urn: Mapped[str] = mapped_column(ForeignKey("cells.urn"))
    cell: Mapped[CellOrm] = relationship(back_populates="tenants")
    ipv4networks: Mapped[List["TenantIpV4NetworkOrm"]] = relationship(
        back_populates="tenant"
    )
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))
