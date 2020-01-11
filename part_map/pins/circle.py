"""View for the pin."""
from part_map.pins.widget import PinWidget
from PySide2 import QtCore, QtGui, QtWidgets


class RoundPin(QtCore.QObject, QtWidgets.QGraphicsEllipseItem):
    """The graphical view of a round pin."""

    clicked = QtCore.Signal(object)

    def __init__(self, pin, rect, show_label=True, parent=None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsEllipseItem.__init__(self, rect, parent)
        self.setFlags(self.ItemIsSelectable)
        self._widget = None

        self.rect = rect

        self.pin = pin
        self.show_label = show_label

    @property
    def widget(self):
        """If a property widget has not been created or has been deleted, create one."""
        if not self._widget:
            self._widget = PinWidget(self)
        return self._widget

    def boundingRect(self):
        """Return the outer bounds of the item as a rectangle.

        All painting must be restricted inside an item's bounding rect. QGraphicsView uses this to
        determine whether the item requires redrawing.
        """
        return self.rect

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
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        painter.drawText(
            self.rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter, self.pin["name"]
        )
        super().paint(painter, option, widget)
