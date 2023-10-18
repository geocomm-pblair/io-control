from typing import List

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from sqlalchemy.orm import mapped_column, Mapped, relationship

from iocontrol.sqa.models import Base


class TenantOrm(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(primary_key=True)
    terraform_assets: Mapped[List["TerraformAssetOrm"]] = relationship(
        back_populates="tenant"
    )


class TerraformAssetOrm(Base):
    __tablename__ = "terraform_assets"

    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("tenants.id"), primary_key=True
    )
    tenant: Mapped["TenantOrm"] = relationship(
        back_populates="terraform_assets"
    )
    asset: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
