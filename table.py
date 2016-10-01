from ui import Term
from functools import reduce

class Table:
    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2

    def __init__(self, align = ALIGN_RIGHT):
        self._align = align
        self._colLength = []
        self._header = None
        self._lines = []
        self._colors = []
        self._header_color = False

    def _update_cols(self, cols):
        colsLen = len(cols)
        if colsLen > len(self._colLength):
            self._colLength.extend([0] * (colsLen - len(self._colLength)))
        for i, col in enumerate(cols):
            if not isinstance(col, str):
                raise TypeError('strings expected')
            if self._colLength[i] < len(col):
                self._colLength[i] = len(col)

    def add_header(self, *cols, **kwargs):
        self._update_cols(cols)
        self._header = cols
        if 'colors' in kwargs and kwargs['color'] == True:
            self._header_color = True

    def add_line(self, *cols):
        if len(cols) < 1:
            self._lines.append(None)
            return
        self._update_cols(cols)
        self._lines.append(cols)

    def add_colors(self, *colors):
        self._colors = list(colors)

    def _get_separator(self):
        totalColLen = reduce(lambda x,y: x+y, self._colLength) + (len(self._colLength) * 3 + 1)
        return '-' * totalColLen + '\n'

    def _get_line(self, cols, with_colors = False):
        s = '|'
        for i, col in enumerate(cols):
            if len(col) < self._colLength[i]:
                padding = self._colLength[i] - len(col) + 1
                if self._align == Table.ALIGN_RIGHT:
                    val = ' ' * padding + col
                elif self._align == Table.ALIGN_LEFT:
                    val = ' ' + col + ' ' * (padding - 1)
                elif self._align == Table.ALIGN_CENTER:
                    if (padding % 2) == 1:
                        mid = int((padding - 1) / 2)
                        val = (mid + 1) * ' ' + col + mid * ' '
                    else:
                        mid = int(padding / 2)
                        val = mid * ' ' + col + mid * ' '
            elif len(col) > self._colLength[i]:
                val = col[:(self._colLength[i] - 3)] + '...'
            else:
                val = ' ' + col
            if with_colors and i < len(self._colors) and self._colors[i] != None:
                val = self._colors[i] + val + Term.END
            s += val + ' |'
        return s

    def print_separator(self):
        print(self._get_separator(), end = '')

    def print(self):
        totalColLen = reduce(lambda x,y: x+y, self._colLength) + (len(self._colLength) * 3 + 1)
        if len(self._lines) < 1:
            return

        separator = self._get_separator()
        table = separator
        if self._header != None:
            table += self._get_line(self._header, self._header_color) + '\n'
            table += separator
        for s in self._lines:
            table += self._get_line(s, True) + '\n'
            table += separator
        print(table, end='')
