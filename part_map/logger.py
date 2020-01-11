"""The logging and debug functionality for prototype."""
import logging
from logging import Logger, LogRecord

from PySide2.QtCore import QObject, Signal


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


class LogQObject(QObject):
    """Create a dummy object to get around the PySide multiple inheritance problem."""

    new_record = Signal(str, str)


class ThreadLogHandler(logging.Handler):
    """Create a custom logging handler that appends each record to the TextEdit Widget."""

    def __init__(self) -> None:
        super().__init__()
        self.log = LogQObject()
        self.new_record = self.log.new_record
        self.setFormatter(logging.Formatter("%(message)s"))
        self.setLevel(logging.DEBUG)

    def emit(self, record: LogRecord) -> None:
        """Append the record to the Widget."""
        msg = self.format(record)
        level = record.levelname
        self.new_record.emit(level, msg)
