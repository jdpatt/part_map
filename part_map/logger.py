"""The logging and debug functionality for prototype."""
import logging
from logging import Logger


def setup_logger(root_name: str) -> Logger:
    """Create a console logger."""
    log = logging.getLogger(root_name)

    # Setup a Console Logger
    console_handler = logging.StreamHandler()
    ch_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(ch_format)
    console_handler.setLevel(logging.INFO)
    log.addHandler(console_handler)

    log.setLevel(logging.DEBUG)

    return log
