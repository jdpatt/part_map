# Part Pinout Visualizer

Generate a visualization of a part to help with pinout or general planning.
Helpful in the early stages of design before layout begins.  Can use it for
anything that is on a grid.

### Usage
```
usage: part_map.py [-h] [--excel] [--json] [--tel] [--rotate] [--save]
                    [--dump] [--nogui]
                    [filename]

positional arguments:
  filename      The file to read in

optional arguments:
  -h, --help    show this help message and exit
  --excel, -e   Load from an Excel file
  --json, -j    Load from a Json file
  --tel, -t     Load from a Telesis file
  --rotate, -r  Rotate the image by 90 degrees
  --save, -s    Save the image as a .png
  --dump, -d    Dump PartObject as a Json File
  --nogui, -n   Do not open GUI window

USAGE:
    part_map.py -e part_spreadsheet.xlsx
    part_map.py -j part.json
    part_map.py -rsdt part.tel
```

### Example of a Artix7
[Artix 7 Pinout Files](https://www.xilinx.com/support/package-pinout-files/artix-7-pkgs.html)

``` part_map.py -e artix7_example.xlsx -s ```
![Artix Example][example_artix]
``` part_map.py -j connector_example.json ```
![Connector Example][example_connector]


[example_artix]: ./example/artix7_example.png?raw=true "BGA Example"
[example_connector]: ./example/connector_example.png?raw=true "Connector Example"