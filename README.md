# Part Pinout Visualizer

Generate a visualization of a part to help with pinout or general planning.
Helpful in the early stages of design before layout begins.  Can use it for
anything that is on a grid.

## Installation

1. Clone this repo
2. Cd into the folder
3. `pip install .`

## Usage

There are three ways to use part-map:

- `python -m part_map` - Opens the GUI without loading a file.
- `part-map` - Opens the GUI without loading a file.
- `part-map load [OPTIONS] FILENAME` - Load the file and open the GUI with any options.

```bash
part-map load -h
Usage: part-map load [OPTIONS] FILENAME

  Open the Part Map GUI and load a file for viewing.

Options:
  --refdes TEXT  The refdes to pull from the Telesis.
  -c, --circles  Draw using circles instead of rectangles.
  -r, --rotate   Rotate the image by 90 degrees.
  --no-labels    Disable the text labels.
  -s, --save     Save the image as a .png.
  -d, --dump     Dump PartObject as a Json File.
  -n, --nogui    Do not open GUI window.
  -h, --help     Show this message and exit.
```

### Example of a Artix7

[Artix 7 Pinout Files](https://www.xilinx.com/support/package-pinout-files/artix-7-pkgs.html)

`part-map load -s artix7_example.xlsx`
![Artix Example][example_artix]

`part-map load connector_example.json`
![Connector Example][example_connector]

[example_artix]:./examples/artix7_example.png?raw=true "BGA Example"
[example_connector]: ./examples/connector_example.png?raw=true "Connector Example"
