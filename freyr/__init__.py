__all__ = [
    "__version__",
    "get_project",
    "get_cache",
    "get_config",
    "get_data",
    "setup_logging",
    "elapsed_timer",
]

import logging
import os
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path
from timeit import default_timer

from rich.logging import RichHandler
from rich.traceback import install

from freyr.console import CONSOLE

__version__ = "0.5.3"


def get_cache() -> Path:
    cache_home = os.getenv("XDG_CACHE_HOME", default=str(Path.home() / ".cache"))
    folder = Path(cache_home).resolve() / "freyr"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_config() -> Path:
    config_home = os.getenv("XDG_CONFIG_HOME", default=str(Path.home() / ".config"))
    folder = Path(config_home).resolve() / "freyr"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_data() -> Path:
    data_home = os.getenv("XDG_DATA_HOME", default=str(Path.home() / ".local" / "share"))
    folder = Path(data_home).resolve() / "freyr"
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_project() -> Path:
    return Path(__file__).parent.parent


def setup_logging(debug: bool = False) -> None:
    install(show_locals=True, max_frames=6, console=CONSOLE)
    log_folder = get_project() / "logs"
    log_folder.mkdir(parents=True, exist_ok=True)

    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        omit_repeated_times=False,
        show_level=True,
        show_time=False,
        show_path=False,
        console=CONSOLE,
    )
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    file_handler = RotatingFileHandler(
        filename=log_folder / "freyr.log", maxBytes=100_000_000, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] {%(name)s} | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        handlers=[console_handler, file_handler],
    )

    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)


@contextmanager
def elapsed_timer() -> float:
    start = default_timer()
    elapser = lambda: default_timer() - start  # noqa: E731
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end - start  # noqa: E731
