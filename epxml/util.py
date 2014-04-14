import csv
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
