import csv
from datetime import datetime
from datetime import timedelta
import markdown2
from lxml import objectify
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import Element


def entry2startend(entry):
    hours_start = int(entry.start / 100 )
    minutes_start = int(entry.start % 100)
    duration = int(entry.duration)
    start = datetime(2000, 1, 1, hours_start, minutes_start)
    end = start + timedelta(minutes=duration)
    return '{:02d}:{:02d} - {:02d}:{:02d}h'.format(start.hour, start.minute, end.hour, end.minute)


def get_entries(xml_in, xpath_filter):

    entries = list()
    if xml_in.startswith('<'):
        xml = xml_in
    else:
        with open(xml_in, 'rb') as fp:
            xml = fp.read()
    root = fromstring(xml)
    for num, entry in enumerate(root.xpath(xpath_filter)):
        entry.tail = None
        entry_d = objectify.fromstring(tostring(entry))
        entry_d.attrib['start-end'] = entry2startend(entry_d)
        entries.append(entry_d)
    return entries


class JinjaView(object):

    def time(self, entry):
        return entry2startend(entry)

    def markdown(self, text):
        return markdown2.markdown(unicode(text))
