"""Main Window of Part Map"""
from pathlib import Path

from PySide2 import QtWidgets

from .gui import Ui_MainWindow
from .logger import ThreadLogHandler, setup_logger
from .object import PartObject


class PartMap(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main Part Map Window."""

    def __init__(self, filename, kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.log = setup_logger("partmap")
        self.setupUi(self)
        self.menubar.setNativeMenuBar(False)

        thread_log = ThreadLogHandler()
        self.log.addHandler(thread_log)
        thread_log.new_record.connect(self.log_message)

        filename = Path(filename)
        self.setWindowTitle(filename.stem)
        self.log.info(f"Filename: {filename}")
        if filename.suffix in [".xlsx", ".xlsm", ".xltm"]:
            self.part = PartObject.from_excel(filename)
        elif filename.suffix in [".json"]:
            self.part = PartObject.from_json(filename)
        elif filename.suffix in [".net", ".txt"]:
            self.part = PartObject.from_telesis(filename, kwargs["refdes"])

        screen_resolution = QtWidgets.QApplication.desktop().screenGeometry()
        view_settings = {
            "width": screen_resolution.width(),
            "height": screen_resolution.height(),
            "title": filename.stem,
            "rotate": kwargs["rotate"],
            "circles": kwargs["circles"],
            "labels": kwargs["no_labels"],
            "factor": 1.0,
            "margin": 5,
        }
        self.log.debug(f"Settings: {view_settings}")
        self.setupUi(self)

        self.view.setup(self.part, view_settings)

        self.connect_actions()

    def connect_actions(self):
        """Connect any actions to slots."""
        # pylint: disable=W0201
        self.actionSave_as_Image.triggered.connect(self.view.save)
        self.actionSave_as_Json.triggered.connect(self.part.dump_json)
        self.actionRotate.triggered.connect(self.view.rotate_drawing)
        self.actionToggle_Shape.triggered.connect(self.view.toggle_style)

    def log_message(self, level, msg) -> None:
        """Log any logger messages via the slot/signal mechanism so that its thread safe."""
        del level  # Unused
        self.statusbar.showMessage(msg, timeout=5000)  # Miliseconds

    def resizeEvent(self, event):
        """Override the resize event to allow the pixmap to rescale."""
        self.view.redraw()
        return super().resizeEvent(event)
