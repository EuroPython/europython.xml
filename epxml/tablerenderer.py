# -*- coding: utf-8 -*-

import os
import sys

import table
import util


def event_renderer(event):
    result = [u'<div class="title">{}</div>'.format(event.title)]
    result.append(u'<div class="speakers">')
    if event.speakers.getchildren():
        for speaker in event.speakers:
            result.append(u'<div class="speaker">{}</div>'.format(speaker.speaker.name))
    result.append(u'</div>')
    return u''.join(result)


def conv(schedule_xml, # schedule XML string or schedule XML filename
        date_str,      # YYYY-MM-DD
        rooms,         # list of rooms
        hour_start=0,  # schedule starts
        hour_end=24,   # schedule ends
        resolution=15, # timeslot resolution in minutes
        caption=None,  # caption of table
        event_renderer=None):

    entries = util.get_entries(schedule_xml, '//day[@date="{}"]/entry'.format(date_str))

    row_headers = list()
    for hour in range(hour_start, hour_end + 1):
        for minute in range(0, 60, resolution):
            row_headers.append('{:02}:{:02}h'.format(hour, minute))
    tb= table.Table(60/resolution * (hour_end - hour_start) , len(rooms))
    tb.caption = caption
    tb.col_headers = rooms
    tb.row_headers = row_headers

    for e in entries:
        e_start = e.start.text      # format '0700'
        s_hour = int(e_start[:2])
        s_minute = int(e_start[2:])
        s_row = (s_hour - hour_start) * (60 / resolution) + s_minute / resolution

        if e.room == 'ALL':
            # span over all columns
            s_col = 0
            colspan = len(rooms)
        elif e.room in rooms:
            # one room
            s_col = rooms.index(e.room)
            colspan = 1
        else:
            # unknown room, skip
            continue

        s_duration = int(e.duration)
        # calculate row span over multiple time slots
        rowspan = s_duration / resolution 

        tb.addCell(s_row, s_col, rowspan=rowspan, colspan=colspan, event=e)

    return tb.render(event_renderer=event_renderer)


if __name__ == '__main__':

    rooms = [u'C01', u'B05/B06', u'B07/B08', u'B09', u'A08']

    with open(sys.argv[1], 'rb') as fp:
        schedule_xml = fp.read()

    print conv(schedule_xml,
               '2014-07-22',
               rooms,
               hour_start=7,
               hour_end=21,
               resolution=15,
               caption=u'üöä - 2014-07-22',
               event_renderer=event_renderer
               )

