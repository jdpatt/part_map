"""Console scripts for prototype."""
import sys

import click

from part_map.part_map import PartMap
from PySide2 import QtWidgets


@click.group(
    invoke_without_command=True, context_settings=dict(help_option_names=["-h", "--help"])
)
@click.pass_context
@click.version_option()
def cli(ctx):
    """Part Map - A Graphical Interface to visual Pinouts."""
    if ctx.invoked_subcommand is None:
        app = QtWidgets.QApplication([])
        gui = PartMap()
        gui.show()
        sys.exit(app.exec_())


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--refdes", help="The refdes to pull from the Telesis.")
@click.option("--circles", "-c", is_flag=True, help="Draw using circles instead of rectangles.")
@click.option("--rotate", "-r", is_flag=True, help="Rotate the image by 90 degrees.")
@click.option("--no-labels", is_flag=True, help="Disable the text labels.")
@click.option("--save", "-s", is_flag=True, help="Save the image as a .png.")
@click.option("--dump", "-d", is_flag=True, help="Dump PartObject as a Json File.")
@click.option("--nogui", "-n", is_flag=True, help="Do not open GUI window.")
def load(filename, **kwargs) -> None:
    """Open the Part Map GUI and load a file for viewing."""

    app = QtWidgets.QApplication([])

    settings = {
        "refdes": kwargs["refdes"],
        "rotate": kwargs["rotate"],
        "circles": kwargs["circles"],
        "labels": not kwargs["no_labels"],
    }

    gui = PartMap(filename, settings)

    if not kwargs["nogui"]:
        gui.show()
    if kwargs["dump"]:
        gui.save_json()
    if kwargs["save"]:
        gui.save_image()
    if kwargs["nogui"]:
        app.closeAllWindows()
    else:
        sys.exit(app.exec_())
