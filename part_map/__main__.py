"""Allow calling part-map with 'python -m part_map' for debugging."""
import sys

from part_map.part_map import PartMap
from PySide2 import QtWidgets

app = QtWidgets.QApplication([])
gui = PartMap()
gui.show()
sys.exit(app.exec_())
