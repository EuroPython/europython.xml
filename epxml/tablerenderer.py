# -*- coding: utf-8 -*-

import os
import sys

import plac
import table
import util


def normalize(s):
    """ Normalize a string in order to be used as CSS class """
    return s.lower().replace(u' ', u'-')


def event_renderer(event):
    """ Renders a single <event> as serialized
        through lxml.objectify as cell content for
        the schedule table.
    """
    result = list()
    css_outer = u' '.join(['topic-{}'.format(normalize(t.topic.text)) for t in event.topics])
    result.append(u'<div class="entry {}">'.format(css_outer))
    result.append(u'<div class="time">{}</div>'.format(event.attrib['start-end']))
    result.append(u'<div class="title">{}</div>'.format(event.title))
    result.append(u'<div class="speakers">')
    if event.speakers.getchildren():
        for speaker in event.speakers:
            result.append(u'<div class="speaker">{}</div>'.format(speaker.speaker.name))
    result.append(u'</div>')
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

        # determine starting row of event
        e_start = e.start.text      # format '0700'
        s_hour = int(e_start[:2])
        s_minute = int(e_start[2:])
        s_row = (s_hour - hour_start) * (60 / resolution) + s_minute / resolution

        # calculate row span over multiple time slots
        s_duration = int(e.duration)
        rowspan = s_duration / resolution 

        # determine col of event
        if e.room == 'ALL':
            # span over all columns
            s_col = 0
            colspan = len(rooms)
            tb.addCell(s_row, s_col, rowspan=rowspan, colspan=colspan, event=e)
        else:
            for room in e.room.text.split(','):
                if room in rooms:
                    s_col = rooms.index(room)
                    colspan = 1
                    tb.addCell(s_row, s_col, rowspan=rowspan, colspan=colspan, event=e)

    return tb.render(event_renderer=event_renderer)


@plac.annotations(
    xml_in=('Schedule XML file', 'option', 'i'),
    html_out=('Output HTML file', 'option', 'o'),
    )
def demo(xml_in, html_out='table.html'):

    rooms = [u'C01', u'B05/B06', u'B07/B08', u'B09', u'A08']

    if not xml_in:
        raise ValueError('Missing --xml-in|-i parameter')
    with open(xml_in, 'rb') as fp:
        schedule_xml = fp.read()

    html = conv(schedule_xml,
               '2014-07-22',
               rooms,
               hour_start=7,
               hour_end=21,
               resolution=15,
               caption=u'2014-07-22',
               event_renderer=event_renderer
               )

    with open(html_out, 'wb') as fp:
        fp.write(html)
        print 'HTML output written to {}'.format(html_out)


def main():
    plac.call(demo)


if __name__ == '__main__':
    main()
