"""View for the pin."""
from PySide2 import QtCore, QtGui, QtWidgets

from part_map.pins.widget import PinWidget


class Pin(QtCore.QObject, QtWidgets.QGraphicsItem):
    """The graphical view of a square pin."""

    clicked = QtCore.Signal(object)

    def __init__(self, pin, rect, show_label=True, view=None, parent=None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsItem.__init__(self, parent)
        self.setFlags(self.ItemIsSelectable)
        self._widget = None

        self.view = view
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
        del option, widget  # Unused
        painter.save()
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 6))
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2))
        painter.setBrush(QtGui.QColor(self.pin["color"]))
        if self.view.settings["circles"]:
            painter.drawEllipse(
                self.rect.adjusted(
                    0, 0, -self.view.settings["margin"], -self.view.settings["margin"]
                )
            )
        else:
            painter.drawRect(self.rect)

        painter.setFont(QtGui.QFont("Arial", self.view.font_size))
        if self.view.settings["labels"]:
            if len(self.pin["name"]) > 7:
                name = self.pin["name"][:7]
            else:
                name = self.pin["name"]
            painter.drawText(self.rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter, name)
        painter.restore()
