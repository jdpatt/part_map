#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
''' Visual pinout of a bga or connector '''
from re import split
from sys import exit, argv
from logging import basicConfig, getLogger, INFO
from json import load, dump
from os.path import abspath, join, dirname, basename
from os import getcwd
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string
from natsort import natsorted
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene)
from PyQt5.QtGui import (QPainter, QBrush, QColor, QFontMetrics, QFont, QImage,
                         QPixmap)
from PyQt5.QtCore import QRectF, Qt, QPoint


class PartViewer(QGraphicsView):
    ''' Create a render of the part and load it into a QWidget '''
    def __init__(self, part, width, height, title='PartViewer', rotate=False):
        self.title = title
        self.height = height
        self.width = width
        self.part = part
        self.orientation = rotate
        self.zoom = 0
        super(PartViewer, self).__init__()
        self.image = self.createImage()
        self.initUI()
        self.total_steps = 0
        self.factor = 1.0

    def initUI(self):
        self.setWindowTitle(self.title)
        self.item = QPixmap.fromImage(self.image)
        item = self.item.scaled(self.width,
                                self.height,
                                Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
        self.scene = QGraphicsScene()
        self.scene.addPixmap(item)
        self.setScene(self.scene)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.ScrollHandDrag)

    def resetZoom(self):
        self.fitInView(QRectF(0, 0, self.width, self.height))

    def wheelEvent(self, event):
        steps = (event.angleDelta().y() / 120)
        self.total_steps += steps
        if (self.total_steps * steps) < 0:
            self.total_steps = steps  # Zoom out by steps
        factor = 1.0 + steps/10.0
        self.factor *= factor
        if self.factor < .6:
            self.factor = .6
        elif self.factor > 5:
            self.factor = 5
            return
        else:
            self.scale(factor, factor)

    def createImage(self):
        COLUMNS = self.part.getColumns()
        ROWS = self.part.getRows()
        num_of_cols = len(COLUMNS)
        num_of_rows = len(ROWS)
        w, h = self.scaleBoxSize(COLUMNS, ROWS)
        img = QImage(w,
                     h + self.HALF_BOX,
                     QImage.Format_RGB32)  # 2k image
        img.fill(QColor('#ffffff'))  # Background Color
        self.paint = QPainter(img)
        self.paint.setRenderHints(QPainter.HighQualityAntialiasing |
                                  QPainter.SmoothPixmapTransform |
                                  QPainter.TextAntialiasing, True)
        if self.orientation:  # TODO: Rotate all pieces in painter not just img
            self.paint.translate(QPoint(w, 0))
            self.paint.rotate(90)
        for hdr_offset, column in enumerate(COLUMNS):
            self.paint.drawText(QRectF(hdr_offset * self.BOX_SIZE + self.HALF_BOX,
                                       0,
                                       self.BOX_SIZE,
                                       self.BOX_SIZE),
                                Qt.AlignCenter,
                                column)
        for y_offset, row in enumerate(ROWS):
            for x_offset, column in enumerate(COLUMNS):
                pn = str(row) + column
                pin = self.part.getPin(pn)
                if pin and pin['name'] is not None:
                    fill = pin['color']
                    brush = QBrush(QColor(fill))
                    self.paint.setBrush(brush)
                    rect = QRectF(self.BOX_SIZE * x_offset + self.HALF_BOX,
                                  self.BOX_SIZE * y_offset + self.BOX_SIZE,
                                  self.BOX_SIZE,
                                  self.BOX_SIZE)
                    self.paint.drawRect(rect)
                    pin_name = pin['name'][:6]
                    self.paint.drawText(rect, Qt.AlignCenter, pin_name)
            self.paint.drawText(QRectF(self.BOX_SIZE * num_of_cols + self.HALF_BOX,
                                       self.BOX_SIZE * y_offset + self.BOX_SIZE,
                                       self.BOX_SIZE,
                                       self.BOX_SIZE),
                                Qt.AlignCenter,
                                row)
        self.paint.end()
        return img

    def save(self):
        save_file = join(PATH, self.title + '.png')
        print(f'Saved to {save_file}')
        self.image.save(save_file)

    def scaleBoxSize(self, COLUMNS, ROWS):
        self.BOX_SIZE = 50.0
        part_width = (len(COLUMNS) + 1) * self.BOX_SIZE
        if 1536.0 > part_width:
            self.window_scale = 1536.0/part_width
        else:
            self.window_scale = part_width/1536.0
        self.BOX_SIZE = self.BOX_SIZE * self.window_scale
        part_width = (len(COLUMNS) + 1) * self.BOX_SIZE + self.BOX_SIZE
        part_height = (len(ROWS) + 1) * self.BOX_SIZE + self.BOX_SIZE
        self.HALF_BOX = self.BOX_SIZE / 2
        return part_width, part_height


