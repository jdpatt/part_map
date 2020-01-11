"""View for the pin."""
from part_map.pins.widget import PinWidget
from PySide2 import QtCore, QtGui, QtWidgets


class SquarePin(QtCore.QObject, QtWidgets.QGraphicsRectItem):
    """The graphical view of a square pin."""

    clicked = QtCore.Signal(object)

    def __init__(self, pin, rect, show_label=True, parent=None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsRectItem.__init__(self, rect, parent)
        self.setFlags(self.ItemIsSelectable)
        self._widget = None

        self.size = rect.width()

        self.pin = pin
        self.show_label = show_label

    @property
    def widget(self):
        """If a property widget has not been created or has been deleted, create one."""
        if not self._widget:
            self._widget = PinWidget(self)
        return self._widget

    def mousePressEvent(self, event):
        """Change the pin color when the user clicks the pin."""
        self.clicked.emit(self.widget)
        self.update()
        super().mousePressEvent(event)

    def paint(self, painter, option, widget):
        """If the pin is selected alter the pen before allowing the base class to draw the rect."""
        self.setBrush(QtGui.QColor(self.pin["color"]))
        if self.isSelected():
            self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 6))
        else:
            self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2))
        super().paint(painter, option, widget)
