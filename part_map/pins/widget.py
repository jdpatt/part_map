"""Widget to allow the user to edit the color and names of pins."""
from PySide2 import QtGui, QtWidgets


class PinWidget(QtWidgets.QWidget):
    """The widget for all pins."""

    def __init__(self, pin_item, parent=None):
        super().__init__(parent)
        self.pin_item = pin_item

        self.color = QtGui.QColor(self.pin_item.pin["color"])
        self.color_button = QtWidgets.QPushButton(self.pin_item.pin["color"])

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setText(self.pin_item.pin["name"])

        layout = QtWidgets.QFormLayout()
        layout.addRow("Name", self.name_edit)
        layout.addRow("Color", self.color_button)
        self.setLayout(layout)

        # Connect Signal/Slots
        self.color_button.clicked.connect(self.change_color)
        self.name_edit.editingFinished.connect(self.change_name)

    def change_color(self):
        """Update the color."""
        color_picker = QtWidgets.QColorDialog(self.color)
        self.color = color_picker.getColor()
        self.color_button.setText(self.color.name())
        self.pin_item.pin["color"] = self.color.name()
        self.pin_item.update()

    def change_name(self):
        """Update the Name"""
        self.pin_item.pin["name"] = self.name_edit.text()
        self.pin_item.update()
