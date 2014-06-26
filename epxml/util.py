import re
import csv
import operator
from datetime import datetime
from datetime import timedelta
import markdown2
from lxml import objectify
import lxml.html
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

def entry2startduration(entry):
    hours_start = int(entry.start / 100 )
    minutes_start = int(entry.start % 100)
    duration = int(entry.duration)
    start = datetime(2000, 1, 1, hours_start, minutes_start)
    if duration <= 60:
        duration_s = u'{} min'.format(duration)
    else:
        hours = duration / 60
        minutes = duration % 60
        duration_s = u'{}h'.format(hours)
        if minutes != 0:
            duration_s += u'{}min'.format(minutes)
    return '{:02d}:{:02d}  ({})'.format(start.hour, start.minute, duration_s)

def get_entries(xml_in, xpath_filter):
    """ Parse 'accepted.xml' file/string and return
        all entries as list filtered using the given 
        xpath filter.
    """

    if xml_in.startswith('<'):
        xml = xml_in
    else:
        with open(xml_in, 'rb') as fp:
            xml = fp.read()

    # lame transliteration with one speaker name causing
    # font embedding problems during PDF generation
#    xml = xml.replace('&#263;', 'c')

    root = fromstring(xml)
    entries = list()
    for num, entry in enumerate(root.xpath(xpath_filter)):
        entry.tail = None
        entry_d = objectify.fromstring(tostring(entry))
        entry_d.attrib['start-end'] = entry2startend(entry_d)
        entries.append(entry_d)

    return sorted(entries, key=operator.itemgetter('title'))


class JinjaView(object):

    def time(self, entry):
        return entry2startend(entry)

    def time_duration(self, entry):
        return entry2startduration(entry)

    def lower(self, s):
        return unicode(s).lower()

    def speaker_name(self, speaker):
        try:
            return speaker.speaker.name
        except AttributeError:
            return u''

    def speaker_profile_url(self, speaker):
        try:
            return speaker.speaker.profile
        except AttributeError:
            return u''

    def speaker_image_url(self, speaker):
        try:
            return speaker.speaker.image
        except AttributeError:
            return u''

    def markdown(self, text, level_offset=3):
        html = markdown2.markdown(unicode(text))
        root = lxml.html.fromstring(html)
        for node in root.xpath('//*'):
            if node.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                h_name = node.tag
                h_level = int(h_name[1:])
                node.tag = 'h{}'.format(h_level + level_offset)

        # change anchor markup
        for node in root.xpath('//a'):
            href = node.attrib['href']
            node.tag = 'span'
            del node.attrib['href']
            node.attrib['class'] = 'link-text'
            new_link = Element('a')
            new_link.text = href
            new_link.attrib['href'] = href
            node.insert(0, new_link)




        return lxml.html.tostring(root, encoding=unicode)
