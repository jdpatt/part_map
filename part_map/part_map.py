"""Main Window of Part Map"""
from pathlib import Path

from PySide2 import QtWidgets

from .gui import Ui_MainWindow
from .logger import setup_logger
from .object import PartObject


class PartMap(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main Part Map Window."""

    def __init__(self, filename, kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.log = setup_logger("partmap")
        filename = Path(filename)
        self.log.info(f"Filename: {filename}")
        self.setWindowTitle(filename.stem)
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

        self.view.part = self.part
        self.view.settings = view_settings

        self.connect_actions()

        # Fill the graphic view
        self.view.generate_render()
        self.view.redraw()

    def connect_actions(self):
        """Connect any actions to slots."""
        # pylint: disable=W0201
        self.actionSave_as_Image.triggered.connect(self.view.save)
        self.actionSave_as_Json.triggered.connect(self.part.dump_json)
        self.actionRotate.triggered.connect(self.view.rotate_drawing)
        self.actionToggle_Shape.triggered.connect(self.view.toggle_style)
