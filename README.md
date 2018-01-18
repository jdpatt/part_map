### BGA Footprint Visual

Wanted a way to visual what pins I was assigning to on large FPGAs.  Takes in a
standard excel file and looks for the columns named "Name" and "Number" then it 
generates a diagram using tkinter.  The color in the cell is determined by the
cell's fill color. Do not use the built-in themes as they do not have a color 
directly assigned to them.  Use the standard colors or excel's color picker to 
pick the cell fill and always use a solid fill. (No gradients)  Since the "Name"
can be a long string when entered into a schematic; the script will cut down the
text to the first 5 characters in a string. (DDR4_CKE0_L  -> DDR4_)

## Example of a Artix7
[Artix 7 Pinout Files](https://www.xilinx.com/support/package-pinout-files/artix-7-pkgs.html)

![BGA Example][example]


[example]: ./example.jpg?raw=true "BGA Example"