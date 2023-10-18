from functools import lru_cache
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import pendulum
from dotenv import load_dotenv
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
from pydantic import ConfigDict

from iocontrol import meta
from iocontrol.pydantic import Field
from iocontrol.pydantic import BaseModel


class EnvInit(BaseModel):
    """Describes environment initialization."""

    model_config = ConfigDict(frozen=True)

    env_file: Optional[Path] = Field(
        default=None,
        description=(
            "the path to the .env file used to configure environment "
            "variables"
        ),
    )
    search_path: Tuple[Path, ...] = Field(
        default_factory=tuple, description="the environment file search path"
    )


@lru_cache(maxsize=1)
def _templates() -> Environment:
    """Get the current template environment."""
    return Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=True,
    )


@lru_cache(maxsize=1)
def template() -> Template:
    """Get the current environment template."""
    return _templates().get_template("{{this}}.env")


@lru_cache(maxsize=1)
def search_paths() -> Tuple[Path]:
    """Get an ordered list of candidate configuration paths."""
    file = f"{meta.this().name}.env"
    dir_ = Path.cwd()
    paths: List[Path] = []
    while True:
        paths.append(dir_ / file)
        if dir_.parent == dir_:
            break
        dir_ = dir_.parent
    return tuple(paths)


@lru_cache(maxsize=1)
def env_file() -> Optional[Path]:
    """Get the path to the current environment file."""
    # Find the most relevant path.
    for p in search_paths():
        if p.is_file():
            return p
    return None


def make(path: Path = None, exists_ok: bool = True) -> Path:
    """
    Create a default `.env` file.

    :param path: the path to the file
    :param exists_ok: do not raise an error if the file exists
    """
    f = (
        ((path or Path().cwd()) / f"{meta.this().name}.env")
        .expanduser()
        .resolve()
    )
    if f.exists():
        if not exists_ok:
            raise FileExistsError(f"{path} exists.")
        return f
    template_ = template().render(
        this=meta.this().name,
        now=pendulum.now().to_cookie_string(),
    )
    f.write_text(template_)
    return f


@lru_cache()
def init():
    """Initialize the configuration environment."""
    # Look for a `.env` file.
    env_file_ = env_file()
    # If we found one, load it.
    if env_file_:
        env_file_ = env_file_.expanduser().resolve()
        # structlog.getLogger().info(
        #     f"Loading environment variables from {env_file_}.",
        #     env_file=str(env_file_),
        #     search_path=tuple(str(p) for p in env_paths()),
        # )
        load_dotenv(env_file())
        return EnvInit(env_file=env_file_, search_path=search_paths())
    else:
        return EnvInit(env_file=None, search_path=search_paths())
        # structlog.getLogger().info(
        #     "No environment files were found.",
        #     env_file=None,
        #     search_path=tuple(str(p) for p in env_paths()),
        # )


# Before we leave the module, let's initialize the environment.
init()
