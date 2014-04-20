
import cStringIO

class BaseCell(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return '{}({},{})'.format(self.__class__.__name__, self.row, self.col)

class EmptyCell(BaseCell):
    pass


class Cell(BaseCell):

    def __init__(self, event, rowspan=1, colspan=1):
        self.event = event
        self.rowspan = rowspan
        self.colspan = colspan

    def __repr__(self):
        return '{}(rowspan={}, colspan={})'.format(self.__class__.__name__, self.rowspan, self.colspan)


class SpanCell(EmptyCell):
    pass


class Table(object):
    """ Abstract HTML table model """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.caption = None
        self.col_headers = list()
        self.row_headers = list()

        for row_index in range(0, rows):
            row = []
            for col_index in range(0, cols):
                row.append(EmptyCell(row_index, col_index))
            self.cells.append(row)

    def addCell(self, row, col, rowspan=1, colspan=1, event=None):

        if not isinstance(self.cells[row][col], EmptyCell):
            raise ValueError('Cell [{}][{}] seems to be already in use'.format(row, col))

        # insert dummy span cell in case of a rowspan or colspan > 1
        for i in range(0, rowspan):
            for j in range(0, colspan):
                self.cells[row + i][col + j]  = SpanCell(row + i, col + j)
        # now insert content cell
        self.cells[row][col] = Cell(event, rowspan, colspan)

    def render(self, event_renderer):

        out = list()
        out.append(u'<table border="1">')

        # table caption
        if self.caption:
            out.append(u'<caption>{}</caption>'.format(self.caption))

        # column headers
        if self.col_headers:
            out.append(u'<thead>')
            out.append(u'<tr>')
            if self.row_headers:
                out.append(u'<th></th>')
            for hd in self.col_headers:
                out.append(u'<th>{}</th>'.format(hd))
            out.append(u'</tr>')
            out.append(u'</thead>')

        out.append('<tbody>')
        for row_index, row in enumerate(self.cells):
            out.append(u'<tr>')
            if self.row_headers:
                out.append(u'<th>{}</th>'.format(self.row_headers[row_index]))
            for cell in row:
                if isinstance(cell, SpanCell):
                    pass
                elif isinstance(cell, EmptyCell):
                    out.append(u'<td width="100" class="empty"></td>')
                elif isinstance(cell, Cell):
                    out.append(u'<td width="100" class="cell" rowspan="{}" colspan="{}">{}</td>'.format(cell.rowspan, cell.colspan, event_renderer(cell.event)))

            out.append(u'</tr>')
        out.append('</tbody>')
        out.append(u'</table>')
        return u'\n'.join(out).encode('utf-8')


if __name__ == '__main__':

    rooms = [u'C01',
             u'B05/06',
             u'B07/08',
             u'B09',
             u'A08']

    hour_start = 7
    hour_end = 24
    resolution = 5

    row_headers = list()
    for hour in range(hour_start, hour_end + 1):
        for minute in range(0, 60, resolution):
            row_headers.append('{:02}:{:02}h'.format(hour, minute))
    table = Table(60/resolution * (hour_end - hour_start) , len(rooms))
    table.col_headers = rooms
    table.row_headers = row_headers
    table.addCell(1, 1, event='Meeting1')
    table.addCell(2, 1, event='Meeting2')
    table.addCell(2, 1, event='Meeting3')
    table.addCell(3, 2, rowspan=2, event='Long Meeting1')
    table.addCell(0, 2, colspan=2, event='Futter')

    def event_renderer(s):
        return '<div>{}</div>'.format(s)

    print table.render(event_renderer)
    
