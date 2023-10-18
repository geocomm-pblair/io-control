from iocontrol import meta
from iocontrol.api import responses
from iocontrol.fastapi import APIRouter

router = APIRouter(
    tags=["system"],
    dependencies=[],
)


@router.get(
    "/meta",
    name="get-meta",
    response_model=meta.PackageMeta,
    response_model_by_alias=True,
    response_model_exclude={"path"},
    responses=responses.errors,
)
async def meta_() -> meta.PackageMeta:
    """Get the current configuration."""
    return meta.this()


@router.get(
    "/health",
    name="get-health",
    response_model=responses.OK,
    response_model_by_alias=True,
    response_model_exclude={"path"},
    responses=responses.errors,
)
async def health() -> responses.OK:
    """Get the current configuration."""
    return responses.OK(message="I am alive.")
