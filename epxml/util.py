import csv
from lxml import objectify
from lxml.etree import tostring
from lxml.etree import fromstring
from lxml.etree import Element


def get_entries(xml_in, xpath_filter):

    entries = list()

    # fix this
    id2title = dict()
    with open('msg.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            id2title[row[0]] = row[1]

    with open(xml_in, 'rb') as fp:
        xml = fp.read()

    root = fromstring(xml)
    for num, entry in enumerate(root.xpath(xpath_filter)):
        title = Element('title')
        title.text = id2title[entry.attrib['id']]
        entry.append(title)
        entry_d = objectify.fromstring(tostring(entry))
        entries.append(entry_d)
    return entries
