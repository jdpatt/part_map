"""Allow calling part-map with 'python -m part_map' for debugging."""
import sys

from PySide2 import QtWidgets

from part_map.part_map import PartMap

APP = QtWidgets.QApplication([])
GUI = PartMap()
GUI.show()
sys.exit(APP.exec_())
