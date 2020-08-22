"""Allow calling part-map with 'python -m part_map' for debugging."""
import sys

from part_map.part_map import PartMap
from PySide2 import QtWidgets

APP = QtWidgets.QApplication([])
GUI = PartMap()
GUI.show()
sys.exit(APP.exec_())
