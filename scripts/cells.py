import numpy as np
import cv2,pickle

from helpers import Helpers
from digit import Digit


class Cells(object):
    '''
    Extracts each cell from the sudoku grid obtained
    from the Extractor
    '''

    def __init__(self, gridLess):
        print 'Extracting cells...',
        self.helpers = Helpers()
        self.cells = self.extractCells(gridLess)
        print 'done.'

    def extractCells(self, sudoku):
        cells = []
        W, H = sudoku.shape
        cell_size = W / 9
        for r in range(0, W, cell_size):
            row = []
            for c in range(0, W, cell_size):
                cell = self.helpers.make_it_square(
                    sudoku[r:r + cell_size, c:c + cell_size], 28)
                cell = self.clean(cell)
                digit = Digit(cell).digit
                #self.helpers.show(digit, 'Buggy')
                digit = self.centerDigit(digit)
                #self.helpers.show(digit, 'After centering')
                row.append(digit//255)
            cells.append(row)
        pickle.dump(cells, open('save','w'))
        return cells

    def clean(self, cell):
        contour = self.helpers.largestContour(cell.copy())
        x, y, w, h = cv2.boundingRect(contour)
        cell = self.helpers.make_it_square(cell[y:y + h, x:x + w], 28)
        cell = 255 * (cell / 150)
        return cell

    def centerDigit(self, digit):
        digit = self.centerX(digit)
        digit = self.centerY(digit)
        return digit

    def centerX(self, digit):
        topLine = self.helpers.getTopLine(digit)
        bottomLine = self.helpers.getBottomLine(digit)
        if topLine is None or bottomLine is None:
            return digit
        centerLine = (topLine + bottomLine) >> 1
        imageCenter = digit.shape[0] >> 1
        digit = self.helpers.rowShift(
            digit, start=topLine, end=bottomLine, length=imageCenter - centerLine)
        return digit

    def centerY(self, digit):
        leftLine = self.helpers.getLeftLine(digit)
        rightLine = self.helpers.getRightLine(digit)
        if leftLine is None or rightLine is None:
            return digit
        centerLine = (leftLine + rightLine) >> 1
        imageCenter = digit.shape[1] >> 1
        digit = self.helpers.colShift(
            digit, start=leftLine, end=rightLine, length=imageCenter - centerLine)
        return digit
