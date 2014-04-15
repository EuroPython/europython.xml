import csv
import markdown2
from lxml import objectify
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import Element


def get_entries(xml_in, xpath_filter):

    entries = list()
    with open(xml_in, 'rb') as fp:
        xml = fp.read()
    root = fromstring(xml)
    for num, entry in enumerate(root.xpath(xpath_filter)):
        entry.tail = None
        entry_d = objectify.fromstring(tostring(entry))
        entries.append(entry_d)
    return entries


class JinjaView(object):

    def time(self, entry):
        hours_start = int(entry.start / 100 )
        minutes_start = int(entry.start % 100)
        duration = int(entry.duration)
        start = datetime(2000, 1, 1, hours_start, minutes_start)
        end = start + timedelta(minutes=duration)
        return '{:02d}:{:02d} - {:02d}:{:02d}h'.format(start.hour, start.minute, end.hour, end.minute)

    def markdown(self, text):
        return markdown2.markdown(unicode(text))
