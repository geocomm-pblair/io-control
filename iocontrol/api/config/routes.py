from iocontrol.api import responses
from iocontrol.config import Config
from iocontrol.config import config
from iocontrol.config import ui
from iocontrol.fastapi import APIRouter

router = APIRouter(
    tags=["configuration"],
    dependencies=[],
)


@router.get(
    "",
    name="get-config",
    response_model=Config,
    response_model_by_alias=True,
    responses=responses.errors,
)
async def config_() -> Config:
    """Get the current configuration."""
    return config()


@router.get(
    "/ui",
    name="get-ui-config",
    response_model=ui.UiConfig,
    response_model_by_alias=True,
    responses=responses.errors,
)
async def ui_config_() -> ui.UiConfig:
    """Get the current user interface (UI) configuration."""
    return ui.config()
