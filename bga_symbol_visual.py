''' Visual pinout of a bga '''
from tkinter import Tk, Canvas, Scrollbar, RIGHT, Y
from re import split
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string
from natsort import natsorted


GRID_SPACING = 0
ELEMENT_SIZE = 24
BORDER = 30
OFFSET = BORDER + GRID_SPACING

def sort_and_split_pin_list(plist):
    ''' Haven't found a cleaner way to sort.  Need A, B, ... Z, AA, ... CA type sorting '''
    r_list = list()
    c_list = list()
    for pin in plist:
        split_pin = split(r'(\d+)', pin)
        if split_pin[0] not in r_list:
            r_list.append(split_pin[0])
        c_list.append(split_pin[1])
    temp = list()
    temp2 = list()
    for item in r_list:
        if len(item) > 1:
            temp.append(item)
        else:
            temp2.append(item)
    temp2 = natsorted(temp2)
    temp2.extend(natsorted(temp))
    return natsorted(set(c_list)), temp2


def read_in_xlsx_file(file):
    '''  Read in native excel and get the pin number, function, and color to shade '''
    workbook = load_workbook(file)
    sheet = workbook.active  #Grab the first sheet
    for col in sheet.iter_cols():
        for cell in col:
            if cell.value == 'Name':
                function_column = column_index_from_string(cell.column)
            if cell.value == 'Number':
                pin_column = column_index_from_string(cell.column)
    bga_dict = dict()
    pin_list = list()
    color_map_dict = dict()
    for excel_row in range(2, sheet.max_row):
        pin = sheet.cell(row=excel_row, column=pin_column)
        function = sheet.cell(row=excel_row, column=function_column)
        if pin.value is not None or function.value is not None:
            bga_dict.update({pin.value:function.value})
            pin_list.append(pin.value)
            if function.value not in color_map_dict:
                if function.fill.patternType == 'solid':
                    color_map_dict.update({pin.value:'#' + function.fill.start_color.rgb[2:]})
    col_list, row_list = sort_and_split_pin_list(pin_list)
    return bga_dict, col_list, row_list, color_map_dict

if __name__ == '__main__':
    BGA, COLUMNS, ROWS, COLORS = read_in_xlsx_file("bga.xlsx")

    MASTER = Tk()
    PIN_SCROLL = Scrollbar(MASTER)
    PIN_SCROLL.pack(side=RIGHT, fill=Y)
    WINDOW = Canvas(MASTER, width=((len(COLUMNS) + 1) * ELEMENT_SIZE) + BORDER,
                    height=(len(ROWS) + 1) * ELEMENT_SIZE + BORDER)
    WINDOW.pack()
    PIN_SCROLL.config(command=WINDOW.yview)

    for hdr_index, row in enumerate(ROWS):
        WINDOW.create_text((ELEMENT_SIZE * hdr_index) + GRID_SPACING + (ELEMENT_SIZE/2),
                           GRID_SPACING + (ELEMENT_SIZE/2),
                           font=("Purisa", 4),
                           text=row)

    # Create the BGA Canvas
    for c_index, column in enumerate(COLUMNS):
        for r_index, row in enumerate(ROWS):
            pinname = row + str(column)
            if pinname in BGA:
                if BGA[pinname] is not None and len(BGA[pinname]) > 5:
                    pin_function = BGA[pinname][:5]
                else:
                    pin_function = BGA[pinname]
                if pinname in COLORS:
                    fill = COLORS[pinname]
                else:
                    fill = ''
                # create_oval for circles
                WINDOW.create_rectangle((ELEMENT_SIZE * r_index) + GRID_SPACING,
                                        (ELEMENT_SIZE * c_index) + OFFSET,
                                        (ELEMENT_SIZE * r_index) + ELEMENT_SIZE,
                                        (ELEMENT_SIZE * c_index) + ELEMENT_SIZE + BORDER,
                                        fill=fill)
                WINDOW.create_text((ELEMENT_SIZE * r_index) + GRID_SPACING + (ELEMENT_SIZE/2),
                                   (ELEMENT_SIZE * c_index) + OFFSET + (ELEMENT_SIZE/2),
                                   font=("Purisa", 4),
                                   text=pin_function)
        WINDOW.create_text((ELEMENT_SIZE * (len(COLUMNS) + 1)) + GRID_SPACING + (ELEMENT_SIZE/2),
                           (ELEMENT_SIZE * c_index) + OFFSET + (ELEMENT_SIZE/2),
                           font=("Purisa", 4),
                           text=column)
    MASTER.mainloop()
