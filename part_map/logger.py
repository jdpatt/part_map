"""The logging and debug functionality for prototype."""
import logging
from logging import Logger


def setup_logger(root_name: str, log_file_path="") -> Logger:
    """Create a console and file handler with the level set to Debug."""
    log = logging.getLogger(root_name)

    # Setup a Console Logger
    console_handler = logging.StreamHandler()
    ch_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(ch_format)
    console_handler.setLevel(logging.ERROR)
    log.addHandler(console_handler)

    # Setup a File Logger
    file_handler = logging.FileHandler(log_file_path, mode="w", delay=True)
    fh_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(fh_format)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

    log.info(f"Log file created at: {log_file_path}")
    return log
