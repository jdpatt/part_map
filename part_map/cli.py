"""Console scripts for prototype."""
import sys

import click

from part_map.part_map import PartMap
from PySide2.QtWidgets import QApplication


@click.group(
    invoke_without_command=True, context_settings=dict(help_option_names=["-h", "--help"])
)
@click.version_option()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--refdes", help="The refdes to pull from the Telesis.")
@click.option("--circles", "-c", is_flag=True, help="Draw using circles instead of rectangles.")
@click.option("--rotate", "-r", is_flag=True, help="Rotate the image by 90 degrees.")
@click.option("--no-labels", is_flag=True, help="Disable the text labels.")
@click.option("--save", "-s", is_flag=True, help="Save the image as a .png.")
@click.option("--dump", "-d", is_flag=True, help="Dump PartObject as a Json File.")
@click.option("--nogui", "-n", is_flag=True, help="Do not open GUI window.")
def cli(filename, **kwargs) -> None:
    """Generate a visualization of a part to help with pinout or general planning.
    Helpful in the early stages of design before layout begins.  Can use it for
    anything that is on a grid.
    """

    app = QApplication([])
    gui = PartMap(filename, kwargs)

    if not kwargs["nogui"]:
        gui.show()
    if kwargs["dump"]:
        gui.part.dump_json()
    if kwargs["save"]:
        gui.view.save()
    if kwargs["nogui"]:
        app.closeAllWindows()
    else:
        sys.exit(app.exec_())
