import os
import sys

import table
import util


if __name__ == '__main__':

    xml_in = sys.argv[1]

    date_str = '2014-07-22'
    entries=util.get_entries(xml_in, '//day[@date="{}"]/entry'.format(date_str))

    rooms = [u'C01',
             u'B05/B06',
             u'B07/B08',
             u'B09',
             u'A08']

    hour_start = 7
    hour_end = 24
    resolution = 15

    row_headers = list()
    for hour in range(hour_start, hour_end + 1):
        for minute in range(0, 60, resolution):
            row_headers.append('{:02}:{:02}h'.format(hour, minute))
    tb= table.Table(60/resolution * (hour_end - hour_start) , len(rooms))
    tb.col_headers = rooms
    tb.row_headers = row_headers


    for e in entries:
        e_start = str(e.start)
        s_hour = int(e_start[:2])
        s_minute = int(e_start[2:])
#        print e.room, s_hour, s_minute
        s_row = (s_hour - hour_start) * (60 / resolution) + s_minute / resolution
        s_col = rooms.index(e.room)
        s_duration = int(e.duration)
        row_span = s_duration / resolution 
#        print s_duration
#        print s_row, s_col, row_span
#        print type(e.title.text)

        t = e.title.text
        if not isinstance(t, unicode):
            t = unicode(t, 'utf8', 'ignore')
        tb.addCell(s_row, s_col, rowspan=row_span, event=t)
        

    print tb.render()
