# Part Pinout Visualizer

Generate a visualization of a part to help with pinout or general planning.
Helpful in the early stages of design before layout begins.  Can use it for
anything that is on a grid.

### Usage
```
$ part-map -h
Usage: part-map [OPTIONS] FILENAME [json|tel|excel]

  Generate a visualization of a part to help with pinout or general
  planning. Helpful in the early stages of design before layout begins.  Can
  use it for anything that is on a grid.

Options:
  --version      Show the version and exit.
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

``` part_map.py -e artix7_example.xlsx -s ```
![Artix Example][example_artix]
``` part_map.py -j connector_example.json ```
![Connector Example][example_connector]


[example_artix]:./examples/artix7_example.png?raw=true "BGA Example"
[example_connector]: ./examples/connector_example.png?raw=true "Connector Example"