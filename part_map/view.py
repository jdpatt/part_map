""" Visual pin out of a BGA or connector """
import logging
from pathlib import Path
from typing import List

from PySide2 import QtCore, QtGui, QtWidgets


class PartViewer(QtWidgets.QGraphicsView):
    """ Create a render of the part and load it into a QWidget """

    # pylint: disable=R0902
    def __init__(self, parent=None):
        super(PartViewer, self).__init__(parent)
        self.log = logging.getLogger("partmap.view")

        self.settings = None
        self.part = None
        self.image = None

        self.box_size = 50
        self.zoom_level = 0

        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.ScrollHandDrag)

    def setup(self, part, settings):
        """Return the settings dictionary."""
        self.part = part
        self.settings = settings
        if self.settings["rotate"]:
            self.rotate_drawing()
        self.generate_render()

    def generate_render(self) -> None:
        """ Generate the part """
        part_cols = self.part.columns
        part_rows = self.part.rows
        self.scale_box_size(part_cols, part_rows)
        self.image = QtGui.QImage(
            self.settings["image_width"],
            self.settings["image_height"] + (self.box_size / 2),
            QtGui.QImage.Format_RGB32,
        )
        self.image.fill(QtGui.QColor("#ffffff"))  # Background Color
        paint = QtGui.QPainter(self.image)
        paint.setRenderHints(
            QtGui.QPainter.HighQualityAntialiasing
            | QtGui.QPainter.SmoothPixmapTransform
            | QtGui.QPainter.TextAntialiasing,
            True,
        )
        for hdr_offset, column in enumerate(part_cols):
            paint.drawText(
                QtCore.QRectF(
                    hdr_offset * self.box_size + int(self.box_size / 2),
                    0,
                    self.box_size,
                    self.box_size,
                ),
                QtCore.Qt.AlignCenter,
                column,
            )
        for y_offset, row in enumerate(part_rows):
            for x_offset, column in enumerate(part_cols):
                pin = self.part.get_pin(str(row), str(column))
                if pin and pin["name"] is not None:
                    fill = pin["color"]
                    brush = QtGui.QBrush(QtGui.QColor(fill))
                    paint.setBrush(brush)
                    if self.settings["circles"]:
                        rect = QtCore.QRectF(
                            self.box_size * x_offset + int(self.box_size / 2),
                            self.box_size * y_offset + self.box_size,
                            self.box_size - self.settings["margin"],
                            self.box_size - self.settings["margin"],
                        )
                        paint.drawEllipse(rect)
                    else:
                        rect = QtCore.QRectF(
                            self.box_size * x_offset + int(self.box_size / 2),
                            self.box_size * y_offset + self.box_size,
                            self.box_size,
                            self.box_size,
                        )
                        paint.drawRect(rect)
                    if not self.settings["labels"]:
                        paint.drawText(rect, QtCore.Qt.AlignCenter, pin["name"][:6])
            paint.drawText(
                QtCore.QRectF(
                    self.box_size * len(part_cols) + int(self.box_size / 2),
                    self.box_size * y_offset + self.box_size,
                    self.box_size,
                    self.box_size,
                ),
                QtCore.Qt.AlignCenter,
                row,
            )
        paint.end()

    def save(self) -> None:
        """ Save the Pixmap as a .png """
        save_file = Path(f'{self.settings["title"]}.png')
        self.log.info(f"Saved image to {save_file}")
        self.image.save(str(save_file))

    def scale_box_size(self, columns: List, rows: List) -> None:
        """ If the part width is less than 1536 (2K width) scale up
        """
        part_width = (len(columns) + 1) * self.box_size
        if part_width < 1536.0:
            window_scale = 1536.0 / part_width
        else:
            window_scale = 1
        self.box_size = int(self.box_size * window_scale)
        self.settings["image_width"] = (len(columns) + 1) * self.box_size + self.box_size
        self.settings["image_height"] = (len(rows) + 1) * self.box_size + self.box_size

    def redraw(self):
        """Update the current pixmap."""
        self.scene.clear()
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.scene.addPixmap(pixmap)

    def toggle_style(self):
        """Change between circles or squares."""
        if self.settings["circles"]:  # If true, set to false for rectangles.
            self.settings["circles"] = False
        else:
            self.settings["circles"] = True
        self.generate_render()
        self.redraw()

    def rotate_drawing(self):
        """Rotate the diagram."""
        part_cols = self.part.columns
        part_rows = self.part.rows
        part_cols.reverse()
        self.part.columns = part_rows
        self.part.rows = part_cols
        self.generate_render()
        self.redraw()

    def wheelEvent(self, event) -> None:  # pylint: disable=C0103
        """ If the wheel is scrolled; figure out how much to zoom """
        steps = event.angleDelta().y() / 120
        self.zoom_level += steps
        if (self.zoom_level * steps) < 0:
            self.zoom_level = steps  # Zoom out by steps
        factor = 1.0 + (steps / 10.0)
        self.settings["factor"] *= factor
        if self.settings["factor"] < 0.3:
            self.settings["factor"] = 0.3
        elif self.settings["factor"] > 5:
            self.settings["factor"] = 5
            return
        else:
            self.scale(factor, factor)
