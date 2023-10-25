from ipaddress import IPv4Network
from typing import Any
from typing import List
from typing import Tuple

from geoalchemy2 import Geometry
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
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


class Model(iocontrol.pydantic.BaseModel):
    """Pydantic model base class for tenant models."""

    model_config = ConfigDict(from_attributes=True)


class CloudOrm(Orm):
    __tablename__ = "clouds"

    id: Mapped[str] = mapped_column(primary_key=True)
    regions: Mapped[List["RegionOrm"]] = relationship(back_populates="cloud")


class ReadCloudModel(Model):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="identifies the cloud")
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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    cloud_id: Mapped[str] = mapped_column(ForeignKey("clouds.id"))
    cloud: Mapped[CloudOrm] = relationship(back_populates="regions")
    cells: Mapped[List["CellOrm"]] = relationship(back_populates="region")

    # Region names must be unique within a cloud.
    UniqueConstraint("cloud_id", "name", name="unq__regions")


class ReadRegionModel(Model):
    model_config = ConfigDict(frozen=True)

    id: int = Field(description="uniquely identifies the region")
    name: str = Field(description="the name of the region")
    cloud: ReadCloudModel = Field(
        description="the cloud that hosts the region"
    )
    # cells: Optional[Tuple["ReadCellModel", ...]] = Field(
    #     default=None,
    #     description="These are the cells presently hosted in this region.",
    # )


class RegionModelsPage(Page):
    """A page of ``Region`` models."""

    regions: Tuple[ReadRegionModel, ...] = Field(
        default_factory=tuple, description="the regions"
    )


class CellIpV4NetworkOrm(Orm):
    __tablename__ = "cell_ipv4networks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public: Mapped[bool] = mapped_column()
    network = Column(types.IPv4Network)
    cell_id: Mapped[str] = mapped_column(ForeignKey("cells.id"))
    cell: Mapped[CloudOrm] = relationship(back_populates="ipv4networks")
    doc = Column(types.JSONB)


class ReadIpV4BlockModel(Model):
    id: int = Field(description="uniquely identifies the block")
    public: bool = Field(description="indicates a public address")
    network: IPv4Network = Field(description="the network block")

    @field_validator("network")
    def validate_network(cls, v: Any) -> Any:
        """Validate network."""
        return IPv4Network(str(v)) if v else v


class CellOrm(Orm):
    __tablename__ = "cells"

    id: Mapped[str] = mapped_column(primary_key=True)
    max_tenants: Mapped[int] = mapped_column(default=40)
    region_id: Mapped[str] = mapped_column(ForeignKey("regions.id"))
    region: Mapped[RegionOrm] = relationship(back_populates="cells")
    tenants: Mapped[List["TenantOrm"]] = relationship(back_populates="cell")
    ipv4networks: Mapped[List["CellIpV4NetworkOrm"]] = relationship(
        back_populates="cell"
    )
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))


class ReadCellModel(Model):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="identifies the cell")
    region: ReadRegionModel = Field(
        description="the region in which the cell resides"
    )


class CellModelsPage(Page):
    """A page of ``Cell`` models."""

    cells: Tuple[ReadCellModel, ...] = Field(
        default_factory=tuple, description="the cells"
    )


class TenantOrm(Orm):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(primary_key=True)
    cell_id: Mapped[str] = mapped_column(
        ForeignKey("cells.id"), primary_key=True
    )
    cell: Mapped[CellOrm] = relationship(back_populates="tenants")
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=4326)))


class ReadTenantModel(Model):
    model_config = ConfigDict(frozen=True)

    id: str = Field(description="identifies the cell")
    cell: ReadCellModel = Field(
        description="the cell in which the tenant resides"
    )


class TenantModelsPage(Page):
    """A page of ``Tenant`` models."""

    tenants: Tuple[ReadTenantModel, ...] = Field(
        default_factory=tuple, description="the cells"
    )
