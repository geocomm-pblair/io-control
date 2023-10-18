from functools import lru_cache
from importlib.metadata import metadata
from pathlib import Path
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Tuple

import semantic_version
from pydantic import BaseModel
from pydantic import Field


def _metadata() -> Mapping[str, Any]:
    """Get metadata for the current package."""
    package = __name__.split(".")[0]
    return metadata(package)


class Version(BaseModel):
    """Describes the library version."""

    major: int = Field(description="the major version")
    minor: int = Field(description="the minor version")
    patch: int = Field(description="the patch version")
    prerelease: Optional[Tuple[str, ...]] = Field(
        default=None, description="pre-release information"
    )
    build: Optional[Tuple[str, ...]] = Field(
        default=None, description="build information"
    )

    class Config:
        """Class configuration options."""

        frozen = True
        populate_by_name = True

    @property
    def version(self) -> str:
        """Get the current version."""
        return str(self)

    @property
    def release(self) -> str:
        return f"{self.major}.{self.minor}"

    def __str__(self) -> str:
        """Get a string."""
        return str(semantic_version.Version(**self.dict()))

    @classmethod
    @lru_cache(maxsize=1)
    def this(cls) -> "Version":
        version = _metadata().get("version")
        semver = semantic_version.Version(version)
        return Version(
            major=semver.major,
            minor=semver.minor,
            patch=semver.patch,
            prerelease=semver.prerelease or None,
            build=semver.build or None,
        )


class PackageMeta(BaseModel):
    """Package metadata."""

    name: str = Field(description="the package name")

    version: Version = Field(description="the package version")
    author: Optional[str] = Field(
        default=None, description="the package author"
    )
    author_email: Optional[str] = Field(
        default=None, description="the author's email"
    )
    path: Path = Field(description="the location of the package")

    def __str__(self):
        """Get a string."""
        return f"{self.name} {self.version}"

    class Config:
        """Class configuration options."""

        frozen = True
        populate_by_name = True


@lru_cache(maxsize=1)
def this() -> PackageMeta:
    """Get the metadata for this library."""
    metadata_ = _metadata()
    return PackageMeta(
        name=metadata_.get("name"),
        version=Version.this(),
        author=metadata_.get("author"),
        author_email=metadata_.get("author_email"),
        path=Path(__file__).parent,
    )
