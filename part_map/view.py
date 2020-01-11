""" Visual pin out of a BGA or connector """
import logging
from pathlib import Path
from typing import List

from part_map.pins import Pin
from PySide2 import QtCore, QtGui, QtWidgets


class PartViewer(QtWidgets.QGraphicsView):
    """ Create a render of the part and load it into a QWidget """

    # pylint: disable=R0902
    def __init__(self, parent=None):
        super(PartViewer, self).__init__(parent)
        self.log = logging.getLogger("partmap.view")

        self.settings = None
        self.part = None

        self.box_size = 50
        self.zoom_level = 0

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtCore.Qt.white)
        self.setScene(self.scene)
        self.scene.setFont(QtGui.QFont("Times", 12))

        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.ScrollHandDrag)
        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

    def setup(self, part, settings):
        """Return the settings dictionary."""
        self.part = part
        self.settings = settings
        if self.settings["rotate"]:
            self.rotate_drawing()
        self.scale_box_size(self.part.columns, self.part.rows)
        self.generate_render()

    def generate_render(self) -> None:
        """ Generate the part """
        self.scene.clear()
        part_cols = self.part.columns
        part_rows = self.part.rows

        # Draw the Header Row
        for hdr_offset, column in enumerate(part_cols):
            text = self.scene.addText(column)
            text.setDefaultTextColor(QtCore.Qt.black)
            text.setPos(hdr_offset * self.box_size + int(self.box_size), int(self.box_size / 2))

        # Draw the Part
        for y_offset, row in enumerate(part_rows):
            for x_offset, column in enumerate(part_cols):
                pin = self.part.get_pin(str(row), str(column))
                if pin:
                    pin_graphic = Pin(
                        pin,
                        QtCore.QRectF(
                            self.box_size * x_offset + int(self.box_size / 2),
                            self.box_size * y_offset + self.box_size,
                            self.box_size,
                            self.box_size,
                        ),
                        show_label=self.settings["labels"],
                        view=self,
                    )
                    self.scene.addItem(pin_graphic)
                    pin_graphic.clicked.connect(
                        self.parentWidget().parentWidget().set_properties_widget
                    )
                text = self.scene.addText(row)
                text.setDefaultTextColor(QtCore.Qt.black)
                text.setPos(
                    self.box_size * len(part_cols) + int(self.box_size),
                    self.box_size * y_offset + self.box_size + int(self.box_size / 2),
                )
        self.scene.update()

    def save(self) -> None:
        """ Save the Pixmap as a .png """
        rect = self.scene.itemsBoundingRect()
        if not rect.isEmpty():  # Only create a screen shot if there is something on it.
            self.scene.setSceneRect(rect)

            image = QtGui.QImage(
                self.scene.sceneRect().width(),
                self.scene.sceneRect().height(),
                QtGui.QImage.Format_RGB32,
            )
            image.fill(QtCore.Qt.transparent)

            painter = QtGui.QPainter(image)
            painter.setRenderHints(
                QtGui.QPainter.HighQualityAntialiasing
                | QtGui.QPainter.SmoothPixmapTransform
                | QtGui.QPainter.TextAntialiasing,
                True,
            )
            self.scene.render(painter)
            painter.end()
            save_file = Path(f'{self.settings["title"]}.png')
            self.log.info(f"Saved image to {save_file}")
            image.save(str(save_file))
        else:
            self.log.error("Nothing to create Image from.")

    def scale_box_size(self, columns: List, rows: List) -> None:
        """If the part width is less than 1536 (2K width) scale up."""
        part_width = (len(columns) + 1) * self.box_size
        if part_width < 1536.0:
            window_scale = 1536.0 / part_width
        else:
            window_scale = 1
        self.box_size = int(self.box_size * window_scale)
        self.settings["image_width"] = (len(columns) + 1) * self.box_size + self.box_size
        self.settings["image_height"] = (len(rows) + 1) * self.box_size + self.box_size
        self.setSceneRect(0, 0, self.settings["image_width"], self.settings["image_height"])
        self.fitInView(self.scene.sceneRect())

    def toggle_style(self):
        """Change between circles or squares."""
        if self.settings["circles"]:  # If true, set to false for rectangles.
            self.settings["circles"] = False
        else:
            self.settings["circles"] = True
        self.scene.update()

    def toggle_labels(self):
        """Change between labels on or off."""
        if self.settings["labels"]:
            self.settings["labels"] = False
        else:
            self.settings["labels"] = True
        self.scene.update()

    def rotate_drawing(self):
        """Rotate the diagram."""
        part_cols = self.part.columns
        part_rows = self.part.rows
        part_cols.reverse()
        self.part.columns = part_rows
        self.part.rows = part_cols
        self.generate_render()

    def mousePressEvent(self, event):
        """Hid the property widget if the view is clicked."""
        if not self.parentWidget().parentWidget().properties.isHidden():
            self.parentWidget().parentWidget().set_properties_widget(None)
            self.parentWidget().parentWidget().properties.setVisible(False)
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        """Zoom the View by the delta detected on the scroll wheel."""
        original_position = self.mapToScene(event.pos())
        if event.angleDelta().y() > 0:
            self.set_zoom(1)
        else:
            self.set_zoom(-1)
        new_position = self.mapToScene(event.pos())
        delta = new_position - original_position
        self.translate(delta.x(), delta.y())

    def reset_zoom(self):
        """Reset the view to the original scale."""
        self.scale(1.0, 1.0)
        self.zoom_level = 0
        self.resetTransform()

    def set_zoom(self, value=0.0):
        """Zoom the View."""
        if value == 0:
            self.reset_zoom()

        new_zoom = value + self.zoom_level
        if -5 <= new_zoom <= 10:
            if value == 1:
                self.zoom_level += 1
                self.scale(1.1, 1.1)
            elif value == -1:
                self.zoom_level += -1
                self.scale(0.9, 0.9)
