from pathlib import Path

from PySide2 import QtCore, QtGui, QtWidgets

from .gui import Ui_MainWindow
from .logger import setup_logger
from .object import PartObject
from .view import PartViewer


class PartMap(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main Part Map Window."""

    def __init__(self, filename, kwargs):
        QtWidgets.QMainWindow.__init__(self)
        self.log = setup_logger("partmap", Path(__file__).parent.joinpath("partmap.log"))
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
        self.graphicsView.part = self.part
        self.graphicsView.settings = view_settings
        self.connect_actions()
        self.graphicsView.generate_render()

    def connect_actions(self):
        """Connect any actions to slots."""
        # pylint: disable=W0201
        self.actionSave_as_Image.triggered.connect(self.graphicsView.save)
        self.actionSave_as_Json.triggered.connect(self.part.dump_json)
        self.actionRotate.triggered.connect(self.graphicsView.rotate_drawing)
        self.actionToggle_Shape.triggered.connect(self.graphicsView.toggle_style)
