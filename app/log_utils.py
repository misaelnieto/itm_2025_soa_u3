"""Logging configuration for the application using RichHandler from the rich library.

How to use in your module:
```python
    from app.logging import logger

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
```
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

from app.config import settings


def setup_logging(
    level: int = logging.INFO,
) -> None:
    """Set up logging configuration with RichHandler.

    Args:
        level (int): Logging level. Default is logging.INFO.

    """
    logger = logging.getLogger("app")
    console = Console()
    rich_handler = RichHandler(
        show_time=False,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True,
        show_path=False,
        console=console,
    )
    rich_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(rich_handler)

    logger.setLevel(level)
    logger.propagate = False

setup_logging(level=logging.DEBUG if settings.verbose else logging.INFO)
logger = logging.getLogger("app")
