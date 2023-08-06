import logging

import click
from rich.logging import RichHandler
from rich.traceback import install


def init(verbose=False):
    """
    Init logging.
        Args:
            verbose (bool):
                Verbose level (DEBUG) or not (INFO).
        Raises:
            AnyError: If anything bad happens.
    """

    install(suppress=[click])

    logging.basicConfig(
        level="DEBUG" if verbose else "INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
                enable_link_path=False,
            )
        ],
    )

    excluded_loggers = (
        "numba",
        "matplotlib",
        "executor",
    )

    for log_name in excluded_loggers:
        other_log = logging.getLogger(log_name)
        other_log.setLevel(logging.WARNING)