class PartObject(object):
    ''' Load and create a part from a source '''
    def __init__(self, pins, filename):
        super(PartObject, self).__init__()
        self.__pins = pins
        self.__columns, self.__rows = self.sortAndSpiltPinList()
        self.filename = basename(filename).split('.')[0]

    @classmethod
    def fromExcel(cls, filename):
        ''' Import an Excel and create a PartObject '''
        number = 'Number'
        name = 'Name'
        workbook = load_workbook(filename)
        sheet = workbook.active  # Grab the first sheet
        header = sheet.iter_cols(max_row=1)
        try:
            column = PartObject.getColIndexOfHeader([number, name], header)
            bga = dict()
            for excel_row in range(2, sheet.max_row + 1):
                pin = sheet.cell(row=excel_row, column=column[number]).value
                net = sheet.cell(row=excel_row, column=column[name])
                if pin is not None or net.value is not None:
                    if net.fill.patternType == 'solid':
                        bga.update({pin: {'name': net.value,
                                          'color': str('#' + net.fill.start_color.rgb[2:])}})
                    else:
                        bga.update({pin: {'name': net.value,
                                          'color': '#ffffff'}})
        except (TypeError, ValueError, KeyError, UnboundLocalError) as error:
            print(error)
            raise
        return cls(bga, filename)

    @classmethod
    def fromTelesis(cls, filename, refdes):
        ''' Import a Telesis formatted file and create a PartObject '''
        with open(tel_file, 'r') as fl:
            tel_text = fl.readlines()
        tel_netlist = dict()
        for line in tel_text:
            reg = match(r'(.*);', line)
            reg2 = findall(ref + r'\.([a-zA-Z0-9]+)', line)
            if reg and reg2:
                net = reg.group(1)
                for reg_match in reg2:
                    pin = reg_match
                    tel_netlist.update(
                        {pin: {'name': net, 'color': '#ffffff'}})
        return cls(tel_netlist, filename)

    @classmethod
    def fromJson(cls, filename):
        ''' Import a json file with a format {pin: {name:, color:}} '''
        return cls(load(open(filename)), filename)

    def getColIndexOfHeader(name, columns):
        indexes = dict()
        for col in columns:
            if col[0].value in name:  # Only look at the first row
                indexes.update(
                    {col[0].value: column_index_from_string(col[0].column)})
        return indexes

    def addPin(self, pin, net, color):
        self.__pins.update({pin: {'name': net, 'color': color}})

    def getColumns(self):
        return self.__columns

    def getRows(self):
        return self.__rows

    def getPin(self, pin):
        if pin in self.__pins:
            return self.__pins[pin]
        return None

    def getPins(self):
        return self.__pins.keys()

    def getNumberofPins(self):
        return len(self.__pins)

    def getNames(self):
        return self.__pins.values()['name']

    def dumpJson(self):
        ''' Dump the PartObject dictionary to a .json file '''
        save_file = join(PATH, self.filename + '.json')
        print(f'Saved to {save_file}')
        with open(save_file, 'w') as outfile:
            dump(self.__pins, outfile, indent=4, separators=(',', ': '))

    def sortAndSpiltPinList(self):
        ''' Take a list of pins and spilt by letter and number then sort '''
        r_list = list()
        c_list = list()
        for pin in self.getPins():
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


def setupLogger(logger_filename):
    ''' Configure a logger at the current level= setting '''
    log_file = join(PATH, logger_filename)
    basicConfig(filename=log_file,
                format='%(levelname)s: %(message)s',
                filemode="w",
                level=INFO)
    logger = getLogger('root')
    return logger


def parseCommandLine():
    ''' Handle any command line input '''
    usage = '''USAGE:
    part_map.py -e part_spreadsheet.xlsx
    part_map.py -j part.json
    part_map.py -rsdt part.tel'''
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            epilog=usage)
    parser.add_argument('filename',
                        nargs='?',
                        default='artix7_example.xlsx',
                        help='The  file to read in')
    parser.add_argument('--excel', '-e',
                        action='store_true',
                        help='Load from an excel file')
    parser.add_argument('--json', '-j',
                        action='store_true',
                        help='Load from a json file')
    parser.add_argument('--tel', '-t',
                        action='store_true',
                        help='Load from a Telesis file')
    parser.add_argument('--refdes',
                        help='The refdes to pull from the Telesis')
    parser.add_argument('--rotate', '-r',
                        action='store_true',
                        help='Rotate the image by 90 degrees')
    parser.add_argument('--save', '-s',
                        action='store_true',
                        help='Save the image as a .png')
    parser.add_argument('--dump', '-d',
                        action='store_true',
                        help='Dump PartObject as a Json File')
    parser.add_argument('--nogui', '-n',
                        action='store_true',
                        help='Do not open GUI window')
    return parser.parse_args()


def main():
    ARGS = parseCommandLine()
    if ARGS.excel:
        PART = PartObject.fromExcel(ARGS.filename)
    elif ARGS.json:
        PART = PartObject.fromJson(ARGS.filename)
    elif ARGS.tel:
        PART = PartObject.fromTelesis(ARGS.filename, ARGS.refdes)
    else:
        exit()
    global app
    app = QApplication(argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    VIEW = PartViewer(PART,
                      width,
                      height,
                      title=basename(ARGS.filename).split('.')[0],
                      rotate=ARGS.rotate)
    if not ARGS.nogui:
        VIEW.show()
    if ARGS.dump:
        PART.dumpJson()
    if ARGS.save:
        VIEW.save()
    if ARGS.nogui:
        app.closeAllWindows()
    else:
        exit(app.exec())


app = None
PATH = getcwd()
# Setup Global Logger module
# LOG = setupLogger('part_map.txt')

if __name__ == '__main__':
    main()
